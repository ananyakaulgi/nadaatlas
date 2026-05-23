"""
Seed common Hindustani and Carnatic talas.
Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_talas.py
"""

import os
import subprocess
import sys
import tempfile

TALAS = [
    # ─────────────────────────────────────────────
    # HINDUSTANI
    # ─────────────────────────────────────────────
    {
        "name": "Teental",
        "name_native": "तीनताल",
        "tradition": "hindustani",
        "beats": 16,
        "vibhag": 4,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "4+4+4+4",
        "common_tempos": ["vilambit", "madhya", "drut"],
        "description": (
            "The most common tala in Hindustani classical music. "
            "16 beats in 4 equal sections of 4. Khali (empty beat) falls on beat 9."
        ),
        "wikipedia_slug": "Teental",
    },
    {
        "name": "Jhaptal",
        "name_native": "झपताल",
        "tradition": "hindustani",
        "beats": 10,
        "vibhag": 4,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "2+3+2+3",
        "common_tempos": ["madhya", "drut"],
        "description": (
            "10-beat tala divided as 2+3+2+3. "
            "Khali falls on beat 6. Widely used in khayal and instrumental music."
        ),
        "wikipedia_slug": "Jhaptal",
    },
    {
        "name": "Rupak",
        "name_native": "रूपक",
        "tradition": "hindustani",
        "beats": 7,
        "vibhag": 3,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "3+2+2",
        "common_tempos": ["madhya", "drut"],
        "description": (
            "7-beat tala with the unusual feature that sam (beat 1) falls in the khali section. "
            "Divided 3+2+2. Popular in thumri, dadra and light classical genres."
        ),
        "wikipedia_slug": "Rupak_tala_(Hindustani)",
    },
    {
        "name": "Ektaal",
        "name_native": "एकताल",
        "tradition": "hindustani",
        "beats": 12,
        "vibhag": 6,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "2+2+2+2+2+2",
        "common_tempos": ["vilambit", "madhya"],
        "description": (
            "12-beat tala in 6 equal vibhags of 2 beats each. "
            "In vilambit khayal it is the tala of choice for slow, expansive alap-style singing."
        ),
        "wikipedia_slug": "Ektaal",
    },
    {
        "name": "Dadra",
        "name_native": "दादरा",
        "tradition": "hindustani",
        "beats": 6,
        "vibhag": 2,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "3+3",
        "common_tempos": ["madhya", "drut"],
        "description": (
            "6-beat tala in 2 vibhags of 3. The defining tala of the dadra light-classical genre. "
            "Also used in thumri and folk music."
        ),
        "wikipedia_slug": "Dadra_tala",
    },
    {
        "name": "Keherwa",
        "name_native": "कहरवा",
        "tradition": "hindustani",
        "beats": 8,
        "vibhag": 2,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "4+4",
        "common_tempos": ["madhya", "drut"],
        "description": (
            "8-beat tala in 2 vibhags of 4. Ubiquitous in folk, devotional, thumri and filmi music."
        ),
        "wikipedia_slug": "Kaharwa",
    },
    {
        "name": "Dhamar",
        "name_native": "धमार",
        "tradition": "hindustani",
        "beats": 14,
        "vibhag": 4,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "5+2+3+4",
        "common_tempos": ["madhya"],
        "description": (
            "14-beat tala associated exclusively with the dhamar style of singing, "
            "performed during Holi celebrations. Divided 5+2+3+4."
        ),
        "wikipedia_slug": "Dhamar",
    },
    {
        "name": "Deepchandi",
        "name_native": "दीपचंदी",
        "tradition": "hindustani",
        "beats": 14,
        "vibhag": 4,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "3+4+3+4",
        "common_tempos": ["vilambit", "madhya"],
        "description": (
            "14-beat tala divided 3+4+3+4. Widely used for slow thumri and semi-classical compositions. "
            "Also called Chandrakauns tala in some traditions."
        ),
        "wikipedia_slug": "Deepchandi",
    },
    {
        "name": "Tilwada",
        "name_native": "तिलवाड़ा",
        "tradition": "hindustani",
        "beats": 16,
        "vibhag": 4,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "4+4+4+4",
        "common_tempos": ["vilambit"],
        "description": (
            "16-beat tala structurally similar to Teental but with a characteristic bol pattern. "
            "Preferred for slow vilambit khayal renditions."
        ),
        "wikipedia_slug": "Tilwada",
    },
    {
        "name": "Chautal",
        "name_native": "चौताल",
        "tradition": "hindustani",
        "beats": 12,
        "vibhag": 6,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "2+2+2+2+2+2",
        "common_tempos": ["madhya", "drut"],
        "description": (
            "12-beat tala in 6 vibhags of 2. Central to dhrupad and dhamar styles; "
            "less used in khayal. Has a driving, martial quality."
        ),
        "wikipedia_slug": "Chautal",
    },
    {
        "name": "Jhoomra",
        "name_native": "झूमरा",
        "tradition": "hindustani",
        "beats": 14,
        "vibhag": 4,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "3+4+3+4",
        "common_tempos": ["vilambit"],
        "description": (
            "14-beat tala used primarily in slow vilambit khayal. "
            "Similar to Deepchandi but with a distinctive bol pattern giving it a lilting feel."
        ),
        "wikipedia_slug": "Jhoomra",
    },
    {
        "name": "Matta Tal",
        "name_native": "मत्त ताल",
        "tradition": "hindustani",
        "beats": 9,
        "vibhag": 3,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "2+3+4",
        "common_tempos": ["madhya"],
        "description": (
            "9-beat tala in 3 unequal vibhags of 2+3+4. Used in dhrupad and some instrumental compositions."
        ),
        "wikipedia_slug": "Matta_tala",
    },
    {
        "name": "Sooltaal",
        "name_native": "सूलताल",
        "tradition": "hindustani",
        "beats": 10,
        "vibhag": 5,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "2+2+2+2+2",
        "common_tempos": ["madhya", "drut"],
        "description": (
            "10-beat tala in 5 equal vibhags of 2. Used in dhrupad; "
            "different from Jhaptal despite the same beat count."
        ),
        "wikipedia_slug": "Sooltaal",
    },
    {
        "name": "Ada Chautal",
        "name_native": "आड़ा चौताल",
        "tradition": "hindustani",
        "beats": 14,
        "vibhag": 7,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "2+2+2+2+2+2+2",
        "common_tempos": ["madhya"],
        "description": (
            "14-beat tala used in dhrupad. The name means 'crooked chautal'. "
            "Has an irregular feel compared to regular 14-beat talas."
        ),
        "wikipedia_slug": "Ada_Chautal",
    },
    {
        "name": "Pancham Sawari",
        "name_native": "पंचम सवारी",
        "tradition": "hindustani",
        "beats": 15,
        "vibhag": 5,
        "sam_beats": "1",
        "jati": None,
        "anga_structure": "3+3+3+3+3",
        "common_tempos": ["madhya"],
        "description": (
            "15-beat tala in 5 equal vibhags of 3. Part of the sawari family of asymmetric talas "
            "used in contemporary and fusion instrumental music."
        ),
        "wikipedia_slug": None,
    },
    # ─────────────────────────────────────────────
    # CARNATIC
    # ─────────────────────────────────────────────
    {
        "name": "Adi Tala",
        "name_native": "ஆதி தாளம்",
        "tradition": "carnatic",
        "beats": 8,
        "vibhag": 3,
        "sam_beats": "1",
        "jati": "chatusra",
        "anga_structure": "4+2+2",
        "common_tempos": ["madhyama kala", "tisra kala"],
        "description": (
            "The most common tala in Carnatic music. "
            "Chatusra jati Triputa tala: one laghu (4 beats) + 2 drutams (2 beats each) = 8 aksharas. "
            "Forms the backbone of most Carnatic compositions."
        ),
        "wikipedia_slug": "Adi_tala",
    },
    {
        "name": "Rupaka Tala",
        "name_native": "ரூபக தாளம்",
        "tradition": "carnatic",
        "beats": 6,
        "vibhag": 2,
        "sam_beats": "1",
        "jati": "chatusra",
        "anga_structure": "2+4",
        "common_tempos": ["madhyama kala"],
        "description": (
            "6-beat tala: one drutam (2) + one chatusra laghu (4). "
            "Second most common Carnatic tala after Adi. Used in many keertanas."
        ),
        "wikipedia_slug": "Rupaka_tala",
    },
    {
        "name": "Misra Chapu",
        "name_native": "மிஸ்ர சாபு",
        "tradition": "carnatic",
        "beats": 7,
        "vibhag": 2,
        "sam_beats": "1",
        "jati": "misra",
        "anga_structure": "3+4",
        "common_tempos": ["madhyama kala", "druta kala"],
        "description": (
            "7-beat chapu tala divided 3+4. One of the most popular talas in Carnatic music, "
            "especially for thevaram and other devotional compositions."
        ),
        "wikipedia_slug": "Misra_Chapu",
    },
    {
        "name": "Khanda Chapu",
        "name_native": "கண்ட சாபு",
        "tradition": "carnatic",
        "beats": 5,
        "vibhag": 2,
        "sam_beats": "1",
        "jati": "khanda",
        "anga_structure": "2+3",
        "common_tempos": ["madhyama kala"],
        "description": (
            "5-beat chapu tala divided 2+3. Used in folk-influenced compositions "
            "and some Carnatic songs with a lively, asymmetric feel."
        ),
        "wikipedia_slug": "Khanda_Chapu",
    },
    {
        "name": "Dhruva Tala",
        "name_native": "த்ருவ தாளம்",
        "tradition": "carnatic",
        "beats": 14,
        "vibhag": 4,
        "sam_beats": "1",
        "jati": "chatusra",
        "anga_structure": "4+2+4+4",
        "common_tempos": ["madhyama kala"],
        "description": (
            "One of the 7 Suladi Sapta Talas. Chatusra jati: laghu+drutam+laghu+laghu = 4+2+4+4 = 14 aksharas."
        ),
        "wikipedia_slug": "Dhruva_tala",
    },
    {
        "name": "Matya Tala",
        "name_native": "மத்ய தாளம்",
        "tradition": "carnatic",
        "beats": 10,
        "vibhag": 3,
        "sam_beats": "1",
        "jati": "chatusra",
        "anga_structure": "4+2+4",
        "common_tempos": ["madhyama kala"],
        "description": (
            "One of the 7 Suladi Sapta Talas. Chatusra jati: laghu+drutam+laghu = 4+2+4 = 10 aksharas."
        ),
        "wikipedia_slug": "Matya_tala",
    },
    {
        "name": "Triputa Tala",
        "name_native": "த்ரிபுட தாளம்",
        "tradition": "carnatic",
        "beats": 7,
        "vibhag": 3,
        "sam_beats": "1",
        "jati": "tisra",
        "anga_structure": "3+2+2",
        "common_tempos": ["madhyama kala"],
        "description": (
            "One of the 7 Suladi Sapta Talas. Tisra jati: laghu+drutam+drutam = 3+2+2 = 7 aksharas. "
            "The chatusra jati version (4+2+2) is the Adi tala."
        ),
        "wikipedia_slug": "Triputa_tala",
    },
    {
        "name": "Ata Tala",
        "name_native": "அட தாளம்",
        "tradition": "carnatic",
        "beats": 14,
        "vibhag": 4,
        "sam_beats": "1",
        "jati": "khanda",
        "anga_structure": "5+5+2+2",
        "common_tempos": ["madhyama kala"],
        "description": (
            "One of the 7 Suladi Sapta Talas. Khanda jati: laghu+laghu+drutam+drutam = 5+5+2+2 = 14 aksharas."
        ),
        "wikipedia_slug": "Ata_tala",
    },
    {
        "name": "Jhampa Tala",
        "name_native": "ஜம்ப தாளம்",
        "tradition": "carnatic",
        "beats": 10,
        "vibhag": 3,
        "sam_beats": "1",
        "jati": "misra",
        "anga_structure": "7+1+2",
        "common_tempos": ["madhyama kala"],
        "description": (
            "One of the 7 Suladi Sapta Talas. Misra jati: laghu+anudrutam+drutam = 7+1+2 = 10 aksharas."
        ),
        "wikipedia_slug": "Jhampa_tala",
    },
    {
        "name": "Eka Tala",
        "name_native": "ஏக தாளம்",
        "tradition": "carnatic",
        "beats": 4,
        "vibhag": 1,
        "sam_beats": "1",
        "jati": "chatusra",
        "anga_structure": "4",
        "common_tempos": ["madhyama kala", "druta kala"],
        "description": (
            "One of the 7 Suladi Sapta Talas. Chatusra jati: single laghu = 4 aksharas. "
            "The simplest of the sapta talas."
        ),
        "wikipedia_slug": "Eka_tala",
    },
]


