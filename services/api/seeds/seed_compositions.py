"""
Seed ~60 landmark compositions across global traditions.

Composer lookup: by wikidata_id
Tradition lookup: by name
Raga lookup:      by name + tradition column
Tala lookup:      by name

Idempotent: uses WHERE NOT EXISTS on (title, composer_id) so re-runs
are safe even without a unique constraint on the compositions table.

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_compositions.py
"""

import os
import subprocess
import sys
import tempfile

# ─────────────────────────────────────────────────────────────────────────────
# Composition data
# Keys:
#   title, title_native, composer_wikidata, tradition, composition_type,
#   raga (name), raga_tradition (carnatic|hindustani), tala (name),
#   maqam, language, year_composed, description, wikipedia_slug
# ─────────────────────────────────────────────────────────────────────────────
COMPOSITIONS = [

    # ═════════════════════════════════════════════════════════════════════════
    # WESTERN CLASSICAL — BAROQUE
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Brandenburg Concerto No. 1 in F major",
        "composer_wikidata": "Q1339",
        "tradition": "Western Classical",
        "composition_type": "concerto",
        "language": "Instrumental",
        "year_composed": 1721,
        "description": (
            "The first of Bach's six Brandenburg Concertos, scored for an unusual "
            "combination including violino piccolo. Dedicated to Margrave Christian "
            "Ludwig of Brandenburg-Schwedt."
        ),
        "wikipedia_slug": "Brandenburg_concertos",
    },
    {
        "title": "Brandenburg Concerto No. 5 in D major",
        "composer_wikidata": "Q1339",
        "tradition": "Western Classical",
        "composition_type": "concerto",
        "language": "Instrumental",
        "year_composed": 1721,
        "description": (
            "The fifth Brandenburg Concerto features the harpsichord as a solo "
            "instrument — considered the first keyboard concerto in history. "
            "The extended harpsichord cadenza in the first movement is groundbreaking."
        ),
        "wikipedia_slug": "Brandenburg_concertos",
    },
    {
        "title": "Mass in B Minor",
        "composer_wikidata": "Q1339",
        "tradition": "Western Classical",
        "composition_type": "mass",
        "language": "Latin",
        "year_composed": 1749,
        "description": (
            "Bach's monumental sacred work assembled across the final decades of his life. "
            "Considered one of the greatest choral works ever written, it encompasses "
            "Kyrie, Gloria, Credo, Sanctus, and Agnus Dei."
        ),
        "wikipedia_slug": "Mass_in_B_minor",
    },
    {
        "title": "The Well-Tempered Clavier, Book I",
        "title_native": "Das Wohltemperierte Klavier",
        "composer_wikidata": "Q1339",
        "tradition": "Western Classical",
        "composition_type": "prelude",
        "language": "Instrumental",
        "year_composed": 1722,
        "description": (
            "A collection of 24 preludes and fugues in all major and minor keys, "
            "demonstrating the equal temperament tuning system. The opening Prelude "
            "in C major is among the most recognised pieces in the repertoire."
        ),
        "wikipedia_slug": "The_Well-Tempered_Clavier",
    },
    {
        "title": "Toccata and Fugue in D minor",
        "composer_wikidata": "Q1339",
        "tradition": "Western Classical",
        "composition_type": "toccata",
        "language": "Instrumental",
        "year_composed": 1704,
        "description": (
            "Bach's most famous organ work, opening with the dramatic descending "
            "toccata motif. A defining icon of Baroque organ music and Western "
            "classical culture."
        ),
        "wikipedia_slug": "Toccata_and_Fugue_in_D_minor,_BWV_565",
    },
    {
        "title": "The Four Seasons",
        "title_native": "Le quattro stagioni",
        "composer_wikidata": "Q1340",
        "tradition": "Western Classical",
        "composition_type": "concerto",
        "language": "Instrumental",
        "year_composed": 1725,
        "description": (
            "Four violin concertos depicting spring, summer, autumn, and winter, "
            "each accompanied by a descriptive sonnet. Vivaldi's most famous works "
            "and among the most performed pieces in classical music."
        ),
        "wikipedia_slug": "The_Four_Seasons_(Vivaldi)",
    },
    {
        "title": "Messiah",
        "composer_wikidata": "Q7302",
        "tradition": "Western Classical",
        "composition_type": "oratorio",
        "language": "English",
        "year_composed": 1741,
        "description": (
            "Handel's masterpiece oratorio on the life of Jesus Christ, compiled "
            "from biblical texts. The Hallelujah chorus is among the most celebrated "
            "moments in Western choral music."
        ),
        "wikipedia_slug": "Messiah_(Handel)",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # WESTERN CLASSICAL — CLASSICAL PERIOD
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Symphony No. 40 in G minor",
        "composer_wikidata": "Q254",
        "tradition": "Western Classical",
        "composition_type": "symphony",
        "language": "Instrumental",
        "year_composed": 1788,
        "description": (
            "One of only two minor-key symphonies Mozart wrote, the Symphony No. 40 "
            "is famous for its urgent, searching first movement. It conveys an emotional "
            "intensity unusual for the Classical period."
        ),
        "wikipedia_slug": "Symphony_No._40_(Mozart)",
    },
    {
        "title": "Don Giovanni",
        "composer_wikidata": "Q254",
        "tradition": "Western Classical",
        "composition_type": "opera",
        "language": "Italian",
        "year_composed": 1787,
        "description": (
            "Mozart's opera on the legendary seducer Don Giovanni, blending comedy "
            "and tragedy. Considered by many the greatest opera ever written, "
            "it premiered in Prague to immediate acclaim."
        ),
        "wikipedia_slug": "Don_Giovanni",
    },
    {
        "title": "Requiem in D minor",
        "composer_wikidata": "Q254",
        "tradition": "Western Classical",
        "composition_type": "requiem",
        "language": "Latin",
        "year_composed": 1791,
        "description": (
            "Left unfinished at Mozart's death at 35, the Requiem was completed by "
            "his student Franz Xaver Süssmayr. One of the most poignant works in "
            "classical music, surrounded by mystery and legend."
        ),
        "wikipedia_slug": "Requiem_(Mozart)",
    },
    {
        "title": "Eine kleine Nachtmusik",
        "composer_wikidata": "Q254",
        "tradition": "Western Classical",
        "composition_type": "serenade",
        "language": "Instrumental",
        "year_composed": 1787,
        "description": (
            "A serenade for string quartet and bass in four movements, its cheerful "
            "opening is among the most recognisable in all classical music. The title "
            "translates as 'A Little Night Music'."
        ),
        "wikipedia_slug": "Eine_kleine_Nachtmusik",
    },
    {
        "title": "Symphony No. 94 in G major \"Surprise\"",
        "composer_wikidata": "Q7349",
        "tradition": "Western Classical",
        "composition_type": "symphony",
        "language": "Instrumental",
        "year_composed": 1792,
        "description": (
            "One of Haydn's London symphonies, nicknamed 'Surprise' for the "
            "sudden fortissimo chord in the otherwise quiet slow movement, "
            "reportedly to wake sleeping audience members."
        ),
        "wikipedia_slug": "Symphony_No._94_(Haydn)",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # WESTERN CLASSICAL — ROMANTIC
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Symphony No. 9 in D minor",
        "composer_wikidata": "Q255",
        "tradition": "Western Classical",
        "composition_type": "symphony",
        "language": "Instrumental/German",
        "year_composed": 1824,
        "description": (
            "Beethoven's final symphony, completed while deaf, introduces a choral "
            "finale setting Schiller's Ode to Joy. It transformed the symphony form "
            "forever and is now the anthem of the European Union."
        ),
        "wikipedia_slug": "Symphony_No._9_(Beethoven)",
    },
    {
        "title": "Piano Sonata No. 14 \"Moonlight\"",
        "composer_wikidata": "Q255",
        "tradition": "Western Classical",
        "composition_type": "sonata",
        "language": "Instrumental",
        "year_composed": 1801,
        "description": (
            "Beethoven's most famous piano sonata, the 'Moonlight' opens with an "
            "hypnotic slow movement of triplet arpeggios under a singing melody. "
            "The nickname was coined by a critic after Beethoven's death."
        ),
        "wikipedia_slug": "Piano_Sonata_No._14_(Beethoven)",
    },
    {
        "title": "Für Elise",
        "composer_wikidata": "Q255",
        "tradition": "Western Classical",
        "composition_type": "bagatelle",
        "language": "Instrumental",
        "year_composed": 1810,
        "description": (
            "A short piano piece in A minor, one of the most immediately recognisable "
            "works in classical music. Discovered after Beethoven's death, the identity "
            "of 'Elise' remains disputed by musicologists."
        ),
        "wikipedia_slug": "Für_Elise",
    },
    {
        "title": "Symphony No. 1 in C minor",
        "composer_wikidata": "Q7294",
        "tradition": "Western Classical",
        "composition_type": "symphony",
        "language": "Instrumental",
        "year_composed": 1876,
        "description": (
            "Brahms spent 14 years completing his first symphony, acutely aware it "
            "would be compared to Beethoven's. Conductor Hans von Bülow called it "
            "'Beethoven's Tenth'. The finale's main theme echoes Beethoven's Ninth."
        ),
        "wikipedia_slug": "Symphony_No._1_(Brahms)",
    },
    {
        "title": "Hungarian Dances",
        "title_native": "Ungarische Tänze",
        "composer_wikidata": "Q7294",
        "tradition": "Western Classical",
        "composition_type": "dance",
        "language": "Instrumental",
        "year_composed": 1869,
        "description": (
            "Twenty-one lively dances based on Hungarian folk themes, originally "
            "for piano four-hands and later orchestrated. No. 5 in G minor is the "
            "most popular, instantly recognisable worldwide."
        ),
        "wikipedia_slug": "Hungarian_Dances_(Brahms)",
    },
    {
        "title": "Nocturne in E-flat major, Op. 9 No. 2",
        "composer_wikidata": "Q1268",
        "tradition": "Western Classical",
        "composition_type": "nocturne",
        "language": "Instrumental",
        "year_composed": 1832,
        "description": (
            "The most famous of Chopin's 21 nocturnes, with a long-breathed singing "
            "melody over a flowing left-hand accompaniment. It encapsulates Chopin's "
            "ability to evoke the poetry of night."
        ),
        "wikipedia_slug": "Nocturnes,_Op._9_(Chopin)",
    },
    {
        "title": "Ballade No. 1 in G minor, Op. 23",
        "composer_wikidata": "Q1268",
        "tradition": "Western Classical",
        "composition_type": "ballade",
        "language": "Instrumental",
        "year_composed": 1836,
        "description": (
            "Chopin's first ballade, possibly inspired by the poems of Adam Mickiewicz, "
            "journeys from hushed lyrical opening to a cataclysmic coda. It is considered "
            "one of the greatest piano works ever written."
        ),
        "wikipedia_slug": "Ballade_No._1_(Chopin)",
    },
    {
        "title": "Caprice No. 24 in A minor",
        "composer_wikidata": "Q168701",
        "tradition": "Western Classical",
        "composition_type": "caprice",
        "language": "Instrumental",
        "year_composed": 1817,
        "description": (
            "The final and most famous of Paganini's 24 Caprices for solo violin. "
            "Its theme has inspired variations by Brahms, Rachmaninoff, and Liszt. "
            "A touchstone of violin virtuosity."
        ),
        "wikipedia_slug": "24_Caprices_for_Solo_Violin_(Paganini)",
    },
    {
        "title": "Swan Lake",
        "title_native": "Лебединое озеро",
        "composer_wikidata": "Q7321",
        "tradition": "Western Classical",
        "composition_type": "ballet",
        "language": "Instrumental",
        "year_composed": 1877,
        "description": (
            "Tchaikovsky's iconic ballet tells the story of Odette, a princess "
            "turned into a swan by an evil sorcerer's curse. The music ranges from "
            "tender pas de deux to the famous Swan Theme — one of classical music's "
            "most recognisable melodies."
        ),
        "wikipedia_slug": "Swan_Lake",
    },
    {
        "title": "The Nutcracker",
        "title_native": "Щелкунчик",
        "composer_wikidata": "Q7321",
        "tradition": "Western Classical",
        "composition_type": "ballet",
        "language": "Instrumental",
        "year_composed": 1892,
        "description": (
            "A Christmas fantasy ballet in two acts, featuring the Waltz of the "
            "Snowflakes, the Sugar Plum Fairy, and the Dance of the Reed Flutes. "
            "The most performed ballet in the world every Christmas season."
        ),
        "wikipedia_slug": "The_Nutcracker",
    },
    {
        "title": "Clair de lune",
        "composer_wikidata": "Q1312",
        "tradition": "Western Classical",
        "composition_type": "suite",
        "language": "Instrumental",
        "year_composed": 1905,
        "description": (
            "The third movement of Debussy's Suite bergamasque, Clair de lune "
            "('Moonlight') is the most beloved piece of Impressionist piano music. "
            "Its shimmering textures evoke the play of moonlight on water."
        ),
        "wikipedia_slug": "Suite_bergamasque",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # CARNATIC
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Endaro Mahanubhavulu",
        "title_native": "ఎందరో మహానుభావులు",
        "composer_wikidata": "Q464485",
        "tradition": "Carnatic Classical",
        "composition_type": "kriti",
        "raga": "Sri",
        "raga_tradition": "carnatic",
        "tala": "Adi",
        "language": "Telugu",
        "year_composed": 1830,
        "description": (
            "The fifth and final of Tyagaraja's Pancharatna Kritis, sung in praise "
            "of great devotees of Lord Rama. Considered one of the most profound "
            "compositions in Carnatic music, it is performed at the annual Tyagaraja "
            "Aradhana festival."
        ),
        "wikipedia_slug": "Endaro_Mahanubhavulu",
    },
    {
        "title": "Jagadananda Karaka",
        "title_native": "జగదానందకారక",
        "composer_wikidata": "Q464485",
        "tradition": "Carnatic Classical",
        "composition_type": "kriti",
        "raga": "Nata",
        "raga_tradition": "carnatic",
        "tala": "Adi",
        "language": "Telugu",
        "year_composed": 1830,
        "description": (
            "The first of Tyagaraja's Pancharatna Kritis, set in Raga Nata. "
            "The opening words 'Jagadananda Karaka' ('O Creator of Universal Joy') "
            "address Lord Rama. Famous for its joyful, expansive character."
        ),
        "wikipedia_slug": "Pancharatna_Kritis",
    },
    {
        "title": "Nagumomu",
        "title_native": "నగుమోము",
        "composer_wikidata": "Q464485",
        "tradition": "Carnatic Classical",
        "composition_type": "kriti",
        "raga": "Abheri",
        "raga_tradition": "carnatic",
        "tala": "Adi",
        "language": "Telugu",
        "year_composed": 1820,
        "description": (
            "One of the most beloved of Tyagaraja's kritis, addressing the "
            "beautiful face of Lord Rama in Raga Abheri. Celebrated for its "
            "lyrical depth and the raga's characteristic bittersweet character."
        ),
        "wikipedia_slug": "Nagumomu",
    },
    {
        "title": "Vathapi Ganapathim Bhaje",
        "title_native": "వాతాపి గణపతిం భజే",
        "composer_wikidata": "Q932522",
        "tradition": "Carnatic Classical",
        "composition_type": "kriti",
        "raga": "Hamsadhvani",
        "raga_tradition": "carnatic",
        "tala": "Adi",
        "language": "Sanskrit",
        "year_composed": 1800,
        "description": (
            "Dikshitar's celebrated kriti in praise of Ganesha, set in the "
            "bright and auspicious Raga Hamsadhvani. One of the most widely "
            "performed Carnatic compositions, traditionally sung at the start "
            "of concerts."
        ),
        "wikipedia_slug": "Vatapi_Ganapathim",
    },
    {
        "title": "Saami Ninne Kori",
        "title_native": "స్వామి నిన్నె కోరి",
        "composer_wikidata": "Q976832",
        "tradition": "Carnatic Classical",
        "composition_type": "kriti",
        "raga": "Anandabhairavi",
        "raga_tradition": "carnatic",
        "tala": "Adi",
        "language": "Telugu",
        "year_composed": 1815,
        "description": (
            "One of Syama Sastri's most moving kritis, addressed to Goddess "
            "Kamakshi in the tender Raga Anandabhairavi. Noted for its deep "
            "devotion and the raga's characteristic pathos."
        ),
        "wikipedia_slug": "Syama_Sastri",
    },
    {
        "title": "Bhagyada Lakshmi Baramma",
        "title_native": "ಭಾಗ್ಯದ ಲಕ್ಷ್ಮಿ ಬಾರಮ್ಮ",
        "composer_wikidata": "Q504002",
        "tradition": "Carnatic Classical",
        "composition_type": "kriti",
        "raga": "Madhyamavati",
        "raga_tradition": "carnatic",
        "tala": "Adi",
        "language": "Kannada",
        "year_composed": 1530,
        "description": (
            "Purandaradasa's most popular composition, a supplication to "
            "Goddess Lakshmi in Raga Madhyamavati. Sung at dawn across Karnataka "
            "and considered a harbinger of good fortune."
        ),
        "wikipedia_slug": "Bhagyada_Lakshmi_Baramma",
    },
    {
        "title": "Padmanabha Pahi",
        "title_native": "പദ്മനാഭ പാഹി",
        "composer_wikidata": "Q731763",
        "tradition": "Carnatic Classical",
        "composition_type": "kriti",
        "raga": "Hamsadhvani",
        "raga_tradition": "carnatic",
        "tala": "Adi",
        "language": "Sanskrit",
        "year_composed": 1835,
        "description": (
            "A devotional kriti by Swathi Thirunal addressed to Lord Padmanabha "
            "of Thiruvananthapuram, in the bright Raga Hamsadhvani. One of the "
            "most beloved compositions from the Kerala court tradition."
        ),
        "wikipedia_slug": "Swathi_Thirunal",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # HINDUSTANI
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Miyan ki Malhar",
        "title_native": "मियाँ की मल्हार",
        "composer_wikidata": "Q382133",
        "tradition": "Hindustani Classical",
        "composition_type": "dhrupad",
        "raga": "Miyan ki Malhar",
        "raga_tradition": "hindustani",
        "language": "Braj Bhasha",
        "year_composed": 1560,
        "description": (
            "One of Tansen's most celebrated creations, this raga is said to have "
            "the power to invoke rain. Performed in the rainy season, Miyan ki Malhar "
            "is a pillar of the Hindustani monsoon raga canon."
        ),
        "wikipedia_slug": "Miyan_ki_Malhar",
    },
    {
        "title": "Darbari Kanada",
        "title_native": "दरबारी कानड़ा",
        "composer_wikidata": "Q382133",
        "tradition": "Hindustani Classical",
        "composition_type": "dhrupad",
        "raga": "Darbari Kanada",
        "raga_tradition": "hindustani",
        "language": "Braj Bhasha",
        "year_composed": 1565,
        "description": (
            "Created by Tansen for the court of Emperor Akbar, Darbari Kanada "
            "('the raga of the court') is performed in the late night with slow, "
            "meditative gamaks. Its regal gravity makes it one of the most "
            "revered ragas in Hindustani music."
        ),
        "wikipedia_slug": "Darbari_Kanada",
    },
    {
        "title": "Chaap Tilak Sab Chheeni",
        "title_native": "छाप तिलक सब छीनी",
        "composer_wikidata": "Q171922",
        "tradition": "Qawwali",
        "composition_type": "qawwali",
        "language": "Braj Bhasha",
        "year_composed": 1300,
        "description": (
            "Amir Khusrau's most famous Sufi composition, describing the spiritual "
            "transformation wrought by the gaze of his master Nizamuddin Auliya. "
            "Still performed at Sufi shrines across South Asia."
        ),
        "wikipedia_slug": "Chaap_Tilak",
    },
    {
        "title": "Aaj Rang Hai",
        "title_native": "आज रंग है",
        "composer_wikidata": "Q171922",
        "tradition": "Qawwali",
        "composition_type": "qawwali",
        "language": "Braj Bhasha",
        "year_composed": 1310,
        "description": (
            "A joyous Holi qawwali attributed to Amir Khusrau, sung in celebration "
            "of the festival of colours. One of the best-loved devotional songs "
            "in the Sufi tradition of South Asia."
        ),
        "wikipedia_slug": "Amir_Khusrau",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # JAZZ
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Take the A Train",
        "composer_wikidata": "Q105682",
        "tradition": "Jazz",
        "composition_type": "jazz",
        "language": "English",
        "year_composed": 1941,
        "description": (
            "Duke Ellington's signature tune, written by Billy Strayhorn, "
            "named after the A train subway line to Harlem. It became the "
            "theme of the Ellington orchestra and one of the most recorded "
            "jazz standards of all time."
        ),
        "wikipedia_slug": "Take_the_\"A\"_Train",
    },
    {
        "title": "Mood Indigo",
        "composer_wikidata": "Q105682",
        "tradition": "Jazz",
        "composition_type": "jazz",
        "language": "English",
        "year_composed": 1930,
        "description": (
            "One of Ellington's earliest and most enduring compositions, "
            "renowned for its unusual low-register voicing — muted trumpet, "
            "muted trombone, and clarinet — which creates its distinctive "
            "brooding, intimate sound."
        ),
        "wikipedia_slug": "Mood_Indigo",
    },
    {
        "title": "So What",
        "composer_wikidata": "Q93341",
        "tradition": "Jazz",
        "composition_type": "jazz",
        "language": "Instrumental",
        "year_composed": 1959,
        "description": (
            "The opening track of Miles Davis's Kind of Blue, the best-selling "
            "jazz album of all time. So What is built on modal scales rather "
            "than chord changes, marking the birth of modal jazz."
        ),
        "wikipedia_slug": "So_What_(Miles_Davis_composition)",
    },
    {
        "title": "Blue in Green",
        "composer_wikidata": "Q93341",
        "tradition": "Jazz",
        "composition_type": "jazz",
        "language": "Instrumental",
        "year_composed": 1959,
        "description": (
            "A meditative ballad from Kind of Blue, whose authorship is shared "
            "between Miles Davis and Bill Evans. Its circular harmonic structure "
            "and subdued mood make it one of jazz's most introspective pieces."
        ),
        "wikipedia_slug": "Blue_in_Green",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # TANGO
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Libertango",
        "composer_wikidata": "Q193236",
        "tradition": "Tango",
        "composition_type": "tango",
        "language": "Instrumental",
        "year_composed": 1974,
        "description": (
            "Piazzolla's most famous composition, its title fusing 'liberty' and "
            "'tango'. Recorded in Milan during his Italian period, Libertango "
            "became the gateway through which millions discovered nuevo tango. "
            "Covered by hundreds of artists across all genres."
        ),
        "wikipedia_slug": "Libertango",
    },
    {
        "title": "Adiós Nonino",
        "title_native": "Adiós Nonino",
        "composer_wikidata": "Q193236",
        "tradition": "Tango",
        "composition_type": "tango",
        "language": "Instrumental",
        "year_composed": 1959,
        "description": (
            "Written in a single night after the death of his father Vicente 'Nonino' "
            "Piazzolla, this elegy is considered Piazzolla's most personal work. "
            "The grief-stricken melody over a relentless ostinato became his "
            "most-performed composition."
        ),
        "wikipedia_slug": "Adiós_Nonino",
    },
    {
        "title": "Oblivion",
        "composer_wikidata": "Q193236",
        "tradition": "Tango",
        "composition_type": "tango",
        "language": "Instrumental",
        "year_composed": 1984,
        "description": (
            "Written for Marco Bellocchio's film Enrico IV, Oblivion is among "
            "Piazzolla's most achingly beautiful slow tangos. Its long, sighing "
            "melody has made it a favourite of cellists and violinists worldwide."
        ),
        "wikipedia_slug": "Oblivion_(Piazzolla)",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # AFROBEAT
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Zombie",
        "composer_wikidata": "Q179872",
        "tradition": "Afrobeat",
        "composition_type": "afrobeat",
        "language": "English/Pidgin",
        "year_composed": 1977,
        "description": (
            "Fela Kuti's blistering indictment of the Nigerian military, comparing "
            "soldiers to mindless zombies who follow orders without thought. "
            "The song sparked riots in Nigeria and led to a military attack on "
            "Fela's Kalakuta Republic commune."
        ),
        "wikipedia_slug": "Zombie_(Fela_Kuti_album)",
    },
    {
        "title": "Lady",
        "composer_wikidata": "Q179872",
        "tradition": "Afrobeat",
        "composition_type": "afrobeat",
        "language": "English/Pidgin",
        "year_composed": 1972,
        "description": (
            "A social commentary on gender roles in Africa, critiquing African "
            "women who adopt Western behaviours. Controversial in its politics yet "
            "musically irresistible — a prime example of Fela's long-form "
            "groove-based composition."
        ),
        "wikipedia_slug": "Lady_(Fela_Kuti_song)",
    },
    {
        "title": "Water No Get Enemy",
        "composer_wikidata": "Q179872",
        "tradition": "Afrobeat",
        "composition_type": "afrobeat",
        "language": "Yoruba/Pidgin",
        "year_composed": 1975,
        "description": (
            "From the album Expensive Shit, this Fela classic uses the Yoruba proverb "
            "'Water has no enemy' to extol the life-giving force that everyone needs. "
            "One of his most hypnotic compositions, built on a slow, deep groove."
        ),
        "wikipedia_slug": "Expensive_Shit/He_Miss_Road",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # ARABIC CLASSICAL
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Inta Omri",
        "title_native": "إنت عمري",
        "composer_wikidata": "Q232793",
        "tradition": "Maqam (Arabic)",
        "composition_type": "muwashshah",
        "maqam": "Rast",
        "language": "Arabic",
        "year_composed": 1964,
        "description": (
            "Meaning 'You Are My Life', Inta Omri is Oum Kalthoum's most celebrated "
            "song, composed by Mohammed Abdel Wahab. She performed it live for the "
            "first time in 1964; the concert recording runs over 90 minutes due to "
            "audience-demanded repetitions."
        ),
        "wikipedia_slug": "Inta_Omri",
    },
    {
        "title": "Al Atlal",
        "title_native": "الأطلال",
        "composer_wikidata": "Q232793",
        "tradition": "Maqam (Arabic)",
        "composition_type": "muwashshah",
        "maqam": "Hijaz",
        "language": "Arabic",
        "year_composed": 1966,
        "description": (
            "Setting the poem 'The Ruins' by Ibrahim Nagi, Al Atlal is considered "
            "Oum Kalthoum's greatest artistic achievement. Its slow unfolding "
            "over more than an hour, with each repetition building emotional intensity, "
            "epitomises the Arabic long-form vocal tradition."
        ),
        "wikipedia_slug": "Al_Atlal",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # FLAMENCO
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Entre dos Aguas",
        "composer_wikidata": "Q273501",
        "tradition": "Flamenco",
        "composition_type": "flamenco",
        "language": "Instrumental",
        "year_composed": 1973,
        "description": (
            "Paco de Lucía's breakthrough recording, a rumba flamenca that became "
            "Spain's most popular instrumental track. Its infectious rhythm "
            "brought flamenco guitar to a mass international audience for the "
            "first time."
        ),
        "wikipedia_slug": "Entre_dos_Aguas",
    },
    {
        "title": "Solo Quiero Caminar",
        "composer_wikidata": "Q273501",
        "tradition": "Flamenco",
        "composition_type": "flamenco",
        "language": "Instrumental",
        "year_composed": 1981,
        "description": (
            "A masterpiece of Paco de Lucía's mature style, blending traditional "
            "flamenco forms with jazz harmonic language. The title means 'I Only "
            "Want to Walk' and reflects Paco's restless musical wandering."
        ),
        "wikipedia_slug": "Solo_Quiero_Caminar",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # OTTOMAN / TURKISH
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Ferahfeza Ayin",
        "title_native": "Ferahfezâ Âyîn-i Şerîfi",
        "composer_wikidata": "Q1593021",
        "tradition": "Turkish Classical",
        "composition_type": "ayin",
        "maqam": "Ferahfeza",
        "language": "Ottoman Turkish",
        "year_composed": 1812,
        "description": (
            "Dede Efendi's most celebrated Mevlevi ayin — the sacred music for the "
            "Whirling Dervishes' sema ceremony. In the rare Ferahfeza makam, "
            "it is considered the crown of the Ottoman sacred classical repertoire."
        ),
        "wikipedia_slug": "Hammamizade_İsmail_Dede_Efendi",
    },

    # ═════════════════════════════════════════════════════════════════════════
    # GRIOT / WEST AFRICAN
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "Sunjata Epic",
        "title_native": "ߛߎ߬ߣߊ߬ߕߊ ߝߊ߱ߛߊ",
        "composer_wikidata": "Q178768",
        "tradition": "Griot",
        "composition_type": "epic",
        "language": "Mandinka",
        "year_composed": 1235,
        "description": (
            "The foundational oral epic of the Mande peoples, preserved and performed "
            "by hereditary jeli (griots) for over 800 years. It recounts the life of "
            "Sundiata Keita, founder of the Mali Empire, accompanied by the kora or "
            "balafon. Each performance is a unique act of living composition."
        ),
        "wikipedia_slug": "Sundiata_epic",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SQL helpers
