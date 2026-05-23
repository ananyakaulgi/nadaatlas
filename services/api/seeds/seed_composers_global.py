"""
Seed global composers — Western Classical, Jazz, Tango, Afrobeat, Arabic, Flamenco.
Also inserts missing traditions (Western Classical, Jazz) if not present.

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_composers_global.py
"""

import os
import subprocess
import sys
import tempfile

# ─────────────────────────────────────────────────────────────────────────────
# Traditions to ensure exist before inserting composers
# ─────────────────────────────────────────────────────────────────────────────
MISSING_TRADITIONS = [
    {
        "name": "Western Classical",
        "name_native": None,
        "region": "Western Europe",
        "subregion": "Europe",
        "origin_period": "Medieval–present",
        "description": (
            "The art music tradition of Western Europe, spanning Gregorian chant through "
            "Baroque, Classical, Romantic, and 20th-century styles. Characterised by written "
            "notation, harmonic counterpoint, and the symphony orchestra."
        ),
        "wikipedia_slug": "Classical_music",
    },
    {
        "name": "Jazz",
        "name_native": None,
        "region": "North America",
        "subregion": "United States",
        "origin_period": "Late 19th century",
        "description": (
            "An American music genre rooted in African American communities, combining "
            "African rhythmic traditions with European harmony. Known for improvisation, "
            "syncopation, swing, and the blues."
        ),
        "wikipedia_slug": "Jazz",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Composers
# ─────────────────────────────────────────────────────────────────────────────
COMPOSERS = [
    # ── Western Classical — Baroque ───────────────────────────────────────────
    {
        "name": "Johann Sebastian Bach",
        "name_native": None,
        "name_sort": "Bach, Johann Sebastian",
        "tradition": "Western Classical",
        "era": "Baroque",
        "born": 1685, "died": 1750,
        "birth_place": "Eisenach, Thuringia",
        "nationality": "German",
        "biography_short": (
            "The towering figure of Baroque music, Bach produced an extraordinary body of "
            "work across every genre of his era: keyboard music, orchestral suites, "
            "Brandenburg concertos, choral passions, and the monumental Mass in B minor. "
            "His counterpoint remains the benchmark of Western musical craft."
        ),
        "wikidata_id": "Q1339",
        "wikipedia_slug": "Johann_Sebastian_Bach",
        "is_verified": True,
    },
    {
        "name": "Antonio Vivaldi",
        "name_native": None,
        "name_sort": "Vivaldi, Antonio",
        "tradition": "Western Classical",
        "era": "Baroque",
        "born": 1678, "died": 1741,
        "birth_place": "Venice, Republic of Venice",
        "nationality": "Italian",
        "biography_short": (
            "Venetian composer and virtuoso violinist whose concertos — especially "
            "The Four Seasons — defined the Baroque concerto form. He wrote over 500 "
            "concertos and 50 operas, and profoundly influenced Bach."
        ),
        "wikidata_id": "Q1340",
        "wikipedia_slug": "Antonio_Vivaldi",
        "is_verified": True,
    },
    {
        "name": "George Frideric Handel",
        "name_native": "Georg Friedrich Händel",
        "name_sort": "Handel, George Frideric",
        "tradition": "Western Classical",
        "era": "Baroque",
        "born": 1685, "died": 1759,
        "birth_place": "Halle, Duchy of Magdeburg",
        "nationality": "German-British",
        "biography_short": (
            "German-born composer who became a British institution, famed above all for "
            "Messiah. Handel dominated London's opera and oratorio scene for decades and "
            "defined the English choral tradition."
        ),
        "wikidata_id": "Q7302",
        "wikipedia_slug": "George_Frideric_Handel",
        "is_verified": True,
    },
    # ── Western Classical — Classical period ──────────────────────────────────
    {
        "name": "Wolfgang Amadeus Mozart",
        "name_native": None,
        "name_sort": "Mozart, Wolfgang Amadeus",
        "tradition": "Western Classical",
        "era": "Classical period",
        "born": 1756, "died": 1791,
        "birth_place": "Salzburg, Holy Roman Empire",
        "nationality": "Austrian",
        "biography_short": (
            "Child prodigy and supreme melodist, Mozart composed 41 symphonies, 27 piano "
            "concertos, and operas including Don Giovanni and The Magic Flute — all before "
            "dying at 35. His music unites formal elegance with profound emotional depth."
        ),
        "wikidata_id": "Q254",
        "wikipedia_slug": "Wolfgang_Amadeus_Mozart",
        "is_verified": True,
    },
    {
        "name": "Joseph Haydn",
        "name_native": None,
        "name_sort": "Haydn, Joseph",
        "tradition": "Western Classical",
        "era": "Classical period",
        "born": 1732, "died": 1809,
        "birth_place": "Rohrau, Austria",
        "nationality": "Austrian",
        "biography_short": (
            "The 'Father of the Symphony' and 'Father of the String Quartet', Haydn spent "
            "30 years as court composer for the Esterházy princes and produced 104 "
            "symphonies, 68 string quartets, and oratorios including The Creation."
        ),
        "wikidata_id": "Q7349",
        "wikipedia_slug": "Joseph_Haydn",
        "is_verified": True,
    },
    # ── Western Classical — Romantic ──────────────────────────────────────────
    {
        "name": "Ludwig van Beethoven",
        "name_native": None,
        "name_sort": "Beethoven, Ludwig van",
        "tradition": "Western Classical",
        "era": "Classical/Romantic",
        "born": 1770, "died": 1827,
        "birth_place": "Bonn, Electorate of Cologne",
        "nationality": "German",
        "biography_short": (
            "Beethoven bridged the Classical and Romantic eras, composing masterworks "
            "including the Ninth Symphony (with its Ode to Joy), the Moonlight Sonata, "
            "and the late string quartets — much of it while profoundly deaf."
        ),
        "wikidata_id": "Q255",
        "wikipedia_slug": "Ludwig_van_Beethoven",
        "is_verified": True,
    },
    {
        "name": "Johannes Brahms",
        "name_native": None,
        "name_sort": "Brahms, Johannes",
        "tradition": "Western Classical",
        "era": "Romantic",
        "born": 1833, "died": 1897,
        "birth_place": "Hamburg, Free City of Hamburg",
        "nationality": "German",
        "biography_short": (
            "A master of symphonic and chamber forms, Brahms balanced Classical "
            "structural rigour with Romantic warmth. His four symphonies, violin concerto, "
            "and German Requiem are cornerstones of the orchestral canon."
        ),
        "wikidata_id": "Q7294",
        "wikipedia_slug": "Johannes_Brahms",
        "is_verified": True,
    },
    {
        "name": "Frédéric Chopin",
        "name_native": "Fryderyk Franciszek Chopin",
        "name_sort": "Chopin, Frédéric",
        "tradition": "Western Classical",
        "era": "Romantic",
        "born": 1810, "died": 1849,
        "birth_place": "Żelazowa Wola, Duchy of Warsaw",
        "nationality": "Polish-French",
        "biography_short": (
            "The supreme poet of the piano, Chopin composed almost exclusively for his "
            "instrument — nocturnes, études, ballades, preludes, and mazurkas that fused "
            "Polish folk idioms with refined French elegance and harmonic innovation."
        ),
        "wikidata_id": "Q1268",
        "wikipedia_slug": "Frédéric_Chopin",
        "is_verified": True,
    },
    {
        "name": "Pyotr Ilyich Tchaikovsky",
        "name_native": "Пётр Ильич Чайковский",
        "name_sort": "Tchaikovsky, Pyotr Ilyich",
        "tradition": "Western Classical",
        "era": "Romantic",
        "born": 1840, "died": 1893,
        "birth_place": "Votkinsk, Russian Empire",
        "nationality": "Russian",
        "biography_short": (
            "Russia's most beloved composer, Tchaikovsky created Swan Lake, The Nutcracker, "
            "and The Sleeping Beauty, along with six symphonies and the spectacular "
            "Violin Concerto. His melodic gift and orchestral colour remain unmatched."
        ),
        "wikidata_id": "Q7321",
        "wikipedia_slug": "Pyotr_Ilyich_Tchaikovsky",
        "is_verified": True,
    },
    {
        "name": "Niccolò Paganini",
        "name_native": None,
        "name_sort": "Paganini, Niccolò",
        "tradition": "Western Classical",
        "era": "Romantic",
        "born": 1782, "died": 1840,
        "birth_place": "Genoa, Republic of Genoa",
        "nationality": "Italian",
        "biography_short": (
            "The most celebrated violinist of his era, Paganini pushed the instrument to "
            "previously unimaginable technical extremes. His 24 Caprices and concertos "
            "redefined virtuosity and inspired Liszt, Schumann, and Brahms."
        ),
        "wikidata_id": "Q168701",
        "wikipedia_slug": "Niccolò_Paganini",
        "is_verified": True,
    },
    {
        "name": "Claude Debussy",
        "name_native": None,
        "name_sort": "Debussy, Claude",
        "tradition": "Western Classical",
        "era": "Impressionist",
        "born": 1862, "died": 1918,
        "birth_place": "Saint-Germain-en-Laye, France",
        "nationality": "French",
        "biography_short": (
            "Pioneer of musical Impressionism, Debussy dissolved traditional harmonic "
            "structures in favour of colour, texture, and atmosphere. Clair de lune, "
            "La Mer, and the Préludes transformed the language of Western music."
        ),
        "wikidata_id": "Q1312",
        "wikipedia_slug": "Claude_Debussy",
        "is_verified": True,
    },
    # ── Jazz ──────────────────────────────────────────────────────────────────
    {
        "name": "Duke Ellington",
        "name_native": None,
        "name_sort": "Ellington, Duke",
        "tradition": "Jazz",
        "era": "20th century",
        "born": 1899, "died": 1974,
        "birth_place": "Washington, D.C., United States",
        "nationality": "American",
        "biography_short": (
            "The most significant composer in jazz history, Ellington led his orchestra "
            "for over five decades and composed over 3,000 pieces — from three-minute "
            "pop gems to extended suites. He elevated jazz to a concert art form."
        ),
        "wikidata_id": "Q105682",
        "wikipedia_slug": "Duke_Ellington",
        "is_verified": True,
    },
    {
        "name": "Miles Davis",
        "name_native": None,
        "name_sort": "Davis, Miles",
        "tradition": "Jazz",
        "era": "20th century",
        "born": 1926, "died": 1991,
        "birth_place": "Alton, Illinois, United States",
        "nationality": "American",
        "biography_short": (
            "The chameleon of jazz, Davis led six distinct revolutionary movements — "
            "bebop, cool jazz, hard bop, modal jazz (Kind of Blue), jazz fusion, and "
            "electric jazz — making him the most restlessly innovative figure in jazz history."
        ),
        "wikidata_id": "Q93341",
        "wikipedia_slug": "Miles_Davis",
        "is_verified": True,
    },
    # ── Tango ─────────────────────────────────────────────────────────────────
    {
        "name": "Astor Piazzolla",
        "name_native": None,
        "name_sort": "Piazzolla, Astor",
        "tradition": "Tango",
        "era": "20th century",
        "born": 1921, "died": 1992,
        "birth_place": "Mar del Plata, Argentina",
        "nationality": "Argentine",
        "biography_short": (
            "Piazzolla revolutionised traditional Argentine tango by infusing it with "
            "jazz harmony and classical counterpoint, creating nuevo tango. Works like "
            "Libertango and Adiós Nonino made tango a global concert music."
        ),
        "wikidata_id": "Q193236",
        "wikipedia_slug": "Astor_Piazzolla",
        "is_verified": True,
    },
    # ── Afrobeat ──────────────────────────────────────────────────────────────
    {
        "name": "Fela Kuti",
        "name_native": "Fela Anikulapo-Kuti",
        "name_sort": "Kuti, Fela",
        "tradition": "Afrobeat",
        "era": "20th century",
        "born": 1938, "died": 1997,
        "birth_place": "Abeokuta, Nigeria",
        "nationality": "Nigerian",
        "biography_short": (
            "Creator of Afrobeat — a fusion of Yoruba music, highlife, jazz, and funk "
            "over driving polyrhythmic percussion. Fela was equally renowned as a political "
            "activist who used his music to challenge Nigerian military rule."
        ),
        "wikidata_id": "Q179872",
        "wikipedia_slug": "Fela_Kuti",
        "is_verified": True,
    },
    # ── Arabic Classical ──────────────────────────────────────────────────────
    {
        "name": "Oum Kalthoum",
        "name_native": "أم كلثوم",
        "name_sort": "Kalthoum, Oum",
        "tradition": "Maqam (Arabic)",
        "era": "20th century",
        "born": 1904, "died": 1975,
        "birth_place": "Tamay ez-Zahayra, Egypt",
        "nationality": "Egyptian",
        "biography_short": (
            "The greatest singer in Arab music history, Oum Kalthoum combined classical "
            "maqam mastery with extraordinary emotional range. Her monthly Cairo concerts "
            "in the 1960s–70s brought the Arab world to a standstill."
        ),
        "wikidata_id": "Q232793",
        "wikipedia_slug": "Umm_Kulthum",
        "is_verified": True,
    },
    # ── Flamenco ─────────────────────────────────────────────────────────────
    {
        "name": "Paco de Lucía",
        "name_native": "Francisco Sánchez Gómez",
        "name_sort": "de Lucía, Paco",
        "tradition": "Flamenco",
        "era": "20th–21st century",
        "born": 1947, "died": 2014,
        "birth_place": "Algeciras, Andalusia, Spain",
        "nationality": "Spanish",
        "biography_short": (
            "The most influential flamenco guitarist of the 20th century, Paco de Lucía "
            "expanded flamenco's vocabulary by incorporating jazz, classical, and Latin "
            "elements. His technique and improvisational freedom redefined the art form."
        ),
        "wikidata_id": "Q273501",
        "wikipedia_slug": "Paco_de_Lucía",
        "is_verified": True,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SQL helpers
# ─────────────────────────────────────────────────────────────────────────────

def esc(v: str) -> str:
    return v.replace("'", "''")


def s(v) -> str:
    return f"'{esc(str(v))}'" if v is not None else "NULL"


def year(v) -> str:
    return f"'{v}-01-01'::date" if v is not None else "NULL"


def build_traditions_sql(traditions: list[dict]) -> str:
    lines = [
        "-- Ensure missing traditions exist",
        "INSERT INTO musical_traditions",
        "  (id, name, name_native, region, subregion, description, origin_period,",
        "   wikipedia_slug, is_active, created_at, updated_at)",
        "VALUES",
    ]
    values = []
    for t in traditions:
        values.append(
            f"  (gen_random_uuid(), {s(t['name'])}, {s(t.get('name_native'))}, "
            f"{s(t['region'])}, {s(t.get('subregion'))}, "
            f"{s(t.get('description'))}, {s(t.get('origin_period'))}, "
            f"{s(t.get('wikipedia_slug'))}, TRUE, NOW(), NOW())"
        )
    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (name) DO NOTHING;")
    return "\n".join(lines)


def build_composers_sql(composers: list[dict]) -> str:
    lines = [
        "",
        "-- Global composers seed",
        "INSERT INTO composers (",
        "  id, name, name_native, name_sort, tradition_id,",
        "  era, born, died, birth_place, nationality,",
        "  biography_short, wikidata_id, wikipedia_slug, is_verified,",
        "  created_at, updated_at",
        ") VALUES",
    ]

    values = []
    for c in composers:
        trad = c.get("tradition")
        tradition_subq = (
            f"(SELECT id FROM musical_traditions WHERE name = '{esc(trad)}' LIMIT 1)"
            if trad else "NULL"
        )
        values.append(
            f"  (gen_random_uuid(), {s(c['name'])}, {s(c.get('name_native'))}, "
            f"{s(c.get('name_sort'))}, {tradition_subq}, "
            f"{s(c.get('era'))}, {year(c.get('born'))}, {year(c.get('died'))}, "
            f"{s(c.get('birth_place'))}, {s(c.get('nationality'))}, "
            f"{s(c.get('biography_short'))}, {s(c['wikidata_id'])}, "
            f"{s(c.get('wikipedia_slug'))}, "
            f"{'TRUE' if c.get('is_verified') else 'FALSE'}, "
            f"NOW(), NOW())"
        )

    lines.append(",\n".join(values))
    lines += [
        "ON CONFLICT (wikidata_id) DO UPDATE SET",
        "  name            = EXCLUDED.name,",
        "  name_native     = EXCLUDED.name_native,",
        "  name_sort       = EXCLUDED.name_sort,",
        "  tradition_id    = EXCLUDED.tradition_id,",
        "  era             = EXCLUDED.era,",
        "  born            = EXCLUDED.born,",
        "  died            = EXCLUDED.died,",
        "  birth_place     = EXCLUDED.birth_place,",
        "  biography_short = EXCLUDED.biography_short,",
        "  wikipedia_slug  = EXCLUDED.wikipedia_slug,",
        "  is_verified     = EXCLUDED.is_verified,",
        "  updated_at      = NOW();",
    ]
    return "\n".join(lines)


def main():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    sql = build_traditions_sql(MISSING_TRADITIONS) + "\n\n" + build_composers_sql(COMPOSERS)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    by_tradition: dict[str, int] = {}
    for c in COMPOSERS:
        t = c.get("tradition") or "Other"
        by_tradition[t] = by_tradition.get(t, 0) + 1

    print(f"Seeding {len(MISSING_TRADITIONS)} traditions + {len(COMPOSERS)} composers...")
    for trad, count in sorted(by_tradition.items()):
        print(f"  {trad}: {count}")

    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ {len(COMPOSERS)} composers seeded.")


if __name__ == "__main__":
    main()
