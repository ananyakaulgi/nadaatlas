"""
Seed music genres — broad listener-facing categories.
Genre = what a listener would call it (Classical, Jazz, Reggae).
Tradition = cultural/historical context (Hindustani, Carnatic, Gnawa).

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_genres.py
"""

import os
import re
import subprocess
import sys
import tempfile

GENRES = [
    # ── Indian Classical ─────────────────────────────────────────────────────
    ("Hindustani Classical",    "hindustani-classical",     "North Indian classical music tradition encompassing khayal, dhrupad, thumri, and instrumental forms."),
    ("Carnatic Classical",      "carnatic-classical",        "South Indian classical music tradition encompassing kriti, varnam, ragam-tanam-pallavi, and concert forms."),

    # ── Western Classical ─────────────────────────────────────────────────────
    ("Classical",               "classical",                 "Western European art music tradition from the medieval period through the 20th century."),
    ("Opera",                   "opera",                     "Western staged dramatic work combining music, singing, and orchestral performance."),
    ("Chamber Music",           "chamber-music",             "Western classical music written for a small ensemble, typically performed without a conductor."),

    # ── Jazz & Blues ─────────────────────────────────────────────────────────
    ("Jazz",                    "jazz",                      "African-American music tradition originating in New Orleans, characterised by improvisation, syncopation, and swing."),
    ("Blues",                   "blues",                     "African-American genre rooted in field hollers, spirituals, and work songs; foundation of much of modern popular music."),
    ("Soul",                    "soul",                      "Music combining gospel, rhythm and blues, and jazz, emphasising emotional expressiveness and vocal technique."),

    # ── Afro-Caribbean & Latin ────────────────────────────────────────────────
    ("Reggae",                  "reggae",                    "Jamaican music characterised by offbeat rhythms, Rastafarian themes, and a strong bass-heavy sound."),
    ("Salsa",                   "salsa",                     "Cuban-derived dance music with roots in son cubano; a dominant form across Latin America and urban Latino communities."),
    ("Afrobeat",                "afrobeat",                  "Genre pioneered by Fela Kuti fusing Yoruba music, jazz, and funk with socially conscious lyrics."),
    ("Bossa Nova",              "bossa-nova",                "Brazilian genre blending samba rhythms with jazz harmonies; emerged in Rio de Janeiro in the late 1950s."),
    ("Samba",                   "samba",                     "Brazilian music and dance genre with African roots; the defining music of Rio Carnival."),

    # ── World / Roots ─────────────────────────────────────────────────────────
    ("World Music",             "world-music",               "Broad umbrella term for non-Western popular and traditional music; often used for cross-cultural fusion."),
    ("Folk",                    "folk",                      "Traditional music passed down through oral tradition within a community or region."),
    ("Traditional",             "traditional",               "Music closely tied to the customs and practices of a specific cultural community."),
    ("Devotional",              "devotional",                "Music composed or performed for religious or spiritual purposes across any tradition."),
    ("Sufi",                    "sufi",                      "Devotional music associated with Islamic mysticism; includes qawwali, sama, and related forms."),
    ("Qawwali",                 "qawwali",                   "Sufi devotional music of South Asia, made internationally known by Nusrat Fateh Ali Khan."),
    ("Gospel",                  "gospel",                    "Christian devotional music rooted in African-American church traditions."),
    ("Spiritual",               "spiritual",                 "African-American religious folk songs originating in the era of slavery."),
    ("Bhajan",                  "bhajan",                    "Hindu devotional songs typically sung in a call-and-response style."),
    ("Kirtan",                  "kirtan",                    "Devotional chanting practice in Hindu and Sikh traditions, often participatory."),

    # ── Middle Eastern ────────────────────────────────────────────────────────
    ("Arabic Music",            "arabic-music",              "Classical and popular music of the Arab world, characterised by the maqam modal system."),
    ("Persian Classical",       "persian-classical",         "Classical music of Iran based on the dastgah modal system, featuring tar, setar, and santour."),
    ("Gnawa",                   "gnawa",                     "Moroccan spiritual music of sub-Saharan origin, performed in healing ceremonies using guembri and krakeb."),
    ("Flamenco",                "flamenco",                  "Andalusian art form encompassing song (cante), guitar (toque), and dance (baile); deeply influenced by Moorish and Romani traditions."),

    # ── African ───────────────────────────────────────────────────────────────
    ("Highlife",                "highlife",                  "West African genre originating in Ghana and Nigeria, blending indigenous rhythms with Western brass and guitar."),
    ("Mbalax",                  "mbalax",                    "Senegalese popular music fusing sabar drumming with Cuban rhythms and Wolof griot traditions."),
    ("Griot Music",             "griot-music",               "Music of the West African jeli (griot) storyteller-musician tradition; encompasses kora, balafon, and vocal praise music."),
    ("Gamelan",                 "gamelan",                   "Ensemble music of Java and Bali built around bronze percussion instruments; a defining art form of Indonesian culture."),

    # ── East Asian ───────────────────────────────────────────────────────────
    ("Chinese Classical",       "chinese-classical",         "Traditional and classical music of China including guqin, pipa, erhu, and regional operatic forms."),
    ("Japanese Classical",      "japanese-classical",        "Traditional music of Japan including koto, shakuhachi, gagaku court music, and theatrical forms."),

    # ── Popular ───────────────────────────────────────────────────────────────
    ("Pop",                     "pop",                       "Broad genre of popular music characterised by catchy melodies, verse-chorus structure, and mass appeal."),
    ("Rock",                    "rock",                      "Genre rooted in 1950s rock and roll, characterised by electric guitar, bass, and drums."),
    ("Electronic",              "electronic",                "Music produced primarily with electronic instruments and technology."),
    ("Hip-Hop",                 "hip-hop",                   "African-American musical and cultural form encompassing rap, DJing, beatboxing, and sampling."),
    ("R&B",                     "r-and-b",                   "Rhythm and blues; a broad genre of African-American popular music with roots in jazz, gospel, and blues."),
    ("Country",                 "country",                   "American popular music rooted in Southern folk, Appalachian, and western cowboy traditions."),
    ("Bluegrass",               "bluegrass",                 "American roots music derived from the music of Scots-Irish and other European immigrants to Appalachia."),
    ("Fado",                    "fado",                      "Portuguese music characterised by mournful tunes and lyrics, often with themes of longing (saudade)."),
]


def escape_sql(v: str) -> str:
    return v.replace("'", "''")


def s(v) -> str:
    return f"'{escape_sql(v)}'" if v else "NULL"


def build_sql(genres) -> str:
    lines = [
        "-- Music genres seed",
        "INSERT INTO genres (id, name, slug, description, created_at, updated_at)",
        "VALUES",
    ]

    values = []
    for name, slug, desc in genres:
        row = f"  (gen_random_uuid(), {s(name)}, {s(slug)}, {s(desc)}, NOW(), NOW())"
        values.append(row)

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (name) DO UPDATE SET")
    lines.append("  slug        = EXCLUDED.slug,")
    lines.append("  description = EXCLUDED.description,")
    lines.append("  updated_at  = NOW();")

    return "\n".join(lines)


def main():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    sql = build_sql(GENRES)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    print(f"Seeding {len(GENRES)} genres...")
    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ {len(GENRES)} genres seeded.")
    print("\nSample:")
    for name, slug, _ in GENRES[:6]:
        print(f"  {name:<28} [{slug}]")


if __name__ == "__main__":
    main()
