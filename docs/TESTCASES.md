# NādaAtlas — Test Cases

Manual and automated test cases organized by phase. Each phase includes its own functional tests plus integration tests that verify cross-phase behaviour as the system grows.

Legend: ✅ Pass | ❌ Fail | ⏭ Skip (dependency not built yet) | 🔄 In Progress

---

## Phase 1 — Encyclopedia API + Data Ingestion

### 1.1 Infrastructure Smoke Tests

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-INF-01 | API health check | `GET /health` | `{"status":"ok","version":"0.1.0"}` | |
| P1-INF-02 | API degraded when DB down | Stop postgres, `GET /health` | 503 with `{"status":"degraded"}` | |
| P1-INF-03 | Swagger UI loads | Open `http://localhost:8000/api/docs` | All routes render, no console errors | |
| P1-INF-04 | ReDoc loads | Open `http://localhost:8000/api/redoc` | Documentation renders | |
| P1-INF-05 | All containers running | `docker compose ps` | 6 services show "running" | |
| P1-INF-06 | Database migration applied | `docker compose exec api alembic current` | Shows revision `001` | |
| P1-INF-07 | pgvector extension present | Query `SELECT * FROM pg_extension WHERE extname='vector'` in Adminer | Row returned | |
| P1-INF-08 | Request ID in every response | `curl -i http://localhost:8000/health` | `X-Request-ID` header present | |
| P1-INF-09 | Security headers present | Check any response headers | `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy` all present | |

---

### 1.2 Authentication

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-AUTH-01 | Valid login returns tokens | `POST /api/v1/auth/token` with correct credentials | 200, `access_token` + `refresh_token` returned | |
| P1-AUTH-02 | Wrong password | `POST /api/v1/auth/token` wrong password | 401, generic error message | |
| P1-AUTH-03 | Non-existent email | `POST /api/v1/auth/token` fake email | 401, **same** error message as wrong password | |
| P1-AUTH-04 | Empty password | `POST /api/v1/auth/token` blank password | 422 validation error | |
| P1-AUTH-05 | Token refresh | `POST /api/v1/auth/refresh` with valid refresh token | 200, new access token | |
| P1-AUTH-06 | Refresh using access token | `POST /api/v1/auth/refresh` with access token | 401 | |
| P1-AUTH-07 | Logout blacklists token | `POST /api/v1/auth/logout`, reuse same token | 401 on reuse | |
| P1-AUTH-08 | Get current user | `GET /api/v1/auth/me` with valid token | 200, user info returned | |
| P1-AUTH-09 | Account lockout triggers | Wrong password 5 times consecutively | 401 with lockout message on 5th attempt | |
| P1-AUTH-10 | Lockout expires | Wait 15 min after lockout, correct password | 200, login succeeds | |
| P1-AUTH-11 | Expired token rejected | Use token after 30-minute TTL | 401 | |
| P1-AUTH-12 | Malformed token rejected | `Authorization: Bearer garbage123` | 401 | |
| P1-AUTH-13 | Missing Authorization header | Call protected endpoint without header | 401 | |

---

### 1.3 Authorization

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-AUTHZ-01 | Public reads require no token | `GET /api/v1/artists` without token | 200 | |
| P1-AUTHZ-02 | Create requires token | `POST /api/v1/artists` without token | 401 | |
| P1-AUTHZ-03 | Update requires token | `PUT /api/v1/artists/{id}` without token | 401 | |
| P1-AUTHZ-04 | Delete requires token | `DELETE /api/v1/artists/{id}` without token | 401 | |
| P1-AUTHZ-05 | Valid token allows create | `POST /api/v1/artists` with Bearer token | 201 | |
| P1-AUTHZ-06 | Superuser-only actions blocked for regular user | Non-superuser attempts admin action | 403 | |

---

