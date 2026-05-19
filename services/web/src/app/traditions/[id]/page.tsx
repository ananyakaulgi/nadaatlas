import { getTradition, getArtists } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import ArtistCard from '@/components/cards/ArtistCard'
import { ExternalLink, ChevronRight } from 'lucide-react'
import type { Metadata } from 'next'

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  try {
    const { id } = await params
    const tradition = await getTradition(id)
    return { title: tradition.name, description: tradition.description || undefined }
  } catch {
    return { title: 'Tradition' }
  }
}

export default async function TraditionDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  let tradition
  try {
    tradition = await getTradition(id)
  } catch {
    notFound()
  }

  let relatedArtists: Awaited<ReturnType<typeof getArtists>>['items'] = []
  try {
    const result = await getArtists({ limit: 100 })
    relatedArtists = result.items.filter(
      (a) => a.musical_tradition?.toLowerCase() === tradition.name.toLowerCase()
    ).slice(0, 6)
  } catch {
    // no artists
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-[#6b5d8a] mb-8">
        <Link href="/traditions" className="hover:text-[#c4b5fd] transition-colors">Traditions</Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-[#f5f0ff]">{tradition.name}</span>
      </nav>

      {/* Header */}
      <div className="mb-10">
        <div className="flex flex-wrap items-start gap-3 mb-3">
          <Badge variant="teal">{tradition.region}</Badge>
          {tradition.subregion && <Badge variant="sage">{tradition.subregion}</Badge>}
          {tradition.origin_period && <Badge variant="gold">{tradition.origin_period}</Badge>}
        </div>

        <h1 className="font-display text-6xl text-[#f5f0ff] mb-2 leading-tight"
          style={{ textShadow: '0 0 40px rgba(124,58,237,0.2)' }}
        >{tradition.name}</h1>

        {tradition.name_native && (
          <p className="font-display text-2xl text-[#a89fc4] italic">{tradition.name_native}</p>
        )}
      </div>

      {/* Description */}
      {tradition.description && (
        <div
          className="rounded-2xl p-8 mb-10"
          style={{
            background: 'rgba(20,14,40,0.7)',
            border: '1px solid rgba(124,58,237,0.2)',
            backdropFilter: 'blur(12px)',
          }}
        >
          <p className="text-[#c4b5fd] leading-relaxed text-lg">{tradition.description}</p>
        </div>
      )}

      {/* Wikipedia link */}
      {tradition.wikipedia_slug && (
        <div className="mb-10">
          <a
            href={`https://en.wikipedia.org/wiki/${tradition.wikipedia_slug}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
            style={{ textShadow: '0 0 8px rgba(245,158,11,0.3)' }}
          >
            <ExternalLink className="w-4 h-4" />
            Read more on Wikipedia
          </a>
        </div>
      )}

      {/* Related Artists */}
      <div>
        <h2 className="font-display text-3xl text-[#f5f0ff] mb-6">Artists of this Tradition</h2>

        {relatedArtists.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {relatedArtists.map((artist) => (
              <ArtistCard key={artist.id} artist={artist} />
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
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No artists recorded yet</p>
            <p className="text-sm text-[#a89fc4]">
              Artists associated with {tradition.name} will appear here as they are added.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
