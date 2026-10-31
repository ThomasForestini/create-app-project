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

- [ ] **1. Scénarios du banc + grille Thermo.** Fait quand :
  - `docs/evaluation/plan/` contient `mto.pdf` et `thermo.pdf` (texte des scénarios rendu en PDF), `maigre.pdf` (copie de `besoins.pdf`) et `grille-mto.md` (copie de la grille figée).
  - `grille-thermo.md` est pré-remplie au format de la grille MTO : attendus sourcés v20, édition requise, questions attendues, erreurs à éviter.
  - Thomas a relu et marqué la grille Thermo `validée`.
- [ ] **2. Mode `config` dans `odoo-question`.** Fait quand :
  - Un `curl` avec le besoin « luminaires sur mesure commandés au fournisseur à la commande client » renvoie des `etapes[]` (`action`, `menu`, `champ`, `valeur`, `statut`, `source`).
  - On y trouve **Replenish on Order (MTO)**, avec une source `mto.html`.
  - D001 (texte) et Q01 (qcm) gardent le même format (non-régression).
  - L'export `workflows/odoo-question.workflow.json` est à jour.
- [ ] **3. `[DEV] odoo-plan` : extraction des besoins** (après 1). Fait quand :
  - `curl` avec `mto.pdf` renvoie les besoins de la grille, Lumitech SAS, 15 jours et Lyon, sans prix ni fournisseur inventés.
  - La question sur la validation des commandes fournisseurs figure dans `questions_ouvertes`.
  - `maigre.pdf` renvoie surtout des questions.
  - Sans jeton, la réponse est 403.
- [ ] **4. Boucle sur les besoins + assemblage** (après 2, 3). Fait quand :
  - `curl` avec `mto.pdf` renvoie un plan ordonné (A2 avant A3, fournisseur créé avant l'onglet Purchase), le test T1, ses questions et un Markdown.
  - La route **Buy** n'apparaît pas et aucune étape multi-step n'est proposée.
  - Le plan arrive en moins de 3 min pour 0,20 USD au plus.
  - `workflows/odoo-plan.workflow.json` est exporté.
- [ ] **5. PDF et `plan:` dans `telegram-assistant`** (après 4). Fait quand :
  - `mto.pdf` envoyé depuis le téléphone reçoit un résumé et le fichier `.md` en moins de 3 min.
  - Un document qui n'est pas un PDF reçoit un message clair.
  - La photo de QCM et la question texte marchent toujours.
  - Les exports sont à jour.
- [ ] **6. Script `scripts/banc-plan.py`** (après 1, 4). Fait quand :
  - Une passe sur `mto.pdf` écrit `docs/evaluation/{date}-plan.json` : plan, latence, coût par appel.
  - Elle écrit aussi une feuille de notation pré-remplie : chaque élément de la grille est trouvé ou absent, avec le statut et la source du plan.
  - URL et jeton sont lus depuis `.env`, et le jeton apparaît 0 fois dans le code (`grep`).
- [ ] **7. Passe complète + rapport** (après 6). Fait quand :
  - `docs/evaluation/{date}-plan.md` note MTO et Thermo (Complet / Partiel / Incorrect, élément par élément).
  - Le rapport compte les instructions fausses marquées « Documenté » et les données inventées.
  - Il compare latence et coût aux critères du PRD et à la V3 de l'ancien projet (0,054 USD, partiel).
  - Il donne des pistes si un scénario n'est pas « Complet ».

## Critère de phase complète

- [ ] Tâches 1 à 7 cochées
- [ ] Depuis Telegram, un PDF client reçoit un plan Odoo 20 étape par étape (menus, champs et valeurs en EN, statut et source par étape) et les questions ouvertes
- [ ] MTO est **Complet**, ou au minimum « Partiel sans instruction fausse » comme la V3. Thermo a 0 instruction fausse en « Documenté » et 0 donnée inventée.
- [ ] Moins de 3 min et 0,20 USD au plus par plan (PRD)

## Points à surveiller

- **Coût de Thermo** : une dizaine de besoins à 0,024 USD environ, plus l'extraction et l'assemblage, risquent de dépasser 0,20 USD. S'il le faut, on regroupera les besoins proches avant la boucle.
- **Édition** : MTO est noté en Community, mais Thermo demande Enterprise (Field Service, Subscriptions, Sign). L'extraction doit le signaler, et la grille Thermo l'attend.

## Prochaine étape

`/execute docs/plans/phase-3-plan.md`