### 1.4 Musical Traditions

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-TRAD-01 | Create with all fields | POST with name, name_native, region, subregion, description, origin_period | 201, UUID returned | |
| P1-TRAD-02 | Create with only required fields | POST with name and region only | 201 | |
| P1-TRAD-03 | Duplicate name rejected | POST same name twice | 409 or 422 | |
| P1-TRAD-04 | Missing required field | POST without `name` | 422 validation error | |
| P1-TRAD-05 | Native script stored correctly | POST with `name_native: "हिन्दुस्तानी शास्त्रीय संगीत"` | GET returns exact same string | |
| P1-TRAD-06 | Get by ID | `GET /api/v1/traditions/{id}` | 200, correct object | |
| P1-TRAD-07 | Get non-existent | `GET /api/v1/traditions/{fake-uuid}` | 404 | |
| P1-TRAD-08 | Get invalid UUID format | `GET /api/v1/traditions/not-a-uuid` | 422 | |
| P1-TRAD-09 | List all paginated | `GET /api/v1/traditions` | 200, paginated list with total count | |
| P1-TRAD-10 | Filter by region | `GET /api/v1/traditions?region=South Asia` | Only South Asian traditions | |
| P1-TRAD-11 | Pagination skip/limit | `GET /api/v1/traditions?skip=0&limit=2` | Max 2 results | |
| P1-TRAD-12 | Limit cap enforced | `GET /api/v1/traditions?limit=999` | Max 100 results returned | |
| P1-TRAD-13 | Update field | `PUT /api/v1/traditions/{id}` with new description | 200, field updated in response | |
| P1-TRAD-14 | Soft delete | `DELETE /api/v1/traditions/{id}` | 200 or 204 | |
| P1-TRAD-15 | Soft-deleted not in list | `GET /api/v1/traditions` after delete | Deleted tradition absent | |
| P1-TRAD-16 | Soft-deleted not fetchable | `GET /api/v1/traditions/{deleted-id}` | 404 | |

---

### 1.5 Instruments

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-INST-01 | Create with Hornbostel-Sachs | POST with `hornbostel_sachs: "321.321"` | 201, stored and returned | |
| P1-INST-02 | Create with native name | POST with `name_native: "सितार"` | Stored and returned correctly | |
| P1-INST-03 | Link to tradition | POST with valid `tradition_id` | Response includes embedded `TraditionSummary` | |
| P1-INST-04 | Link to non-existent tradition | POST with fake `tradition_id` | 404 or 422 | |
| P1-INST-05 | Filter by hs_category | `GET /api/v1/instruments?hs_category=chordophone` | Only chordophones returned | |
| P1-INST-06 | Filter by tradition | `GET /api/v1/instruments?tradition_id={uuid}` | Only that tradition's instruments | |
| P1-INST-07 | Get by ID | `GET /api/v1/instruments/{id}` | 200, full object | |
| P1-INST-08 | Soft delete | `DELETE /api/v1/instruments/{id}` | 200 or 204, not in list after | |

---

### 1.6 Artists

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-ART-01 | Create with native name | POST `name: "Ravi Shankar"`, `name_native: "रवि शंकर"` | 201, both names stored | |
| P1-ART-02 | List returns summary only | `GET /api/v1/artists` | Returns ArtistSummary (no full biography field) | |
| P1-ART-03 | Detail returns full biography | `GET /api/v1/artists/{id}` | Returns ArtistDetail with `biography` field | |
| P1-ART-04 | Search by name | `GET /api/v1/artists/search?q=ravi` | Returns matching artists | |
| P1-ART-05 | Search case insensitive | `GET /api/v1/artists/search?q=RAVI` | Same results as lowercase | |
| P1-ART-06 | Search no results | `GET /api/v1/artists/search?q=zzznomatch` | Empty list, not 404 | |
| P1-ART-07 | Search endpoint not confused with UUID | `GET /api/v1/artists/search?q=test` | Does not 422 treating "search" as UUID | |
| P1-ART-08 | Filter by musical_tradition | `GET /api/v1/artists?musical_tradition=Carnatic` | Only Carnatic artists | |
| P1-ART-09 | Filter by nationality | `GET /api/v1/artists?nationality=Indian` | Only Indian artists | |
| P1-ART-10 | tradition field separate from genre | Create with `musical_tradition="Hindustani Classical"` — verify it is not stored in a genre field | Stored in correct field | |
| P1-ART-11 | Soft delete removes from list | `DELETE /api/v1/artists/{id}`, then `GET /api/v1/artists` | Deleted artist absent | |

---

