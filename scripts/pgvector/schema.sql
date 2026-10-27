-- Schéma de la bibliothèque Odoo, repris de schema-tables-bibliotheque.ts (ancien projet).
-- Les enums Drizzle deviennent des colonnes text : le dump n'apporte que des données (COPY).
-- Les index (dont HNSW) sont créés après l'import par indexes.sql, plus rapide que pendant le COPY.

create extension if not exists vector;

create table if not exists knowledge_sources (
  id uuid primary key default gen_random_uuid(),
  kind text not null,
  title text not null,
  url text not null unique,
  url_fr text,
  odoo_version text not null,
  module text,
  category text,
  path text not null,
  revision text,
  docs_commit text,
  license text,
  reliability text not null,
  status text not null default 'pending',
  error text,
  ingested_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists knowledge_chunks (
  id uuid primary key default gen_random_uuid(),
  source_id uuid not null references knowledge_sources(id) on delete cascade,
  odoo_version text not null,
  module text,
  ordinal integer not null,
  breadcrumb text not null,
  url text not null,
  anchor text,
  anchor_verified boolean not null default false,
  content text not null,
  content_hash text not null,
  token_count integer,
  embedding vector(1536),
  embedding_model text,
  start_seconds integer,
  end_seconds integer,
  search_vector tsvector generated always as (to_tsvector('english', breadcrumb || ' ' || content)) stored,
  created_at timestamptz not null default now()
);
