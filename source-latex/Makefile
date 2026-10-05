# Compilation du dossier T005. Deux passes : la seconde resout les renvois
# internes (table des matieres, equations, tableaux, figures).
NOM = main
SORTIE = ../T005_Mise_en_place_du_DNS_GANDAL_LaTeX.pdf

all:
	pdflatex -interaction=nonstopmode $(NOM).tex
	pdflatex -interaction=nonstopmode $(NOM).tex

propre:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.synctex.gz

verifier: all
	@echo "Recherche des tirets longs proscrits dans le texte compose :"
	@pdftotext -enc UTF-8 $(NOM).pdf - | grep -c $$'—\|–' || true

.PHONY: all propre verifier
