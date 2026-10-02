`uv run python -m app.main`

## Database migrations (Alembic)

Files Alembic needs (everything else is generated):

| File | Purpose |
| --- | --- |
| `alembic.ini` | Points Alembic at the `migrations/` folder. No DB URL here. |
| `migrations/env.py` | Connects using `settings.database_url` and diffs against `Base.metadata`. |
| `migrations/script.py.mako` | Template for new migration files. Don't edit. |
| `migrations/versions/` | The migrations themselves. |

### Setup (already done)

1. `uv add alembic asyncpg "sqlalchemy[asyncio]"`
2. `uv run alembic init -t async migrations`, then trim `alembic.ini` and `env.py` down to what's committed.
3. `.env` has `DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/shortener`.

### Everyday workflow

1. Start Postgres: `docker compose up -d db`
2. Change a model in `app/models.py`.
3. Generate a migration: `uv run alembic revision --autogenerate -m "describe change"`
4. Open the new file in `migrations/versions/` and check it. Autogenerate misses things like renames (it sees a drop plus an add).
5. Apply it: `uv run alembic upgrade head`
6. Undo the last one if needed: `uv run alembic downgrade -1`

### Adding a new model

Import it somewhere `migrations/env.py` already loads, or autogenerate won't see it. The existing `import app.models` covers anything defined in `app/models.py`. If you add another models file, import it in `env.py` too.

### Limitations

`migrations/env.py` only supports online mode, so `alembic upgrade head --sql` (offline SQL output) is not supported. It will connect to the DB and apply the migration for real.

### Useful commands

- `uv run alembic current`: which revision the DB is on
- `uv run alembic history`: list of migrations
