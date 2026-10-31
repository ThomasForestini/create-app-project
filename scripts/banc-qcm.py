#!/usr/bin/env python3
"""Banc QCM : rejoue les images de docs/evaluation/qcm/img sur le webhook odoo-qcm et compare au corrigé.

Usage :
  python3 scripts/banc-qcm.py                       # 30 images neutres + 5 photos
  python3 scripts/banc-qcm.py --limit 5             # passe d'essai sur les 5 premières images
  python3 scripts/banc-qcm.py --ids Q04,photo-02

Écrit docs/evaluation/{date}-qcm.json (ou {date}-qcm-essai-{HHMM}.json avec --limit / --ids) et affiche un résumé :
taux de bonnes réponses (corrigé validé), « Documenté » faux, lecture correcte, latence et coût moyens.
Les photos n'ont pas de corrigé : elles comptent pour la lecture (lisible attendu) et la latence.
L'URL et le jeton sont lus dans .env (ODOO_WEBHOOK_URL avec odoo-question remplacé par odoo-qcm, ODOO_WEBHOOK_TOKEN).
"""
import argparse
import base64
import difflib
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QCM = os.path.join(ROOT, "docs", "evaluation", "qcm")
IMG = os.path.join(QCM, "img")
MAX_BYTES = 3_500_000  # l'API Anthropic refuse les images de plus de 5 Mo en base64 (≈ 3,75 Mo bruts)
PHOTOS_ILLISIBLES = {"photo-02"}  # de biais, énoncé coupé


