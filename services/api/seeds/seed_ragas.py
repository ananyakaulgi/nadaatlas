"""
Seed ragas into the NadaAtlas database.
Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_ragas.py

Covers ~50 ragas across Hindustani and Carnatic traditions with full field data.
Notation used:
  Hindustani: S R G M P D N (natural); suffix ♭ = komal (flat), # = tivra (sharp)
  Carnatic:   S R1/R2 G2/G3 M1/M2 P D1/D2 N2/N3 (standard solfège numbering)
"""

import os
import subprocess
import sys
import tempfile

RAGAS = [

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Kalyan That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Yaman",
        "name_native": "यमन",
        "tradition": "both",
        "hindustani_name": "Yaman",
        "carnatic_name": "Kalyani",
        "that": "Kalyan",
        "melakarta_number": 65,
        "arohana": "S R G M# P D N S'",
        "avarohana": "S' N D P M# G R S",
        "vadi": "G (Gandhar)",
        "samvadi": "N (Nishad)",
        "pakad": "N R G M# D N R' S'",
        "time_of_day": "evening",
        "rasa": "Shringara (love/beauty)",
        "description": "One of the most popular ragas in Hindustani classical music, performed in the early evening. Uses only tivra Madhyam (sharp 4th), all other notes are natural. Equivalent to Kalyani in Carnatic music.",
        "wikipedia_slug": "Yaman_(raga)",
    },
    {
        "name": "Bhupali",
        "name_native": "भूपाली",
        "tradition": "both",
        "hindustani_name": "Bhupali",
        "carnatic_name": "Mohanam",
        "that": "Kalyan",
        "arohana": "S R G P D S'",
        "avarohana": "S' D P G R S",
        "vadi": "G (Gandhar)",
        "samvadi": "D (Dhaivat)",
        "pakad": "G R S D' S R G",
        "time_of_day": "evening",
        "rasa": "Shringara (love/beauty)",
        "description": "A pentatonic raga omitting Madhyam and Nishad. Its simple, clear structure makes it one of the most accessible and beloved ragas. Known as Mohanam in Carnatic music.",
        "wikipedia_slug": "Bhupali",
    },
    {
        "name": "Kedar",
        "name_native": "केदार",
        "tradition": "hindustani",
        "that": "Kalyan",
        "arohana": "S M P M# D N S'",
        "avarohana": "S' N D M# P M G S",
        "vadi": "M (Madhyam)",
        "samvadi": "S (Shadja)",
        "pakad": "S M P M# D M# P",
        "time_of_day": "evening",
        "rasa": "Bhakti (devotion)",
        "description": "A devotional evening raga named after the Kedarnath shrine. Uses both shuddha and tivra Madhyam, giving it a distinctive wavering quality.",
        "wikipedia_slug": "Kedar_(raga)",
    },
    {
        "name": "Hameer",
        "name_native": "हमीर",
        "tradition": "hindustani",
        "that": "Kalyan",
        "arohana": "S R G M P D N S'",
        "avarohana": "S' N D P M# D P M G R S",
        "vadi": "D (Dhaivat)",
        "samvadi": "G (Gandhar)",
        "time_of_day": "late night",
        "rasa": "Shringara (love/beauty)",
        "description": "A majestic late-night raga combining notes of both Kalyan and Bilawal thats. Known for its stately movements and emotional depth.",
        "wikipedia_slug": "Hameer",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Bhairav That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Bhairav",
        "name_native": "भैरव",
        "tradition": "hindustani",
        "that": "Bhairav",
        "arohana": "S R♭ G M P D♭ N S'",
        "avarohana": "S' N D♭ P M G R♭ S",
        "vadi": "D♭ (komal Dhaivat)",
        "samvadi": "R♭ (komal Rishabh)",
        "pakad": "D♭ P M G R♭ S",
        "time_of_day": "dawn",
        "rasa": "Shanta (peace/serenity)",
        "description": "An ancient morning raga of great antiquity, associated with Lord Shiva. Creates an atmosphere of austere serenity. One of the few ragas employing both komal Rishabh and komal Dhaivat.",
        "wikipedia_slug": "Bhairav_(raga)",
    },
    {
        "name": "Ahir Bhairav",
        "name_native": "अहीर भैरव",
        "tradition": "hindustani",
        "that": "Bhairav",
        "arohana": "S R♭ G M P D N S'",
        "avarohana": "S' N D P M G R♭ S",
        "vadi": "M (Madhyam)",
        "samvadi": "S (Shadja)",
        "time_of_day": "morning",
        "rasa": "Karuna (pathos)",
        "description": "A morning raga combining the Bhairav that's komal Rishabh with shuddha Dhaivat. Has a folk-like quality evoking pastoral scenes.",
        "wikipedia_slug": "Ahir_Bhairav",
    },
    {
        "name": "Ramkali",
        "name_native": "रामकली",
        "tradition": "hindustani",
        "that": "Bhairav",
        "arohana": "S R♭ G♭ M P D♭ N S'",
        "avarohana": "S' N D♭ P M G♭ R♭ S",
        "vadi": "G♭ (komal Gandhar)",
        "samvadi": "N (Nishad)",
        "time_of_day": "dawn",
        "rasa": "Shanta (peace/serenity)",
        "description": "A dawn raga closely related to Bhairav but with komal Gandhar added. Deeply meditative in character.",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Bhairavi That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Bhairavi",
        "name_native": "भैरवी",
        "tradition": "hindustani",
        "that": "Bhairavi",
        "arohana": "S R♭ G♭ M P D♭ N♭ S'",
        "avarohana": "S' N♭ D♭ P M G♭ R♭ S",
        "vadi": "M (Madhyam)",
        "samvadi": "S (Shadja)",
        "pakad": "M G♭ R♭ S N♭' D♭' P",
        "time_of_day": "morning",
        "rasa": "Karuna (pathos/compassion)",
        "description": "Traditionally performed at the end of a concert as a farewell raga. Uses all komal notes except Madhyam and Pancham. Evokes deep emotion, longing, and pathos. One of the most beloved ragas in all of Indian music.",
        "wikipedia_slug": "Bhairavi_(raga)",
    },
    {
        "name": "Malkauns",
        "name_native": "मालकौंस",
        "tradition": "both",
        "hindustani_name": "Malkauns",
        "carnatic_name": "Hindolam",
        "that": "Bhairavi",
        "arohana": "S G♭ M D♭ N♭ S'",
        "avarohana": "S' N♭ D♭ M G♭ S",
        "vadi": "M (Madhyam)",
        "samvadi": "S (Shadja)",
        "pakad": "N♭' D♭' M G♭ M D♭ N♭ S'",
        "time_of_day": "late night",
        "rasa": "Raudra/Vira (fierce/heroic)",
        "description": "One of the most ancient ragas, omitting Rishabh and Pancham entirely. Associated with Lord Shiva and said to have the power to summon supernatural forces. Known as Hindolam in Carnatic music.",
        "wikipedia_slug": "Malkauns",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Kafi That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Kafi",
        "name_native": "काफी",
        "tradition": "both",
        "hindustani_name": "Kafi",
        "carnatic_name": "Kharaharapriya",
        "that": "Kafi",
        "melakarta_number": 22,
        "arohana": "S R G♭ M P D N♭ S'",
        "avarohana": "S' N♭ D P M G♭ R S",
        "vadi": "P (Pancham)",
        "samvadi": "S (Shadja)",
        "time_of_day": "late night",
        "rasa": "Shringara/Karuna (love/pathos)",
        "description": "A late-night raga with a warm, intimate character. Widely used in thumri, dadra, and folk music. Equivalent to the 22nd melakarta Kharaharapriya in Carnatic music.",
        "wikipedia_slug": "Kafi_(raga)",
    },
    {
        "name": "Bhimpalasi",
        "name_native": "भीमपलासी",
        "tradition": "hindustani",
        "that": "Kafi",
        "arohana": "S G♭ M P N♭ S'",
        "avarohana": "S' N♭ D P M G♭ R S",
        "vadi": "M (Madhyam)",
        "samvadi": "S (Shadja)",
        "pakad": "N♭ D P M G♭ M R S",
        "time_of_day": "afternoon",
        "rasa": "Shringara (love/beauty)",
        "description": "An afternoon raga of great appeal and beauty. Omits Rishabh on the ascent, giving it a distinctive character. One of the most popular ragas for vocal and instrumental music.",
        "wikipedia_slug": "Bhimpalasi",
    },
    {
        "name": "Bageshri",
        "name_native": "बागेश्री",
        "tradition": "hindustani",
        "that": "Kafi",
        "arohana": "S G♭ M D N S'",
        "avarohana": "S' N D M G♭ R S",
        "vadi": "M (Madhyam)",
        "samvadi": "S (Shadja)",
        "pakad": "M D N S' R' S' N D M",
        "time_of_day": "late night",
        "rasa": "Shringara (love/longing)",
        "description": "A hauntingly beautiful late-night raga associated with a woman waiting for her beloved. Omits Pancham on the ascent. Popular in khayal and thumri forms.",
        "wikipedia_slug": "Bageshri",
    },
    {
        "name": "Megh",
        "name_native": "मेघ",
        "tradition": "hindustani",
        "that": "Kafi",
        "arohana": "S R M P N S'",
        "avarohana": "S' N D P M R S",
        "vadi": "P (Pancham)",
        "samvadi": "S (Shadja)",
        "season": "monsoon",
        "rasa": "Shringara (longing/rain)",
        "description": "The raga of the monsoon clouds, traditionally sung to invoke rain. Associated with longing and the first rains of the season.",
        "wikipedia_slug": "Megh_(raga)",
    },
    {
        "name": "Desh",
        "name_native": "देस",
        "tradition": "hindustani",
        "that": "Khamaj",
        "arohana": "S R M P N S'",
        "avarohana": "S' N D P M G R S",
        "vadi": "P (Pancham)",
        "samvadi": "S (Shadja)",
        "time_of_day": "evening",
        "rasa": "Shringara (love/beauty)",
        "description": "A popular evening raga with a light, pleasant character. Widely used in film music and folk-influenced compositions. The name means 'country' or 'homeland'.",
        "wikipedia_slug": "Desh_(raga)",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Asavari That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Darbari Kanada",
        "name_native": "दरबारी कानड़ा",
        "tradition": "hindustani",
        "that": "Asavari",
        "arohana": "S R G♭ M P D♭ N♭ S'",
        "avarohana": "S' N♭ D♭ P M G♭ R S",
        "vadi": "R (Rishabh)",
        "samvadi": "P (Pancham)",
        "pakad": "R G♭ R S N♭' D♭' P",
        "time_of_day": "late night",
        "rasa": "Karuna/Vira (pathos/heroic)",
        "description": "A grand, majestic raga said to have been composed by Miyan Tansen for Emperor Akbar's court (darbari = of the court). Takes hours to develop fully. Characterised by a slow oscillation on komal Gandhar.",
        "wikipedia_slug": "Darbari_Kanada",
    },
    {
        "name": "Asavari",
        "name_native": "आसावरी",
        "tradition": "hindustani",
        "that": "Asavari",
        "arohana": "S R M P D♭ S'",
        "avarohana": "S' N♭ D♭ P M G♭ R S",
        "vadi": "D♭ (komal Dhaivat)",
        "samvadi": "G♭ (komal Gandhar)",
        "time_of_day": "morning",
        "rasa": "Karuna (pathos)",
        "description": "A morning raga with a distinctly folk flavour, evoking the landscapes of rural India. The parent raga of the Asavari that.",
        "wikipedia_slug": "Asavari_(raga)",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Todi That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Todi",
        "name_native": "तोड़ी",
        "tradition": "both",
        "hindustani_name": "Miyan ki Todi",
        "carnatic_name": "Hanumatodi",
        "that": "Todi",
        "melakarta_number": 8,
        "arohana": "S R♭ G♭ M# P D♭ N S'",
        "avarohana": "S' N D♭ P M# G♭ R♭ S",
        "vadi": "D♭ (komal Dhaivat)",
        "samvadi": "G♭ (komal Gandhar)",
        "pakad": "R♭ G♭ M# G♭ R♭ S",
        "time_of_day": "morning",
        "rasa": "Karuna/Shringara (pathos/love)",
        "description": "One of the most complex and profound ragas, taking years to master. Uses komal Re, komal Ga, tivra Ma, and komal Dha simultaneously. Said to have been created by Miyan Tansen. Equivalent to the 8th melakarta Hanumatodi in Carnatic music.",
        "wikipedia_slug": "Todi_(raga)",
    },
    {
        "name": "Multani",
        "name_native": "मुल्तानी",
        "tradition": "hindustani",
        "that": "Todi",
        "arohana": "S G♭ M# P D♭ N S'",
        "avarohana": "S' N D♭ P M# G♭ R♭ S",
        "vadi": "P (Pancham)",
        "samvadi": "S (Shadja)",
        "time_of_day": "afternoon",
        "rasa": "Karuna (pathos)",
        "description": "An afternoon raga from the Todi family, named after the city of Multan. Omits Rishabh on the ascent.",
        "wikipedia_slug": "Multani_(raga)",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Marwa That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Marwa",
        "name_native": "मारवा",
        "tradition": "hindustani",
        "that": "Marwa",
        "arohana": "S R♭ G M# D N S'",
        "avarohana": "S' N D M# G R♭ S",
        "vadi": "R♭ (komal Rishabh)",
        "samvadi": "D (Dhaivat)",
        "pakad": "N' R♭ G M# D N",
        "time_of_day": "evening",
        "rasa": "Vira/Adbhuta (heroic/wonder)",
        "description": "Performed at sunset. Notable for the complete absence of Pancham (5th) and the unusual combination of komal Rishabh with tivra Madhyam, creating a profound sense of tension and yearning.",
        "wikipedia_slug": "Marwa_(raga)",
    },
    {
        "name": "Puriya",
        "name_native": "पूरिया",
        "tradition": "hindustani",
        "that": "Marwa",
        "arohana": "S R♭ G M# D N S'",
        "avarohana": "S' N D M# G R♭ S",
        "vadi": "G (Gandhar)",
        "samvadi": "N (Nishad)",
        "time_of_day": "evening",
        "rasa": "Shringara (love/longing)",
        "description": "An evening raga similar to Marwa but with Gandhar as the vadi. Creates a mood of restrained yearning. Often confused with Marwa by beginners.",
    },
    {
        "name": "Sohini",
        "name_native": "सोहिनी",
        "tradition": "hindustani",
        "that": "Marwa",
        "arohana": "S R♭ G M# P N S'",
        "avarohana": "S' N P M# G R♭ S",
        "vadi": "G (Gandhar)",
        "samvadi": "N (Nishad)",
        "time_of_day": "late night",
        "rasa": "Shringara (love/longing)",
        "description": "A late-night raga from the Marwa family, distinguished by the inclusion of Pancham. Romantic and yearning in character.",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Poorvi That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Shree",
        "name_native": "श्री",
        "tradition": "hindustani",
        "that": "Poorvi",
        "arohana": "S R♭ M# P N♭ S'",
        "avarohana": "S' N♭ D P M# R♭ S",
        "vadi": "R♭ (komal Rishabh)",
        "samvadi": "P (Pancham)",
        "time_of_day": "evening",
        "rasa": "Bhakti/Adbhuta (devotion/wonder)",
        "description": "A majestic sunset raga combining komal Rishabh, tivra Madhyam, and komal Nishad. Associated with auspiciousness and the divine.",
        "wikipedia_slug": "Shree_(raga)",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Bilawal That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Bilawal",
        "name_native": "बिलावल",
        "tradition": "both",
        "hindustani_name": "Bilawal",
        "carnatic_name": "Shankarabharanam",
        "that": "Bilawal",
        "melakarta_number": 29,
        "arohana": "S R G M P D N S'",
        "avarohana": "S' N D P M G R S",
        "vadi": "D (Dhaivat)",
        "samvadi": "G (Gandhar)",
        "time_of_day": "morning",
        "rasa": "Shanta (peace/serenity)",
        "description": "The parent raga of the Bilawal that, equivalent to the Western major scale. A morning raga of calm and brightness. Known as Shankarabharanam (29th melakarta) in Carnatic music.",
        "wikipedia_slug": "Bilawal_(raga)",
    },
    {
        "name": "Durga",
        "name_native": "दुर्गा",
        "tradition": "hindustani",
        "that": "Bilawal",
        "arohana": "S R M P D S'",
        "avarohana": "S' D P M R S",
        "vadi": "D (Dhaivat)",
        "samvadi": "R (Rishabh)",
        "time_of_day": "evening",
        "rasa": "Bhakti/Shringara (devotion/beauty)",
        "description": "A pentatonic raga omitting Gandhar and Nishad. Bright and devotional in character, associated with the goddess Durga.",
        "wikipedia_slug": "Durga_(raga)",
    },

    # ══════════════════════════════════════════════════════════════════════
    # HINDUSTANI — Khamaj That
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Khamaj",
        "name_native": "खमाज",
        "tradition": "both",
        "hindustani_name": "Khamaj",
        "carnatic_name": "Harikambhoji",
        "that": "Khamaj",
        "melakarta_number": 28,
        "arohana": "S G M P D N S'",
        "avarohana": "S' N♭ D P M G R S",
        "vadi": "G (Gandhar)",
        "samvadi": "N (Nishad)",
        "time_of_day": "night",
        "rasa": "Shringara (love/romance)",
        "description": "A romantic night raga popular in light classical forms like thumri and ghazal. Uses shuddha Nishad on the ascent and komal Nishad on the descent. Equivalent to Harikambhoji (28th melakarta) in Carnatic music.",
        "wikipedia_slug": "Khamaj_(raga)",
    },
    {
        "name": "Tilak Kamod",
        "name_native": "तिलक कामोद",
        "tradition": "hindustani",
        "that": "Khamaj",
        "arohana": "S R G P D S'",
        "avarohana": "S' N D P M G R S",
        "vadi": "R (Rishabh)",
        "samvadi": "P (Pancham)",
        "time_of_day": "night",
        "rasa": "Shringara (love/romance)",
        "description": "A popular night raga with a cheerful, romantic quality. Often performed in lighter forms of classical music.",
        "wikipedia_slug": "Tilak_Kamod",
    },

    # ══════════════════════════════════════════════════════════════════════
    # CARNATIC — Melakarta ragas
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Mayamalavagowla",
        "name_native": "மாயாமாளவகௌள",
        "tradition": "carnatic",
        "melakarta_number": 15,
        "arohana": "S R1 G3 M1 P D1 N3 S'",
        "avarohana": "S' N3 D1 P M1 G3 R1 S",
        "vadi": "S (Shadja)",
        "samvadi": "P (Pancham)",
        "description": "The 15th melakarta, traditionally the first raga taught to Carnatic students. Its scale is perfectly symmetric — the intervals on the ascent mirror those on the descent exactly.",
        "wikipedia_slug": "Mayamalavagowla",
    },
    {
        "name": "Kalyani",
        "name_native": "கல்யாணி",
        "tradition": "both",
        "hindustani_name": "Yaman",
        "carnatic_name": "Kalyani",
        "melakarta_number": 65,
        "arohana": "S R2 G3 M2 P D2 N3 S'",
        "avarohana": "S' N3 D2 P M2 G3 R2 S",
        "vadi": "G3 (Antara Gandhar)",
        "samvadi": "N3 (Kakali Nishad)",
        "time_of_day": "evening",
        "rasa": "Shringara (love/beauty)",
        "description": "The 65th melakarta, one of the most majestic ragas in Carnatic music. Uses tivra Madhyam (M2). Equivalent to Yaman in Hindustani music.",
        "wikipedia_slug": "Kalyani_(raga)",
    },
    {
        "name": "Shankarabharanam",
        "name_native": "சங்கராபரணம்",
        "tradition": "both",
        "hindustani_name": "Bilawal",
        "carnatic_name": "Shankarabharanam",
        "melakarta_number": 29,
        "arohana": "S R2 G3 M1 P D2 N3 S'",
        "avarohana": "S' N3 D2 P M1 G3 R2 S",
        "vadi": "S (Shadja)",
        "samvadi": "P (Pancham)",
        "description": "The 29th melakarta, equivalent to the Western major scale. One of the most important ragas in Carnatic music, used for a vast repertoire of compositions.",
        "wikipedia_slug": "Shankarabharanam",
    },
    {
        "name": "Kharaharapriya",
        "name_native": "கரஹரப்பிரியா",
        "tradition": "both",
        "hindustani_name": "Kafi",
        "carnatic_name": "Kharaharapriya",
        "melakarta_number": 22,
        "arohana": "S R2 G2 M1 P D2 N2 S'",
        "avarohana": "S' N2 D2 P M1 G2 R2 S",
        "vadi": "P (Pancham)",
        "samvadi": "S (Shadja)",
        "description": "The 22nd melakarta, equivalent to Kafi in Hindustani music. Parent of many important janya ragas including Abhogi and Sri Ranjani.",
        "wikipedia_slug": "Kharaharapriya",
    },
    {
        "name": "Hanumatodi",
        "name_native": "ஹனுமதோடி",
        "tradition": "both",
        "hindustani_name": "Miyan ki Todi",
        "carnatic_name": "Hanumatodi",
        "melakarta_number": 8,
        "arohana": "S R1 G2 M1 P D1 N2 S'",
        "avarohana": "S' N2 D1 P M1 G2 R1 S",
        "vadi": "M1 (Shuddha Madhyam)",
        "samvadi": "S (Shadja)",
        "description": "The 8th melakarta, equivalent to Todi in Hindustani music. One of the most important morning ragas in Carnatic music.",
        "wikipedia_slug": "Hanumatodi",
    },
    {
        "name": "Natabhairavi",
        "name_native": "நடபைரவி",
        "tradition": "both",
        "hindustani_name": "Asavari",
        "carnatic_name": "Natabhairavi",
        "melakarta_number": 20,
        "arohana": "S R2 G2 M1 P D1 N1 S'",
        "avarohana": "S' N1 D1 P M1 G2 R2 S",
        "vadi": "D1 (Shuddha Dhaivat)",
        "samvadi": "G2 (Sadharana Gandhar)",
        "description": "The 20th melakarta, equivalent to Asavari in Hindustani music. Parent of Abheri and other popular janya ragas.",
        "wikipedia_slug": "Natabhairavi",
    },
    {
        "name": "Harikambhoji",
        "name_native": "ஹரிகாம்போஜி",
        "tradition": "both",
        "hindustani_name": "Khamaj",
        "carnatic_name": "Harikambhoji",
        "melakarta_number": 28,
        "arohana": "S R2 G3 M1 P D2 N2 S'",
        "avarohana": "S' N2 D2 P M1 G3 R2 S",
        "vadi": "P (Pancham)",
        "samvadi": "S (Shadja)",
        "description": "The 28th melakarta, equivalent to Khamaj in Hindustani music. Parent of Kedaragowla, Kambhoji, and many other popular ragas.",
        "wikipedia_slug": "Harikambhoji",
    },
    {
        "name": "Charukeshi",
        "name_native": "சாருகேசி",
        "tradition": "carnatic",
        "melakarta_number": 26,
        "arohana": "S R2 G3 M1 P D1 N1 S'",
        "avarohana": "S' N1 D1 P M1 G3 R2 S",
        "vadi": "P (Pancham)",
        "samvadi": "S (Shadja)",
        "description": "The 26th melakarta. A unique raga combining the upper structure of Bhairavi with the lower structure of Shankarabharanam. Very popular in both classical and film music.",
        "wikipedia_slug": "Charukeshi",
    },
    {
        "name": "Kiravani",
        "name_native": "கிரவாணி",
        "tradition": "carnatic",
        "melakarta_number": 21,
        "arohana": "S R2 G2 M1 P D1 N3 S'",
        "avarohana": "S' N3 D1 P M1 G2 R2 S",
        "vadi": "P (Pancham)",
        "samvadi": "S (Shadja)",
        "description": "The 21st melakarta. Has a unique emotional quality; the combination of komal Ga, komal Dha with Kakali Nishad gives it a plaintive, searching character. Equivalent to the Western harmonic minor scale.",
        "wikipedia_slug": "Kiravani",
    },

    # ══════════════════════════════════════════════════════════════════════
    # CARNATIC — Janya (derived) ragas
    # ══════════════════════════════════════════════════════════════════════
    {
        "name": "Hamsadhvani",
        "name_native": "ஹம்ஸத்வனி",
        "tradition": "carnatic",
        "arohana": "S R2 G3 P N3 S'",
        "avarohana": "S' N3 P G3 R2 S",
        "vadi": "G3 (Antara Gandhar)",
        "samvadi": "N3 (Kakali Nishad)",
        "time_of_day": "evening",
        "rasa": "Shringara/Karuna (beauty/pathos)",
        "description": "A beautiful pentatonic janya raga derived from Shankarabharanam (omitting Madhyam and Dhaivat). Very popular for concert openings and auspicious occasions. Widely used in film music across South India.",
        "wikipedia_slug": "Hamsadhvani",
    },
    {
        "name": "Mohanam",
        "name_native": "மோஹனம்",
        "tradition": "both",
        "hindustani_name": "Bhupali",
        "carnatic_name": "Mohanam",
        "arohana": "S R2 G3 P D2 S'",
        "avarohana": "S' D2 P G3 R2 S",
        "vadi": "G3 (Antara Gandhar)",
        "samvadi": "D2 (Chatushruti Dhaivat)",
        "time_of_day": "evening",
        "rasa": "Shringara (love/beauty)",
        "description": "A pentatonic janya raga from Harikambhoji, equivalent to Bhupali in Hindustani music. One of the most popular ragas in South Indian classical and film music. The scale matches the pentatonic major scale.",
        "wikipedia_slug": "Mohanam",
    },
    {
        "name": "Hindolam",
        "name_native": "ஹிந்தோளம்",
        "tradition": "both",
        "hindustani_name": "Malkauns",
        "carnatic_name": "Hindolam",
        "arohana": "S G2 M1 D1 N1 S'",
        "avarohana": "S' N1 D1 M1 G2 S",
        "vadi": "M1 (Shuddha Madhyam)",
        "samvadi": "S (Shadja)",
        "time_of_day": "late night",
        "rasa": "Raudra/Vira (fierce/heroic)",
        "description": "A pentatonic janya raga omitting Rishabh and Pancham. Equivalent to Malkauns in Hindustani music. One of the most ancient ragas in Indian music.",
        "wikipedia_slug": "Hindolam",
    },
    {
        "name": "Abhogi",
        "name_native": "ஆபோகி",
        "tradition": "both",
        "hindustani_name": "Abhogi Kanada",
        "carnatic_name": "Abhogi",
        "arohana": "S R2 G2 M1 D2 S'",
        "avarohana": "S' D2 M1 G2 R2 S",
        "vadi": "G2 (Sadharana Gandhar)",
        "samvadi": "D2 (Chatushruti Dhaivat)",
        "time_of_day": "afternoon",
        "rasa": "Shringara (love/beauty)",
        "description": "A pentatonic janya raga from Kharaharapriya, omitting Pancham and Nishad. Has a sweet, devotional character and is popular in both Carnatic and Hindustani music.",
        "wikipedia_slug": "Abhogi",
    },
    {
        "name": "Revati",
        "name_native": "ரேவதி",
        "tradition": "carnatic",
        "arohana": "S R1 M1 P N2 S'",
        "avarohana": "S' N2 P M1 R1 S",
        "vadi": "S (Shadja)",
        "samvadi": "P (Pancham)",
        "time_of_day": "evening",
        "rasa": "Karuna (pathos/compassion)",
        "description": "A pentatonic janya raga with a deeply emotive, plaintive character. The combination of shuddha Rishabh and kaisiki Nishad gives it a unique colour.",
        "wikipedia_slug": "Revati_(raga)",
    },
    {
        "name": "Amritavarshini",
        "name_native": "அமிர்தவர்ஷிணி",
        "tradition": "carnatic",
        "arohana": "S G3 M2 P N3 S'",
        "avarohana": "S' N3 P M2 G3 S",
        "vadi": "M2 (Pratimadhyam)",
        "samvadi": "S (Shadja)",
        "season": "monsoon",
        "rasa": "Adbhuta (wonder/supernatural)",
        "description": "A raga traditionally sung to invoke rain. Said to have the power to summon monsoon clouds when performed correctly. Uses tivra Madhyam.",
        "wikipedia_slug": "Amritavarshini",
    },
    {
        "name": "Sri Ranjani",
        "name_native": "ஸ்ரீரஞ்சனி",
        "tradition": "carnatic",
        "arohana": "S R2 G2 M1 D2 N2 S'",
        "avarohana": "S' N2 D2 M1 G2 R2 S",
        "vadi": "G2 (Sadharana Gandhar)",
        "samvadi": "N2 (Kaisiki Nishad)",
        "time_of_day": "evening",
        "rasa": "Shringara/Karuna (love/pathos)",
        "description": "A popular janya raga from Kharaharapriya with an extremely appealing, melodic character. Widely used in both classical compositions and film music.",
        "wikipedia_slug": "Sri_Ranjani",
    },
    {
        "name": "Bilahari",
        "name_native": "பிலஹரி",
        "tradition": "carnatic",
        "arohana": "S R2 G3 P D2 S'",
        "avarohana": "S' N3 D2 P M1 G3 R2 S",
        "vadi": "G3 (Antara Gandhar)",
        "samvadi": "D2 (Chatushruti Dhaivat)",
        "time_of_day": "morning",
        "rasa": "Shringara (love/beauty)",
        "description": "A popular janya raga from Shankarabharanam used in morning concerts. The vakra (zigzag) movements in the avarohana give it a distinctive personality.",
        "wikipedia_slug": "Bilahari",
    },
    {
        "name": "Vasanta",
        "name_native": "வசந்தா",
        "tradition": "carnatic",
        "arohana": "S G3 M2 D1 N3 S'",
        "avarohana": "S' N3 D1 M2 R2 G3 R2 S",
        "vadi": "G3 (Antara Gandhar)",
        "samvadi": "N3 (Kakali Nishad)",
        "season": "spring",
        "rasa": "Shringara (love/spring)",
        "description": "A raga associated with the spring season and the festival of Holi. Its bright, joyous character captures the essence of new beginnings.",
        "wikipedia_slug": "Vasanta_(raga)",
    },
]


