"""
Seed Indigenous North American musical traditions, instruments, and artists.

Covers: Plains Nations, Haudenosaunee (Iroquois), Pacific Northwest Coast,
Diné (Navajo), Anishinaabe (Ojibwe), Inuit/Yup'ik, and the contemporary
Pan-Indian Powwow circuit.

METHODOLOGY NOTE:
  We only document publicly shared musical traditions. Sacred and ceremonial
  music that nations have not shared publicly is intentionally omitted.
  Descriptions use each nation's own terminology where possible.

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_native_american_traditions.py
"""

import os
import sys
from uuid import uuid4
from datetime import date

import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.environ.get("DATABASE_URL") or (
    "postgresql://postgres:uzGvKmjbUjIrpeBbTzfQhnLzheFbashG"
    "@ballast.proxy.rlwy.net:10439/railway"
)

# ---------------------------------------------------------------------------
# Region
# ---------------------------------------------------------------------------

REGION = {
    "id": str(uuid4()),
    "name": "Indigenous North America",
    "continent": "Americas",
    "description": (
        "The Indigenous nations of North America — from the Arctic coast to the "
        "Gulf of Mexico — represent hundreds of distinct musical traditions, each "
        "inseparable from language, land, ceremony, and community. This region "
        "encompasses the contiguous United States, Canada, and Alaska."
    ),
}

# ---------------------------------------------------------------------------
# Traditions
# ---------------------------------------------------------------------------

