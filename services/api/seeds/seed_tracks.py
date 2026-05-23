"""
Seed landmark tracks across world traditions.
Artist lookup by name; album lookup by title + artist.

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_tracks.py
"""

import os
import subprocess
import sys
import tempfile

# ─────────────────────────────────────────────────────────────────────────────
# Track data
# Keys: title, title_native, artist_name, album_title (optional),
#       musical_tradition, raga, tala, maqam, duration_seconds,
#       track_number, youtube_url, spotify_url
# ─────────────────────────────────────────────────────────────────────────────
TRACKS = [

    # ── Carnatic ──────────────────────────────────────────────────────────────
    {
        "title": "Vinathasuta",
        "artist_name": "M.S. Subbulakshmi",
        "musical_tradition": "Carnatic",
        "raga": "Hamsadhvani",
        "tala": "Adi",
        "duration_seconds": 480,
        "youtube_url": "https://www.youtube.com/watch?v=pPALHaYaFJA",
    },
    {
        "title": "Bhavayami Raghuramam",
        "artist_name": "M.S. Subbulakshmi",
        "musical_tradition": "Carnatic",
        "raga": "Yamuna Kalyani",
        "tala": "Adi",
        "duration_seconds": 420,
    },
    {
        "title": "Vaishnava Janato",
        "artist_name": "M.S. Subbulakshmi",
        "musical_tradition": "Carnatic",
        "duration_seconds": 300,
        "youtube_url": "https://www.youtube.com/watch?v=FtMV_DllYpY",
    },
    {
        "title": "Raga Bhairavi — Alaap, Jod, Jhala",
        "artist_name": "Ravi Shankar",
        "musical_tradition": "Carnatic",
        "raga": "Bhairavi",
        "duration_seconds": 1560,
    },
    {
        "title": "Raga Yaman — Alaap & Gat",
        "artist_name": "Ravi Shankar",
        "musical_tradition": "Hindustani Classical",
        "raga": "Yaman",
        "tala": "Teentaal",
        "duration_seconds": 2100,
        "youtube_url": "https://www.youtube.com/watch?v=oZ5F6S7dlWY",
    },
    {
        "title": "Raga Sindhi Bhairavi",
        "artist_name": "Ravi Shankar",
        "musical_tradition": "Hindustani Classical",
        "raga": "Sindhi Bhairavi",
        "duration_seconds": 900,
    },

    # ── Hindustani ────────────────────────────────────────────────────────────
    {
        "title": "Raga Darbari Kanada",
        "artist_name": "Shivkumar Sharma",
        "musical_tradition": "Hindustani Classical",
        "raga": "Darbari Kanada",
        "tala": "Teentaal",
        "duration_seconds": 2400,
    },
    {
        "title": "Raga Bhimpalasi",
        "artist_name": "Shivkumar Sharma",
        "musical_tradition": "Hindustani Classical",
        "raga": "Bhimpalasi",
        "tala": "Teentaal",
        "duration_seconds": 1800,
    },
    {
        "title": "Raga Puriya Dhanashri",
        "artist_name": "Ali Akbar Khan",
        "musical_tradition": "Hindustani Classical",
        "raga": "Puriya Dhanashri",
        "tala": "Teentaal",
        "duration_seconds": 3000,
    },
    {
        "title": "Raga Marwa",
        "artist_name": "Ali Akbar Khan",
        "musical_tradition": "Hindustani Classical",
        "raga": "Marwa",
        "duration_seconds": 2700,
    },
    {
        "title": "Mero Allah Meherbaan",
        "artist_name": "Pandit Jasraj",
        "musical_tradition": "Hindustani Classical",
        "raga": "Bhairavi",
        "tala": "Teentaal",
        "duration_seconds": 720,
    },

    # ── Qawwali ───────────────────────────────────────────────────────────────
    {
        "title": "Allah Hoo Allah Hoo",
        "title_native": "اللہ ہو اللہ ہو",
        "artist_name": "Nusrat Fateh Ali Khan",
        "musical_tradition": "Qawwali",
        "duration_seconds": 780,
        "youtube_url": "https://www.youtube.com/watch?v=wFkq0iBZqno",
    },
    {
        "title": "Tumhe Dillagi Bhool Jaani Padegi",
        "title_native": "تمہے دلگی بھول جانی پڑے گی",
        "artist_name": "Nusrat Fateh Ali Khan",
        "musical_tradition": "Qawwali",
        "duration_seconds": 660,
    },
    {
        "title": "Mustt Mustt",
        "artist_name": "Nusrat Fateh Ali Khan",
        "musical_tradition": "Qawwali",
        "duration_seconds": 510,
        "youtube_url": "https://www.youtube.com/watch?v=5UdZ1mZsKlc",
    },

    # ── Jazz ──────────────────────────────────────────────────────────────────
    {
        "title": "Take Five",
        "artist_name": "Dave Brubeck",
        "album_title": "Time Out",
        "musical_tradition": "Jazz",
        "duration_seconds": 324,
        "youtube_url": "https://www.youtube.com/watch?v=vmDDOFXSgAs",
    },
    {
        "title": "Blue Rondo à la Turk",
        "artist_name": "Dave Brubeck",
        "album_title": "Time Out",
        "musical_tradition": "Jazz",
        "duration_seconds": 366,
    },
    {
        "title": "Strange Meadow Lark",
        "artist_name": "Dave Brubeck",
        "album_title": "Time Out",
        "musical_tradition": "Jazz",
        "duration_seconds": 375,
    },
    {
        "title": "Mood Indigo",
        "artist_name": "Duke Ellington",
        "musical_tradition": "Jazz",
        "duration_seconds": 198,
        "youtube_url": "https://www.youtube.com/watch?v=sY-XhVJHFRw",
    },
    {
        "title": "It Don't Mean a Thing (If It Ain't Got That Swing)",
        "artist_name": "Duke Ellington",
        "musical_tradition": "Jazz",
        "duration_seconds": 216,
    },
    {
        "title": "So What",
        "artist_name": "Miles Davis",
        "musical_tradition": "Jazz",
        "duration_seconds": 561,
        "youtube_url": "https://www.youtube.com/watch?v=zqNTltOGh5c",
    },
    {
        "title": "Blue in Green",
        "artist_name": "Miles Davis",
        "musical_tradition": "Jazz",
        "duration_seconds": 337,
    },
    {
        "title": "All Blues",
        "artist_name": "Miles Davis",
        "musical_tradition": "Jazz",
        "duration_seconds": 694,
    },
    {
        "title": "Feeling Good",
        "artist_name": "Nina Simone",
        "musical_tradition": "Jazz",
        "duration_seconds": 186,
        "youtube_url": "https://www.youtube.com/watch?v=oHRNrgDIJfo",
    },
    {
        "title": "I Put a Spell on You",
        "artist_name": "Nina Simone",
        "musical_tradition": "Jazz",
        "duration_seconds": 216,
        "youtube_url": "https://www.youtube.com/watch?v=GXi91-4SjlQ",
    },
    {
        "title": "Sinnerman",
        "artist_name": "Nina Simone",
        "musical_tradition": "Jazz",
        "duration_seconds": 600,
        "youtube_url": "https://www.youtube.com/watch?v=O-SpFzsKPZc",
    },

    # ── Tango ─────────────────────────────────────────────────────────────────
    {
        "title": "Libertango",
        "artist_name": "Astor Piazzolla",
        "musical_tradition": "Argentine Tango",
        "duration_seconds": 196,
        "youtube_url": "https://www.youtube.com/watch?v=DFu0KVhCT9s",
    },
    {
        "title": "Adiós Nonino",
        "artist_name": "Astor Piazzolla",
        "musical_tradition": "Argentine Tango",
        "duration_seconds": 270,
        "youtube_url": "https://www.youtube.com/watch?v=9_7loz-HWUM",
    },
    {
        "title": "Oblivion",
        "artist_name": "Astor Piazzolla",
        "musical_tradition": "Argentine Tango",
        "duration_seconds": 210,
        "youtube_url": "https://www.youtube.com/watch?v=yAsgBnMpNa8",
    },

    # ── Flamenco ─────────────────────────────────────────────────────────────
    {
        "title": "Entre dos Aguas",
        "artist_name": "Paco de Lucía",
        "musical_tradition": "Flamenco",
        "duration_seconds": 288,
        "youtube_url": "https://www.youtube.com/watch?v=0HmFKkHvPgE",
    },
    {
        "title": "Solo Quiero Caminar",
        "artist_name": "Paco de Lucía",
        "musical_tradition": "Flamenco",
        "duration_seconds": 396,
    },
    {
        "title": "Río Ancho",
        "artist_name": "Paco de Lucía",
        "musical_tradition": "Flamenco",
        "duration_seconds": 330,
        "youtube_url": "https://www.youtube.com/watch?v=a7XGqB3gFI0",
    },

    # ── Afrobeat ─────────────────────────────────────────────────────────────
    {
        "title": "Zombie",
        "artist_name": "Fela Kuti",
        "musical_tradition": "Afrobeat",
        "duration_seconds": 720,
        "youtube_url": "https://www.youtube.com/watch?v=ala6LbcpWIo",
    },
    {
        "title": "Lady",
        "artist_name": "Fela Kuti",
        "musical_tradition": "Afrobeat",
        "duration_seconds": 660,
    },
    {
        "title": "Water No Get Enemy",
        "artist_name": "Fela Kuti",
        "musical_tradition": "Afrobeat",
        "duration_seconds": 900,
        "youtube_url": "https://www.youtube.com/watch?v=KkIBaLdkKOE",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SQL helpers
# ─────────────────────────────────────────────────────────────────────────────

def esc(v: str) -> str:
    return v.replace("'", "''")


def s(v) -> str:
    return f"'{esc(str(v))}'" if v is not None else "NULL"


def artist_subq(name: str) -> str:
    return f"(SELECT id FROM artists WHERE LOWER(name) = LOWER('{esc(name)}') AND deleted_at IS NULL LIMIT 1)"


def album_subq(title: str, artist_name: str) -> str:
    return (
        f"(SELECT al.id FROM albums al "
        f"JOIN artists a ON a.id = al.artist_id "
        f"WHERE LOWER(al.title) = LOWER('{esc(title)}') "
        f"AND LOWER(a.name) = LOWER('{esc(artist_name)}') "
        f"LIMIT 1)"
    )


def build_sql(tracks: list[dict]) -> str:
    stmts = ["-- NadaAtlas tracks seed"]

    for t in tracks:
        artist_id = artist_subq(t["artist_name"])
        album_id  = album_subq(t["album_title"], t["artist_name"]) if t.get("album_title") else "NULL"

        guard = (
            f"NOT EXISTS ("
            f"SELECT 1 FROM tracks "
            f"WHERE LOWER(title) = LOWER({s(t['title'])}) "
            f"AND artist_id = {artist_id} "
            f"AND deleted_at IS NULL"
            f")"
        )

        stmt = f"""INSERT INTO tracks (
  id, title, title_native, artist_id, album_id, musical_tradition,
  raga, tala, maqam, duration_seconds, track_number,
  youtube_url, spotify_url, created_at, updated_at
)
SELECT
  gen_random_uuid(),
  {s(t['title'])},
  {s(t.get('title_native'))},
  {artist_id},
  {album_id},
  {s(t.get('musical_tradition'))},
  {s(t.get('raga'))},
  {s(t.get('tala'))},
  {s(t.get('maqam'))},
  {t['duration_seconds'] if t.get('duration_seconds') else 'NULL'},
  {t['track_number'] if t.get('track_number') else 'NULL'},
  {s(t.get('youtube_url'))},
  {s(t.get('spotify_url'))},
  NOW(), NOW()
WHERE {guard}
  AND {artist_id} IS NOT NULL;"""
        stmts.append(stmt)

    return "\n\n".join(stmts)


def main():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    sql = build_sql(TRACKS)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    by_tradition: dict[str, int] = {}
    for t in TRACKS:
        trad = t.get("musical_tradition") or "Unknown"
        by_tradition[trad] = by_tradition.get(trad, 0) + 1

    print(f"Seeding {len(TRACKS)} tracks...")
    for trad, count in sorted(by_tradition.items()):
        print(f"  {trad}: {count}")

    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ Done — {len(TRACKS)} tracks attempted.")


if __name__ == "__main__":
    main()
