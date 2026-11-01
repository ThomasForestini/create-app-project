# Plan — Phase 4 : Robustesse

> PRD parent : `PRD.md`
> Date : 2026-11-01

## Architecture retenue

- **Coût** : cache de prompt Anthropic (`cache_control`) sur la partie commune des appels de lot de `odoo-question` en mode `config` (consignes, glossaire). Les lots partent aujourd'hui en parallèle. Si le cache n'est jamais relu, le premier lot passe seul et les autres suivent.
- **Thermo** : avec l'économie réalisée, un besoin par lot pour les besoins Helpdesk et Field Service, au lieu de 3 au plus.
- **Journal** : table `journal` dans le Postgres pgvector du VPS, écrite par `telegram-assistant` à chaque réponse, y compris en cas d'erreur.
- **Telegram** : découpage en plusieurs messages de 4 096 caractères au plus, sans casser les balises HTML. Erreurs nommées (type de demande, étape, n° d'exécution), plus un workflow Error Trigger pour les pannes hors branches.
- **PROD** : copie `[PROD]` des 4 workflows sur le bot actuel. Les `[DEV]` passent sur un nouveau bot, et le banc continue de viser les webhooks `[DEV]`.
- Hors de cette phase : QCM à 90 % (26/30 aujourd'hui), réservé à une évolution dédiée (`/evoluer`).

## Tâches

- [x] **1. Cache de prompt dans les lots `config`.** Fait quand :
  - dans un plan MTO, les lots 2 et suivants montrent `cache_read_input_tokens` > 0 ;
  - le calcul du coût applique les tarifs d'écriture et de lecture du cache ;
  - ~~3 plans MTO coûtent moins qu'en fin de Phase 3 (0,196 à 0,243 USD)~~ remplacé (décision de Thomas, 01/11/2026) par le gain mesuré à plan égal : 3 076 tokens relus par lot, soit −0,0055 USD par lot (−7 à 8 % par plan MTO) ; 3 plans MTO restent Complet (0,227, 0,212 et 0,284 USD) ;
  - D001 (texte) et Q01 (qcm) gardent le même format ; l'export `odoo-question` est à jour.
- [x] **2. Lots Helpdesk / Field Service liés + banc Thermo** (après 1 ; revue le 01/11/2026 après un essai à 0,506 USD, voir Découvertes). Fait quand :
  - la règle 7 de l'extraction prévoit un lot Helpdesk (tickets, alias, SLA, et planification d'intervention depuis le ticket) et un lot Field Service (feuille, rapport, signature, facturation des interventions) ; le plafond passe à 6 lots (prompt et `Read extraction`) ;
  - dans un plan Thermo, la question du lot Helpdesk nomme la planification depuis le ticket, et le plan contient **After-Sales** → **Field Service** et **Plan Intervention** (A9) ;
  - critère remplacé (décision de Thomas, 01/11/2026, après 3 essais) : 3 plans Thermo avec la règle finale, chacun à 0 « Documenté » faux, 0,50 USD au plus, moins de 3 min et au moins 14 éléments présents sur 16 (A1 à A16), un élément présent en partie comptant comme présent (décision de Thomas) : 15, 14 et 16 sur 16, 0,425 à 0,436 USD, 113 à 139 s ; MTO Complet 3/3 (0,176 à 0,243 USD) ; rapport `2026-11-01-plan-v4.md` ; le Complet à chaque tirage passe à une évolution dédiée. Critère d'origine : ~~3 plans Thermo de suite sont notés **Complet** élément par élément (A7, A9 et A10 compris ; A10 est compté présent s'il figure en entier dans un test, avec la page `field_service` citée : décision de Thomas du 01/11/2026), chacun à 0,50 USD au plus (plafond relevé de 0,40 USD par Thomas le 01/11/2026, premier tirage à 0,467 USD) et en moins de 3 min~~ ;
  - 3 plans MTO restent Complet ;
  - aucun « Documenté » faux, aucune donnée inventée ;
  - le rapport `docs/evaluation/{date}-plan-v4.md` est écrit, et les exports sont à jour.
- [ ] **3. Table `journal` (Postgres).** Fait quand :
  - `scripts/pgvector/journal.sql` crée la table : `ts`, `type` (texte, qcm ou plan), `duree_ms`, `cout_usd`, `statut`, `erreur`, `execution_id` ;
  - après 1 question, 1 photo et 1 PDF sur Telegram, `select` renvoie 3 lignes, avec la durée et le coût renseignés ;
  - une panne de l'insertion ne bloque pas la réponse (`onError` continue).