TRADITIONS = [
    {
        "id": str(uuid4()),
        "name": "Plains Nations Music",
        "name_native": "Oyate Olowan (Lakota: Songs of the People)",
        "region": "Indigenous North America",
        "subregion": "Great Plains",
        "description": (
            "The musical traditions of the Plains Nations — including the Lakota, Dakota, "
            "Nakota, Cheyenne, Arapaho, Blackfoot, Crow, Comanche, and Kiowa peoples — "
            "centre on the human voice and the drum. Song is understood as a living entity: "
            "songs are received in dreams, inherited through family lines, or owned by "
            "ceremonial societies, and each carries specific protocols for when and how it "
            "may be sung.\n\n"
            "The large communal drum — typically a bass drum struck by four or more singers "
            "in unison — is considered the heartbeat of the people. Singing style uses a "
            "high-pitched, open-throated delivery with characteristic descending phrases, "
            "often employing vocables (non-lexical syllables such as 'hey-ya-hey') rather "
            "than literal text. Song categories include honour songs, war songs, love songs, "
            "lullabies, healing songs, and the sacred songs of specific ceremonial societies.\n\n"
            "NOTE: Many Plains ceremonial songs are sacred and are not documented here. "
            "This entry focuses on the publicly shared repertoire including powwow music, "
            "honour songs, and recorded contemporary expressions of the tradition."
        ),
        "origin_period": "Pre-contact (documented from c. 1700s onward)",
        "wikipedia_slug": "Music_of_the_Great_Plains",
    },
    {
        "id": str(uuid4()),
        "name": "Haudenosaunee Music",
        "name_native": "Haudenosaunee (People of the Longhouse)",
        "region": "Indigenous North America",
        "subregion": "Northeastern Woodlands",
        "description": (
            "The Haudenosaunee Confederacy — comprising the Mohawk, Oneida, Onondaga, "
            "Cayuga, Seneca, and Tuscarora nations — has one of the richest musical "
            "traditions in North America. Music permeates social, ceremonial, and political "
            "life within the longhouse tradition.\n\n"
            "The water drum — a small wooden or clay vessel partially filled with water, "
            "covered with a wet hide — produces a distinctive resonant sound unique to "
            "Haudenosaunee music. It is played alongside the horn (or cow horn) rattle in "
            "social dance songs. The water drum's pitch changes with the amount of water "
            "inside, allowing subtle tonal variation.\n\n"
            "Social dances — including the Stomp Dance, Smoke Dance, and various animal "
            "dances — use song to build community cohesion. The Condolence Ceremony uses "
            "specific songs to mourn leaders and raise new ones. The Green Corn Ceremony "
            "and Midwinter Ceremony both feature extensive musical components.\n\n"
            "NOTE: Many Haudenosaunee ceremonial songs are restricted and are not "
            "documented here. This entry covers the publicly shared social dance and "
            "recorded musical traditions."
        ),
        "origin_period": "Pre-contact Northeastern Woodlands",
        "wikipedia_slug": "Music_of_the_Iroquois",
    },
    {
        "id": str(uuid4()),
        "name": "Pacific Northwest Coast Music",
        "name_native": "Various (Haida, Tlingit, Kwakwaka'wakw, Coast Salish)",
        "region": "Indigenous North America",
        "subregion": "Pacific Northwest",
        "description": (
            "The nations of the Pacific Northwest Coast — including the Haida, Tlingit, "
            "Tsimshian, Kwakwaka'wakw, Nuu-chah-nulth, and Coast Salish peoples — share "
            "a coastal environment that shaped musical traditions closely tied to the cedar "
            "tree, the salmon, and the ocean.\n\n"
            "Music in these traditions is typically owned: songs are property, passed down "
            "within clans or families, displayed publicly at potlatches alongside the "
            "distribution of wealth. A potlatch song sung by the wrong person is a serious "
            "cultural offence. The big house (longhouse) is the principal performance space; "
            "large painted drums are beaten while masked dancers re-enact ancestral stories "
            "and spirit encounters.\n\n"
            "Instruments include large cedar plank drums, hand drums, rattles of various "
            "materials (puffin beaks, deer hooves, shells), and whistles that represent "
            "supernatural voices. Choral singing by groups of singers accompanies most "
            "ceremonies. The revival of these traditions in the late 20th century — after "
            "decades of suppression under the Canadian potlatch ban (1885–1951) — is one "
            "of the most significant cultural stories in North America."
        ),
        "origin_period": "Pre-contact Pacific Northwest Coast",
        "wikipedia_slug": "Music_of_the_Pacific_Northwest_Coast_peoples",
    },
    {
        "id": str(uuid4()),
        "name": "Diné Bizaad Music",
        "name_native": "Diné (The People — Navajo Nation)",
        "region": "Indigenous North America",
        "subregion": "Southwest",
        "description": (
            "Diné (Navajo) music is deeply integrated with the Diné spiritual worldview "
            "expressed in Hózhó — the concept of balance, beauty, and harmony that "
            "permeates all aspects of life. The Navajo Nation (Dinétah), spanning parts of "
            "Arizona, New Mexico, and Utah, is the largest land area of any nation in the "
            "United States.\n\n"
            "Ceremonial music is central to the Navajo tradition. Healing ceremonies "
            "(Sings or Chantways), including the Blessingway, Nightway (Yéii Bicheii), "
            "and Enemyway, involve extended multi-night sequences of songs performed by "
            "trained Hataalii (singers/medicine men). Each ceremony has hundreds of songs "
            "that must be sung in precise order — errors can invalidate the ceremony.\n\n"
            "The Apache fiddle (tsii' edo'a'tl — 'wood that sings'), a unique bowed "
            "chordophone made from agave stalk, is used in the related Apache tradition "
            "and shares some features with Navajo musical practice.\n\n"
            "Secular musical traditions include Squaw Dance songs, social round dances, "
            "and contemporary expressions by artists like Sharon Burch and Radmilla Cody "
            "who blend traditional Navajo songs with country and folk genres.\n\n"
            "NOTE: Ceremonial chantway songs are sacred and restricted. This entry "
            "focuses on publicly documented secular and contemporary music."
        ),
        "origin_period": "Athabascan migration to the Southwest c. 1400–1525 CE",
        "wikipedia_slug": "Music_of_the_Navajo_people",
    },
    {
        "id": str(uuid4()),
        "name": "Anishinaabe Music",
        "name_native": "Anishinaabe (Ojibwe / Chippewa)",
        "region": "Indigenous North America",
        "subregion": "Great Lakes",
        "description": (
            "The Anishinaabe peoples — including the Ojibwe (Chippewa), Odawa, and "
            "Potawatomi nations of the Great Lakes region — share a musical tradition "
            "centred on the drum as a living, sacred being. The Anishinaabe origin story "
            "describes the world emerging from sound.\n\n"
            "The Midewiwin (Grand Medicine Society) is the principal ceremonial institution, "
            "and its songs — documented on birchbark scrolls, one of the few instances of "
            "Indigenous North American music notation — form a body of healing and "
            "initiation music passed through generations of members.\n\n"
            "The Dream Dance (or Drum Dance) tradition involves a large ceremonial drum "
            "given specific protocol and treated as a sacred being. Songs in the Dream "
            "Dance tradition are received in visions and used specifically with that drum.\n\n"
            "Secular music includes love songs (nagamonan), war songs (nakamowi), "
            "lullabies, and the jingle dress dance songs of the modern powwow circuit — "
            "the jingle dress dance originated among the Ojibwe in the early 20th century "
            "as a healing dance."
        ),
        "origin_period": "Great Lakes region, pre-contact",
        "wikipedia_slug": "Music_of_the_Ojibwe",
    },
    {
        "id": str(uuid4()),
        "name": "Inuit and Yup'ik Music",
        "name_native": "Katajjaq / Inuit throat singing",
        "region": "Indigenous North America",
        "subregion": "Arctic — Canada, Alaska, Greenland",
        "description": (
            "The Inuit peoples of the Arctic — including Inuit of Canada and Greenland "
            "and the related Yup'ik of Alaska — have a distinct musical tradition shaped "
            "by the extremes of Arctic life. The most distinctive practice is "
            "katajjaq — Inuit throat singing — performed traditionally by two women facing "
            "each other, sharing breath, and interlocking rhythmic vocal patterns of "
            "animal sounds, environmental sounds, and abstract vocables into a kind of "
            "musical game. The first person to laugh or run out of breath loses.\n\n"
            "The Inuit frame drum (qilaut or qilaun) — a large, thin drum made of animal "
            "hide stretched over a hoop of driftwood or bone — is beaten while a single "
            "performer dances and sings, with communal groups responding in chorus. "
            "Drum dances are associated with celebrations, hunting success, and conflict "
            "resolution through competitive performance.\n\n"
            "Contemporary artists like Tanya Tagaq (Kivalliq Inuit) have taken katajjaq "
            "into entirely new contexts — solo experimental performance, collaboration "
            "with rock and electronic musicians — while maintaining deep connection to "
            "its Arctic origins."
        ),
        "origin_period": "Arctic coast, pre-contact",
        "wikipedia_slug": "Inuit_throat_singing",
    },
    {
        "id": str(uuid4()),
        "name": "Contemporary Powwow Music",
        "name_native": "Pan-Indian / Intertribal",
        "region": "Indigenous North America",
        "subregion": "Pan-North American",
        "description": (
            "The powwow is a modern Pan-Indian tradition — a gathering that brings "
            "together members of many different nations for singing, dancing, and "
            "community. Though its roots lie in Plains Nations ceremony, the contemporary "
            "powwow circuit developed across North America through the 20th century as a "
            "form of cultural affirmation and intertribal connection, especially in urban "
            "areas with relocatee populations.\n\n"
            "Powwow music is performed by drum groups — typically 4 to 10 or more men "
            "seated around a large bass drum, singing in unison. The repertoire includes "
            "Grand Entry songs, Honor songs, Intertribal songs (open to all dancers), "
            "Veterans songs, Round Dance songs, and competition dance songs for specific "
            "categories: Men's Traditional, Men's Fancy, Women's Jingle, Women's Fancy "
            "Shawl, Grass Dance, and others.\n\n"
            "Major drum groups — including Blacklodge Singers, Northern Cree, Drum "
            "Royale, and many others — have achieved wide followings through recordings "
            "and the powwow circuit. The Native American Music Awards (Nammys) were "
            "established in 1998 to recognise achievements across powwow, traditional, "
            "and contemporary Indigenous music."
        ),
        "origin_period": "20th century, developed from Plains and Great Lakes traditions",
        "wikipedia_slug": "Powwow_(Native_American)",
    },
]

