#!/usr/bin/env python3
"""Grille de notation à l'aveugle des 12 questions de référence, à partir de deux passes de scripts/duel-modeles.py.

Usage :
  python3 scripts/grille-notation.py docs/evaluation/2026-10-27-claude-sonnet-5-5.json docs/evaluation/2026-10-27-gemini-4-argon.json

Écrit docs/evaluation/{date}-grille-notation.md (réponses « A » et « B », tirées au hasard par question) et
docs/evaluation/{date}-grille-cle.json (quel modèle est A ou B) : n'ouvrir la clé qu'après la notation.
"""
import json
import os
import random
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRITERIA = os.path.expanduser("~/Desktop/a-reprendre-odoo/jeux-de-test/i5-jeu-evaluation.md")
ROWS = ["Indispensable", "Erreurs à éviter", "Complète", "Partielle", "Incorrecte"]


def criteria_by_question():
    text = open(CRITERIA, encoding="utf-8").read()
    out = {}
    for block in re.split(r"\n## ", text)[1:]:
        m = re.match(r"(Q\d+) — (.+)", block)
        if not m:
            continue
        rows = dict(re.findall(r"^\| ([^|]+?) \| (.+) \|$", block, re.M))
        out[m.group(1)] = {"titre": m.group(2).strip(), **{k: rows.get(k, "—") for k in ROWS}}
    return out


def render_answer(r):
    a = r.get("reponse")
    if not a:
        return f"_Pas de réponse : {r.get('erreur')}_"
    mark = lambda i: "✅" if i["statut"] == "Documenté" else "⚠️"
    lines = [f"**Statut : {a['statut']}** · couverture {a['couverture']}", "", f"{mark(a['resume'])} {a['resume']['texte']}"]
    for title, key in (("Prérequis", "prerequis"), ("Étapes", "etapes"), ("Attention", "avertissements")):
        if a[key]:
            lines += ["", f"_{title}_"]
            for k, i in enumerate(a[key], 1):
                head = f"**{i['titre']}** — " if i.get("titre") else ""
                prefix = f"{k}." if key == "etapes" else "-"
                lines.append(f"{prefix} {mark(i)} {head}{i['texte']}")
    for title, key in (("Pistes à tester", "pistes"), ("Non couvert", "nonCouvert")):
        if a[key]:
            lines += ["", f"_{title}_"] + [f"- {p}" for p in a[key]]
    lines += ["", "_Sources :_ " + " · ".join(f"[{s['n']}] {s['url'].split('/20.0/')[-1]}" for s in a["sources"])]
    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    runs = [json.load(open(p, encoding="utf-8")) for p in sys.argv[1:]]
    by_model = {run["modele"]: {r["id"]: r for r in run["resultats"] if r["jeu"] == "i5"} for run in runs}
    models = list(by_model)
    crit = criteria_by_question()
    rng = random.Random()

    key, parts = {}, [
        f"# Grille de notation — duel {date.today().strftime('%d/%m/%Y')}",
        "",
        "Pour chaque question, note **A** et **B** : `Complète`, `Partielle` ou `Incorrecte` (définitions sous chaque question).",
        "Remplace `___` par ta note. Les modèles sont masqués : la clé est dans `*-grille-cle.json`, à ouvrir après.",
        "",
        "| Question | A | B |",
        "|---|---|---|",
    ]
    ids = sorted(crit, key=lambda q: int(q[1:]))
    parts += [f"| {q} | ___ | ___ |" for q in ids]
    for q in ids:
        order = models[:]
        rng.shuffle(order)
        key[q] = {"A": order[0], "B": order[1]}
        c = crit[q]
        question = next((by_model[m][q]["question"] for m in models if q in by_model[m]), "")
        parts += ["", "---", "", f"## {q} — {c['titre']}", "", f"> {question}", "",
                  f"**Indispensable** : {c['Indispensable']}", "", f"**Erreurs à éviter** : {c['Erreurs à éviter']}", "",
                  f"**Complète** : {c['Complète']} · **Partielle** : {c['Partielle']} · **Incorrecte** : {c['Incorrecte']}"]
        for label in ("A", "B"):
            r = by_model[key[q][label]].get(q, {"erreur": "question absente de la passe"})
            parts += ["", f"### Réponse {label}", "", render_answer(r), "", f"**Note {label} : ___**"]

    out_dir = os.path.join(ROOT, "docs", "evaluation")
    stem = os.path.join(out_dir, f"{date.today().isoformat()}-grille")
    with open(f"{stem}-notation.md", "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n")
    with open(f"{stem}-cle.json", "w", encoding="utf-8") as f:
        json.dump(key, f, ensure_ascii=False, indent=2)
    print(f"→ {os.path.relpath(stem, ROOT)}-notation.md\n→ {os.path.relpath(stem, ROOT)}-cle.json (à ouvrir après la notation)")


if __name__ == "__main__":
    main()
