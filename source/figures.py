# -*- coding: utf-8 -*-
"""Schemas du livrable T005, traces en primitives vectorielles.

Toutes les chaines sont mesurees avant trace : la taille de police est
reduite automatiquement lorsqu'un libelle depasse la largeur disponible,
de sorte qu'aucun texte ne deborde d'un cadre ni de la colonne.
"""

import math
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, PolyLine

NAVY = colors.HexColor("#1B3A57")
TEAL = colors.HexColor("#146B6B")
GOLD = colors.HexColor("#B08432")
GREY = colors.HexColor("#5C6670")
RED = colors.HexColor("#A33A3A")
BOX = colors.HexColor("#FFFFFF")
BAND = colors.HexColor("#EDF3F3")
HOST = colors.HexColor("#F6F5F0")
LINE = colors.HexColor("#9AA5AD")

W = 470.0


def _fit(text, font, size, maxw, floor=4.5):
    """Plus grande taille inferieure ou egale a size pour laquelle le texte tient."""
    s = size
    while s > floor and pdfmetrics.stringWidth(text, font, s) > maxw:
        s -= 0.15
    return s


def _t(d, x, y, s, size=6.6, font="Sans", color=NAVY, anchor="start", maxw=None):
    if maxw:
        size = _fit(s, font, size, maxw)
    d.add(String(x, y, s, fontName=font, fontSize=size, fillColor=color,
                 textAnchor=anchor))


def _box(d, x, y, w, h, fill=BOX, stroke=NAVY, lw=0.7, r=2.5, dash=None):
    rc = Rect(x, y, w, h, fillColor=fill, strokeColor=stroke, strokeWidth=lw)
    rc.rx = r
    rc.ry = r
    if dash:
        rc.strokeDashArray = dash
    d.add(rc)


def _node(d, x, y, w, h, title, lines=(), fill=BOX, stroke=NAVY, tsize=6.6,
          lsize=5.9, tcolor=NAVY, lcolor=GREY):
    """Cadre a titre centre et lignes monospace centrees, texte ajuste."""
    _box(d, x, y, w, h, fill=fill, stroke=stroke)
    pad = 5.0
    inner = w - 2 * pad
    cx = x + w / 2.0
    ts = _fit(title, "Sans-Bold", tsize, inner)
    yy = y + h - ts - 4.0
    d.add(String(cx, yy, title, fontName="Sans-Bold", fontSize=ts,
                 fillColor=tcolor, textAnchor="middle"))
    yy -= 3.0
    for ln in lines:
        ls = _fit(ln, "Mono", lsize, inner)
        yy -= ls + 2.0
        d.add(String(cx, yy, ln, fontName="Mono", fontSize=ls,
                     fillColor=lcolor, textAnchor="middle"))


def _step(d, x, y, w, h, num, title, lines):
    """Cadre a bandeau de titre, pour les etapes numerotees."""
    _box(d, x, y, w, h, fill=BOX, stroke=TEAL, lw=0.8)
    d.add(Rect(x, y + h - 13, w, 13, fillColor=TEAL, strokeColor=TEAL,
               strokeWidth=0.8))
    d.add(String(x + 5, y + h - 9.6, num, fontName="Sans-Bold", fontSize=6.6,
                 fillColor=colors.white))
    ts = _fit(title, "Sans-Bold", 6.3, w - 30)
    d.add(String(x + 15 + (w - 15) / 2.0, y + h - 9.6, title,
                 fontName="Sans-Bold", fontSize=ts, fillColor=colors.white,
                 textAnchor="middle"))
    yy = y + h - 25
    for t in lines:
        s = _fit(t, "Mono", 5.9, w - 12)
        d.add(String(x + w / 2.0, yy, t, fontName="Mono", fontSize=s,
                     fillColor=GREY, textAnchor="middle"))
        yy -= s + 2.6


