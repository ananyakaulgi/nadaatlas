"""
Seed musical traditions into the NadaAtlas database.
Run with:
    DATABASE_URL="postgresql+asyncpg://..." python3 seed_traditions.py
"""
import os
import subprocess
import sys
import tempfile

TRADITIONS = [
    # ── South Asia ────────────────────────────────────────────────────────────
    {
        "name": "Hindustani Classical",
        "name_native": "हिन्दुस्तानी शास्त्रीय संगीत",
        "region": "South Asia",
        "subregion": "North India",
        "origin_period": "13th century",
        "description": "The classical music tradition of northern India, Pakistan, and Bangladesh, centred on raga and tala performed in elaborate improvisation.",
        "wikipedia_slug": "Hindustani_classical_music",
    },
    {
        "name": "Carnatic Classical",
        "name_native": "கர்நாடக இசை",
        "region": "South Asia",
        "subregion": "South India",
        "origin_period": "15th century",
        "description": "The classical music tradition of southern India, characterised by fixed compositions, kriti forms, and virtuosic improvisation within strict frameworks.",
        "wikipedia_slug": "Carnatic_music",
    },
    {
        "name": "Dhrupad",
        "name_native": "ध्रुपद",
        "region": "South Asia",
        "subregion": "North India",
        "origin_period": "15th century",
        "description": "The oldest surviving form of Hindustani classical music, known for its austere, meditative style and extensive alap.",
        "wikipedia_slug": "Dhrupad",
    },
    {
        "name": "Qawwali",
        "name_native": "قوالی",
        "region": "South Asia",
        "subregion": "Pakistan / North India",
        "origin_period": "13th century",
        "description": "Devotional Sufi music of South Asia, performed with call-and-response singing, harmonium, tabla, and clapping.",
        "wikipedia_slug": "Qawwali",
    },
    {
        "name": "Baul",
        "name_native": "বাউল",
        "region": "South Asia",
        "subregion": "Bengal",
        "origin_period": "15th century",
        "description": "Syncretic mystic minstrel tradition of Bengal, blending Sufi and Vaishnava elements with ecstatic song and the one-stringed ektara.",
        "wikipedia_slug": "Baul",
    },
    {
        "name": "Bhajan",
        "name_native": "भजन",
        "region": "South Asia",
        "subregion": "India",
        "origin_period": "Medieval",
        "description": "Hindu devotional song tradition spanning regional styles, sung in praise of deities, especially Vishnu, Krishna, and Rama.",
        "wikipedia_slug": "Bhajan",
    },
    # ── East Asia ─────────────────────────────────────────────────────────────
    {
        "name": "Guqin",
        "name_native": "古琴",
        "region": "East Asia",
        "subregion": "China",
        "origin_period": "Ancient (pre-3rd century BC)",
        "description": "Solo zither tradition of China, considered the instrument of scholars and sages, emphasising meditative, understated expression.",
        "wikipedia_slug": "Guqin",
    },
    {
        "name": "Gagaku",
        "name_native": "雅楽",
        "region": "East Asia",
        "subregion": "Japan",
        "origin_period": "7th century",
        "description": "Imperial court music of Japan, one of the world's oldest surviving orchestral traditions, featuring wind, string, and percussion instruments.",
        "wikipedia_slug": "Gagaku",
    },
    {
        "name": "Noh",
        "name_native": "能",
        "region": "East Asia",
        "subregion": "Japan",
        "origin_period": "14th century",
        "description": "Highly stylised Japanese musical drama combining chant, flute, and percussion in slow, symbolic performance.",
        "wikipedia_slug": "Noh",
    },
    {
        "name": "Pansori",
        "name_native": "판소리",
        "region": "East Asia",
        "subregion": "Korea",
        "origin_period": "17th century",
        "description": "Korean genre of musical storytelling for solo singer and drummer, known for its intense vocal techniques and epic narratives.",
        "wikipedia_slug": "Pansori",
    },
    {
        "name": "Peking Opera",
        "name_native": "京剧",
        "region": "East Asia",
        "subregion": "China",
        "origin_period": "Late 18th century",
        "description": "National opera form of China combining music, vocal performance, mime, acrobatics, and dance with elaborate costumes.",
        "wikipedia_slug": "Peking_opera",
    },
    # ── Southeast Asia ────────────────────────────────────────────────────────
    {
        "name": "Gamelan",
        "name_native": "Gamelan",
        "region": "Southeast Asia",
        "subregion": "Indonesia / Bali / Java",
        "origin_period": "Ancient",
        "description": "Ensemble music tradition of Indonesia centred on tuned percussion — gongs, metallophones, and drums — with regional variations in Bali and Java.",
        "wikipedia_slug": "Gamelan",
    },
    {
        "name": "Pinpeat",
        "name_native": "ពិណពាទ្យ",
        "region": "Southeast Asia",
        "subregion": "Cambodia",
        "origin_period": "Angkor period",
        "description": "Classical ceremonial ensemble of Cambodia used in royal rituals, theatre, and religious ceremonies, featuring gong circles and xylophones.",
        "wikipedia_slug": "Pinpeat",
    },
    {
        "name": "Mor Lam",
        "name_native": "หมอลำ",
        "region": "Southeast Asia",
        "subregion": "Laos / Northeast Thailand",
        "origin_period": "Ancient",
        "description": "Traditional singing style of Laos and Isan Thailand, featuring rapid vocal ornamentation accompanied by the khaen mouth organ.",
        "wikipedia_slug": "Mor_lam",
    },
    {
        "name": "Kulintang",
        "name_native": "Kulintang",
        "region": "Southeast Asia",
        "subregion": "Philippines / Borneo / Sulawesi",
        "origin_period": "Pre-colonial",
        "description": "Gong-chime ensemble tradition of the southern Philippines and Borneo, used in ceremonies and social gatherings.",
        "wikipedia_slug": "Kulintang",
    },
    # ── Central Asia ──────────────────────────────────────────────────────────
    {
        "name": "Maqam",
        "name_native": "مقام",
        "region": "Central Asia",
        "subregion": "Uzbekistan / Tajikistan",
        "origin_period": "Medieval",
        "description": "Classical court music tradition of Central Asia built on large-scale suites (shashmaqam) combining instrumental and vocal sections.",
        "wikipedia_slug": "Shashmaqam",
    },
    {
        "name": "Aqyn",
        "name_native": "Ақын",
        "region": "Central Asia",
        "subregion": "Kazakhstan / Kyrgyzstan",
        "origin_period": "Ancient",
        "description": "Tradition of improvising poet-singers of the Kazakh and Kyrgyz steppe, performing epics and lyric verse to the dombra or komuz.",
        "wikipedia_slug": "Aqyn",
    },
    # ── Middle East & North Africa ────────────────────────────────────────────
    {
        "name": "Maqam (Arabic)",
        "name_native": "مقام عربي",
        "region": "Middle East & North Africa",
        "subregion": "Arab World",
        "origin_period": "Medieval",
        "description": "The Arabic modal system underlying classical and popular music across the Arab world, defining melodic frameworks and emotional character.",
        "wikipedia_slug": "Arabic_maqam",
    },
    {
        "name": "Andalusian Classical",
        "name_native": "الموسيقى الأندلسية",
        "region": "Middle East & North Africa",
        "subregion": "Morocco / Algeria / Tunisia",
        "origin_period": "9th century",
        "description": "Classical tradition descended from medieval Al-Andalus, preserved in North Africa in large-scale nuba suites.",
        "wikipedia_slug": "Andalusian_classical_music",
    },
    {
        "name": "Persian Classical",
        "name_native": "موسیقی کلاسیک ایرانی",
        "region": "Middle East & North Africa",
        "subregion": "Iran",
        "origin_period": "Qajar period (19th century codification)",
        "description": "The classical music of Iran, based on the radif — a canon of melodic modes — performed on instruments such as tar, setar, and santur.",
        "wikipedia_slug": "Persian_traditional_music",
    },
    {
        "name": "Gnawa",
        "name_native": "ڭناوة",
        "region": "Middle East & North Africa",
        "subregion": "Morocco",
        "origin_period": "Medieval",
        "description": "Spiritual music and ritual healing practice of Moroccan Gnawa communities, combining trance rhythms with low-pitched guembri bass and metal castanets.",
        "wikipedia_slug": "Gnawa_music",
    },
    {
        "name": "Chaabi",
        "name_native": "الشعبي",
        "region": "Middle East & North Africa",
        "subregion": "Algeria / Morocco",
        "origin_period": "Early 20th century",
        "description": "Popular urban folk music of Algeria and Morocco blending Andalusian, Bedouin, and Berber elements.",
        "wikipedia_slug": "Cha%27bi_(Morocco)",
    },
    # ── West Africa ───────────────────────────────────────────────────────────
    {
        "name": "Griot",
        "name_native": "Jeli",
        "region": "West Africa",
        "subregion": "Mande-speaking West Africa",
        "origin_period": "13th century",
        "description": "Hereditary oral historian and musician tradition of West Africa; griots preserve genealogies and epic histories through song and kora or balafon.",
        "wikipedia_slug": "Griot",
    },
    {
        "name": "Highlife",
        "name_native": "Highlife",
        "region": "West Africa",
        "subregion": "Ghana / Nigeria",
        "origin_period": "Early 20th century",
        "description": "Guitar- and brass-driven popular music of Ghana and Nigeria blending African rhythms with Western harmonic structure.",
        "wikipedia_slug": "Highlife",
    },
    {
        "name": "Afrobeat",
        "name_native": "Afrobeat",
        "region": "West Africa",
        "subregion": "Nigeria",
        "origin_period": "1970s",
        "description": "Fusion of Yoruba music, jazz, funk, and political commentary pioneered by Fela Kuti, driven by complex polyrhythmic percussion.",
        "wikipedia_slug": "Afrobeat",
    },
    {
        "name": "Mbalax",
        "name_native": "Mbalax",
        "region": "West Africa",
        "subregion": "Senegal / Gambia",
        "origin_period": "1970s",
        "description": "Senegalese popular music driven by the sabar drum, blending Wolof griot tradition with Cuban and jazz influences.",
        "wikipedia_slug": "Mbalax",
    },
    # ── East Africa ───────────────────────────────────────────────────────────
    {
        "name": "Taarab",
        "name_native": "Taarab",
        "region": "East Africa",
        "subregion": "Zanzibar / Tanzania / Kenya",
        "origin_period": "Late 19th century",
        "description": "Swahili sung poetry tradition blending Arab, Indian, and African musical elements, central to Zanzibari weddings and social life.",
        "wikipedia_slug": "Taarab",
    },
    {
        "name": "Ethiopian Orthodox Chant",
        "name_native": "ዜማ",
        "region": "East Africa",
        "subregion": "Ethiopia",
        "origin_period": "4th century",
        "description": "Ancient liturgical chant tradition of the Ethiopian Orthodox Church, attributed to Saint Yared, using the qign, ezl, and araray modes.",
        "wikipedia_slug": "Ethiopian_music",
    },
    # ── Southern Africa ───────────────────────────────────────────────────────
    {
        "name": "Isicathamiya",
        "name_native": "Isicathamiya",
        "region": "Southern Africa",
        "subregion": "South Africa / Zulu",
        "origin_period": "Early 20th century",
        "description": "Zulu a cappella choral tradition of South Africa, performed softly with careful footwork, made internationally known by Ladysmith Black Mambazo.",
        "wikipedia_slug": "Isicathamiya",
    },
    {
        "name": "Mbube",
        "name_native": "Mbube",
        "region": "Southern Africa",
        "subregion": "South Africa",
        "origin_period": "1930s",
        "description": "South African choral style characterised by powerful unison singing and close harmony, precursor to isicathamiya.",
        "wikipedia_slug": "Mbube_(music)",
    },
    # ── Western Europe ────────────────────────────────────────────────────────
    {
        "name": "Flamenco",
        "name_native": "Flamenco",
        "region": "Western Europe",
        "subregion": "Andalusia, Spain",
        "origin_period": "18th century",
        "description": "Art form of Andalusian Romani origin combining cante (song), toque (guitar), baile (dance), and palmas (handclapping) with deep emotional intensity.",
        "wikipedia_slug": "Flamenco",
    },
    {
        "name": "Fado",
        "name_native": "Fado",
        "region": "Western Europe",
        "subregion": "Portugal",
        "origin_period": "Early 19th century",
        "description": "Portuguese song genre characterised by saudade — a bittersweet longing — sung over the Portuguese guitar and viola baixo.",
        "wikipedia_slug": "Fado",
    },
    {
        "name": "Celtic Traditional",
        "name_native": "Ceol Traidisiúnta",
        "region": "Western Europe",
        "subregion": "Ireland / Scotland / Brittany / Wales",
        "origin_period": "Medieval",
        "description": "Folk instrumental and song tradition of the Celtic nations, centred on fiddle, uilleann pipes, tin whistle, and communal session playing.",
        "wikipedia_slug": "Celtic_music",
    },
    {
        "name": "Occitan Troubadour",
        "name_native": "Trobador",
        "region": "Western Europe",
        "subregion": "Southern France",
        "origin_period": "11th–13th century",
        "description": "Medieval courtly lyric poetry and song of southern France in Occitan, foundational to Western secular vocal tradition.",
        "wikipedia_slug": "Troubadour",
    },
    # ── Eastern Europe ────────────────────────────────────────────────────────
    {
        "name": "Byzantine Chant",
        "name_native": "Βυζαντινή μουσική",
        "region": "Eastern Europe",
        "subregion": "Greece / Orthodox Christian world",
        "origin_period": "4th century",
        "description": "Monophonic liturgical chant of the Eastern Orthodox Church, notated in neumes and built on eight modes (octoechos).",
        "wikipedia_slug": "Byzantine_music",
    },
    {
        "name": "Klezmer",
        "name_native": "כלזמר",
        "region": "Eastern Europe",
        "subregion": "Ashkenazi Jewish diaspora",
        "origin_period": "Medieval",
        "description": "Instrumental folk music of Ashkenazi Jewish communities in Eastern Europe, characterised by expressive clarinet and violin mimicking the human voice.",
        "wikipedia_slug": "Klezmer",
    },
    {
        "name": "Bulgarian Folk",
        "name_native": "Българска народна музика",
        "region": "Eastern Europe",
        "subregion": "Bulgaria",
        "origin_period": "Ancient",
        "description": "Folk tradition of Bulgaria known for complex asymmetric rhythms (additive metres), rich polyphony, and the gaida bagpipe.",
        "wikipedia_slug": "Music_of_Bulgaria",
    },
    # ── Northern Europe ───────────────────────────────────────────────────────
    {
        "name": "Sámi Joik",
        "name_native": "Joik",
        "region": "Northern Europe",
        "subregion": "Scandinavia / Sápmi",
        "origin_period": "Ancient",
        "description": "Traditional vocal form of the Sámi people, conceived not as a song about a person or place but as an embodiment of them.",
        "wikipedia_slug": "Joik",
    },
    {
        "name": "Nordic Folk",
        "name_native": "Nordisk folkmusik",
        "region": "Northern Europe",
        "subregion": "Scandinavia",
        "origin_period": "Medieval",
        "description": "Folk traditions of Scandinavia including Swedish polska, Norwegian hardingfele, and Finnish kantele music.",
        "wikipedia_slug": "Nordic_folk_music",
    },
    # ── North America ─────────────────────────────────────────────────────────
    {
        "name": "Blues",
        "name_native": "Blues",
        "region": "North America",
        "subregion": "Southern United States",
        "origin_period": "Late 19th century",
        "description": "African American music tradition originating in the Deep South, built on call-and-response, the 12-bar form, and expressive guitar and voice.",
        "wikipedia_slug": "Blues",
    },
    {
        "name": "Bluegrass",
        "name_native": "Bluegrass",
        "region": "North America",
        "subregion": "Appalachia, United States",
        "origin_period": "1940s",
        "description": "American roots music derived from Appalachian folk and Celtic traditions, featuring banjo, mandolin, fiddle, and close-harmony singing.",
        "wikipedia_slug": "Bluegrass_music",
    },
    {
        "name": "Cajun",
        "name_native": "Cajun",
        "region": "North America",
        "subregion": "Louisiana, United States",
        "origin_period": "18th century",
        "description": "French-Louisiana folk tradition blending Acadian, Creole, and Native American influences around accordion, fiddle, and French lyrics.",
        "wikipedia_slug": "Cajun_music",
    },
    # ── Caribbean ─────────────────────────────────────────────────────────────
    {
        "name": "Son Cubano",
        "name_native": "Son Cubano",
        "region": "Caribbean",
        "subregion": "Cuba",
        "origin_period": "Late 19th century",
        "description": "Cuban genre blending Spanish guitar tradition with African rhythms and call-and-response vocals, foundational to salsa and Latin jazz.",
        "wikipedia_slug": "Son_cubano",
    },
    {
        "name": "Reggae",
        "name_native": "Reggae",
        "region": "Caribbean",
        "subregion": "Jamaica",
        "origin_period": "Late 1960s",
        "description": "Jamaican music genre rooted in ska and rocksteady, characterised by the offbeat rhythmic accent and Rastafarian spiritual themes.",
        "wikipedia_slug": "Reggae",
    },
    {
        "name": "Calypso",
        "name_native": "Calypso",
        "region": "Caribbean",
        "subregion": "Trinidad and Tobago",
        "origin_period": "Early 20th century",
        "description": "Afro-Caribbean music of Trinidad known for improvised satirical lyrics and the annual Carnival competition tradition.",
        "wikipedia_slug": "Calypso_music",
    },
    # ── South America ─────────────────────────────────────────────────────────
    {
        "name": "Tango",
        "name_native": "Tango",
        "region": "South America",
        "subregion": "Argentina / Uruguay",
        "origin_period": "Late 19th century",
        "description": "Dance music of the Río de la Plata region, born in the working-class neighbourhoods of Buenos Aires, combining African, Italian, and Spanish elements.",
        "wikipedia_slug": "Tango_music",
    },
    {
        "name": "Samba",
        "name_native": "Samba",
        "region": "South America",
        "subregion": "Brazil",
        "origin_period": "Early 20th century",
        "description": "Brazilian music and dance with African roots, the heartbeat of Rio Carnival, defined by syncopated rhythms and the surdo bass drum.",
        "wikipedia_slug": "Samba",
    },
    {
        "name": "Bossa Nova",
        "name_native": "Bossa Nova",
        "region": "South America",
        "subregion": "Brazil",
        "origin_period": "Late 1950s",
        "description": "Sophisticated Brazilian genre blending samba rhythms with jazz harmony, developed in Rio de Janeiro's Zona Sul.",
        "wikipedia_slug": "Bossa_nova",
    },
    {
        "name": "Andean Folk",
        "name_native": "Música andina",
        "region": "South America",
        "subregion": "Andes (Peru / Bolivia / Ecuador)",
        "origin_period": "Pre-Columbian",
        "description": "Indigenous and mestizo music of the Andean highlands, featuring panpipes, charango, and pentatonic melodies.",
        "wikipedia_slug": "Andean_music",
    },
    {
        "name": "Cumbia",
        "name_native": "Cumbia",
        "region": "South America",
        "subregion": "Colombia",
        "origin_period": "17th century",
        "description": "Afro-Colombian coastal music blending African, indigenous, and Spanish elements, now a pan-Latin American popular genre.",
        "wikipedia_slug": "Cumbia",
    },
    # ── Oceania ───────────────────────────────────────────────────────────────
    {
        "name": "Aboriginal Australian",
        "name_native": "Yidaki",
        "region": "Oceania",
        "subregion": "Australia",
        "origin_period": "Ancient (40,000+ years)",
        "description": "Indigenous music traditions of Australia, including didgeridoo drone, songlines, and ceremonial song cycles tied to land and ancestors.",
        "wikipedia_slug": "Music_of_Australia",
    },
    {
        "name": "Polynesian Traditional",
        "name_native": "Hiva",
        "region": "Oceania",
        "subregion": "Polynesia",
        "origin_period": "Ancient",
        "description": "Traditional music and dance of the Polynesian peoples (Samoa, Tonga, Hawaii, Māori), featuring choral song, percussion, and ritual performance.",
        "wikipedia_slug": "Music_of_Polynesia",
    },
]


