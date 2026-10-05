# Projet GANDAL, equipe 20

Depot des livrables de FOMETHE SOBMBANANG MAXIMILIEN pour le projet GANDAL
(cellule Reseaux et Securite).

## Livrables

Deux compositions du meme dossier de realisation de la tache T005, mise en
place du service DNS.

| Fichier | Composition |
| --- | --- |
| `T005_Mise_en_place_du_DNS_GANDAL_LaTeX.pdf` | LaTeX, police Latin Modern, identite ENSPY orange. Version de reference. |
| `T005_Mise_en_place_du_DNS_GANDAL.pdf` | ReportLab, premiere composition. |

La version LaTeX emploie la typographie classique des publications
scientifiques et formalise en notation mathematique le plan d'adressage, le
calcul du nombre de zones et d'enregistrements, la contrainte de MTU et la
fonction d'etiquetage des vues. Elle porte une identite visuelle propre :
orange Polytechnique en couleur directrice, anthracite pour le texte,
couverture a bandeau pleine largeur, numeros de chapitre en pave plein,
filets de tableau orange et paragraphes au carre.

Le dossier Il couvre la conception du service, les
configurations de reference des quatre instances, le cycle de vie des
enregistrements, les procedures d'exploitation et les criteres de recette.

Le dossier consomme le plan d'adressage arrete par le document 02 du corpus
et respecte la regle du corpus selon laquelle aucun deploiement ni essai
n'est presente comme effectue : les controles de recette portent le statut
NON EXECUTE.

La tache T009 (tests, validation, reprise et documentation), egalement
attribuee au meme responsable, depend des resultats des autres lots et reste
hors du perimetre de ce livrable.

## Reproduction des documents

### Version LaTeX, dans `source-latex/`

```
apt-get install texlive-latex-base texlive-latex-recommended \
                texlive-latex-extra texlive-fonts-recommended \
                texlive-lang-french texlive-pictures lmodern
cd source-latex && make
```

Deux passes de `pdflatex` sont necessaires pour resoudre les renvois internes.
Les quatre schemas sont traces en TikZ, les configurations composees avec
`listings`. `make verifier` recherche les tirets longs proscrits dans le texte
compose.

### Version ReportLab, dans `source/`

```
pip install reportlab
cd source && python3 build.py
```

Le script applique deux controles automatiques avant livraison : absence des
tirets longs proscrits dans les sources, puis dans le texte reellement extrait
du PDF produit.