def _head_tri(d, x1, y1, x2, y2, color, head):
    if head <= 0:
        return
    ang = math.atan2(y2 - y1, x2 - x1)
    a = ang + math.radians(150)
    b = ang - math.radians(150)
    d.add(Polygon([x2, y2,
                   x2 + head * math.cos(a), y2 + head * math.sin(a),
                   x2 + head * math.cos(b), y2 + head * math.sin(b)],
                  fillColor=color, strokeColor=color, strokeWidth=0.3))


def _arrow(d, x1, y1, x2, y2, color=TEAL, lw=0.85, dash=None, head=4.0):
    ln = Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=lw)
    if dash:
        ln.strokeDashArray = dash
    d.add(ln)
    _head_tri(d, x1, y1, x2, y2, color, head)


def _elbow(d, pts, color=TEAL, lw=0.85, dash=None, head=4.0):
    flat = []
    for p in pts:
        flat.extend(p)
    pl = PolyLine(flat, strokeColor=color, strokeWidth=lw)
    if dash:
        pl.strokeDashArray = dash
    d.add(pl)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    _head_tri(d, x1, y1, x2, y2, color, head)


def _cross(d, cx, cy, r=3.4, color=RED, lw=1.1):
    d.add(Line(cx - r, cy - r, cx + r, cy + r, strokeColor=color, strokeWidth=lw))
    d.add(Line(cx - r, cy + r, cx + r, cy - r, strokeColor=color, strokeWidth=lw))


# ------------------------------------------------------------------ figure 1

def fig_architecture():
    """Deux panneaux disjoints : placement physique, puis chemins logiques."""
    H = 344.0
    d = Drawing(W, H)

    # ---- panneau 1 : repartition sur les hotes
    _t(d, 0, H - 10, "PANNEAU 1   RÉPARTITION DES QUATRE INSTANCES SUR LES "
                     "TROIS HÔTES", 6.8, "Sans-Bold", TEAL, maxw=W)

    hosts = [
        (0, "HÔTE H1", "10.30.0.11",
         [("ns1   autoritatif primaire", "10.30.4.10"),
          ("rec2   résolveur récursif", "10.30.4.13")]),
        (160, "HÔTE H2", "10.30.0.12",
         [("rec1   résolveur récursif", "10.30.4.12")]),
        (320, "HÔTE H3", "10.30.0.13",
         [("ns2   autoritatif secondaire", "10.30.4.11")]),
    ]
    for x, name, mgmt, vms in hosts:
        _box(d, x, 238, 150, 88, fill=HOST, stroke=NAVY, lw=0.8)
        _t(d, x + 7, 315, name, 6.9, "Sans-Bold", NAVY)
        _t(d, x + 143, 315, mgmt, 6.0, "Mono", GREY, "end")
        yy = 280
        for label, ip in vms:
            _node(d, x + 8, yy, 134, 26, label, [ip], stroke=TEAL,
                  tsize=6.2, lsize=5.9)
            yy -= 34

    _t(d, 0, 226, "Anti-affinité par rôle : les deux membres d'une même paire ne "
                  "résident jamais sur le même hôte, de sorte que toute perte d'un "
                  "hôte laisse un serveur de chaque rôle en service.",
       6.1, "Sans", GREY, maxw=W)
    d.add(Line(0, 217, W, 217, strokeColor=LINE, strokeWidth=0.5))

    # ---- panneau 2 : chemins logiques
    _t(d, 0, 205, "PANNEAU 2   CHEMINS DE RÉSOLUTION", 6.8, "Sans-Bold", TEAL)

    _node(d, 0, 116, 126, 56, "CLIENTS AUTORISÉS",
          ["VNets tenant 10.30.64.0/18", "gestion 10.30.0.0/24",
           "VPN admin 10.30.16.32/28"], stroke=NAVY, tsize=6.5)
    _node(d, 172, 116, 126, 56, "RÉSOLVEURS rec1 et rec2",
          ["10.30.4.12 et 10.30.4.13", "allow-from puis vue",
           "cache indexé par étiquette"], stroke=TEAL, tsize=6.5)
    _node(d, 344, 116, 126, 56, "AUTORITATIFS ns1 et ns2",
          ["10.30.4.10 et 10.30.4.11", "zone gandal.internal",
           "et 30.10.in-addr.arpa"], stroke=NAVY, tsize=6.5)

    _arrow(d, 128, 140, 170, 140, TEAL, 0.9)
    _t(d, 149, 147, "UDP/TCP 53", 5.9, "Mono", TEAL, "middle")
    _arrow(d, 300, 140, 342, 140, NAVY, 0.9)
    _t(d, 321, 147, "forward-zones", 5.9, "Mono", NAVY, "middle")

    _node(d, 172, 44, 126, 44, "RACINE PUBLIQUE",
          ["via PF-WAN puis R1", "dnssec=validate"], stroke=GREY, tsize=6.5)
    _node(d, 344, 44, 126, 44, "RÉPLICATION",
          ["NOTIFY puis AXFR ou IXFR", "signés TSIG, ns1 vers ns2"], stroke=GOLD,
          tsize=6.5)
    _arrow(d, 235, 115, 235, 90, GREY, 0.85, dash=(2, 2))
    _arrow(d, 407, 115, 407, 90, GOLD, 0.85)

    # chemin direct interdit
    _elbow(d, [(63, 173), (63, 183), (407, 183), (407, 174)], color=RED, lw=0.85,
           dash=(2.5, 2), head=0)
    _cross(d, 235, 183)
    _t(d, 235, 191, "accès direct d'un VNet tenant aux serveurs autoritatifs : "
                    "refusé au pare-feu", 6.1, "Sans-Bold", RED, "middle", maxw=W)

    _t(d, 0, 28, "La carte réseau unique par hôte et le commutateur SW1 unique "
                 "restent des dépendances communes. La redondance couvre la perte "
                 "d'une machine", 6.1, "Sans", GREY, maxw=W)
    _t(d, 0, 19, "virtuelle ou d'un hôte, et non celle de SW1 ou du routeur R1.",
       6.1, "Sans", GREY, maxw=W)
    return d


