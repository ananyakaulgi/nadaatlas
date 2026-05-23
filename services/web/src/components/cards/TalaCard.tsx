import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import type { Tala } from '@/lib/types'

const TRADITION_COLORS = {
  hindustani: { border: 'rgba(245,158,11,0.3)', glow: 'rgba(245,158,11,0.12)', badge: 'gold' as const },
  carnatic:   { border: 'rgba(20,184,166,0.3)',  glow: 'rgba(20,184,166,0.1)',  badge: 'teal' as const },
  both:       { border: 'rgba(124,58,237,0.3)',  glow: 'rgba(124,58,237,0.12)', badge: 'lavender' as const },
}

export default function TalaCard({ tala }: { tala: Tala }) {
  const colors = TRADITION_COLORS[tala.tradition as keyof typeof TRADITION_COLORS] ?? TRADITION_COLORS.both

  return (
    <Link href={`/talas/${tala.id}`}>
      <div
        className="group relative rounded-2xl p-6 hover:scale-[1.01] transition-all duration-300 h-full flex flex-col"
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
          <h3 className="font-display text-xl text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors leading-tight">
            {tala.name}
          </h3>
          <Badge variant={colors.badge} className="shrink-0 capitalize">
            {tala.tradition}
          </Badge>
        </div>

        {tala.name_native && (
          <p className="relative z-10 font-display text-[#a89fc4] text-sm italic mb-3">{tala.name_native}</p>
        )}

        {/* Beat count — big prominent number */}
        {tala.beats !== null && (
          <div className="relative z-10 flex items-baseline gap-1.5 mb-3">
            <span
              className="font-display text-4xl font-light leading-none"
              style={{ color: colors.badge === 'gold' ? '#f59e0b' : colors.badge === 'teal' ? '#2dd4bf' : '#c4b5fd'  /* lavender */ }}
            >
              {tala.beats}
            </span>
            <span className="text-[#6b5d8a] text-sm">beats</span>
            {tala.anga_structure && (
              <span className="font-mono text-xs text-[#a89fc4] ml-2">{tala.anga_structure}</span>
            )}
          </div>
        )}

        {/* Jati */}
        {tala.jati && (
          <div className="relative z-10 mb-3">
            <Badge variant="sage" className="capitalize">{tala.jati} jati</Badge>
          </div>
        )}

        {/* Description excerpt */}
        {tala.description && (
          <p className="relative z-10 text-sm text-[#a89fc4] leading-relaxed line-clamp-2 flex-1 mt-1">
            {tala.description}
          </p>
        )}

        {/* Common tempos */}
        {tala.common_tempos && tala.common_tempos.length > 0 && (
          <div className="relative z-10 mt-3 pt-3 border-t border-[rgba(124,58,237,0.1)] flex flex-wrap gap-1">
            {tala.common_tempos.map((t) => (
              <span key={t} className="text-xs text-[#6b5d8a] capitalize">{t}</span>
            ))}
          </div>
        )}
      </div>
    </Link>
  )
}
