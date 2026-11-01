#!/usr/bin/env python3
"""Banc plan : envoie les PDF de docs/evaluation/plan au webhook odoo-plan et pré-remplit la notation.

Usage :
  python3 scripts/banc-plan.py                      # MTO + Thermo
  python3 scripts/banc-plan.py --scenarios mto      # un seul scénario
  python3 scripts/banc-plan.py --scenarios maigre   # sans grille : plan, latence et coût seulement

Écrit docs/evaluation/{date}-plan.json (plan, latence, coût par appel, par scénario ; une nouvelle passe
remplace le scénario rejoué et garde les autres) et docs/evaluation/{date}-plan-notation.md : pour chaque
élément de la grille, trouvé ou absent, avec les étapes, statuts et sources du plan. La note finale
(Complet / Partiel / Incorrect) reste à porter à la main.
L'URL et le jeton sont lus dans .env (ODOO_WEBHOOK_URL avec odoo-question remplacé par odoo-plan, ODOO_WEBHOOK_TOKEN).
"""
import argparse
import base64
import difflib
import json
import math
import os
import re
import sys
import time
import urllib.request
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(ROOT, "docs", "evaluation", "plan")
EVAL = os.path.join(ROOT, "docs", "evaluation")
SCENARIOS = {
    "mto": ("mto.pdf", "grille-mto.md"),
    "thermo": ("thermo.pdf", "grille-thermo.md"),
    "maigre": ("maigre.pdf", None),
}


