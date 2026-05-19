-- NādaAtlas — Core World Music Traditions Seed
-- Safe to re-run: ON CONFLICT (name) DO NOTHING skips existing rows.

INSERT INTO musical_traditions (id, name, region, subregion, description, origin_period, is_active)
VALUES

-- ── South Asia ──────────────────────────────────────────────────────────────
(gen_random_uuid(), 'Hindustani Classical',  'South Asia', 'North India',      'Classical music tradition of North India rooted in ancient Hindu scriptures and enriched by Persian influence under the Mughal empire.',         '13th century',   true),
(gen_random_uuid(), 'Carnatic',              'South Asia', 'South India',      'Classical music tradition of South India, one of the oldest in the world, with highly structured melodic and rhythmic systems.',                   '15th century',   true),
(gen_random_uuid(), 'Dhrupad',               'South Asia', 'North India',      'The oldest surviving form of Hindustani classical music, characterised by slow, meditative exposition of ragas and complex rhythmic cycles.',        '15th century',   true),
(gen_random_uuid(), 'Thumri',                'South Asia', 'North India',      'Semi-classical vocal form associated with devotional poetry, expressiveness, and romantic themes; closely linked to the Braj Bhasha language.',     '19th century',   true),
(gen_random_uuid(), 'Ghazal',                'South Asia', 'North India',      'Lyrical poetry sung in a call-and-response couplet structure; deeply connected to Sufi mysticism and Urdu literary tradition.',                   '12th century',   true),
(gen_random_uuid(), 'Qawwali',               'South Asia', 'Pakistan/India',   'Devotional Sufi music performed in shrines and gatherings; ecstatic in nature, aimed at inducing a state of spiritual union with the divine.',     '13th century',   true),
(gen_random_uuid(), 'Baul',                  'South Asia', 'Bengal',           'Syncretic folk-spiritual tradition of Bengal blending Hindu Vaishnava and Sufi elements; performed by wandering mystic minstrels.',               '15th century',   true),
(gen_random_uuid(), 'Bhajan & Kirtan',       'South Asia', 'India-wide',       'Hindu devotional music traditions; Bhajan are individual contemplative songs, Kirtan are congregational call-and-response chants.',                'Ancient',        true),

-- ── East Asia ───────────────────────────────────────────────────────────────
(gen_random_uuid(), 'Chinese Classical',     'East Asia',  'China',            'Ancient instrumental and vocal traditions rooted in Confucian philosophy; instruments include guqin, pipa, and erhu.',                            'Ancient',        true),
(gen_random_uuid(), 'Japanese Gagaku',       'East Asia',  'Japan',            'Oldest surviving orchestral music tradition in the world, performed at the Japanese imperial court since the 7th century.',                       '7th century',    true),
(gen_random_uuid(), 'Korean Traditional',    'East Asia',  'Korea',            'Encompasses court music (jeongganbo), folk music, and pansori storytelling; core instruments include gayageum, haegeum, and janggu.',             'Ancient',        true),
(gen_random_uuid(), 'Mongolian Throat Singing','East Asia', 'Mongolia',        'Khoomei and its variants allow a single vocalist to produce multiple pitches simultaneously by manipulating resonances in the vocal tract.',       'Ancient',        true),

-- ── Southeast Asia ──────────────────────────────────────────────────────────
(gen_random_uuid(), 'Gamelan',               'Southeast Asia', 'Indonesia',    'Percussion-dominated ensemble tradition of Java and Bali; integral to ceremonial, theatrical, and spiritual life in Indonesian culture.',         '8th century',    true),
(gen_random_uuid(), 'Thai Piphat',           'Southeast Asia', 'Thailand',     'Classical Thai ensemble featuring xylophones, gongs, and oboe; performed at royal ceremonies, classical dance, and Khon masked drama.',           'Ancient',        true),
(gen_random_uuid(), 'Vietnamese Ca Trù',     'Southeast Asia', 'Vietnam',      'UNESCO-recognised chamber music tradition involving a female singer, a zither, and drums; historically performed for the royal court.',           '15th century',   true),
(gen_random_uuid(), 'Philippine Kulintang',  'Southeast Asia', 'Philippines',  'Gong-chime music tradition of indigenous Moro peoples; distinct from Javanese gamelan, with unique improvisatory and rhythmic character.',         'Pre-colonial',   true),

