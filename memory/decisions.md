# Décisions d'architecture du projet

> Ce fichier a deux usages :
>
> 1. **ADR fondateurs/architecturaux numérotés** (écrits par `/architect` Étape 6.6 ADR-001 + `/evoluer` Étape 5f si choix significatif). Format strict, idempotent (ne réécrit pas un ADR existant).
> 2. **Harvest libre** (écrit par `/close` lors du harvest learnings, zone `<!-- close:decisions -->` ci-dessous, format bullet libre).
>
> Les deux coexistent : ADR numérotés en tête (rigueur), bullets en bas (rapidité).

## ADR — Architecture Decision Records

> Format : `ADR-NNN — {Titre court}` puis bloc `Status / Date / Context / Decision / Consequences`. Status ∈ {Accepted, Superseded, Deprecated}. Numérotation strictement incrémentale, jamais réutilisée.

<!-- ADR-NNN entries appended here by /architect (Étape 6.6) and /evoluer (Étape 5f) -->

### ADR-001 — Stack initiale : n8n + Telegram + pgvector VPS + Sonnet 5.5

- **Status** : Accepted
- **Date** : 2026-10-25
- **Context** : Brief `docs/brainstorms/2026-10-25-assistant-odoo-telegram.md`, `project_type: automation`, usage perso. Reprise de l'ancien projet AgentIA-Odoo (Next.js) dont l'échec venait d'un excès d'infrastructure avant validation du cœur.
- **Decision** : n8n self-hosted (Hostinger) + Telegram comme seule interface. Postgres + pgvector en conteneur sur le même VPS (pas de pause ni de quota, contrairement à Supabase gratuit), bibliothèque Odoo 20 réutilisée telle quelle avec `gemini-embedding-2`. Rédaction par Claude Sonnet 5.5, à confirmer par un duel mesuré contre Gemini en Phase 1.
- **Consequences** : Verrouille `gemini-embedding-2` (changer = revectoriser). Débloque un MVP sans UI web. Le VPS devient point unique (n8n + BDD) — repli Supabase si l'accès Docker manque.

---

## Décisions (harvest libre)

<!-- close:decisions -->
{Vide au démarrage. Premier exemple après quelques sessions :

- **2026-05-15** — BDD : Supabase au lieu de Neon. Rationale : Auth + BDD + Realtime en un, RLS native, gratuit jusqu'à 500 MB suffisant pour le MVP.
- **2026-05-22** — Hosting : Vercel au lieu de Netlify. Rationale : meilleure intégration Next.js, déploiement preview par PR, gratuit pour projet perso.
- **2026-06-01** — Email transactionnel : Resend. Rationale : DX moderne (React Email), 3000 emails/mois gratuit, dépendance minimale.}
<!-- /close:decisions -->
