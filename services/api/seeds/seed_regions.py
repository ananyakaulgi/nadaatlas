"""
Seed music regions — continents, countries, and cultural sub-regions relevant
to world music traditions on NadaAtlas.

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_regions.py
"""

import os
import subprocess
import sys
import tempfile

REGIONS = [
    # ── South Asia ──────────────────────────────────────────────────────────
    {"name": "North India",         "continent": "Asia", "country_name": "India",       "state": None,               "description": "Heartland of Hindustani classical music; home to the major gharanas of Agra, Jaipur, Kirana, Patiala, and Delhi."},
    {"name": "South India",         "continent": "Asia", "country_name": "India",       "state": None,               "description": "Home of Carnatic classical music, with major centres in Chennai, Mysuru, Thiruvananthapuram, and the Krishna-Godavari delta."},
    {"name": "Bengal",              "continent": "Asia", "country_name": "India",       "state": "West Bengal",      "description": "Distinct musical culture encompassing Rabindra Sangeet, Baul folk tradition, and the Vishnupur gharana of Hindustani music."},
    {"name": "Punjab",              "continent": "Asia", "country_name": "India",       "state": "Punjab",           "description": "Source of Punjabi folk music, bhangra, and the Patiala gharana. Shared cultural heritage with Pakistani Punjab."},
    {"name": "Rajasthan",           "continent": "Asia", "country_name": "India",       "state": "Rajasthan",        "description": "Rich desert folk tradition: Manganiyar and Langa communities, Mewar and Jaipur court music, and the sarangi tradition."},
    {"name": "Kerala",              "continent": "Asia", "country_name": "India",       "state": "Kerala",           "description": "Home of Sopana Sangeetam, Kerala's own classical tradition, alongside Carnatic music and unique percussion ensembles like Panchavadyam."},
    {"name": "Pakistan",            "continent": "Asia", "country_name": "Pakistan",    "state": None,               "description": "Continuation of Hindustani music via qawwali and khayal; major traditions in Lahore and the Punjab heartland."},
    {"name": "Bangladesh",          "continent": "Asia", "country_name": "Bangladesh",  "state": None,               "description": "Baul mystical folk music, Bhatiali river songs, and a shared Hindustani heritage with Bengal."},
    {"name": "Sri Lanka",           "continent": "Asia", "country_name": "Sri Lanka",   "state": None,               "description": "Sinhala and Tamil musical traditions; Carnatic influence in the north, distinct folk forms across the island."},

    # ── Middle East & North Africa ───────────────────────────────────────────
    {"name": "Iran",                "continent": "Asia", "country_name": "Iran",        "state": None,               "description": "Persian classical music (dastgah system), tar, setar, and santur traditions with deep influence across the broader region."},
    {"name": "Turkey",              "continent": "Asia", "country_name": "Turkey",      "state": None,               "description": "Ottoman makam tradition, saz, ney, and the rich Anatolian folk music landscape."},
    {"name": "Egypt",               "continent": "Africa","country_name": "Egypt",      "state": None,               "description": "Centre of Arabic music: maqam tradition, tarab style, and the legacy of Umm Kulthum and Mohamed Abdel Wahab."},
    {"name": "Morocco",             "continent": "Africa","country_name": "Morocco",    "state": None,               "description": "Home of Gnawa spiritual music, Andalusian classical music (Al-Ala), Amazigh folk, and Chaabi pop."},
    {"name": "Algeria",             "continent": "Africa","country_name": "Algeria",    "state": None,               "description": "Chaabi, Rai, and Kabyle Berber traditions; a distinct branch of the Andalusian classical tradition (Sanaa)."},
    {"name": "Iraq",                "continent": "Asia", "country_name": "Iraq",        "state": None,               "description": "Maqam al-Iraqi, one of the most developed vocal maqam traditions; home of the joza fiddle and rich urban classical music."},
    {"name": "Arabian Peninsula",   "continent": "Asia", "country_name": None,          "state": None,               "description": "Covering Saudi Arabia, UAE, Yemen, and Gulf states; sawt, leiwah, and traditional Bedouin and coastal music forms."},
    {"name": "Israel & Palestine",  "continent": "Asia", "country_name": None,          "state": None,               "description": "Intersection of Mizrahi, Sephardic, and Arabic musical traditions alongside diverse immigrant musical cultures."},

    # ── West Africa ──────────────────────────────────────────────────────────
    {"name": "West Africa",         "continent": "Africa","country_name": None,         "state": None,               "description": "Broad region encompassing the griot tradition, kora, balafon, djembe, and the roots of much of the African diaspora's music."},
    {"name": "Mali",                "continent": "Africa","country_name": "Mali",       "state": None,               "description": "Home of the Mande jeli (griot) tradition, kora virtuosos like Toumani Diabaté, and the desert blues of Tinariwen."},
    {"name": "Senegal",             "continent": "Africa","country_name": "Senegal",    "state": None,               "description": "Sabar drumming, mbalax, tama talking drum, and the spiritual music of the Mouride Sufi brotherhood."},
    {"name": "Guinea",              "continent": "Africa","country_name": "Guinea",     "state": None,               "description": "Rich balafon and kora tradition; Bala Faséké lineage and the Conakry school of West African classical music."},
    {"name": "Nigeria",             "continent": "Africa","country_name": "Nigeria",    "state": None,               "description": "Jùjú, Afrobeat, Highlife, and traditional Yoruba, Igbo, and Hausa musical forms; birthplace of Fela Kuti's Afrobeat."},
    {"name": "Ghana",               "continent": "Africa","country_name": "Ghana",      "state": None,               "description": "Highlife, Kpanlogo drumming, fontomfrom royal drums, and the diverse musical traditions of Akan, Ewe, and Ga peoples."},

    # ── East Africa ──────────────────────────────────────────────────────────
    {"name": "East Africa",         "continent": "Africa","country_name": None,         "state": None,               "description": "Taarab coastal music, Swahili song culture, Ethiopian highland traditions, and the horn of Africa's diverse musical forms."},
    {"name": "Ethiopia",            "continent": "Africa","country_name": "Ethiopia",   "state": None,               "description": "Unique pentatonic modal system (qenet), begena lyre, masinko fiddle, and the ceremonial music of the Ethiopian Orthodox church."},
    {"name": "East African Coast",  "continent": "Africa","country_name": None,         "state": None,               "description": "Taarab music of Zanzibar, Mombasa, and Dar es Salaam: a synthesis of Arab, Indian, and African traditions."},

    # ── Sub-Saharan Africa ───────────────────────────────────────────────────
    {"name": "Central Africa",      "continent": "Africa","country_name": None,         "state": None,               "description": "Forest and savanna traditions: likembe thumb piano, Baka polyphonic singing, and the great Congo Basin musical heritage."},
    {"name": "Southern Africa",     "continent": "Africa","country_name": None,         "state": None,               "description": "Mbira (thumb piano) of Zimbabwe, Zulu isicathamiya choral tradition, South African township jazz, and Afrikaner boeremusiek."},

    # ── Europe ───────────────────────────────────────────────────────────────
    {"name": "Iberian Peninsula",   "continent": "Europe","country_name": None,         "state": None,               "description": "Flamenco of Andalusia, Portuguese Fado, and the deep Moorish-influenced musical heritage of Spain and Portugal."},
    {"name": "Balkans",             "continent": "Europe","country_name": None,         "state": None,               "description": "Complex asymmetric rhythms, polyphonic singing (Georgia, Albania), brass band tradition, and the meeting of Ottoman and Slavic musical cultures."},
    {"name": "Eastern Europe",      "continent": "Europe","country_name": None,         "state": None,               "description": "Klezmer, Romani (Gypsy) music, and the rich folk traditions of Poland, Ukraine, Hungary, and Romania."},
    {"name": "Celtic Regions",      "continent": "Europe","country_name": None,         "state": None,               "description": "Irish, Scottish, Welsh, and Breton traditions: uilleann pipes, fiddle, harp, and modal song forms."},

    # ── Americas ─────────────────────────────────────────────────────────────
    {"name": "Cuba",                "continent": "Americas","country_name": "Cuba",     "state": None,               "description": "Son Cubano, Rumba, Danzón, Cha-cha-chá, and Timba: a rich synthesis of African and Spanish musical elements."},
    {"name": "Brazil",              "continent": "Americas","country_name": "Brazil",   "state": None,               "description": "Samba, Bossa Nova, Forró, Baião, Choro, and the vast musical diversity of Afro-Brazilian and indigenous traditions."},
    {"name": "Caribbean",           "continent": "Americas","country_name": None,       "state": None,               "description": "Reggae, Calypso, Steelpan, Dancehall, Zouk, Kompa, and the diverse Afro-Caribbean musical cultures across the islands."},
    {"name": "Andean Region",       "continent": "Americas","country_name": None,       "state": None,               "description": "Andean folk music of Peru, Bolivia, Ecuador, and Chile: charango, quena, zampoña, and the huayno and yaravi genres."},
    {"name": "Mexico",              "continent": "Americas","country_name": "Mexico",   "state": None,               "description": "Mariachi, Son Jarocho, Corrido, and the diverse indigenous and mestizo musical traditions across Mexico's regions."},

    # ── East Asia ────────────────────────────────────────────────────────────
    {"name": "China",               "continent": "Asia", "country_name": "China",       "state": None,               "description": "Guqin, pipa, erhu, and the vast regional traditions: Kunqu opera, Cantonese music, and the Beijing zheng school."},
    {"name": "Japan",               "continent": "Asia", "country_name": "Japan",       "state": None,               "description": "Koto, shakuhachi, biwa, gagaku court music, noh and kabuki theatrical music, and the shamisen tradition."},
    {"name": "Korea",               "continent": "Asia", "country_name": "South Korea", "state": None,               "description": "Jeongganbo notation system, gayageum, haegeum, pansori vocal tradition, and nongak farmer's percussion."},

    # ── Southeast Asia ───────────────────────────────────────────────────────
    {"name": "Indonesia",           "continent": "Asia", "country_name": "Indonesia",   "state": None,               "description": "Gamelan orchestras of Java and Bali, kecak choral music, angklung bamboo ensembles, and the diverse musical cultures across 17,000 islands."},
    {"name": "Southeast Asia",      "continent": "Asia", "country_name": None,          "state": None,               "description": "Pin peat court music of Cambodia, piphat of Thailand and Myanmar, kulintang gong music of the Philippines and Malaysia."},

    # ── Central Asia ─────────────────────────────────────────────────────────
    {"name": "Central Asia",        "continent": "Asia", "country_name": None,          "state": None,               "description": "Dutar, doira, and the classical maqam traditions of Uzbekistan and Tajikistan; Kazakh dombra and Kyrgyz manas epic singing."},
]


