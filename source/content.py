# -*- coding: utf-8 -*-
"""Contenu du livrable T005 : mise en place du service DNS GANDAL."""

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (Spacer, PageBreak, NextPageTemplate, Paragraph,
                                KeepTogether, Table, TableStyle)

from engine import (S, P, bullets, numbered, caption, make_table, CodeBlock,
                    NoteBox, FigureBox, HRule, SetHead, chapter,
                    CONTENT_W, NAVY, TEAL, GOLD, GREY, RULE, LIGHT)
import figures as F

CW = CONTENT_W


def story(doc):
    s = []
    add = s.append
    ext = s.extend

    # =================================================================
    # COUVERTURE
    # =================================================================
    add(Spacer(1, 34 * mm))
    add(P("Université de Yaoundé I", "cover_inst"))
    add(P("École Nationale Supérieure Polytechnique de Yaoundé", "cover_inst"))
    add(P("Département de Génie Informatique", "cover_dept"))
    add(Spacer(1, 26 * mm))
    add(P("DOSSIER DE RÉALISATION GANDAL  /  TÂCHE T005", "cover_kicker"))
    add(Spacer(1, 5))
    add(P("Mise en place<br/>du service DNS", "cover_title"))
    add(Spacer(1, 7))
    add(P("Conception détaillée, configurations et procédures d'exploitation "
          "du socle de résolution de noms", "cover_sub"))
    add(Spacer(1, 10))
    add(HRule(70, 1.4, GOLD))
    add(Spacer(1, 12 * mm))
    add(P("Présenté dans le cadre de", "cover_small"))
    add(P("Spécifications d'ingénierie datacenter", "cover_val"))
    add(Spacer(1, 40 * mm))

    t = Table([[Paragraph("RÉALISÉ PAR", S["cover_lab"]),
                Paragraph("PÉRIMÈTRE", S["cover_lab"])],
               [Paragraph("FOMETHE SOBMBANANG MAXIMILIEN", S["cover_val"]),
                Paragraph("Cellule Réseaux et Sécurité", S["cover_val"])],
               [Paragraph("Équipe 20, projet GANDAL", S["cover_small"]),
                Paragraph("Services Network, tâche T005", S["cover_small"])]],
              colWidths=[CW * 0.52, CW * 0.48], hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    add(t)
    add(Spacer(1, 10))
    add(HRule(CW, 0.6, RULE))
    add(Spacer(1, 6))
    t = Table([[Paragraph("Année universitaire 2025 / 2026", S["cover_small"]),
                Paragraph("Version 1.0  /  5 octobre 2026", S["cover_small"])]],
              colWidths=[CW * 0.5, CW * 0.5], hAlign="LEFT")
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("ALIGN", (1, 0), (1, 0), "RIGHT")]))
    add(t)

    add(NextPageTemplate("front"))
    add(PageBreak())

    # =================================================================
    # FICHE DE TACHE
    # =================================================================
    add(P("Fiche de tâche et résumé", "h1"))
    add(HRule(CW, 1.1, GOLD, space=2))
    add(Spacer(1, 10))

    rows = [
        ["Identifiant", "T005"],
        ["Intitulé", "Mettre en place le DNS"],
        ["Responsable", "FOMETHE SOBMBANANG MAXIMILIEN"],
        ["Pondération et priorité", "8 / 10, priorité haute"],
        ["Cellule", "Réseaux et Sécurité, lot Services Network"],
        ["Prérequis consommés",
         "T001 plan d'adressage et modèle IPAM (figé par le document 02), "
         "T003 réseau de management"],
        ["Tâches coordonnées",
         "T004 DHCP haute disponibilité, T006 synchronisation temporelle, "
         "T007 agent réseau et API de provisionnement"],
        ["Livrable", "Le présent dossier : conception, configurations, procédures "
                     "et critères de recette du service DNS"],
        ["Hors périmètre",
         "T009 tests, validation, reprise et documentation, qui exploite les "
         "critères définis au chapitre 6 une fois les autres lots disponibles"],
    ]
    add(make_table(["Rubrique", "Contenu"], rows, [CW * 0.26, CW * 0.74]))
    add(Spacer(1, 14))

    add(P("Résumé", "h2"))
    add(P("Ce dossier définit et paramètre le service de résolution de noms de "
          "GANDAL. Il sépare strictement le rôle autoritatif du rôle récursif, "
          "retient PowerDNS conformément à l'arbitrage du document 03, et construit "
          "l'espace de nommage interne à partir du plan d'adressage arrêté par le "
          "document 02. Il traite la confidentialité des noms entre domaines par une "
          "politique de sélection des zones indexée sur l'adresse source, doublée "
          "d'un filtrage réseau qui interdit aux VNets tenant d'atteindre les "
          "serveurs autoritatifs."))
    add(P("Le cycle de vie des enregistrements est confié à un propriétaire "
          "d'écriture unique, l'agent réseau, au moyen de l'API autoritative "
          "exposée derrière une terminaison TLS. Les opérations sont rejouables "
          "sans effet de bord, et une panne de publication laisse l'opération dans "
          "un état dégradé observable sans libérer une adresse encore utilisée."))
    add(P("Les configurations proposées sont complètes et cohérentes avec les "
          "contraintes matérielles du projet : une carte réseau par hôte, un "
          "commutateur unique, une MTU utile de 1450 octets imposée par "
          "l'encapsulation VXLAN. Conformément à la règle du corpus, aucun "
          "déploiement ni aucun essai n'est présenté comme effectué : les "
          "contrôles de recette sont énoncés avec leur commande, leur résultat "
          "attendu et le statut NON EXÉCUTÉ."))
    add(Spacer(1, 10))
    add(NoteBox("Mots-clés", [
        "GANDAL ; DNS ; PowerDNS ; zone autoritative ; résolveur récursif ; "
        "espace de nommage interne ; isolation multi-tenant ; TSIG ; DNSSEC ; "
        "publication idempotente ; mode dégradé."]))

    add(PageBreak())

    # =================================================================
    # ABREVIATIONS + SOMMAIRE
    # =================================================================
    add(P("Abréviations propres au dossier", "h1"))
    add(HRule(CW, 1.1, GOLD, space=2))
    add(Spacer(1, 10))
    add(P("Le glossaire général du corpus reste applicable. Les termes ci-dessous "
          "sont ceux que ce dossier emploie de manière spécifique."))
    add(Spacer(1, 5))
    rows = [
        ["Autoritatif", "Serveur qui détient les données d'une zone et répond avec "
                        "l'indicateur AA. Il ne résout pas les noms des autres zones."],
        ["Récursif", "Résolveur qui interroge la chaîne des serveurs autoritatifs "
                       "pour le compte d'un client et met les réponses en cache."],
        ["AXFR / IXFR", "Transfert complet ou incrémental d'une zone entre serveurs."],
        ["TSIG", "Signature symétrique des messages DNS, définie par le RFC 8945, "
                 "employée ici pour les transferts de zone."],
        ["NTA", "Negative Trust Anchor : exception locale de validation DNSSEC "
                "sur une branche de l'arbre."],
        ["RRset", "Ensemble des enregistrements partageant le même nom, la même "
                  "classe et le même type ; unité de modification de l'API."],
        ["PTR", "Enregistrement de résolution inverse, d'une adresse vers un nom."],
        ["Vue", "Ensemble de zones qu'une catégorie de clients est autorisée à "
                "résoudre ; déterminée ici par l'adresse source."],
        ["dnstap", "Format et transport de journalisation structurée des échanges DNS."],
        ["EDNS", "Extension du protocole DNS permettant notamment d'annoncer une "
                 "taille de réponse UDP supérieure à 512 octets."],
    ]
    add(make_table(["Terme", "Définition retenue"], rows, [CW * 0.17, CW * 0.83]))

    add(PageBreak())
    add(P("Sommaire", "h1"))
    add(HRule(CW, 1.1, GOLD, space=2))
    add(Spacer(1, 9))
    toc = [
        ("1", "Objectifs, périmètre et exigences couvertes", [
            "1.1  Objectif de la tâche et définition du service attendu",
            "1.2  Contexte repris du corpus et données d'entrée",
            "1.3  Registre des exigences couvertes",
            "1.4  Limites de périmètre et articulation avec les autres tâches",
        ]),
        ("2", "Conception du service de résolution", [
            "2.1  Séparation des rôles autoritatif et récursif",
            "2.2  Espace de nommage, zones directes et zones inverses",
            "2.3  Placement, redondance et domaines de panne",
            "2.4  Politique de durée de vie et cohérence avec le bail DHCP",
            "2.5  Dimensionnement et contraintes de transport",
            "2.6  Profil DNS par tenant et interfaces consommatrices",
        ]),
        ("3", "Isolation et confidentialité des noms", [
            "3.1  Expression du besoin et scénarios à empêcher",
            "3.2  Politique de sélection des zones par adresse source",
            "3.3  Filtrage réseau et matrice de flux",
            "3.4  Cas particulier des profils VPN",
        ]),
        ("4", "Configurations de référence", [
            "4.1  Serveurs autoritatifs ns1 et ns2",
            "4.2  Création des zones et des clés de transfert",
            "4.3  Résolveurs récursifs rec1 et rec2",
            "4.4  Script de politique de vue",
            "4.5  Exposition de l'API et des métriques",
        ]),
        ("5", "Cycle de vie des enregistrements et exploitation", [
            "5.1  Propriétaire d'écriture unique et séquence de publication",
            "5.2  Idempotence, rejeu et réconciliation",
            "5.3  Suppression, quarantaine et mode dégradé",
            "5.4  Amorçage, ordre de reprise et adresses de secours",
            "5.5  Journalisation, métriques et alertes",
            "5.6  Sauvegarde, restauration et gestion des secrets",
        ]),
        ("6", "Contrôles de recette de la tâche", [
            "6.1  Critères d'acceptation et commandes associées",
            "6.2  Transmission à la campagne de validation",
        ]),
        ("7", "Hypothèses, limites et points à valider", []),
    ]
    for num, title, subs in toc:
        add(Paragraph("%s   %s" % (num, title), S["toc1"]))
        for sub in subs:
            add(Paragraph(sub, S["toc2"]))
    add(Paragraph("Références", S["toc1"]))

    add(SetHead(doc, "1  /  Objectifs, périmètre et exigences couvertes"))
    add(NextPageTemplate("body"))

    # =================================================================
    # CHAPITRE 1
    # =================================================================
    add(PageBreak())
    add(Spacer(1, 10))
    add(Paragraph("CHAPITRE 1", S["h1num"]))
    add(Paragraph("Objectifs, périmètre et exigences couvertes", S["h1"]))
    add(HRule(CW, 1.1, GOLD, space=2))
    add(Spacer(1, 11))

    add(P("1.1  Objectif de la tâche et définition du service attendu", "h2"))
    add(P("La tâche T005 consiste à mettre en place le service DNS de GANDAL. "
          "Dans le découpage du suivi d'équipe, elle se situe après le gel du plan "
          "d'adressage et du modèle IPAM, et en parallèle du DHCP haute "
          "disponibilité et de la synchronisation temporelle. Le service attendu "
          "n'est pas un simple serveur de noms : le document 03 lui assigne quatre "
          "fonctions distinctes."))
    ext(bullets([
        "<b>Publier l'espace de nommage interne du datacenter</b>, c'est-à-dire "
        "les noms d'infrastructure et les noms des machines de chaque tenant, avec "
        "les résolutions inverses correspondantes.",
        "<b>Fournir une résolution récursive contrôlée</b> aux machines "
        "autorisées, pour les noms internes comme pour les noms publics.",
        "<b>Garantir la confidentialité des noms entre domaines</b> : un tenant ne "
        "doit lire ni la zone d'infrastructure ni la zone d'un autre tenant.",
        "<b>S'insérer dans le cycle de vie d'une allocation</b> : la publication "
        "d'un enregistrement est une étape de la machine d'états de création, "
        "entre l'attribution du bail et l'exposition de l'état READY.",
    ]))
    add(P("Mettre en place le DNS signifie donc arrêter une architecture, un "
          "espace de nommage, des règles d'accès et un mécanisme de mise à jour, "
          "puis produire les configurations et procédures qui permettent de les "
          "appliquer de manière reproductible. C'est l'objet des chapitres 2 à 5."))
    add(Spacer(1, 4))
    add(NoteBox("Règle de restitution du corpus", [
        "Tous les documents de cadrage de GANDAL précisent que la règle est "
        "d'effectuer une simulation au préalable et qu'aucun déploiement ni essai "
        "n'est présenté comme effectué. Ce dossier respecte cette règle : il "
        "fournit des configurations et des procédures complètes, mais les "
        "contrôles du chapitre 6 portent le statut NON EXÉCUTÉ. Produire les "
        "preuves correspondantes relève de la tâche T009, qui n'est pas traitée "
        "ici."]))

    add(P("1.2  Contexte repris du corpus et données d'entrée", "h2"))
    add(P("Les choix qui suivent sont contraints par des décisions déjà arrêtées. "
          "Elles ne sont pas rediscutées ici ; elles sont rappelées parce qu'elles "
          "déterminent directement la conception du service."))
    add(Spacer(1, 3))
    rows = [
        ["Trois hôtes XCP-ng, une NIC par hôte, un commutateur L2 et un routeur "
         "non manageables",
         "La redondance logicielle ne peut couvrir que la perte d'une machine "
         "virtuelle ou d'un hôte. SW1 et R1 restent des dépendances communes "
         "assumées.", "Document 01, 2.1"],
        ["Bloc 10.30.0.0/16, VNet Services en 10.30.4.0/24, DNS autoritatif "
         "en .10 et .11, DNS récursif en .12 et .13",
         "Les adresses des quatre instances sont imposées. Ce dossier les "
         "consomme sans redéfinition locale.", "Document 02, tableau 2.5"],
        ["Tenant n associé au préfixe 10.30.(63+n).0/24, pour 1 ≤ n ≤ 50",
         "La correspondance entre un tenant, sa zone directe et sa zone inverse "
         "se déduit arithmétiquement, ce qui rend la génération des zones et la "
         "politique de vue déterministes.", "Document 02, 2.4"],
        ["VXLAN sur IPv4 avec MTU externe de 1500 octets",
         "Au plus 1450 octets utiles pour le paquet IP interne. Le "
         "dimensionnement des réponses DNS en doit tenir compte.",
         "Document 02, 2.5"],
        ["PowerDNS Authoritative complété de PowerDNS Recursor",
         "Choix proposé par la comparaison du document 03 ; BIND reste "
         "l'alternative documentée du corpus.", "Document 03, tableau 1.1"],
        ["Aucun VNet surveillé n'initie de connexion vers Monitoring",
         "Les journaux et métriques du DNS sont conservés localement et lus en "
         "pull. Aucun envoi direct n'est configuré.", "Document 03, 2.7"],
        ["Deux instances de chaque service, sur des hôtes distincts",
         "Objectif de continuité logique, sans prétendre à l'élimination des "
         "points uniques de défaillance.", "NET-NFR-001"],
    ]
    add(make_table(["Contrainte ou décision antérieure", "Conséquence sur le service DNS",
                    "Source"], rows, [CW * 0.31, CW * 0.52, CW * 0.17]))
    add(caption("Tableau 1.1  Données d'entrée de la tâche T005 et leurs conséquences "
                "directes"))

    add(P("1.3  Registre des exigences couvertes", "h2"))
    add(P("Le tableau suivant relie chaque exigence du registre des services réseau "
          "au mécanisme retenu dans ce dossier et au contrôle de recette qui "
          "permettra de la vérifier. Les identifiants de contrôle C01 à C15 sont "
          "définis au chapitre 6."))
    add(Spacer(1, 3))
    rows = [
        ["NET-FR-004", "Paramètres DNS par tenant",
         "Objet profil DNS porté par l'IPAM et consommé par DHCP et Templates (2.6)",
         "C03"],
        ["NET-FR-006", "DNS interne et mises à jour",
         "Zones internes autoritatives et publication par l'agent via l'API (2.2, 5.1)",
         "C01, C10"],
        ["NET-FR-007", "Récursion DNS autorisée",
         "allow-from restreint aux préfixes du plan, sortie 53 explicite (4.3)",
         "C07"],
        ["NET-FR-008", "Confidentialité des noms entre domaines",
         "Politique de vue par adresse source, transferts fermés, autoritatif non "
         "exposé (3.2, 3.3)", "C04, C05, C06"],
        ["NET-FR-012", "Allocation et libération idempotentes",
         "Modification par RRset avec lecture préalable et clé d'idempotence (5.2)",
         "C10"],
        ["NET-FR-013", "Paramètres VM via Templates",
         "Profil DNS transmis par le contrat IF-NS-06 (2.6)", "C03"],
        ["NET-FR-014", "Métriques services",
         "Point de métriques en lecture seule, interrogé en pull (5.5)", "C14"],
        ["NET-FR-016", "API administratives chiffrées",
         "API autoritative liée à la boucle locale derrière une terminaison TLS (4.5)",
         "C10"],
        ["NET-FR-017", "DNS accessible selon profil VPN",
         "Vue administration pour le pool VPN admin, refus par défaut pour le pool "
         "utilisateur (3.4)", "C06"],
        ["NET-FR-018", "Journaux horodatés",
         "Journalisation dnstap horodatée en UTC, conservée localement (5.5)", "C14"],
        ["NET-FR-019", "Gestion de l'infrastructure isolée",
         "Les VNets tenant ne joignent ni le plan de gestion ni les autoritatifs (3.3)",
         "C08"],
        ["NET-FR-020", "Simulation avant déploiement",
         "Statut NON EXÉCUTÉ maintenu ; maquette préalable exigée (chapitre 7)", "aucun"],
        ["NET-NFR-001", "Deux instances DNS",
         "Deux autoritatifs et deux récursifs répartis sur les trois hôtes (2.3)",
         "C09"],
        ["NET-NFR-003", "Reconstruction en moins de 60 min",
         "Export des zones et procédure de restauration (5.6) ; mesure confiée à T009",
         "aucun"],
        ["NET-NFR-005", "Protection des communications administratives",
         "TLS sur l'API, TSIG sur les transferts (4.2, 4.5)", "C04"],
        ["NET-NFR-006", "Rejeu déterministe et idempotent",
         "Opérations convergentes sur l'état désiré des RRsets (5.2)", "C10"],
        ["NET-NFR-007", "Secrets absents des dépôts en clair",
         "Clés API et TSIG injectées au démarrage ; empreinte en configuration (5.6)",
         "aucun"],
        ["IF-NS-03", "DNS vers VNet/SDN : profils et ACL par tenant",
         "Étiquette de vue dérivée du préfixe tenant (3.2)", "C05"],
        ["IF-NS-06", "Agent vers Templates : réseau, DNS, MTU",
         "Contenu normalisé du profil DNS (2.6)", "C03"],
        ["IF-NS-08", "Network vers Monitoring : lecture en pull",
         "Aucune initiation sortante depuis les VM DNS (5.5)", "C14"],
    ]
    add(make_table(["Exigence", "Objet", "Mécanisme retenu et section",
                    "Contrôle"], rows,
                   [CW * 0.145, CW * 0.195, CW * 0.50, CW * 0.16]))
    add(caption("Tableau 1.2  Traçabilité entre les exigences du registre et les "
                "mécanismes de ce dossier"))

    add(P("1.4  Limites de périmètre et articulation avec les autres tâches", "h2"))
    add(P("Trois tâches voisines touchent au même cycle de vie sans relever de "
          "T005. Les points de contact sont explicités pour éviter une double "
          "définition."))
    rows = [
        ["T004, DHCP haute disponibilité (B. Heudep Djandja)",
         "T005 fournit les adresses des résolveurs et le nom de domaine à "
         "distribuer dans les options 6, 15 et 119. T005 ne définit ni les scopes, "
         "ni le mode de haute disponibilité de Kea, ni la durée de bail. La valeur "
         "de bail est ici une hypothèse de travail, signalée comme telle."],
        ["T006, synchronisation temporelle (B. Heudep Djandja)",
         "La validation DNSSEC et la journalisation corrélable supposent une "
         "horloge correcte. T005 énonce cette dépendance et la contrainte "
         "d'amorçage à froid, mais ne configure pas chrony."],
        ["T007, agent réseau et API de provisionnement (P. Pangui Pianne)",
         "T005 définit le contrat que l'agent doit respecter pour publier un "
         "enregistrement et le comportement attendu en cas d'échec. "
         "L'implémentation de l'agent ne relève pas de ce dossier."],
        ["T009, tests, validation, reprise et documentation",
         "Seconde tâche attribuée au même responsable. Elle dépend des résultats "
         "des lots précédents et n'est pas traitée ici. Le chapitre 6 lui transmet "
         "des critères d'acceptation déjà formulés, qui devront être exécutés et "
         "archivés dans ce cadre."],
    ]
    add(make_table(["Tâche voisine", "Point de contact et répartition"], rows,
                   [CW * 0.3, CW * 0.7]))
    add(caption("Tableau 1.3  Frontières de la tâche T005"))

    # =================================================================
    # CHAPITRE 2
    # =================================================================
    ext(chapter(doc, "2", "Conception du service de résolution"))

    add(P("2.1  Séparation des rôles autoritatif et récursif", "h2"))
    add(P("Le document 03 impose de distinguer au moins deux rôles de service et "
          "précise qu'une instance récursive partagée non filtrée est insuffisante. "
          "Cette séparation n'est pas une préférence de mise en œuvre : elle découle "
          "de trois propriétés incompatibles sur une même instance."))
    ext(bullets([
        "Un serveur autoritatif doit répondre avec autorité pour les zones qu'il "
        "détient et ne doit rien résoudre d'autre. Un résolveur doit au contraire "
        "parcourir l'arbre public et conserver un cache.",
        "Les populations de clients diffèrent. L'autoritatif n'a que quatre "
        "interlocuteurs légitimes : son homologue, les deux résolveurs et l'agent. "
        "Le résolveur sert au contraire l'ensemble des machines autorisées.",
        "Les surfaces d'attaque diffèrent. Exposer l'autoritatif aux tenants "
        "reviendrait à leur offrir un point d'interrogation direct de toutes les "
        "zones hébergées, que seule une politique interne pourrait ensuite "
        "restreindre.",
    ]))
    add(P("La conception retient donc deux serveurs autoritatifs, ns1 et ns2, qui "
          "ne sont joignables que depuis le VNet Services, et deux résolveurs "
          "récursifs, rec1 et rec2, qui constituent le seul point de résolution "
          "offert aux machines clientes. Les résolveurs atteignent l'espace interne "
          "par une redirection explicite de zone, et l'espace public par une "
          "récursion ordinaire."))
    add(Spacer(1, 6))
    add(FigureBox(F.fig_architecture()))
    add(caption("Figure 2.1  Architecture du service DNS : placement des quatre "
                "instances, flux autorisés et dépendances communes"))

    add(P("2.2  Espace de nommage, zones directes et zones inverses", "h2"))
    add(P("La zone gandal.internal est conservée comme proposition de nommage "
          "interne, conformément au document 03. Le suffixe est pertinent : "
          "l'ICANN a réservé le domaine de premier niveau internal à l'usage privé "
          "et ne le délègue pas dans la racine publique. Un nom construit sous ce "
          "suffixe ne peut donc pas entrer en collision avec un nom Internet, ce "
          "qui n'est pas le cas d'un suffixe arbitraire."))

    add(P("Découpage retenu", "h3"))
    ext(bullets([
        "<b>gandal.internal</b> porte le SOA, les enregistrements NS du service et "
        "les adresses des quatre serveurs, puis délègue ses zones filles.",
        "<b>infra.gandal.internal</b> contient l'inventaire d'infrastructure : "
        "hôtes, orchestrateur, bastion, machines pfSense, services de base et "
        "collecteurs.",
        "<b>tenant-0NN.gandal.internal</b>, pour NN de 001 à 050, contient la "
        "passerelle du tenant et les noms de ses machines.",
    ]))
    add(P("Les serveurs de noms sont volontairement nommés au niveau de l'apex, "
          "sous la forme ns1.gandal.internal, et non à l'intérieur de "
          "infra.gandal.internal. Ce choix évite une délégation dont les serveurs "
          "porteraient un nom situé sous la zone déléguée, configuration qui exige "
          "des enregistrements de collage dans la zone parente et complique "
          "inutilement la reconstruction."))

    add(P("Résolution inverse", "h3"))
    add(P("Toutes les plages du projet appartiennent au bloc 10.30.0.0/16 et sont "
          "découpées en /24, en /28 ou en /29. Comme le projet détient l'intégralité "
          "de l'espace, une zone inverse par /24 suffit à couvrir les sous-réseaux "
          "plus petits qu'elle contient : les quatre /28 de la plage DMZ et VPN "
          "relèvent tous de 16.30.10.in-addr.arpa, et les trois /29 de "
          "synchronisation de 17.30.10.in-addr.arpa. Le découpage sans classe du "
          "RFC 2317, utile lorsqu'un /24 est partagé entre plusieurs autorités, "
          "n'a donc aucune raison d'être introduit ici."))
    add(Spacer(1, 6))
    add(FigureBox(F.fig_zones()))
    add(caption("Figure 2.2  Arborescence des zones directes et inverses"))

    rows = [
        ["Zone racine interne", "gandal.internal", "1", "SOA, NS, adresses des "
         "serveurs, délégations"],
        ["Zone d'infrastructure", "infra.gandal.internal", "1",
         "environ 40 noms, statiques"],
        ["Zones tenant", "tenant-001 à tenant-050 .gandal.internal", "50",
         "passerelle statique, machines publiées par l'agent"],
        ["Inverses d'infrastructure",
         "0, 1, 2, 4, 5, 6, 7, 8, 10, 16, 17 .30.10.in-addr.arpa", "11",
         "un /24 inverse couvre les /28 et /29 qu'il contient"],
        ["Inverses tenant", "64 à 113 .30.10.in-addr.arpa", "50",
         "tenant n associé à l'octet 63 + n"],
        ["<b>Total</b>", "", "<b>113</b>", "volume compatible avec une base locale"],
    ]
    add(make_table(["Catégorie", "Nom ou intervalle", "Nombre", "Contenu"],
                   rows, [CW * 0.22, CW * 0.34, CW * 0.1, CW * 0.34]))
    add(caption("Tableau 2.1  Inventaire des zones à créer"))

    add(P("2.3  Placement, redondance et domaines de panne", "h2"))
    add(P("L'exigence NET-NFR-001 demande deux instances par service, et le "
          "document Underlay rappelle que la présence de plusieurs serveurs ne "
          "garantit pas leur indépendance si tous partagent le même hyperviseur. "
          "Le placement doit donc satisfaire une contrainte d'anti-affinité par "
          "rôle : les deux membres d'une paire ne résident jamais sur le même hôte."))
    add(P("Avec quatre instances et trois hôtes, un hôte en porte nécessairement "
          "deux. La répartition retenue place ns1 et rec2 sur H1, rec1 sur H2 et "
          "ns2 sur H3. Elle est préférable à un regroupement sur deux hôtes "
          "seulement, car elle laisse trois instances sur quatre en service après "
          "la perte de H2 ou de H3."))
    add(Spacer(1, 3))
    rows = [
        ["Fonctionnement nominal", "ns1 (H1), ns2 (H3)", "rec1 (H2), rec2 (H1)",
         "Service complet"],
        ["Perte de H1", "ns2", "rec1", "Un serveur de chaque rôle, capacité réduite "
         "de moitié ; ns2 devient le seul autoritatif et ne reçoit plus de "
         "transfert, donc plus de publication"],
        ["Perte de H2", "ns1, ns2", "rec2", "Résolution et publication nominales"],
        ["Perte de H3", "ns1", "rec1, rec2", "Publication nominale, réplication "
         "suspendue jusqu'au retour de ns2"],
        ["Perte de SW1", "aucune", "aucune", "Hors de portée de la redondance "
         "logicielle ; limite matérielle assumée par le cadrage"],
    ]
    add(make_table(["Scénario", "Autoritatifs restants", "Récursifs restants",
                    "Conséquence"], rows,
                   [CW * 0.17, CW * 0.17, CW * 0.17, CW * 0.49]))
    add(caption("Tableau 2.2  Effet de la perte d'un hôte sur le service de résolution"))
    add(Spacer(1, 4))
    add(NoteBox("Conséquence à retenir pour la reprise", [
        "La perte de H1 supprime le seul serveur autoritatif primaire. La "
        "résolution se poursuit sur ns2, qui continue de servir les zones "
        "transférées jusqu'à expiration du paramètre expire du SOA, fixé à sept "
        "jours. En revanche, aucune nouvelle publication n'est possible pendant "
        "cette période. La procédure de reprise consiste à restaurer ns1 depuis "
        "l'export des zones, et non à promouvoir ns2, afin de conserver un "
        "propriétaire d'écriture unique.",
        "Cette distinction entre continuité du trafic existant et impossibilité "
        "d'opérations nouvelles correspond exactement au résultat attendu du test "
        "G04 du document 01."], accent=GOLD,
        bg=colors.HexColor("#FAF5EA")))

    add(P("2.4  Politique de durée de vie et cohérence avec le bail DHCP", "h2"))
    add(P("Les durées de vie ne sont pas un réglage de confort : elles déterminent "
          "le délai pendant lequel une réponse périmée peut encore circuler après "
          "la suppression d'un enregistrement. Deux règles les gouvernent. "
          "Premièrement, la durée de vie d'un enregistrement dynamique doit rester "
          "nettement inférieure à la durée du bail qui l'a produit. Deuxièmement, "
          "une adresse ne peut être réattribuée à un autre tenant qu'après "
          "expiration des caches qui ont pu mémoriser son ancien nom."))
    add(Spacer(1, 3))
    rows = [
        ["SOA refresh", "3600 s", "Fréquence de contrôle de ns2 en l'absence de "
         "NOTIFY ; la réplication normale reste déclenchée par NOTIFY."],
        ["SOA retry", "900 s", "Nouvelle tentative après échec de transfert."],
        ["SOA expire", "604800 s", "Durée pendant laquelle ns2 continue de servir une "
         "zone sans contact avec ns1 ; dimensionnée pour couvrir une panne longue "
         "de H1."],
        ["SOA minimum", "300 s", "Durée de mémorisation d'une réponse négative. "
         "Une valeur courte évite qu'un nom publié tardivement reste introuvable."],
        ["Enregistrements d'infrastructure", "3600 s",
         "Noms stables, modifiés par une opération planifiée."],
        ["Enregistrements A et PTR tenant", "300 s",
         "Publiés et retirés avec le bail. Valeur retenue comme hypothèse pour un "
         "bail de 3600 s, soit un rapport de 1 à 12."],
        ["Quarantaine avant réutilisation", "900 s",
         "Proposée à l'IPAM. Elle couvre la durée de vie de l'enregistrement "
         "supprimé et une marge pour les clients qui ignorent cette durée. Elle "
         "répond au point laissé À VALIDER par le document 03."],
    ]
    add(make_table(["Paramètre", "Valeur proposée", "Justification"], rows,
                   [CW * 0.28, CW * 0.14, CW * 0.58]))
    add(caption("Tableau 2.3  Politique de durée de vie"))
    add(P("La durée de bail de 3600 secondes est une hypothèse de travail : elle "
          "relève de la tâche T004. Si elle est modifiée, la règle à conserver est "
          "que la durée de vie DNS reste au plus égale au quart du bail, et que la "
          "quarantaine reste supérieure à la somme de la durée de vie directe et "
          "de la durée de vie négative."))

    add(P("2.5  Dimensionnement et contraintes de transport", "h2"))
    add(P("Le volume à servir se déduit du plan d'adressage. Chaque tenant dispose "
          "d'un pool dynamique de 190 adresses, de .10 à .199. Dans l'hypothèse "
          "haute où les cinquante pools seraient pleins, le service publierait "
          "9 500 enregistrements A et autant de PTR, auxquels s'ajoutent environ "
          "330 enregistrements statiques, soit un peu moins de 20 000 "
          "enregistrements. La cible historique de 500 baux simultanés conduit en "
          "revanche à un régime courant d'environ 1 300 enregistrements."))
    add(P("Ce volume ne justifie pas un serveur de base de données dédié. Le "
          "moteur de stockage SQLite intégré à PowerDNS est retenu pour le "
          "périmètre minimal, la réplication étant assurée par transfert de zone et "
          "non par duplication de base. Un moteur relationnel partagé constitue "
          "une extension à envisager si la mesure du débit d'écriture de l'agent "
          "le justifie."))
    add(Spacer(1, 3))
    rows = [
        ["ns1, ns2", "2 vCPU", "2 GiB", "20 GiB",
         "Base SQLite, journal local, export des zones"],
        ["rec1, rec2", "2 vCPU", "4 GiB", "20 GiB",
         "Mémoire dimensionnée pour le cache d'enregistrements et le cache paquet"],
    ]
    add(make_table(["Instance", "Processeur", "Mémoire", "Disque",
                    "Remarque"], rows,
                   [CW * 0.14, CW * 0.13, CW * 0.12, CW * 0.12, CW * 0.49]))
    add(caption("Tableau 2.4  Dimensionnement proposé des machines virtuelles"))

    add(P("Taille des réponses et MTU", "h3"))
    add(P("Le document 02 établit qu'avec une MTU externe de 1500 octets, "
          "l'encapsulation VXLAN sur IPv4 laisse au plus 1450 octets au paquet IP "
          "interne. Une réponse DNS qui dépasserait cette taille serait fragmentée "
          "ou perdue selon le comportement des équipements intermédiaires, et ce "
          "type de défaut se manifeste de manière intermittente, donc difficile à "
          "diagnostiquer."))
    add(P("La taille annoncée par EDNS est en conséquence fixée à 1232 octets sur "
          "les quatre instances, valeur qui laisse une marge confortable sous les "
          "1450 octets disponibles et qui correspond à la recommandation issue du "
          "DNS Flag Day 2020. Au-delà de ce seuil, la réponse est tronquée et le "
          "client bascule en TCP, comportement prévisible et observable. Les "
          "règles de pare-feu doivent donc autoriser le port 53 en TCP comme en "
          "UDP, point souvent omis."))

    add(P("2.6  Profil DNS par tenant et interfaces consommatrices", "h2"))
    add(P("Le modèle IPAM minimal du document 03 comporte un champ DNS_profile "
          "dont le contenu n'est pas spécifié. Ce dossier le définit, car il "
          "constitue le point de passage unique entre la conception DNS, les "
          "options distribuées par DHCP et les paramètres remis aux Templates."))
    add(CodeBlock("""
{
  "profile_id":        "tenant-standard-v1",
  "tenant_id":         7,
  "resolvers":         ["10.30.4.12", "10.30.4.13"],
  "search_domains":    ["tenant-007.gandal.internal"],
  "forward_zone":      "tenant-007.gandal.internal",
  "reverse_zone":      "70.30.10.in-addr.arpa",
  "record_ttl":        300,
  "publication":       "agent",
  "external_recursion": true,
  "view_tag":          1007
}
"""))
    add(Paragraph("Listing 2.1  Objet profil DNS porté par l'IPAM, instancié pour le "
                  "tenant 7 (préfixe 10.30.70.0/24)", S["capcode"]))
    add(Spacer(1, 4))
    rows = [
        ["IF-NS-02, vers DHCP",
         "resolvers alimente l'option 6, search_domains l'option 15 et l'option "
         "119. Le serveur Kea ne redéfinit aucune de ces valeurs localement."],
        ["IF-NS-06, vers Templates",
         "resolvers, search_domains et la MTU utile sont remis au mécanisme "
         "d'initialisation de la machine. Le profil ne contient aucun secret."],
        ["IF-NS-03, vers VNet/SDN",
         "view_tag matérialise le profil de résolution et la liste de contrôle "
         "d'accès associée au tenant."],
        ["IF-NS-05, vers Backend par l'agent",
         "forward_zone et reverse_zone désignent les deux zones à modifier lors "
         "d'une publication ou d'un retrait."],
    ]
    add(make_table(["Interface", "Usage du profil"], rows, [CW * 0.26, CW * 0.74]))
    add(caption("Tableau 2.5  Consommation du profil DNS par les interfaces du lot "
                "Services Network"))
    add(P("Un second profil, admin-v1, désigne les mêmes résolveurs avec le "
          "domaine de recherche infra.gandal.internal et l'étiquette de vue 1. Il "
          "s'applique aux machines du plan de gestion et au pool VPN "
          "administrateur."))

    # =================================================================
    # CHAPITRE 3
    # =================================================================
    ext(chapter(doc, "3", "Isolation et confidentialité des noms"))

    add(P("3.1  Expression du besoin et scénarios à empêcher", "h2"))
    add(P("L'exigence NET-FR-008 porte sur la confidentialité des noms entre "
          "domaines. Le document 03 la précise sans ambiguïté : le mécanisme de "
          "résolution doit empêcher la lecture d'une zone d'infrastructure ou d'un "
          "autre tenant par les clients non autorisés, et cacher un enregistrement "
          "dans le portail ne suffit pas. Le test S04 formule la vérification "
          "attendue : depuis une machine du VNet USER, une requête vers la zone "
          "d'infrastructure et vers la zone d'un tenant voisin doit se solder par "
          "un refus ou une absence d'information."))
    add(P("Trois scénarios doivent être couverts, et chacun appelle une "
          "contre-mesure distincte."))
    add(Spacer(1, 3))
    rows = [
        ["Interrogation directe d'un serveur autoritatif par une machine tenant",
         "Le serveur autoritatif répondrait pour toute zone hébergée, y compris "
         "celles des autres tenants.",
         "Filtrage réseau : les adresses 10.30.4.10 et 10.30.4.11 ne sont pas "
         "joignables depuis un VNet tenant (section 3.3)."],
        ["Transfert de zone demandé par un client quelconque",
         "Un transfert divulgue l'intégralité d'une zone en une requête.",
         "Transferts restreints à ns2 par adresse et signés par une clé TSIG "
         "(section 4.2)."],
        ["Requête vers une zone étrangère au travers du résolveur partagé",
         "Le résolveur résout toutes les zones internes pour tous ses clients.",
         "Politique de sélection des zones indexée sur l'adresse source "
         "(section 3.2)."],
    ]
    add(make_table(["Scénario", "Ce qui serait divulgué", "Contre-mesure retenue"],
                   rows, [CW * 0.3, CW * 0.33, CW * 0.37]))
    add(caption("Tableau 3.1  Scénarios de divulgation et contre-mesures"))
    add(P("Une énumération par requêtes successives reste théoriquement possible "
          "à l'intérieur de la vue d'un tenant, c'est-à-dire sur ses propres noms. "
          "Ce résidu est accepté : il ne franchit aucune frontière de tenant."))

    add(P("3.2  Politique de sélection des zones par adresse source", "h2"))
    add(P("Les deux options ouvertes par le document 03 sont de séparer "
          "physiquement les points de résolution par tenant, ou d'appliquer une "
          "politique démontrée de sélection des zones. La première option "
          "supposerait cinquante paires de résolveurs, ce que le matériel "
          "disponible exclut. La seconde est donc retenue."))
    add(P("Son principe est direct. Le plan d'adressage associe le tenant n au "
          "préfixe 10.30.(63+n).0/24. L'adresse source d'une requête détermine donc "
          "sans ambiguïté le tenant émetteur, et par conséquent les deux seules "
          "zones internes qu'il est autorisé à résoudre : sa zone directe et sa "
          "zone inverse. Toute autre demande portant sur l'espace interne reçoit un "
          "code REFUSED, qui ne révèle pas l'existence du nom demandé, contrairement "
          "à une réponse NXDOMAIN."))
    add(Spacer(1, 4))
    add(NoteBox("Point de conception critique : où placer le contrôle", [
        "Une vérification placée dans le seul point d'entrée de résolution serait "
        "insuffisante. Le résolveur consulte son cache paquet avant d'engager la "
        "résolution : une réponse construite pour un tenant pourrait être "
        "restituée telle quelle à un autre, et la politique serait contournée par "
        "le cache lui-même.",
        "La fonction gettag() est évaluée avant toute consultation de cache et sa "
        "valeur de retour entre dans la clé du cache paquet. Le contrôle est donc "
        "construit en deux temps : gettag() calcule l'étiquette de vue à partir de "
        "l'adresse source, puis preresolve() applique la règle en s'appuyant sur "
        "cette étiquette. Deux vues distinctes ne peuvent alors jamais partager une "
        "entrée de cache."], accent=GOLD, bg=colors.HexColor("#FAF5EA")))
    add(Spacer(1, 6))
    add(FigureBox(F.fig_chemin()))
    add(caption("Figure 3.1  Chemin d'une requête issue d'une machine tenant et points "
                "d'application de la politique"))

    rows = [
        ["1", "Plan de gestion 10.30.0.0/24, VNet Services 10.30.4.0/24, "
              "Monitoring 10.30.5.0/24, pool VPN administrateur 10.30.16.32/28",
         "Vue administration : résolution de l'ensemble de l'espace interne et de "
         "l'espace public."],
        ["1000 + n", "Préfixe du tenant n, soit 10.30.(63+n).0/24",
         "Zone directe tenant-0NN.gandal.internal, zone inverse "
         "(63+n).30.10.in-addr.arpa, et espace public."],
        ["999", "Toute autre source acceptée par allow-from, notamment le pool "
                "VPN utilisateur 10.30.16.16/28",
         "Espace public uniquement ; tout nom interne reçoit REFUSED."],
        ["aucune", "Source hors allow-from",
         "La requête n'est pas traitée par le résolveur."],
    ]
    add(make_table(["Étiquette", "Adresses source", "Portée de résolution"],
                   rows, [CW * 0.12, CW * 0.41, CW * 0.47]))
    add(caption("Tableau 3.2  Vues définies par la politique de sélection des zones"))

    add(P("3.3  Filtrage réseau et matrice de flux", "h2"))
    add(P("La politique applicative ne remplace pas le filtrage. Les règles "
          "suivantes complètent les politiques de référence du document 02 et "
          "sont appliquées sur les passerelles pfSense des VNets concernés, "
          "conformément aux interfaces IF-INT-05 et IF-INT-07."))
    add(Spacer(1, 3))
    rows = [
        ["VNet tenant 10.30.(63+n).0/24", "10.30.4.12, 10.30.4.13", "UDP et TCP 53",
         "Autoriser", "Seul point de résolution offert aux tenants"],
        ["VNet tenant", "10.30.4.10, 10.30.4.11", "tout", "Refuser et journaliser",
         "Les autoritatifs ne sont pas exposés aux tenants"],
        ["VNet tenant", "10.30.0.0/24", "tout", "Refuser",
         "Règle existante du document 02, rappelée ici"],
        ["10.30.4.12, 10.30.4.13", "10.30.4.10, 10.30.4.11", "UDP et TCP 53",
         "Autoriser", "Redirection de zone interne"],
        ["10.30.4.12, 10.30.4.13", "Internet", "UDP et TCP 53", "Autoriser via PF-WAN",
         "Récursion sur l'espace public, journalisée"],
        ["10.30.4.11 (ns2)", "10.30.4.10 (ns1)", "TCP 53", "Autoriser",
         "Transfert de zone signé TSIG"],
        ["10.30.4.10 (ns1)", "10.30.4.11 (ns2)", "UDP 53", "Autoriser",
         "Message NOTIFY"],
        ["10.30.4.41 (agent)", "10.30.4.10", "TCP 8443", "Autoriser",
         "API autoritative derrière terminaison TLS"],
        ["10.30.4.41 (agent)", "ns1, ns2, rec1, rec2", "UDP et TCP 53", "Autoriser",
         "Contrôle de publication sur les quatre instances"],
        ["10.30.0.0/24, 10.30.16.32/28", "10.30.4.12, 10.30.4.13", "UDP et TCP 53",
         "Autoriser", "Vue administration"],
        ["10.30.16.16/28 (VPN utilisateur)", "10.30.4.12, 10.30.4.13",
         "UDP et TCP 53", "Autoriser",
         "Admis par allow-from, mais limité à l'espace public par la vue 999 "
         "(section 3.4)"],
        ["10.30.5.10 (Monitoring)", "ns1, ns2, rec1, rec2", "TCP 8443",
         "Autoriser", "Lecture des métriques, initiée par Monitoring"],
        ["ns1, ns2, rec1, rec2", "10.30.5.0/24", "tout", "Refuser",
         "Aucune initiation vers Monitoring, conformément à IF-NS-08"],
        ["Toute autre source", "ns1, ns2, rec1, rec2", "tout", "Refuser",
         "Refus par défaut"],
    ]
    add(make_table(["Source", "Destination", "Service", "Décision", "Motif"],
                   rows, [CW * 0.21, CW * 0.17, CW * 0.13, CW * 0.16, CW * 0.33]))
    add(caption("Tableau 3.3  Matrice de flux du service DNS"))
    add(P("Deux points méritent attention. Le refus du trafic des tenants vers les "
          "autoritatifs doit être journalisé : une hausse de ce compteur signale "
          "soit une erreur de distribution des résolveurs, soit une tentative "
          "délibérée. Par ailleurs, le port 53 doit être ouvert en TCP autant qu'en "
          "UDP, faute de quoi toute réponse tronquée deviendrait irrécupérable, "
          "avec un symptôme limité à certaines requêtes seulement."))

    add(P("3.4  Cas particulier des profils VPN", "h2"))
    add(P("L'exigence NET-FR-017 demande que le DNS soit accessible selon le "
          "profil VPN. Le plan d'adressage distingue trois pools : administrateur "
          "en 10.30.16.32/28, utilisateur en 10.30.16.16/28 et site à site en "
          "10.30.16.48/28, les deux derniers étant classés en extension."))
    add(P("Le pool administrateur ne pose pas de difficulté : il est traité comme "
          "le plan de gestion et reçoit la vue administration, sous réserve de "
          "l'autorisation délivrée par IAM au moment de l'ouverture de session."))
    add(P("Le pool utilisateur pose en revanche un problème de conception qu'il "
          "faut énoncer plutôt que masquer. Une politique fondée sur l'adresse "
          "source ne peut pas distinguer deux utilisateurs de tenants différents "
          "qui reçoivent leur adresse d'un même pool partagé de quatorze adresses. "
          "Trois réponses sont possibles."))
    ext(numbered([
        "Attribuer une sous-plage distincte par tenant, ce que la taille du pool "
        "actuel ne permet pas pour cinquante tenants.",
        "Faire porter l'identité du tenant par le concentrateur VPN, qui "
        "attribuerait une adresse stable par session et transmettrait la "
        "correspondance au résolveur, au titre de l'interface IF-EXT-07.",
        "Refuser toute résolution interne au pool utilisateur et médier les accès "
        "par le Backend, conformément à IF-EXT-06.",
    ]))
    add(P("La troisième réponse est retenue pour le périmètre minimal, parce "
          "qu'elle est la seule applicable sans donnée supplémentaire et parce "
          "qu'elle est cohérente avec le statut d'extension du pool utilisateur. "
          "L'étiquette 999 du tableau 3.2 matérialise ce refus. La deuxième réponse "
          "constitue l'évolution naturelle dès que la correspondance session vers "
          "tenant sera fournie."))

    # =================================================================
    # CHAPITRE 4
    # =================================================================
    ext(chapter(doc, "4", "Configurations de référence"))

    add(P("Les configurations de ce chapitre sont complètes et cohérentes entre "
          "elles. Elles correspondent à la branche 4.9 de PowerDNS Authoritative "
          "et à la branche 5 de PowerDNS Recursor. Deux précautions de version "
          "s'imposent avant application : les directives primary et secondary "
          "remplacent les anciennes directives master et slave depuis la version "
          "4.5, et la branche 5 du résolveur introduit un format YAML équivalent au "
          "format classique employé ici. Le format attendu par la version "
          "effectivement installée doit être vérifié."))

    add(P("4.1  Serveurs autoritatifs ns1 et ns2", "h2"))
    add(CodeBlock("""
# /etc/powerdns/pdns.conf
# GANDAL T005 : ns1, serveur autoritatif primaire, 10.30.4.10, hote H1

# --- stockage : volume faible, replication assuree par transfert de zone
launch=gsqlite3
gsqlite3-database=/var/lib/powerdns/pdns.sqlite3

# --- ecoute restreinte a l'adresse de service du VNet Services
local-address=10.30.4.10
local-port=53

# --- role
primary=yes
secondary=no

# --- replication : ns2 est le seul destinataire et le seul demandeur autorise
allow-axfr-ips=10.30.4.11/32
only-notify=10.30.4.11
also-notify=10.30.4.11

# --- valeurs par defaut des zones creees
default-ttl=3600
default-soa-content=ns1.gandal.internal hostmaster.gandal.internal 0 3600 900 604800 300

# --- transport : rester sous la MTU utile de 1450 octets imposee par VXLAN
udp-truncation-threshold=1232
max-tcp-connections=50

# --- discretion et isolement
version-string=anonymous
security-poll-suffix=

# --- API locale ; la terminaison TLS est assuree par le mandataire (section 4.5)
webserver=yes
webserver-address=127.0.0.1
webserver-port=8081
webserver-allow-from=127.0.0.1/32
api=yes
api-key=$PDNS_API_KEY_NS1

# --- journalisation
loglevel=4
log-dns-queries=no
log-dns-details=yes

# --- execution sous systemd
setuid=pdns
setgid=pdns
daemon=no
guardian=no
"""))
    add(Paragraph("Listing 4.1  Configuration du serveur autoritatif primaire ns1",
                  S["capcode"]))
    add(Spacer(1, 3))
    add(P("Quatre directives appellent un commentaire. La journalisation des "
          "requêtes est désactivée sur l'autoritatif : ses clients légitimes sont "
          "au nombre de quatre et l'identité réelle du demandeur n'y est pas "
          "visible, puisque les requêtes arrivent par le résolveur. La "
          "journalisation utile est placée sur le résolveur, où l'adresse source "
          "est celle du client. La directive security-poll-suffix vidée désactive "
          "la vérification périodique de version auprès d'un domaine externe, "
          "requête inutile et indésirable dans un environnement fermé. La "
          "directive version-string masque la version du logiciel dans la réponse "
          "à version.bind. Enfin, la clé d'API n'est pas écrite dans le fichier : "
          "elle est injectée dans l'environnement du service au démarrage, depuis "
          "le magasin de secrets. À partir de la version 4.7, la directive api-key "
          "accepte également une empreinte produite par la commande pdnsutil "
          "hash-password, ce qui évite toute forme en clair."))
    add(Spacer(1, 5))
    add(CodeBlock("""
# /etc/powerdns/pdns.conf
# GANDAL T005 : ns2, serveur autoritatif secondaire, 10.30.4.11, hote H3
# Seules les directives qui different de ns1 sont reproduites.

local-address=10.30.4.11

primary=no
secondary=yes

# --- ns1 est la seule source de NOTIFY et de transfert acceptee
allow-notify-from=10.30.4.10/32
xfr-cycle-interval=60
xfr-max-received-mbytes=50

# --- aucun transfert sortant : ns2 ne sert de source a personne
allow-axfr-ips=

api-key=$PDNS_API_KEY_NS2
"""))
    add(Paragraph("Listing 4.2  Écarts de configuration du serveur autoritatif "
                  "secondaire ns2", S["capcode"]))
    add(P("La directive allow-axfr-ips laissée vide ferme toute possibilité de "
          "transfert depuis ns2. L'API de ns2 reste active pour la supervision et "
          "l'inspection locale, mais le mandataire placé devant elle n'autorise "
          "que la méthode GET, de sorte que le propriétaire d'écriture reste "
          "unique au sens de la section 5.1."))

    add(P("4.2  Création des zones et des clés de transfert", "h2"))
    add(P("La clé de transfert est unique parce que l'unique transfert du "
          "dispositif va de ns1 vers ns2. Le document 03 évoque des clés TSIG "
          "limitées par zone : cette granularité devient nécessaire dans la "
          "variante où les mises à jour dynamiques du RFC 2136 seraient employées, "
          "chaque émetteur ne devant alors pouvoir modifier que sa propre zone. "
          "Cette variante n'est pas retenue, comme l'explique la section 5.1."))
    add(CodeBlock("""
# --- sur ns1 : generation de la cle de transfert
pdnsutil generate-tsig-key gandal-xfr hmac-sha256
# la valeur produite est deposee dans le magasin de secrets, jamais dans Git

# --- zone racine interne et identites des serveurs
pdnsutil create-zone gandal.internal ns1.gandal.internal
pdnsutil add-record  gandal.internal @   NS 3600 ns2.gandal.internal.
pdnsutil add-record  gandal.internal ns1 A  3600 10.30.4.10
pdnsutil add-record  gandal.internal ns2 A  3600 10.30.4.11
pdnsutil add-record  gandal.internal rec1 A 3600 10.30.4.12
pdnsutil add-record  gandal.internal rec2 A 3600 10.30.4.13

# --- zone d'infrastructure, puis sa delegation depuis la zone parente
pdnsutil create-zone infra.gandal.internal ns1.gandal.internal
pdnsutil add-record  infra.gandal.internal @ NS 3600 ns2.gandal.internal.
pdnsutil add-record  gandal.internal infra NS 3600 ns1.gandal.internal.
pdnsutil add-record  gandal.internal infra NS 3600 ns2.gandal.internal.

# --- inventaire d'infrastructure, extrait
pdnsutil add-record infra.gandal.internal h1      A 3600 10.30.0.11
pdnsutil add-record infra.gandal.internal h2      A 3600 10.30.0.12
pdnsutil add-record infra.gandal.internal h3      A 3600 10.30.0.13
pdnsutil add-record infra.gandal.internal xo      A 3600 10.30.0.20
pdnsutil add-record infra.gandal.internal bastion A 3600 10.30.0.21
pdnsutil add-record infra.gandal.internal kea1    A 3600 10.30.4.20
pdnsutil add-record infra.gandal.internal kea2    A 3600 10.30.4.21
pdnsutil add-record infra.gandal.internal ntp1    A 3600 10.30.4.30
pdnsutil add-record infra.gandal.internal ntp2    A 3600 10.30.4.31
pdnsutil add-record infra.gandal.internal ipam    A 3600 10.30.4.40
pdnsutil add-record infra.gandal.internal agent   A 3600 10.30.4.41

# --- zones inverses d'infrastructure
for O in 0 1 2 4 5 6 7 8 10 16 17 ; do
  pdnsutil create-zone "${O}.30.10.in-addr.arpa" ns1.gandal.internal
  pdnsutil add-record  "${O}.30.10.in-addr.arpa" @ NS 3600 ns2.gandal.internal.
done

# --- cinquante tenants : zone directe, zone inverse et delegation
for N in $(seq 1 50) ; do
  T=$(printf 'tenant-%03d' "$N")
  O=$(( 63 + N ))
  pdnsutil create-zone "${T}.gandal.internal" ns1.gandal.internal
  pdnsutil add-record  "${T}.gandal.internal" @  NS 3600 ns2.gandal.internal.
  pdnsutil add-record  "${T}.gandal.internal" gw A  3600 "10.30.${O}.1"
  pdnsutil create-zone "${O}.30.10.in-addr.arpa" ns1.gandal.internal
  pdnsutil add-record  "${O}.30.10.in-addr.arpa" @ NS  3600 ns2.gandal.internal.
  pdnsutil add-record  "${O}.30.10.in-addr.arpa" 1 PTR 3600 "gw.${T}.gandal.internal."
  pdnsutil add-record  gandal.internal "$T" NS 3600 ns1.gandal.internal.
  pdnsutil add-record  gandal.internal "$T" NS 3600 ns2.gandal.internal.
done

# --- transfert signe et increment automatique du numero de serie par l'API
for Z in $(pdnsutil list-all-zones) ; do
  pdnsutil set-meta "$Z" TSIG-ALLOW-AXFR gandal-xfr
  pdnsutil set-meta "$Z" SOA-EDIT-API    DEFAULT
done

# --- controle de coherence avant mise en service
pdnsutil rectify-all-zones
pdnsutil check-all-zones
"""))
    add(Paragraph("Listing 4.3  Création de l'espace de nommage sur ns1", S["capcode"]))
    add(Spacer(1, 3))
    add(CodeBlock("""
# --- sur ns2 : import de la meme cle, puis declaration des zones secondaires
pdnsutil import-tsig-key gandal-xfr hmac-sha256 "$TSIG_GANDAL_XFR"

for Z in $(cat /etc/gandal/zones.list) ; do
  pdnsutil create-secondary-zone "$Z" 10.30.4.10
  pdnsutil activate-tsig-key     "$Z" gandal-xfr secondary
done
"""))
    add(Paragraph("Listing 4.4  Déclaration des zones secondaires sur ns2", S["capcode"]))
    add(P("La métadonnée SOA-EDIT-API fixée à DEFAULT fait incrémenter le numéro de "
          "série à chaque modification reçue par l'API. C'est cette incrémentation "
          "qui déclenche le message NOTIFY et le transfert vers ns2 ; sans elle, "
          "les deux serveurs divergeraient silencieusement."))

    add(P("4.3  Résolveurs récursifs rec1 et rec2", "h2"))
    add(CodeBlock("""
# /etc/powerdns/recursor.conf
# GANDAL T005 : rec1, resolveur recursif, 10.30.4.12, hote H2
# rec2 est identique, avec local-address=10.30.4.13 sur l'hote H1

local-address=10.30.4.12
local-port=53
threads=2
pdns-distributes-queries=no

# --- clients autorises : strictement les prefixes du plan 02
allow-from=10.30.0.0/24, 10.30.4.0/24, 10.30.5.0/24, 10.30.6.0/24, 10.30.7.0/24,
           10.30.8.0/24, 10.30.16.16/28, 10.30.16.32/28, 10.30.64.0/18

# --- espace interne : redirection vers les serveurs autoritatifs
forward-zones=gandal.internal=10.30.4.10;10.30.4.11
forward-zones+=30.10.in-addr.arpa=10.30.4.10;10.30.4.11

# Sans cette directive, le resolveur servirait localement les zones inverses
# privees du RFC 6303 et court-circuiterait la redirection ci-dessus.
serve-rfc1918=no

# --- validation DNSSEC de l'espace public, exception traitee dans le fichier Lua
dnssec=validate
lua-config-file=/etc/powerdns/recursor-config.lua

# --- politique de selection des zones (section 4.4)
lua-dns-script=/etc/powerdns/views.lua

# --- transport : rester sous la MTU utile de 1450 octets imposee par VXLAN
edns-outgoing-bufsize=1232
udp-truncation-threshold=1232
qname-minimization=yes

# --- cache dimensionne pour 4 GiB de memoire
max-cache-entries=500000
max-packetcache-entries=250000
max-cache-ttl=86400
max-negative-ttl=300

# --- discretion et isolement
version-string=anonymous
security-poll-suffix=
export-etc-hosts=no

# --- point de metriques, expose par le mandataire (section 4.5)
webserver=yes
webserver-address=127.0.0.1
webserver-port=8082
webserver-allow-from=127.0.0.1/32
api-key=$PDNS_REC_API_KEY

loglevel=4
"""))
    add(Paragraph("Listing 4.5  Configuration du résolveur récursif rec1",
                  S["capcode"]))
    add(Spacer(1, 3))
    add(P("La directive serve-rfc1918 mérite d'être soulignée. Par défaut, le "
          "résolveur se déclare autoritatif et vide pour les zones inverses des "
          "espaces privés, afin d'éviter des requêtes inutiles vers la racine. "
          "Dans GANDAL, ce comportement empêcherait toute résolution inverse "
          "interne. Il est donc désactivé et remplacé par une redirection "
          "explicite de 30.10.in-addr.arpa vers les autoritatifs."))
    add(P("La directive export-etc-hosts est maintenue à la valeur non : le fichier "
          "hosts local des résolveurs contient le socle de secours décrit à la "
          "section 5.4, qui n'a pas vocation à être publié et qui pourrait entrer "
          "en contradiction avec les zones autoritatives."))
    add(Spacer(1, 5))
    add(CodeBlock("""
-- /etc/powerdns/recursor-config.lua
-- Charge par la directive lua-config-file.

-- Le domaine de premier niveau "internal" est reserve a l'usage prive et n'est
-- pas delegue dans la racine publique. Avec dnssec=validate, le resolveur
-- obtiendrait de la racine une preuve signee de son inexistence et declarerait
-- toute reponse interne invalide. L'exception locale ci-dessous suspend la
-- validation sous cette branche, et sous elle seulement.
addNTA("internal.", "espace de nommage interne GANDAL, non delegue et non signe")

-- Aucune exception n'est necessaire pour 10.in-addr.arpa : cette branche est
-- deleguee sans enregistrement DS dans l'arbre public, donc deja non signee.

-- Journalisation structuree vers un collecteur local du VNet Services.
-- Monitoring lit ensuite les fichiers produits en pull (IF-NS-08).
dnstapFrameStreamServer({"/var/run/pdns-recursor/dnstap.sock"})
"""))
    add(Paragraph("Listing 4.6  Configuration Lua du résolveur : exception de "
                  "validation et journalisation", S["capcode"]))

    add(P("4.4  Script de politique de vue", "h2"))
    add(P("Le script ci-dessous met en œuvre les vues du tableau 3.2. Il est "
          "volontairement court et sans accès externe : il s'exécute pour chaque "
          "requête et toute opération coûteuse s'y traduirait directement en "
          "latence de résolution."))
    add(CodeBlock("""
-- /etc/powerdns/views.lua
-- Politique de selection des zones par adresse source.
-- Exigences couvertes : NET-FR-008, IF-NS-03 ; scenario de test S04.

local ZONE_RACINE = "gandal.internal"
local SUFFIXE_INV = "30.10.in-addr.arpa"

local TAG_ADMIN = 1     -- gestion, services, monitoring, VPN administrateur
local TAG_REFUS = 999   -- source autorisee mais sans vue interne

local reseauxAdmin = newNMG()
reseauxAdmin:addMask("10.30.0.0/24")
reseauxAdmin:addMask("10.30.4.0/24")
reseauxAdmin:addMask("10.30.5.0/24")
reseauxAdmin:addMask("10.30.16.32/28")

local reseauxTenant = newNMG()
reseauxTenant:addMask("10.30.64.0/18")

-- Plan 02 : le tenant n occupe 10.30.(63+n).0/24, pour 1 <= n <= 50.
local function numeroTenant(adresse)
  local o3 = tonumber(adresse:toString():match("^10%.30%.(%d+)%.%d+$"))
  if o3 == nil or o3 < 64 or o3 > 113 then return nil end
  return o3 - 63
end

-- gettag() est evalue avant toute consultation de cache et sa valeur entre
-- dans la cle du cache paquet : deux vues ne partagent jamais une reponse.
function gettag(remote, ednssubnet, localip, qname, qtype, ednsoptions, tcp)
  if reseauxAdmin:match(remote) then return TAG_ADMIN end
  if reseauxTenant:match(remote) then
    local n = numeroTenant(remote)
    if n ~= nil then return 1000 + n end
  end
  return TAG_REFUS
end

local function sousDomaine(nom, zone)
  return nom == zone or nom:sub(-(#zone + 1)) == ("." .. zone)
end

function preresolve(dq)
  local nom     = dq.qname:toStringNoDot():lower()
  local interne = sousDomaine(nom, ZONE_RACINE)
  local inverse = sousDomaine(nom, SUFFIXE_INV)

  -- Les noms publics suivent la recursion ordinaire, quelle que soit la vue.
  if not interne and not inverse then return false end

  if dq.tag == TAG_ADMIN then return false end

  if dq.tag > 1000 then
    local n           = dq.tag - 1000
    local zoneDirecte = string.format("tenant-%03d.%s", n, ZONE_RACINE)
    local zoneInverse = string.format("%d.%s", n + 63, SUFFIXE_INV)
    if sousDomaine(nom, zoneDirecte) or sousDomaine(nom, zoneInverse) then
      return false
    end
  end

  -- REFUSED plutot que NXDOMAIN : le refus ne revele pas l'existence du nom.
  dq.rcode = pdns.REFUSED
  return true
end
"""))
    add(Paragraph("Listing 4.7  Politique de sélection des zones appliquée sur rec1 "
                  "et rec2", S["capcode"]))
    add(P("Le script refuse également l'apex gandal.internal aux sources tenant, "
          "ce qui empêche l'énumération des délégations et donc la découverte de "
          "la liste des tenants. Il laisse en revanche passer sans traitement "
          "toute requête portant sur un nom public, afin de ne pas pénaliser le "
          "cas le plus fréquent."))

    add(P("4.5  Exposition de l'API et des métriques", "h2"))
    add(P("Le serveur HTTP intégré à PowerDNS ne fournit pas de terminaison TLS. "
          "L'exigence NET-FR-016, qui demande des API administratives chiffrées, "
          "est donc satisfaite en liant ce serveur à la boucle locale et en plaçant "
          "devant lui un mandataire qui assure le chiffrement et le contrôle "
          "d'accès par adresse."))
    add(CodeBlock("""
# /etc/nginx/conf.d/pdns-api.conf  sur ns1 (10.30.4.10)

server {
    listen 10.30.4.10:8443 ssl;
    server_name ns1.gandal.internal;

    ssl_certificate     /etc/ssl/gandal/ns1.crt;   # PKI interne, IF-EXT-01
    ssl_certificate_key /etc/ssl/gandal/ns1.key;
    ssl_protocols       TLSv1.2 TLSv1.3;

    # Seul l'agent reseau publie des enregistrements.
    location /api/ {
        allow 10.30.4.41/32;
        deny  all;
        proxy_pass http://127.0.0.1:8081;
    }

    # Seul Monitoring lit les metriques, et il en est l'initiateur.
    location = /metrics {
        allow 10.30.5.10/32;
        deny  all;
        proxy_pass http://127.0.0.1:8081/metrics;
    }

    location / { return 404; }
}

# Sur ns2, le bloc /api/ est complete par la restriction suivante, qui
# garantit l'unicite du proprietaire d'ecriture :
#     limit_except GET { deny all; }
#
# Sur rec1 et rec2, seul le bloc /metrics est publie, vers 127.0.0.1:8082.
"""))
    add(Paragraph("Listing 4.8  Terminaison TLS et contrôle d'accès devant l'API "
                  "autoritative", S["capcode"]))
    add(P("Ce montage répond également à l'interface IF-NS-08 : les quatre "
          "instances n'ouvrent aucune connexion vers Monitoring, qui vient lire "
          "leur point de métriques. La limitation de débit en réponse n'est pas "
          "activée sur les serveurs autoritatifs, et cette absence est délibérée : "
          "PowerDNS Authoritative n'intègre pas cette fonction, et le risque "
          "d'amplification qu'elle traite suppose une exposition publique que la "
          "matrice de flux interdit. Si cette exposition devait changer, un "
          "répartiteur DNS spécialisé devrait être placé en amont."))

    # =================================================================
    # CHAPITRE 5
    # =================================================================
    ext(chapter(doc, "5", "Cycle de vie des enregistrements et exploitation"))

    add(P("5.1  Propriétaire d'écriture unique et séquence de publication", "h2"))
    add(P("Le document 03 pose une règle explicite : ne choisir qu'un propriétaire "
          "d'écriture par enregistrement. Il ouvre deux pistes, la mise à jour "
          "dynamique issue de Kea au moyen du RFC 2136, ou la mise à jour par "
          "l'agent au travers de l'API autoritative."))
    add(Spacer(1, 3))
    rows = [
        ["Mise à jour par l'agent via l'API autoritative",
         "Un seul émetteur pour toutes les zones. La modification porte sur un "
         "RRset complet, ce qui rend l'opération naturellement convergente. Le "
         "retour d'API fournit un état exploitable par la machine d'états et "
         "corrélable à un operation_id.",
         "Ajoute une dépendance à la disponibilité de l'agent pour toute "
         "publication.", "<b>Retenue</b>"],
        ["Mise à jour dynamique RFC 2136 déclenchée par Kea",
         "Rapproche la publication de l'attribution du bail et supprime un "
         "intermédiaire.",
         "Introduit un second émetteur, donc un conflit possible de propriété sur "
         "les mêmes enregistrements. Exige une clé TSIG par zone, soit "
         "cent-treize clés à gérer, et une compatibilité du moteur de stockage "
         "qui reste à vérifier.", "Alternative documentée"],
    ]
    add(make_table(["Option", "Apport", "Limite", "Décision"], rows,
                   [CW * 0.22, CW * 0.3, CW * 0.33, CW * 0.15]))
    add(caption("Tableau 5.1  Arbitrage du mécanisme de mise à jour"))
    add(Spacer(1, 6))
    add(FigureBox(F.fig_sequence()))
    add(caption("Figure 5.1  Séquence de publication d'un enregistrement et branche "
                "dégradée"))
    add(P("Les deux appels ci-dessous constituent le contrat que l'agent doit "
          "respecter. Ils sont donnés pour une machine du tenant 7 recevant "
          "l'adresse 10.30.70.37, qui appartient bien au pool dynamique .10 à "
          ".199 défini par le document 02."))
    add(CodeBlock("""
PATCH /api/v1/servers/localhost/zones/tenant-007.gandal.internal.  HTTP/1.1
Host: ns1.gandal.internal:8443
X-API-Key: <cle injectee depuis le magasin de secrets>
Content-Type: application/json

{
  "rrsets": [{
    "name": "vm-0042.tenant-007.gandal.internal.",
    "type": "A",
    "ttl": 300,
    "changetype": "REPLACE",
    "records": [ { "content": "10.30.70.37", "disabled": false } ],
    "comments": [ { "account": "agent",
                    "content": "operation_id=7f3c..., lease_id=..." } ]
  }]
}

PATCH /api/v1/servers/localhost/zones/70.30.10.in-addr.arpa.  HTTP/1.1

{
  "rrsets": [{
    "name": "37.70.30.10.in-addr.arpa.",
    "type": "PTR",
    "ttl": 300,
    "changetype": "REPLACE",
    "records": [ { "content": "vm-0042.tenant-007.gandal.internal.",
                   "disabled": false } ]
  }]
}
"""))
    add(Paragraph("Listing 5.1  Publication conjointe de l'enregistrement direct et "
                  "de l'enregistrement inverse", S["capcode"]))
    add(P("La publication n'est pas considérée comme acquise à la réception du "
          "code 204. L'agent interroge ensuite ns1, ns2, rec1 et rec2 pour le nom "
          "publié et ne fait progresser l'opération vers l'état SERVICES_READY "
          "qu'après concordance des quatre réponses. Ce contrôle détecte en "
          "particulier un transfert de zone bloqué, défaut qui resterait sinon "
          "invisible jusqu'à la première panne de ns1."))

    add(P("5.2  Idempotence, rejeu et réconciliation", "h2"))
    add(P("L'exigence NET-NFR-006 demande un rejeu déterministe et idempotent. "
          "Le choix d'un changement de type REPLACE portant sur un RRset complet "
          "y répond par construction : l'état final ne dépend pas du nombre "
          "d'exécutions. Une précaution reste nécessaire."))
    add(NoteBox("Précaution sur le rejeu", [
        "Une modification par l'API incrémente le numéro de série de la zone, y "
        "compris lorsque le contenu soumis est identique à celui déjà publié. Un "
        "rejeu systématique provoquerait donc autant de transferts de zone "
        "inutiles vers ns2.",
        "L'agent doit par conséquent lire le RRset avant de l'écrire et "
        "n'émettre la modification que si le contenu diffère. Le rejeu reste "
        "correct dans tous les cas, mais il devient également économe."]))
    add(P("Une réconciliation périodique compare les allocations enregistrées dans "
          "l'IPAM aux enregistrements effectivement publiés, dans les deux sens. "
          "Elle signale les divergences sans les corriger automatiquement : une "
          "correction automatique sur un état mal compris est le moyen le plus "
          "rapide de propager une erreur à l'ensemble des zones. Deux familles de "
          "divergence sont attendues, l'enregistrement publié sans allocation "
          "correspondante, trace d'une suppression incomplète, et l'allocation "
          "active sans enregistrement, trace d'une publication interrompue."))

    add(P("5.3  Suppression, quarantaine et mode dégradé", "h2"))
    add(P("L'ordre de suppression est l'inverse de l'ordre de publication et il "
          "n'est pas interchangeable. Le document 03 impose d'attendre le retrait "
          "des interfaces virtuelles et la fin des références avant libération, et "
          "précise qu'une panne DNS ne libère pas une adresse encore utilisée."))
    ext(numbered([
        "Retrait de l'interface virtuelle de la machine et fin du bail.",
        "Suppression des enregistrements A et PTR par un changement de type "
        "DELETE sur les deux zones concernées.",
        "Attente de la durée de quarantaine, fixée à 900 secondes et supérieure à "
        "la durée de vie des enregistrements supprimés.",
        "Retour de l'adresse au pool par l'IPAM.",
    ]))
    add(P("Si la suppression des enregistrements échoue, l'adresse n'est pas "
          "rendue au pool et l'opération reste dans l'état DELETING, observable. "
          "Le comportement symétrique s'applique à la publication : une panne de "
          "l'API ou des serveurs autoritatifs laisse l'opération en cours, "
          "signalée par une alerte, sans que l'adresse déjà attribuée soit "
          "considérée comme libre. Le trafic des machines déjà configurées n'est "
          "pas interrompu : seules les opérations nouvelles sont suspendues. "
          "Cette distinction est précisément ce que le test G04 doit établir."))

    add(P("5.4  Amorçage, ordre de reprise et adresses de secours", "h2"))
    add(P("Le document Underlay insiste sur la rupture des cycles de démarrage : "
          "si le serveur DNS et le bastion dépendent uniquement d'un ensemble dont "
          "l'accès suppose ces mêmes services, une panne générale rend la "
          "restauration difficile. Le socle minimal ci-dessous doit donc être "
          "présent sur les trois hôtes, sur XO, sur le bastion et sur les machines "
          "de services."))
    add(CodeBlock("""
# /etc/hosts  : socle de reprise GANDAL
# Permet d'administrer et de reconstruire l'infrastructure sans dependre
# du service DNS lui-meme. Non publie : voir export-etc-hosts=no.

127.0.0.1    localhost
10.30.0.11   h1.infra.gandal.internal         h1
10.30.0.12   h2.infra.gandal.internal         h2
10.30.0.13   h3.infra.gandal.internal         h3
10.30.0.20   xo.infra.gandal.internal         xo
10.30.0.21   bastion.infra.gandal.internal    bastion
10.30.4.10   ns1.gandal.internal              ns1
10.30.4.11   ns2.gandal.internal              ns2
10.30.4.12   rec1.gandal.internal             rec1
10.30.4.13   rec2.gandal.internal             rec2
10.30.4.20   kea1.infra.gandal.internal       kea1
10.30.4.21   kea2.infra.gandal.internal       kea2
10.30.4.30   ntp1.infra.gandal.internal       ntp1
10.30.4.31   ntp2.infra.gandal.internal       ntp2
10.30.4.40   ipam.infra.gandal.internal       ipam
10.30.4.41   agent.infra.gandal.internal      agent
"""))
    add(Paragraph("Listing 5.2  Adresses de secours à conserver hors du service DNS",
                  S["capcode"]))
    add(Spacer(1, 3))
    rows = [
        ["1", "Transport et hôtes", "Aucune", "Les hyperviseurs se joignent par "
         "adresse de gestion, sans résolution."],
        ["2", "Source de temps", "Transport",
         "La validation DNSSEC et la vérification des certificats exigent une "
         "horloge plausible. Au démarrage à froid, le client de temps doit être "
         "autorisé à corriger un écart important avant toute vérification "
         "cryptographique."],
        ["3", "Autoritatifs ns1 puis ns2", "Temps",
         "Le fichier hosts suffit à les atteindre."],
        ["4", "Résolveurs rec1 et rec2", "Autoritatifs",
         "Leur propre résolution locale pointe sur la boucle locale, jamais sur "
         "leur homologue, afin d'éviter une dépendance croisée."],
        ["5", "IPAM puis agent", "DNS",
         "La réconciliation ne démarre qu'une fois le DNS joignable."],
        ["6", "DHCP", "DNS et IPAM",
         "Les options distribuées référencent les résolveurs."],
        ["7", "Orchestration et supervision", "Ensemble des précédents",
         "Dernière étape ; la supervision constate l'état sans conditionner la "
         "remise en service."],
    ]
    add(make_table(["Rang", "Élément remis en service", "Dépend de",
                    "Remarque"], rows,
                   [CW * 0.07, CW * 0.24, CW * 0.16, CW * 0.53]))
    add(caption("Tableau 5.2  Ordre de reprise après indisponibilité étendue"))
    add(P("Le point sensible est le rang 2. La validation cryptographique du "
          "temps par NTS suppose un certificat valide, dont la vérification "
          "suppose une horloge correcte, qui suppose elle-même le service de "
          "temps. Le document 03 signale ce cas sans le trancher. Du point de vue "
          "du DNS, la conséquence est simple : si l'horloge est fausse, la "
          "validation DNSSEC rejette des réponses publiques pourtant légitimes, "
          "ce qui se manifeste par des codes SERVFAIL sur l'espace public alors "
          "que l'espace interne répond normalement. Ce symptôme doit figurer dans "
          "la procédure de diagnostic, car il oriente immédiatement vers "
          "l'horloge et non vers le DNS."))

    add(P("5.5  Journalisation, métriques et alertes", "h2"))
    add(P("La journalisation est placée sur les résolveurs, seuls points où "
          "l'adresse source est celle du client réel. Elle est horodatée en temps "
          "universel coordonné, conformément à NET-FR-018, et limitée aux "
          "éléments nécessaires : horodatage, adresse source, nom demandé, type, "
          "code de réponse et étiquette de vue. La durée de conservation et la "
          "responsabilité des données relèvent de l'interface avec IAM et les "
          "responsables métier."))
    add(Spacer(1, 3))
    rows = [
        ["Disponibilité de chaque instance",
         "Absence de réponse à une sonde SOA pendant 60 s", "Majeure"],
        ["Écart de numéro de série entre ns1 et ns2",
         "Écart persistant au-delà de deux cycles de transfert, soit 120 s",
         "Majeure : la réplication est rompue et la redondance n'est plus "
         "effective"],
        ["Taux de réponses REFUSED par vue",
         "Hausse significative par rapport à la référence",
         "Mineure : politique trop stricte, mauvaise distribution des "
         "résolveurs, ou tentative d'accès"],
        ["Taux de réponses SERVFAIL",
         "Hausse sur l'espace public",
         "Majeure : dérive d'horloge, perte de la sortie externe ou échec de "
         "validation"],
        ["Âge du dernier transfert réussi sur ns2",
         "Supérieur à 2 x refresh, soit 7200 s", "Majeure"],
        ["Opérations de publication en échec",
         "Toute opération bloquée au-delà de son délai", "Majeure"],
        ["Divergence IPAM et zones publiées",
         "Toute divergence persistant après deux cycles de réconciliation",
         "Mineure, à instruire"],
        ["Tentatives de transfert de zone refusées",
         "Toute occurrence", "À instruire en sécurité"],
        ["Absence de données de collecte",
         "Interruption de la lecture en pull", "Majeure : la panne de collecte "
         "doit alerter, et non effacer silencieusement les traces"],
    ]
    add(make_table(["Indicateur", "Seuil ou condition", "Portée"], rows,
                   [CW * 0.3, CW * 0.3, CW * 0.4]))
    add(caption("Tableau 5.3  Indicateurs et alertes du service DNS"))

    add(P("5.6  Sauvegarde, restauration et gestion des secrets", "h2"))
    add(P("L'objectif historique de reconstruction en moins de soixante minutes "
          "reste à évaluer, et cette évaluation relève de T009. Ce dossier en "
          "fournit les éléments : ce qui doit être sauvegardé, où, et dans quel "
          "ordre la restauration s'effectue."))
    add(CodeBlock("""
# --- export quotidien de l'etat autoritatif, depuis ns1
install -d -m 0750 /var/backups/gandal/dns
for Z in $(pdnsutil list-all-zones) ; do
  pdnsutil list-zone "$Z" > "/var/backups/gandal/dns/${Z}.zone"
done

# --- l'export est verse dans le depot versionne, sans aucun secret
#     Les cles TSIG et les cles d'API restent dans le magasin de secrets.

# --- restauration de ns1 sur une machine neuve
pdnsutil import-tsig-key gandal-xfr hmac-sha256 "$TSIG_GANDAL_XFR"
for F in /var/backups/gandal/dns/*.zone ; do
  Z=$(basename "$F" .zone)
  pdnsutil create-zone "$Z" ns1.gandal.internal
  pdnsutil load-zone   "$Z" "$F"
  pdnsutil set-meta    "$Z" TSIG-ALLOW-AXFR gandal-xfr
  pdnsutil set-meta    "$Z" SOA-EDIT-API    DEFAULT
done
pdnsutil rectify-all-zones
pdnsutil check-all-zones
"""))
    add(Paragraph("Listing 5.3  Export et restauration de l'état autoritatif",
                  S["capcode"]))
    add(Spacer(1, 3))
    rows = [
        ["Clé TSIG de transfert", "Magasin de secrets",
         "Rotation annuelle ou sur incident. La rotation se fait en déclarant la "
         "nouvelle clé sur les deux serveurs avant de retirer l'ancienne."],
        ["Clé d'API de ns1", "Magasin de secrets, injectée dans l'environnement "
         "du service",
         "Rotation lors de tout changement du porteur de l'agent. L'empreinte "
         "peut figurer en configuration à partir de la version 4.7."],
        ["Certificat TLS du mandataire", "PKI interne, interface IF-EXT-01",
         "Renouvellement avant échéance ; la supervision du délai restant fait "
         "partie des indicateurs attendus."],
        ["Exports de zones", "Dépôt versionné et copie hors du cluster",
         "Une copie qui ne serait disponible que dans le cluster administré "
         "n'offre aucune reprise autonome après sa perte."],
    ]
    add(make_table(["Élément", "Emplacement", "Règle"], rows,
                   [CW * 0.22, CW * 0.28, CW * 0.5]))
    add(caption("Tableau 5.4  Gestion des secrets et des sauvegardes du service"))

    # =================================================================
    # CHAPITRE 6
    # =================================================================
    ext(chapter(doc, "6", "Contrôles de recette de la tâche"))

    add(P("6.1  Critères d'acceptation et commandes associées", "h2"))
    add(P("Les contrôles ci-dessous définissent ce que signifie exactement, pour "
          "T005, que le service DNS est en place. Ils portent sur le service "
          "lui-même et non sur le comportement d'ensemble du datacenter. "
          "Conformément à la règle du corpus, leur statut initial est NON EXÉCUTÉ "
          "et aucun résultat n'est présenté comme obtenu."))
    add(Spacer(1, 3))
    rows = [
        ["C01", "Réponse autoritative directe",
         "dig +norecurse @10.30.4.10 ns1.gandal.internal A",
         "NOERROR, indicateur aa présent, réponse 10.30.4.10"],
        ["C02", "Cohérence entre les deux autoritatifs",
         "dig +short @10.30.4.10 tenant-007.gandal.internal SOA puis la même "
         "requête sur 10.30.4.11",
         "Numéros de série identiques après réception du NOTIFY"],
        ["C03", "Résolution inverse d'une machine tenant",
         "dig +short @10.30.4.12 -x 10.30.70.37",
         "vm-0042.tenant-007.gandal.internal."],
        ["C04", "Transfert de zone refusé à un tiers",
         "dig @10.30.4.10 gandal.internal AXFR depuis une source autre que ns2",
         "Transfert refusé ; le transfert signé demandé par ns2 reste possible"],
        ["C05", "Isolation entre tenants",
         "depuis 10.30.70.37 : dig @10.30.4.12 gw.tenant-008.gandal.internal A",
         "REFUSED, sans divulgation de l'existence du nom"],
        ["C06", "Isolation de l'infrastructure",
         "depuis 10.30.70.37 : dig @10.30.4.12 xo.infra.gandal.internal A",
         "REFUSED ; la même requête depuis le pool VPN administrateur aboutit"],
        ["C07", "Récursion autorisée et bornée",
         "depuis 10.30.70.37 : dig @10.30.4.12 example.org A ; puis la même "
         "requête depuis une source hors allow-from",
         "NOERROR dans le premier cas, absence de service dans le second"],
        ["C08", "Autoritatif inatteignable depuis un tenant",
         "depuis 10.30.70.37 : dig +time=2 +tries=1 @10.30.4.10 "
         "gw.tenant-007.gandal.internal A",
         "Absence de réponse, refus journalisé sur la passerelle"],
        ["C09", "Bascule sur perte d'une instance",
         "Arrêt de ns1 puis requête sur ns2 ; arrêt de rec1 puis requête depuis "
         "un client dont le resolv.conf liste .12 et .13",
         "Résolution maintenue dans les deux cas ; publication suspendue pendant "
         "l'arrêt de ns1"],
        ["C10", "Idempotence de la publication",
         "Émission deux fois du même appel du listing 5.1",
         "État final identique, aucun doublon, aucun second transfert si la "
         "lecture préalable est implémentée"],
        ["C11", "Mode dégradé de publication",
         "Arrêt de l'API autoritative pendant une publication",
         "Opération maintenue en état observable, adresse non rendue au pool, "
         "alerte levée"],
        ["C12", "Amorçage sans DNS",
         "Depuis H1, accès à XO et au bastion avec le service DNS arrêté",
         "Accès obtenu par le socle de reprise du listing 5.2"],
        ["C13", "Comportement sous contrainte de MTU",
         "dig +dnssec +bufsize=1232 sur une réponse volumineuse, puis dig +tcp",
         "Troncature suivie d'une reprise en TCP, sans perte silencieuse"],
        ["C14", "Journaux et métriques en lecture pull",
         "Lecture du point de métriques depuis 10.30.5.10, puis tentative "
         "d'initiation depuis une instance DNS vers Monitoring",
         "Lecture réussie, initiation inverse refusée, horodatage en temps "
         "universel"],
        ["C15", "Discrétion du service",
         "dig @10.30.4.10 version.bind CH TXT", "Réponse anonymisée"],
    ]
    add(make_table(["Code", "Objet", "Précondition et action", "Résultat attendu"],
                   rows, [CW * 0.07, CW * 0.2, CW * 0.38, CW * 0.35]))
    add(caption("Tableau 6.1  Contrôles de recette de T005 ; statut initial de "
                "l'ensemble : NON EXÉCUTÉ"))

    add(P("6.2  Transmission à la campagne de validation", "h2"))
    add(P("Plusieurs scénarios du corpus dépassent le périmètre de cette tâche "
          "parce qu'ils engagent d'autres lots ou mesurent des cibles globales. "
          "Ils sont rappelés ici avec la contribution que T005 leur apporte, afin "
          "que la campagne de validation puisse les reprendre sans redéfinir le "
          "contexte."))
    add(Spacer(1, 3))
    rows = [
        ["S04, document 03", "Requêtes DNS vers l'infrastructure et vers un tenant "
         "voisin depuis le VNet USER",
         "C05 et C06 en constituent la vérification unitaire ; S04 y ajoute le "
         "parcours complet depuis une machine réellement provisionnée."],
        ["S08, document 03", "Restauration depuis une sauvegarde indépendante",
         "La procédure et le contenu de la sauvegarde sont fournis à la section "
         "5.6 ; la mesure du délai reste à produire."],
        ["G04, document 01", "Coupure de XO puis d'un service DNS",
         "Le comportement attendu est décrit à la section 5.3 : continuité du "
         "trafic existant, suspension des opérations nouvelles."],
        ["V09, document 02", "Création de cinquante VNets et cinq cents baux",
         "La génération des cent-treize zones est automatisée par le listing 4.3 ; "
         "la tenue en charge du service reste à mesurer."],
        ["NET-NFR-003", "Reconstruction en moins de soixante minutes",
         "Éléments de reprise fournis aux sections 5.4 et 5.6 ; la cible est à "
         "évaluer et non à présumer."],
    ]
    add(make_table(["Scénario", "Objet", "Contribution de T005"], rows,
                   [CW * 0.16, CW * 0.34, CW * 0.5]))
    add(caption("Tableau 6.2  Scénarios transmis à la campagne de validation"))

    # =================================================================
    # CHAPITRE 7
    # =================================================================
    ext(chapter(doc, "7", "Hypothèses, limites et points à valider"))

    add(P("La qualité d'un dossier de conception tient autant à ce qu'il établit "
          "qu'à ce qu'il signale comme non établi. Les éléments ci-dessous "
          "distinguent les hypothèses prises faute de donnée, les points dont la "
          "vérification conditionne l'application, et les limites structurelles "
          "que la conception ne peut pas lever."))
    add(Spacer(1, 4))

    add(P("7.1  Hypothèses formulées", "h3"))
    rows = [
        ["Durée de bail DHCP de 3600&#160;s",
         "Donnée manquante, relevant de T004. Elle fixe la durée de vie des "
         "enregistrements dynamiques et la quarantaine. La règle de "
         "proportionnalité énoncée à la section 2.4 reste valable si la valeur "
         "change.", "Hypothèse"],
        ["Quarantaine de 900&#160;s avant réutilisation d'une adresse",
         "Le document 03 laisse cette durée À VALIDER. La valeur proposée couvre "
         "la durée de vie directe et négative avec une marge.", "Proposition"],
        ["Récursion complète vers la racine publique",
         "Préférée à une redirection vers un résolveur d'opérateur, dont le "
         "comportement n'est pas maîtrisé et dont la disponibilité dépendrait "
         "d'un équipement non manageable.", "Choix"],
        ["VNI 30404 pour le VNet Services",
         "Pris dans la réserve de travail 30404 à 30408 du document 02. "
         "L'identifiant réellement attribué par le contrôleur doit être relevé et "
         "rapproché de cette réserve.", "Proposition"],
        ["Moteur de stockage SQLite",
         "Suffisant pour cent-treize zones et un régime courant de l'ordre de "
         "1 300 enregistrements. Un moteur relationnel partagé reste une "
         "extension.", "Choix"],
    ]
    add(make_table(["Élément", "Justification", "Statut"], rows,
                   [CW * 0.27, CW * 0.58, CW * 0.15]))
    add(caption("Tableau 7.1  Hypothèses et choix à confirmer"))

    add(P("7.2  Points à vérifier avant application", "h3"))
    ext(bullets([
        "<b>Versions exactes des logiciels.</b> Les directives primary et "
        "secondary supposent une version 4.5 ou supérieure du serveur "
        "autoritatif. La branche 5 du résolveur propose un format de "
        "configuration YAML qu'il faut distinguer du format classique employé "
        "ici. La disponibilité de la journalisation dnstap dépend également des "
        "options de compilation du paquet retenu.",
        "<b>Collecteur de journalisation.</b> Le composant qui consomme le flux "
        "dnstap et produit les fichiers lus par Monitoring n'est pas arrêté. Son "
        "choix doit respecter la règle d'absence d'initiation vers Monitoring.",
        "<b>Comportement réel de la sortie externe.</b> La récursion vers la "
        "racine suppose que le routeur R1 laisse passer le port 53 sortant en "
        "UDP et en TCP sans altération. Le document 01 rappelle que les fonctions "
        "réelles de ce routeur restent à vérifier.",
        "<b>Correspondance entre session VPN et tenant.</b> Tant qu'elle n'est "
        "pas fournie par le lot VPN et IAM, le pool VPN utilisateur reste privé "
        "de résolution interne, comme expliqué à la section 3.4.",
        "<b>Coût du script de politique.</b> Le script de la section 4.4 "
        "s'exécute à chaque requête. Son incidence sur la latence doit être "
        "mesurée à la charge attendue avant mise en service, même si son contenu "
        "est volontairement minimal.",
    ]))

    add(P("7.3  Limites structurelles assumées", "h3"))
    ext(bullets([
        "La redondance du service couvre la perte d'une machine virtuelle ou "
        "d'un hôte. Elle ne couvre ni la perte du commutateur SW1, ni celle du "
        "routeur R1, qui restent des dépendances communes imposées par le "
        "cadrage matériel.",
        "La politique de vue repose sur l'adresse source. Elle suppose donc que "
        "l'usurpation d'adresse à l'intérieur d'un VNet est traitée par la "
        "segmentation et les protections du lot VNet et SDN. Le DNS ne constitue "
        "pas, à lui seul, un mécanisme d'authentification du demandeur.",
        "Un tenant peut énumérer ses propres noms. Cette propriété est inhérente "
        "à un service de résolution ouvert à ses clients et ne franchit aucune "
        "frontière de tenant.",
        "Aucun déploiement n'a été réalisé et aucune mesure n'a été produite. "
        "Les volumes, les délais et les capacités énoncés sont des estimations de "
        "conception, à confronter à la maquette avant toute mise en service.",
    ]))

    add(P("Conclusion", "h2"))
    add(P("Ce dossier fournit ce que la tâche T005 demandait : une architecture de "
          "résolution arrêtée, un espace de nommage entièrement dérivé du plan "
          "d'adressage du document 02, un mécanisme démontré d'isolation entre "
          "domaines, des configurations applicables pour les quatre instances, et "
          "un cycle de vie des enregistrements compatible avec la machine d'états "
          "du document 03."))
    add(P("Trois décisions en constituent l'ossature. La séparation stricte des "
          "rôles autoritatif et récursif, qui rend l'isolation applicable plutôt "
          "que seulement souhaitée. L'indexation de la politique de vue sur "
          "l'étiquette calculée avant le cache, qui empêche le cache de "
          "contourner la politique. Enfin le propriétaire d'écriture unique, qui "
          "rend la publication rejouable et la réconciliation possible."))
    add(P("Le service reste conditionné aux hypothèses du chapitre 7 et à la "
          "simulation préalable exigée par NET-FR-020. L'exécution des contrôles "
          "du chapitre 6, la mesure des cibles de reconstruction et "
          "l'archivage des preuves relèvent de la tâche T009, qui interviendra "
          "lorsque les lots DHCP, temps et agent seront disponibles."))

    # =================================================================
    # REFERENCES
    # =================================================================
    add(SetHead(doc, "Références"))
    add(PageBreak())
    add(P("Références", "h1"))
    add(HRule(CW, 1.1, GOLD, space=2))
    add(Spacer(1, 10))

    refs = [
        "Projet GANDAL. <b>Architecture globale GANDAL</b>, document 01, version 1.2, "
        "4 octobre 2026. Besoins, exigences, responsabilités et interfaces du "
        "datacenter.",
        "Projet GANDAL. <b>Conception VNet et SDN GANDAL</b>, document 02, version 1.2, "
        "4 octobre 2026. Plan d'adressage détaillé, réservations VNI, MTU et "
        "matrice de flux. Référence des plages consommées par ce dossier.",
        "Projet GANDAL. <b>Services réseau GANDAL</b>, document 03, version 1.2, "
        "4 octobre 2026. IPAM, DHCP, DNS, temps et provisionnement des machines "
        "virtuelles. Arbitrage logiciel et machine d'états de création.",
        "Projet GANDAL. <b>Topologie cible GANDAL</b>, document 04, version 1.2, "
        "4 octobre 2026. Inventaire des objets à représenter et conventions de "
        "dessin.",
        "Projet GANDAL. <b>Services réseau et infrastructure Underlay</b>, état de "
        "l'art technique, octobre 2026. Adressage, résolution de noms, "
        "dépendances de démarrage et accès d'administration.",
        "Projet GANDAL. <b>Suivi des tâches de l'équipe 20</b>, 2026. Attribution "
        "des tâches T001 à T009.",
        "IETF. <b>RFC 1034, Domain names, concepts and facilities</b>, 1987. "
        "Définition de la délégation, de l'autorité et de la mise en cache.",
        "IETF. <b>RFC 1035, Domain names, implementation and specification</b>, 1987. "
        "Format des messages, transferts de zone et champs du SOA.",
        "IETF. <b>RFC 2317, Classless IN-ADDR.ARPA delegation</b>, 1998. "
        "Découpage inverse sans classe, examiné puis écarté à la section 2.2.",
        "IETF. <b>RFC 6303, Locally served DNS zones</b>, 2011. Fondement du "
        "comportement par défaut neutralisé par la directive serve-rfc1918.",
        "IETF. <b>RFC 6891, Extension mechanisms for DNS, EDNS(0)</b>, 2013. "
        "Annonce de la taille de réponse UDP, paramétrée à 1232 octets.",
        "IETF. <b>RFC 7766, DNS transport over TCP</b>, 2016. Justification de "
        "l'ouverture obligatoire du port 53 en TCP.",
        "IETF. <b>RFC 8945, Secret key transaction authentication for DNS, TSIG</b>, "
        "2020. Signature des transferts de zone entre ns1 et ns2.",
        "IETF. <b>RFC 2136, Dynamic updates in the domain name system</b>, 1997. "
        "Mécanisme de l'alternative évaluée au tableau 5.1.",
        "IETF. <b>RFC 4035, Protocol modifications for the DNS security "
        "extensions</b>, 2005. Validation DNSSEC et traitement des branches non "
        "signées.",
        "ICANN. <b>Board resolution on the reservation of the .internal top level "
        "domain for private use</b>, 2024. Fondement du choix de suffixe interne.",
        "PowerDNS. <b>Authoritative server documentation</b> : settings, HTTP API et "
        "pdnsutil. Documentation évolutive ; la version installée doit être "
        "confirmée avant application.",
        "PowerDNS. <b>Recursor documentation</b> : settings, scripting Lua, gettag "
        "et preresolve. Documentation évolutive ; la version installée doit être "
        "confirmée avant application.",
        "DNS Flag Day 2020. <b>Recommandation sur la taille des messages DNS en UDP</b>. "
        "Origine de la valeur de 1232 octets.",
        "XCP-ng Project. <b>Networking et XCP-ng 8.3 LTS</b>. Version cible du corpus, "
        "à confirmer sur les hôtes.",
    ]
    for i, r in enumerate(refs, 1):
        add(Paragraph("[%d]  %s" % (i, r),
                      ParagraphStyleRef()))
    return s


def ParagraphStyleRef():
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_JUSTIFY
    return ParagraphStyle("ref", fontName="Serif", fontSize=8.4, leading=12.2,
                          alignment=TA_JUSTIFY, leftIndent=17, firstLineIndent=-17,
                          spaceAfter=5.5, textColor=colors.HexColor("#1A1A1A"))