# ─────────────────────────────────────────────────────────────────────────────

def esc(v: str) -> str:
    return v.replace("'", "''")


def s(v) -> str:
    return f"'{esc(str(v))}'" if v is not None else "NULL"


def composer_subq(wikidata: str | None) -> str:
    if not wikidata:
        return "NULL"
    return f"(SELECT id FROM composers WHERE wikidata_id = '{esc(wikidata)}' LIMIT 1)"


def tradition_subq(name: str | None) -> str:
    if not name:
        return "NULL"
    return f"(SELECT id FROM musical_traditions WHERE name = '{esc(name)}' LIMIT 1)"


def raga_subq(name: str | None, tradition: str | None) -> str:
    if not name:
        return "NULL"
    base = f"SELECT id FROM ragas WHERE LOWER(name) = LOWER('{esc(name)}')"
    if tradition:
        base += f" AND LOWER(tradition) = LOWER('{esc(tradition)}')"
    return f"({base} LIMIT 1)"


def tala_subq(name: str | None) -> str:
    if not name:
        return "NULL"
    return f"(SELECT id FROM talas WHERE LOWER(name) = LOWER('{esc(name)}') LIMIT 1)"


def build_sql(compositions: list[dict]) -> str:
    stmts = ["-- NadaAtlas compositions seed"]
    for c in compositions:
        comp_id   = composer_subq(c.get("composer_wikidata"))
        trad_id   = tradition_subq(c.get("tradition"))
        raga_id   = raga_subq(c.get("raga"), c.get("raga_tradition"))
        tala_id   = tala_subq(c.get("tala"))

        # WHERE NOT EXISTS guard — match on title + composer (or title alone if no composer)
        if c.get("composer_wikidata"):
            guard = (
                f"NOT EXISTS ("
                f"SELECT 1 FROM compositions "
                f"WHERE title = {s(c['title'])} "
                f"AND composer_id = {comp_id}"
                f")"
            )
        else:
            guard = (
                f"NOT EXISTS ("
                f"SELECT 1 FROM compositions WHERE title = {s(c['title'])}"
                f")"
            )

        stmt = f"""INSERT INTO compositions (
  id, title, title_native, composer_id, tradition_id, composition_type,
  raga_id, tala_id, maqam, language, description, year_composed,
  wikipedia_slug, created_at, updated_at
)
SELECT
  gen_random_uuid(),
  {s(c['title'])},
  {s(c.get('title_native'))},
  {comp_id},
  {trad_id},
  {s(c.get('composition_type'))},
  {raga_id},
  {tala_id},
  {s(c.get('maqam'))},
  {s(c.get('language'))},
  {s(c.get('description'))},
  {c['year_composed'] if c.get('year_composed') else 'NULL'},
  {s(c.get('wikipedia_slug'))},
  NOW(), NOW()
WHERE {guard};"""
        stmts.append(stmt)

    return "\n\n".join(stmts)


def main():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    if not db_url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(1)

    sql = build_sql(COMPOSITIONS)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    by_tradition: dict[str, int] = {}
    for c in COMPOSITIONS:
        t = c.get("tradition") or "Unknown"
        by_tradition[t] = by_tradition.get(t, 0) + 1

    print(f"Seeding {len(COMPOSITIONS)} compositions...")
    for trad, count in sorted(by_tradition.items()):
        print(f"  {trad}: {count}")

    result = subprocess.run(["psql", db_url, "-f", tmp_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ Done — {len(COMPOSITIONS)} compositions attempted.")


if __name__ == "__main__":
    main()
