# Plan — Phase 3 : PDF client

> PRD parent : `PRD.md`
> Date : 2026-10-31

## Architecture retenue

- `[DEV] odoo-plan` (nouveau) reçoit un PDF en base64 ou un texte.
  - Deux déclencheurs : Execute Workflow Trigger (appel par Telegram) et webhook protégé Header Auth (utilisé par le banc).
  - **Extraction** (Sonnet 5.5, PDF lu nativement) : `{besoins[], donnees_client, questions_ouvertes}`. Seules les données présentes dans le document sont reprises (fournisseur, délais, sites).
  - **Boucle sur les besoins** : chaque besoin part dans `odoo-question` en mode `config`, qui renvoie des étapes avec chemin de menu, champ, valeur en EN, statut et source. La recherche et le contrôle en ligne de la Phase 1 sont réutilisés.
  - **Assemblage** (Sonnet 5.5) : il ordonne les dépendances, supprime les doublons (une installation citée par deux besoins), écrit le test de bout en bout, et produit un JSON plus un Markdown.
- `telegram-assistant` reçoit un document PDF, ou un texte qui commence par `plan:`. Il renvoie un résumé court (besoins compris, étapes par statut, questions ouvertes) et le plan complet en fichier `.md`. Le découpage des messages longs reste en Phase 4.
- Scénarios du banc : ceux de `~/Desktop/a-reprendre-odoo/jeux-de-test/scenarios-clients/`. MTO a sa grille figée du 18/10/2026. La grille de Thermo Services est à écrire puis à valider par Thomas.

## Tâches

- [x] **1. Scénarios du banc + grille Thermo.** Fait quand :
  - `docs/evaluation/plan/` contient `mto.pdf` et `thermo.pdf` (texte des scénarios rendu en PDF), `maigre.pdf` (copie de `besoins.pdf`) et `grille-mto.md` (copie de la grille figée).
  - `grille-thermo.md` est pré-remplie au format de la grille MTO : attendus sourcés v20, édition requise, questions attendues, erreurs à éviter.
  - Thomas a relu et marqué la grille Thermo `validée`.
- [x] **2. Mode `config` dans `odoo-question`.** Fait quand :
  - Un `curl` avec le besoin « luminaires sur mesure commandés au fournisseur à la commande client » renvoie des `etapes[]` (`action`, `menu`, `champ`, `valeur`, `statut`, `source`).
  - On y trouve **Replenish on Order (MTO)**, avec une source `mto.html`.
  - D001 (texte) et Q01 (qcm) gardent le même format (non-régression).
  - L'export `workflows/odoo-question.workflow.json` est à jour.
- [x] **3. `[DEV] odoo-plan` : extraction des besoins** (après 1). Fait quand :
  - `curl` avec `mto.pdf` renvoie les besoins de la grille, Lumitech SAS, 15 jours et Lyon, sans prix ni fournisseur inventés.
  - La question sur la validation des commandes fournisseurs figure dans `questions_ouvertes`.
  - `maigre.pdf` renvoie surtout des questions.
  - Sans jeton, la réponse est 403.
