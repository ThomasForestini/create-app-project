# Phase 3 — Grille du scénario Thermo Services (figée avant la génération réelle)

**Statut : validée** (Thomas, 31/10/2026)

Rédigée le 31/10/2026, avant toute génération par `odoo-plan`, à partir de la documentation Odoo 20.0 indexée dans pgvector. Notes : [thermo.pdf](thermo.pdf) (transcription fictive). Projet : Odoo 20.0, édition **Enterprise** (Helpdesk, Planning et Subscriptions sont des apps Enterprise).

## Attendu (opérations concrètes, sourcées 20.0)

| # | Élément | Source attendue |
|---|---|---|
| A1 | Installer Ventes, Inventaire, Achats, Facturation, Helpdesk, Planning, Abonnements, Projet + Feuilles de temps (installation peu documentée : « À vérifier » admis) | — |
| A2 | Édition **Enterprise** signalée comme requise (Helpdesk, Planning/Field Service, Subscriptions) | — |
| A3 | Devis signé et payé en ligne : **Sales app ‣ Configuration ‣ Settings**, section **Quotations & Orders** → **Online Signature** + **Online Payment**, champ **Payment X %** = 30 ; fournisseur de paiement (**Payment Providers**) à configurer | create_quotations § Configuration ; get_signature_to_validate ; get_paid_to_validate |
| A4 | Gros modèles commandés à la signature : **Replenish on Order (MTO)** activé (**Inventory app ‣ Configuration ‣ Settings**, **Logistics**), produit : **Routes** → MTO + **Purchase** coché ; onglet *Purchase* : **Vendor** = Daikin, **Unit Price** et délai = À renseigner | mto § Enable the MTO route, § Configure a product for MTO |
| A5 | Pièces détachées : produit **Goods** + **Track Inventory** ; règle **Inventory app ‣ Operations ‣ Replenishment** → **New**, **Min** / **Max** = À renseigner (Kevin) | reordering_rules § Product type configuration, § Create a reordering rule |
| A6 | Tickets par e-mail : **Helpdesk app ‣ Configuration ‣ Helpdesk Teams** → équipe SAV → **Channels ‣ Email Alias** (sav@) ; limite on-premise / domaine personnalisé signalée | receiving_tickets § Email alias |
| A7 | SLA 4 heures ouvrées : **Helpdesk app ‣ Configuration ‣ SLA Policies** → **New**, **Helpdesk Team**, **Reach Stage** + délai 4 h ; heures ouvrées via **Working Hours** / **Company Working Hours** | sla § Create a new SLA policy, § Establish a target, § Meet SLA deadlines |
| A8 | Field Service dans **Planning** : **Planning ‣ Configuration ‣ Settings**, section **Field Service** → **Field Service**, **Worksheets**, **Billing**, **Products** ; modèle de rapport : **Planning ‣ Configuration ‣ Worksheet Templates** | field_service § intro, § Configuration, § Invoicing, § Products |
| A9 | Intervention planifiée depuis le ticket : équipe Helpdesk, section **After-Sales** → **Field Service** ; sur le ticket **Plan Intervention** | after_sales § Plan field service interventions from a ticket |
| A10 | Sur place : **Sign In**, onglet **Worksheet**, bouton **Products**, **Complete** ; signature client : **Customer Preview** → **Sign Report** | field_service § Intervention logging, § Customer report |
| A11 | Facturation du temps passé : Projet + Feuilles de temps, projet **Billable** avec **Timesheets** ; **Service to Bill** sur l'employé (tarif = À renseigner) | field_service § Time-based invoicing |
| A12 | Contrat d'entretien annuel : plan récurrent (**Billing Period** = 1 **Years**) puis produit d'abonnement à 180 EUR (**Subscriptions app ‣ Products ‣ Products**) | subscriptions § Set up recurring plans, § Product form configuration |
| A13 | Facturation seule, sans comptabilité complète : app **Invoicing** (pas **Accounting**) ; suivi des paiements | accounting § intro |
| A14 | Logo sur devis et factures : **Settings**, section **Companies** → **Configure Document Layout** (logo = À fournir par le client) | pdf_reports § Default layout ; companies § Company |
| A15 | Un entrepôt (Nantes), réception et livraison en 1 étape : aucune configuration multi-étapes | receipts_delivery_one_step ou rien |
| A16 | Dépendances : MTO activé avant la route produit ; Daikin créé avant l'onglet *Purchase* ; équipe Helpdesk avant SLA et **After-Sales** ; **Billing** avant **Products** ; plan récurrent avant le produit d'abonnement ; Projet + Feuilles de temps avant A11 | — |
| T1 | Test vente : devis gros modèle → envoi → client **Sign & Pay** (30 %) → commande confirmée → demande de prix Daikin générée | get_signature_to_validate § Order confirmations ; mto § Replenishment workflow |
| T2 | Test SAV : e-mail à l'alias → ticket avec échéance SLA → **Plan Intervention** → **Sign In** → feuille + pièces → **Complete** → **Sign Report** → facture depuis la commande liée | receiving_tickets ; sla ; after_sales ; field_service |
| T3 | Test abonnement : devis avec le plan annuel et le produit à 180 EUR → confirmation → la commande devient un abonnement | subscriptions § Create a subscriptions quotation |

## Questions attendues (non bloquantes)
- Seuils **Min** / **Max** des pièces détachées : « faudrait voir avec Kevin ».
- Fournisseur(s) des pièces détachées et des modèles courants : absent des notes.
- Délai de livraison et prix d'achat Daikin : absents des notes.
- Prestataire de paiement en ligne pour l'acompte (Stripe, virement, etc.) : absent des notes.
- Ce que couvre « répondre en moins de 4 heures » (prise en charge ou résolution) et les horaires ouvrés : à préciser pour choisir **Reach Stage** et **Working Hours**.
- Hébergement (Odoo Online / Odoo.sh ou on-premise) et domaine thermo-services.fr : conditionne l'alias sav@.
- Tarif horaire du temps passé, et interventions sous garantie (**Under Warranty**) : absents des notes.
- Liste des modèles « courants » (stockés) et « gros » (MTO) : absente des notes.
- Format d'export attendu par l'expert-comptable : absent des notes.

## Erreurs à éviter
- Inventer un seuil, un prix, un délai Daikin, un tarif horaire, un fournisseur des pièces ou un nom de modèle.
- Envoyer vers l'ancienne app **Field Service** (« Field Service ‣ Configuration ‣ Settings ») : en 20.0, Field Service est une option de **Planning**.
- Imposer l'app **Sign** pour la signature des devis : **Online Signature** de Ventes suffit (la signature du rapport passe par **Sign Report**).
- Installer ou configurer la comptabilité complète (**Accounting**, plan comptable, rapprochement bancaire).
- Faire cocher la route **Buy** dans **Routes** sans **Multi-Step Routes**, ou configurer une réception ou une livraison en 2 ou 3 étapes.
- Ne pas signaler qu'Enterprise est requis, ou présenter l'alias e-mail comme fonctionnel sur un on-premise sans serveur externe.
- Présenter comme « Documenté » une opération que la source ne soutient pas.

## Notation
- **Complet** : A2 à A14, A16, T1 et T2 présents, sourcés 20.0, sans erreur ci-dessus ; questions pertinentes (au moins seuils, fournisseur des pièces, prestataire de paiement, portée du SLA).
- **Partiel** : un élément manquant ou non sourcé sans être signalé.
- **Incorrect** : une erreur ci-dessus présentée comme documentée, ou une donnée métier inventée.
