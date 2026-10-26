# Plan — Phase 1 : Socle + question texte

> PRD parent : `PRD.md`
> Date : 2026-10-26

## Architecture retenue

- `[DEV] odoo-question` : cœur recherche + réponse. Deux déclencheurs : Execute Workflow Trigger (appel par Telegram) et webhook protégé Header Auth (`POST {question, model}`, utilisé par le banc).
- `[DEV] telegram-assistant` : Telegram Trigger → filtre `chat_id` → appel du cœur → réponse.
- Bibliothèque pgvector = **trouver** les passages (recherche sémantique FR → doc EN). Site officiel `odoo.com/documentation/20.0` = **vérifier** (relecture des pages citées en direct, contrôle de fraîcheur).
- Postgres sur le réseau Docker de n8n, aucun port public.
- Le duel rejoue la chaîne de production via le webhook : même recherche, seule la rédaction change.

## Tâches

- [ ] **1. Postgres + pgvector sur le VPS, bibliothèque v20 importée** — conteneur `pgvector/pgvector` sur le réseau Docker de n8n, sans port public ; import de `knowledge-20.0.sql.gz` ; index HNSW ; procédure dans `docs/setup-pgvector.md`. Fait quand : `SELECT count(*) FROM knowledge_chunks WHERE odoo_version='20.0'` ≈ 8 963 ; une requête de similarité répond en < 1 s ; `nc -z <ip-publique> 5432` échoue depuis le Mac ; fraîcheur contrôlée en comparant ~10 pages de la bibliothèque avec leur version en ligne sur `odoo.com/documentation/20.0`, écart noté dans le doc.
- [ ] **2. Bot Telegram + credentials n8n** — bot créé via @BotFather, `chat_id` récupéré ; credentials Postgres, Gemini, Telegram, Header Auth (webhook) créées dans n8n (Anthropic existe déjà) ; valeurs non secrètes en placeholders dans `.env.example`. Fait quand : `n8n_manage_credentials` liste les 5 credentials ; un workflow jetable obtient un vecteur de 1 536 dimensions depuis Gemini et lit une ligne de `knowledge_chunks` ; le bot répond à `/start` (test manuel).
- [ ] **3. Recherche dans `[DEV] odoo-question`** (après 1 et 2) — question → 1 à 5 sous-questions en anglais avec le glossaire FR→EN → embeddings `gemini-embedding-2` → pgvector filtré `odoo_version='20.0'` → 8 à 12 passages diversifiés (plafond de passages par page). Fait quand : `n8n_test_workflow` sur D001 renvoie 8 à 12 passages dont un de la page `finance/accounting/bank` ; workflow exporté dans `workflows/odoo-question.workflow.json`.
- [ ] **4. Réponse sourcée + contrôle sur le site officiel + webhook** (après 3) — rédaction avec les consignes de l'ancien projet (11 règles, schéma JSON) ; paramètre `model` (Sonnet 5.5 / Gemini) ; second appel de contrôle qui relit en direct la page complète des 1 à 3 sources citées sur `odoo.com/documentation/20.0` et passe en « À vérifier » toute affirmation non justifiée ; si le site ne répond pas, contrôle sur les extraits de la bibliothèque sans bloquer ; webhook protégé Header Auth. Fait quand : `curl` sur D001 renvoie un JSON conforme (`statut` ∈ {Documenté, À vérifier, Non couvert}, ≥ 1 URL source issue des passages) ; question hors sujet (« recette des crêpes ») → `Non couvert` ; appel sans en-tête → 401/403 ; site simulé indisponible (URL invalide) → réponse quand même renvoyée ; export à jour.
- [ ] **5. Workflow `[DEV] telegram-assistant`** (après 4) — Telegram Trigger → filtre `chat_id` → appel `odoo-question` → mise en forme simple (statut, réponse, liens), tronquée à 4 096 caractères (découpage propre en Phase 4). Fait quand : une question texte envoyée depuis le téléphone reçoit une réponse sourcée en < 60 s ; un message d'un autre compte s'arrête au filtre (vérifié dans `n8n_executions`) ; exporté dans `workflows/telegram-assistant.workflow.json`.
- [ ] **6. Script de banc `scripts/duel-modeles`** (après 4) — rejoue `questions-doc.json` (106) et `i5-questions.json` (12) sur le webhook pour un modèle donné ; enregistre réponse, statut, sources, latence, coût dans `docs/evaluation/{date}-{model}.json` ; calcule le rappel des pages attendues parmi les sources citées ; URL et jeton du webhook lus depuis `.env`. Fait quand : une passe de 5 questions produit le JSON + un résumé (rappel, répartition des statuts, coût moyen, latence moyenne) ; `grep` du jeton dans le code = 0 résultat.
- [ ] **7. Duel + choix du modèle** (après 6) — passe complète Sonnet 5.5 et meilleur Gemini du moment (identifié au moment du duel) ; grille pré-remplie fournie, notation manuelle des 12 questions de référence (Complète / Partielle / Incorrecte). Règle de décision : 1) moins d'« Incorrecte », 2) plus de « Complète », 3) meilleur rappel sur les 106, 4) coût le plus bas. Fait quand : `docs/evaluation/{date}-duel.md` contient le tableau comparatif + verdict ; modèle gagnant fixé par défaut dans `odoo-question` ; `CLAUDE.md ## Stack` mis à jour ; coût moyen du gagnant ≤ 0,05 USD par question.

## Notes

- Les 12 questions de référence mélangent v18/19/20 ; la bibliothèque est v20 uniquement : sur les questions 18/19 on vérifie surtout que l'assistant signale l'écart de version.
- Seuil de rappel à 95 % (ancien projet : 99 %), marge car les sous-questions sont désormais générées dans n8n.

## Critère de phase complète

- [ ] Toutes les tâches 1 à 7 sont cochées
- [ ] Depuis Telegram, une question texte Odoo 20 reçoit une réponse avec statut + lien vers la doc officielle v20 ; tout autre `chat_id` est ignoré
- [ ] Rappel des pages attendues sur les 106 questions doc ≥ 95 %
- [ ] Modèle de rédaction figé sur une mesure, pas sur un pari

## Prochaine étape

`/execute docs/plans/phase-1-plan.md`
