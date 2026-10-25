# Brainstorm : Assistant Odoo sur Telegram (analyse de PDF client + révision certification)

## Idée en 1 phrase
Un assistant personnel sur Telegram, propulsé par n8n, à qui j'envoie soit un PDF client (il me dit précisément quoi configurer dans Odoo et comment), soit la photo d'un QCM de certification Odoo (il me donne la bonne réponse avec une brève explication sourcée, pour que j'apprenne).

## Besoin clarifié
- **Pour qui** : moi uniquement (usage personnel, pas d'authentification multi-utilisateurs).
- **Pour quoi** :
  - *Analyse de PDF client* : bien comprendre la demande du client et sortir les étapes de configuration Odoo dans le détail (menus, champs, valeurs), en anglais comme dans l'interface.
  - *Révision de la certification Odoo* : j'ai un pool de questions à choix multiples (exemple : `Odoo 19 certification.pdf`, une soixantaine de questions sur Sales, CRM, Accounting, Inventory, MRP, Studio…). Pour chaque photo, l'assistant donne la bonne réponse + une brève explication + la source, pour que je passe ensuite la vraie certification **seul, sans l'agent**.
- **Exigence n°1 : la précision.** Une réponse doit être juste et sourcée ; en cas de doute, l'assistant le dit (« À vérifier ») au lieu d'inventer.
- **Contexte** : projet from-scratch, mais **reprise d'un projet précédent** (« AgentIA-Odoo », Next.js + pgvector + Gemini) dont l'essentiel est sauvegardé dans `~/Desktop/a-reprendre-odoo/`.

## Contraintes connues
- Versions Odoo : **20 en priorité** (la plus récente, décision utilisateur). La 19 (version du pool de questions actuel) viendra éventuellement plus tard.
- Pas d'instance Odoo disponible. Pour vérifier une réponse « À vérifier » à la main : **runbot.odoo.com** (bases de test gratuites par version, Enterprise inclus, `admin`/`admin`).
- Instance n8n existante (self-hosted Hostinger), MCP n8n connecté en mode API.
- Budget : non fixé ; ordre de grandeur mesuré sur l'ancien projet ≈ 0,02 USD par question et ≈ 0,09 USD par plan de configuration, négligeable à usage perso.

## Matériel réutilisable (`~/Desktop/a-reprendre-odoo/`)
- `bibliotheque/knowledge-20.0.sql.gz` : doc officielle Odoo 20 indexée (1 126 pages, 8 963 passages, vecteurs `gemini-embedding-2` 1 536 dim). Odoo 19 non conservé (réindexation ≈ 0,15 USD depuis `odoo/documentation`).
- `consignes-ia/` : consignes de réponse sourcée (11 règles), schémas JSON, prompts « consultant ».
- `glossaire/` : libellés Odoo FR → EN (la doc est en anglais).
- `jeux-de-test/` : 106 questions doc + 40 pratiques + 12 de référence avec grille, scénarios clients (PDF, docx, transcription).
- `LISEZMOI.md` : leçons apprises (sous-questions, diversité des passages, 3 statuts, second appel de contrôle).

## Alternatives explorées
- **Interface web (Next.js)** : écartée pour la v1. C'est ce qui a alourdi l'ancien projet ; Telegram suffit pour un usage perso, depuis le téléphone.
- **Modèle seul, sans base documentaire** : écarté. Impossible de garantir la précision sur des menus Odoo qui changent d'une version à l'autre ; il faut une recherche dans la doc officielle de la bonne version.
- **Utiliser les réponses en vert du PDF comme corrigé** : écarté. Ce sont les réponses d'un candidat à 78 % (≈ 1 sur 5 fausse, beaucoup non marquées). Le PDF sert de pool de questions et, une fois les réponses vérifiées, de jeu de test.
- **Changer de modèle d'embedding** : écarté pour l'instant, car il faudrait revectoriser ; garder `gemini-embedding-2` permet de réutiliser la bibliothèque Odoo 20 telle quelle.

## Direction recommandée
- **n8n + Telegram** : un workflow qui reçoit un message, aiguille selon le type (photo de QCM / PDF / question texte), cherche dans la doc officielle indexée, puis répond avec statut (*Documenté / À vérifier / Non couvert*) et lien source.
- **Recherche** : `gemini-embedding-2` + base vectorielle (pgvector) rechargée depuis l'export ; patterns de l'ancien projet (1 à 5 sous-questions, 8 à 12 passages diversifiés, glossaire FR→EN).
- **Réponse** : modèle haut de gamme (pas « flash »). Choix par **duel mesuré** sur les jeux de test existants : Claude Sonnet 5.5 vs meilleur Gemini du moment ; pari de départ Claude Sonnet 5.5.
- **Démarrer petit** : une seule version, **Odoo 20** (bibliothèque déjà indexée, rechargeable sans coût), le cas QCM d'abord (le plus simple à mesurer), puis le PDF client. Odoo 19 éventuellement plus tard.
- **Attention** : le pool `Odoo 19 certification.pdf` porte sur la v19. Certaines réponses peuvent différer en v20 (menus, libellés, fonctionnalités). L'assistant doit le signaler quand la doc v20 contredit une question pensée pour la v19.

## Hypothèses encore à valider
- [ ] Où héberger la base vectorielle (Postgres sur le VPS n8n, Supabase gratuit, autre) ? → `/architect`
- [ ] Le meilleur modèle de réponse en précision (duel sur les jeux de test) → première phase
- [ ] La bibliothèque Odoo 20 (export du 18/10/2026) est-elle encore à jour, ou faut-il la rafraîchir depuis `odoo/documentation` branche 20.0 ?
- [ ] Existe-t-il des questions types de certification v20 (le pool actuel est v19) ?
- [ ] Format de réponse lisible sur Telegram (longueur, liens, statut de confiance)
- [ ] Corrigé vérifié d'un échantillon du PDF de certification (via doc + runbot) pour mesurer le taux de bonnes réponses
- [ ] Ordre de priorité entre le volet QCM et le volet PDF client

## Inspirations
Exploration du dossier `~/Desktop/a-reprendre-odoo/` (pas de recherche web) : scores de référence (99 % de sections retrouvées sur 106 questions), bilans V1→V3 du plan de configuration MTO, et cause principale de l'échec de l'ancien projet (trop d'infrastructure avant d'avoir validé le cœur du produit).

## Prochaine étape suggérée
`/architect docs/brainstorms/2026-10-25-assistant-odoo-telegram.md` (projet neuf, pas encore de PRD).
