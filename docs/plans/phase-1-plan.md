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

- [x] **1. Postgres + pgvector sur le VPS, bibliothèque v20 importée** — conteneur `pgvector/pgvector` sur le réseau Docker de n8n, sans port public ; import de `knowledge-20.0.sql.gz` ; index HNSW ; procédure dans `docs/setup-pgvector.md`. Fait quand : `SELECT count(*) FROM knowledge_chunks WHERE odoo_version='20.0'` ≈ 8 963 ; une requête de similarité répond en < 1 s ; `nc -z <ip-publique> 5432` échoue depuis le Mac ; fraîcheur contrôlée en comparant ~10 pages de la bibliothèque avec leur version en ligne sur `odoo.com/documentation/20.0`, écart noté dans le doc.
- [x] **2. Bot Telegram + credentials n8n** — bot créé via @BotFather, `chat_id` récupéré ; credentials Postgres, Gemini, Telegram, Header Auth (webhook) créées dans n8n (Anthropic existe déjà) ; valeurs non secrètes en placeholders dans `.env.example`. Fait quand : `n8n_manage_credentials` liste les 5 credentials ; un workflow jetable obtient un vecteur de 1 536 dimensions depuis Gemini et lit une ligne de `knowledge_chunks` ; le bot répond à `/start` (test manuel).
- [x] **3. Recherche dans `[DEV] odoo-question`** (après 1 et 2) — question → 1 à 5 sous-questions en anglais avec le glossaire FR→EN → embeddings `gemini-embedding-2` → pgvector filtré `odoo_version='20.0'` → 8 à 12 passages diversifiés (plafond de passages par page). Fait quand : `n8n_test_workflow` sur D001 renvoie 8 à 12 passages dont un de la page `finance/accounting/bank` ; workflow exporté dans `workflows/odoo-question.workflow.json`.
- [x] **4. Réponse sourcée + contrôle sur le site officiel + webhook** (après 3) — rédaction avec les consignes de l'ancien projet (11 règles, schéma JSON) ; paramètre `model` (Sonnet 5.5 / Gemini) ; second appel de contrôle qui relit en direct la page complète des 1 à 3 sources citées sur `odoo.com/documentation/20.0` et passe en « À vérifier » toute affirmation non justifiée ; si le site ne répond pas, contrôle sur les extraits de la bibliothèque sans bloquer ; webhook protégé Header Auth. Fait quand : `curl` sur D001 renvoie un JSON conforme (`statut` ∈ {Documenté, À vérifier, Non couvert}, ≥ 1 URL source issue des passages) ; question hors sujet (« recette des crêpes ») → `Non couvert` ; appel sans en-tête → 401/403 ; site simulé indisponible (URL invalide) → réponse quand même renvoyée ; export à jour.
- [x] **5. Workflow `[DEV] telegram-assistant`** (après 4) — Telegram Trigger → filtre `chat_id` → appel `odoo-question` → mise en forme simple (statut, réponse, liens), tronquée à 4 096 caractères (découpage propre en Phase 4). Fait quand : une question texte envoyée depuis le téléphone reçoit une réponse sourcée en < 60 s ; un message d'un autre compte s'arrête au filtre (vérifié dans `n8n_executions`) ; exporté dans `workflows/telegram-assistant.workflow.json`.
- [x] **6. Script de banc `scripts/duel-modeles`** (après 4) — rejoue `questions-doc.json` (106) et `i5-questions.json` (12) sur le webhook pour un modèle donné ; enregistre réponse, statut, sources, latence, coût dans `docs/evaluation/{date}-{model}.json` ; calcule le rappel des pages attendues parmi les sources citées ; URL et jeton du webhook lus depuis `.env`. Fait quand : une passe de 5 questions produit le JSON + un résumé (rappel, répartition des statuts, coût moyen, latence moyenne) ; `grep` du jeton dans le code = 0 résultat.
- [x] **7. Duel + choix du modèle** (après 6) — passe complète Sonnet 5.5 et meilleur Gemini du moment (identifié au moment du duel) ; grille pré-remplie fournie, notation manuelle des 12 questions de référence (Complète / Partielle / Incorrecte). Règle de décision : 1) moins d'« Incorrecte », 2) plus de « Complète », 3) meilleur rappel sur les 106, 4) coût le plus bas. Fait quand : `docs/evaluation/{date}-duel.md` contient le tableau comparatif + verdict ; modèle gagnant fixé par défaut dans `odoo-question` ; `CLAUDE.md ## Stack` mis à jour ; coût moyen du gagnant ≤ 0,05 USD par question.

