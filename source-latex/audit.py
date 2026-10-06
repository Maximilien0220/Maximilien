# -*- coding: utf-8 -*-
"""Audit de mise en page du dossier T005.

Quatre controles independants :
  1. signalements de TeX (lignes et cellules trop larges ou trop hautes) ;
  2. caracteres typographiques proscrits dans le texte compose ;
  3. chevauchements reels entre mots, a partir des boites englobantes ;
  4. mots qui se touchent sans se chevaucher, typiquement deux colonnes de
     tableau dont les contenus se rejoignent ;
  5. extension de l'encre, mesuree au balayage raster a 200 points par pouce.
"""

import glob
import io
import os
import re
import subprocess
import sys

PDF = "main.pdf"
LOG = "p2.log"
MM_PT = 2.834645            # millimetre exprime en points PostScript
DPI = 200
MM_PX = DPI / 25.4

# Geometrie declaree dans le preambule.
BLOC_G, BLOC_D = 24.0, 182.0
BLOC_H, BLOC_B = 30.0, 270.0
PROTRUSION = 0.6            # marge toleree pour la protrusion de microtype, en mm

PROSCRITS = {chr(0x2014): "tiret cadratin",
             chr(0x2013): "tiret demi-cadratin",
             chr(0x2015): "barre horizontale",
             chr(0x2012): "tiret numeral"}

anomalies = 0


def titre(n, texte):
    print("\n%d. %s" % (n, texte))
    print("   " + "-" * (len(texte) + 1))


def verdict(ok, message):
    global anomalies
    if not ok:
        anomalies += 1
    print("   [%s] %s" % ("ok" if ok else "ANOMALIE", message))


# --------------------------------------------------------------- 1. TeX
titre(1, "Signalements de TeX")
log = io.open(LOG, encoding="utf-8", errors="replace").read()
sign = [l for l in log.split("\n")
        if l.startswith("Overfull") or l.startswith("Underfull")]
for l in sign:
    print("       " + l.strip())
verdict(not sign, "%d boite trop large ou trop haute" % len(sign))


# --------------------------------------------- 2. caracteres proscrits
titre(2, "Caracteres typographiques proscrits")
texte = subprocess.run(["pdftotext", "-enc", "UTF-8", PDF, "-"],
                       capture_output=True, check=True).stdout.decode("utf-8")
trouves = {n: texte.count(c) for c, n in PROSCRITS.items() if c in texte}
verdict(not trouves, "occurrences : %s" % (trouves if trouves else "aucune"))


# ------------------------------------------------- 3. chevauchements
titre(3, "Chevauchements entre mots")
subprocess.run(["pdftotext", "-bbox-layout", PDF, "audit.html"], check=True)
doc = io.open("audit.html", encoding="utf-8", errors="replace").read()
pages = re.findall(r'<page width="[\d.]+" height="[\d.]+">(.*?)</page>', doc, re.S)
motif = re.compile(r'<word xMin="([\d.-]+)" yMin="([\d.-]+)" '
                   r'xMax="([\d.-]+)" yMax="([\d.-]+)">(.*?)</word>')
conflits = []
for n, corps in enumerate(pages, 1):
    mots = []
    for m in motif.finditer(corps):
        x0, y0, x1, y1 = map(float, m.groups()[:4])
        t = re.sub(r"<.*?>", "", m.group(5))
        # les delimiteurs extensibles sont assembles de pieces qui se recouvrent
        if any(0xF000 <= ord(c) <= 0xF8FF for c in t):
            continue
        if x1 - x0 > 1.5 and y1 - y0 > 1.5:
            mots.append((x0, y0, x1, y1, t))
    mots.sort(key=lambda w: w[1])
    for i in range(len(mots)):
        xa0, ya0, xa1, ya1, ta = mots[i]
        for j in range(i + 1, len(mots)):
            xb0, yb0, xb1, yb1, tb = mots[j]
            if yb0 > ya1:
                break
            ix = min(xa1, xb1) - max(xa0, xb0)
            iy = min(ya1, yb1) - max(ya0, yb0)
            if ix <= 0.4 or iy <= 0.4:
                continue
            aire = ix * iy
            petite = min((xa1 - xa0) * (ya1 - ya0), (xb1 - xb0) * (yb1 - yb0))
            if aire > 0.35 * petite:
                conflits.append((n, ta, tb))
for c in conflits[:8]:
    print("       page %d : %r et %r" % c)
verdict(not conflits, "%d chevauchement sur %d pages" % (len(conflits), len(pages)))


# ------------------------------------------------- 4. mots qui se touchent
titre(4, "Mots qui se touchent")

# Une espace fine francaise mesure environ 1,7 pt : en dessous de 1,2 pt,
# deux mots distincts se rejoignent et le texte devient illisible.
ECART_MIN = 1.2


