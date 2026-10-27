-- Index de la bibliothèque, à lancer après l'import du dump.
create unique index if not exists knowledge_sources_kind_version_path_idx on knowledge_sources (kind, odoo_version, path);
create index if not exists knowledge_sources_odoo_version_idx on knowledge_sources (odoo_version);
create index if not exists knowledge_chunks_source_id_idx on knowledge_chunks (source_id);
create index if not exists knowledge_chunks_version_module_idx on knowledge_chunks (odoo_version, module);
create index if not exists knowledge_chunks_embedding_idx on knowledge_chunks using hnsw (embedding vector_cosine_ops);
create index if not exists knowledge_chunks_search_idx on knowledge_chunks using gin (search_vector);
analyze knowledge_sources;
analyze knowledge_chunks;
-- Parcours itératif de l'index HNSW (pgvector 0.8) : la recherche filtrée (kind, version) garde assez de candidats.
alter database odoo_knowledge set hnsw.iterative_scan = relaxed_order;
alter database odoo_knowledge set hnsw.ef_search = 100;
