# STRUCTURE.md — Carte d'architecture du projet

> Ce fichier est **rempli automatiquement par `/architect`** Étape 6.5 après scaffold du repo. Il est ensuite **lu par `/prime`** au début de chaque session pour charger le contexte d'architecture rapidement.
>
> Tu peux le mettre à jour à la main si tu réorganises le projet après le scaffold initial. `/architect` ne réécrit pas par-dessus si le fichier existe déjà — il appendera dans une section "Modifications post-scaffold" si tu relances l'étape 6.

## Arborescence

<!-- architect:directories -->
- `workflows/` — fichiers `.workflow.json` exportés depuis n8n (1 par workflow), versionnés git
- `scripts/` — utilitaires CLI (import de la bibliothèque dans pgvector, banc de mesure / duel de modèles)
- `docs/` — brainstorms, plans de phase, procédures opérationnelles (ex : import bibliothèque, setup VPS)
- Matériel source hors repo : `~/Desktop/a-reprendre-odoo/` (bibliothèque v20, consignes IA, glossaire, jeux de test)
<!-- /architect:directories -->

## Patterns clés

<!-- architect:patterns -->
- 1 fichier `.workflow.json` par workflow n8n, versionné git, push via MCP `n8n_create_workflow` / `n8n_update_full_workflow`
- Telegram Trigger → filtre `chat_id` → aiguillage par type (texte / photo / PDF) → recherche pgvector → rédaction LLM → réponse Telegram
- Recherche : 1-5 sous-questions (glossaire FR→EN) → embeddings `gemini-embedding-2` → 8-12 passages diversifiés filtrés `odoo_version = '20.0'`
- Réponse structurée JSON avec statut (*Documenté / À vérifier / Non couvert*) + sources, puis mise en forme Telegram
- Secrets uniquement dans les credentials n8n (jamais dans les JSON exportés)
<!-- /architect:patterns -->

## Tests

<!-- architect:tests -->
- Tests via `n8n_test_workflow` MCP avec payload type, ou exécution manuelle dans l'UI n8n
- Banc de mesure rejouable sur les jeux de test (106 questions doc + 12 de référence + échantillon QCM corrigé) — résultats datés dans `docs/`
<!-- /architect:tests -->

## Conventions d'arborescence

<!-- architect:conventions -->
- Nommage workflows : `[ENV] {scope}-{action}` (ex : `[DEV] telegram-question-texte`, `[PROD] telegram-assistant`)
- Fichiers : kebab-case ; export workflow = `workflows/{scope}-{action}.workflow.json`
- Libellés Odoo en anglais, explications en français
<!-- /architect:conventions -->

## Intégrations externes

<!-- structure:integrations -->
- **n8n** self-hosted Hostinger (`https://n8n-ijcp.srv1468750.hstgr.cloud`) — MCP `n8n-mcp` en mode API
- **Telegram Bot API** — interface utilisateur (credential n8n)
- **Postgres + pgvector** — conteneur Docker sur le VPS, tables `knowledge_sources` / `knowledge_chunks`
- **Google Gemini API** — `gemini-embedding-2` (embeddings)
- **Anthropic API** — Claude Sonnet 5.5 (rédaction + vision)
- **runbot.odoo.com** — vérification manuelle des réponses « À vérifier »
<!-- /structure:integrations -->

## Fichiers clés

<!-- structure:key-files -->
- `PRD.md` — scope, phases, critères de succès
- `workflows/` — workflows n8n exportés (vide à l'init)
- `.mcp.json` (gitignoré) — config MCP n8n avec clé API
- `~/Desktop/a-reprendre-odoo/bibliotheque/knowledge-20.0.sql.gz` + `schema-tables-bibliotheque.ts` — données et schéma de la bibliothèque
<!-- /structure:key-files -->

## Évolutions livrées (résumé)

<!-- structure:evolutions-summary -->
_(Aucune évolution livrée pour l'instant.)_
<!-- /structure:evolutions-summary -->
