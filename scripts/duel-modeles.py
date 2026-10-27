#!/usr/bin/env python3
"""Banc de mesure : rejoue les jeux de test sur le webhook odoo-question pour un modèle de rédaction.

Usage :
  python3 scripts/duel-modeles.py --model claude-sonnet-5-5             # 106 questions doc + 12 de référence
  python3 scripts/duel-modeles.py --model gemini-3.8-flash --limit 5    # passe d'essai
  python3 scripts/duel-modeles.py --model claude-sonnet-5-5 --set i5 --ids Q1,Q3

Écrit docs/evaluation/{date}-{modèle}.json (ou {date}-{modèle}-essai-{HHMM}.json avec --limit / --ids) et affiche un résumé :
rappel des pages attendues parmi les sources citées, répartition des statuts, coût et latence moyens.
L'URL et le jeton du webhook sont lus dans .env (ODOO_WEBHOOK_URL, ODOO_WEBHOOK_TOKEN), jamais dans ce fichier.
"""
import argparse
import json
import os
import statistics
import sys
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SETS_DIR = os.path.expanduser("~/Desktop/a-reprendre-odoo/jeux-de-test")
SETS = {"doc": "questions-doc.json", "i5": "i5-questions.json"}
DOCS_PREFIX = "https://www.odoo.com/documentation/20.0/"


def load_env(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


def page_key(url_or_path):
    """Clé de page comparable : « finance/accounting/bank » pour une URL, un chemin ou une ancre de la doc v20."""
    key = url_or_path.split("#")[0]
    if key.startswith(DOCS_PREFIX):
        key = key[len(DOCS_PREFIX):]
    if key.endswith(".html"):
        key = key[: -len(".html")]
    if key.startswith("applications/"):
        key = key[len("applications/"):]
    return key.strip("/")


def ask(url, token, question, model, timeout):
    body = json.dumps({"question": question, "model": model}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-Odoo-Token": token})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode("utf-8"))


def run_one(q, set_name, args, url, token):
    started = time.time()
    answer, error = None, None
    for attempt in range(2):  # un second essai si le webhook renvoie une erreur (API saturée, délai dépassé)
        try:
            answer = ask(url, token, q["question"], args.model, args.timeout)
            error = None
            break
        # OSError couvre URLError, HTTPError et socket.timeout (qui n'hérite pas de TimeoutError avant Python 3.10).
        except (OSError, json.JSONDecodeError) as e:
            error = f"{type(e).__name__}: {getattr(e, 'code', '')} {e}".strip()
    latency_ms = round((time.time() - started) * 1000)

    expected = [page_key(e) for e in q.get("expected", [])]
    cited = sorted({page_key(s["url"]) for s in (answer or {}).get("sources", [])})
    found = [e for e in expected if e in cited]
    result = {
        "id": q["id"],
        "jeu": set_name,
        "version": q.get("version"),
        "question": q["question"],
        "attendues": expected,
        "pagesCitees": cited,
        "trouvees": found,
        "rappel": round(len(found) / len(expected), 3) if expected else None,
        "statut": (answer or {}).get("statut"),
        "couverture": (answer or {}).get("couverture"),
        "coutUsd": ((answer or {}).get("cout") or {}).get("usd"),
        "dureeServeurMs": (answer or {}).get("dureeMs"),
        "latenceMs": latency_ms,
        "erreur": error,
        "reponse": answer,
    }
    mark = "ERREUR" if error else f"{result['statut']:<11} rappel {result['rappel']}"
    print(f"  {q['id']:<5} {mark}  {latency_ms / 1000:.0f} s", flush=True)
    return result


def summarize(results):
    ok = [r for r in results if not r["erreur"]]
    doc = [r for r in ok if r["jeu"] == "doc" and r["rappel"] is not None]
    costs = [r["coutUsd"] for r in ok if r["coutUsd"] is not None]
    latencies = [r["latenceMs"] for r in ok]
    return {
        "questions": len(results),
        "erreurs": len(results) - len(ok),
        "rappelDoc": round(statistics.mean(r["rappel"] for r in doc), 3) if doc else None,
        "questionsDocCompletes": f"{sum(r['rappel'] == 1 for r in doc)}/{len(doc)}",
        "rappelI5": round(statistics.mean(r["rappel"] for r in ok if r["jeu"] == "i5" and r["rappel"] is not None), 3)
        if any(r["jeu"] == "i5" for r in ok) else None,
        "statuts": dict(Counter(r["statut"] for r in ok)),
        "coutMoyenUsd": round(statistics.mean(costs), 5) if costs else None,
        "coutTotalUsd": round(sum(costs), 4) if costs else None,
        "latenceMoyenneS": round(statistics.mean(latencies) / 1000, 1) if latencies else None,
        "latenceMaxS": round(max(latencies) / 1000, 1) if latencies else None,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True, help="modèle de rédaction (ex. claude-sonnet-5-5, gemini-3.8-flash)")
    p.add_argument("--set", choices=["doc", "i5", "all"], default="all")
    p.add_argument("--limit", type=int, help="nombre de questions par jeu (passe d'essai)")
    p.add_argument("--ids", help="identifiants séparés par des virgules (ex. D001,Q3)")
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--timeout", type=int, default=180, help="délai par question, en secondes")
    p.add_argument("--sets-dir", default=DEFAULT_SETS_DIR)
    args = p.parse_args()

    env = load_env(os.path.join(ROOT, ".env"))
    url, token = env.get("ODOO_WEBHOOK_URL"), env.get("ODOO_WEBHOOK_TOKEN")
    if not url or not token:
        sys.exit("ODOO_WEBHOOK_URL et ODOO_WEBHOOK_TOKEN doivent être définis dans .env")

    wanted_ids = set(args.ids.split(",")) if args.ids else None
    jobs = []
    for set_name in (["doc", "i5"] if args.set == "all" else [args.set]):
        with open(os.path.join(args.sets_dir, SETS[set_name]), encoding="utf-8") as f:
            questions = json.load(f)["questions"]
        if wanted_ids:
            questions = [q for q in questions if q["id"] in wanted_ids]
        if args.limit:
            questions = questions[: args.limit]
        jobs += [(q, set_name) for q in questions]
    if not jobs:
        sys.exit("Aucune question sélectionnée.")

    print(f"{len(jobs)} question(s), modèle {args.model}, {args.concurrency} en parallèle")
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        results = list(pool.map(lambda job: run_one(job[0], job[1], args, url, token), jobs))

    summary = summarize(results)
    # Les passes d'essai portent l'heure : plusieurs essais le même jour ne s'écrasent pas.
    suffix = f"-essai-{time.strftime('%H%M')}" if (args.limit or args.ids) else ""
    out_dir = os.path.join(ROOT, "docs", "evaluation")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{date.today().isoformat()}-{args.model}{suffix}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"modele": args.model, "date": date.today().isoformat(), "jeu": args.set,
                   "resume": summary, "resultats": results}, f, ensure_ascii=False, indent=2)

    print("\nRésumé")
    for key, value in summary.items():
        print(f"  {key:<22} {value}")
    print(f"\n→ {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