## Notes

- Les 12 questions de référence mélangent v18/19/20 ; la bibliothèque est v20 uniquement : sur les questions 18/19 on vérifie surtout que l'assistant signale l'écart de version.
- Seuil de rappel à 95 % (ancien projet : 99 %), marge car les sous-questions sont désormais générées dans n8n.

## Découvertes (hors plan)

- 26/10/2026 : la v20 compte 10 355 passages, pas 8 963 : documentation 8 963 + structure du logiciel 1 102 + vidéos 290. La tâche 3 doit décider si la recherche filtre `kind = 'odoo_documentation'` ou garde les trois.
- 26/10/2026 : 57 pages sur 1 126 ont changé en ligne depuis l'import du 18/10, et 46 pages en ligne manquent dans la bibliothèque (détail dans `docs/setup-pgvector.md`). À prévoir : une réindexation périodique.

- 26/10/2026 (tâche 3) : sous-questions générées par **Claude Haiku 5.5** (outil forcé), pas par Gemini. L'API de génération Gemini était instable ce jour-là (`gemini-3.1-flash-lite` : 30 à 60 s pour 94 tokens ; `gemini-3.8-flash` : 503 ; `gemini-2.5-flash-lite` : retiré). Les embeddings Gemini restent rapides (< 0,5 s). Haiku 5.5 refuse le paramètre `temperature`.
- 26/10/2026 (tâche 3) : la recherche est exacte (parcours complet, ~0,5 s pour 5 requêtes), sans l'index HNSW. Le planificateur ne l'utilise pas dans une jointure latérale. Piège évité : sans `with … as materialized`, le texte était reconverti en vecteur à chaque ligne (16 s).
- 26/10/2026 (tâche 3) : recherche vectorielle seule, documentation officielle uniquement. L'ancien moteur avait aussi du plein texte, des sections voisines et des places réservées à la structure du logiciel : à ajouter seulement si le rappel de la tâche 6 est < 95 %.
- 26/10/2026 (tâche 3) : test fait en `curl` sur le webhook protégé (même chemin que `n8n_test_workflow`, qui ne peut pas porter le jeton sans l'exposer). D001 : 12 passages, n° 1 = passage de référence `bank.html#create-a-bank-account`, 3,4 s. Contrôle D020, D050, D090 : page attendue trouvée.
- 26/10/2026 (tâche 4) : rédaction Claude par sorties structurées (`output_config.format`), car Sonnet 5.5 refuse l'outil forcé (400). Contrôle des citations par **Haiku 5.5**, qui relit les 1 à 3 pages les plus citées en direct et passe en « À vérifier » tout ce qui n'est pas confirmé (raison « Modifié en ligne : … » si la page a changé). Paramètre d'entrée `docsBase` ajouté pour simuler un site indisponible.
- 26/10/2026 (tâche 4) : mesures sur D001 : Sonnet 5.5 → 27 s, 0,026 USD, 9 éléments documentés sur 11 ; `gemini-3.1-flash-lite` → 15 s, 0,003 USD ; `gemini-3.8-flash` → 503 « high demand » (deux essais). Hors sujet → « Non couvert » en 6 s. Sans jeton ou mauvais jeton → 403. Site indisponible → réponse renvoyée, contrôle sur les extraits.
- 27/10/2026 (tâche 5) : question depuis le téléphone → réponse sourcée en 29 s (exécution n8n 282, 31,5 s de bout en bout). Pas de second compte Telegram : filtre vérifié avec une copie à l'identique du nœud Filter alimentée par de faux messages (exécutions 284-286) → `chat_id` 111222333 bloqué, `chat_id` 5688120478 accepté, photo bloquée. Test réel avec un autre compte à refaire si l'occasion se présente.
- 27/10/2026 (tâche 6) : `scripts/duel-modeles.py` (Python, bibliothèque standard). Passe de 5 questions Sonnet 5.5 → rappel 5/5, 22,9 s et 0,025 USD en moyenne (`docs/evaluation/2026-10-27-claude-sonnet-5-5-essai-2125.json`). Jeton : 0 occurrence dans `scripts/`, `workflows/`, `docs/`. Le statut « Documenté » est rare (1 sur 5) : il exige couverture complète + tous les éléments confirmés + aucune piste. À garder en tête pour la lecture du duel.
- 27/10/2026 (tâche 7) : la clé Gemini était en niveau gratuit (quota 0 sur Pro/Argon, Flash relégués en basse priorité : c'est la cause des 503 et lenteurs des tâches 3 et 4). Facturation activée par Thomas. Duel Sonnet 5.5 contre `gemini-4-argon` : égalité sur les 3 premiers critères (2 Incorrecte, 0 Complète, rappel 100 % chacun), Sonnet gagne au coût durable (0,024 contre 0,036 USD dès le 01/12). Notation reçue en PDF (la page de notation en ligne n'a pas servi).
- 27/10/2026 (tâche 7) : aucune réponse « Complète » sur les 12 questions de référence et les mêmes erreurs de version pour les deux modèles (Q10, Q11) → limites de la chaîne (8-12 passages pour des processus multi-pages, bibliothèque v20 seule), pas du modèle. Pistes dans `docs/evaluation/2026-10-27-duel.md`.

## Critère de phase complète

- [ ] Toutes les tâches 1 à 7 sont cochées
- [ ] Depuis Telegram, une question texte Odoo 20 reçoit une réponse avec statut + lien vers la doc officielle v20 ; tout autre `chat_id` est ignoré
- [ ] Rappel des pages attendues sur les 106 questions doc ≥ 95 %
- [ ] Modèle de rédaction figé sur une mesure, pas sur un pari

## Prochaine étape

`/execute docs/plans/phase-1-plan.md`

## Validation Phase 1

### Méthode utilisée
- B : test workflow n8n — appels réels du webhook, exécutions n8n lues via l'API, base pgvector interrogée sur le VPS, message Telegram envoyé depuis le téléphone (27/10/2026).

### Tests réalisés
- [x] Workflows `[DEV] odoo-question` (20 nœuds) et `[DEV] telegram-assistant` (7 nœuds) actifs, validation n8n 0 erreur / 0 avertissement
- [x] Conteneur `pgvector` healthy, 10 355 passages v20 (8 963 documentation) ; port 5432 fermé depuis Internet
- [x] Webhook sans jeton → 403, mauvais jeton → 403
- [x] Hors sujet (crêpes) → « Non couvert » en 6 s
- [x] Site officiel indisponible → réponse renvoyée (15 s), contrôle sur les extraits
- [x] Échantillon neuf D040-D049 → 10/10 pages attendues, 21,6 s et 0,023 USD en moyenne
- [x] Rappel sur les 106 questions doc : 100 % (duel du 27/10/2026)
- [x] Telegram de bout en bout : exécution 560 (filtre passé → odoo-question → message envoyé, 17,8 s) et 561 (sous-workflow, 4 sources v20, contrôle en ligne, 0,021 USD)
- [x] Modèle figé sur une mesure : Sonnet 5.5 (`docs/evaluation/2026-10-27-duel.md`)
- [~] Autre `chat_id` ignoré : vérifié par une copie identique du nœud Filter (pas de second compte Telegram)

### Verdict
- **✅ OK**

### Points non bloquants
- Site indisponible : la réponse peut afficher « Documenté » alors que la légende Telegram dit « vérifié sur la doc en ligne » → adapter le texte en Phase 4.
- Aucune réponse « Complète » sur les 12 questions de référence (processus multi-modules, questions v18/v19) → pistes dans le rapport du duel.