- [ ] **4. Découpage des messages longs.** Fait quand :
  - une réponse ou un résumé de plan de plus de 4 096 caractères arrive en plusieurs messages, chacun de 4 096 caractères au plus ;
  - aucune erreur Telegram « can't parse entities » ;
  - plus aucune mention « tronqué » ;
  - les messages courts arrivent toujours en un seul message.
- [ ] **5. Erreurs visibles** (après 3). Fait quand :
  - en forçant une panne (sous-workflow désactivé, puis clé Anthropic invalide sur une copie DEV), Telegram reçoit en moins de 30 s un message qui nomme le type de demande, l'étape en échec et le n° d'exécution n8n ;
  - le journal porte une ligne `statut = erreur` ;
  - une exception dans un nœud de mise en forme est signalée par le workflow Error Trigger.
- [ ] **6. Bot DEV + workflows `[PROD]`** (après 1 à 5). Fait quand :
  - Thomas a créé le bot DEV (BotFather) et sa credential existe dans n8n ;
  - une question, une photo et un PDF envoyés au bot actuel produisent des exécutions `[PROD]` seulement ;
  - les mêmes envois au bot DEV produisent des exécutions `[DEV]` ;
  - aucun `[PROD]` n'appelle un ID de workflow `[DEV]` (vérifié par `grep` sur les exports) ;
  - les exports `[PROD]` sont versionnés dans `workflows/`.
- [ ] **7. Passe de non-régression + bilan des critères du PRD** (après 6). Fait quand :
  - `banc-qcm.py` donne au moins 26/30, 0 « Documenté » faux et 0,05 USD au plus par question ;
  - une requête sur `journal` donne la latence et le coût moyens par type, comparés aux critères du PRD (< 60 s par photo, < 3 min par PDF, 0,05 USD par question, 0,50 USD par plan) ;
  - le résultat est ajouté au rapport de la tâche 2.

## Critère de phase complète

- [ ] Les tâches 1 à 7 sont cochées.
- [ ] Le bot `[PROD]` traite les questions, les photos et les PDF. Chaque réponse est journalisée, les messages longs sont découpés, les pannes sont nommées sur Telegram, et Thermo comme MTO sont Complet à chaque tirage pour 0,50 USD au plus.

## Découvertes (hors plan)

- 01/11/2026 : préfixe mis en cache dans un lot `config` = 3 076 tokens (consignes + schéma) sur 10 000 à 14 000 en entrée de la rédaction. Gain mesuré : 0,0055 USD par lot qui relit le cache, moins 0,0015 USD d'écriture pour le lot 1, soit environ 0,01 à 0,02 USD par plan MTO (7 à 8 %). L'écart d'un tirage à l'autre (3 ou 4 lots, page complète, étape web) va de 0,18 à 0,28 USD et masque ce gain.
- 01/11/2026 : bug de Phase 3 corrigé pendant la tâche 1 parce qu'il bloquait « MTO Complet » : `Finalize plan` créait un fournisseur « 15 jours » quand l'extraction nommait la donnée « Délai de livraison fournisseur » (déjà présent au tirage MTO n°2 de `2026-11-01-plan-v3-mto.json`). Le filtre ne garde plus que les données intitulées « Fournisseur » ou « Vendor ».

- 01/11/2026 : tâche 2, premier essai Thermo (règle « un besoin Helpdesk ou Field Service seul dans son lot », plafond passé de 5 à 9 lots, poussé sur `[DEV] odoo-plan`) : 8 lots, 0,506 USD, 119 s. L'extraction n'applique la règle qu'en partie : planification et rapport signé restent ensemble dans un lot, tickets et SLA sont fusionnés en un seul besoin. **Reach Stage** est présent, mais **Plan Intervention** (A9) et **Sign Report** (A10) manquent toujours. Résultat : Partiel, au-dessus du plafond de 0,40 USD. Tâche 2 revue (lots Helpdesk / Field Service liés, 6 lots au plus) : 0,467 USD, A9 réglé ; plafond relevé à 0,50 USD par Thomas. Deux besoins (facturation sans compta, logo) restaient hors des 6 lots : la règle 7 exige maintenant que chaque besoin entre dans un lot, et les abonnements ne vont plus dans le lot Field Service. Tirage suivant (0,433 USD, 130 s) : tous les besoins sont dans un lot ; A7, A9, A12 et A14 sont présents ; A10 est incomplet dans le test (ni **Sign In** ni **Customer Preview**), A11 aussi (pas de projet **Billable** avec **Timesheets**), et A13 (**Invoicing**) n'est pas résolu. Le lot Field Service, avec ses 3 besoins, reste le point faible.

## Prochaine étape

`/execute docs/plans/phase-4-plan.md`
