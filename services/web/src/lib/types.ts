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

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}
