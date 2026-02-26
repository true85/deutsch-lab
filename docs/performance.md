# Performance Tuning

## Indexing
- Keep `level`, `theme`, `next_review` indexes on main tables.
- Add composite indexes if query patterns become stable.
- For pgvector:
  - Use `ivfflat` for large static datasets.
  - Use `hnsw` if frequent inserts/updates.
  - Run `ANALYZE` after bulk inserts.

## Query Patterns
- Prefer filtered queries before vector search.
- Avoid `SELECT *` in production; fetch only needed columns.
- Use `range(offset, limit)` for pagination.

## API
- Cache common recommendation lists per user (short TTL).
- Add request-level rate limiting (already enabled).
- Log slow queries for follow-up optimization.

## DB Maintenance
- Periodic `VACUUM` and `ANALYZE`.
- Monitor table bloat and index hit rate.
