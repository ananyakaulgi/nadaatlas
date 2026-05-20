"""
Fetch ALL musical instruments from Wikidata (P31=Q34379) and seed into MusiCompass DB.
Writes SQL to /tmp/instruments_wikidata.sql then pipes it through docker to postgres.
"""
import requests
import json
import time
import re
import subprocess
import sys

SPARQL = "https://query.wikidata.org/sparql"
HEADERS = {"User-Agent": "MusiCompass/1.0 (ananya.kaulgi@gmail.com) Wikidata instrument ingestion"}

# ── Country → Region mapping ──────────────────────────────────────────────────
COUNTRY_REGION = {
    # South Asia
    "India": "South Asia", "Pakistan": "South Asia", "Bangladesh": "South Asia",
    "Sri Lanka": "South Asia", "Nepal": "South Asia", "Bhutan": "South Asia",
    "Afghanistan": "Central Asia",
    # East Asia
    "China": "East Asia", "Japan": "East Asia", "South Korea": "East Asia",
    "North Korea": "East Asia", "Taiwan": "East Asia", "Mongolia": "Central Asia",
    # Southeast Asia
    "Indonesia": "Southeast Asia", "Malaysia": "Southeast Asia", "Philippines": "Southeast Asia",
    "Thailand": "Southeast Asia", "Vietnam": "Southeast Asia", "Cambodia": "Southeast Asia",
    "Myanmar": "Southeast Asia", "Laos": "Southeast Asia", "Singapore": "Southeast Asia",
    "Brunei": "Southeast Asia", "Timor-Leste": "Southeast Asia",
    # Central Asia
    "Kazakhstan": "Central Asia", "Uzbekistan": "Central Asia", "Kyrgyzstan": "Central Asia",
    "Tajikistan": "Central Asia", "Turkmenistan": "Central Asia", "Azerbaijan": "Middle East & North Africa",
    "Armenia": "Middle East & North Africa", "Georgia": "Middle East & North Africa",
    # Middle East & North Africa
    "Iran": "Middle East & North Africa", "Iraq": "Middle East & North Africa",
    "Turkey": "Middle East & North Africa", "Syria": "Middle East & North Africa",
    "Lebanon": "Middle East & North Africa", "Jordan": "Middle East & North Africa",
    "Israel": "Middle East & North Africa", "Palestine": "Middle East & North Africa",
    "Saudi Arabia": "Middle East & North Africa", "Yemen": "Middle East & North Africa",
    "Oman": "Middle East & North Africa", "United Arab Emirates": "Middle East & North Africa",
    "Qatar": "Middle East & North Africa", "Kuwait": "Middle East & North Africa",
    "Bahrain": "Middle East & North Africa", "Egypt": "Middle East & North Africa",
    "Libya": "Middle East & North Africa", "Tunisia": "Middle East & North Africa",
    "Algeria": "Middle East & North Africa", "Morocco": "Middle East & North Africa",
    "Sudan": "East Africa", "South Sudan": "East Africa",
    # West Africa
    "Nigeria": "West Africa", "Ghana": "West Africa", "Senegal": "West Africa",
    "Mali": "West Africa", "Guinea": "West Africa", "Sierra Leone": "West Africa",
    "Liberia": "West Africa", "Ivory Coast": "West Africa", "Burkina Faso": "West Africa",
    "Benin": "West Africa", "Togo": "West Africa", "Gambia": "West Africa",
    "Guinea-Bissau": "West Africa", "Cape Verde": "West Africa", "Niger": "West Africa",
    "Mauritania": "West Africa",
    # East Africa
    "Ethiopia": "East Africa", "Kenya": "East Africa", "Tanzania": "East Africa",
    "Uganda": "East Africa", "Rwanda": "East Africa", "Burundi": "East Africa",
    "Somalia": "East Africa", "Djibouti": "East Africa", "Eritrea": "East Africa",
    "Madagascar": "East Africa",
    # Central Africa
    "Democratic Republic of the Congo": "Central Africa",
    "Republic of the Congo": "Central Africa", "Cameroon": "Central Africa",
    "Central African Republic": "Central Africa", "Chad": "Central Africa",
    "Gabon": "Central Africa", "Equatorial Guinea": "Central Africa",
    # Southern Africa
    "South Africa": "Southern Africa", "Zimbabwe": "Southern Africa",
    "Mozambique": "Southern Africa", "Zambia": "Southern Africa",
    "Malawi": "Southern Africa", "Angola": "Southern Africa",
    "Namibia": "Southern Africa", "Botswana": "Southern Africa",
    "Lesotho": "Southern Africa", "Swaziland": "Southern Africa",
    # Western Europe
    "Spain": "Western Europe", "Portugal": "Western Europe", "France": "Western Europe",
    "Italy": "Western Europe", "Germany": "Western Europe", "Austria": "Western Europe",
    "Switzerland": "Western Europe", "Belgium": "Western Europe",
    "Netherlands": "Western Europe", "Ireland": "Western Europe",
    "United Kingdom": "Western Europe", "Greece": "Western Europe",
    "Malta": "Western Europe",
    # Northern Europe
    "Sweden": "Northern Europe", "Norway": "Northern Europe", "Finland": "Northern Europe",
    "Denmark": "Northern Europe", "Iceland": "Northern Europe", "Estonia": "Northern Europe",
    "Latvia": "Northern Europe", "Lithuania": "Northern Europe",
    # Eastern Europe
    "Russia": "Eastern Europe", "Ukraine": "Eastern Europe", "Poland": "Eastern Europe",
    "Czech Republic": "Eastern Europe", "Slovakia": "Eastern Europe",
    "Hungary": "Eastern Europe", "Romania": "Eastern Europe", "Bulgaria": "Eastern Europe",
    "Serbia": "Eastern Europe", "Croatia": "Eastern Europe", "Slovenia": "Eastern Europe",
    "Bosnia and Herzegovina": "Eastern Europe", "North Macedonia": "Eastern Europe",
    "Albania": "Eastern Europe", "Montenegro": "Eastern Europe",
    "Moldova": "Eastern Europe", "Belarus": "Eastern Europe",
    # North America
    "United States": "North America", "Canada": "North America", "Mexico": "North America",
    # Caribbean
    "Cuba": "Caribbean", "Jamaica": "Caribbean", "Trinidad and Tobago": "Caribbean",
    "Haiti": "Caribbean", "Dominican Republic": "Caribbean", "Puerto Rico": "Caribbean",
    "Barbados": "Caribbean", "Bahamas": "Caribbean",
    # Central America
    "Guatemala": "South America", "Belize": "South America", "Honduras": "South America",
    "El Salvador": "South America", "Nicaragua": "South America", "Costa Rica": "South America",
    "Panama": "South America",
    # South America
    "Brazil": "South America", "Argentina": "South America", "Chile": "South America",
    "Peru": "South America", "Bolivia": "South America", "Ecuador": "South America",
    "Colombia": "South America", "Venezuela": "South America", "Uruguay": "South America",
    "Paraguay": "South America", "Guyana": "South America", "Suriname": "South America",
    # Oceania
    "Australia": "Oceania", "New Zealand": "Oceania", "Papua New Guinea": "Oceania",
    "Fiji": "Oceania", "Samoa": "Oceania", "Tonga": "Oceania",
    "Solomon Islands": "Oceania", "Vanuatu": "Oceania",
}

