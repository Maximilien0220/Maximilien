# -*- coding: utf-8 -*-
"""Moteur de mise en page du livrable T005 (GANDAL)."""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether,
                                PageBreak, Flowable, NextPageTemplate)
from reportlab.graphics.shapes import (Drawing, Rect, String, Line, Polygon,
                                       PolyLine, Group)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = colors.HexColor("#1B3A57")
TEAL = colors.HexColor("#146B6B")
GOLD = colors.HexColor("#B08432")
GREY = colors.HexColor("#5C6670")
LIGHT = colors.HexColor("#F2F1EC")
RULE = colors.HexColor("#C9CDD2")
CODEBG = colors.HexColor("#F5F6F7")
BOXBG = colors.HexColor("#EDF3F3")

PAGE_W, PAGE_H = A4
LMARGIN = 22 * mm
RMARGIN = 22 * mm
TMARGIN = 24 * mm
BMARGIN = 20 * mm
CONTENT_W = PAGE_W - LMARGIN - RMARGIN   # ~ 470 pt


def register_fonts():
    pdfmetrics.registerFont(TTFont("Serif", os.path.join(FONT_DIR, "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("Serif-Bold", os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Sans", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("Sans-Bold", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", os.path.join(FONT_DIR, "DejaVuSansMono.ttf")))
    pdfmetrics.registerFont(TTFont("Mono-Bold", os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")))
    pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                                  italic="Serif", boldItalic="Serif-Bold")
    pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold",
                                  italic="Sans", boldItalic="Sans-Bold")
    pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-Bold",
                                  italic="Mono", boldItalic="Mono-Bold")


S = {}


def build_styles():
    S["body"] = ParagraphStyle("body", fontName="Serif", fontSize=9.3, leading=14.2,
                               alignment=TA_JUSTIFY, textColor=colors.HexColor("#1A1A1A"),
                               spaceAfter=6)
    S["body_first"] = ParagraphStyle("body_first", parent=S["body"], spaceBefore=1)
    S["bullet"] = ParagraphStyle("bullet", parent=S["body"], leftIndent=13, bulletIndent=3,
                                 spaceAfter=3.5, alignment=TA_JUSTIFY)
    S["h1num"] = ParagraphStyle("h1num", fontName="Sans-Bold", fontSize=8.2, leading=10,
                                textColor=TEAL, spaceAfter=3)
    S["h1"] = ParagraphStyle("h1", fontName="Sans-Bold", fontSize=19, leading=23,
                             textColor=NAVY, spaceAfter=4)
    S["h2"] = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=11.6, leading=14,
                             textColor=NAVY, spaceBefore=13, spaceAfter=5)
    S["h3"] = ParagraphStyle("h3", fontName="Sans-Bold", fontSize=9.8, leading=12.5,
                             textColor=TEAL, spaceBefore=9, spaceAfter=3.5)
    S["h4"] = ParagraphStyle("h4", fontName="Serif-Bold", fontSize=9.3, leading=12.5,
                             textColor=colors.HexColor("#243B4A"), spaceBefore=7, spaceAfter=2)
    S["caption"] = ParagraphStyle("caption", fontName="Sans", fontSize=7.9, leading=10.2,
                                  alignment=TA_CENTER, textColor=GREY, spaceBefore=4,
                                  spaceAfter=9)
    S["capcode"] = ParagraphStyle("capcode", fontName="Sans", fontSize=7.9, leading=10.2,
                                  alignment=TA_LEFT, textColor=GREY, spaceBefore=1,
                                  spaceAfter=3)
    S["th"] = ParagraphStyle("th", fontName="Sans-Bold", fontSize=7.9, leading=9.8,
                             textColor=colors.white)
    S["td"] = ParagraphStyle("td", fontName="Serif", fontSize=7.9, leading=10.3,
                             textColor=colors.HexColor("#1A1A1A"))
    S["td_b"] = ParagraphStyle("td_b", parent=S["td"], fontName="Serif-Bold")
    S["td_m"] = ParagraphStyle("td_m", parent=S["td"], fontName="Mono", fontSize=7.1,
                               leading=9.8)
    S["code"] = ParagraphStyle("code", fontName="Mono", fontSize=7.2, leading=9.5,
                               textColor=colors.HexColor("#16222B"))
    S["note"] = ParagraphStyle("note", fontName="Serif", fontSize=8.5, leading=12.4,
                               alignment=TA_JUSTIFY, textColor=colors.HexColor("#1F3340"))
    S["notehead"] = ParagraphStyle("notehead", fontName="Sans-Bold", fontSize=7.8,
                                   leading=10, textColor=TEAL, spaceAfter=2)
    S["toc1"] = ParagraphStyle("toc1", fontName="Sans-Bold", fontSize=9.3, leading=16,
                               textColor=NAVY)
    S["toc2"] = ParagraphStyle("toc2", fontName="Serif", fontSize=9, leading=14,
                               leftIndent=16, textColor=colors.HexColor("#243B4A"))
    S["cover_inst"] = ParagraphStyle("cover_inst", fontName="Sans-Bold", fontSize=9.6,
                                     leading=14, textColor=NAVY)
    S["cover_dept"] = ParagraphStyle("cover_dept", fontName="Sans", fontSize=8.6,
                                     leading=13, textColor=GREY)
    S["cover_kicker"] = ParagraphStyle("cover_kicker", fontName="Sans-Bold", fontSize=8.2,
                                       leading=11, textColor=TEAL)
    S["cover_title"] = ParagraphStyle("cover_title", fontName="Sans-Bold", fontSize=27,
                                      leading=33, textColor=NAVY)
    S["cover_sub"] = ParagraphStyle("cover_sub", fontName="Serif", fontSize=11,
                                    leading=16, textColor=GREY)
    S["cover_lab"] = ParagraphStyle("cover_lab", fontName="Sans-Bold", fontSize=7.2,
                                    leading=10, textColor=TEAL)
    S["cover_val"] = ParagraphStyle("cover_val", fontName="Serif", fontSize=10.4,
                                    leading=14, textColor=NAVY)
    S["cover_small"] = ParagraphStyle("cover_small", fontName="Serif", fontSize=8.6,
                                      leading=12, textColor=GREY)
    return S


# ---------------------------------------------------------------- flowables

class HRule(Flowable):
    def __init__(self, width, thickness=0.7, color=RULE, space=0):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color
        self.height = thickness + space

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


class CodeBlock(Flowable):
    """Bloc de code monospace, fond clair, filet lateral, pagination propre."""

    LEAD = 9.6
    PADX = 7
    PADY = 6

    def __init__(self, text, width=CONTENT_W, fontsize=7.2):
        Flowable.__init__(self)
        self.fontsize = fontsize
        self.width = width
        self.lines = self._wrap(text)
        self.height = len(self.lines) * self.LEAD + 2 * self.PADY

    def _wrap(self, text):
        avail = self.width - 2 * self.PADX - 3
        out = []
        for raw in text.strip("\n").split("\n"):
            line = raw.rstrip()
            if not line:
                out.append("")
                continue
            if pdfmetrics.stringWidth(line, "Mono", self.fontsize) <= avail:
                out.append(line)
                continue
            indent = len(line) - len(line.lstrip())
            pad = " " * (indent + 4)
            cur = ""
            for word in line.split(" "):
                cand = word if not cur else cur + " " + word
                if pdfmetrics.stringWidth(cand, "Mono", self.fontsize) <= avail:
                    cur = cand
                else:
                    if cur:
                        out.append(cur)
                    cur = pad + word
                    while pdfmetrics.stringWidth(cur, "Mono", self.fontsize) > avail:
                        n = len(cur)
                        while n > 1 and pdfmetrics.stringWidth(cur[:n], "Mono", self.fontsize) > avail:
                            n -= 1
                        out.append(cur[:n])
                        cur = pad + cur[n:]
            if cur:
                out.append(cur)
        return out

    def wrap(self, aw, ah):
        return self.width, self.height

    def split(self, aw, ah):
        usable = ah - 2 * self.PADY
        if usable < 3 * self.LEAD:
            return []
        n = int(usable // self.LEAD)
        if n >= len(self.lines):
            return [self]
        if len(self.lines) - n < 2:
            n = len(self.lines) - 2
        if n < 2:
            return []
        a = CodeBlock("\n".join(self.lines[:n]) or " ", self.width, self.fontsize)
        b = CodeBlock("\n".join(self.lines[n:]) or " ", self.width, self.fontsize)
        return [a, b]

    def draw(self):
        c = self.canv
        c.setFillColor(CODEBG)
        c.setStrokeColor(colors.HexColor("#E0E3E6"))
        c.setLineWidth(0.5)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=1)
        c.setFillColor(TEAL)
        c.rect(0, 0, 2.2, self.height, stroke=0, fill=1)
        c.setFont("Mono", self.fontsize)
        y = self.height - self.PADY - self.fontsize + 1.2
        for line in self.lines:
            stripped = line.lstrip()
            if stripped.startswith("#") or stripped.startswith("--") or stripped.startswith(";"):
                c.setFillColor(colors.HexColor("#6B7A82"))
            else:
                c.setFillColor(colors.HexColor("#16222B"))
            c.drawString(self.PADX + 3, y, line)
            y -= self.LEAD


class NoteBox(Flowable):
    """Encadre d'attention ou de decision."""

    def __init__(self, title, paragraphs, width=CONTENT_W, accent=TEAL, bg=BOXBG):
        Flowable.__init__(self)
        self.width = width
        self.accent = accent
        self.bg = bg
        self.title = title
        self.paras = [Paragraph(t, S["note"]) for t in paragraphs]
        self.head = Paragraph(title.upper(), S["notehead"]) if title else None
        self.padx = 9
        self.pady = 7
        self._h = None

    def wrap(self, aw, ah):
        inner = self.width - 2 * self.padx - 3
        h = 2 * self.pady
        if self.head:
            h += self.head.wrap(inner, ah)[1] + 2
        for p in self.paras:
            h += p.wrap(inner, ah)[1] + 3
        self._h = h
        self.height = h
        return self.width, h

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.setStrokeColor(colors.HexColor("#D6DEDE"))
        c.setLineWidth(0.5)
        c.rect(0, 0, self.width, self._h, stroke=1, fill=1)
        c.setFillColor(self.accent)
        c.rect(0, 0, 2.6, self._h, stroke=0, fill=1)
        inner = self.width - 2 * self.padx - 3
        y = self._h - self.pady
        if self.head:
            hh = self.head.wrap(inner, self._h)[1]
            y -= hh
            self.head.drawOn(c, self.padx + 3, y)
            y -= 2
        for p in self.paras:
            ph = p.wrap(inner, self._h)[1]
            y -= ph
            p.drawOn(c, self.padx + 3, y)
            y -= 3


class FigureBox(Flowable):
    """Enveloppe un Drawing pour le centrer dans la colonne."""

    def __init__(self, drawing, width=CONTENT_W):
        Flowable.__init__(self)
        self.d = drawing
        self.width = width
        self.height = drawing.height

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        x = (self.width - self.d.width) / 2.0
        self.d.drawOn(self.canv, x, 0)


# ---------------------------------------------------------------- helpers

def P(text, style="body"):
    return Paragraph(text, S[style])


def bullets(items, style="bullet", marker="•"):
    return [Paragraph(t, S[style], bulletText=marker) for t in items]


def numbered(items, style="bullet"):
    return [Paragraph(t, S[style], bulletText="%d." % (i + 1))
            for i, t in enumerate(items)]


def caption(text):
    return Paragraph(text, S["caption"])


def make_table(header, rows, widths, align_first_mono=False, font_small=False,
               zebra=True, head_bg=NAVY):
    """Construit un tableau robuste : toutes les cellules sont des Paragraph."""
    body_style = S["td_m"] if font_small else S["td"]
    data = [[Paragraph(h, S["th"]) for h in header]]
    for r in rows:
        line = []
        for i, cell in enumerate(r):
            if isinstance(cell, Paragraph):
                line.append(cell)
            else:
                st = S["td_m"] if (align_first_mono and i == 0) else body_style
                line.append(Paragraph(str(cell), st))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, head_bg),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, LIGHT] if zebra else [colors.white]),
        ("INNERGRID", (0, 1), (-1, -1), 0.25, colors.HexColor("#DEE1E4")),
    ]
    t.setStyle(TableStyle(cmds))
    return t


