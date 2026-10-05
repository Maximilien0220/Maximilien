# -*- coding: utf-8 -*-
"""Production du livrable PDF T005 et controles automatiques de conformite."""

import io
import os
import sys
import unicodedata

from engine import register_fonts, build_styles, Doc
import content

OUT = "/home/user/Maximilien/T005_Mise_en_place_du_DNS_GANDAL.pdf"

# Caracteres proscrits par la consigne, verifies avant et apres generation.
INTERDITS = {
    chr(0x2014): "tiret cadratin",
    chr(0x2013): "tiret demi-cadratin",
    chr(0x2015): "barre horizontale",
    chr(0x2012): "tiret numeral",
}

SOURCES = ["engine.py", "figures.py", "content.py", "build.py"]


def controle_sources():
    """Aucune occurrence des caracteres proscrits dans les sources."""
    faute = False
    for path in SOURCES:
        texte = io.open(path, encoding="utf-8").read()
        for ligne_no, ligne in enumerate(texte.split("\n"), 1):
            for car, nom in INTERDITS.items():
                if car in ligne:
                    print("  REFUS  %s:%d  %s present" % (path, ligne_no, nom))
                    faute = True
    return not faute


def controle_pdf(path):
    """Verification du texte reellement extrait du PDF produit.

    Le flux PDF est compresse : une recherche d'octets dans le fichier brut
    produirait des faux positifs. Le texte est donc extrait page par page.
    """
    import subprocess
    brut = subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", path, "-"],
                          capture_output=True, check=True).stdout.decode("utf-8")
    faute = False
    for no, page in enumerate(brut.split("\f"), 1):
        for ligne_no, ligne in enumerate(page.split("\n"), 1):
            for car, nom in INTERDITS.items():
                if car in ligne:
                    print("  REFUS  page %d ligne %d : %s" % (no, ligne_no, nom))
                    print("         %s" % ligne.strip()[:110])
                    faute = True
    return not faute


def main():
    print("Controle des sources avant generation")
    if not controle_sources():
        sys.exit(1)
    print("  aucun caractere proscrit dans les sources")

    register_fonts()
    build_styles()
    doc = Doc(OUT, title="Mise en place du service DNS GANDAL, tache T005",
              author="FOMETHE SOMBANANG Maximilien",
              subject="Projet GANDAL, cellule Reseaux et Securite, tache T005",
              creator="Cellule Reseaux et Securite, projet GANDAL")
    story = content.story(doc)
    doc.build(story)

    print("Generation terminee : %s" % OUT)
    print("  pages de corps : %d" % doc.body_n)
    print("  pages liminaires : %d" % doc.front_n)
    print("  taille : %.1f Ko" % (os.path.getsize(OUT) / 1024.0))

    print("Controle du PDF produit")
    if not controle_pdf(OUT):
        sys.exit(1)
    print("  aucun caractere proscrit dans le flux PDF")


if __name__ == "__main__":
    main()