HS_CATEGORY = {
    "1": "Idiophone",
    "2": "Membranophone",
    "3": "Chordophone",
    "4": "Aerophone",
    "5": "Electrophone",
}

def hs_to_category(hs_code):
    if not hs_code:
        return None
    first = str(hs_code).strip()[0]
    return HS_CATEGORY.get(first)


def sparql_query(query, retries=3):
    for attempt in range(retries):
        try:
            r = requests.get(
                SPARQL,
                params={"query": query, "format": "json"},
                headers=HEADERS,
                timeout=60,
            )
            r.raise_for_status()
            return r.json()["results"]["bindings"]
        except Exception as e:
            if attempt < retries - 1:
                print(f"  Retry {attempt+1} after error: {e}", file=sys.stderr)
                time.sleep(5)
            else:
                print(f"  Failed after {retries} attempts: {e}", file=sys.stderr)
                return []


def escape_sql(s):
    if s is None:
        return "NULL"
    # Escape single quotes
    s = str(s).replace("'", "''")
    return f"'{s}'"


def fetch_all_instruments():
    """Paginate through all Wikidata musical instruments."""
    instruments = {}  # keyed by QID to deduplicate
    offset = 0
    batch_size = 100

    print(f"Fetching instruments from Wikidata in batches of {batch_size}...")

    while True:
        query = f"""
SELECT DISTINCT ?item ?itemLabel ?itemDescription ?originLabel ?hsClass ?nativeLabel ?wp_slug
WHERE {{
  ?item wdt:P31 wd:Q34379.
  OPTIONAL {{
    ?item wdt:P495 ?origin.
    ?origin rdfs:label ?originLabel.
    FILTER(LANG(?originLabel) = "en")
  }}
  OPTIONAL {{ ?item wdt:P1762 ?hsClass. }}
  OPTIONAL {{
    ?item wdt:P1705 ?nativeLabel.
    FILTER(LANG(?nativeLabel) != "en")
  }}
  OPTIONAL {{
    ?article schema:about ?item;
             schema:inLanguage "en";
             schema:isPartOf <https://en.wikipedia.org/>.
    BIND(REPLACE(STR(?article), "https://en.wikipedia.org/wiki/", "") AS ?wp_slug)
  }}
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "en".
  }}
}}
ORDER BY ?itemLabel
LIMIT {batch_size}
OFFSET {offset}
"""
        rows = sparql_query(query)
        if not rows:
            break

        for row in rows:
            qid = row["item"]["value"].split("/")[-1]
            name = row.get("itemLabel", {}).get("value", "")
            # Skip if name looks like a QID (no English label)
            if re.match(r'^Q\d+$', name):
                continue
            # Skip very short or empty names
            if len(name) < 2:
                continue

            desc = row.get("itemDescription", {}).get("value")
            origin = row.get("originLabel", {}).get("value")
            hs_code = row.get("hsClass", {}).get("value")
            native = row.get("nativeLabel", {}).get("value")
            wp_slug = row.get("wp_slug", {}).get("value")
            if wp_slug:
                wp_slug = wp_slug.replace("%27", "'").replace("%22", '"')

            region = COUNTRY_REGION.get(origin) if origin else None

            # Deduplicate by QID, keep richest record
            if qid not in instruments or (region and not instruments[qid]["origin_region"]):
                instruments[qid] = {
                    "name": name,
                    "name_native": native,
                    "hs_code": hs_code,
                    "hs_category": hs_to_category(hs_code),
                    "description": desc,
                    "origin_region": region,
                    "origin_country": origin,
                    "wikipedia_slug": wp_slug,
                }

        fetched = offset + len(rows)
        print(f"  Fetched {fetched} instruments so far (batch size: {len(rows)})")

        if len(rows) < batch_size:
            break

        offset += batch_size
        time.sleep(1)  # Be polite to Wikidata

    return instruments


