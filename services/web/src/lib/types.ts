export interface Tradition {
  id: number
  name: string
  name_native: string | null
  region: string
  subregion: string | null
  description: string | null
  origin_period: string | null
  wikipedia_slug: string | null
  is_active: boolean
  created_at: string
}

export interface Artist {
  id: number
  name: string
  name_native: string | null
  name_sort: string | null
  biography_short: string | null
  born: string | null
  died: string | null
  birth_place: string | null
  nationality: string | null
  musical_tradition: string | null
  image_url: string | null
  website_url: string | null
  tradition: Tradition | null
  primary_instrument: string | null
  is_verified: boolean
}

export interface ArtistSummary {
  id: string
  name: string
  name_native: string | null
  musical_tradition: string | null
  image_url: string | null
}

export interface AlbumSummary {
  id: string
  title: string
  release_date: string | null
  cover_image_url: string | null
}

export interface AlbumArtist {
  id: number
  name: string
  name_native: string | null
  musical_tradition: string | null
  image_url: string | null
}

export interface Album {
  id: number
  title: string
  title_native: string | null
  release_date: string | null
  album_type: string | null
  musical_tradition: string | null
  label: string | null
  description: string | null
  cover_image_url: string | null
  artist: AlbumArtist | null
}

export interface Instrument {
  id: number
  name: string
  name_native: string | null
  hornbostel_sachs: string | null
  hs_category: string | null
  description: string | null
  origin_region: string | null
  materials: string[] | null
  image_url: string | null
  tradition: Tradition | null
  wikipedia_slug: string | null
}

export interface Track {
  id: string
  title: string
  title_native: string | null
  duration_seconds: number | null
  track_number: number | null
  musical_tradition: string | null
  raga: string | null
  tala: string | null
  maqam: string | null
  youtube_url: string | null
  spotify_url: string | null
  artist: ArtistSummary
  album: AlbumSummary | null
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

export interface Raga {
  id: string
  name: string
  name_native: string | null
  tradition: string
  hindustani_name: string | null
  carnatic_name: string | null
  that: string | null
  melakarta_number: number | null
  arohana: string | null
  avarohana: string | null
  vadi: string | null
  samvadi: string | null
  pakad: string | null
  time_of_day: string | null
  season: string | null
  rasa: string | null
  description: string | null
  wikipedia_slug: string | null
  created_at: string
  updated_at: string
}

export interface Tala {
  id: string
  name: string
  name_native: string | null
  tradition: string
  beats: number | null
  vibhag: number | null
  sam_beats: string | null
  jati: string | null
  anga_structure: string | null
  common_tempos: string[] | null
  description: string | null
  wikipedia_slug: string | null
  created_at: string
  updated_at: string
}

export interface Region {
  id: string
  name: string
  continent: string | null
  country_name: string | null
  state: string | null
  description: string | null
  created_at: string
  updated_at: string
}

export interface Genre {
  id: string
  name: string
  slug: string
  description: string | null
  created_at: string
  updated_at: string
}

export interface TraditionSummary {
  id: string
  name: string
  region: string
}

export interface RagaSummary {
  id: string
  name: string
  tradition: string
  that: string | null
  melakarta_number: number | null
  arohana: string | null
}

export interface TalaSummary {
  id: string
  name: string
  tradition: string
  beats: number | null
  anga_structure: string | null
}

export interface ComposerSummary {
  id: string
  name: string
  name_sort: string | null
  era: string | null
  nationality: string | null
}

export interface Composer {
  id: string
  name: string
  name_native: string | null
  name_sort: string | null
  tradition_id: string | null
  tradition: TraditionSummary | null
  era: string | null
  born: string | null
  died: string | null
  birth_place: string | null
  nationality: string | null
  biography_short: string | null
  biography: string | null
  musicbrainz_id: string | null
  wikidata_id: string | null
  wikipedia_slug: string | null
  image_url: string | null
  website_url: string | null
  is_verified: boolean
  created_at: string
  updated_at: string
}

export interface Composition {
  id: string
  title: string
  title_native: string | null
  composer_id: string | null
  tradition_id: string | null
  composition_type: string | null
  raga_id: string | null
  tala_id: string | null
  maqam: string | null
  language: string | null
  lyrics: string | null
  description: string | null
  year_composed: number | null
  wikipedia_slug: string | null
  composer: ComposerSummary | null
  raga: RagaSummary | null
  tala: TalaSummary | null
  tradition: TraditionSummary | null
  created_at: string
  updated_at: string
}