# ---------------------------------------------------------------------------
# Instruments
# ---------------------------------------------------------------------------

INSTRUMENTS = [
    {
        "id": str(uuid4()),
        "name": "Powwow Drum",
        "name_native": "Čhaŋčheğa (Lakota)",
        "instrument_family": "Percussion",
        "hornbostel_sachs": "211.311",
        "hs_category": "Membranophone",
        "description": (
            "The large communal drum at the centre of powwow music — a bass drum "
            "typically 2 to 3 feet in diameter, with two heads of rawhide stretched "
            "over a wooden frame. Struck by four to twelve singers seated around it, "
            "the powwow drum represents the heartbeat of the Earth and is treated as a "
            "living, sacred being. Each drum has protocols: it must not touch the ground "
            "without a blanket or stand, and some drums have names, songs, and histories. "
            "The sound carries long distances across open ground, coordinating the "
            "movements of hundreds of dancers."
        ),
        "origin_region": "Great Plains, North America",
        "materials": ["rawhide", "wood", "sinew"],
        "wikipedia_slug": "Hand_drum_(Plains_Indians)",
    },
    {
        "id": str(uuid4()),
        "name": "Native American Hand Drum",
        "name_native": "Tewel (Ojibwe) / various",
        "instrument_family": "Percussion",
        "hornbostel_sachs": "211.311.12",
        "hs_category": "Membranophone",
        "description": (
            "A single-headed frame drum 12 to 18 inches in diameter, held in one hand "
            "and struck with a beater in the other. Used across virtually all Indigenous "
            "North American traditions for solo song, healing ceremonies, storytelling, "
            "and travel songs. The head is typically rawhide or commercial drum skin; "
            "the frame is bent wood, sometimes with pebbles or seeds sealed inside for "
            "a rattle effect. Each nation has its own traditions for making, decorating, "
            "and using hand drums."
        ),
        "origin_region": "Widespread across North America",
        "materials": ["rawhide", "wood", "sinew"],
        "wikipedia_slug": "Frame_drum",
    },
    {
        "id": str(uuid4()),
        "name": "Water Drum",
        "name_native": "Ganöhsesge:owa (Haudenosaunee)",
        "instrument_family": "Percussion",
        "hornbostel_sachs": "211.311",
        "hs_category": "Membranophone",
        "description": (
            "The distinctive drum of the Haudenosaunee (Iroquois) nations — a small "
            "wooden or clay vessel, typically 8 to 12 inches tall, partially filled "
            "with water. A thin wet deerskin or groundhog hide is stretched across the "
            "top and held in place with a wooden hoop. The combination of water and "
            "damp skin produces a deep, resonant sound unlike any other drum. The pitch "
            "can be altered by tilting the drum to change the amount of water in contact "
            "with the membrane. Played with a crooked wooden beater alongside the horn "
            "rattle in social dance music."
        ),
        "origin_region": "Northeastern Woodlands, North America",
        "materials": ["wood", "clay", "rawhide", "water"],
        "wikipedia_slug": "Water_drum",
    },
    {
        "id": str(uuid4()),
        "name": "Native American Flute",
        "name_native": "Siyotanka (Lakota) / Courting Flute",
        "instrument_family": "Wind",
        "hornbostel_sachs": "421.121.12",
        "hs_category": "Aerophone",
        "description": (
            "The Native American flute is a two-chambered, end-blown flute — unique in "
            "world organology for its internal block (or 'bird') that directs the "
            "player's breath against a sharp edge to create sound. The two air chambers "
            "are separated by an external tie-down block; breath passes through the "
            "first chamber, exits through a hole in the wood under the external block, "
            "and is directed into the second (sounding) chamber. The result is a "
            "haunting, breathy tone that does not require complex embouchure.\n\n"
            "Traditionally associated with courtship on the Plains and in the Southwest, "
            "the flute was played by young men outside a woman's tipi or home. Materials "
            "include cedar, walnut, cherry, and other woods; decoration may include "
            "beadwork, carving, and feathers. R. Carlos Nakai is credited with the "
            "modern revival and popularisation of this instrument internationally."
        ),
        "origin_region": "Plains and Southwest, North America",
        "materials": ["cedar", "walnut", "cherry wood", "sinew"],
        "wikipedia_slug": "Native_American_flute",
    },
    {
        "id": str(uuid4()),
        "name": "Gourd Rattle",
        "name_native": "Híshe (Apache) / various",
        "instrument_family": "Percussion",
        "hornbostel_sachs": "112.12",
        "hs_category": "Idiophone",
        "description": (
            "One of the most widespread instruments across Indigenous North America, "
            "the gourd rattle is made from a dried gourd (Lagenaria siceraria) or "
            "rawhide container filled with pebbles, seeds, or small stones. The handle "
            "is a carved wooden stick. Rattles are essential ceremonial tools across "
            "many traditions — they accompany song and dance, mark rhythm, and are "
            "believed in many traditions to attract benevolent spirits and dispel malevolent ones. "
            "Specific rattles belong to specific ceremonies and are not interchangeable."
        ),
        "origin_region": "Widespread across North America",
        "materials": ["gourd", "rawhide", "wood", "pebbles"],
        "wikipedia_slug": "Rattle_(percussion)",
    },
    {
        "id": str(uuid4()),
        "name": "Apache Fiddle",
        "name_native": "Tsii' edo'a'tl (Diné/Apache: 'wood that sings')",
        "instrument_family": "Strings",
        "hornbostel_sachs": "321.312",
        "hs_category": "Chordophone",
        "description": (
            "The Apache fiddle (also called the Apache violin) is a unique bowed "
            "chordophone found among the Western Apache and related Athabascan-speaking "
            "peoples of the American Southwest. It is made from a single hollowed-out "
            "stalk of the century plant (agave), with one or two strings of sinew or "
            "plant fibre stretched over the body. The bow is a curved stick with sinew "
            "strands. Its tone is delicate and nasal, quite unlike European fiddles.\n\n"
            "The Apache fiddle is one of very few bowed instruments indigenous to the "
            "Americas — most bowed instruments elsewhere arrived with European contact. "
            "It is used for personal entertainment, courtship, and social occasions "
            "rather than ceremony."
        ),
        "origin_region": "American Southwest",
        "materials": ["agave stalk", "sinew", "wood"],
        "wikipedia_slug": "Apache_fiddle",
    },
    {
        "id": str(uuid4()),
        "name": "Inuit Drum (Qilaut)",
        "name_native": "Qilaut (Inuktitut) / Qilaun",
        "instrument_family": "Percussion",
        "hornbostel_sachs": "211.311.12",
        "hs_category": "Membranophone",
        "description": (
            "The large frame drum of the Inuit peoples — made from a thin ring of "
            "driftwood, bone, or willow, with a membrane of seal intestine, bladder, "
            "or dried stomach stretched across one side. Unlike most frame drums, the "
            "qilaut is struck on the wooden frame rather than the membrane itself, "
            "producing a resonant, booming sound. The performer holds the drum in one "
            "hand and strikes it with a short stick while dancing and singing, rotating "
            "the drum to vary the rhythm. Drum dances are community events held to "
            "celebrate hunting success, welcome visitors, and resolve conflicts."
        ),
        "origin_region": "Arctic North America — Inuit territories",
        "materials": ["driftwood", "bone", "seal intestine", "willow"],
        "wikipedia_slug": "Qilaut",
    },
    {
        "id": str(uuid4()),
        "name": "Turtle Shell Rattle",
        "name_native": "Various — widespread in Northeastern Woodlands",
        "instrument_family": "Percussion",
        "hornbostel_sachs": "112.12",
        "hs_category": "Idiophone",
        "description": (
            "A rattle made from the shell of a box turtle (Terrapene carolina), filled "
            "with pebbles or dried corn and attached to a wooden handle. Associated "
            "particularly with Haudenosaunee and other Northeastern Woodlands traditions, "
            "the turtle is a significant symbol in the creation stories of many nations "
            "(North America is known as 'Turtle Island' in many Indigenous traditions). "
            "Turtle shell rattles are used in social dances and some healing contexts."
        ),
        "origin_region": "Northeastern Woodlands, North America",
        "materials": ["turtle shell", "wood", "pebbles", "corn"],
        "wikipedia_slug": "Rattle_(percussion)",
    },
    {
        "id": str(uuid4()),
        "name": "Horn Rattle",
        "name_native": "Ga:gä (Haudenosaunee)",
        "instrument_family": "Percussion",
        "hornbostel_sachs": "112.12",
        "hs_category": "Idiophone",
        "description": (
            "The Haudenosaunee (Iroquois) horn rattle is made from snapping turtle shell "
            "or carved from cow horn or deer antler, filled with dried corn or pebbles. "
            "It is played as the standard rhythmic accompaniment to the water drum in "
            "Haudenosaunee social dance music — the two instruments form an inseparable "
            "pair, their interlocking rhythms driving the social dances of the longhouse."
        ),
        "origin_region": "Northeastern Woodlands, North America",
        "materials": ["horn", "antler", "dried corn"],
        "wikipedia_slug": None,
    },
    {
        "id": str(uuid4()),
        "name": "Big Drum (Ojibwe Drum Dance Drum)",
        "name_native": "Dewe'igan (Ojibwe: 'that which beats')",
        "instrument_family": "Percussion",
        "hornbostel_sachs": "211.311",
        "hs_category": "Membranophone",
        "description": (
            "The ceremonial drum of the Ojibwe Drum Dance tradition — a large bass drum "
            "suspended horizontally on four decorated posts at waist height, traditionally "
            "received in a vision and considered a living being with a name, a spirit, "
            "and specific keepers. The drum is elaborately decorated with ribbons, "
            "eagle feathers, and painted designs. Four men sit at the four cardinal "
            "directions and drum simultaneously while singers perform Drum Dance songs. "
            "The tradition spread from the Ojibwe to many other Great Lakes and Plains "
            "nations in the late 19th century."
        ),
        "origin_region": "Great Lakes — Ojibwe / Anishinaabe territories",
        "materials": ["rawhide", "wood", "sinew", "ribbon", "feathers"],
        "wikipedia_slug": None,
    },
]

