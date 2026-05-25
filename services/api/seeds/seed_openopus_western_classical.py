"""Seed / refresh Western Classical data from OpenOpus.

Usage:
    python seeds/seed_openopus_western_classical.py [--dry-run] [--works-limit N]

What it does
------------
1. Fetches all 220 composers from https://api.openopus.org/composer/list/epoch/all.json
   (gives: openopus id, complete_name, birth, death, epoch, portrait URL)
2. Fetches the full work dump from https://api.openopus.org/work/dump.json
   (works are nested under each composer object by complete_name)
3. For each OpenOpus composer:
   - If already in our DB (matched by complete_name, case-insensitive):
       * Updates openopus_id, image_url (if blank), born/died, era
   - If NOT in our DB:
       * Inserts new composer under the Western Classical tradition
4. For each work of each composer now in our DB:
   - Inserts the composition if it doesn't already exist (matched by title + composer_id)
   - Maps OpenOpus genre → our composition_type
   - Records openopus_id (composite key "composer_openopus_id:title_slug") for dedup

Licence: OpenOpus data is released under CC0. No API key required.
"""
from __future__ import annotations

import argparse
import re
import sys
from typing import Optional
import json
import uuid

import requests
import psycopg2
import psycopg2.extras
from psycopg2.extras import execute_values

# ── Config ──────────────────────────────────────────────────────────────────
DB_URL = "postgresql://postgres:uzGvKmjbUjIrpeBbTzfQhnLzheFbashG@ballast.proxy.rlwy.net:10439/railway"
OPENOPUS_COMPOSERS_URL = "https://api.openopus.org/composer/list/epoch/all.json"
OPENOPUS_DUMP_URL      = "https://api.openopus.org/work/dump.json"
WESTERN_CLASSICAL_NAME = "Western Classical"

# OpenOpus epoch → our era label
EPOCH_MAP = {
    "Medieval":       "Medieval",
    "Renaissance":    "Renaissance",
    "Baroque":        "Baroque",
    "Classical":      "Classical",
    "Early Romantic": "Romantic",
    "Romantic":       "Romantic",
    "Late Romantic":  "Romantic",
    "20th Century":   "20th Century",
    "Post-War":       "20th Century",
    "21st Century":   "Contemporary",
}

# OpenOpus genre → our composition_type
GENRE_MAP = {
    "Orchestral": "orchestral",
    "Chamber":    "chamber",
    "Keyboard":   "keyboard",
    "Stage":      "stage",
    "Vocal":      "vocal",
    "Popular":    "other",
    "Recommended": "other",
}


def fetch_json(url: str) -> dict:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:200]


def parse_year_as_date(date_str: Optional[str]) -> Optional[str]:
    """Return a DB-friendly date string ('YYYY-01-01') from an OpenOpus date like '1837-01-01'."""
    if not date_str:
        return None
    try:
        year = int(date_str[:4])
        return f"{year:04d}-01-01"
    except (ValueError, TypeError):
        return None