def typographique(mot):
    """Vrai pour un fragment de formule ou un signe isole, kerne a dessein."""
    return len(mot) < 2 or not any(c.isalnum() for c in mot)


jointures = []
for n, corps in enumerate(pages, 1):
    mots = []
    for m in motif.finditer(corps):
        x0, y0, x1, y1 = map(float, m.groups()[:4])
        t = re.sub(r"<.*?>", "", m.group(5))
        if any(0xF000 <= ord(c) <= 0xF8FF for c in t):
            continue
        mots.append((x0, y0, x1, y1, t))
    # regroupement par recouvrement vertical, et non par ordonnee arrondie :
    # deux cellules voisines n'ont pas toujours la meme ligne de base.
    mots.sort(key=lambda w: (w[1], w[0]))
    lignes = []
    for mot in mots:
        place = False
        for ligne in lignes:
            y0, y1 = mot[1], mot[3]
            ry0, ry1 = ligne[0]
            rec = min(y1, ry1) - max(y0, ry0)
            if rec > 0.5 * min(y1 - y0, ry1 - ry0):
                ligne[0] = (min(y0, ry0), max(y1, ry1))
                ligne[1].append(mot)
                place = True
                break
        if not place:
            lignes.append([(mot[1], mot[3]), [mot]])
    for _, contenu in lignes:
        contenu.sort(key=lambda w: w[0])
        for i in range(len(contenu) - 1):
            a, b = contenu[i], contenu[i + 1]
            ecart = b[0] - a[2]
            if ecart >= ECART_MIN or typographique(a[4]) or typographique(b[4]):
                continue
            # Un indice jouxte sa base a dessein. Il se reconnait a trois
            # traits simultanes : corps plus petit, sommet plus bas et
            # descente sous la ligne de base de la base.
            ha, hb = a[3] - a[1], b[3] - b[1]
            petit, grand = (a, b) if ha < hb else (b, a)
            indice = (min(ha, hb) / max(ha, hb) < 0.85
                      and petit[3] > grand[3] + 0.8
                      and petit[1] > grand[1] + 2.0)
            if not indice:
                jointures.append((n, round(ecart, 2), a[4], b[4]))

for j in jointures[:8]:
    print("       page %d : ecart %.2f pt entre %r et %r" % j)
verdict(not jointures, "%d jointure sous %.1f pt" % (len(jointures), ECART_MIN))


# ------------------------------------------------------ 5. encre reelle
titre(5, "Extension de l'encre, balayage raster")
if os.path.isdir("raster"):
    for f in glob.glob("raster/*.png"):
        os.remove(f)
else:
    os.mkdir("raster")
subprocess.run(["pdftoppm", "-r", str(DPI), "-png", PDF, "raster/p"], check=True)

try:
    from PIL import Image
except ImportError:
    print("   Pillow absent : controle raster ignore")
    sys.exit(1)

gauche, droite = 1e9, 0.0
collisions = []
images = sorted(glob.glob("raster/p-*.png"))
for f in images[1:]:                       # la couverture est a fond perdu
    im = Image.open(f).convert("L")
    w, h = im.size
    px = im.load()
    lignes = []
    for y in range(h):
        a, b = w, 0
        for x in range(w):
            if px[x, y] < 190:
                if x < a:
                    a = x
                b = x
        if b:
            lignes.append((y, a, b))
            gauche = min(gauche, a / MM_PX)
            droite = max(droite, b / MM_PX)
    # blocs d'encre separes par au moins 3 mm de blanc
    blocs, debut, prec = [], None, None
    for y, a, b in lignes:
        if prec is None or y - prec > 3 * MM_PX:
            if debut is not None:
                blocs.append((debut, prec))
            debut = y
        prec = y
    if debut is not None:
        blocs.append((debut, prec))
    if len(blocs) >= 2:
        ecart = (blocs[-1][0] - blocs[-2][1]) / MM_PX
        if ecart < 4.0:
            collisions.append((os.path.basename(f), round(ecart, 1)))

print("       bord gauche atteint : %6.2f mm   (bloc de texte : %.0f mm)"
      % (gauche, BLOC_G))
print("       bord droit atteint  : %6.2f mm   (bloc de texte : %.0f mm)"
      % (droite, BLOC_D))
verdict(gauche > BLOC_G - PROTRUSION and droite < BLOC_D + PROTRUSION,
        "depassement au plus egal a %.1f mm, compatible avec la protrusion"
        % PROTRUSION)
verdict(not collisions,
        "distance corps vers pied de page : %s"
        % ("toujours superieure a 4 mm" if not collisions else collisions))


# ------------------------------------------------------------- synthese
print("\n%s" % ("=" * 62))
if anomalies:
    print("AUDIT : %d anomalie(s) a corriger" % anomalies)
    sys.exit(1)
print("AUDIT : aucune anomalie sur %d pages" % len(images))