# ------------------------------------------------------------------ figure 2

def fig_zones():
    H = 232.0
    d = Drawing(W, H)
    colw = 220.0
    xr = 250.0

    _t(d, 0, H - 9, "ESPACE DIRECT", 6.8, "Sans-Bold", TEAL)
    _t(d, xr, H - 9, "ESPACE INVERSE", 6.8, "Sans-Bold", TEAL)

    _node(d, 0, H - 56, colw, 38, "gandal.internal",
          ["SOA, NS ns1 et ns2, adresses des 4 serveurs",
           "délégations NS vers les zones filles"], stroke=NAVY)
    _node(d, 24, H - 114, colw - 24, 34, "infra.gandal.internal",
          ["hôtes, XO, bastion, pfSense, services"], stroke=TEAL)
    _node(d, 24, H - 162, colw - 24, 34, "tenant-001 à tenant-050 .gandal.internal",
          ["50 zones, une par tenant"], stroke=TEAL)
    _elbow(d, [(12, H - 56), (12, H - 97), (22, H - 97)], color=LINE, lw=0.7, head=3.2)
    _elbow(d, [(12, H - 56), (12, H - 145), (22, H - 145)], color=LINE, lw=0.7, head=3.2)

    _node(d, xr, H - 56, colw, 38, "30.10.in-addr.arpa",
          ["le /16 appartient entièrement au projet",
           "aucun découpage RFC 2317 nécessaire"], stroke=NAVY)
    _node(d, xr + 24, H - 114, colw - 24, 34, "11 zones d'infrastructure",
          ["octets 0, 1, 2, 4, 5, 6, 7, 8, 10, 16 et 17"], stroke=TEAL)
    _node(d, xr + 24, H - 162, colw - 24, 34, "50 zones tenant",
          ["octets 64 à 113, une zone par /24"], stroke=TEAL)
    _elbow(d, [(xr + 12, H - 56), (xr + 12, H - 97), (xr + 22, H - 97)],
           color=LINE, lw=0.7, head=3.2)
    _elbow(d, [(xr + 12, H - 56), (xr + 12, H - 145), (xr + 22, H - 145)],
           color=LINE, lw=0.7, head=3.2)

    _box(d, 0, 4, W, 46, fill=BAND, stroke=TEAL, lw=0.6, dash=(2, 2))
    _t(d, 8, 38, "CORRESPONDANCE ENTRE UN TENANT, SA ZONE DIRECTE ET SA ZONE "
                 "INVERSE", 6.4, "Sans-Bold", TEAL, maxw=W - 16)
    _t(d, 8, 26, "tenant n, pour 1 <= n <= 50   :   tenant-0NN.gandal.internal   et   "
                 "(63+n).30.10.in-addr.arpa", 6.1, "Mono", NAVY, maxw=W - 16)
    _t(d, 8, 14, "exemple pour n = 7   :   tenant-007.gandal.internal   et   "
                 "70.30.10.in-addr.arpa, préfixe 10.30.70.0/24",
       6.1, "Mono", NAVY, maxw=W - 16)
    return d