def main(dry_run: bool = False, works_limit: int = 0) -> None:
    print("Fetching OpenOpus composer list …")
    raw_composers = fetch_json(OPENOPUS_COMPOSERS_URL).get("composers", [])
    print(f"  → {len(raw_composers)} composers received")

    print("Fetching OpenOpus work dump …")
    dump_data = fetch_json(OPENOPUS_DUMP_URL)
    # Works are nested inside each composer in the dump
    dump_composers = dump_data.get("composers", [])
    # Build a map: complete_name (lower) → list of works
    works_by_name: dict[str, list[dict]] = {}
    for dc in dump_composers:
        key = dc.get("complete_name", "").strip().lower()
        works_by_name[key] = dc.get("works", [])
    print(f"  → {len(dump_composers)} composer entries with works in dump")

    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # ── Look up Western Classical tradition id ───────────────────────────────
    cur.execute(
        "SELECT id FROM musical_traditions WHERE name = %s LIMIT 1",
        (WESTERN_CLASSICAL_NAME,),
    )
    row = cur.fetchone()
    if not row:
        print(f"ERROR: Could not find tradition '{WESTERN_CLASSICAL_NAME}' in DB.")
        sys.exit(1)
    tradition_id: str = str(row["id"])
    print(f"  → Western Classical tradition id: {tradition_id}")

    # ── Fetch existing composers from our DB ─────────────────────────────────
    cur.execute("SELECT id, name, openopus_id, image_url FROM composers")
    existing: dict[str, dict] = {
        r["name"].strip().lower(): dict(r) for r in cur.fetchall()
    }
    print(f"  → {len(existing)} composers already in our DB")

    composers_updated = 0
    composers_inserted = 0

    # Accumulate all work rows for a single bulk insert at the end
    all_work_rows: list[tuple] = []

    # ── Pass 1: process composers ────────────────────────────────────────────
    for oc in raw_composers:
        full_name  = oc.get("complete_name", "").strip()
        oo_id      = str(oc.get("id", ""))
        epoch      = oc.get("epoch", "")
        portrait   = oc.get("portrait") or None
        birth_year = parse_year_as_date(oc.get("birth"))
        death_year = parse_year_as_date(oc.get("death"))
        era        = EPOCH_MAP.get(epoch, epoch)
        name_key   = full_name.lower()

        if name_key in existing:
            # ── UPDATE existing composer ─────────────────────────────────────
            db_row = existing[name_key]
            db_id  = str(db_row["id"])

            # Only fill in image if we don't already have one
            new_image = portrait if not db_row.get("image_url") and portrait else None

            if not dry_run:
                cur.execute(
                    """
                    UPDATE composers SET
                        openopus_id = COALESCE(openopus_id, %s),
                        image_url   = COALESCE(image_url, %s),
                        born        = COALESCE(born, %s),
                        died        = COALESCE(died, %s),
                        era         = COALESCE(era, %s),
                        updated_at  = now()
                    WHERE id = %s
                    """,
                    (oo_id, new_image, birth_year, death_year, era, db_id),
                )
            composers_updated += 1
            composer_db_id = db_id

        else:
            # ── INSERT new composer ──────────────────────────────────────────
            new_id = str(uuid.uuid4())
            if not dry_run:
                cur.execute(
                    """
                    INSERT INTO composers
                        (id, name, tradition_id, era, born, died, image_url, openopus_id,
                         is_verified, created_at, updated_at)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, true, now(), now())
                    ON CONFLICT DO NOTHING
                    """,
                    (new_id, full_name, tradition_id, era,
                     birth_year, death_year, portrait, oo_id),
                )
            composers_inserted += 1
            composer_db_id = new_id
            # Add to existing map so works can reference it
            existing[name_key] = {"id": new_id, "openopus_id": oo_id}

        # ── Collect works for this composer ──────────────────────────────────
        works = works_by_name.get(name_key, [])
        if works_limit:
            works = works[:works_limit]

        seen_oo_ids: set[str] = set()
        for work in works:
            title = (work.get("title") or "").strip()
            if not title:
                continue

            subtitle  = (work.get("subtitle") or "").strip() or None
            comp_type = GENRE_MAP.get(work.get("genre", ""), "other")
            work_oo_id = f"{oo_id}:{slugify(title)}"[:128]

            if work_oo_id in seen_oo_ids:
                continue  # deduplicate within same composer
            seen_oo_ids.add(work_oo_id)

            all_work_rows.append((
                str(uuid.uuid4()),   # id
                title,               # title
                subtitle,            # description
                composer_db_id,      # composer_id
                tradition_id,        # tradition_id
                comp_type,           # composition_type
                work_oo_id,          # openopus_id
            ))

    print(f"  → {len(all_work_rows)} work rows collected; bulk inserting …")

    # ── Pass 2: bulk-insert all works ────────────────────────────────────────
    works_inserted = 0
    works_skipped  = 0

    if not dry_run and all_work_rows:
        CHUNK = 500
        for i in range(0, len(all_work_rows), CHUNK):
            chunk = all_work_rows[i : i + CHUNK]
            execute_values(
                cur,
                """
                INSERT INTO compositions
                    (id, title, description, composer_id, tradition_id,
                     composition_type, openopus_id, created_at, updated_at)
                VALUES %s
                ON CONFLICT (openopus_id) DO NOTHING
                """,
                chunk,
                template="(%s, %s, %s, %s, %s, %s, %s, now(), now())",
                page_size=CHUNK,
            )
            works_inserted += cur.rowcount
            print(f"    chunk {i // CHUNK + 1}: inserted {cur.rowcount}")
        works_skipped = len(all_work_rows) - works_inserted
    elif dry_run:
        works_inserted = len(all_work_rows)

    if not dry_run:
        conn.commit()
        print("\n✅ Committed.")
    else:
        conn.rollback()
        print("\n🔍 Dry-run — no changes written.")

    print(
        f"\nSummary:\n"
        f"  Composers updated : {composers_updated}\n"
        f"  Composers inserted: {composers_inserted}\n"
        f"  Works inserted    : {works_inserted}\n"
        f"  Works skipped (dup): {works_skipped}"
    )

    cur.close()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed OpenOpus Western Classical data")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and compute but do not write to DB")
    parser.add_argument("--works-limit", type=int, default=0, help="Limit works per composer (0 = all)")
    args = parser.parse_args()
    main(dry_run=args.dry_run, works_limit=args.works_limit)