def escape_sql(s):
    if s is None:
        return "NULL"
    return "'" + str(s).replace("'", "''") + "'"


def generate_sql(traditions):
    lines = [
        "-- NadaAtlas musical traditions seed",
        "INSERT INTO musical_traditions (id, name, name_native, region, subregion, description, origin_period, wikipedia_slug, is_active, created_at, updated_at)",
        "VALUES",
    ]
    values = []
    for t in traditions:
        values.append(
            f"  (gen_random_uuid(), {escape_sql(t['name'])}, {escape_sql(t.get('name_native'))}, "
            f"{escape_sql(t['region'])}, {escape_sql(t.get('subregion'))}, "
            f"{escape_sql(t.get('description'))}, {escape_sql(t.get('origin_period'))}, "
            f"{escape_sql(t.get('wikipedia_slug'))}, true, now(), now())"
        )
    lines.append(",\n".join(values))
    lines += [
        "ON CONFLICT (name) DO UPDATE SET",
        "  name_native    = COALESCE(EXCLUDED.name_native,    musical_traditions.name_native),",
        "  region         = EXCLUDED.region,",
        "  subregion      = COALESCE(EXCLUDED.subregion,      musical_traditions.subregion),",
        "  description    = COALESCE(EXCLUDED.description,    musical_traditions.description),",
        "  origin_period  = COALESCE(EXCLUDED.origin_period,  musical_traditions.origin_period),",
        "  wikipedia_slug = COALESCE(EXCLUDED.wikipedia_slug, musical_traditions.wikipedia_slug),",
        "  updated_at     = now()",
        ";",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable is required.", file=sys.stderr)
        sys.exit(1)

    # Swap asyncpg driver for psql-compatible URL
    psql_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    sql = generate_sql(TRADITIONS)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        sql_path = f.name

    print(f"Seeding {len(TRADITIONS)} musical traditions...")
    result = subprocess.run(
        ["psql", psql_url, "-f", sql_path],
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print("STDERR:", result.stderr.strip(), file=sys.stderr)
        sys.exit(1)

    print(f"✅ Done — {len(TRADITIONS)} traditions seeded.")