def escape_sql(val: str) -> str:
    return val.replace("'", "''")


def build_sql() -> str:
    lines = [
        "-- Raga seed data for नाद Atla𝄞",
        "-- Generated by seeds/seed_ragas.py",
        "",
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
    for r in RAGAS:
        def s(key):
            v = r.get(key)
            return f"'{escape_sql(v)}'" if v else "NULL"

        def n(key):
            v = r.get(key)
            return str(v) if v is not None else "NULL"

        row = (
            f"  (gen_random_uuid(), {s('name')}, {s('name_native')}, {s('tradition')}, "
            f"{s('hindustani_name')}, {s('carnatic_name')}, "
            f"{s('that')}, {n('melakarta_number')}, "
            f"{s('arohana')}, {s('avarohana')}, "
            f"{s('vadi')}, {s('samvadi')}, {s('pakad')}, "
            f"{s('time_of_day')}, {s('season')}, {s('rasa')}, "
            f"{s('description')}, {s('wikipedia_slug')}, "
            f"NOW(), NOW())"
        )
        values.append(row)

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (name) DO UPDATE SET")
    lines.append("  name_native      = EXCLUDED.name_native,")
    lines.append("  tradition        = EXCLUDED.tradition,")
    lines.append("  hindustani_name  = EXCLUDED.hindustani_name,")
    lines.append("  carnatic_name    = EXCLUDED.carnatic_name,")
    lines.append("  that             = EXCLUDED.that,")
    lines.append("  melakarta_number = EXCLUDED.melakarta_number,")
    lines.append("  arohana          = EXCLUDED.arohana,")
    lines.append("  avarohana        = EXCLUDED.avarohana,")
    lines.append("  vadi             = EXCLUDED.vadi,")
    lines.append("  samvadi          = EXCLUDED.samvadi,")
    lines.append("  pakad            = EXCLUDED.pakad,")
    lines.append("  time_of_day      = EXCLUDED.time_of_day,")
    lines.append("  season           = EXCLUDED.season,")
    lines.append("  rasa             = EXCLUDED.rasa,")
    lines.append("  description      = EXCLUDED.description,")
    lines.append("  wikipedia_slug   = EXCLUDED.wikipedia_slug,")
    lines.append("  updated_at       = NOW();")

    return "\n".join(lines)


def main():
    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Strip asyncpg prefix if present — psql uses plain postgresql://
    psql_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

    sql = build_sql()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        tmp_path = f.name

    print(f"Seeding {len(RAGAS)} ragas...")
    result = subprocess.run(["psql", psql_url, "-f", tmp_path], capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"✓ {len(RAGAS)} ragas seeded successfully.")


if __name__ == "__main__":
    main()