# ---------------------------------------------------------------------------
# Artists
# ---------------------------------------------------------------------------

ARTISTS = [
    {
        "id": str(uuid4()),
        "name": "Buffy Sainte-Marie",
        "name_native": None,
        "nationality": "Canadian",
        "birth_place": "Piapot Cree Nation, Saskatchewan, Canada",
        "born": date(1941, 2, 20),
        "musical_tradition": "Plains Nations Music",
        "primary_instrument": "acoustic guitar",
        "biography_short": (
            "Plains Cree singer-songwriter, activist, and educator whose career spans "
            "six decades. Wrote 'Universal Soldier', won an Academy Award for 'Up Where "
            "We Belong', and became one of the most globally recognised Indigenous musicians."
        ),
        "biography": (
            "Buffy Sainte-Marie (born February 20, 1941) is a Cree singer-songwriter, "
            "musician, visual artist, and activist from the Piapot Cree First Nation in "
            "Saskatchewan. Adopted as an infant and raised in Massachusetts, she rediscovered "
            "her Indigenous heritage as a young adult and built a career that has made her "
            "one of the most important voices in both folk music and Indigenous rights.\n\n"
            "Her 1964 debut album 'It's My Way!' introduced a distinctive guitar style that "
            "blended folk, country, and Plains vocal traditions. 'Universal Soldier' (1964), "
            "written after observing soldiers at an airport, became an anthem of the anti-war "
            "movement and has been covered by hundreds of artists. She was one of the first "
            "major artists to incorporate Indigenous themes, imagery, and language into "
            "mainstream popular music.\n\n"
            "From 1976 to 1981 she appeared regularly on Sesame Street, introducing Indigenous "
            "culture and breastfeeding to millions of children. In 1983, she co-wrote 'Up "
            "Where We Belong' with Jack Nitzsche and Will Jennings, which won the Academy "
            "Award for Best Original Song. She remained active into her eighties: her 2017 "
            "album 'Medicine Songs' addressed contemporary Indigenous political issues, and "
            "she won the Polaris Music Prize in 2015 for 'Power in the Blood'."
        ),
        "wikipedia_slug": "Buffy_Sainte-Marie",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Buffy_Sainte-Marie_2012.jpg/440px-Buffy_Sainte-Marie_2012.jpg",
        "is_verified": True,
    },
    {
        "id": str(uuid4()),
        "name": "R. Carlos Nakai",
        "name_native": None,
        "nationality": "American",
        "birth_place": "Flagstaff, Arizona, USA",
        "born": date(1946, 4, 16),
        "musical_tradition": "Diné Bizaad Music",
        "primary_instrument": "Native American flute",
        "biography_short": (
            "Diné (Navajo) and Ute flutist widely credited with the global revival of the "
            "Native American flute. His 1989 album 'Canyon Trilogy' became the first "
            "Indigenous music recording to achieve platinum sales."
        ),
        "biography": (
            "R. Carlos Nakai (born April 16, 1946) is a Diné (Navajo) and Ute musician "
            "from Flagstaff, Arizona, widely regarded as the world's foremost performer "
            "and ambassador of the Native American flute. Trained initially as a classical "
            "trumpeter, a car accident in the 1970s damaged his embouchure and led him to "
            "explore the cedar flute — an instrument he had never studied formally but which "
            "became his life's work.\n\n"
            "Nakai's approach transformed the Native American flute from a folk instrument "
            "used in courtship and personal expression into a globally recognised voice. "
            "His 1989 album 'Canyon Trilogy', recorded in the natural reverb of a Colorado "
            "canyon, sold over a million copies — the first recording of Indigenous North "
            "American music to achieve platinum status. It introduced the flute's breathy, "
            "pentatonic sound to a worldwide audience and established him as the defining "
            "voice of the New Age music movement's Indigenous strand.\n\n"
            "Nakai has recorded over 50 albums spanning solo flute, chamber collaborations "
            "with Japanese koto players, Tibetan monks, and Western orchestras. He holds "
            "honorary doctorates from multiple universities and has been central to the "
            "academic study of Native American flute music through his writings and teaching."
        ),
        "wikipedia_slug": "R._Carlos_Nakai",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/R_Carlos_Nakai.jpg/440px-R_Carlos_Nakai.jpg",
        "is_verified": True,
    },
    {
        "id": str(uuid4()),
        "name": "Joanne Shenandoah",
        "name_native": "Tekalihwa:khwa (Oneida: 'She sings')",
        "nationality": "American",
        "birth_place": "Oneida Nation Territory, New York, USA",
        "born": date(1957, 6, 23),
        "died": date(2021, 10, 22),
        "musical_tradition": "Haudenosaunee Music",
        "primary_instrument": "voice",
        "biography_short": (
            "Oneida Nation singer, multiple Grammy and Nammy award winner, and one of "
            "the most celebrated voices in Indigenous North American music. Her recordings "
            "blended traditional Haudenosaunee songs with contemporary arrangements."
        ),
        "biography": (
            "Joanne Shenandoah (June 23, 1957 – October 22, 2021) was an Oneida Nation "
            "musician, the daughter of jazz guitarist Merce Shenandoah and an Oneida "
            "mother, born in Oneida territory near Syracuse, New York. She carried both "
            "her family's musical gift and her nation's ceremonial traditions into a "
            "recording career that produced over 15 albums and won more Native American "
            "Music Awards (Nammys) than any other artist.\n\n"
            "Her voice — a rich, warm mezzo-soprano trained in both Western and traditional "
            "Haudenosaunee styles — was the defining sound of her work. Albums like "
            "'Matriarch: Iroquois Women's Songs' (1998), 'Eagle Cries' (1995), and 'Life "
            "Blood' (1991) drew on the social dance songs, lullabies, and morning songs "
            "of the longhouse tradition, presenting them to audiences worldwide without "
            "compromising their integrity.\n\n"
            "She was a member of the Haudenosaunee Standing Committee on Burial Rules and "
            "Regulations and deeply committed to cultural preservation. She performed at "
            "Presidential inaugurations, received a Grammy nomination, and was named a "
            "United Nations Goodwill Ambassador. She died on October 22, 2021, of COVID-19 "
            "complications, leaving a legacy that transformed how Indigenous North American "
            "music is understood globally."
        ),
        "wikipedia_slug": "Joanne_Shenandoah",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Joanne_Shenandoah.jpg/440px-Joanne_Shenandoah.jpg",
        "is_verified": True,
    },
    {
        "id": str(uuid4()),
        "name": "Tanya Tagaq",
        "name_native": None,
        "nationality": "Canadian",
        "birth_place": "Cambridge Bay (Ikaluktutiak), Nunavut, Canada",
        "born": date(1975, 12, 5),
        "musical_tradition": "Inuit and Yup'ik Music",
        "primary_instrument": "voice (throat singing)",
        "biography_short": (
            "Inuit throat singer, composer, and visual artist from Nunavut who transformed "
            "katajjaq from a two-person social game into a boundary-breaking solo art form. "
            "Won Canada's Polaris Music Prize in 2014."
        ),
        "biography": (
            "Tanya Tagaq (born December 5, 1975) is an Inuit musician, artist, and "
            "activist from Cambridge Bay (Ikaluktutiak) in Nunavut, Canada. She is the "
            "most internationally prominent practitioner of katajjaq (Inuit throat "
            "singing) — a vocal tradition traditionally performed by two women facing "
            "each other, interlocking breath-driven rhythmic patterns until one of them "
            "laughs or loses breath.\n\n"
            "Tagaq taught herself throat singing while studying at the Nova Scotia College "
            "of Art and Design, away from her community and without elders to guide her. "
            "This isolation led her to develop a radical solo practice — using loop "
            "pedals, microphones, and her own physical voice to layer the sounds of "
            "katajjaq into a disturbing, powerful sonic landscape that has been compared "
            "to avant-garde music, metal, and shamanic performance.\n\n"
            "Her 2014 album 'Animism' won the Polaris Music Prize, Canada's highest music "
            "honour, and she has collaborated with Björk, the Kronos Quartet, and many "
            "others. Her performances address Inuit land rights, the crisis of missing "
            "and murdered Indigenous women, and the impact of climate change on Arctic "
            "life. She received the Governor General's Performing Arts Award in 2015."
        ),
        "wikipedia_slug": "Tanya_Tagaq",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Tanya_Tagaq.jpg/440px-Tanya_Tagaq.jpg",
        "is_verified": True,
    },
    {
        "id": str(uuid4()),
        "name": "Robbie Robertson",
        "name_native": None,
        "nationality": "Canadian",
        "birth_place": "Toronto, Ontario, Canada",
        "born": date(1943, 7, 5),
        "died": date(2023, 8, 9),
        "musical_tradition": "Haudenosaunee Music",
        "primary_instrument": "electric guitar",
        "biography_short": (
            "Mohawk and Jewish guitarist, songwriter, and leader of The Band — one of "
            "rock music's most celebrated groups. His 1994 album 'Music for the Native "
            "Americans' directly addressed his Haudenosaunee heritage."
        ),
        "biography": (
            "Robbie Robertson (July 5, 1943 – August 9, 2023) was a Canadian musician, "
            "songwriter, and film composer of Mohawk/Cayuga (Haudenosaunee) and Jewish "
            "heritage, born in Toronto. He grew up between Toronto and the Six Nations "
            "Reserve, spending summers with his mother's Haudenosaunee family before "
            "departing at 16 to join Ronnie Hawkins' touring band — an apprenticeship "
            "that led to the formation of The Band.\n\n"
            "The Band — Robertson alongside Levon Helm, Rick Danko, Richard Manuel, and "
            "Garth Hudson — created a body of work that drew on American roots music "
            "(country, folk, R&B, gospel) with unusual depth and storytelling. Albums "
            "like 'Music from Big Pink' (1968) and 'The Band' (1969) influenced virtually "
            "every major rock act of the following decade. Robertson's guitar style — "
            "angular, melodic, deeply rhythmic — became one of the most imitated in "
            "rock history.\n\n"
            "His 1994 album 'Music for the Native Americans', recorded as a soundtrack to "
            "a Turner Broadcasting documentary series, directly engaged his Haudenosaunee "
            "heritage, collaborating with the Ulali vocal ensemble and incorporating "
            "traditional songs alongside original compositions. It introduced his "
            "Indigenous identity to audiences who knew him only as a rock musician."
        ),
        "wikipedia_slug": "Robbie_Robertson",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Robbie_Robertson.jpg/440px-Robbie_Robertson.jpg",
        "is_verified": True,
    },
    {
        "id": str(uuid4()),
        "name": "John Trudell",
        "name_native": None,
        "nationality": "American",
        "birth_place": "Omaha, Nebraska, USA",
        "born": date(1946, 2, 15),
        "died": date(2015, 12, 8),
        "musical_tradition": "Plains Nations Music",
        "primary_instrument": "voice (spoken word / poetry)",
        "biography_short": (
            "Santee Dakota poet, musician, and activist; former chairman of the American "
            "Indian Movement (AIM). His spoken-word recordings over rock and blues backings "
            "created a distinctive art form that influenced a generation of Indigenous artists."
        ),
        "biography": (
            "John Trudell (February 15, 1946 – December 8, 2015) was a Santee Dakota "
            "Sioux poet, musician, actor, and political activist from Omaha, Nebraska. "
            "As national chairman of the American Indian Movement (AIM) from 1973 to 1979, "
            "he was one of the most prominent Indigenous rights voices in the United States; "
            "FBI files on him ran to more than 17,000 pages.\n\n"
            "The 1979 fire that killed his wife, mother-in-law, and three children at the "
            "family home on the Pine Ridge Reservation transformed him. The FBI characterised "
            "the fire as 'accidental'; AIM members maintained it was retribution for Trudell's "
            "burning of an American flag outside FBI headquarters the previous day. Trudell "
            "channelled his grief into writing poetry at a furious pace.\n\n"
            "Beginning in the late 1980s, he developed a distinctive musical form — "
            "spoken-word poetry delivered over rock, blues, and traditional drum backings, "
            "with musicians including Jesse Ed Davis and the Graffiti Band. Albums like "
            "'AKA Grafitti Man' (1986, re-released 1992) and 'Johnny Damas and Me' (1994) "
            "were critically acclaimed as sui generis works that fit no genre but spoke "
            "from a specific cultural and spiritual location. Jackson Browne called him "
            "'one of the most important poets of the 20th century.'"
        ),
        "wikipedia_slug": "John_Trudell",
        "image_url": None,
        "is_verified": False,
    },
    {
        "id": str(uuid4()),
        "name": "Sharon Burch",
        "name_native": None,
        "nationality": "American",
        "birth_place": "Newcomb, New Mexico, USA",
        "born": date(1957, 1, 1),
        "musical_tradition": "Diné Bizaad Music",
        "primary_instrument": "voice",
        "biography_short": (
            "Navajo-German singer who has recorded traditional Navajo songs and original "
            "compositions in the Navajo language, preserving the beauty of the Diné "
            "vocal tradition for new generations."
        ),
        "biography": (
            "Sharon Burch was born in Newcomb, New Mexico, on the Navajo Nation, to a "
            "Navajo mother and a German-American father. Growing up between two cultures, "
            "she found her path through the Navajo songs she learned from her mother and "
            "maternal family — songs that became the bedrock of her recording career.\n\n"
            "Her albums, including 'Yazzie Girl' (1989) and 'Touch the Sweet Earth' (1995), "
            "present traditional Navajo songs — lullabies, walking songs, and social songs "
            "— alongside original compositions in both Navajo and English. Her clear, "
            "unaffected soprano voice and sparse acoustic accompaniment allow the beauty "
            "of the Navajo language itself to be the foreground. She is among the first "
            "Navajo artists to record traditional songs for commercial distribution, and "
            "her work has been used in language revitalisation and cultural education programs.\n\n"
            "She is associated with Canyon Records, the Arizona-based independent label "
            "that has documented Indigenous North American music since 1951 and holds "
            "one of the most important archives of its kind."
        ),
        "wikipedia_slug": None,
        "image_url": None,
        "is_verified": False,
    },
    {
        "id": str(uuid4()),
        "name": "Kevin Locke",
        "name_native": "Tokaheya Inajin (Hunkpapa Lakota: 'First to Rise')",
        "nationality": "American",
        "birth_place": "Standing Rock Sioux Reservation, North Dakota, USA",
        "born": date(1954, 1, 1),
        "musical_tradition": "Plains Nations Music",
        "primary_instrument": "Native American flute",
        "biography_short": (
            "Hunkpapa Lakota and Anishinaabe flutist, hoop dancer, and UNESCO-recognised "
            "cultural ambassador. Widely regarded as one of the greatest living practitioners "
            "of the Lakota love flute and the Eagle Dance hoop tradition."
        ),
        "biography": (
            "Kevin Locke (Tokaheya Inajin, 'First to Rise') is a Hunkpapa Lakota and "
            "Anishinaabe (Chippewa) musician, hoop dancer, and storyteller from the "
            "Standing Rock Sioux Reservation in North Dakota. He is considered one of "
            "the foremost custodians of the Lakota love flute tradition and the Eagle "
            "Dance hoop dance — a solo dance form in which the performer manipulates up "
            "to 28 hoops simultaneously to create representations of the eagle and other "
            "natural forms.\n\n"
            "Locke has performed the love flute and hoop dance as a cultural ambassador "
            "in over 70 countries, presenting these traditions to audiences who have never "
            "encountered them. He has been recognised by the United Nations Educational, "
            "Scientific and Cultural Organization (UNESCO) as a living treasure of "
            "intangible cultural heritage.\n\n"
            "His recordings document both the traditional Lakota flute repertoire and "
            "his own compositions in the traditional style. He speaks the Lakota language "
            "fluently — increasingly rare — and uses music as a vehicle for language "
            "transmission and cultural continuity."
        ),
        "wikipedia_slug": "Kevin_Locke",
        "image_url": None,
        "is_verified": False,
    },
]

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def now_sql():
    return "NOW()"