def escape_sql(v: str) -> str:
    return v.replace("'", "''")


def s(v) -> str:
    return f"'{escape_sql(v)}'" if v else "NULL"


def build_sql(regions: list[dict]) -> str:
    lines = [
        "-- World music regions seed",
        "INSERT INTO regions (id, name, continent, country_name, state, description, created_at, updated_at)",
        "VALUES",
    ]

    values = []
    for r in regions:
        row = (
            f"  (gen_random_uuid(), {s(r['name'])}, {s(r['continent'])}, "
            f"{s(r['country_name'])}, {s(r['state'])}, {s(r['description'])}, NOW(), NOW())"
        )
        values.append(row)

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (name) DO UPDATE SET")
    lines.append("  continent    = EXCLUDED.continent,")
    lines.append("  country_name = EXCLUDED.country_name,")
    lines.append("  state        = EXCLUDED.state,")
    lines.append("  description  = EXCLUDED.description,")
    lines.append("  updated_at   = NOW();")

    return "\n".join(lines)


def main():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    sql = build_sql(REGIONS)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    by_continent: dict[str, int] = {}
    for r in REGIONS:
        c = r["continent"] or "Other"
        by_continent[c] = by_continent.get(c, 0) + 1

    print(f"Seeding {len(REGIONS)} regions...")
    for continent, count in sorted(by_continent.items()):
        print(f"  {continent}: {count}")

    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ {len(REGIONS)} regions seeded.")


if __name__ == "__main__":
    main()