def load_env(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


def ask(url, token, pdf_path, timeout):
    with open(pdf_path, "rb") as f:
        body = json.dumps({"pdf": base64.b64encode(f.read()).decode("ascii")}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-Odoo-Token": token})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode("utf-8"))


def norm(s):
    return " ".join(re.sub(r"[*_`]", "", s or "").lower().split())


def parse_grid(path):
    """Éléments (# | Élément | Source attendue), questions attendues et erreurs à éviter de la grille."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    sections = dict(re.findall(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M))
    section = lambda prefix: next((v for k, v in sections.items() if k.startswith(prefix)), "")
    elements = []
    for line in section("Attendu").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and re.fullmatch(r"[AT]\d+", cells[0]):
            elements.append({"id": cells[0], "texte": cells[1], "source": cells[2],
                             "libelles": re.findall(r"\*\*(.+?)\*\*", cells[1]),
                             "pages": [s.split(" §")[0].strip() for s in re.split(r"[;,]| ou ", cells[2])
                                       if re.fullmatch(r"[a-z][a-z0-9_]+", s.split(" §")[0].strip())]})
    bullets = lambda s: [l[2:].strip() for l in s.splitlines() if l.startswith("- ")]
    return elements, bullets(section("Questions attendues")), bullets(section("Erreurs à éviter"))


def step_text(e):
    return norm(" ".join([e["action"], e["menu"], e["champ"], e["valeur"], e.get("detail", "")]))


def match_element(el, plan):
    """Étapes (ou tests pour T*) qui contiennent au moins la moitié des libellés en gras de l'élément."""
    labels = [norm(l) for l in el["libelles"]]
    if not labels:
        return None  # rien à chercher automatiquement : à juger à la main
    need = max(1, math.ceil(len(labels) / 2))
    if el["id"].startswith("T"):
        hits = [t for t in plan["tests"] if sum(l in norm(t["titre"] + " " + " ".join(t["etapes"])) for l in labels) >= need]
        return [{"test": t["titre"], "statut": "test (non contrôlé)", "sources": t["pages"]} for t in hits]
    hits = [e for e in plan["etapes"] if sum(l in step_text(e) for l in labels) >= need]
    return [{"etape": e["n"], "statut": e["statut"], "sources": e["source"]} for e in hits]


def page_found(pages, hits):
    urls = " ".join(s for h in hits for s in h["sources"])
    return any(f"/{p}.html" in urls for p in pages)


def notation(name, plan, grid_path, run):
    elements, questions, errors = parse_grid(grid_path)
    lines = [f"## {name.upper()} — {plan.get('client', '?')}", "",
             f"Latence {run['latenceMs'] / 1000:.0f} s · coût {run['coutUsd']} USD · étapes : "
             + ", ".join(f"{v} {k}" for k, v in plan["parStatut"].items()) + "", "",
             "| # | Élément attendu | Trouvé | Étapes / tests du plan (statut) | Page attendue citée | Note |",
             "|---|---|---|---|---|---|"]
    for el in elements:
        hits = match_element(el, plan)
        if hits is None:
            found, where, page = "à juger", "—", "—"
        else:
            found = "oui" if hits else "absent"
            where = "<br>".join(f"{h.get('etape', h.get('test'))} ({h['statut']})" for h in hits) or "—"
            page = ("oui" if page_found(el["pages"], hits) else "non") if el["pages"] and hits else "—"
        lines.append(f"| {el['id']} | {el['texte']} | {found} | {where} | {page} | |")
    lines += ["", "**Questions attendues** (question du plan la plus proche, à confirmer)", ""]
    plan_q = [q["question"] for q in plan["questions_ouvertes"]]
    for q in questions:
        best = max(plan_q, key=lambda p: difflib.SequenceMatcher(None, norm(q), norm(p)).ratio(), default="")
        lines.append(f"- {q}\n  → {best or '(aucune question)'}")
    lines += ["", "**Erreurs à éviter** (libellés en gras cherchés dans les étapes)", ""]
    for err in errors:
        labels = [norm(l) for l in re.findall(r"\*\*(.+?)\*\*", err)]
        hits = [e["n"] for e in plan["etapes"] if any(l in step_text(e) for l in labels)] if labels else None
        flag = "à juger" if hits is None else (f"étapes {hits} à examiner" if hits else "non détectée")
        lines.append(f"- {err} → {flag}")
    lines += ["", f"Données inventées : à juger (données client extraites : "
              + "; ".join(f"{d['donnee']} = {d['valeur']}" for d in plan["donnees_client"]) + ")",
              "", "**Note du scénario** : à porter (Complet / Partiel / Incorrect)", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenarios", default="mto,thermo", help="liste parmi " + ", ".join(SCENARIOS))
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    names = [s.strip() for s in args.scenarios.split(",") if s.strip()]
    unknown = [n for n in names if n not in SCENARIOS]
    if unknown:
        sys.exit(f"Scénario inconnu : {', '.join(unknown)}")

    env = load_env(os.path.join(ROOT, ".env"))
    url = env["ODOO_WEBHOOK_URL"].replace("odoo-question", "odoo-plan")
    token = env["ODOO_WEBHOOK_TOKEN"]

    today = date.today().isoformat()
    out_json = os.path.join(EVAL, f"{today}-plan.json")
    out_md = os.path.join(EVAL, f"{today}-plan-notation.md")
    results = {}
    if os.path.exists(out_json):
        with open(out_json, encoding="utf-8") as f:
            results = json.load(f).get("scenarios", {})

    for name in names:
        pdf, grid = SCENARIOS[name]
        print(f"{name} : envoi de {pdf}…", flush=True)
        started = time.time()
        plan, error = None, None
        try:
            plan = ask(url, token, os.path.join(PLAN, pdf), args.timeout)
        except Exception as exc:  # noqa: BLE001 — l'échec est consigné dans le résultat
            error = str(exc)
        latence = round((time.time() - started) * 1000)
        results[name] = {
            "pdf": pdf, "grille": grid, "date": datetime.now().isoformat(timespec="seconds"),
            "latenceMs": latence, "coutUsd": plan["cout"]["usd"] if plan else None,
            "coutParAppel": plan["cout"]["details"] if plan else [], "erreur": error, "plan": plan,
        }
        print(f"  {'erreur : ' + error if error else 'ok'} · {latence / 1000:.0f} s · "
              f"{results[name]['coutUsd']} USD", flush=True)

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"date": today, "scenarios": results}, f, ensure_ascii=False, indent=2)

    parts = [f"# Notation des plans — {today}", "",
             "Feuille pré-remplie par `scripts/banc-plan.py` : « trouvé » = une même étape contient au moins la moitié "
             "des libellés en gras de l'élément. À relire élément par élément avant de noter.", ""]
    for name, run in results.items():
        if run["plan"] and run["grille"]:
            parts.append(notation(name, run["plan"], os.path.join(PLAN, run["grille"]), run))
        elif run["plan"]:
            parts += [f"## {name.upper()} — sans grille", "",
                      f"{len(run['plan']['besoins'])} besoins, {len(run['plan']['questions_ouvertes'])} questions, "
                      f"{len(run['plan']['etapes'])} étapes · {run['latenceMs'] / 1000:.0f} s · {run['coutUsd']} USD", ""]
        else:
            parts += [f"## {name.upper()} — échec : {run['erreur']}", ""]
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Écrit {os.path.relpath(out_json, ROOT)} et {os.path.relpath(out_md, ROOT)}")


if __name__ == "__main__":
    main()