- [x] **4. Boucle sur les besoins + assemblage** (après 2, 3). Fait quand :
  - `curl` avec `mto.pdf` renvoie un plan ordonné (A2 avant A3, fournisseur créé avant l'onglet Purchase), le test T1, ses questions et un Markdown.
  - La route **Buy** n'apparaît pas et aucune étape multi-step n'est proposée.
  - Le plan arrive en moins de 3 min pour 0,20 USD au plus.
  - `workflows/odoo-plan.workflow.json` est exporté.
- [x] **5. PDF et `plan:` dans `telegram-assistant`** (après 4). Fait quand :
  - `mto.pdf` envoyé depuis le téléphone reçoit un résumé et le fichier `.md` en moins de 3 min.
  - Un document qui n'est pas un PDF reçoit un message clair.
  - La photo de QCM et la question texte marchent toujours.
  - Les exports sont à jour.
- [x] **6. Script `scripts/banc-plan.py`** (après 1, 4). Fait quand :
  - Une passe sur `mto.pdf` écrit `docs/evaluation/{date}-plan.json` : plan, latence, coût par appel.
  - Elle écrit aussi une feuille de notation pré-remplie : chaque élément de la grille est trouvé ou absent, avec le statut et la source du plan.
  - URL et jeton sont lus depuis `.env`, et le jeton apparaît 0 fois dans le code (`grep`).
- [x] **7. Passe complète + rapport** (après 6). Fait quand :
  - `docs/evaluation/{date}-plan.md` note MTO et Thermo (Complet / Partiel / Incorrect, élément par élément).
  - Le rapport compte les instructions fausses marquées « Documenté » et les données inventées.
  - Il compare latence et coût aux critères du PRD et à la V3 de l'ancien projet (0,054 USD, partiel).
  - Il donne des pistes si un scénario n'est pas « Complet ».

## Tâches ajoutées après `/validate` ⚠️ Partiel (31/10/2026)

Décisions de Thomas : plus de « Partiel » ; repli internet quand la bibliothèque (doc + 15 vidéos Odoo Tutorials indexées) ne suffit pas, statut 🌐 *Web* jamais « Documenté » ; plafond de 0,20 USD par plan gardé ; repli activé dans tout `odoo-question` (texte, QCM, plan). Les 1 047 vidéos eLearning restent pour une phase dédiée.

- [x] **8. Données client rattachées à leur objet.** Fait quand :
  - l'extraction rattache chaque donnée à sa famille de produits ou à son flux, et aucun lot ne mélange deux familles aux données différentes ;
  - le contrôle en mode `config` refuse « Documenté » à une étape qui applique une donnée client à un autre objet que celui du document ;
  - 3 plans MTO de suite ne placent Lumitech SAS que sur le sur-mesure.
- [x] **9. Prérequis ajoutés par le code** (après 8). Fait quand :
  - `Finalize plan` ajoute, en « À vérifier », une étape d'installation par app citée dans les menus et une étape « Créer le fournisseur X » avant le premier champ **Vendor** qui porte un nom du document ;
  - sur MTO, A1, A5 et A7 sont présents, dans le bon ordre.
- [x] **10. Vidéos puis repli internet dans `odoo-question`.** Fait quand :
  - la recherche pgvector inclut les 290 passages des 15 vidéos Odoo Tutorials (aujourd'hui exclus par `kind = 'odoo_documentation'`) ; une affirmation appuyée seulement par un transcript porte le statut 🎬 *Vidéo* (lien YouTube), jamais « Documenté » ;
  - si la réponse est incomplète (couverture `partial` / `insufficient`, points non couverts, ou éléments sans source), un appel avec l'outil `web_search` (`max_uses` plafonné) cherche ces seuls points ; chaque ajout porte le statut 🌐 *Web*, son URL et l'extrait cité, et n'est gardé que si l'URL figure dans les résultats de la recherche et que l'extrait la soutient ;
  - une question entièrement couverte (D001) ne déclenche aucune recherche web ;
  - une question hors bibliothèque reçoit des éléments 🌐 *Web* sourcés ; Telegram affiche le badge 🌐 ;
  - en mode `config`, les étapes 🌐 ont `action`, `menu`, `champ`, `valeur`, `statut` = `Web` et `source` ;
  - le banc QCM (`banc-qcm.py`) ne perd pas de bonne réponse et ne compte aucun « Documenté » faux de plus ; coût moyen ≤ 0,05 USD par question ;
  - exports à jour.
- [x] **11. Coût du plan ≤ 0,40 USD** (après 8 à 10 ; plafond relevé de 0,20 à 0,40 USD par Thomas le 01/11/2026). Fait quand :
  - l'assemblage reçoit seulement action, menu, champ, valeur et statut de chaque étape ;
  - MTO et Thermo coûtent chacun 0,40 USD au plus, repli web compris, en moins de 3 min.
- [ ] **12. Banc final : MTO et Thermo « Complet »** (après 8 à 11). Résultat au 01/11/2026 : MTO Complet 3/3, Thermo Partiel 2/2 ; « Complet à chaque tirage » pour Thermo reporté en Phase 4 par décision de Thomas (voir `docs/evaluation/2026-11-01-plan-v2.md`). Fait quand :
  - `docs/evaluation/{date}-plan-v2.md` note MTO et Thermo **Complet** élément par élément (un élément couvert par une étape 🌐 *Web* sourcée compte comme couvert, en le signalant) ;
  - 0 « Documenté » faux, 0 donnée inventée, sur 3 plans MTO et 2 plans Thermo ;
  - les écarts restants, s'il y en a, ont une cause et une piste.

## Critère de phase complète

- [ ] Tâches 1 à 12 cochées
- [x] Depuis Telegram, un PDF client reçoit un plan Odoo 20 étape par étape (menus, champs et valeurs en EN, statut et source par étape) et les questions ouvertes
- [ ] MTO et Thermo sont **Complet** (décision du 31/10/2026 : plus de « Partiel »), avec 0 instruction fausse en « Documenté » et 0 donnée inventée.
- [ ] Moins de 3 min et 0,40 USD au plus par plan (PRD, relevé le 01/11/2026)

## Points à surveiller

- **Coût de Thermo** : une dizaine de besoins à 0,024 USD environ, plus l'extraction et l'assemblage, risquent de dépasser 0,20 USD. S'il le faut, on regroupera les besoins proches avant la boucle.
- **Édition** : MTO est noté en Community, mais Thermo demande Enterprise (Field Service, Subscriptions, Sign). L'extraction doit le signaler, et la grille Thermo l'attend.

## Prochaine étape

`/execute docs/plans/phase-3-plan.md`

## Découvertes (hors plan)

- 31/10/2026 : en 20.0, Field Service est une option de l'app **Planning** (pas d'app Field Service dédiée dans la doc indexée), et la signature de devis passe par **Online Signature** de Ventes : l'app Sign n'est pas requise pour Thermo (grille Thermo à jour).
- 31/10/2026 : mode `config`, un besoin coûte 0,036 USD et 34 s (MTO). Pour Thermo, environ 10 besoins font environ 0,36 USD, au-dessus des 0,20 USD : le regroupement des besoins proches (Points à surveiller) sera sans doute nécessaire en tâche 4.
- 31/10/2026 : sur MTO, le modèle met le réglage dans `champ` et l'action (« Cocher la case ») dans `valeur` pour une case à cocher, et ne crée pas le fournisseur avant l'onglet *Purchase* : à corriger à l'assemblage (tâche 4), qui ordonne les dépendances.
- 31/10/2026 : l'extraction MTO (15 s, 0,032 USD) sort 8 besoins, dont un qui est une décision non prise (validation des commandes fournisseurs). À 0,036 USD le besoin, la boucle seule coûte environ 0,29 USD : le regroupement est nécessaire dès MTO, et les besoins qui ne sont que des décisions ouvertes ne doivent pas partir dans `odoo-question`.
- 31/10/2026 : l'Execute Workflow Trigger de `odoo-question` ne déclare que `question`, `model`, `choix`. Sans objet pour l'instant : `odoo-plan` appelle les lots par le webhook (HTTP Request, en parallèle), car Execute Workflow les enchaînerait (3 lots à environ 30 s chacun). À compléter si un autre workflow appelle un jour le mode `config`.
- 31/10/2026 : extraction avec `lots` (5 au plus) : MTO donne 3 lots, 68 à 73 s et 0,184 à 0,187 USD par plan, près du plafond de 0,20 USD. L'assemblage (0,053 USD) est le poste le plus cher.
- 31/10/2026 : 1er essai MTO : **Multi-Step Routes** activé pour régler la réception en 1 étape (réglage par défaut), et les 15 jours placés dans **Delivery Time** (délai client). Corrigé par une règle d'assemblage (écarter les confirmations de défaut, le multi-step non demandé et les données mal placées) et une règle du mode `config` (le délai fournisseur va au délai d'achat).
- 31/10/2026 : au 2e essai MTO, l'assemblage garde en dernière étape « Confirmer la commande client » (L2.6), qui est une action de test et pas un paramétrage, sourcée par `receipts_delivery_two_steps` (« À vérifier »). À surveiller au banc (tâche 7).
- 31/10/2026 : banc (rapport `docs/evaluation/2026-10-31-plan.md`) : MTO Incorrect à la passe du banc (Lumitech SAS reporté sur les standards), Partiel dans les 4 autres plans de la même version ; Thermo Partiel, 0 « Documenté » faux, 0 donnée inventée, mais 0,32 USD. Les pistes 1 à 7 du rapport sont hors plan, à arbitrer.
- 31/10/2026 (tâche 8) : 3 plans MTO sans Lumitech sur les standards, mais le plan n°3 perd l'activation de **Replenish on Order (MTO)** (A2) : l'assemblage peut écarter une étape « Documenté » utile. À traiter en tâche 11 (garder toute étape « Documenté » sauf doublon).
- 01/11/2026 (tâche 10) : repli web = Haiku 5.5 + `web_search_20260318` en appel direct (`allowed_callers: ["direct"]`) : c'est le seul mode qui rend des citations avec `cited_text` (avec le filtrage dynamique, aucune citation). Environ 0,024 USD par appel (2 recherches). Banc QCM : 26/30 inchangé, 0 « Documenté » faux, 0,035 USD et 18,9 s en moyenne, web sur 15 questions. Le web n'intervient pas sur la lettre choisie : il n'a corrigé aucune des 4 erreurs (Q13, Q18, Q22, Q26) ; piste hors plan : laisser le web trancher quand la couverture doc est `insufficient`.
- 01/11/2026 (tâche 11) : lots sans web et en effort `low`, extraction en effort `low`, assemblage par références (+ `a_chercher`), un seul appel web par plan (Haiku, `max_tokens` 12 000 : à 4 000, Haiku s'arrêtait avant d'écrire). Mesures : MTO 0,209 USD / 80 s, Thermo 0,346 USD / 89 s. Plancher : environ 0,035 USD par lot rédigé par Sonnet. Un premier essai a ramené du cross-dock (multi-step) par le web : interdit dans les consignes web et `a_chercher`.
- 01/11/2026 (tâche 12) : banc v2 (`docs/evaluation/2026-11-01-plan-v2.md`) : MTO Complet 3/3 (0,20 à 0,22 USD, 70 à 79 s) ; Thermo Partiel 2/2 (A7 Reach Stage ; A9 After-Sales dans 1 plan), 0 « Documenté » faux, 0 donnée inventée, 0,355 USD, 107 s. Correctifs ajoutés en cours de tâche : étapes « Documenté » écartées sans raison remises par le code, actions de test renvoyées dans `tests`, 3 besoins au plus par lot, conflit de version (route **Buy**) réglé par consigne. Deux essais annulés : 8 passages par page, besoins sans étape envoyés au web (ce dernier reconfigurait la réception et la livraison en 1 étape sur MTO). Tâche 12 non cochée : Thermo n'est pas Complet.
- 01/11/2026 : piste « page complète » ajoutée à `odoo-question` (nœuds `Pick passages` → `Load full pages` → `Select passages`, mode config seulement). Elle règle la question SLA seule, mais pas le banc (MTO 2 Complet / 1 Incorrect par une étape 🌐, Thermo 2 Partiel). Badge 🎬 vu sur Telegram (« nouveautés du Helpdesk ») ; badge 🌐 pas encore vu sur téléphone.
- 01/11/2026 : essai « lot des manques + contrôle web par Haiku » (choisi par Thomas) : contrôle web efficace, mais Thermo à 0,45-0,48 USD, A9 toujours absent, étapes non demandées ajoutées. Annulé, `odoo-plan` restauré depuis l'export. Le contrôle web seul (sans lot des manques) reste une piste réutilisable.

