import { getTala } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'

export const dynamic = 'force-dynamic'

interface Props { params: Promise<{ id: string }> }

export default async function TalaDetailPage({ params }: Props) {
  const { id } = await params
  let tala
  try {
    tala = await getTala(id)
  } catch {
    notFound()
  }

  const TRADITION_COLORS = {
    hindustani: { border: 'rgba(245,158,11,0.3)',  accent: '#f59e0b', badge: 'gold' as const },
    carnatic:   { border: 'rgba(20,184,166,0.3)',  accent: '#2dd4bf', badge: 'teal' as const },
    both:       { border: 'rgba(124,58,237,0.3)',  accent: '#c4b5fd', badge: 'purple' as const },
  }
  const colors = TRADITION_COLORS[tala.tradition as keyof typeof TRADITION_COLORS] ?? TRADITION_COLORS.both

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link href="/talas" className="text-sm text-[#6b5d8a] hover:text-[#a89fc4] transition-colors mb-8 inline-flex items-center gap-1">
        ← All talas
      </Link>

      {/* Title */}
      <div className="mt-6 mb-10">
        <div className="flex flex-wrap items-start gap-3 mb-3">
          <h1 className="font-display text-5xl text-[#f5f0ff]">{tala.name}</h1>
          <Badge variant={colors.badge} className="mt-2 capitalize">{tala.tradition}</Badge>
        </div>
        {tala.name_native && (
          <p className="font-display text-2xl text-[#a89fc4] italic">{tala.name_native}</p>
        )}
      </div>

      {/* Beat count hero */}
      {tala.beats !== null && (
        <div
          className="rounded-2xl p-8 mb-8 flex items-center gap-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: `1px solid ${colors.border}`, backdropFilter: 'blur(12px)' }}
        >
          <div className="text-center">
            <p
              className="font-display leading-none mb-1"
              style={{ fontSize: '5rem', color: colors.accent }}
            >
              {tala.beats}
            </p>
            <p className="text-[#6b5d8a] text-sm uppercase tracking-wide">beats</p>
          </div>
          <div className="space-y-3">
            {tala.anga_structure && (
              <div>
                <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Structure</p>
                <p className="font-mono text-2xl text-[#f5f0ff] tracking-wider">{tala.anga_structure}</p>
              </div>
            )}
            {tala.vibhag && (
              <p className="text-sm text-[#a89fc4]">{tala.vibhag} vibhags</p>
            )}
            {tala.jati && (
              <Badge variant="sage" className="capitalize">{tala.jati} jati</Badge>
            )}
          </div>
        </div>
      )}

      {/* Details grid */}
      <div
        className="rounded-2xl p-6 mb-8"
        style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
      >
        <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Details</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          {tala.sam_beats && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Sam (Beat 1)</p>
              <p className="text-[#f5f0ff]">Beat {tala.sam_beats}</p>
            </div>
          )}
          {tala.common_tempos && tala.common_tempos.length > 0 && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Common Tempos</p>
              <p className="text-[#f5f0ff] capitalize">{tala.common_tempos.join(', ')}</p>
            </div>
          )}
        </div>
      </div>

      {/* Description */}
      {tala.description && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-3">About</h2>
          <p className="text-[#a89fc4] leading-relaxed">{tala.description}</p>
        </div>
      )}

      {tala.wikipedia_slug && (
        <a
          href={`https://en.wikipedia.org/wiki/${tala.wikipedia_slug}`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
        >
          Read on Wikipedia ↗
        </a>
      )}
    </div>
  )
}
