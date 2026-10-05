# Projet GANDAL, equipe 20

Depot des livrables de FOMETHE SOMBANANG Maximilien pour le projet GANDAL
(cellule Reseaux et Securite).

## Livrable courant

`T005_Mise_en_place_du_DNS_GANDAL.pdf` : dossier de realisation de la tache
T005, mise en place du service DNS. Il couvre la conception du service, les
configurations de reference des quatre instances, le cycle de vie des
enregistrements, les procedures d'exploitation et les criteres de recette.

Le dossier consomme le plan d'adressage arrete par le document 02 du corpus
et respecte la regle du corpus selon laquelle aucun deploiement ni essai
n'est presente comme effectue : les controles de recette portent le statut
NON EXECUTE.

La tache T009 (tests, validation, reprise et documentation), egalement
attribuee au meme responsable, depend des resultats des autres lots et reste
hors du perimetre de ce livrable.

## Reproduction du document

Le PDF est genere par les scripts du repertoire `source/`, sans chaine
LaTeX, a partir de la bibliotheque ReportLab.

```
pip install reportlab
cd source && python3 build.py
```

Le script de generation applique deux controles automatiques avant livraison :
absence des tirets longs proscrits dans les sources, puis dans le texte
reellement extrait du PDF produit.
