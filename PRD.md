<!--
PRD vivant discipliné. Cap 100 lignes hard.
Mis à jour par /evoluer (déplace checkboxes Hors scope → Scope actuel, append Implementation Phases).
JAMAIS réécrit destructivement.
-->

# PRD — Assistant Odoo

> Niveau : **STANDARD** · project_type : automation · Créé le 25/10/2026

## 1. Vision

Un assistant personnel sur Telegram, propulsé par n8n, qui répond avec précision et sources à l'appui sur Odoo 20 : bonne réponse expliquée à une photo de QCM de certification, puis plan de configuration détaillé (menus, champs, valeurs en anglais) à partir d'un PDF client. En cas de doute, il le dit au lieu d'inventer.

## 2. Personas

- **Thomas** — consultant Odoo en préparation de certification. Depuis son téléphone, il envoie une photo de QCM ou un PDF client. Douleur : vérifier chaque réponse ou chaque chemin de menu dans la doc v20 prend du temps, et les corrigés disponibles sont faux à ~20 %.

## 3. Scope actuel (V1)

### Core
- [x] Question texte → réponse sourcée (statut *Documenté / À vérifier / Non couvert* + lien doc v20)
- [ ] Photo de QCM → bonne(s) réponse(s) + brève explication + source, signalement si la doc v20 contredit une question pensée v19
- [ ] PDF client → plan de configuration Odoo 20 étape par étape (menus, champs, valeurs en EN)

### Technique
- [x] Postgres + pgvector en conteneur sur le VPS Hostinger (à côté de n8n), bibliothèque Odoo 20 rechargée depuis `knowledge-20.0.sql.gz`
- [x] Bot Telegram filtré sur mon seul `chat_id`
- [x] Recherche : `gemini-embedding-2` (1 536 dim), 1-5 sous-questions, 8-12 passages diversifiés, glossaire FR→EN
- [x] Rédaction : Claude Sonnet 5.5 (pari de départ), confirmé ou remplacé par le duel de la Phase 1
- [x] Workflows n8n versionnés dans `workflows/*.workflow.json`
- [ ] Banc de mesure rejouable (jeux de test existants + échantillon QCM corrigé)

## 4. Hors scope (différé)

- [ ] Odoo 19 (réindexation ≈ 0,15 USD) — seulement si le pool v19 diverge trop de la v20
- [ ] Interface web — Telegram suffit pour un usage perso ; c'est ce qui a alourdi l'ancien projet
- [ ] Multi-utilisateurs / authentification
- [ ] Rafraîchissement automatique de la bibliothèque depuis `odoo/documentation` branche 20.0
- [ ] Mémoire de conversation (questions de suivi sur la réponse précédente)

## 5. Constraints non-négociables

- Précision avant tout : chaque réponse porte un statut et au moins une source ; jamais de réponse « Documenté » sans passage de doc qui la justifie.
- Source de vérité = doc officielle Odoo **20** indexée. Les réponses en vert du PDF de certification ne servent jamais de corrigé.
- Libellés Odoo (menus, champs) en anglais comme dans l'interface ; explications en français.
- Usage strictement personnel : tout message d'un autre `chat_id` est ignoré.
- Aucun secret en clair dans le repo (credentials stockés dans n8n, `.env` gitignoré).
- Simplicité : pas d'infrastructure ajoutée tant que le cœur (précision) n'est pas mesuré.

## 6. Success Criteria

- ≥ 90 % de bonnes réponses sur un échantillon de 30 questions du PDF de certification, corrigé vérifié à la main (doc + runbot).
- ≤ 1 réponse marquée « Documenté » fausse sur cet échantillon (les erreurs doivent tomber en « À vérifier »).
- Réponse reçue sur Telegram en < 60 s pour une photo de QCM, < 3 min pour un PDF client.
- Coût moyen ≤ 0,05 USD par question et ≤ 0,20 USD par plan de configuration.

## 7. Implementation Phases

- **Phase 1 — Socle + question texte** : pgvector sur VPS + import v20, bot Telegram filtré, workflow question texte → recherche → réponse sourcée à 3 statuts ; duel Sonnet 5.5 vs meilleur Gemini sur les jeux de test existants (106 doc + 12 de référence), modèle gagnant figé. ✅ Terminée le 2026-10-27
- **Phase 2 — QCM photo** : photo → lecture de la question et des choix (vision) → réponse + explication + source ; corrigé vérifié de 30 questions ; mesure du taux de bonnes réponses.
- **Phase 3 — PDF client** : PDF → extraction des besoins → plan de configuration Odoo 20 étape par étape ; validé sur les scénarios clients existants (dont MTO).
- **Phase 4 — Robustesse** : format Telegram lisible (découpage messages longs), gestion d'erreurs visible, journal coûts/latence, workflows `[PROD]`.

## 8. Risks & Mitigations

- **Risque** : réponses v20 fausses pour des questions pensées v19 → **Mitigation** : l'assistant signale l'écart ; Odoo 19 en Hors scope activable.
- **Risque** : hallucination de menus/champs → **Mitigation** : statut obligatoire, second appel de contrôle (leçon de l'ancien projet), statut « À vérifier » par défaut si passage absent.
- **Risque** : bibliothèque v20 (export 18/10/2026) obsolète → **Mitigation** : contrôle du commit `docs_commit` vs branche 20.0 en Phase 1, rafraîchissement manuel si écart important.
- **Risque** : lecture d'une photo de QCM floue ou partielle → **Mitigation** : l'assistant renvoie la question lue avant de répondre ; demande une nouvelle photo si illisible.
- **Risque** : retomber dans l'excès d'infrastructure de l'ancien projet → **Mitigation** : un seul workflow par phase, pas de nouvelle brique sans besoin mesuré.
- **Risque** : accès au VPS insuffisant pour lancer un conteneur Postgres → **Mitigation** : vérifié en tâche 1 de la Phase 1 ; repli Supabase gratuit.
