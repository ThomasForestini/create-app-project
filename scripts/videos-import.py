#!/usr/bin/env python3
"""Import des vidéos Odoo Tutorials dans la bibliothèque pgvector.

Pour chaque vidéo de scripts/videos/liste-videos.json, envoi au webhook n8n video-import, qui produit la fiche,
calcule les embeddings (gemini-embedding-2) et enregistre la vidéo. Une vidéo déjà enregistrée est sautée (rejouable).
- mode gemini (par défaut) : Gemini regarde la vidéo YouTube côté Google (≈ 0,0043 USD par minute de vidéo, menus vus à l'écran) ;
- mode transcript : sous-titres YouTube récupérés depuis ce poste, fiche Haiku 5.5 (≈ 0,001 USD par vidéo), mais
  YouTube bloque l'adresse IP après une vingtaine de vidéos.

Usage :
  python3 scripts/videos-import.py --course "Inventory"   # pilote sur un cours
  python3 scripts/videos-import.py --limit 5               # 5 premières vidéos
  python3 scripts/videos-import.py --budget 25             # tout (hors doublons et développement), arrêt à 25 USD
  python3 scripts/videos-import.py --mode transcript       # fiches Haiku à partir des sous-titres

Avancement dans tmp/videos-etat.json (reprise après coupure). L'URL et le jeton sont lus dans .env
(ODOO_WEBHOOK_URL avec odoo-question remplacé par video-import, ODOO_WEBHOOK_TOKEN).
"""
import argparse
import json
import os
import time
import urllib.request
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, as_completed, wait

from youtube_transcript_api import YouTubeTranscriptApi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTE = os.path.join(ROOT, "scripts", "videos", "liste-videos.json")
ETAT = os.path.join(ROOT, "tmp", "videos-etat.json")
# Versions française et espagnole de cours déjà présents en anglais (doublons dans la recherche), et cours de
# développement Python, inutiles pour paramétrer.
EXCLUS = {"Odoo Academy - Comptabilité", "Odoo Academy - (e)-facturation", "Partner Bootcamp en español",
          "Smart Tutorial - Localización de Argentina", "Smart Tutorial - Localización de México",
          "Technical Training - Introduction to Development", "Technical Training"}
FENETRE_S = 120


def load_env(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v.strip().strip('"')
    return env


def transcript(api, video_id):
    """Sous-titres (anglais de préférence) regroupés en fenêtres de 2 minutes."""
    t = api.fetch(video_id, languages=["en", "fr", "es"])
    segments, cur = [], None
    for s in t:
        if cur is None or s.start - cur["start"] >= FENETRE_S:
            cur = {"start": s.start, "end": s.start + s.duration, "text": ""}
            segments.append(cur)
        cur["text"] = f"{cur['text']} {s.text.replace(chr(10), ' ')}".strip()
        cur["end"] = s.start + s.duration
    return t.language_code, segments


def send(url, token, payload, timeout=300):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "X-Odoo-Token": token})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read() or b"{}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--course", help="un seul cours (titre exact)")
    p.add_argument("--limit", type=int)
    p.add_argument("--concurrency", type=int, default=3)
    p.add_argument("--mode", choices=["gemini", "transcript"], default="gemini")
    p.add_argument("--budget", type=float, help="arrêt quand le coût de la passe atteint ce montant (USD)")
    args = p.parse_args()

    env = load_env(os.path.join(ROOT, ".env"))
    url = env["ODOO_WEBHOOK_URL"].replace("odoo-question", "video-import")
    token = env["ODOO_WEBHOOK_TOKEN"]
    videos = json.load(open(LISTE, encoding="utf-8"))["videos"]
    videos = [v for v in videos if (v["course"] == args.course if args.course else v["course"] not in EXCLUS)]
    os.makedirs(os.path.dirname(ETAT), exist_ok=True)
    etat = json.load(open(ETAT, encoding="utf-8")) if os.path.exists(ETAT) else {}
    todo = [v for v in videos if etat.get(v["id"], {}).get("statut") not in ("ok", "sans transcript")][: args.limit]
    print(f"{len(todo)} vidéo(s) à traiter sur {len(videos)}", flush=True)

    api = YouTubeTranscriptApi()
    usd, bloque = 0.0, 0

    def save():
        json.dump(etat, open(ETAT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    with ThreadPoolExecutor(args.concurrency) as pool:
        futures = {}
        for i, v in enumerate(todo, 1):
            if args.mode == "gemini":
                # Pas plus d'envois en attente que de requêtes en parallèle : le plafond reste respecté.
                while len(futures) >= args.concurrency:
                    for fut in wait(futures, return_when=FIRST_COMPLETED).done:
                        j, w = futures.pop(fut)
                        usd += report(fut, j, w, len(todo), etat)
                        save()
                if args.budget and usd >= args.budget:
                    print(f"Plafond de {args.budget:.2f} USD atteint : arrêt (relancer pour continuer).", flush=True)
                    break
                futures[pool.submit(send, url, token, v, 700)] = (i, v)
                continue
            # Transcripts récupérés un par un, avec une pause, pour ne pas être freiné par YouTube.
            try:
                lang, segments = transcript(api, v["id"])
                bloque = 0
            except Exception as e:  # noqa: BLE001 — sous-titres absents, vidéo privée, blocage YouTube
                name = type(e).__name__
                etat[v["id"]] = {"statut": "sans transcript" if name in ("TranscriptsDisabled", "NoTranscriptFound", "VideoUnavailable") else "erreur", "erreur": name}
                print(f"[{i}/{len(todo)}] {v['title']} : {name}", flush=True)
                save()
                if name in ("RequestBlocked", "IpBlocked"):
                    bloque += 1
                    if bloque >= 3:
                        # Arrêt après les envois déjà partis, pour noter leur résultat.
                        print("YouTube bloque les requêtes : arrêt après les envois en cours (relancer plus tard).", flush=True)
                        break
                    time.sleep(60)
                continue
            payload = {**v, "language": lang, "segments": segments}
            futures[pool.submit(send, url, token, payload)] = (i, v)
            time.sleep(1.5)
            # Résultats déjà arrivés.
            for fut in [f for f in futures if f.done()]:
                j, w = futures.pop(fut)
                usd += report(fut, j, w, len(todo), etat)
                save()
        for fut in as_completed(futures):
            j, w = futures[fut]
            usd += report(fut, j, w, len(todo), etat)
            save()
    ok = sum(1 for v in videos if etat.get(v["id"], {}).get("statut") == "ok")
    print(f"Terminé : {ok}/{len(videos)} vidéos en base · coût de cette passe ≈ {usd:.2f} USD")


def report(fut, i, v, total, etat):
    try:
        r = fut.result()
        etat[v["id"]] = {"statut": "ok", "passages": r.get("passages"), "usd": r.get("usd"), "deja": not r.get("ajoutee")}
        done = "déjà en base" if not r.get("ajoutee") else f"{r.get('passages')} passages"
        print(f"[{i}/{total}] {v['title']} : {done}", flush=True)
        return r.get("usd") or 0
    except Exception as e:  # noqa: BLE001
        etat[v["id"]] = {"statut": "erreur", "erreur": str(e)[:300]}
        print(f"[{i}/{total}] {v['title']} : échec n8n ({str(e)[:120]})", flush=True)
        return 0


if __name__ == "__main__":
    main()
