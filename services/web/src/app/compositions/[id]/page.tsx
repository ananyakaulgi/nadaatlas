import { getComposition } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'

export const dynamic = 'force-dynamic'

interface Props { params: Promise<{ id: string }> }

export default async function CompositionDetailPage({ params }: Props) {
  const { id } = await params
  let composition
  try {
    composition = await getComposition(id)
  } catch {
    notFound()
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link href="/compositions" className="text-sm text-[#6b5d8a] hover:text-[#a89fc4] transition-colors mb-8 inline-flex items-center gap-1">
        ← All compositions
      </Link>

      {/* Title */}
      <div className="mt-6 mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-2">{composition.title}</h1>
        {composition.title_native && (
          <p className="font-display text-2xl text-[#a89fc4] italic mb-4">{composition.title_native}</p>
        )}
        <div className="flex flex-wrap gap-2">
          {composition.composition_type && (
            <Badge variant="purple" className="capitalize">{composition.composition_type}</Badge>
          )}
          {composition.language && <Badge variant="sage">{composition.language}</Badge>}
          {composition.year_composed && <Badge variant="gold">{composition.year_composed}</Badge>}
          {composition.tradition && <Badge variant="teal">{composition.tradition.name}</Badge>}
        </div>
      </div>

      {/* Key info */}
      <div
        className="rounded-2xl p-6 mb-8"
        style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
      >
        <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Details</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          {composition.composer && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Composer</p>
              <Link href={`/composers/${composition.composer.id}`} className="text-[#f59e0b] hover:text-[#fbbf24] transition-colors">
                {composition.composer.name}
              </Link>
            </div>
          )}
          {composition.raga && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Raga</p>
              <Link href={`/ragas/${composition.raga.id}`} className="text-[#c4b5fd] hover:text-[#f5f0ff] transition-colors">
                {composition.raga.name}
              </Link>
            </div>
          )}
          {composition.tala && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Tala</p>
              <Link href={`/talas/${composition.tala.id}`} className="text-[#2dd4bf] hover:text-[#f5f0ff] transition-colors">
                {composition.tala.name}
              </Link>
            </div>
          )}
          {composition.maqam && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Maqam</p>
              <p className="text-[#f5f0ff]">{composition.maqam}</p>
            </div>
          )}
        </div>
      </div>

      {/* Description */}
      {composition.description && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-3">About</h2>
          <p className="text-[#a89fc4] leading-relaxed">{composition.description}</p>
        </div>
      )}

      {/* Lyrics */}
      {composition.lyrics && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(245,158,11,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-3">Lyrics</h2>
          <pre className="text-[#a89fc4] leading-relaxed whitespace-pre-wrap font-sans text-sm">
            {composition.lyrics}
          </pre>
        </div>
      )}

      {/* Wikipedia */}
      {composition.wikipedia_slug && (
        <a
          href={`https://en.wikipedia.org/wiki/${composition.wikipedia_slug}`}
          target="_blank" rel="noopener noreferrer"
          className="inline-flex items-center gap-2 text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
        >
          Read on Wikipedia ↗
        </a>
      )}
    </div>
  )
}