# ------------------------------------------------------------------ figure 3

def fig_sequence():
    """Six etapes disposees en deux rangees de trois."""
    H = 250.0
    d = Drawing(W, H)
    bw, gap, bh = 146.0, 16.0, 56.0
    y1 = H - 62
    y2 = y1 - 92

    r1 = [("1", "BAIL ATTRIBUÉ",
           ["Kea délivre 10.30.70.37", "à la VIF de la machine"]),
          ("2", "PUBLICATION DU A",
           ["agent vers l'API de ns1", "PATCH rrset, type REPLACE"]),
          ("3", "PUBLICATION DU PTR",
           ["zone 70.30.10.in-addr.arpa", "même operation_id"])]
    r2 = [("4", "RÉPLICATION",
           ["NOTIFY de ns1 vers ns2", "AXFR ou IXFR signé TSIG"]),
          ("5", "CONTRÔLE",
           ["requête sur ns1, ns2,", "rec1 et rec2 ; concordance"]),
          ("6", "ÉTAT READY",
           ["exposé au Backend", "operation_id conservé"])]

    for row, y in ((r1, y1), (r2, y2)):
        for i, (num, title, lines) in enumerate(row):
            x = i * (bw + gap)
            _step(d, x, y, bw, bh, num, title, lines)
            if i < 2:
                _arrow(d, x + bw + 2, y + 20, x + bw + gap - 2, y + 20,
                       NAVY, 0.9, head=3.4)

    # enchainement de la rangee 1 vers la rangee 2
    xr = 2 * (bw + gap) + bw / 2.0
    ymid = y1 - 16
    _elbow(d, [(xr, y1), (xr, ymid), (bw / 2.0, ymid), (bw / 2.0, y2 + bh + 2)],
           color=NAVY, lw=0.9, head=3.4)

    # branche degradee
    _arrow(d, bw + gap + bw / 2.0, y2, bw + gap + bw / 2.0, y2 - 14, RED, 0.85,
           dash=(2.5, 2), head=3.4)
    _box(d, 40, y2 - 46, W - 80, 32, fill=colors.HexColor("#FBEEEE"), stroke=RED,
         lw=0.7)
    _t(d, W / 2.0, y2 - 26, "Échec de publication ou de contrôle : l'opération "
                            "reste observable en état dégradé,", 6.1, "Sans-Bold",
       RED, "middle", maxw=W - 96)
    _t(d, W / 2.0, y2 - 38, "l'adresse n'est pas rendue au pool et une alerte est "
                            "levée.", 6.1, "Sans", RED, "middle", maxw=W - 96)

    _box(d, 0, 4, W, 28, fill=BAND, stroke=TEAL, lw=0.6, dash=(2, 2))
    _t(d, 8, 22, "CORRESPONDANCE AVEC LA MACHINE D'ÉTATS DU DOCUMENT 03", 6.3,
       "Sans-Bold", TEAL, maxw=W - 16)
    _t(d, 8, 11, "étapes 1 à 3 : SERVICES_READY en cours   /   étapes 4 et 5 : "
                 "conditions de SERVICES_READY   /   étape 6 : READY",
       6.1, "Mono", NAVY, maxw=W - 16)
    return d