# ---------------------------------------------------------------- document

class Doc(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(self, path, pagesize=A4,
                                 leftMargin=LMARGIN, rightMargin=RMARGIN,
                                 topMargin=TMARGIN, bottomMargin=BMARGIN, **kw)
        frame = Frame(LMARGIN, BMARGIN, CONTENT_W,
                      PAGE_H - TMARGIN - BMARGIN, id="main",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame], onPage=self._cover),
            PageTemplate(id="front", frames=[frame], onPage=self._front),
            PageTemplate(id="body", frames=[frame], onPage=self._body),
        ])
        self.current_head = ""
        self.pending_head = None
        self.suppress_once = False
        self.front_n = 0
        self.body_n = 0
        self.page_label = ""

    # --- decors
    def _cover(self, canv, doc):
        canv.saveState()
        canv.setFillColor(NAVY)
        canv.rect(0, 0, 11 * mm, PAGE_H, stroke=0, fill=1)
        canv.setFillColor(GOLD)
        canv.rect(11 * mm, PAGE_H - 102 * mm, 3.2 * mm, 46 * mm, stroke=0, fill=1)
        canv.setStrokeColor(colors.HexColor("#E3E1DA"))
        canv.setLineWidth(0.9)
        x0, y0 = PAGE_W - 78 * mm, PAGE_H - 96 * mm
        canv.lines([(x0, y0, x0 + 55 * mm, y0 + 55 * mm),
                    (x0 + 55 * mm, y0 + 55 * mm, x0 + 55 * mm, y0),
                    (x0 + 55 * mm, y0, x0, y0)])
        canv.setStrokeColor(GOLD)
        canv.setLineWidth(0.8)
        canv.lines([(x0 + 14 * mm, y0 + 12 * mm, x0 + 46 * mm, y0 + 44 * mm),
                    (x0 + 46 * mm, y0 + 44 * mm, x0 + 46 * mm, y0 + 12 * mm)])
        canv.restoreState()

    def _front(self, canv, doc):
        self.front_n += 1
        self.page_label = _roman(self.front_n)
        self._footer(canv, doc)

    def _body(self, canv, doc):
        self.body_n += 1
        self.page_label = str(self.body_n)
        if self.pending_head is not None:
            self.current_head = self.pending_head
            self.pending_head = None
        show = self.current_head and not self.suppress_once
        self.suppress_once = False
        canv.saveState()
        if show:
            canv.setFont("Sans", 7.2)
            canv.setFillColor(GREY)
            canv.drawString(LMARGIN, PAGE_H - TMARGIN + 11, self.current_head)
            canv.setStrokeColor(RULE)
            canv.setLineWidth(0.5)
            canv.line(LMARGIN, PAGE_H - TMARGIN + 6.5,
                      PAGE_W - RMARGIN, PAGE_H - TMARGIN + 6.5)
        canv.restoreState()
        self._footer(canv, doc)

    def _footer(self, canv, doc, roman=False):
        canv.saveState()
        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.5)
        canv.line(LMARGIN, BMARGIN - 9, PAGE_W - RMARGIN, BMARGIN - 9)
        canv.setFont("Sans", 6.8)
        canv.setFillColor(GREY)
        canv.drawString(LMARGIN, BMARGIN - 17.5,
                        "PROJET GANDAL  /  CELLULE RÉSEAUX ET SÉCURITÉ  /  TÂCHE T005")
        canv.setFont("Sans-Bold", 7.4)
        canv.setFillColor(NAVY)
        canv.drawRightString(PAGE_W - RMARGIN, BMARGIN - 17.5, self.page_label)
        canv.restoreState()


def _roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"),
            (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"),
            (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, sym in vals:
        while n >= v:
            out += sym
            n -= v
    return out


class SetHead(Flowable):
    """Marqueur invisible : arme le titre courant pour les pages suivantes.

    Il est pose avant le saut de page qui ouvre un chapitre. L'en-tete est
    donc omis sur la page de titre du chapitre, puis affiche ensuite.
    """

    def __init__(self, doc, text, suppress=True):
        Flowable.__init__(self)
        self.doc = doc
        self.text = text
        self.suppress = suppress
        self.width = 0
        self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        self.doc.pending_head = self.text
        if self.suppress:
            self.doc.suppress_once = True


def chapter(doc, num, title, running=None):
    """Arme l'en-tete, passe a une nouvelle page et compose le titre."""
    out = [SetHead(doc, running or ("%s  /  %s" % (num, title))), PageBreak()]
    out.append(Spacer(1, 10))
    out.append(Paragraph("CHAPITRE %s" % num, S["h1num"]))
    out.append(Paragraph(title, S["h1"]))
    out.append(HRule(CONTENT_W, 1.1, GOLD, space=2))
    out.append(Spacer(1, 11))
    return out