-- ── Central Asia ────────────────────────────────────────────────────────────
(gen_random_uuid(), 'Afghan Rubab',          'Central Asia', 'Afghanistan',    'Classical music centred on the rubab lute; foundational to the music of Afghanistan and a precursor to the Hindustani sitar tradition.',          'Ancient',        true),
(gen_random_uuid(), 'Azerbaijani Mugham',    'Central Asia', 'Azerbaijan',     'Modal classical tradition combining improvisation, poetry, and melody; UNESCO-recognised as part of the intangible cultural heritage of humanity.', '15th century',   true),

-- ── Middle East & North Africa ──────────────────────────────────────────────
(gen_random_uuid(), 'Arabic Maqam',          'Middle East & North Africa', 'Arab world', 'Modal music system spanning Arabic-speaking countries; maqamat define the melodic and emotional character of each composition.',      'Medieval',       true),
(gen_random_uuid(), 'Persian Classical',     'Middle East & North Africa', 'Iran',       'Radif-based modal system of Iran with 12 dastgahs; emphasises improvisation and a deep connection between poetry and melody.',         'Ancient',        true),
(gen_random_uuid(), 'Turkish Makam',         'Middle East & North Africa', 'Turkey',     'Ottoman and Turkish classical music tradition using a refined system of makam modes; performed with instruments like oud and ney.',      'Medieval',       true),
(gen_random_uuid(), 'Gnawa',                 'Middle East & North Africa', 'Morocco',    'Ritual and trance music of Moroccan Gnawa communities with West African roots; ceremonies use the guembri bass lute and metal qraqeb.', '12th century',   true),

-- ── West Africa ─────────────────────────────────────────────────────────────
(gen_random_uuid(), 'West African Griot',    'West Africa', 'Mali/Senegal',    'Oral historian-musician tradition of the Mandé people; griots preserve genealogy, history, and social memory through the kora and balafon.',     'Ancient',        true),
(gen_random_uuid(), 'Mbalax',                'West Africa', 'Senegal',         'Urban dance music of Senegal blending traditional sabar drumming with jazz, Latin, and rock; popularised globally by Youssou N''Dour.',           '1970s',          true),

-- ── East & Southern Africa ──────────────────────────────────────────────────
(gen_random_uuid(), 'Ethiopian Traditional', 'East Africa',     'Ethiopia',   'Ancient music culture using the pentatonic qenet modal system; links sacred and secular traditions through instruments like the masenqo and krar.', 'Ancient',       true),
(gen_random_uuid(), 'South African Mbaqanga','Southern Africa', 'South Africa','Township jive style blending Zulu musical elements with electric guitar; a cornerstone of South African urban identity since the 1960s.',        '1960s',          true),
(gen_random_uuid(), 'Congolese Soukous',     'Central Africa',  'Congo',       'Rumba-derived guitar-pop tradition from the Congo; characterised by fast, intricate guitar patterns and became the dominant pan-African pop style.','1960s',         true),

-- ── Latin America & Caribbean ───────────────────────────────────────────────
(gen_random_uuid(), 'Brazilian Samba',       'South America', 'Brazil',        'Syncretic Afro-Brazilian music and dance form rooted in Candomblé rhythms; the heartbeat of Rio Carnival and Brazilian national identity.',      'Early 20th century', true),
(gen_random_uuid(), 'Argentine Tango',       'South America', 'Argentina',     'Music and dance form born in the port communities of Buenos Aires blending African, European, and indigenous elements; UNESCO-listed.',           'Late 19th century',  true),
(gen_random_uuid(), 'Andean',                'South America', 'Andes region',  'Music of indigenous and mestizo Andean communities using pan flutes, charango, and bombo; rooted in pre-Columbian ceremonial traditions.',        'Pre-colonial',       true),
(gen_random_uuid(), 'Colombian Cumbia',      'South America', 'Colombia',      'Afro-Colombian coastal tradition blending Indigenous, African, and Spanish elements; foundational to Latin popular music across the Americas.',   '17th century',       true),
(gen_random_uuid(), 'Cuban Son',             'Caribbean',     'Cuba',          'Fusion of African rhythm and Spanish melody that became the basis of salsa; originated in Oriente province in the late 19th century.',            'Late 19th century',  true),
(gen_random_uuid(), 'Reggae',                'Caribbean',     'Jamaica',       'Jamaican music rooted in ska and rocksteady, defined by off-beat rhythms and socially conscious lyrics; globally spread through Bob Marley.',      '1960s',              true),

