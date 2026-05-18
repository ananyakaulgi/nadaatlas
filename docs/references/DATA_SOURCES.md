# NādaAtlas — Data Sources & References

Every piece of data in NādaAtlas is traceable to a primary source. This document is the canonical reference for all databases, APIs, archives, institutions, and libraries used across all phases.

Sources are grouped by type, then by musical tradition where applicable. Each entry includes: what data it provides, access method, cost, rate limits, and which ingestion job consumes it.

---

## Table of Contents

1. [Primary Music Databases](#1-primary-music-databases)
2. [Encyclopedic & Biographical Sources](#2-encyclopedic--biographical-sources)
3. [Audio & Video Link Sources](#3-audio--video-link-sources)
4. [World & Traditional Music Specialist Sources](#4-world--traditional-music-specialist-sources)
   - [South Asian Music](#41-south-asian-music)
   - [East Asian Music](#42-east-asian-music)
   - [Southeast Asian Music](#43-southeast-asian-music)
   - [Middle Eastern & Central Asian Music](#44-middle-eastern--central-asian-music)
   - [African Music](#45-african-music)
   - [Latin American & Caribbean Music](#46-latin-american--caribbean-music)
   - [European Folk & Classical](#47-european-folk--classical)
   - [North American Traditions](#48-north-american-traditions)
   - [Oceania](#49-oceania)
   - [Devotional & Sacred Music](#410-devotional--sacred-music)
5. [Institutional Archives & Libraries](#5-institutional-archives--libraries)
6. [Academic & Ethnomusicological Sources](#6-academic--ethnomusicological-sources)
7. [Instrument Databases](#7-instrument-databases)
8. [Image Sources](#8-image-sources)
9. [Lyrics & Notation Sources](#9-lyrics--notation-sources)
10. [Community & Aggregator Sources](#10-community--aggregator-sources)
11. [Source Reliability Tiers](#11-source-reliability-tiers)

---

## 1. Primary Music Databases

These are the backbone sources ingested daily by the core pipeline.

### MusicBrainz
- **URL:** https://musicbrainz.org
- **API:** https://musicbrainz.org/doc/MusicBrainz_API
- **What it provides:** Open music encyclopedia. Artists, releases, recordings, labels, relationships, ISRCs, MBIDs (stable unique identifiers). Coverage strongest for Western music; improving for world music.
- **Access:** Free, no API key. Requires User-Agent header identifying your application.
- **Rate limit:** 1 request/second. Exceeding results in temporary IP ban.
- **Data format:** JSON / XML
- **License:** CC0 (public domain)
- **Ingestion jobs:** `sync_musicbrainz_artists`, `sync_musicbrainz_releases`
- **Notes:** Use MBIDs as the universal artist/recording identifier across all sources. MusicBrainz is the authoritative cross-reference key.

### Wikidata
- **URL:** https://www.wikidata.org
- **SPARQL endpoint:** https://query.wikidata.org/sparql
- **What it provides:** Multilingual structured data for artists, instruments, genres, works. Best source for non-Western artists — often has data in native scripts (Hindi, Chinese, Arabic, Japanese) not available anywhere else.
- **Access:** Free, no key. SPARQL queries via HTTP GET.
- **Rate limit:** ~200 requests/second; heavy SPARQL queries may time out — keep targeted.
- **Data format:** JSON (SPARQL results)
- **License:** CC0
- **Ingestion jobs:** `sync_wikidata_artists`, `enrich_native_names`
- **Notes:** Critical for world music coverage. Query by instrument (e.g., all kora players), by tradition (e.g., all Carnatic musicians), by country. Returns native-language names essential for NādaAtlas.

### Discogs
- **URL:** https://www.discogs.com
- **API:** https://www.discogs.com/developers
- **What it provides:** 19M+ releases with pressing details, labels, country of origin, formats. Excellent for regional releases not in MusicBrainz. Strong world music, folk, ethnic releases.
- **Access:** Free (anonymous: 25 req/min; authenticated: 60 req/min). Register at discogs.com/settings/developers.
- **Rate limit:** 25 req/min unauthenticated, 60 req/min authenticated
- **Data format:** JSON
- **License:** CC BY-SA 3.0
- **Ingestion jobs:** `sync_discogs_releases`
- **Notes:** Best source for physical release metadata (vinyl, cassette). Useful for identifying regional pressing countries and labels that reveal musical tradition context.

### Last.fm
- **URL:** https://www.last.fm
- **API:** https://www.last.fm/api
- **What it provides:** Artist tags (community-applied genre/tradition labels), similar artists, listener counts, play counts. Tags are often more accurate for world music traditions than MusicBrainz genres.
- **Access:** Free API key. Register at last.fm/api/account/create.
- **Rate limit:** ~5 requests/second
- **Data format:** JSON
- **License:** Terms of Service (non-commercial research use permitted)
- **Ingestion jobs:** `sync_lastfm_tags`, `sync_lastfm_similar`
- **Notes:** Last.fm community tags like "hindustani classical," "kora," "gamelan" are invaluable for tradition classification. Use as enrichment layer on top of MusicBrainz data.

---

## 2. Encyclopedic & Biographical Sources

### Wikipedia (English)
- **URL:** https://en.wikipedia.org
- **API:** https://en.wikipedia.org/api/rest_v1/
- **What it provides:** Artist biographies, genre histories, instrument descriptions, tradition overviews.
- **Access:** Free, no key. Set descriptive User-Agent.
- **Rate limit:** 200 requests/second
- **Data format:** JSON (Parsoid HTML or plain text extract)
- **License:** CC BY-SA 4.0
- **Ingestion jobs:** `enrich_wikipedia_bios`
- **Notes:** Use `/page/summary/{title}` for clean biographical extracts. Always store `wikipedia_url` alongside bio text for attribution.

### Wikipedia (Multilingual — Critical for World Music)
- **URLs:**
  - Hindi: https://hi.wikipedia.org
  - Japanese: https://ja.wikipedia.org
  - Chinese (Simplified): https://zh.wikipedia.org
  - Arabic: https://ar.wikipedia.org
  - Korean: https://ko.wikipedia.org
  - Portuguese (Brazilian artists): https://pt.wikipedia.org
  - Spanish (Latin American artists): https://es.wikipedia.org
  - French (African artists): https://fr.wikipedia.org
  - Persian: https://fa.wikipedia.org
  - Turkish: https://tr.wikipedia.org
  - Tamil: https://ta.wikipedia.org
  - Telugu: https://te.wikipedia.org
  - Kannada: https://kn.wikipedia.org
  - Bengali: https://bn.wikipedia.org
- **What it provides:** Biographical data for artists whose primary coverage is in their native language — unavailable or minimal in English Wikipedia.
- **Access:** Same REST API, substitute language code in domain.
- **Ingestion jobs:** `enrich_multilingual_bios`
- **Notes:** A Carnatic vocalist may have 10 lines in English Wikipedia and 10 paragraphs in Tamil Wikipedia. Always query native-language Wikipedia first for non-Western artists.

### Grove Music Online (Oxford Music Online)
- **URL:** https://www.oxfordmusiconline.com/grovemusic
- **What it provides:** Authoritative scholarly articles on all musical traditions, instruments, composers, performers. The gold standard for musical scholarship.
- **Access:** Subscription required (~$395/year individual). Check if available via library access.
- **Data format:** Web (no public API — manual curation or licensed data)
- **License:** Proprietary
- **Usage:** Manual curation for instrument descriptions, tradition overviews. Not automated ingestion.
- **Notes:** Use Grove Music as the authoritative reference for writing instrument descriptions and tradition summaries. Cite it as a reference source on relevant pages.

### AllMusic
- **URL:** https://www.allmusic.com
- **What it provides:** Editorial biographies, genre classifications, album reviews, similar artists, mood/theme tags.
- **Access:** No public API. Data available via careful web scraping respecting robots.txt.
- **License:** Proprietary — use as reference for manual curation only.
- **Notes:** Useful editorial lens for Western popular music. Limited world music coverage.

---

## 3. Audio & Video Link Sources

### YouTube Data API v3
- **URL:** https://developers.google.com/youtube/v3
- **Console:** https://console.cloud.google.com
- **What it provides:** Video search, channel data, video metadata (title, duration, thumbnail, view count). Used to find official performances, recordings, and live concerts for every artist.
- **Access:** Free API key. Enable "YouTube Data API v3" in Google Cloud Console.
- **Rate limit:** 10,000 units/day free. Search = 100 units/query. Read = 1 unit/request.
- **Data format:** JSON
- **License:** YouTube Terms of Service. Embed-only (no download).
- **Ingestion jobs:** `fetch_youtube_links`
- **Notes:** Search queries: `"{artist name} official"`, `"{artist name} concert"`, `"{artist name} {tradition} performance"`. For non-Western artists, also search in native script: `"रवि शंकर"`, `"小泽征尔"`.

### Spotify Web API
- **URL:** https://developer.spotify.com
- **Dashboard:** https://developer.spotify.com/dashboard
- **What it provides:** Track metadata, album art (high quality), artist images, preview clips (30-second audio), audio features (tempo, key, energy, danceability — used for Phase 4 recommendations), related artists.
- **Access:** Free. Register app, obtain Client ID + Secret. Use Client Credentials flow for metadata (no user login required).
- **Rate limit:** ~100 requests/second with Client Credentials
- **Data format:** JSON
- **License:** Spotify Developer Terms. No downloading. Embed via Spotify Web Playback SDK.
- **Ingestion jobs:** `sync_spotify_metadata`, `fetch_spotify_audio_features`
- **Notes:** Spotify artist images are the best quality freely available. Audio features (valence, energy, acousticness) are critical for Phase 4 recommendation engine.

### SoundCloud API
- **URL:** https://developers.soundcloud.com
- **What it provides:** Independent artist tracks, world music uploads, traditional recordings not on Spotify/YouTube. Often has rare regional content.
- **Access:** Free API key. Apply at soundcloud.com/you/apps.
- **Rate limit:** 15,000 requests/hour
- **Data format:** JSON
- **Ingestion jobs:** `fetch_soundcloud_links`

### Bandcamp
- **URL:** https://bandcamp.com
- **What it provides:** Independent and regional artists — particularly strong for folk, traditional, and world music genres that major platforms underserve.
- **Access:** No official public API. Links discovered via search and MusicBrainz URL relationships.
- **Ingestion jobs:** Populated via MusicBrainz URL relationships (MusicBrainz stores Bandcamp links for artists)

### Internet Archive (archive.org)
- **URL:** https://archive.org
- **API:** https://archive.org/developers/internetarchive/api/
- **What it provides:** Historical recordings, out-of-copyright music, ethnomusicological field recordings, live concert recordings. Exceptional for pre-1950 world music.
- **Access:** Free, no key for read access.
- **Data format:** JSON metadata + direct audio file links
- **License:** Varies per item (mostly CC or public domain)
- **Ingestion jobs:** `fetch_archive_recordings`
- **Notes:** Invaluable for historical recordings of traditional music. Smithsonian Folkways content, Alan Lomax field recordings, and many ethnomusicological archives are hosted here.

---

## 4. World & Traditional Music Specialist Sources

### 4.1 South Asian Music

#### Sangeet Natak Akademi
- **URL:** https://www.sangeetnatak.gov.in
- **What it provides:** India's national academy for music, dance, and drama. Artist award recipients (Akademi Award, Sangeet Natak Akademi Fellowship), biographical records, tradition documentation.
- **Access:** Web (manual curation). No public API.
- **Notes:** Official Indian government recognition database. Highest authority for verifying Indian classical musician credentials.

#### Swarganga School of Music
- **URL:** https://www.swarganga.org
- **What it provides:** Hindustani classical raga database, taal reference, gharana genealogies, musician biographies. Searchable by raga, taal, gharana.
- **Access:** Web (manual curation + structured data scraping)
- **Notes:** Best free resource for Hindustani raga metadata. Use for `musical_tradition` classification of Indian classical tracks.

#### Carnatica
- **URL:** https://www.carnatica.net
- **What it provides:** Carnatic music compositions, raga reference, krithi texts, concert recordings database.
- **Access:** Web (manual curation)

#### Raag Hindustani
- **URL:** https://www.raag-hindustani.com
- **What it provides:** Educational resource for Hindustani ragas — raga characteristics, time of day, season, associated emotions (rasa). Critical for metadata enrichment.
- **Access:** Web

#### ITC Sangeet Research Academy
- **URL:** https://www.itcsra.org
- **What it provides:** Documentation of Hindustani classical gharanas, maestro biographies, archival recordings.
- **Access:** Web (manual curation)

#### Saptak Annual Music Festival Archive
- **URL:** https://www.saptak.org
- **What it provides:** Performance records, artist lists from one of India's premier classical music festivals.

#### Sur Sagar (Pakistan Music Archive)
- **URL:** Research via PTV (Pakistan Television) archives and Radio Pakistan archives
- **What it provides:** Pakistani classical and folk music documentation

---

### 4.2 East Asian Music

#### Ongaku No Tomo Sha (Japan)
- **URL:** https://www.ongakunotomo.co.jp
- **What it provides:** Japanese music publisher and database — traditional and classical Japanese music scores, artist records.

#### National Gugak Center (Korea)
- **URL:** https://www.gugak.go.kr/en
- **What it provides:** Korean traditional music (국악) documentation, artist biographies, instrument descriptions, audio-visual archive.
- **Access:** Web + partial API for archive access.
- **Notes:** Official Korean government institution. Authoritative source for Korean classical music.

#### China Music Information Center
- **URL:** http://www.cmic.org.cn
- **What it provides:** Chinese music documentation — traditional instruments, regional styles, composer records.

#### Traditional Music of Japan (NHK Archives)
- **URL:** https://www.nhk.or.jp/archives
- **What it provides:** NHK broadcast archives of Japanese traditional music performances — gagaku, koto, shamisen, noh.

#### Traditional Music Archive — SOAS University of London
- **URL:** https://www.soas.ac.uk/musicology
- **What it provides:** Academic recordings and documentation of East and Southeast Asian music traditions.

#### Music Research Institute — Chinese Academy of Arts
- **URL:** Research via Wikidata and academic publications

#### Korean Music Archive (한국음악아카이브)
- **URL:** https://www.gugakarchive.kr
- **What it provides:** Digital archive of Korean traditional music recordings, scores, and performance documentation.

---

### 4.3 Southeast Asian Music

#### SOAS Ethnomusicology Archive (Southeast Asia)
- **URL:** https://www.soas.ac.uk
- **What it provides:** Field recordings, academic documentation of Southeast Asian traditions — gamelan, piphat, kulintang.

#### Gamelan Archive — University of Washington
- **URL:** https://ethnomusicology.washington.edu
- **What it provides:** Extensive gamelan documentation, instrument photographs, performance recordings.

#### Vietnam National Academy of Music
- **URL:** https://hvanvn.edu.vn
- **What it provides:** Vietnamese traditional music documentation, artist records.

#### Center for Khmer Studies
- **URL:** https://khmerstudies.org
- **What it provides:** Cambodian music documentation, pin peat ensemble records.

#### Indonesian Directorate General of Culture
- **URL:** https://kebudayaan.kemdikbud.go.id
- **What it provides:** Official Indonesian cultural heritage database including gamelan traditions, regional music.

---

### 4.4 Middle Eastern & Central Asian Music

#### Arab Music Encyclopedia
- **URL:** https://www.arabicmusicencyclopedia.com
- **What it provides:** Arabic maqam reference, artist biographies, historical recordings.

#### Radif of Iranian Music (UNESCO)
- **URL:** https://ich.unesco.org/en/RL/radif-of-iranian-music-00279
- **What it provides:** Documentation of Persian classical music's radif (repertoire system). UNESCO Intangible Cultural Heritage.

#### Aga Khan Music Initiative
- **URL:** https://www.akdn.org/our-agencies/aga-khan-trust-for-culture/music-initiative
- **What it provides:** Central Asian and Middle Eastern music documentation, artist biographies, recordings. Focus on Tajik, Uzbek, Afghan, and broader Central Asian traditions.

#### AMAR Foundation for Arab Music Archiving and Research
- **URL:** https://www.amar-foundation.org
- **What it provides:** Archive of golden-age Arab music (1900–1975), biographies, recordings. Exceptional historical depth.
- **Notes:** Best source for early 20th century Arab music documentation.

#### Turkish Music Portal (TRT Arşivi)
- **URL:** https://muzik.trt.com.tr
- **What it provides:** Turkish Radio and Television archives — Turkish classical (makam), folk, Anatolian recordings.

#### Azerbaijan National Conservatory Archives
- **URL:** Via Wikidata and academic publications
- **What it provides:** Mugham documentation, ashug tradition, Azerbaijani instrument records.

#### SOAS Middle East Music Archive
- **URL:** https://www.soas.ac.uk/musicology
- **What it provides:** Academic field recordings from the Middle East and Central Asia.

---

### 4.5 African Music

#### African Music Encyclopedia (ILAM)
- **URL:** https://www.ru.ac.za/ilam
- **What it provides:** International Library of African Music at Rhodes University, South Africa. Largest archive of African music in the world. Field recordings, instrument documentation, artist records across all sub-Saharan traditions.
- **Notes:** World's most authoritative source for African traditional music documentation.

#### Smithsonian Folkways — African Catalogue
- **URL:** https://folkways.si.edu
- **What it provides:** Curated African music recordings with extensive liner notes and cultural documentation. Covers all regions of Africa.
- **Access:** Free metadata API. Audio via subscription.

#### African Music Research (SOAS)
- **URL:** https://www.soas.ac.uk/music/research
- **What it provides:** Academic documentation of West African, East African, and Southern African traditions.

#### Griot Database — West African Oral Tradition
- **URL:** Research via https://www.griots.org and academic sources
- **What it provides:** Genealogical and biographical records of West African griot families and their oral tradition repertoires.

#### African Music Archive (Universität Mainz)
- **URL:** https://www.uni-mainz.de/eng/
- **What it provides:** German academic archive of African music field recordings.

#### Ethiopia Music Database
- **URL:** Research via Wikidata, ethnomusicological publications
- **What it provides:** Ethiopian musical traditions — Tizita, Gurage music, Dorze tradition, Beta Israel liturgical music.

#### Nollywood & Afrobeats Archives
- **URL:** https://www.audiomack.com (for contemporary), academic sources for historical
- **What it provides:** Nigerian music documentation — highlife, jùjú, fújì, afrobeats timeline.

#### Gnawa Music Archive (Morocco)
- **URL:** Research via UNESCO ICH database: https://ich.unesco.org/en/RL/gnawa-music-01178
- **What it provides:** Gnawa spiritual music documentation — UNESCO Intangible Cultural Heritage.

---

### 4.6 Latin American & Caribbean Music

#### Biblioteca Nacional de Brasil
- **URL:** https://www.bn.gov.br
- **What it provides:** Brazilian music archive — choro, samba, bossa nova historical documentation.

#### Museu do Samba (Rio de Janeiro)
- **URL:** https://www.museudosamba.org.br
- **What it provides:** Samba school histories, sambistas biographies, samba styles documentation.

#### SADAIC (Argentine Authors & Composers Society)
- **URL:** https://www.sadaic.org.ar
- **What it provides:** Argentine music composers registry, tango documentation.

#### BIEM / Latin Music Societies
- **URL:** Research via BIEM member organizations per country
- **What it provides:** Composers' society registries — useful for verifying Latin American composers.

#### Andean Music Archive (Centro de Etnomusicología Andina)
- **URL:** Research via Pontificia Universidad Católica del Peru archives
- **What it provides:** Andean music documentation — huayno, marinera, sanjuanito, sikuri pan flute traditions.

#### Cuba Music Archive (EGREM)
- **URL:** https://www.egrem.com.cu
- **What it provides:** Official Cuban state music label archives — son cubano, rumba, danzón historical recordings.

#### Cubadisco Archive
- **URL:** https://www.cubadisco.com
- **What it provides:** Comprehensive Cuban discography database.

#### Smithsonian Folkways — Latin America & Caribbean
- **URL:** https://folkways.si.edu
- **What it provides:** Field recordings and liner notes for Andean, Caribbean, Afro-Latin traditions.

#### Biblioteca Nacional de Colombia
- **URL:** https://www.bibliotecanacional.gov.co
- **What it provides:** Colombian music documentation — cumbia, vallenato, porro historical records.

#### Roots Reggae Archive (Jamaica)
- **URL:** Research via https://www.reggaearchive.com and Jamaican Music Museum records
- **What it provides:** Reggae, ska, rocksteady, dancehall artist documentation.

---

### 4.7 European Folk & Classical

#### IMSLP (Petrucci Music Library)
- **URL:** https://imslp.org
- **What it provides:** World's largest library of public domain music scores — Western classical from medieval to early 20th century. 700,000+ scores.
- **Access:** Free. No API (web scraping respecting robots.txt).
- **License:** Public domain / CC
- **Notes:** Essential for classical music notation data. Confirms composer names, work titles, opus numbers.

#### Discogs Classical Catalogue
- **URL:** https://www.discogs.com/search?genre=Classical
- **What it provides:** Classical music release data — performances, conductors, orchestras, recording dates.

#### Norsk Folkemusikksamling (Norwegian Folk Music Collection)
- **URL:** https://www.uio.no/english/research/interdisciplinary-research-areas/music-folk
- **What it provides:** Norwegian folk music archive — hardanger fiddle, slått, bygdedans documentation.

#### Musikverket (Sweden)
- **URL:** https://musikverket.se
- **What it provides:** Swedish music heritage archive — folk music, visa, polska documentation.

#### Folk Music Archive Finland (Kansanmusiikki-instituutti)
- **URL:** https://www.kansanmusiikki-instituutti.fi
- **What it provides:** Finnish folk music — kantele, joik, runo-song documentation.

#### Sámi Cultural Archive (Ája)
- **URL:** https://sami-arkiiva.no
- **What it provides:** Sámi joik archive — personal songs, yoik documentation. UNESCO Intangible Cultural Heritage.

#### Irish Traditional Music Archive (ITMA)
- **URL:** https://www.itma.ie
- **What it provides:** The national archive of Irish traditional music. Tunes, songs, dances, recordings, biographies.
- **Notes:** Finest specialist archive for Celtic music. Open access for research.

#### Scottish Traditional Music Archive
- **URL:** https://www.tobarandualchais.co.uk
- **What it provides:** Tobar an Dualchais (Well of Heritage) — Scottish Gaelic song and story archive.

#### Archivo del Cante Flamenco (Spain)
- **URL:** Research via Centro Andaluz de Flamenco: https://www.centroandaluzdeflamenco.es
- **What it provides:** Flamenco styles (palos), cantaores, guitarristas documentation. Official Andalusian government archive.

#### Arquivo do Fado (Portugal)
- **URL:** https://www.museudofado.pt
- **What it provides:** Fado Museum archive — fadistas biographies, fado styles, historical recordings.

#### Bulgarian State Archive of Folk Music
- **URL:** Research via Bulgarian Academy of Sciences ethnomusicology department
- **What it provides:** Bulgarian polyphonic folk music, wedding music documentation.

#### Romani Music Archive (Université de Paris)
- **URL:** Research via academic publications and ICTM
- **What it provides:** Romani musical traditions — manele, brass band music, jazz manouche roots.

---

### 4.8 North American Traditions

#### Blues Archive — University of Mississippi
- **URL:** https://blues.olemiss.edu
- **What it provides:** World's largest collection of blues music research materials. Artist documentation, field recordings.

#### Alan Lomax Archive (Association for Cultural Equity)
- **URL:** https://www.culturalequity.org
- **What it provides:** Landmark field recordings of American folk, blues, Appalachian, and world music traditions. Mid-20th century recordings now public domain.
- **Access:** https://archive.org/details/alan-lomax-collection
- **Notes:** Irreplaceable. Lomax recorded music traditions that would otherwise be lost — Appalachian shape-note, Mississippi blues, Cuban son, Caribbean folk.

#### Smithsonian Folkways (USA)
- **URL:** https://folkways.si.edu
- **API:** https://folkways.si.edu/api
- **What it provides:** 50,000+ recordings with detailed liner notes — American folk, blues, jazz, Native American, world traditions. Scholarly curation.
- **Access:** Free metadata API. Audio via subscription.
- **License:** Smithsonian Terms of Service

#### Native American Music Archive (NMAI)
- **URL:** https://americanindian.si.edu
- **What it provides:** Smithsonian National Museum of the American Indian — Native American musical traditions, ceremonial music documentation, artist records.
- **Notes:** Approach with cultural sensitivity. Some ceremonial recordings are restricted by tribal consent protocols.

#### American Folklife Center (Library of Congress)
- **URL:** https://www.loc.gov/folklife
- **What it provides:** Archive of American folk music — over 4 million items. Appalachian, Cajun, Tejano, Native American, blues, gospel field recordings.
- **Access:** https://www.loc.gov/collections/american-folklife-center-collections

#### Jazz at Lincoln Center Archive
- **URL:** https://www.jazz.org
- **What it provides:** Jazz biographies, historical documentation, performance records.

#### New Orleans Jazz Museum
- **URL:** https://www.nolajazzmuseum.org
- **What it provides:** New Orleans jazz documentation, artist histories, recording archives.

---

### 4.9 Oceania

#### PARADISEC (Pacific and Regional Archive for Digital Sources in Endangered Cultures)
- **URL:** https://www.paradisec.org.au
- **What it provides:** 16,000+ hours of recordings from the Pacific region — Papua New Guinea, Vanuatu, Solomon Islands, Indonesia, Australia. Field recordings of endangered musical traditions.
- **Access:** Free for research. Some items restricted.
- **Notes:** Critical source for Melanesian, Micronesian, and Polynesian traditional music not documented anywhere else.

#### AIATSIS (Australian Institute of Aboriginal and Torres Strait Islander Studies)
- **URL:** https://aiatsis.gov.au
- **What it provides:** Aboriginal Australian music documentation — songlines, ceremonial music, didgeridoo traditions. Largest collection of indigenous Australian cultural material in the world.
- **Access:** Free catalogue access. Some recordings restricted by community protocols.
- **Notes:** Cultural sensitivity required. Many recordings are restricted and require community permission to use.

#### Te Ara — Encyclopedia of New Zealand
- **URL:** https://teara.govt.nz
- **What it provides:** Māori music documentation — waiata, haka, traditional instruments, contemporary Māori artists.

#### Ethnomusicology Collection — University of Auckland
- **URL:** Research via university library
- **What it provides:** Pacific music field recordings, Polynesian music documentation.

#### Bishop Museum (Hawaii)
- **URL:** https://www.bishopmuseum.org
- **What it provides:** Hawaiian music documentation — hula, slack-key guitar, traditional chant (oli), ukulele history.

---

### 4.10 Devotional & Sacred Music

#### Gregorian Chant Archive (Cantus Database)
- **URL:** https://cantus.uwaterloo.ca
- **What it provides:** Database of medieval chant manuscripts — antiphons, responsories, hymns from Catholic liturgical tradition.
- **Access:** Free, searchable.

#### Thesaurus Musicarum Latinarum
- **URL:** https://chmtl.indiana.edu/tml
- **What it provides:** Latin music theory texts from the medieval and Renaissance periods.

#### Tibet Music Archive (Shambhala Archives)
- **URL:** Research via https://www.tbrc.org (Buddhist Digital Resource Center)
- **What it provides:** Tibetan Buddhist music documentation — ritual chant, monastic music, Tibetan opera (lhamo).

#### Sikh Heritage Archive (Shiromani Gurdwara Parbandhak Committee)
- **URL:** Research via https://www.sgpc.net
- **What it provides:** Sikh kirtan documentation — ragas of Guru Granth Sahib, prominent ragis (kirtan performers) biographies.

#### Sufi Music Archive
- **URL:** Research via https://www.sufismus.ch and academic sources
- **What it provides:** Sufi sama and qawwali documentation, major dargah performance records.

#### Jewish Music Research Centre (Hebrew University)
- **URL:** https://www.jewish-music.huji.ac.il
- **What it provides:** Comprehensive Jewish music documentation — cantorial music, Sephardic songs, Yemenite traditions, klezmer, Hasidic niggunim.

#### Orthodox Christian Music Archive (Byzantine Chant)
- **URL:** https://www.ibyzantine.net and https://www.analogion.com
- **What it provides:** Byzantine chant documentation — eight-mode system (octoechos), hagiopolitan chant, liturgical music of Eastern Orthodox churches.

---

## 5. Institutional Archives & Libraries

### Smithsonian Institution
- **URL:** https://www.si.edu
- **Folkways:** https://folkways.si.edu
- **What it provides:** Comprehensive global music coverage across Smithsonian Folkways label. 50,000+ recordings. Strongest specialist source for non-Western and endangered traditions.
- **Notes:** Folkways has a metadata API. Liner notes are scholarly and citable.

### Library of Congress — Music Division
- **URL:** https://www.loc.gov/music
- **What it provides:** World's largest music collection. Historical recordings, scores, ethnomusicological archives, Alan Lomax collection.

### British Library Sound Archive
- **URL:** https://www.bl.uk/collection-guides/sound-archive
- **What it provides:** 6.5 million recordings — world's largest public sound archive. Strong South Asian, Caribbean, and African collections from Commonwealth-era field recordings.

### Bibliothèque nationale de France — Music Department
- **URL:** https://gallica.bnf.fr
- **What it provides:** French music heritage — medieval manuscripts to contemporary. Strong North African coverage.

### IRCAM (Institut de Recherche et Coordination Acoustique/Musique)
- **URL:** https://www.ircam.fr
- **What it provides:** Contemporary and experimental music documentation. Catalogue of 20th/21st century composers.

### Ethnologisches Museum Berlin (Phonogrammarchiv)
- **URL:** https://www.smb.museum/en/museums-institutions/ethnologisches-museum
- **What it provides:** One of the oldest ethnomusicological archives in the world. Field recordings from Africa, Asia, and the Pacific from 1900 onwards.

### Vienna Phonogrammarchiv (Austrian Academy of Sciences)
- **URL:** https://www.oeaw.ac.at/phonogrammarchiv
- **What it provides:** Historic phonographic recordings — late 19th and early 20th century world music field recordings. UNESCO Memory of the World.

---

## 6. Academic & Ethnomusicological Sources

### ICTM (International Council for Traditional Music)
- **URL:** https://www.ictmusic.org
- **What it provides:** Global authority on traditional and folk music research. Study group publications, conference proceedings, world music documentation. Member national committees provide country-level expertise.
- **Notes:** Not a data API — use for manual curation and as a reference authority for tradition classification.

### Society for Ethnomusicology (SEM)
- **URL:** https://www.ethnomusicology.org
- **What it provides:** Academic journal (Ethnomusicology), directory of ethnomusicologists, research resources.
- **Notes:** Best academic body for verification of non-Western music traditions. Cross-reference classifications with SEM publications.

### JSTOR Global Plants / RILM Abstracts of Music Literature
- **URL:** https://rilm.org
- **What it provides:** RILM is the most comprehensive index of music literature — 1.2 million records. Essential for verifying facts about obscure traditions.
- **Access:** Subscription required. Check library access.

### Ethnomusicology Review (UCLA)
- **URL:** https://ethnomusicologyreview.ucla.edu
- **What it provides:** Open-access academic articles on world music traditions.

### Music Traditions (UK)
- **URL:** https://www.mustrad.org.uk
- **What it provides:** British folk and world music documentation.

---

## 7. Instrument Databases

### Hornbostel-Sachs Classification System
- **Reference:** Hornbostel, E.M. von, and C. Sachs. 1914. "Systematik der Musikinstrumente." Zeitschrift für Ethnologie 46:553–90.
- **What it provides:** The universal instrument classification system used by NādaAtlas. All instruments are classified as: Chordophones (strings), Aerophones (wind), Membranophones (drums), Idiophones (self-sounding), Electrophones (electronic).
- **Online reference:** https://www.mimo-international.com/MIMO/instrument-classification/hornbostel-sachs.aspx

### MIMO (Musical Instrument Museums Online)
- **URL:** https://www.mimo-international.com
- **What it provides:** Consortium of European instrument museums. 50,000+ instrument records with photographs, Hornbostel-Sachs classifications, descriptions.
- **Access:** Free searchable database + API.
- **Notes:** Best source for instrument images, physical descriptions, and historical context across all world traditions.

### Edinburgh University Collection of Historic Musical Instruments
- **URL:** https://collections.ed.ac.uk/mimed
- **What it provides:** Instrument database with photographs and detailed descriptions.

### Musical Instrument Museum (MIM) Phoenix
- **URL:** https://mim.org
- **What it provides:** Instruments from 200+ countries with cultural context. Good for non-Western instrument photography and descriptions.

### Grinnell College Musical Instrument Collection
- **URL:** https://omeka.grinnell.edu/s/MusicalInstruments
- **What it provides:** Open-access instrument database with cultural documentation.

### Sitar, Sarod, Tabla Reference (Buckingham)
- **URL:** Research via academic publications
- **What it provides:** Detailed construction and classification of South Asian instruments.

---

## 8. Image Sources

### Wikimedia Commons
- **URL:** https://commons.wikimedia.org
- **API:** https://www.mediawiki.org/wiki/API:Main_page
- **What it provides:** Free-licensed images for artists, instruments, album covers (historical), venues. Many South Asian, African, and Latin American musician photographs.
- **Access:** Free, no key. Query via MediaWiki API.
- **License:** CC BY-SA, CC BY, Public Domain (verified per image)
- **Ingestion jobs:** `fetch_artist_images`
- **Notes:** Always store license type, author, and source URL alongside each image for proper attribution.

### MusicBrainz Cover Art Archive
- **URL:** https://coverartarchive.org
- **API:** https://coverartarchive.org/doc
- **What it provides:** Album cover art linked to MusicBrainz releases. Community-submitted, openly licensed.
- **Access:** Free, no key.
- **License:** Varies (CC BY, CC BY-SA, public domain)

### Spotify Artist Images
- **URL:** Via Spotify Web API (artist.images array)
- **What it provides:** High-resolution artist photographs. Best quality of any automated source.
- **License:** Spotify ToS — display only, no permanent storage of images.
- **Notes:** Cache image URLs; do not rehost Spotify images. Refresh URLs on expiry.

### Last.fm Artist Images
- **URL:** Via Last.fm API (artist.getInfo)
- **What it provides:** Artist photographs submitted by community.

---

## 9. Lyrics & Notation Sources

### IMSLP (Western Classical Scores)
- **URL:** https://imslp.org
- **What it provides:** 700,000+ public domain classical music scores. Bach, Beethoven, Mozart, and thousands more.

### Musopen
- **URL:** https://musopen.org/api
- **What it provides:** Free public domain classical music scores and recordings.
- **Access:** Free API key.

### Hindustani Classical Bandish Database
- **URL:** Research via Swarganga and Sangeet Natak Akademi
- **What it provides:** Compositions (bandishes) in Hindustani ragas with notation in sargam.

### Carnatic Compositions Archive
- **URL:** https://www.karnatik.com
- **What it provides:** Carnatic music compositions — krithi texts, raga classifications, composer biographies.

### Genius (Contemporary Lyrics)
- **URL:** https://genius.com/api-clients
- **What it provides:** Lyrics for contemporary music. API available.
- **License:** Fair use for display; do not redistribute in bulk.

### Musixmatch
- **URL:** https://developer.musixmatch.com
- **What it provides:** 100M+ song lyrics in multiple languages. Best source for non-English lyrics — useful for multilingual world music content.
- **Access:** Free tier: 2,000 requests/day.

---

## 10. Community & Aggregator Sources

### Rate Your Music (Sonemic)
- **URL:** https://rateyourmusic.com
- **What it provides:** Community genre classifications, release ratings, artist connections. Strong world music tagging. No public API — manual curation only.

### AllMusic Genre Hierarchy
- **URL:** https://www.allmusic.com/genres
- **What it provides:** Editorial genre taxonomy — useful as a reference for building NādaAtlas's own genre/tradition hierarchy.

### Every Noise at Once
- **URL:** https://everynoise.com
- **What it provides:** Spotify's genre map — 6,000+ genre categories with representative tracks. Excellent for identifying microgenres and regional styles.
- **Notes:** Use as reference for genre taxonomy. Not an API — manual curation.

### Setlist.fm
- **URL:** https://api.setlist.fm/docs/1.0
- **What it provides:** 9.6M+ concert setlists — tracks performed, venue, date, city. Useful for performance history and identifying which songs an artist regularly performs.
- **Access:** Free API key.
- **Ingestion jobs:** `fetch_setlists` (Phase 3+)

### Songkick
- **URL:** https://www.songkick.com/developer
- **What it provides:** Concert and tour data — historical and upcoming performances. Venue information.
- **Access:** Free API key (apply at songkick.com/developer).

---

## 11. Source Reliability Tiers

Not all sources are equal. NādaAtlas uses a three-tier reliability system for all data:

| Tier | Label | Description | Examples |
|------|-------|-------------|---------|
| **Tier 1** | Authoritative | Official government institutions, national academies, UNESCO heritage documentation, major academic archives | Sangeet Natak Akademi, ILAM, National Gugak Center, Library of Congress, Smithsonian Folkways |
| **Tier 2** | Reliable | Well-maintained specialist databases, established music institutions, peer-reviewed academic sources | MusicBrainz, Wikidata, IMSLP, ITMA, Grove Music Online, ICTM publications |
| **Tier 3** | Community | Community-maintained databases, editorial sources, aggregators | Wikipedia, Last.fm tags, Discogs, AllMusic, Rate Your Music |

Data from lower tiers is accepted only when:
- No Tier 1 or Tier 2 source covers the artist/tradition
- Multiple Tier 3 sources agree
- The data can be cross-verified against other sources

All data stored in NādaAtlas includes a `source_tier` and `source_url` field so users can evaluate the provenance of any fact.

---

## Attribution Requirements

NādaAtlas is committed to proper attribution of all data sources. Every page that uses data from an external source displays:
- Source name
- Source URL
- License (where applicable)
- Date of last sync

This is both an ethical requirement and a legal one for sources licensed under Creative Commons Attribution terms.

---

*This document is maintained alongside the codebase. When a new data source is added to the ingestion pipeline, it must be documented here before the PR is merged.*

*Last updated: May 2026*
