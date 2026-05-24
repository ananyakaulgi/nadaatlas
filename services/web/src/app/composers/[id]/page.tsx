import { getComposer, getCompositions } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import type { Composition } from '@/lib/types'

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

  // Fetch this composer's compositions
  let compositions: Composition[] = []
  try {
    const result = await getCompositions({ composer_id: id, limit: 20 })
    compositions = result.items
  } catch {
    // non-fatal — composer page still renders without compositions
  }

  const birthYear = composer.born ? new Date(composer.born).getFullYear() : null
  const deathYear = composer.died ? new Date(composer.died).getFullYear() : null
  const lifespan  = birthYear
    ? deathYear
      ? `${birthYear} – ${deathYear}`
      : `b. ${birthYear}`
    : null

  const COMP_TYPE_COLORS: Record<string, 'teal' | 'lavender' | 'rose' | 'sage' | 'gold'> = {
    kriti: 'teal', varnam: 'teal', tillana: 'teal', padam: 'teal', javali: 'teal',
    khayal: 'lavender', dhrupad: 'lavender', thumri: 'lavender', tarana: 'lavender',
    ghazal: 'rose', qawwali: 'rose', bhajan: 'rose',
    symphony: 'sage', concerto: 'sage', sonata: 'sage', suite: 'sage', oratorio: 'sage',
    opera: 'gold', ballet: 'gold',
    tango: 'lavender', maqam: 'teal',
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link href="/composers" className="text-sm text-[#6b5d8a] hover:text-[#a89fc4] transition-colors mb-8 inline-flex items-center gap-1">
        ← All composers
      </Link>

      {/* ── Header ──────────────────────────────────────────────────────────── */}
      <div className="mt-6 mb-10 flex gap-8 items-start">
        {/* Portrait */}
        {composer.image_url && (
          <div className="shrink-0">
            <img
              src={composer.image_url}
              alt={composer.name}
              className="w-28 h-36 object-cover rounded-xl"
              style={{ border: '1px solid rgba(124,58,237,0.25)' }}
            />
          </div>
        )}

        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-start gap-3 mb-2">
            <h1 className="font-display text-5xl text-[#f5f0ff] leading-tight">{composer.name}</h1>
            {composer.is_verified && <span className="text-[#f59e0b] mt-2 text-xl" title="Verified">✦</span>}
          </div>
          {composer.name_native && (
            <p className="font-display text-2xl text-[#a89fc4] italic mb-3">{composer.name_native}</p>
          )}
          <div className="flex flex-wrap gap-2">
            {composer.era && <Badge variant="gold">{composer.era}</Badge>}
            {lifespan && <Badge variant="sage">{lifespan}</Badge>}
            {composer.tradition && <Badge variant="teal">{composer.tradition.name}</Badge>}
            {composer.nationality && <Badge variant="lavender">{composer.nationality}</Badge>}
          </div>
        </div>
      </div>

      {/* ── Quick facts ─────────────────────────────────────────────────────── */}
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

      {/* ── Biography ───────────────────────────────────────────────────────── */}
      {(composer.biography || composer.biography_short) && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Biography</h2>
          {composer.biography ? (
            /* Multi-paragraph biography */
            composer.biography.split('\n\n').map((para, i) => (
              <p key={i} className="text-[#a89fc4] leading-relaxed mb-4 last:mb-0">
                {para.trim()}
              </p>
            ))
          ) : (
            <p className="text-[#a89fc4] leading-relaxed">{composer.biography_short}</p>
          )}
        </div>
      )}

      {/* ── Compositions ────────────────────────────────────────────────────── */}
      {compositions.length > 0 && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(245,158,11,0.15)', backdropFilter: 'blur(12px)' }}
        >
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-display text-xl text-[#f5f0ff]">Compositions</h2>
            <span
              className="text-xs px-2.5 py-0.5 rounded-full"
              style={{ background: 'rgba(245,158,11,0.12)', border: '1px solid rgba(245,158,11,0.25)', color: '#f59e0b' }}
            >
              {compositions.length} works
            </span>
          </div>
          <div className="space-y-3">
            {compositions.map((c) => {
              const typeColor = COMP_TYPE_COLORS[c.composition_type?.toLowerCase() ?? ''] ?? 'sage'
              return (
                <Link key={c.id} href={`/compositions/${c.id}`}>
                  <div
                    className="group flex items-start gap-4 rounded-xl p-4 transition-all duration-200 hover:bg-[rgba(124,58,237,0.08)]"
                    style={{ border: '1px solid rgba(124,58,237,0.1)' }}
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-baseline gap-2 mb-1.5">
                        <span className="font-display text-base text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors">
                          {c.title}
                        </span>
                        {c.title_native && (
                          <span className="font-display text-sm text-[#a89fc4] italic">{c.title_native}</span>
                        )}
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {c.composition_type && (
                          <Badge variant={typeColor} className="capitalize">{c.composition_type}</Badge>
                        )}
                        {c.raga && <Badge variant="teal">{c.raga.name}</Badge>}
                        {c.tala && <Badge variant="sage">{c.tala.name}</Badge>}
                        {c.year_composed && (
                          <Badge variant="sage">{c.year_composed}</Badge>
                        )}
                        {c.language && <Badge variant="sage">{c.language}</Badge>}
                      </div>
                      {c.description && (
                        <p className="text-xs text-[#6b5d8a] mt-2 line-clamp-2 leading-relaxed">
                          {c.description}
                        </p>
                      )}
                    </div>
                    <span className="text-[#f59e0b] opacity-0 group-hover:opacity-100 transition-opacity shrink-0 mt-1 text-sm">→</span>
                  </div>
                </Link>
              )
            })}
          </div>

          {/* Link to full compositions list filtered by this composer */}
          <div className="mt-4 pt-4 border-t border-[rgba(124,58,237,0.1)]">
            <Link
              href={`/compositions?composer_id=${id}`}
              className="text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
            >
              Browse all compositions by {composer.name} →
            </Link>
          </div>
        </div>
      )}

      {/* ── External links ──────────────────────────────────────────────────── */}
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