def generate_sql(instruments):
    # Deduplicate by name (case-insensitive), keeping the richest record
    by_name = {}
    for qid, inst in instruments.items():
        key = inst["name"].lower()
        if key not in by_name:
            by_name[key] = inst
        else:
            existing = by_name[key]
            # Prefer record with more fields filled in
            score = lambda x: sum(1 for v in x.values() if v)
            if score(inst) > score(existing):
                by_name[key] = inst

    print(f"  After name-deduplication: {len(by_name)} unique instruments")

    lines = []
    lines.append("-- Wikidata instrument seed — generated by MusiCompass ingest_instruments.py")
    lines.append("INSERT INTO instruments (id, name, name_native, hs_category, hornbostel_sachs, description, origin_region, wikipedia_slug, created_at, updated_at)")
    lines.append("VALUES")

    values = []
    for _, inst in by_name.items():
        name = escape_sql(inst["name"])
        native = escape_sql(inst["name_native"])
        hs_cat = escape_sql(inst["hs_category"])
        hs_code = escape_sql(inst["hs_code"])
        desc = escape_sql(inst["description"])
        region = escape_sql(inst["origin_region"])
        slug = escape_sql(inst["wikipedia_slug"])
        values.append(
            f"  (gen_random_uuid(), {name}, {native}, {hs_cat}, {hs_code}, {desc}, {region}, {slug}, now(), now())"
        )

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (name) DO UPDATE SET")
    lines.append("  description      = COALESCE(EXCLUDED.description, instruments.description),")
    lines.append("  name_native      = COALESCE(EXCLUDED.name_native, instruments.name_native),")
    lines.append("  hs_category      = COALESCE(EXCLUDED.hs_category, instruments.hs_category),")
    lines.append("  hornbostel_sachs = COALESCE(EXCLUDED.hornbostel_sachs, instruments.hornbostel_sachs),")
    lines.append("  origin_region    = COALESCE(EXCLUDED.origin_region, instruments.origin_region),")
    lines.append("  wikipedia_slug   = COALESCE(EXCLUDED.wikipedia_slug, instruments.wikipedia_slug),")
    lines.append("  updated_at       = now()")
    lines.append(";")

    return "\n".join(lines)


if __name__ == "__main__":
    instruments = fetch_all_instruments()
    print(f"\nTotal unique instruments fetched: {len(instruments)}")

    print("Generating SQL...")
    sql = generate_sql(instruments)

    sql_path = "/tmp/instruments_wikidata.sql"
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write(sql)
    print(f"SQL written to {sql_path} ({len(sql)} bytes)")

    print("Inserting into database via docker...")
    pg_container = subprocess.check_output(
        ["docker", "ps", "--filter", "name=postgres", "-q"],
        text=True
    ).strip()

    if not pg_container:
        print("ERROR: postgres container not found!")
        sys.exit(1)

    with open(sql_path, "rb") as f:
        result = subprocess.run(
            ["docker", "exec", "-i", pg_container, "psql", "-U", "nadaatlas", "-d", "nadaatlas"],
            stdin=f,
            capture_output=True,
            text=True,
        )

    print("STDOUT:", result.stdout.strip())
    if result.stderr:
        print("STDERR:", result.stderr.strip()[:500])

    # Final count
    count_result = subprocess.run(
        ["docker", "exec", pg_container, "psql", "-U", "nadaatlas", "-d", "nadaatlas",
         "-c", "SELECT COUNT(*) FROM instruments WHERE deleted_at IS NULL;"],
        capture_output=True, text=True
    )
    print("\nFinal instrument count:")
    print(count_result.stdout)
