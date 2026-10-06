# Compilation du dossier T005. Deux passes : la seconde resout les renvois
# internes (table des matieres, equations, tableaux, figures, listings).
NOM = main

all:
	pdflatex -interaction=nonstopmode $(NOM).tex
	pdflatex -interaction=nonstopmode $(NOM).tex

# Audit de mise en page : signalements de TeX, caracteres proscrits,
# chevauchements entre mots, extension reelle de l'encre.
audit: all
	python3 audit.py

propre:
	rm -rf *.aux *.log *.out *.toc *.synctex.gz audit.html raster

.PHONY: all audit propre
