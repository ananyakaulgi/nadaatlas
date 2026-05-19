import { getAlbum } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import { Music, ChevronRight } from 'lucide-react'
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
    const album = await getAlbum(id)
    return { title: album.title, description: album.description || undefined }
  } catch {
    return { title: 'Album' }
  }
}

export default async function AlbumDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  let album
  try {
    album = await getAlbum(id)
  } catch {
    notFound()
  }

  const year = formatYear(album.release_date)

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-[#6b5d8a] mb-8">
        <Link href="/albums" className="hover:text-[#c4b5fd] transition-colors">Albums</Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-[#f5f0ff]">{album.title}</span>
      </nav>

      <div className="grid grid-cols-1 md:grid-cols-[280px_1fr] gap-10">
        {/* Cover */}
        <div>
          <div
            className="aspect-square rounded-2xl overflow-hidden flex items-center justify-center"
            style={{
              background: 'linear-gradient(135deg, rgba(76,29,149,0.4), rgba(245,158,11,0.15))',
              border: '1px solid rgba(245,158,11,0.2)',
              boxShadow: '0 4px 24px rgba(245,158,11,0.08)',
            }}
          >
            {album.cover_image_url ? (
              <img
                src={album.cover_image_url}
                alt={album.title}
                className="w-full h-full object-cover"
              />
            ) : (
              <Music className="w-16 h-16 text-[#c4b5fd] opacity-30" />
            )}
          </div>
        </div>

        {/* Info */}
        <div>
          <h1 className="font-display text-5xl text-[#f5f0ff] mb-2 leading-tight">{album.title}</h1>

          {album.title_native && (
            <p className="font-display text-xl text-[#a89fc4] italic mb-4">{album.title_native}</p>
          )}

          {album.artist && (
            <p className="text-lg text-[#a89fc4] mb-5">
              by{' '}
              <Link href={`/artists/${album.artist.id}`} className="text-[#f59e0b] hover:text-[#fbbf24] transition-colors">
                {album.artist.name}
              </Link>
            </p>
          )}

          <div className="flex flex-wrap gap-2 mb-6">
            {album.album_type && <Badge variant="gold">{album.album_type}</Badge>}
            {year && <Badge variant="default">{year}</Badge>}
            {album.musical_tradition && <Badge variant="teal">{album.musical_tradition}</Badge>}
          </div>

          <dl className="space-y-3 text-sm">
            {album.label && (
              <div className="flex gap-3">
                <dt className="text-[#6b5d8a] w-20 shrink-0">Label</dt>
                <dd className="text-[#c4b5fd]">{album.label}</dd>
              </div>
            )}
            {album.release_date && (
              <div className="flex gap-3">
                <dt className="text-[#6b5d8a] w-20 shrink-0">Released</dt>
                <dd className="text-[#c4b5fd]">{album.release_date}</dd>
              </div>
            )}
          </dl>
        </div>
      </div>

      {/* Description */}
      {album.description && (
        <div
          className="mt-10 rounded-2xl p-8"
          style={{
            background: 'rgba(20,14,40,0.7)',
            border: '1px solid rgba(124,58,237,0.18)',
            backdropFilter: 'blur(12px)',
          }}
        >
          <h2 className="font-display text-2xl text-[#f5f0ff] mb-4">About this album</h2>
          <p className="text-[#c4b5fd] leading-relaxed">{album.description}</p>
        </div>
      )}

      {album.artist && (
        <div className="mt-8">
          <Link
            href={`/artists/${album.artist.id}`}
            className="inline-flex items-center gap-2 text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
            style={{ textShadow: '0 0 8px rgba(245,158,11,0.3)' }}
          >
            ← Back to {album.artist.name}
          </Link>
        </div>
      )}
    </div>
  )
}