### 1.7 Albums

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-ALB-01 | Create linked to valid artist | POST with valid `artist_id` | 201, album linked | |
| P1-ALB-02 | Create with non-existent artist | POST with fake `artist_id` | 404 or 422 | |
| P1-ALB-03 | Filter by artist | `GET /api/v1/albums?artist_id={uuid}` | Only that artist's albums | |
| P1-ALB-04 | Filter by tradition | `GET /api/v1/albums?musical_tradition=Jazz` | Only Jazz albums | |
| P1-ALB-05 | Get by ID | `GET /api/v1/albums/{id}` | 200, includes ArtistSummary embed | |
| P1-ALB-06 | Soft delete | `DELETE /api/v1/albums/{id}` | Not in list after | |
| P1-ALB-07 | Artist delete cascades | Delete artist, `GET /api/v1/albums?artist_id={id}` | No albums returned | |

---

### 1.8 Tracks

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-TRK-01 | Create with raga field | POST with `raga: "Yaman"` | Stored and returned | |
| P1-TRK-02 | Create with tala field | POST with `tala: "Teentaal"` | Stored and returned | |
| P1-TRK-03 | Create with maqam field | POST with `maqam: "Rast"` | Stored and returned | |
| P1-TRK-04 | Filter by raga | `GET /api/v1/tracks?raga=Yaman` | Only matching tracks | |
| P1-TRK-05 | Filter by artist | `GET /api/v1/tracks?artist_id={uuid}` | Only that artist's tracks | |
| P1-TRK-06 | Filter by album | `GET /api/v1/tracks?album_id={uuid}` | Only that album's tracks | |
| P1-TRK-07 | Filter by tradition | `GET /api/v1/tracks?musical_tradition=Hindustani Classical` | Correct tracks returned | |
| P1-TRK-08 | Track without album (standalone) | POST with `artist_id` but no `album_id` | 201, album_id null in response | |
| P1-TRK-09 | Artist delete cascades to tracks | Delete artist, query tracks | No tracks for that artist | |

---

### 1.9 Input Validation & Security

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-SEC-01 | SQL injection in search | `GET /artists/search?q='; DROP TABLE artists;--` | 200 empty list, no crash, table still exists | |
| P1-SEC-02 | XSS in name field | POST artist with `name: "<script>alert(1)</script>"` | Stored as plain text, not executed in response | |
| P1-SEC-03 | Rate limiting enforced | 61+ requests/minute from same IP | 429 Too Many Requests | |
| P1-SEC-04 | Security headers on every response | Check headers on any endpoint | `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy` present | |
| P1-SEC-05 | CORS blocks unknown origin | Request from unlisted origin | CORS error, request blocked | |
| P1-SEC-06 | Oversized payload rejected | POST artist with 500,000 char biography | 413 or 422 | |
| P1-SEC-07 | Request ID unique per request | Two consecutive requests | Different `X-Request-ID` on each response | |
| P1-SEC-08 | Password not in any response | Login, inspect all response fields | No field contains the password | |
| P1-SEC-09 | Token not in logs | Trigger auth and check `docker compose logs api` | No JWT token values in log output | |

---

### 1.10 TOTP MFA

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-MFA-01 | Setup returns QR URI | `POST /api/v1/auth/totp/setup` with token | Returns `secret` + `otpauth://` URI + backup codes | |
| P1-MFA-02 | Enable with valid code | Scan QR in authenticator app, `POST /api/v1/auth/totp/verify` | TOTP enabled on account | |
| P1-MFA-03 | Login requires TOTP after enable | `POST /auth/token` without totp_code | 401 | |
| P1-MFA-04 | Login with correct TOTP | `POST /auth/login` with valid 6-digit code | 200, tokens returned | |
| P1-MFA-05 | Login with wrong TOTP | `POST /auth/login` with `totp_code: "000000"` | 401 | |
| P1-MFA-06 | Backup code works | Use a backup code instead of TOTP | 200 | |
| P1-MFA-07 | Backup code is single-use | Use same backup code twice | 401 on second attempt | |
| P1-MFA-08 | Disable TOTP | `POST /auth/totp/disable` with correct password | TOTP disabled, login works without code | |

---

### 1.11 Data Ingestion Pipeline

