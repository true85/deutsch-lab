# Backup & Restore

## Supabase Backups
- Use Supabase Dashboard → Database → Backups.
- Enable daily backups for production.
- Verify at least one full backup before major schema changes.

## SQL Dump (Manual)
- Export schema + data from Supabase SQL Editor:
  - Use `pg_dump` via Supabase connection string (server-side).
  - Store the dump in a secure location.

## Restore Workflow
1) Create a new Supabase project.
2) Apply schema migration SQL.
3) Restore data from dump.
4) Rebuild indexes (pgvector, ivfflat/hnsw).
5) Verify API endpoints (`/health`, `/supabase-health`).

## Safety Notes
- Never store secrets in dumps.
- Rotate keys after restoration.
