# NādaAtlas

> *Nāda* (नाद) — Sanskrit: the primordial sound, the cosmic vibration from which all music is born.  
> *Atlas* — a complete mapping of the world.

**NādaAtlas** is the world's most comprehensive music encyclopedia — every tradition, every instrument, every culture, every era. From Hindustani ragas to West African kora, from Andean pan flutes to Nordic folk, from Japanese gagaku to Congolese soukous. No tradition is too obscure, no region too remote.

---

## What NādaAtlas Is

A living, daily-updated platform that combines:

- **Encyclopedia** — biographies, traditions, instruments, and histories for every musician and musical form on earth
- **Catalog** — organized by instrument, tradition, region, era, and culture with deep cross-referencing
- **Links** — curated connections to performances, recordings, and music available on YouTube, Spotify, and beyond
- **Recommendations** — intelligent discovery of music you have never heard but will love
- **Radio** — curated stations by tradition, mood, era, and instrument

---

## Music Traditions Covered

| Region | Traditions |
|--------|-----------|
| **South Asia** | Hindustani Classical, Carnatic, Dhrupad, Khyal, Thumri, Ghazal, Qawwali, Baul, Indian Folk |
| **East Asia** | Chinese Classical & Opera, Japanese Gagaku & Koto, Korean Jeongak & Pansori, Mongolian Throat Singing, Tibetan |
| **Southeast Asia** | Indonesian Gamelan, Thai Piphat, Vietnamese Ca Trù, Philippine Kulintang, Cambodian Pin Peat |
| **Middle East & Central Asia** | Arabic Maqam, Persian Classical, Turkish Makam, Afghan Rubab, Azerbaijani Mugham, Shashmaqam |
| **Africa** | West African Griot & Kora, Malian, Ethiopian, Nigerian Afrobeats & Jùjú, South African Mbaqanga, Congolese Soukous, Gnawa |
| **Latin America** | Brazilian Samba & Bossa Nova, Andean Pan Flute, Argentine Tango, Cuban Son, Colombian Cumbia, Mariachi |
| **Caribbean** | Reggae, Calypso, Steel Pan, Kompa, Merengue, Bomba |
| **Europe** | Western Classical, Opera, Nordic Folk, Sámi Joik, Celtic, Flamenco, Fado, Balkan, Romani |
| **North America** | Blues, Jazz, Appalachian & Bluegrass, Native American, Gospel, Country |
| **Oceania** | Aboriginal Australian, Māori, Hawaiian Hula & Slack-Key, Polynesian |
| **Devotional** | Gregorian Chant, Tibetan Buddhist, Hindu Bhajan & Kirtan, Qawwali, Jewish Cantorial, Sikh Kirtan |

---

## Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Encyclopedia — artist biographies, discographies, instruments, daily ingestion | 🔨 Building |
| 2 | Catalog — organized by instrument, tradition, era, region | 📋 Planned |
| 3 | Links — curated performance and recording links | 📋 Planned |
| 4 | Recommendations + Player | 📋 Planned |
| 5 | Radio Stations | 📋 Planned |

---

## Tech Stack

- **Backend** — FastAPI (Python 3.12), SQLAlchemy 2.0, Alembic, Pydantic v2
- **Database** — PostgreSQL 16 + pgvector, Redis 7, Elasticsearch 8
- **Frontend** — Next.js 14, TypeScript, Tailwind CSS
- **Mobile** — React Native 0.74 (Phase 3+)
- **Infrastructure** — Docker Compose → Hetzner VPS → AWS (at scale)
- **Edge** — Cloudflare (WAF, DDoS, CDN)

---

## Data Sources

See [docs/references/](docs/references/) for the complete annotated list of all data sources, APIs, databases, and archives used to build NādaAtlas.

---

## License

Private repository. All rights reserved.
