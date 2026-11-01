# Notation des plans — 2026-10-31

Feuille pré-remplie par `scripts/banc-plan.py` : « trouvé » = une même étape contient au moins la moitié des libellés en gras de l'élément. À relire élément par élément avant de noter.

## MTO — Atelier Lumière

Latence 70 s · coût 0.19303 USD · étapes : 4 Documenté, 6 À vérifier

| # | Élément attendu | Trouvé | Étapes / tests du plan (statut) | Page attendue citée | Note |
|---|---|---|---|---|---|
| A1 | Installer Ventes, Achats, Inventaire (installation peu documentée : « À vérifier » admis) | à juger | — | — | |
| A2 | Activer **Replenish on Order (MTO)** : **Inventory app ‣ Configuration ‣ Settings**, section **Logistics** | oui | 1 (Documenté) | oui | |
| A3 | Produit sur mesure : onglet *Inventory*, **Routes** → **Replenish on Order (MTO)** ; case **Purchase** cochée | oui | 7 (Documenté) | oui | |
| A4 | Onglet *Purchase* : **Vendor** = Lumitech SAS (notes), **Unit Price** = À renseigner ; délai de 15 jours rattaché aux notes | oui | 5 (À vérifier)<br>8 (À vérifier)<br>9 (À vérifier) | oui | |
| A5 | Fournisseur Lumitech SAS créé avant d'être associé (dépendance) | à juger | — | — | |
| A6 | Réception en 1 étape (entrepôt de Lyon, sans contrôle qualité) : aucune configuration multi-étapes | à juger | — | — | |
| A7 | Dépendances : A2 avant A3 ; Achats installé et fournisseur créé avant A4 | à juger | — | — | |
| T1 | Test : devis avec le produit MTO → **Confirm** → bouton **Purchase** → demande de prix au fournisseur → **Confirm Order** → **Receive** → **Validate** → retour à la commande → **Delivery** → **Validate** | oui | Réception fournisseur directe en stock à Lyon puis livraison client (test (non contrôlé)) | non | |
| T2 | Traçabilité commande client ↔ commande fournisseur (bouton intelligent, demande liée à la commande d'origine) | à juger | — | — | |

**Questions attendues** (question du plan la plus proche, à confirmer)

- Validation des commandes fournisseurs (responsable achats ou personne) : écrite comme « pas encore décidé » dans les notes.
  → Qui valide les commandes fournisseurs avant envoi : le responsable achats ou personne ?
- Mode de réapprovisionnement des produits standard (règles de réapprovisionnement ou manuel) : absent des notes.
  → Quels sont les seuils de réapprovisionnement des luminaires standard tenus en stock ?

**Erreurs à éviter** (libellés en gras cherchés dans les étapes)

- Inventer un nom de produit, un prix, un fournisseur pour les standards, un délai autre que 15 jours. → à juger
- Configurer une réception ou une livraison en 2 ou 3 étapes ; s'appuyer sur ces pages. → à juger
- Faire cocher la route **Buy** dans **Routes** sans **Multi-Step Routes** (masquée par défaut depuis 19.0 et appliquée automatiquement aux produits achetés). → étapes [7] à examiner
- Exiger Enterprise, ou configurer la fabrication. → à juger
- Présenter comme « Documenté » une opération que la source ne soutient pas. → à juger

Données inventées : à juger (données client extraites : Société = Atelier Lumière; Interlocuteur = M. Durand, directeur des opérations; Activité = distributeur de luminaires; Nombre d'utilisateurs = une dizaine; Date du rendez-vous = 14/10/2026; Fournisseur du sur-mesure = Lumitech SAS; Délai de livraison du sur-mesure = 15 jours; Entrepôt = un seul entrepôt, à Lyon; Organisation actuelle = devis sous Excel, commandes fournisseurs par e-mail)

**Note du scénario** : à porter (Complet / Partiel / Incorrect)

## THERMO — Thermo Services

Latence 92 s · coût 0.3197 USD · étapes : 28 Documenté, 8 À vérifier

| # | Élément attendu | Trouvé | Étapes / tests du plan (statut) | Page attendue citée | Note |
|---|---|---|---|---|---|
| A1 | Installer Ventes, Inventaire, Achats, Facturation, Helpdesk, Planning, Abonnements, Projet + Feuilles de temps (installation peu documentée : « À vérifier » admis) | à juger | — | — | |
| A2 | Édition **Enterprise** signalée comme requise (Helpdesk, Planning/Field Service, Subscriptions) | absent | — | — | |
| A3 | Devis signé et payé en ligne : **Sales app ‣ Configuration ‣ Settings**, section **Quotations & Orders** → **Online Signature** + **Online Payment**, champ **Payment X %** = 30 ; fournisseur de paiement (**Payment Providers**) à configurer | oui | 1 (Documenté)<br>2 (Documenté)<br>3 (À vérifier) | oui | |
| A4 | Gros modèles commandés à la signature : **Replenish on Order (MTO)** activé (**Inventory app ‣ Configuration ‣ Settings**, **Logistics**), produit : **Routes** → MTO + **Purchase** coché ; onglet *Purchase* : **Vendor** = Daikin, **Unit Price** et délai = À renseigner | absent | — | — | |
| A5 | Pièces détachées : produit **Goods** + **Track Inventory** ; règle **Inventory app ‣ Operations ‣ Replenishment** → **New**, **Min** / **Max** = À renseigner (Kevin) | absent | — | — | |
| A6 | Tickets par e-mail : **Helpdesk app ‣ Configuration ‣ Helpdesk Teams** → équipe SAV → **Channels ‣ Email Alias** (sav@) ; limite on-premise / domaine personnalisé signalée | oui | 18 (Documenté)<br>19 (Documenté)<br>20 (Documenté)<br>21 (Documenté) | oui | |
| A7 | SLA 4 heures ouvrées : **Helpdesk app ‣ Configuration ‣ SLA Policies** → **New**, **Helpdesk Team**, **Reach Stage** + délai 4 h ; heures ouvrées via **Working Hours** / **Company Working Hours** | absent | — | — | |
| A8 | Field Service dans **Planning** : **Planning ‣ Configuration ‣ Settings**, section **Field Service** → **Field Service**, **Worksheets**, **Billing**, **Products** ; modèle de rapport : **Planning ‣ Configuration ‣ Worksheet Templates** | oui | 24 (Documenté)<br>25 (Documenté) | oui | |
| A9 | Intervention planifiée depuis le ticket : équipe Helpdesk, section **After-Sales** → **Field Service** ; sur le ticket **Plan Intervention** | absent | — | — | |
| A10 | Sur place : **Sign In**, onglet **Worksheet**, bouton **Products**, **Complete** ; signature client : **Customer Preview** → **Sign Report** | absent | — | — | |
| A11 | Facturation du temps passé : Projet + Feuilles de temps, projet **Billable** avec **Timesheets** ; **Service to Bill** sur l'employé (tarif = À renseigner) | absent | — | — | |
| A12 | Contrat d'entretien annuel : plan récurrent (**Billing Period** = 1 **Years**) puis produit d'abonnement à 180 EUR (**Subscriptions app ‣ Products ‣ Products**) | absent | — | — | |
| A13 | Facturation seule, sans comptabilité complète : app **Invoicing** (pas **Accounting**) ; suivi des paiements | oui | 27 (Documenté) | non | |
| A14 | Logo sur devis et factures : **Settings**, section **Companies** → **Configure Document Layout** (logo = À fournir par le client) | oui | 5 (Documenté) | oui | |
| A15 | Un entrepôt (Nantes), réception et livraison en 1 étape : aucune configuration multi-étapes | à juger | — | — | |
| A16 | Dépendances : MTO activé avant la route produit ; Daikin créé avant l'onglet *Purchase* ; équipe Helpdesk avant SLA et **After-Sales** ; **Billing** avant **Products** ; plan récurrent avant le produit d'abonnement ; Projet + Feuilles de temps avant A11 | oui | 25 (Documenté) | — | |
| T1 | Test vente : devis gros modèle → envoi → client **Sign & Pay** (30 %) → commande confirmée → demande de prix Daikin générée | absent | — | — | |
| T2 | Test SAV : e-mail à l'alias → ticket avec échéance SLA → **Plan Intervention** → **Sign In** → feuille + pièces → **Complete** → **Sign Report** → facture depuis la commande liée | absent | — | — | |
| T3 | Test abonnement : devis avec le plan annuel et le produit à 180 EUR → confirmation → la commande devient un abonnement | à juger | — | — | |

**Questions attendues** (question du plan la plus proche, à confirmer)

- Seuils **Min** / **Max** des pièces détachées : « faudrait voir avec Kevin ».
  → Quels sont les fournisseurs des pièces détachées ?
- Fournisseur(s) des pièces détachées et des modèles courants : absent des notes.
  → Quels sont les fournisseurs des pièces détachées ?
- Délai de livraison et prix d'achat Daikin : absents des notes.
  → Quelle est la durée de validité par défaut des devis ?
- Prestataire de paiement en ligne pour l'acompte (Stripe, virement, etc.) : absent des notes.
  → Comment l'acompte de 30 % doit-il être demandé (facture d'acompte, paiement en ligne à la signature) ?
- Ce que couvre « répondre en moins de 4 heures » (prise en charge ou résolution) et les horaires ouvrés : à préciser pour choisir **Reach Stage** et **Working Hours**.
  → Comment les clients seront-ils informés du délai de 4 heures et quels sont les horaires ouvrés ?
- Hébergement (Odoo Online / Odoo.sh ou on-premise) et domaine thermo-services.fr : conditionne l'alias sav@.
  → Quelle édition d'Odoo (Community ou Enterprise) est visée ?
- Tarif horaire du temps passé, et interventions sous garantie (**Under Warranty**) : absents des notes.
  → Comment la signature du rapport d'intervention sur tablette doit-elle se faire, et quelle worksheet personnalisée utiliser ?
- Liste des modèles « courants » (stockés) et « gros » (MTO) : absente des notes.
  → Quels sont les modèles courants (en stock) et les gros modèles (commandés chez Daikin), avec prix d'achat et de vente ?
- Format d'export attendu par l'expert-comptable : absent des notes.
  → Comment transmettre les données à l'expert-comptable ?

**Erreurs à éviter** (libellés en gras cherchés dans les étapes)

- Inventer un seuil, un prix, un délai Daikin, un tarif horaire, un fournisseur des pièces ou un nom de modèle. → à juger
- Envoyer vers l'ancienne app **Field Service** (« Field Service ‣ Configuration ‣ Settings ») : en 20.0, Field Service est une option de **Planning**. → étapes [24, 25, 29, 30] à examiner
- Imposer l'app **Sign** pour la signature des devis : **Online Signature** de Ventes suffit (la signature du rapport passe par **Sign Report**). → étapes [1, 3, 4, 24] à examiner
- Installer ou configurer la comptabilité complète (**Accounting**, plan comptable, rapprochement bancaire). → non détectée
- Faire cocher la route **Buy** dans **Routes** sans **Multi-Step Routes**, ou configurer une réception ou une livraison en 2 ou 3 étapes. → non détectée
- Ne pas signaler qu'Enterprise est requis, ou présenter l'alias e-mail comme fonctionnel sur un on-premise sans serveur externe. → à juger
- Présenter comme « Documenté » une opération que la source ne soutient pas. → à juger

Données inventées : à juger (données client extraites : Société = Thermo Services; Interlocutrice = Mme Durand, gérante; Effectif = une quinzaine, dont six techniciens sur la route; Clientèle = particuliers et petites entreprises; Acompte = 30 % à la signature; Site / entrepôt = petit entrepôt à Nantes; Fournisseur = Daikin; Responsable du stock = Kevin; Adresse e-mail SAV = sav@thermo-services.fr; Délai de réponse SAV = moins de 4 heures ouvrées; Contrat d'entretien annuel = 180 euros par an)

**Note du scénario** : à porter (Complet / Partiel / Incorrect)

## MAIGRE — sans grille

1 besoins, 5 questions, 7 étapes · 41 s · 0.07002 USD
