"""
Seed all 72 Carnatic Melakarta ragas from Wikipedia's Melakarta page.
Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_ragas_carnatic_melakarta.py
"""

import os
import re
import ssl
import subprocess
import sys
import tempfile
import urllib.request
import json

# Python 3.14 on macOS often lacks bundled certs — bypass for public Wikipedia API
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE


def fetch_melakarta_wikitext() -> str:
    url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=parse&page=Melakarta&prop=wikitext&format=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "NadaAtlas/1.0"})
    with urllib.request.urlopen(req, context=_ssl_ctx) as r:
        return json.load(r)["parse"]["wikitext"]["*"]


def parse_svaraC(template: str) -> str:
    """Extract notes from {{svaraC|S|R1|G2|M1|P|D2|N3|S'}} → 'S R1 G2 M1 P D2 N3 S'''"""
    notes = re.findall(r"\|([^|{}]+)", template)
    return " ".join(n.strip() for n in notes if n.strip())


def parse_melakartas(wikitext: str) -> list[dict]:
    ragas = []

    # Match each table row: |NUMBER  ||''[[RagaName|DisplayName]]'' \n |{{svaraC|...}}
    row_pattern = re.compile(
        r"\|\s*(\d+)\s*\|\|''?\[\[([^\]|]+)(?:\|([^\]]+))?\]\]''?"
        r"\s*\n\|(\{\{svaraC[^}]+\}\})",
        re.MULTILINE,
    )

    for m in row_pattern.finditer(wikitext):
        number = int(m.group(1))
        page_name = m.group(2).strip()
        display_name = (m.group(3) or m.group(2)).strip()
        # Clean up diacritics styling
        display_name = re.sub(r"[''']", "", display_name).strip()
        page_name = re.sub(r"[''']", "", page_name).strip()
        scale_template = m.group(4)
        scale = parse_svaraC(scale_template)

        # For melakartas the scale is identical ascending and descending
        arohana = scale
        avarohana = " ".join(reversed(scale.split()))
        # Fix: S' should come first in avarohana then end with S
        notes = scale.split()
        avarohana = " ".join(reversed(notes))

        tradition = "carnatic"
        description = (
            f"The {number}{'st' if number==1 else 'nd' if number==2 else 'rd' if number==3 else 'th'} "
            f"Melakarta raga in Carnatic music. "
            f"{'Uses Shuddha Madhyam (M1).' if number <= 36 else 'Uses Prathi Madhyam (M2).'}"
        )

        wikipedia_slug = page_name.replace(" ", "_")

        ragas.append({
            "name": display_name,
            "name_native": None,
            "tradition": tradition,
            "melakarta_number": number,
            "arohana": arohana,
            "avarohana": avarohana,
            "description": description,
            "wikipedia_slug": wikipedia_slug,
        })

    return ragas


def escape_sql(val: str) -> str:
    return val.replace("'", "''")


def s(v):
    return f"'{escape_sql(v)}'" if v else "NULL"


def build_sql(ragas: list[dict]) -> str:
    lines = [
        "-- 72 Carnatic Melakarta ragas seeded from Wikipedia",
        "INSERT INTO ragas (",
        "  id, name, name_native, tradition,",
        "  hindustani_name, carnatic_name,",
        "  that, melakarta_number,",
        "  arohana, avarohana,",
        "  vadi, samvadi, pakad,",
        "  time_of_day, season, rasa,",
        "  description, wikipedia_slug,",
        "  created_at, updated_at",
        ") VALUES",
    ]

    values = []
    for r in ragas:
        row = (
            f"  (gen_random_uuid(), {s(r['name'])}, NULL, 'carnatic', "
            f"NULL, {s(r['name'])}, "
            f"NULL, {r['melakarta_number']}, "
            f"{s(r['arohana'])}, {s(r['avarohana'])}, "
            f"NULL, NULL, NULL, "
            f"NULL, NULL, NULL, "
            f"{s(r['description'])}, {s(r['wikipedia_slug'])}, "
            f"NOW(), NOW())"
        )
        values.append(row)

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (name) DO UPDATE SET")
    lines.append("  tradition        = EXCLUDED.tradition,")
    lines.append("  melakarta_number = EXCLUDED.melakarta_number,")
    lines.append("  arohana          = EXCLUDED.arohana,")
    lines.append("  avarohana        = EXCLUDED.avarohana,")
    lines.append("  description      = EXCLUDED.description,")
    lines.append("  wikipedia_slug   = EXCLUDED.wikipedia_slug,")
    lines.append("  updated_at       = NOW();")

    return "\n".join(lines)


def main():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    print("Fetching Melakarta page from Wikipedia...")
    wikitext = fetch_melakarta_wikitext()

    ragas = parse_melakartas(wikitext)
    print(f"Parsed {len(ragas)} Melakarta ragas")

    if len(ragas) < 60:
        print("WARNING: expected 72, got fewer. Showing sample:")
        for r in ragas[:5]:
            print(f"  [{r['melakarta_number']}] {r['name']} — {r['arohana']}")

    sql = build_sql(ragas)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    print(f"Seeding {len(ragas)} Melakarta ragas into DB...")
    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ {len(ragas)} Melakarta ragas seeded.")

    # Show sample
    print("\nSample:")
    for r in sorted(ragas, key=lambda x: x["melakarta_number"])[:5]:
        print(f"  [{r['melakarta_number']:2d}] {r['name']:<30} {r['arohana']}")


if __name__ == "__main__":
    main()
