import { getInstrument } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import { ExternalLink, ChevronRight } from 'lucide-react'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  try {
    const { id } = await params
    const instrument = await getInstrument(id)
    return { title: instrument.name, description: instrument.description || undefined }
  } catch {
    return { title: 'Instrument' }
  }
}

export default async function InstrumentDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  let instrument
  try {
    instrument = await getInstrument(id)
  } catch {
    notFound()
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-[#6b5d8a] mb-8">
        <Link href="/instruments" className="hover:text-[#c4b5fd] transition-colors">Instruments</Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-[#f5f0ff]">{instrument.name}</span>
      </nav>

      {/* Header */}
      <div className="mb-8">
        <div className="flex flex-wrap gap-2 mb-4">
          {instrument.hs_category && <Badge variant="lavender">{instrument.hs_category}</Badge>}
          {instrument.origin_region && <Badge variant="teal">{instrument.origin_region}</Badge>}
        </div>

        <h1 className="font-display text-6xl text-[#f5f0ff] mb-2 leading-tight"
          style={{ textShadow: '0 0 40px rgba(167,139,250,0.2)' }}
        >{instrument.name}</h1>

        {instrument.name_native && (
          <p className="font-display text-2xl text-[#a89fc4] italic">{instrument.name_native}</p>
        )}
      </div>

      {/* Details card */}
      <div
        className="rounded-2xl p-8 mb-8"
        style={{
          background: 'rgba(20,14,40,0.7)',
          border: '1px solid rgba(167,139,250,0.18)',
          backdropFilter: 'blur(12px)',
        }}
      >
        <dl className="space-y-4">
          {instrument.hornbostel_sachs && (
            <div>
              <dt className="text-xs text-[#6b5d8a] uppercase tracking-widest mb-1">Hornbostel-Sachs</dt>
              <dd className="text-sm text-[#c4b5fd] font-mono">{instrument.hornbostel_sachs}</dd>
            </div>
          )}
          {instrument.hs_category && (
            <div>
              <dt className="text-xs text-[#6b5d8a] uppercase tracking-widest mb-1">Category</dt>
              <dd className="text-sm text-[#c4b5fd]">{instrument.hs_category}</dd>
            </div>
          )}
          {instrument.origin_region && (
            <div>
              <dt className="text-xs text-[#6b5d8a] uppercase tracking-widest mb-1">Origin Region</dt>
              <dd className="text-sm text-[#c4b5fd]">{instrument.origin_region}</dd>
            </div>
          )}
          {instrument.materials && instrument.materials.length > 0 && (
            <div>
              <dt className="text-xs text-[#6b5d8a] uppercase tracking-widest mb-2">Materials</dt>
              <dd className="flex flex-wrap gap-2">
                {instrument.materials.map((material) => (
                  <Badge key={material} variant="cream">{material}</Badge>
                ))}
              </dd>
            </div>
          )}
        </dl>
      </div>

      {/* Description */}
      {instrument.description && (
        <div
          className="rounded-2xl p-8 mb-8"
          style={{
            background: 'rgba(20,14,40,0.7)',
            border: '1px solid rgba(124,58,237,0.18)',
            backdropFilter: 'blur(12px)',
          }}
        >
          <h2 className="font-display text-2xl text-[#f5f0ff] mb-4">About</h2>
          <p className="text-[#c4b5fd] leading-relaxed text-lg">{instrument.description}</p>
        </div>
      )}

      {/* Tradition link */}
      {instrument.tradition && (
        <div className="mb-8">
          <h2 className="font-display text-xl text-[#f5f0ff] mb-3">Associated Tradition</h2>
          <Link href={`/traditions/${instrument.tradition.id}`}>
            <div
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm text-[#5eead4] hover:opacity-80 transition-opacity"
              style={{
                background: 'rgba(20,184,166,0.1)',
                border: '1px solid rgba(20,184,166,0.2)',
              }}
            >
              {instrument.tradition.name}
            </div>
          </Link>
        </div>
      )}

      {/* Wikipedia link */}
      {instrument.wikipedia_slug && (
        <a
          href={`https://en.wikipedia.org/wiki/${instrument.wikipedia_slug}`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
          style={{ textShadow: '0 0 8px rgba(245,158,11,0.3)' }}
        >
          <ExternalLink className="w-4 h-4" />
          Read more on Wikipedia
        </a>
      )}
    </div>
  )
}