-- ── Europe ──────────────────────────────────────────────────────────────────
(gen_random_uuid(), 'Flamenco',              'Western Europe',  'Spain',        'Andalusian art form combining cante (song), toque (guitar), baile (dance), and jaleo (vocalisation); deeply shaped by Romani, Moorish, and Jewish influences.', '18th century', true),
(gen_random_uuid(), 'Fado',                  'Western Europe',  'Portugal',     'Portuguese song tradition expressing saudade — melancholic longing; UNESCO-listed; originated in Lisbon taverns in the early 19th century.',      'Early 19th century', true),
(gen_random_uuid(), 'Celtic',                'Western Europe',  'British Isles','Traditional music of Ireland, Scotland, Wales, and Brittany; characterised by modal melodies, fiddle, pipes, and oral transmission.',            'Ancient',            true),
(gen_random_uuid(), 'Nordic Folk',           'Northern Europe', 'Scandinavia',  'Folk music traditions of Norway, Sweden, Denmark, and Finland; includes hardanger fiddle, nyckelharpa, and kalevala runo singing.',              'Ancient',            true),
(gen_random_uuid(), 'Sámi Joik',             'Northern Europe', 'Sápmi',        'Traditional Sámi vocal form; a joik is not merely a song but a personal dedication — it doesn''t describe a subject, it embodies them.',        'Ancient',            true),
(gen_random_uuid(), 'Balkan',                'Southern Europe', 'Balkans',      'Diverse folk traditions of Southeast Europe united by additive rhythms, modal melodies, and polyphonic singing; encompasses Serbian, Bulgarian, Albanian, and Greek styles.', 'Ancient', true),
(gen_random_uuid(), 'Romani',                'Eastern Europe',  'Europe-wide',  'Music of the Romani diaspora spanning flamenco, Hungarian verbunkos, Balkan brass, and jazz manouche; characterised by ornamentation and improvisation.', 'Medieval', true),
(gen_random_uuid(), 'Gregorian Chant',       'Western Europe',  'Europe-wide',  'Monophonic sacred vocal music of the Roman Catholic Church; the oldest notated musical tradition in the Western world.',                         '9th century',        true),

-- ── North America ───────────────────────────────────────────────────────────
(gen_random_uuid(), 'Blues',                 'North America', 'Southern USA',  'African American vocal and instrumental form rooted in field hollers, spirituals, and work songs; foundation of rock, jazz, and R&B.',            'Late 19th century',  true),
(gen_random_uuid(), 'Jazz',                  'North America', 'New Orleans',   'African American synthesis of blues, ragtime, and European harmony; defined by improvisation and swing rhythm; born in New Orleans c.1900.',       'Early 20th century', true),
(gen_random_uuid(), 'Bluegrass',             'North America', 'Appalachian',   'High-energy string band music of Appalachia blending Scottish-Irish folk with African American blues and jazz; known for virtuosic instrumental breaks.', '1940s',        true),
(gen_random_uuid(), 'Native American',       'North America', 'North America', 'Diverse musical traditions of Indigenous peoples of North America; ceremonial songs, drumming circles, and flute music tied to land, spirit, and community.', 'Ancient', true),

-- ── Oceania ─────────────────────────────────────────────────────────────────
(gen_random_uuid(), 'Aboriginal Australian', 'Oceania', 'Australia',          'World''s oldest continuous musical tradition; songlines encode maps of the landscape; didgeridoo and clapsticks accompany ceremonial song.',       'Ancient (60,000+ years)', true),
(gen_random_uuid(), 'Māori Waiata',          'Oceania', 'New Zealand',        'Traditional vocal music of the Māori people of Aotearoa; waiata are performed at ceremonies, funerals, and as greetings; closely tied to whakapapa (genealogy).', 'Pre-colonial', true),
(gen_random_uuid(), 'Hawaiian',              'Oceania', 'Hawaii',             'Music of Native Hawaiians combining ancient chant (oli) and hula with the ukulele and slack-key guitar traditions that emerged after Polynesian contact.', 'Ancient',    true),

-- ── Devotional / Cross-regional ─────────────────────────────────────────────
(gen_random_uuid(), 'Buddhist Chanting',     'East Asia', 'Asia-wide',        'Sacred vocal traditions of Theravada, Mahayana, and Vajrayana Buddhism; includes Tibetan overtone chanting, Japanese shomyo, and Thai pali recitation.', 'Ancient', true)

ON CONFLICT (name) DO NOTHING;
