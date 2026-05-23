"""
Seed key composers across Indian classical, Persian, Arabic, and other traditions.
Data sourced from well-known musicological references.

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_composers.py
"""

import os
import subprocess
import sys
import tempfile

# tradition_id is resolved at runtime via a subquery on musical_traditions.name
# We embed the tradition name as a lookup key.
COMPOSERS = [
    # ─────────────────────────────────────────────────────────────────────────
    # CARNATIC TRINITY (the three foundational composers of Carnatic music)
    # ─────────────────────────────────────────────────────────────────────────
    {
        "name": "Tyagaraja",
        "name_native": "త్యాగరాజు",
        "name_sort": "Tyagaraja",
        "tradition": "Carnatic",
        "era": "18th–19th century",
        "born": 1767, "died": 1847,
        "birth_place": "Tiruvarur, Tamil Nadu",
        "nationality": "Indian",
        "biography_short": "The most revered composer in Carnatic music, Tyagaraja composed over 700 kritis, predominantly in Telugu, in praise of Lord Rama. His works span virtually all Carnatic ragas and form the core of the contemporary concert repertoire.",
        "wikidata_id": "Q464485",
        "wikipedia_slug": "Tyagaraja",
        "is_verified": True,
    },
    {
        "name": "Muthuswami Dikshitar",
        "name_native": "முத்துசாமி தீட்சிதர்",
        "name_sort": "Dikshitar, Muthuswami",
        "tradition": "Carnatic",
        "era": "18th–19th century",
        "born": 1775, "died": 1835,
        "birth_place": "Tiruvarur, Tamil Nadu",
        "nationality": "Indian",
        "biography_short": "One of the Carnatic Trinity, Dikshitar composed over 450 kritis primarily in Sanskrit, with remarkable harmonic sophistication. He is credited with introducing several Hindustani ragas into the Carnatic system and penning the iconic Navagraha kritis.",
        "wikidata_id": "Q932522",
        "wikipedia_slug": "Muthuswami_Dikshitar",
        "is_verified": True,
    },
    {
        "name": "Syama Sastri",
        "name_native": "శ్యామ శాస్త్రి",
        "name_sort": "Sastri, Syama",
        "tradition": "Carnatic",
        "era": "18th–19th century",
        "born": 1762, "died": 1827,
        "birth_place": "Tiruvarur, Tamil Nadu",
        "nationality": "Indian",
        "biography_short": "The eldest of the Carnatic Trinity, Syama Sastri composed around 300 kritis, predominantly in Telugu, with deep devotion to Goddess Meenakshi. His kritis are celebrated for their melodic beauty and emotional depth.",
        "wikidata_id": "Q976832",
        "wikipedia_slug": "Syama_Sastri",
        "is_verified": True,
    },

    # ─────────────────────────────────────────────────────────────────────────
    # OTHER MAJOR CARNATIC COMPOSERS
    # ─────────────────────────────────────────────────────────────────────────
    {
        "name": "Purandaradasa",
        "name_native": "ಪುರಂದರದಾಸ",
        "name_sort": "Purandaradasa",
        "tradition": "Carnatic",
        "era": "15th–16th century",
        "born": 1484, "died": 1564,
        "birth_place": "Kshemapura, Karnataka",
        "nationality": "Indian",
        "biography_short": "Revered as the 'Father of Carnatic Music', Purandaradasa systematised the teaching of Carnatic music and composed over 475,000 songs (of which ~1,000 survive) in Kannada and Telugu.",
        "wikidata_id": "Q504002",
        "wikipedia_slug": "Purandaradasa",
        "is_verified": True,
    },
    {
        "name": "Swathi Thirunal",
        "name_native": "സ്വാതിതിരുനാൾ",
        "name_sort": "Swathi Thirunal",
        "tradition": "Carnatic",
        "era": "19th century",
        "born": 1813, "died": 1846,
        "birth_place": "Thiruvananthapuram, Kerala",
        "nationality": "Indian",
        "biography_short": "Maharaja of Travancore and prolific composer, Swathi Thirunal composed kritis in Sanskrit, Malayalam, Telugu, Hindi, and Manipravalam, bridging Carnatic and Hindustani styles.",
        "wikidata_id": "Q731763",
        "wikipedia_slug": "Swathi_Thirunal",
        "is_verified": True,
    },
    {
        "name": "Papanasam Sivan",
        "name_native": "பாபநாசம் சிவன்",
        "name_sort": "Sivan, Papanasam",
        "tradition": "Carnatic",
        "era": "19th–20th century",
        "born": 1890, "died": 1973,
        "birth_place": "Poovani, Tamil Nadu",
        "nationality": "Indian",
        "biography_short": "Prolific Carnatic composer and Tamil devotional poet, known as the 'Tamil Tyagaraja'. Composed over 500 kritis in Tamil, many of which are central to the concert repertoire.",
        "wikidata_id": "Q1053012",
        "wikipedia_slug": "Papanasam_Sivan",
        "is_verified": True,
    },

    # ─────────────────────────────────────────────────────────────────────────
    # HINDUSTANI COMPOSERS & DHRUPAD MASTERS
    # ─────────────────────────────────────────────────────────────────────────
    {
        "name": "Tansen",
        "name_native": "तानसेन",
        "name_sort": "Tansen",
        "tradition": "Hindustani",
        "era": "16th century",
        "born": 1506, "died": 1589,
        "birth_place": "Gwalior, Madhya Pradesh",
        "nationality": "Indian",
        "biography_short": "The most celebrated musician in Indian history, Tansen was one of the Navaratnas (nine jewels) of Emperor Akbar's court. He is credited with creating several ragas including Miyan ki Todi, Miyan ki Malhar, and Darbari Kanada.",
        "wikidata_id": "Q382133",
        "wikipedia_slug": "Tansen",
        "is_verified": True,
    },
    {
        "name": "Amir Khusrau",
        "name_native": "امیر خسرو",
        "name_sort": "Khusrau, Amir",
        "tradition": "Hindustani",
        "era": "13th–14th century",
        "born": 1253, "died": 1325,
        "birth_place": "Patiyali, Uttar Pradesh",
        "nationality": "Indian",
        "biography_short": "Sufi poet, musician, and scholar credited with creating or popularising the khayal, qawwali, and tarana forms. He is also associated with the invention of the tabla and sitar, though these claims are debated by scholars.",
        "wikidata_id": "Q171922",
        "wikipedia_slug": "Amir_Khusrau",
        "is_verified": True,
    },
    {
        "name": "Vishnu Narayan Bhatkhande",
        "name_native": "विष्णु नारायण भातखंडे",
        "name_sort": "Bhatkhande, Vishnu Narayan",
        "tradition": "Hindustani",
        "era": "19th–20th century",
        "born": 1860, "died": 1936,
        "birth_place": "Mumbai, Maharashtra",
        "nationality": "Indian",
        "biography_short": "Pioneering musicologist who systematised Hindustani classical music, creating the 10-thaat classification system still in use today. He authored the four-volume Hindustani Sangeet Paddhati and founded music schools across India.",
        "wikidata_id": "Q1339065",
        "wikipedia_slug": "Vishnu_Narayan_Bhatkhande",
        "is_verified": True,
    },
    {
        "name": "Vishnu Digambar Paluskar",
        "name_native": "विष्णु दिगंबर पलुसकर",
        "name_sort": "Paluskar, Vishnu Digambar",
        "tradition": "Hindustani",
        "era": "19th–20th century",
        "born": 1872, "died": 1931,
        "birth_place": "Kurundwad, Maharashtra",
        "nationality": "Indian",
        "biography_short": "Pioneering vocalist and reformer who founded the Gandharva Mahavidyalaya in Lahore (1901), the first institution to systematically teach Hindustani classical music. He is credited with bringing classical music to the masses.",
        "wikidata_id": "Q3556547",
        "wikipedia_slug": "Vishnu_Digambar_Paluskar",
        "is_verified": True,
    },
    {
        "name": "Alladiya Khan",
        "name_native": "अल्लादिया खाँ",
        "name_sort": "Khan, Alladiya",
        "tradition": "Hindustani",
        "era": "19th–20th century",
        "born": 1855, "died": 1946,
        "birth_place": "Atrauli, Rajasthan",
        "nationality": "Indian",
        "biography_short": "Founder of the Jaipur-Atrauli gharana, one of the most influential schools of khayal singing. Known for complex taans, intricate rhythmic patterns, and a repertoire of rare ragas.",
        "wikidata_id": "Q4730042",
        "wikipedia_slug": "Alladiya_Khan",
        "is_verified": True,
    },

    # ─────────────────────────────────────────────────────────────────────────
    # PERSIAN CLASSICAL
    # ─────────────────────────────────────────────────────────────────────────
    {
        "name": "Abu Nasr al-Farabi",
        "name_native": "أبو نصر الفارابي",
        "name_sort": "Farabi, al-",
        "tradition": "Persian Classical",
        "era": "9th–10th century",
        "born": 872, "died": 950,
        "birth_place": "Farab, Kazakhstan (historical Khorasan)",
        "nationality": "Kazakh/Persian",
        "biography_short": "Islamic Golden Age polymath and music theorist whose Kitab al-Musiqi al-Kabir (Grand Book of Music) is the most comprehensive medieval treatise on music theory in the Arab-Persian tradition.",
        "wikidata_id": "Q41085",
        "wikipedia_slug": "Al-Farabi",
        "is_verified": True,
    },
    {
        "name": "Safi al-Din al-Urmawi",
        "name_native": "صفي الدين الأرموي",
        "name_sort": "Urmawi, Safi al-Din",
        "tradition": "Persian Classical",
        "era": "13th century",
        "born": 1216, "died": 1294,
        "birth_place": "Urmia, Iran",
        "nationality": "Persian",
        "biography_short": "Celebrated medieval musician and theorist who served at the Abbasid court in Baghdad. His Kitab al-Adwar codified the maqam modal system and 17-tone scale theory that underpins Arabic and Persian classical music.",
        "wikidata_id": "Q713338",
        "wikipedia_slug": "Safi_al-Din_al-Urmawi",
        "is_verified": True,
    },

    # ─────────────────────────────────────────────────────────────────────────
    # ARABIC / OTTOMAN
    # ─────────────────────────────────────────────────────────────────────────
    {
        "name": "Ziryab",
        "name_native": "زرياب",
        "name_sort": "Ziryab",
        "tradition": "Arabic Music",
        "era": "9th century",
        "born": 789, "died": 857,
        "birth_place": "Baghdad, Iraq",
        "nationality": "Arab",
        "biography_short": "Legendary Andalusian-Arab musician, poet, and polymath who revolutionised music in Moorish Spain. Credited with adding a fifth string to the oud and founding a conservatory in Córdoba that influenced the development of European music.",
        "wikidata_id": "Q313275",
        "wikipedia_slug": "Ziryab",
        "is_verified": True,
    },
    {
        "name": "Hammamizade İsmail Dede Efendi",
        "name_native": "Hammamîzâde İsmâil Dede Efendi",
        "name_sort": "Dede Efendi",
        "tradition": "Turkish Classical",
        "era": "18th–19th century",
        "born": 1778, "died": 1846,
        "birth_place": "Istanbul, Turkey",
        "nationality": "Turkish",
        "biography_short": "The greatest composer of the Ottoman classical tradition, Dede Efendi composed over 500 works in the fasıl suite form. A Mevlevi dervish, his compositions bridge the sacred and secular in Ottoman music.",
        "wikidata_id": "Q1593021",
        "wikipedia_slug": "Hammamizade_İsmail_Dede_Efendi",
        "is_verified": True,
    },

    # ─────────────────────────────────────────────────────────────────────────
    # WEST AFRICAN / GRIOT
    # ─────────────────────────────────────────────────────────────────────────
    {
        "name": "Sunjata Keita",
        "name_native": "ߛߎ߬ߣߊ߬ߕߊ ߞߌ߬ߕߊ",
        "name_sort": "Keita, Sunjata",
        "tradition": "Griot Music",
        "era": "13th century",
        "born": 1217, "died": 1255,
        "birth_place": "Niani, Mali Empire",
        "nationality": "Malian",
        "biography_short": "Founder of the Mali Empire, whose heroic deeds are preserved and retold by Mande jeli (griots) through the Sundiata epic — one of the world's great oral literary and musical traditions, still performed today.",
        "wikidata_id": "Q178768",
        "wikipedia_slug": "Sundiata_Keita",
        "is_verified": True,
    },
]