def run():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor()

    print("=== Seeding Indigenous North American music ===\n")

    # ── 1. Region ──────────────────────────────────────────────────────────
    print("Creating region: Indigenous North America")
    cur.execute(
        """
        INSERT INTO regions (id, name, continent, description, created_at, updated_at)
        VALUES (%s, %s, %s, %s, NOW(), NOW())
        ON CONFLICT (name) DO UPDATE SET
            description = EXCLUDED.description,
            updated_at  = NOW()
        RETURNING id, name
        """,
        (REGION["id"], REGION["name"], REGION["continent"], REGION["description"]),
    )
    row = cur.fetchone()
    region_id = row[0]
    print(f"  → {row[1]} (id={region_id})\n")

    # ── 2. Traditions ──────────────────────────────────────────────────────
    tradition_ids: dict[str, str] = {}
    print("Creating traditions:")
    for t in TRADITIONS:
        cur.execute(
            """
            INSERT INTO musical_traditions
                (id, name, name_native, region, subregion, description,
                 origin_period, wikipedia_slug, region_id, is_active,
                 created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, NOW(), NOW())
            ON CONFLICT (name) DO UPDATE SET
                name_native     = EXCLUDED.name_native,
                description     = EXCLUDED.description,
                origin_period   = EXCLUDED.origin_period,
                wikipedia_slug  = EXCLUDED.wikipedia_slug,
                region_id       = EXCLUDED.region_id,
                updated_at      = NOW()
            RETURNING id, name
            """,
            (
                t["id"], t["name"], t["name_native"], t["region"],
                t.get("subregion"), t["description"], t["origin_period"],
                t["wikipedia_slug"], region_id,
            ),
        )
        row = cur.fetchone()
        tradition_ids[t["name"]] = str(row[0])
        print(f"  ✓ {row[1]}")

    print()

    # ── 3. Instruments ─────────────────────────────────────────────────────
    print("Creating instruments:")
    for inst in INSTRUMENTS:
        cur.execute(
            """
            INSERT INTO instruments
                (id, name, name_native, instrument_family, hornbostel_sachs,
                 hs_category, description, origin_region, materials,
                 wikipedia_slug, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT (name) DO UPDATE SET
                name_native      = EXCLUDED.name_native,
                description      = EXCLUDED.description,
                origin_region    = EXCLUDED.origin_region,
                wikipedia_slug   = EXCLUDED.wikipedia_slug,
                updated_at       = NOW()
            RETURNING id, name
            """,
            (
                inst["id"], inst["name"], inst["name_native"],
                inst["instrument_family"], inst["hornbostel_sachs"],
                inst["hs_category"], inst["description"],
                inst["origin_region"], inst["materials"],
                inst["wikipedia_slug"],
            ),
        )
        row = cur.fetchone()
        print(f"  ✓ {row[1]}")

    print()

    # ── 4. Artists ─────────────────────────────────────────────────────────
    print("Creating artists:")
    for a in ARTISTS:
        trad_name = a.get("musical_tradition")
        tradition_id = tradition_ids.get(trad_name) if trad_name else None

        cur.execute(
            """
            INSERT INTO artists
                (id, name, name_native, nationality, birth_place,
                 born, died, musical_tradition, tradition_id,
                 biography_short, biography,
                 wikipedia_slug, image_url, is_verified,
                 created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT DO NOTHING
            RETURNING id, name
            """,
            (
                a["id"], a["name"], a.get("name_native"),
                a["nationality"], a["birth_place"],
                a["born"], a.get("died"),
                a["musical_tradition"], tradition_id,
                a["biography_short"], a["biography"],
                a.get("wikipedia_slug"), a.get("image_url"),
                a.get("is_verified", False),
            ),
        )
        row = cur.fetchone()
        if row:
            print(f"  ✓ {row[1]}")
        else:
            print(f"  — {a['name']} (already exists, skipped)")

    print()

    conn.commit()
    cur.close()
    conn.close()
    print("=== Done ===")
    print(f"\nSummary:")
    print(f"  1 region")
    print(f"  {len(TRADITIONS)} traditions")
    print(f"  {len(INSTRUMENTS)} instruments")
    print(f"  {len(ARTISTS)} artists")


if __name__ == "__main__":
    run()
