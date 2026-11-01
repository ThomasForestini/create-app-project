-- Journal des réponses du bot : une ligne par message traité (question, photo ou PDF), y compris en cas d'erreur.
-- Écrit par [DEV]/[PROD] telegram-assistant (nœud « Write journal »). Rejouable sans effet si la table existe.
create table if not exists journal (
  id bigserial primary key,
  ts timestamptz not null default now(),
  type text not null check (type in ('texte', 'qcm', 'plan')),
  duree_ms integer,
  cout_usd numeric(10, 5),
  statut text not null check (statut in ('ok', 'erreur')),
  erreur text,
  execution_id text
);

create index if not exists journal_ts_idx on journal (ts);