def load_env(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


def image_base64(path):
    """Base64 de l'image, réduite avec sips (macOS) si elle dépasse la limite de l'API."""
    if os.path.getsize(path) > MAX_BYTES:
        with tempfile.TemporaryDirectory() as tmp:
            small = os.path.join(tmp, "small.jpg")
            subprocess.run(["sips", "-Z", "2000", "-s", "format", "jpeg", path, "--out", small],
                           check=True, capture_output=True)
            with open(small, "rb") as f:
                return base64.b64encode(f.read()).decode("ascii"), "image/jpeg"
    mime = "image/png" if path.endswith(".png") else "image/jpeg"
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii"), mime


def ask(url, token, path, timeout):
    data, mime = image_base64(path)
    body = json.dumps({"image_base64": data, "mime_type": mime}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-Odoo-Token": token})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode("utf-8"))


def similarity(a, b):
    norm = lambda s: " ".join((s or "").lower().split())
    return round(difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(), 3)


def run_one(code, path, pool, corrige, args, url, token):
    started = time.time()
    answer, error = None, None
    for attempt in range(2):  # un second essai si le webhook renvoie une erreur (API saturée, délai dépassé)
        try:
            answer = ask(url, token, path, args.timeout)
            error = None
            break
        except (OSError, json.JSONDecodeError) as e:
            error = f"{type(e).__name__}: {getattr(e, 'code', '')} {e}".strip()
    latency_ms = round((time.time() - started) * 1000)
    a = answer or {}

    q, c = pool.get(code), corrige.get(code)
    expected_readable = code not in PHOTOS_ILLISIBLES
    if q:  # image neutre : la lecture doit retrouver l'énoncé et le nombre de choix du pool
        sim = similarity(a.get("question_lue"), q["question"])
        reading_ok = bool(a.get("lisible")) and sim >= 0.9 and len(a.get("choix") or []) == len(q["choix"])
    else:  # photo : seul le verdict lisible / illisible est attendu
        sim = None
        reading_ok = bool(a.get("lisible")) == expected_readable
    given = sorted(a.get("bonnes_reponses") or [])
    correct = (given == sorted(c["bonnes_reponses"])) if c else None

    result = {
        "code": code,
        "image": os.path.relpath(path, ROOT),
        "id": q["id"] if q else None,
        "module": q["module"] if q else None,
        "attendues": sorted(c["bonnes_reponses"]) if c else None,
        "donnees": given,
        "correcte": correct,
        "statut": a.get("statut"),
        "statutReponse": (a.get("resume") or {}).get("statut"),
        "lisible": a.get("lisible"),
        "lisibleAttendu": expected_readable,
        "similariteLecture": sim,
        "lectureCorrecte": None if error else reading_ok,
        "ecartVersion": a.get("ecart_version"),
        "ecartV19V20Corrige": c["ecart_v19_v20"] if c else None,
        "coutUsd": (a.get("cout") or {}).get("usd"),
        "latenceMs": latency_ms,
        "erreur": error,
        "reponse": answer,
    }
    if error:
        mark = "ERREUR"
    elif correct is None:
        mark = f"lisible {a.get('lisible')} (attendu {expected_readable})"
    else:
        mark = f"{'OK ' if correct else 'FAUX'} {''.join(given) or '-':<3} attendu {''.join(c['bonnes_reponses']):<3} {result['statut']}"
    print(f"  {code:<9} {mark}  {latency_ms / 1000:.0f} s", flush=True)
    return result


def summarize(results):
    ok = [r for r in results if not r["erreur"]]
    graded = [r for r in ok if r["correcte"] is not None]
    costs = [r["coutUsd"] for r in ok if r["coutUsd"] is not None]
    latencies = [r["latenceMs"] for r in ok]
    return {
        "images": len(results),
        "erreurs": len(results) - len(ok),
        "bonnesReponses": f"{sum(r['correcte'] for r in graded)}/{len(graded)}",
        "tauxBonnesReponses": round(sum(r["correcte"] for r in graded) / len(graded), 3) if graded else None,
        "documenteFaux": sum(1 for r in graded if not r["correcte"] and r["statut"] == "Documenté"),
        "reponseDocumenteeFausse": sum(1 for r in graded if not r["correcte"] and r["statutReponse"] == "Documenté"),
        "lectureCorrecte": f"{sum(bool(r['lectureCorrecte']) for r in ok)}/{len(ok)}",
        "statuts": dict(Counter(r["statut"] for r in ok)),
        "coutMoyenUsd": round(statistics.mean(costs), 5) if costs else None,
        "coutTotalUsd": round(sum(costs), 4) if costs else None,
        "latenceMoyenneS": round(statistics.mean(latencies) / 1000, 1) if latencies else None,
        "latenceMaxS": round(max(latencies) / 1000, 1) if latencies else None,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--limit", type=int, help="nombre d'images (passe d'essai)")
    p.add_argument("--ids", help="codes séparés par des virgules (ex. Q04,photo-02)")
    p.add_argument("--concurrency", type=int, default=3)
    p.add_argument("--timeout", type=int, default=180, help="délai par image, en secondes")
    args = p.parse_args()

    env = load_env(os.path.join(ROOT, ".env"))
    base, token = env.get("ODOO_WEBHOOK_URL"), env.get("ODOO_WEBHOOK_TOKEN")
    if not base or not token:
        sys.exit("ODOO_WEBHOOK_URL et ODOO_WEBHOOK_TOKEN doivent être définis dans .env")
    url = base.rsplit("/", 1)[0] + "/odoo-qcm"

    with open(os.path.join(QCM, "pool.json"), encoding="utf-8") as f:
        pool = {q["code_banc"]: q for q in json.load(f)["questions"] if q.get("code_banc")}
    with open(os.path.join(QCM, "corrige.json"), encoding="utf-8") as f:
        corrige = {q["code_banc"]: q for q in json.load(f)["questions"]}
    not_validated = [code for code, c in corrige.items() if not c["valide"]]
    if not_validated:
        print(f"Attention : corrigé non validé pour {', '.join(not_validated)}")

    images = sorted(f for f in os.listdir(IMG) if f.lower().endswith((".png", ".jpg", ".jpeg")))
    jobs = [(os.path.splitext(f)[0], os.path.join(IMG, f)) for f in images]
    if args.ids:
        wanted = set(args.ids.split(","))
        jobs = [j for j in jobs if j[0] in wanted]
    if args.limit:
        jobs = jobs[: args.limit]
    if not jobs:
        sys.exit("Aucune image sélectionnée.")

    print(f"{len(jobs)} image(s), {args.concurrency} en parallèle")
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        results = list(executor.map(lambda j: run_one(j[0], j[1], pool, corrige, args, url, token), jobs))

    summary = summarize(results)
    # Les passes d'essai portent l'heure : plusieurs essais le même jour ne s'écrasent pas.
    suffix = f"-essai-{time.strftime('%H%M')}" if (args.limit or args.ids) else ""
    out = os.path.join(ROOT, "docs", "evaluation", f"{date.today().isoformat()}-qcm{suffix}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"date": date.today().isoformat(), "resume": summary, "resultats": results},
                  f, ensure_ascii=False, indent=2)

    print("\nRésumé")
    for key, value in summary.items():
        print(f"  {key:<24} {value}")
    print(f"\n→ {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