## Validation Phase 3

### Méthode utilisée
- B : déclencheurs réels (webhooks `odoo-plan` et `odoo-question`), banc de clôture de 5 plans, exécution Telegram du 01/11/2026 relue dans n8n.

### Tests réalisés
- [x] PDF depuis Telegram : `mto.pdf` → attente, résumé (19 étapes, dont 16 Documenté), fichier `plan-atelier-lumiere.md`, en 76 s pour 0,269 USD.
- [x] Plan MTO par le webhook : 74 s ; chaque étape a action, menu, champ, valeur, statut et source ; 3 tests, 9 questions.
- [x] MTO, banc de clôture : Complet 3/3, sans Buy, sans multi-step, sans donnée inventée ; 0,196 à 0,243 USD.
- [x] Non-régression : D001 même format ; Q01 = B ; banc QCM 26/30 avec 0 « Documenté » faux ; 403 sans jeton.
- [✗] Thermo Complet : Partiel 2/2 (A7, A9 ou A10 selon le tirage), sans « Documenté » faux ni donnée inventée.
- [✗] Coût de Thermo : 0,401 et 0,414 USD (plafond 0,40 USD).

### Verdict
- **⚠️ Partiel, accepté par Thomas le 01/11/2026** : les deux écarts de Thermo sont reportés en Phase 4 (PRD § 7).