def escape_sql(v: str) -> str:
    return v.replace("'", "''")


def s(v) -> str:
    return f"'{escape_sql(str(v))}'" if v is not None else "NULL"


def year(v) -> str:
    """Format an integer year as a PostgreSQL date literal (Jan 1 of that year)."""
    return f"'{v}-01-01'::date" if v is not None else "NULL"


def build_sql(composers: list[dict]) -> str:
    lines = [
        "-- Key composers seed",
        "-- tradition_id resolved via subquery on musical_traditions.name",
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
        if trad:
            tradition_subq = f"(SELECT id FROM musical_traditions WHERE name = '{escape_sql(trad)}' LIMIT 1)"
        else:
            tradition_subq = "NULL"

        row = (
            f"  (gen_random_uuid(), {s(c['name'])}, {s(c.get('name_native'))}, {s(c.get('name_sort'))}, "
            f"{tradition_subq}, "
            f"{s(c.get('era'))}, {year(c.get('born'))}, {year(c.get('died'))}, "
            f"{s(c.get('birth_place'))}, {s(c.get('nationality'))}, "
            f"{s(c.get('biography_short'))}, {s(c.get('wikidata_id'))}, {s(c.get('wikipedia_slug'))}, "
            f"{'TRUE' if c.get('is_verified') else 'FALSE'}, "
            f"NOW(), NOW())"
        )
        values.append(row)

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (wikidata_id) DO UPDATE SET")
    lines.append("  name            = EXCLUDED.name,")
    lines.append("  name_native     = EXCLUDED.name_native,")
    lines.append("  name_sort       = EXCLUDED.name_sort,")
    lines.append("  tradition_id    = EXCLUDED.tradition_id,")
    lines.append("  era             = EXCLUDED.era,")
    lines.append("  born            = EXCLUDED.born,")
    lines.append("  died            = EXCLUDED.died,")
    lines.append("  birth_place     = EXCLUDED.birth_place,")
    lines.append("  biography_short = EXCLUDED.biography_short,")
    lines.append("  wikipedia_slug  = EXCLUDED.wikipedia_slug,")
    lines.append("  is_verified     = EXCLUDED.is_verified,")
    lines.append("  updated_at      = NOW();")

    return "\n".join(lines)


def main():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    sql = build_sql(COMPOSERS)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    by_tradition: dict[str, int] = {}
    for c in COMPOSERS:
        t = c.get("tradition") or "Other"
        by_tradition[t] = by_tradition.get(t, 0) + 1

    print(f"Seeding {len(COMPOSERS)} composers...")
    for trad, count in sorted(by_tradition.items()):
        print(f"  {trad}: {count}")

    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ {len(COMPOSERS)} composers seeded.")
    print("\nSample:")
    for c in COMPOSERS[:5]:
        era = c.get("era", "")
        print(f"  {c['name']:<40} {era}")


if __name__ == "__main__":
    main()
