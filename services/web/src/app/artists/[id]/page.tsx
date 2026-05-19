import { getArtist, getAlbums } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import AlbumCard from '@/components/cards/AlbumCard'
import { ExternalLink, ChevronRight, MapPin } from 'lucide-react'
import type { Metadata } from 'next'

function formatYear(dateStr: string | null): string | null {
  if (!dateStr) return null
  try { return String(new Date(dateStr).getFullYear()) } catch { return null }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  try {
    const { id } = await params
    const artist = await getArtist(id)
    return { title: artist.name, description: artist.biography_short || undefined }
  } catch {
    return { title: 'Artist' }
  }
}

export default async function ArtistDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  let artist
  try {
    artist = await getArtist(id)
  } catch {
    notFound()
  }

  let albums: Awaited<ReturnType<typeof getAlbums>>['items'] = []
  try {
    const result = await getAlbums({ artist_id: id, limit: 50 })
    albums = result.items
  } catch {
    // no albums
  }

  const bornYear = formatYear(artist.born)
  const diedYear = formatYear(artist.died)

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-[#6b5d8a] mb-8">
        <Link href="/artists" className="hover:text-[#c4b5fd] transition-colors">Artists</Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-[#f5f0ff]">{artist.name}</span>
      </nav>

      {/* Hero */}
      <div
        className="rounded-2xl p-10 mb-10"
        style={{
          background: 'rgba(20,14,40,0.7)',
          border: '1px solid rgba(20,184,166,0.2)',
          backdropFilter: 'blur(12px)',
          boxShadow: '0 4px 32px rgba(20,184,166,0.08)',
        }}
      >
        <h1 className="font-display text-6xl text-[#f5f0ff] mb-2 leading-tight">{artist.name}</h1>

        {artist.name_native && (
          <p className="font-display text-2xl text-[#a89fc4] italic mb-5">{artist.name_native}</p>
        )}

        <div className="flex flex-wrap gap-4 text-sm text-[#a89fc4]">
          {bornYear && (
            <span>{bornYear}{diedYear ? ` – ${diedYear}` : ''}</span>
          )}
          {artist.birth_place && (
            <span className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5" />
              {artist.birth_place}
            </span>
          )}
          {artist.nationality && <span>{artist.nationality}</span>}
          {artist.primary_instrument && (
            <span className="text-[#f59e0b]">{artist.primary_instrument}</span>
          )}
        </div>

        {artist.musical_tradition && (
          <div className="mt-5">
            {artist.tradition ? (
              <Link href={`/traditions/${artist.tradition.id}`}>
                <Badge variant="teal" className="hover:opacity-80 transition-opacity cursor-pointer">
                  {artist.musical_tradition}
                </Badge>
              </Link>
            ) : (
              <Badge variant="teal">{artist.musical_tradition}</Badge>
            )}
          </div>
        )}
      </div>

      {/* Biography */}
      {artist.biography_short && (
        <div className="mb-10">
          <h2 className="font-display text-3xl text-[#f5f0ff] mb-5">Biography</h2>
          <div
            className="rounded-2xl p-8"
            style={{
              background: 'rgba(20,14,40,0.7)',
              border: '1px solid rgba(124,58,237,0.18)',
              backdropFilter: 'blur(12px)',
            }}
          >
            <p className="text-[#c4b5fd] leading-relaxed text-lg">{artist.biography_short}</p>
          </div>
        </div>
      )}

      {/* Website */}
      {artist.website_url && (
        <div className="mb-10">
          <a
            href={artist.website_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
            style={{ textShadow: '0 0 8px rgba(245,158,11,0.3)' }}
          >
            <ExternalLink className="w-4 h-4" />
            Official website
          </a>
        </div>
      )}

      {/* Albums */}
      <div>
        <h2 className="font-display text-3xl text-[#f5f0ff] mb-6">Discography</h2>

        {albums.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
            {albums.map((album) => (
              <AlbumCard key={album.id} album={album} />
            ))}
          </div>
        ) : (
          <div
            className="rounded-2xl p-8 text-center"
            style={{
              background: 'rgba(20,14,40,0.7)',
              border: '1px solid rgba(124,58,237,0.15)',
              backdropFilter: 'blur(12px)',
            }}
          >
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No albums recorded yet</p>
            <p className="text-sm text-[#a89fc4]">
              Albums by {artist.name} will appear here as they are added.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
