#!/usr/bin/env python3
"""Grille de relecture du corrigé QCM, à partir de pool.json et corrige.json.

Usage : python3 scripts/qcm-grille.py
Sortie : docs/evaluation/qcm/grille-relecture.md (à relancer après chaque modification du corrigé)

Le choix de Rémy est affiché pour information : c'est ici une aide à la relecture humaine,
jamais un corrigé, et il n'est jamais transmis au modèle.
"""
import json
import os

QCM = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "evaluation", "qcm")
LETTRES = "ABCDEF"
COULEUR = {"vert": "vert (sa réponse)", "orange": "orange (erreur probable)", "bleu": "bleu (réponse alternative)"}


def main():
    pool = {q["code_banc"]: q for q in json.load(open(os.path.join(QCM, "pool.json"), encoding="utf-8"))["questions"]
            if q["echantillon"]}
    corrige = json.load(open(os.path.join(QCM, "corrige.json"), encoding="utf-8"))["questions"]

    a_trancher = [c["code_banc"] for c in corrige if c["methode"] == "runbot" or c["confiance"] != "haute"]
    valides = sum(c["valide"] for c in corrige)
    lignes = [
        "# Grille de relecture — corrigé QCM (30 questions)",
        "",
        f"> Générée par `scripts/qcm-grille.py`. Validées : **{valides}/30**.",
        "> Pour chaque question : vérifier la réponse proposée (doc v20 ou runbot.odoo.com, admin/admin), "
        "corriger `bonnes_reponses` dans `corrige.json` si besoin, puis passer `valide` à `true`.",
        "",
        f"**À vérifier en priorité sur runbot ou à confiance moyenne/faible ({len(a_trancher)})** : {', '.join(a_trancher)}",
        "",
    ]
    for c in corrige:
        q = pool[c["code_banc"]]
        proposees = c["bonnes_reponses"]
        remy = [LETTRES[i] for i, ch in enumerate(q["choix"]) if ch["couleur_remy"] == "vert"]
        lignes += [f"## {c['code_banc']} — {q['module']} ({q['id']}, p. {q['page']})", "", f"**{q['question']}**", ""]
        for i, ch in enumerate(q["choix"]):
            marque = " ✅" if LETTRES[i] in proposees else ""
            lignes.append(f"- {LETTRES[i]}. {ch['texte']}{marque}")
        lignes += [
            "",
            f"- Proposé : **{', '.join(proposees) or 'à trancher'}** · méthode {c['methode']} · confiance {c['confiance']}"
            + (" · ⚠️ écart v19/v20" if c["ecart_v19_v20"] else ""),
            f"- Source : {c['url_doc_v20']}",
            f"- Note : {c['note']}",
        ]
        couleurs = [f"{LETTRES[i]} {COULEUR[ch['couleur_remy']]}" for i, ch in enumerate(q["choix"]) if ch["couleur_remy"]]
        if couleurs:
            desaccord = " · **≠ proposé**" if remy and sorted(remy) != sorted(proposees) else ""
            lignes.append(f"- Rémy (info) : {', '.join(couleurs)}{desaccord}")
        lignes += [f"- [{'x' if c['valide'] else ' '}] Validé par Thomas", ""]
    sortie = os.path.join(QCM, "grille-relecture.md")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    print(f"{sortie} — {valides}/30 validées, {len(a_trancher)} à vérifier en priorité")


if __name__ == "__main__":
    main()