| ID | Test | Steps | Expected Result | Status |
|----|------|-------|----------------|--------|
| P1-ING-01 | Worker starts cleanly | `docker compose logs worker` | All 5 jobs logged as scheduled, no errors | |
| P1-ING-02 | MusicBrainz job runs | Trigger manually (see IMPLEMENTATION.md) | Artists appear in `GET /api/v1/artists` | |
| P1-ING-03 | Upsert is idempotent | Run MusicBrainz job twice | Same artist count — no duplicates created | |
| P1-ING-04 | Wikipedia enrichment populates biography | Run Wikipedia job for an artist | `biography` and `biography_short` fields populated | |
| P1-ING-05 | Native name extracted | Wikipedia job for Japanese/Hindi/Arabic artist | `name_native` populated in non-Latin script | |
| P1-ING-06 | Wikidata sync runs | Trigger Wikidata job | `wikidata_id` populated on matching artists | |
| P1-ING-07 | Spotify enrichment runs | Trigger Spotify job (requires `SPOTIFY_CLIENT_ID` set) | `spotify_id` and `image_url` populated | |
| P1-ING-08 | Jobs do not overlap | Check scheduler logs | Max 1 instance of each job running at any time | |
| P1-ING-09 | Failed job does not crash worker | Kill a dependency mid-job | Worker logs the error and continues; other jobs still scheduled | |

---

## Phase 2 — Catalog (Planned)

> Tests to be written when Phase 2 is built. Listed here as placeholders.

### 2.1 Catalog Structure
- Browsing by instrument family
- Browsing by era (ancient, medieval, modern)
- Browsing by region with sub-region drill-down
- Cross-referenced links: tradition → instruments → artists → albums

### 2.2 Integration: Phase 1 + Phase 2
- Artist pages in Phase 1 correctly link to catalog entries in Phase 2
- Catalog filters return correct Phase 1 artist/album data
- Instrument catalog entries reference live artist data

---

## Phase 3 — Performance Links (Planned)

> Tests to be written when Phase 3 is built.

### 3.1 External Links
- YouTube link resolves and is not dead
- Spotify link resolves to correct track/album
- Links survive artist page updates (no orphaned links)

### 3.2 Integration: Phase 1 + Phase 2 + Phase 3
- Artist detail page shows biography (Phase 1) + catalog position (Phase 2) + performance links (Phase 3)
- Deleting an artist cascades to remove all associated links

---

## Phase 4 — Recommendations + Player (Planned)

> Tests to be written when Phase 4 is built.

### 4.1 Recommendations
- Similar artist recommendations are non-empty for ingested artists
- Recommendations do not surface soft-deleted artists
- Cold start (no listening history) returns tradition-based defaults
- Vector embeddings populated after ingestion

### 4.2 Player
- Embedded player loads without auth
- Player respects CORS and CSP headers (no blocked resources)

### 4.3 Integration: All Phases
- Recommendation engine draws on catalog metadata (Phase 2) + links (Phase 3)
- Playing a track from a recommendation updates discovery history

---

## Phase 5 — Radio Stations (Planned)

> Tests to be written when Phase 5 is built.

### 5.1 Radio
- Station by tradition plays only tracks from that tradition
- Station by region plays geographically correct tracks
- Station skips soft-deleted tracks
- Continuous play does not repeat tracks within a session

### 5.2 Integration: All Phases
- Radio station metadata links back to artist encyclopedia pages (Phase 1)
- Radio track queue updates daily as ingestion adds new content (Phase 1 pipeline)

---

## Cross-Phase Integration Tests (Running Total)

These run after each phase is added to verify nothing broke.

| ID | Test | Phases Involved | Status |
|----|------|----------------|--------|
| INT-01 | Full stack boots cleanly from scratch | 1 | |
| INT-02 | Ingestion → API → response round trip | 1 | |
| INT-03 | Auth token from Phase 1 works on Phase 2 endpoints | 1+2 | ⏭ |
| INT-04 | Catalog links resolve to live artist data | 1+2 | ⏭ |
| INT-05 | Artist page aggregates data from all built phases | 1+2+3 | ⏭ |
| INT-06 | Recommendation respects soft-deleted content from all phases | 1+2+3+4 | ⏭ |
| INT-07 | Radio station reflects daily ingestion updates | 1+5 | ⏭ |
