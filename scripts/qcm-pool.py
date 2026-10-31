#!/usr/bin/env python3
"""Extrait le pool de questions QCM du PDF de certification Odoo 19 (mail de Rémy Claes).

Usage : python scripts/qcm-pool.py ["~/Downloads/Odoo 19 certification.pdf"]
Dépendance : pymupdf (pip install pymupdf).
Sortie : docs/evaluation/qcm/pool.json

Les couleurs de Rémy (vert / orange / bleu) sont gardées en métadonnée seulement :
elles ne sont jamais un corrigé et ne doivent jamais être montrées au modèle.
"""
import json
import os
import random
import re
import sys
from collections import Counter

import fitz

PDF = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/Downloads/Odoo 19 certification.pdf")
SORTIE = os.path.join(os.path.dirname(__file__), "..", "docs", "evaluation", "qcm", "pool.json")
COULEURS = {0x216E4E: "vert", 0xE06C00: "orange", 0x1558BC: "bleu"}
TAILLE_ECHANTILLON = 30
GRAINE = 20261028
# Artefacts du PDF source : formules LaTeX ($...$) mal converties dans deux énoncés Purchase
MATH = re.compile(r"\$([^$]*)\$")
NUMERO_PARASITE = re.compile(r" 2[5-7]\d$")  # numéros de ligne collés aux choix Purchase (259-276)
PARASITES = [" By changing the attribute display type in the Style tab"]  # fragment collé dans un énoncé Knowledge
INCOMPLETES = {"Multiple = ? ft": "énoncé incomplet dans la source (valeur du multiple perdue)"}


def lignes(doc):
    """Lignes du corps du mail (hors en-têtes/pieds Gmail), avec un drapeau 'puce'."""
    for pno, page in enumerate(doc):
        puces = [d["rect"] for d in page.get_drawings()
                 if d.get("fill") and all(abs(c - v) < 0.02 for c, v in zip(d["fill"], (0.16, 0.16, 0.18)))
                 and d["rect"].width < 6]
        for bloc in page.get_text("dict")["blocks"]:
            for ligne in bloc.get("lines", []):
                spans = [s for s in ligne["spans"] if s["text"].strip()]
                if not spans or spans[0]["size"] < 9:
                    continue
                x0, y0, x1, y1 = ligne["bbox"]
                couleurs = Counter(COULEURS.get(s["color"]) for s in spans)
                yield {
                    "page": pno + 1,
                    "x": x0,
                    "texte": " ".join(s["text"].strip() for s in spans),
                    "font": spans[0]["font"],
                    "taille": spans[0]["size"],
                    "couleur": couleurs.most_common(1)[0][0],
                    "puce": any(y0 - 2 <= (r.y0 + r.y1) / 2 <= y1 + 2 and r.x1 < x0 for r in puces),
                }


def extraire(doc):
    questions, module, courante, debut = [], None, None, False
    for l in lignes(doc):
        if l["font"] == "SegoeUI-Bold":
            if not re.fullmatch(r"Question \d+", l["texte"]):  # intertitre parasite p.18
                module, debut = l["texte"], True
            continue
        if not debut:  # préambule du mail
            continue
        if l["font"].startswith("SegoeUI"):
            if courante is None or courante["choix"]:
                courante = {"module": module, "page": l["page"], "question": l["texte"], "choix": []}
                questions.append(courante)
            else:
                courante["question"] += " " + l["texte"]
        elif l["puce"]:
            courante["choix"].append({"texte": l["texte"], "couleur_remy": l["couleur"]})
        elif courante and courante["choix"]:
            courante["choix"][-1]["texte"] += " " + l["texte"]
        else:
            raise ValueError(f"Ligne non classée p.{l['page']} : {l['texte']!r}")
    for q in questions:
        if "\\geq" in q["question"] or "~ft" in q["question"]:
            t = q["question"].replace("\\$", "§").replace("Multiple $=$ ft", "Multiple = ? ft")
            t = MATH.sub(r"\1", t).replace("\\geq", "≥").replace("~", " ").replace("§", "$")
            q["question"] = re.sub(r"\s*([=≥])\s*", r" \1 ", t)
        for fragment in PARASITES:
            q["question"] = q["question"].replace(fragment, "")
        for c in q["choix"]:
            c["texte"] = NUMERO_PARASITE.sub("", c["texte"])
        q["remarque"] = next((r for motif, r in INCOMPLETES.items() if motif in q["question"]), None)
    # Doublon tronqué (même énoncé recopié sous l'intertitre parasite) : on garde la première occurrence
    uniques = []
    for q in questions:
        textes = [c["texte"] for c in q["choix"]]
        if not any(u["question"] == q["question"] and textes == [c["texte"] for c in u["choix"]][:len(textes)]
                   for u in uniques):
            uniques.append(q)
    return uniques


def main():
    questions = extraire(fitz.open(PDF))
    for i, q in enumerate(questions, 1):
        q["id"] = f"P{i:03d}"
        couleurs = {c["couleur_remy"] for c in q["choix"]} - {None}
        q["couleurs_remy"] = sorted(couleurs)
        q["echantillon"] = False

    # Échantillon : toutes les orange/bleu, puis complété au hasard (graine fixe) en répartissant par module
    obligatoires = [q for q in questions if {"orange", "bleu"} & set(q["couleurs_remy"])]
    rng = random.Random(GRAINE)
    reste = [q for q in questions if q not in obligatoires and not q["remarque"]]
    rng.shuffle(reste)
    choisies = list(obligatoires)
    while len(choisies) < TAILLE_ECHANTILLON and reste:
        par_module = Counter(q["module"] for q in choisies)
        reste.sort(key=lambda q: par_module[q["module"]])
        choisies.append(reste.pop(0))
    for q in choisies:
        q["echantillon"] = True
    for n, q in enumerate(sorted(choisies, key=lambda q: q["id"]), 1):
        q["code_banc"] = f"Q{n:02d}"

    pool = {
        "source": os.path.basename(PDF),
        "note": "couleur_remy = surlignage de Rémy Claes (vert = sa réponse, orange = erreur probable, "
                "bleu = réponse alternative). Métadonnée seulement : jamais un corrigé, jamais montrée au modèle.",
        "nb_questions": len(questions),
        "questions": [{k: q.get(k) for k in ("id", "code_banc", "echantillon", "module", "page", "question",
                                             "choix", "couleurs_remy", "remarque")} for q in questions],
    }
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, "w", encoding="utf-8") as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)
    print(f"{len(questions)} questions, {len(choisies)} en échantillon sur "
          f"{len({q['module'] for q in choisies})} modules ({len(obligatoires)} orange/bleu) → {SORTIE}")
    print("Par module :", dict(Counter(q["module"] for q in questions)))
    print("Échantillon :", dict(Counter(q["module"] for q in choisies)))


if __name__ == "__main__":
    main()
