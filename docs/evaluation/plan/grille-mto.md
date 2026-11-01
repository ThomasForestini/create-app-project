# Phase 1 — Grille du scénario MTO (figée avant la génération réelle)

Rédigée le 18/10/2026, avant l'unique génération réelle autorisée, à partir de la documentation Odoo 20.0 indexée (page `inventory_and_mrp/inventory/warehouses_storage/replenishment/mto`, passages 0 à 11). Notes : [scenario-mto.txt](scenario-mto.txt). Projet : Odoo 20.0, édition Community.

## Attendu (opérations concrètes, sourcées 20.0)

| # | Élément | Source attendue |
|---|---|---|
| A1 | Installer Ventes, Achats, Inventaire (installation peu documentée : « À vérifier » admis) | — |
| A2 | Activer **Replenish on Order (MTO)** : **Inventory app ‣ Configuration ‣ Settings**, section **Logistics** | mto § Enable the MTO route |
| A3 | Produit sur mesure : onglet *Inventory*, **Routes** → **Replenish on Order (MTO)** ; case **Purchase** cochée | mto § Configure a product for MTO |
| A4 | Onglet *Purchase* : **Vendor** = Lumitech SAS (notes), **Unit Price** = À renseigner ; délai de 15 jours rattaché aux notes | mto § For purchased products |
| A5 | Fournisseur Lumitech SAS créé avant d'être associé (dépendance) | — |
| A6 | Réception en 1 étape (entrepôt de Lyon, sans contrôle qualité) : aucune configuration multi-étapes | receipts_delivery_one_step ou rien |
| A7 | Dépendances : A2 avant A3 ; Achats installé et fournisseur créé avant A4 | — |
| T1 | Test : devis avec le produit MTO → **Confirm** → bouton **Purchase** → demande de prix au fournisseur → **Confirm Order** → **Receive** → **Validate** → retour à la commande → **Delivery** → **Validate** | mto § Replenishment workflow |
| T2 | Traçabilité commande client ↔ commande fournisseur (bouton intelligent, demande liée à la commande d'origine) | mto § intro, Validate replenishment order |

## Questions attendues (non bloquantes)
- Validation des commandes fournisseurs (responsable achats ou personne) : écrite comme « pas encore décidé » dans les notes.
- Mode de réapprovisionnement des produits standard (règles de réapprovisionnement ou manuel) : absent des notes.

## Erreurs à éviter
- Inventer un nom de produit, un prix, un fournisseur pour les standards, un délai autre que 15 jours.
- Configurer une réception ou une livraison en 2 ou 3 étapes ; s'appuyer sur ces pages.
- Faire cocher la route **Buy** dans **Routes** sans **Multi-Step Routes** (masquée par défaut depuis 19.0 et appliquée automatiquement aux produits achetés).
- Exiger Enterprise, ou configurer la fabrication.
- Présenter comme « Documenté » une opération que la source ne soutient pas.

## Notation
- **Complet** : A2 à A4, A6, A7, T1 présents, sourcés 20.0, sans erreur ci-dessus ; questions pertinentes.
- **Partiel** : un élément manquant ou non sourcé sans être signalé.
- **Incorrect** : une erreur ci-dessus présentée comme documentée, ou une donnée métier inventée.
