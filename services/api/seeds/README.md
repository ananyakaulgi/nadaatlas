# Seeds

Reference data seeds for MusiCompass. Run these once against a fresh database after migrations.

## Order

| File | Description |
|------|-------------|
| `001_instruments_curated.sql` | ~80 hand-curated world music instruments with full metadata |
| `002_instruments_orchestral.sql` | Western orchestral, chamber, and folk instruments with proper descriptions |
| `ingest_instruments_wikidata.py` | Fetches all ~760 musical instruments from Wikidata and upserts them |

## Running SQL seeds

```bash
# Via docker
docker exec -i <postgres-container> psql -U nadaatlas -d nadaatlas < seeds/001_instruments_curated.sql
docker exec -i <postgres-container> psql -U nadaatlas -d nadaatlas < seeds/002_instruments_orchestral.sql
```

## Running the Wikidata ingestion script

```bash
pip install requests
python3 seeds/ingest_instruments_wikidata.py
```

Requires the postgres docker container to be running. Fetches ~560 unique instruments from
the Wikidata SPARQL endpoint and upserts them (safe to re-run).
