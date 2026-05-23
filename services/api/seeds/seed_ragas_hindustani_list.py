"""
Seed Hindustani raga names from Wikipedia's list page.
Inserts ~1100 ragas with tradition='hindustani' and name only.
Existing records with richer data are preserved (ON CONFLICT DO NOTHING).

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_ragas_hindustani_list.py
"""

import json
import os
import re
import ssl
import subprocess
import sys
import tempfile
import urllib.request

# Python 3.14 on macOS often lacks bundled certs
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE


THAAT_KEYWORDS = [
    "Kalyan", "Bilawal", "Khamaj", "Bhairav", "Poorvi",
    "Marwa", "Marva", "Kafi", "Asavari", "Bhairavi", "Todi",
]


def fetch_wikitext(page: str) -> str:
    url = (
        "https://en.wikipedia.org/w/api.php"
        f"?action=parse&page={urllib.request.quote(page)}&prop=wikitext&format=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "NadaAtlas/1.0"})
    with urllib.request.urlopen(req, context=_ssl_ctx) as r:
        return json.load(r)["parse"]["wikitext"]["*"]


def extract_thaat(raw: str) -> str | None:
    """Pull thaat from strings like '(Marwa Thaat)' or '(Kalyan aang)'."""
    for kw in THAAT_KEYWORDS:
        if re.search(rf"\b{kw}\b", raw, re.IGNORECASE):
            # Normalize Marva → Marwa
            return "Marwa" if kw.lower() == "marva" else kw
    return None


def clean_name(raw: str) -> str | None:
    """
    Clean a raw list item line into a raga name.
    Returns None if the line should be skipped.
    """
    s = raw.strip()

    # Remove leading * bullet
    s = re.sub(r"^\*+\s*", "", s)

    # Remove <ref ...> tags
    s = re.sub(r"<ref[^>]*/?>.*?</ref>", "", s, flags=re.DOTALL)
    s = re.sub(r"<ref[^>]*/?>", "", s)

    # Unwrap [[Link|Display]] → Display; [[Link]] → Link
    s = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)

    # Remove parenthetical suffixes: (raga), (raagini), (Marwa Thaat), (raga's son) etc.
    s = re.sub(r"\s*\([^)]*\)", "", s)

    # Remove trailing qualifiers after "/" (e.g. "Bageshri / Bageshree" → "Bageshri")
    s = s.split("/")[0]

    # Remove trailing wiki formatting artifacts
    s = re.sub(r"[*'\[\]{}|]", "", s)
    s = s.strip()

    # Skip empty, very short, or section headers
    if not s or len(s) < 2:
        return None
    # Skip if it looks like a section header (ALL CAPS single word)
    if s.isupper() and len(s) <= 3:
        return None

    return s


def parse_ragas(wikitext: str) -> list[dict]:
    ragas = []
    seen_names: set[str] = set()

    for line in wikitext.splitlines():
        stripped = line.strip()
        if not stripped.startswith("*"):
            continue

        raw = stripped
        name = clean_name(raw)
        if not name:
            continue

        # De-duplicate
        key = name.lower()
        if key in seen_names:
            continue
        seen_names.add(key)

        # Try to extract thaat from the original raw line
        that = extract_thaat(raw)

        ragas.append({
            "name": name,
            "that": that,
        })

    return ragas


def escape_sql(v: str) -> str:
    return v.replace("'", "''")


def s(v: str | None) -> str:
    return f"'{escape_sql(v)}'" if v else "NULL"


def build_sql(ragas: list[dict]) -> str:
    lines = [
        "-- Hindustani raga names from Wikipedia list",
        "-- ON CONFLICT DO NOTHING preserves existing richer records",
        "INSERT INTO ragas (",
        "  id, name, tradition, that,",
        "  created_at, updated_at",
        ") VALUES",
    ]

    values = []
    for r in ragas:
        row = (
            f"  (gen_random_uuid(), {s(r['name'])}, 'hindustani', {s(r['that'])}, "
            f"NOW(), NOW())"
        )
        values.append(row)

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (name) DO NOTHING;")
    return "\n".join(lines)


def main():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    print("Fetching Hindustani raga list from Wikipedia...")
    wikitext = fetch_wikitext("List_of_ragas_in_Hindustani_classical_music")

    ragas = parse_ragas(wikitext)
    print(f"Parsed {len(ragas)} raga names")

    # Stats
    with_thaat = [r for r in ragas if r["that"]]
    print(f"  → {len(with_thaat)} have thaat info, {len(ragas)-len(with_thaat)} name-only")

    # Sample
    print("\nSample (first 10):")
    for r in ragas[:10]:
        thaat_str = f"  [{r['that']}]" if r["that"] else ""
        print(f"  {r['name']}{thaat_str}")

    sql = build_sql(ragas)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    print(f"\nSeeding {len(ragas)} ragas (ON CONFLICT DO NOTHING)...")
    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ Done. {len(ragas)} ragas processed (existing rich records untouched).")


if __name__ == "__main__":
    main()
