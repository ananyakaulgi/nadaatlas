import { getComposer } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'

export const dynamic = 'force-dynamic'

interface Props { params: Promise<{ id: string }> }

export default async function ComposerDetailPage({ params }: Props) {
  const { id } = await params
  let composer
  try {
    composer = await getComposer(id)
  } catch {
    notFound()
  }

  const birthYear = composer.born ? new Date(composer.born).getFullYear() : null
  const deathYear = composer.died ? new Date(composer.died).getFullYear() : null

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link href="/composers" className="text-sm text-[#6b5d8a] hover:text-[#a89fc4] transition-colors mb-8 inline-flex items-center gap-1">
        ← All composers
      </Link>

      {/* Title */}
      <div className="mt-6 mb-10">
        <div className="flex flex-wrap items-start gap-3 mb-3">
          <h1 className="font-display text-5xl text-[#f5f0ff]">{composer.name}</h1>
          {composer.is_verified && <span className="text-[#f59e0b] mt-2 text-xl" title="Verified">✦</span>}
        </div>
        {composer.name_native && (
          <p className="font-display text-2xl text-[#a89fc4] italic mb-3">{composer.name_native}</p>
        )}
        <div className="flex flex-wrap gap-2">
          {composer.era && <Badge variant="gold">{composer.era}</Badge>}
          {(birthYear || deathYear) && (
            <Badge variant="sage">
              {birthYear ?? '?'}{deathYear ? ` – ${deathYear}` : ' –'}
            </Badge>
          )}
          {composer.tradition && <Badge variant="teal">{composer.tradition.name}</Badge>}
          {composer.nationality && <Badge variant="lavender">{composer.nationality}</Badge>}
        </div>
      </div>

      {/* Quick facts */}
      <div
        className="rounded-2xl p-6 mb-8"
        style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
      >
        <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Overview</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          {birthYear && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Born</p>
              <p className="text-[#f5f0ff]">{birthYear}{composer.birth_place ? `, ${composer.birth_place}` : ''}</p>
            </div>
          )}
          {deathYear && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Died</p>
              <p className="text-[#f5f0ff]">{deathYear}</p>
            </div>
          )}
          {composer.nationality && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Nationality</p>
              <p className="text-[#f5f0ff]">{composer.nationality}</p>
            </div>
          )}
          {composer.tradition && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Tradition</p>
              <p className="text-[#f5f0ff]">{composer.tradition.name}</p>
            </div>
          )}
          {composer.era && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Era</p>
              <p className="text-[#f5f0ff]">{composer.era}</p>
            </div>
          )}
        </div>
      </div>

      {/* Biography */}
      {(composer.biography || composer.biography_short) && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-3">Biography</h2>
          <p className="text-[#a89fc4] leading-relaxed whitespace-pre-line">
            {composer.biography || composer.biography_short}
          </p>
        </div>
      )}

      {/* External links */}
      <div className="flex flex-wrap gap-4">
        {composer.wikipedia_slug && (
          <a
            href={`https://en.wikipedia.org/wiki/${composer.wikipedia_slug}`}
            target="_blank" rel="noopener noreferrer"
            className="text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
          >
            Wikipedia ↗
          </a>
        )}
        {composer.wikidata_id && (
          <a
            href={`https://www.wikidata.org/wiki/${composer.wikidata_id}`}
            target="_blank" rel="noopener noreferrer"
            className="text-sm text-[#6b5d8a] hover:text-[#a89fc4] transition-colors"
          >
            Wikidata ↗
          </a>
        )}
        {composer.website_url && (
          <a
            href={composer.website_url}
            target="_blank" rel="noopener noreferrer"
            className="text-sm text-[#6b5d8a] hover:text-[#a89fc4] transition-colors"
          >
            Website ↗
          </a>
        )}
      </div>
    </div>
  )
}
