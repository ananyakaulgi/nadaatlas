import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import type { Raga } from '@/lib/types'

const TRADITION_COLORS = {
  hindustani: { border: 'rgba(245,158,11,0.3)', glow: 'rgba(245,158,11,0.12)', badge: 'gold' as const },
  carnatic:   { border: 'rgba(20,184,166,0.3)',  glow: 'rgba(20,184,166,0.1)',  badge: 'teal' as const },
  both:       { border: 'rgba(124,58,237,0.3)',  glow: 'rgba(124,58,237,0.12)', badge: 'lavender' as const },
}

export default function RagaCard({ raga }: { raga: Raga }) {
  const colors = TRADITION_COLORS[raga.tradition as keyof typeof TRADITION_COLORS] ?? TRADITION_COLORS.both
  const hasScale = raga.arohana && raga.arohana.length > 0

  return (
    <Link href={`/ragas/${raga.id}`}>
      <div
        className="group relative rounded-2xl p-5 hover:scale-[1.01] transition-all duration-300 h-full flex flex-col"
        style={{
          background: 'rgba(20,14,40,0.65)',
          backdropFilter: 'blur(12px)',
          border: `1px solid ${colors.border}`,
          boxShadow: `0 2px 16px ${colors.glow}`,
        }}
      >
        <div
          className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
          style={{ background: `radial-gradient(ellipse at top left, ${colors.glow}, transparent 65%)` }}
        />

        {/* Header */}
        <div className="relative z-10 flex items-start justify-between gap-2 mb-2">
          <h3 className="font-display text-lg text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors leading-tight">
            {raga.name}
          </h3>
          <Badge variant={colors.badge} className="shrink-0 capitalize text-xs">
            {raga.tradition === 'both' ? 'Both' : raga.tradition}
          </Badge>
        </div>

        {/* Native name */}
        {raga.name_native && (
          <p className="relative z-10 font-display text-[#a89fc4] text-sm italic mb-2">{raga.name_native}</p>
        )}

        {/* Thaat / Melakarta */}
        <div className="relative z-10 flex flex-wrap gap-1.5 mb-3">
          {raga.that && <Badge variant="sage">Thaat: {raga.that}</Badge>}
          {raga.melakarta_number && <Badge variant="sage">Melakarta #{raga.melakarta_number}</Badge>}
        </div>

        {/* Scale */}
        {hasScale && (
          <div className="relative z-10 mb-3">
            <p className="text-xs text-[#6b5d8a] mb-1 uppercase tracking-wide">Ārohana</p>
            <p className="font-mono text-xs text-[#c4b5fd] tracking-wider">{raga.arohana}</p>
          </div>
        )}

        {/* Vadi */}
        {(raga.vadi || raga.time_of_day) && (
          <div className="relative z-10 flex gap-3 text-xs text-[#a89fc4] mt-auto pt-3 border-t border-[rgba(124,58,237,0.1)]">
            {raga.vadi && <span>Vadi: <span className="text-[#f5f0ff]">{raga.vadi}</span></span>}
            {raga.time_of_day && <span>Time: <span className="text-[#f5f0ff]">{raga.time_of_day}</span></span>}
          </div>
        )}

        {!hasScale && !raga.vadi && (
          <p className="relative z-10 text-xs text-[#6b5d8a] mt-auto italic">Musical details to be added</p>
        )}
      </div>
    </Link>
  )
}
