import type { Tradition, Artist, Album, Instrument, PaginatedResponse } from './types'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchAPI<T>(path: string): Promise<T> {
  const url = `${BASE_URL}${path}`
  const res = await fetch(url, { next: { revalidate: 60 } })
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
}): Promise<PaginatedResponse<Artist>> {
  const qs = new URLSearchParams()
  if (params?.skip !== undefined) qs.set('skip', String(params.skip))
  if (params?.limit !== undefined) qs.set('limit', String(params.limit))
  if (params?.musical_tradition) qs.set('musical_tradition', params.musical_tradition)
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
