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

- [ ] **1. Cache de prompt dans les lots `config`.** Fait quand :
  - dans un plan MTO, les lots 2 et suivants montrent `cache_read_input_tokens` > 0 ;
  - le calcul du coût applique les tarifs d'écriture et de lecture du cache ;
  - 3 plans MTO coûtent moins qu'en fin de Phase 3 (0,196 à 0,243 USD) et restent Complet ;
  - D001 (texte) et Q01 (qcm) gardent le même format ; l'export `odoo-question` est à jour.
- [ ] **2. Lots fins Helpdesk / Field Service + banc Thermo** (après 1). Fait quand :
  - un besoin Helpdesk ou Field Service part seul dans son lot ;
  - 3 plans Thermo de suite sont notés **Complet** élément par élément (A7, A9 et A10 compris), chacun à 0,40 USD au plus et en moins de 3 min ;
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
  - une requête sur `journal` donne la latence et le coût moyens par type, comparés aux critères du PRD (< 60 s par photo, < 3 min par PDF, 0,05 USD par question, 0,40 USD par plan) ;
  - le résultat est ajouté au rapport de la tâche 2.

## Critère de phase complète

- [ ] Les tâches 1 à 7 sont cochées.
- [ ] Le bot `[PROD]` traite les questions, les photos et les PDF. Chaque réponse est journalisée, les messages longs sont découpés, les pannes sont nommées sur Telegram, et Thermo comme MTO sont Complet à chaque tirage pour 0,40 USD au plus.

## Prochaine étape

`/execute docs/plans/phase-4-plan.md`