# ------------------------------------------------------------------ figure 4

def fig_chemin():
    H = 224.0
    d = Drawing(W, H)
    y0 = H - 46

    _node(d, 0, y0, 104, 40, "VM DU TENANT 007",
          ["10.30.70.37", "resolv.conf : .12 puis .13"], stroke=NAVY, tsize=6.4)
    _node(d, 122, y0, 104, 40, "PASSERELLE .1",
          ["paire PF-USER", "VIP 10.30.70.1"], stroke=NAVY, tsize=6.4)
    _node(d, 244, y0, 104, 40, "FILTRE pfSense",
          ["53 autorisé vers .12 et .13", ".10 et .11 refusés"], stroke=RED,
          tsize=6.4)
    _node(d, 366, y0, 104, 40, "rec1 ou rec2",
          ["allow-from vérifié", "gettag() calcule la vue"], stroke=TEAL,
          tsize=6.4)
    for x in (105, 227, 349):
        _arrow(d, x, y0 + 20, x + 16, y0 + 20, TEAL, 0.9, head=3.4)

    # bloc de decision
    _box(d, 0, 96, W, 62, fill=BAND, stroke=TEAL, lw=0.8)
    _t(d, 8, 146, "preresolve() : politique de sélection des zones", 6.7,
       "Sans-Bold", TEAL)
    _t(d, 8, 133, "nom sous tenant-007.gandal.internal ou 70.30.10.in-addr.arpa  :  "
                  "résolution autorisée", 6.1, "Mono", NAVY, maxw=W - 16)
    _t(d, 8, 121, "nom sous infra.gandal.internal ou sous un autre tenant  :  "
                  "REFUSED, sans divulgation", 6.1, "Mono", RED, maxw=W - 16)
    _t(d, 8, 109, "nom public  :  récursion ordinaire, quelle que soit la vue",
       6.1, "Mono", GREY, maxw=W - 16)
    _arrow(d, 418, y0, 418, 159, TEAL, 0.9, head=3.4)

    _node(d, 0, 34, 144, 46, "AUTORITATIFS ns1 et ns2",
          ["10.30.4.10 et 10.30.4.11", "atteints par forward-zones"], stroke=NAVY,
          tsize=6.4)
    _node(d, 163, 34, 144, 46, "RACINE PUBLIQUE",
          ["via PF-WAN puis R1", "dnssec=validate"], stroke=GREY, tsize=6.4)
    _node(d, 326, 34, 144, 46, "JOURNAL dnstap",
          ["horodatage en UTC", "lu en pull par Monitoring"], stroke=GOLD,
          tsize=6.4)
    _arrow(d, 72, 95, 72, 82, NAVY, 0.85, head=3.4)
    _arrow(d, 235, 95, 235, 82, GREY, 0.85, dash=(2, 2), head=3.4)
    _arrow(d, 398, 95, 398, 82, GOLD, 0.85, head=3.4)

    _t(d, 0, 20, "L'étiquette de vue est calculée avant toute consultation de cache "
                 "et entre dans la clé du cache paquet : deux vues distinctes ne "
                 "peuvent", 6.1, "Sans-Bold", TEAL, maxw=W)
    _t(d, 0, 11, "jamais partager une réponse. Un contrôle placé dans preresolve() "
                 "seul n'offrirait pas cette garantie.", 6.1, "Sans", GREY, maxw=W)
    return d