def escape_sql(v: str) -> str:
    return v.replace("'", "''")


def s(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, list):
        items = ", ".join(f"'{escape_sql(x)}'" for x in v)
        return f"ARRAY[{items}]::text[]"
    return f"'{escape_sql(str(v))}'"


def n(v) -> str:
    return str(v) if v is not None else "NULL"


def build_sql(talas: list[dict]) -> str:
    lines = [
        "-- Hindustani and Carnatic talas",
        "INSERT INTO talas (",
        "  id, name, name_native, tradition,",
        "  beats, vibhag, sam_beats, jati,",
        "  anga_structure, common_tempos,",
        "  description, wikipedia_slug,",
        "  created_at, updated_at",
        ") VALUES",
    ]

    values = []
    for t in talas:
        row = (
            f"  (gen_random_uuid(), {s(t['name'])}, {s(t['name_native'])}, {s(t['tradition'])}, "
            f"{n(t['beats'])}, {n(t['vibhag'])}, {s(t['sam_beats'])}, {s(t['jati'])}, "
            f"{s(t['anga_structure'])}, {s(t['common_tempos'])}, "
            f"{s(t['description'])}, {s(t['wikipedia_slug'])}, "
            f"NOW(), NOW())"
        )
        values.append(row)

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (name) DO UPDATE SET")
    lines.append("  tradition     = EXCLUDED.tradition,")
    lines.append("  beats         = EXCLUDED.beats,")
    lines.append("  vibhag        = EXCLUDED.vibhag,")
    lines.append("  sam_beats     = EXCLUDED.sam_beats,")
    lines.append("  anga_structure = EXCLUDED.anga_structure,")
    lines.append("  common_tempos = EXCLUDED.common_tempos,")
    lines.append("  description   = EXCLUDED.description,")
    lines.append("  updated_at    = NOW();")

    return "\n".join(lines)


def main():
    import tempfile

    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    sql = build_sql(TALAS)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    hindustani = sum(1 for t in TALAS if t["tradition"] == "hindustani")
    carnatic = sum(1 for t in TALAS if t["tradition"] == "carnatic")
    print(f"Seeding {len(TALAS)} talas ({hindustani} Hindustani, {carnatic} Carnatic)...")

    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ {len(TALAS)} talas seeded.\n")
    print("Sample:")
    for t in TALAS[:6]:
        print(f"  [{t['tradition'][:4]}] {t['name']:<20} {t['beats']} beats  {t['anga_structure']}")


if __name__ == "__main__":
    main()
