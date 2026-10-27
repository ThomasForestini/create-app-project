# Postgres + pgvector sur le VPS — bibliothèque Odoo 20

> Installé le 26/10/2026 (Phase 1, tâche 1).

## Ce qui tourne

- Conteneur `pgvector` (image `pgvector/pgvector:pg17`), dans `/root/pgvector/` sur le VPS (`ssh hostinger-vps`).
- Rattaché au réseau Docker de n8n (`n8n-ijcp_default`), **aucun port publié** : n8n y accède par l'hôte `pgvector:5432`, rien d'autre.
- Base `odoo_knowledge`, utilisateur `odoo`. Mot de passe : `.env` local (`PGVECTOR_PASSWORD`, gitignoré) et `/root/pgvector/.env` sur le VPS (droits 600).
- Volume Docker `pgvector_pgvector-data` (survit au redémarrage du conteneur).

Fichiers versionnés : [`scripts/pgvector/`](../scripts/pgvector/) (`docker-compose.yml`, `schema.sql`, `indexes.sql`).

## Procédure (rejouable)

Depuis la racine du projet, sur le Mac :

```bash
ssh hostinger-vps 'mkdir -p /root/pgvector'
scp scripts/pgvector/{docker-compose.yml,schema.sql,indexes.sql} hostinger-vps:/root/pgvector/
grep '^PGVECTOR_\(DB\|USER\|PASSWORD\)=' .env | ssh hostinger-vps 'umask 077; cat > /root/pgvector/.env'
scp ~/Desktop/a-reprendre-odoo/bibliotheque/knowledge-20.0.sql.gz hostinger-vps:/root/pgvector/
```

Puis sur le VPS (`ssh hostinger-vps`) :

```bash
cd /root/pgvector && docker compose up -d
set -a && . ./.env && set +a
P="docker exec -i pgvector psql -v ON_ERROR_STOP=1 -q -U $PGVECTOR_USER -d $PGVECTOR_DB"
$P < schema.sql
gzip -dc knowledge-20.0.sql.gz | $P   # ~8 s ; le dump vide d'abord la v20, donc réimport sans doublon
$P < indexes.sql                      # ~8 s, dont l'index HNSW
```

Le dump ne contient que des données (`COPY`) : le schéma vient de `schema-tables-bibliotheque.ts` de l'ancien projet, traduit dans `schema.sql` (enums remplacés par `text`). Il se termine par un contrôle qui échoue si un passage n'a pas de vecteur.

## Vérifications (26/10/2026)

| Contrôle | Résultat |
|----------|----------|
| Passages v20 | 10 355 au total : documentation **8 963**, structure du logiciel 1 102, vidéos 290 (1 315 sources) |
| Vecteurs | 1 536 dimensions, tous `gemini-embedding-2` |
| Recherche par similarité (vecteur littéral, top 10) | **3,9 ms**, via l'index HNSW `knowledge_chunks_embedding_idx` |
| Pertinence | Vecteur d'un passage de `finance/accounting/bank` → voisins : `bank.html#create-a-bank-account`, `get_started/journals.html` |
| Port public | `nc -z 187.124.35.144 5432` depuis le Mac → échec (exit 1) ; aucune écoute 5432 sur l'hôte |
| Accès depuis n8n | `nc -z pgvector 5432` dans le conteneur n8n → OK |

Note pour la tâche 3 : la recherche doit filtrer `kind` si on ne veut que la documentation officielle (`odoo_documentation`) ; sans filtre elle remonte aussi les passages structure et vidéos.

## Fraîcheur de la bibliothèque

Chaque source garde `revision`, l'empreinte git du fichier `.rst` au moment de l'import (commit `cdcbebe`, bibliothèque construite le 18/10/2026). On la compare au fichier actuel de la branche `20.0` de `github.com/odoo/documentation` (head `8c75237`, 26/10/2026).

**Échantillon de 10 pages** (9 tirées au hasard + `finance/accounting/bank`) : 10/10 identiques, chaque page en ligne répond HTTP 200 avec le même titre.

| Page | Fichier | Page en ligne |
|------|---------|---------------|
| point_of_sale/payment_methods | identique | 200 |
| crm/track_leads | identique | 200 |
| payroll_localizations/hong_kong | identique | 200 |
| inventory_and_mrp/manufacturing | identique | 200 |
| employees/training_attendances | identique | 200 |
| developer/howtos/standalone_owl_application | identique | 200 |
| phone/axivox/dial_plan_basics | identique | 200 |
| website/web_design/elements | identique | 200 |
| calendar/outlook | identique | 200 |
| finance/accounting/bank | identique | 200 |

**Sur l'ensemble des 1 126 pages de documentation** : 1 069 identiques (95 %), **57 modifiées** depuis l'import, 0 supprimée ; **46 pages** `.rst` existent en ligne sans être dans la bibliothèque. Les modifications touchent surtout inventaire / achats / réapprovisionnement, point de vente, tableur, IA et localisations fiscales.

Conséquence : écart faible mais réel en 8 jours. C'est ce que couvre la relecture en direct des pages citées (tâche 4). Une réindexation périodique reste à prévoir (hors Phase 1).

Commande de mesure (Mac, `gh` connecté) — utiliser un autre nom que `path` dans les boucles zsh, `path` y est lié à `$PATH` :

```bash
gh api "repos/odoo/documentation/git/trees/20.0?recursive=1" \
  --jq '.tree[] | select(.path|endswith(".rst")) | .path + "|" + .sha' > tree.txt
# puis comparer avec : select path, revision from knowledge_sources where kind='odoo_documentation'
```
