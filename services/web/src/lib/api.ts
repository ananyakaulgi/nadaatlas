import type {
  Tradition, Artist, Album, Instrument,
  Raga, Tala, Composer, Composition, Region, Genre, Track,
  PaginatedResponse,
} from './types'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchAPI<T>(path: string): Promise<T> {
  const url = `${BASE_URL}${path}`
  const res = await fetch(url, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${url}`)
  }
  return res.json()
}

// Traditions
export async function getTraditions(params?: {
  skip?: number
  limit?: number
  region?: string
}): Promise<PaginatedResponse<Tradition>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.region) qs.set('region', params.region)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/traditions/${query}`)
}

export async function getTradition(id: number | string): Promise<Tradition> {
  return fetchAPI(`/api/v1/traditions/${id}`)
}

// Artists
export async function getArtists(params?: {
  skip?: number
  limit?: number
  musical_tradition?: string
  search?: string
}): Promise<PaginatedResponse<Artist>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.musical_tradition) qs.set('musical_tradition', params.musical_tradition)
  if (params?.search) qs.set('search', params.search)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/artists/${query}`)
}

export async function getArtist(id: number | string): Promise<Artist> {
  return fetchAPI(`/api/v1/artists/${id}`)
}

// Albums
export async function getAlbums(params?: {
  skip?: number
  limit?: number
  artist_id?: number | string
  musical_tradition?: string
}): Promise<PaginatedResponse<Album>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.artist_id !== undefined) qs.set('artist_id', String(params.artist_id))
  if (params?.musical_tradition) qs.set('musical_tradition', params.musical_tradition)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/albums/${query}`)
}

export async function getAlbum(id: number | string): Promise<Album> {
  return fetchAPI(`/api/v1/albums/${id}`)
}

// Instruments
export async function getInstruments(params?: {
  skip?: number
  limit?: number
}): Promise<PaginatedResponse<Instrument>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/instruments/${query}`)
}

export async function getInstrument(id: number | string): Promise<Instrument> {
  return fetchAPI(`/api/v1/instruments/${id}`)
}

// Ragas
export async function getRagas(params?: {
  skip?: number
  limit?: number
  tradition?: string
  that?: string
  melakarta_number?: number
  search?: string
}): Promise<PaginatedResponse<Raga>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.tradition) qs.set('tradition', params.tradition)
  if (params?.that) qs.set('that', params.that)
  if (params?.melakarta_number !== undefined) qs.set('melakarta_number', String(params.melakarta_number))
  if (params?.search) qs.set('search', params.search)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/ragas/${query}`)
}

export async function getRaga(id: string): Promise<Raga> {
  return fetchAPI(`/api/v1/ragas/${id}`)
}

// Talas
export async function getTalas(params?: {
  skip?: number
  limit?: number
  tradition?: string
  beats?: number
}): Promise<PaginatedResponse<Tala>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.tradition) qs.set('tradition', params.tradition)
  if (params?.beats !== undefined) qs.set('beats', String(params.beats))
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/talas/${query}`)
}

export async function getTala(id: string): Promise<Tala> {
  return fetchAPI(`/api/v1/talas/${id}`)
}

// Composers
export async function getComposers(params?: {
  skip?: number
  limit?: number
  tradition_id?: string
  era?: string
  nationality?: string
  search?: string
}): Promise<PaginatedResponse<Composer>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.tradition_id) qs.set('tradition_id', params.tradition_id)
  if (params?.era) qs.set('era', params.era)
  if (params?.nationality) qs.set('nationality', params.nationality)
  if (params?.search) qs.set('search', params.search)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/composers/${query}`)
}

export async function getComposer(id: string): Promise<Composer> {
  return fetchAPI(`/api/v1/composers/${id}`)
}

// Regions
export async function getRegions(params?: {
  skip?: number
  limit?: number
  continent?: string
}): Promise<PaginatedResponse<Region>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.continent) qs.set('continent', params.continent)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/regions/${query}`)
}

// Compositions
export async function getCompositions(params?: {
  skip?: number
  limit?: number
  tradition_id?: string
  composer_id?: string
  raga_id?: string
  tala_id?: string
  composition_type?: string
  search?: string
}): Promise<PaginatedResponse<Composition>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.tradition_id) qs.set('tradition_id', params.tradition_id)
  if (params?.composer_id) qs.set('composer_id', params.composer_id)
  if (params?.raga_id) qs.set('raga_id', params.raga_id)
  if (params?.tala_id) qs.set('tala_id', params.tala_id)
  if (params?.composition_type) qs.set('composition_type', params.composition_type)
  if (params?.search) qs.set('search', params.search)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/compositions/${query}`)
}

export async function getComposition(id: string): Promise<Composition> {
  return fetchAPI(`/api/v1/compositions/${id}`)
}

// Tracks
export async function getTracks(params?: {
  skip?: number
  limit?: number
  artist_id?: string
  album_id?: string
  musical_tradition?: string
  raga?: string
  search?: string
}): Promise<PaginatedResponse<Track>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.artist_id) qs.set('artist_id', params.artist_id)
  if (params?.album_id) qs.set('album_id', params.album_id)
  if (params?.musical_tradition) qs.set('musical_tradition', params.musical_tradition)
  if (params?.raga) qs.set('raga', params.raga)
  if (params?.search) qs.set('search', params.search)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/tracks/${query}`)
}

export async function getTrack(id: string): Promise<Track> {
  return fetchAPI(`/api/v1/tracks/${id}`)
}

// Genres
export async function getGenres(params?: {
  skip?: number
  limit?: number
  search?: string
}): Promise<PaginatedResponse<Genre>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.search) qs.set('search', params.search)
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return fetchAPI(`/api/v1/genres/${query}`)
}
