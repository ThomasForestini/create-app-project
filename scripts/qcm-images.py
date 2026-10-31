#!/usr/bin/env python3
"""Rend les 30 questions de l'échantillon en PNG neutres (texte noir sur fond blanc, aucun surlignage).

Usage : python scripts/qcm-images.py
Dépendance : pillow (pip install pillow).
Sortie : docs/evaluation/qcm/img/Q01.png .. Q30.png

Les choix sont précédés d'un bouton radio vide, comme à l'écran de l'examen : aucune lettre,
aucune couleur, rien qui trahisse la réponse de Rémy.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

QCM = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "evaluation", "qcm")
POLICE = "/System/Library/Fonts/Supplemental/Arial.ttf"
POLICE_GRAS = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
LARGEUR, MARGE, RETRAIT = 1200, 60, 60


def couper(draw, texte, police, largeur):
    lignes, courante = [], ""
    for mot in texte.split():
        essai = f"{courante} {mot}".strip()
        if draw.textlength(essai, font=police) <= largeur:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    return lignes + [courante]


def rendre(q, chemin):
    gras, normal = ImageFont.truetype(POLICE_GRAS, 30), ImageFont.truetype(POLICE, 28)
    brouillon = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    enonce = couper(brouillon, q["question"], gras, LARGEUR - 2 * MARGE)
    choix = [couper(brouillon, c["texte"], normal, LARGEUR - 2 * MARGE - RETRAIT) for c in q["choix"]]
    hauteur = MARGE * 2 + len(enonce) * 42 + 30 + sum(len(c) * 38 + 28 for c in choix)

    img = Image.new("RGB", (LARGEUR, hauteur), "white")
    draw = ImageDraw.Draw(img)
    y = MARGE
    for ligne in enonce:
        draw.text((MARGE, y), ligne, font=gras, fill="black")
        y += 42
    y += 30
    for lignes in choix:
        draw.ellipse((MARGE + 4, y + 4, MARGE + 28, y + 28), outline="black", width=2)
        for ligne in lignes:
            draw.text((MARGE + RETRAIT, y), ligne, font=normal, fill="black")
            y += 38
        y += 28
    img.save(chemin)


def main():
    questions = [q for q in json.load(open(os.path.join(QCM, "pool.json"), encoding="utf-8"))["questions"]
                 if q["echantillon"]]
    os.makedirs(os.path.join(QCM, "img"), exist_ok=True)
    for q in questions:
        rendre(q, os.path.join(QCM, "img", f"{q['code_banc']}.png"))
    print(f"{len(questions)} images → {os.path.join(QCM, 'img')}")


if __name__ == "__main__":
    main()
