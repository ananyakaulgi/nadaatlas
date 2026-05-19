import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import type { Tradition } from '@/lib/types'

export default function TraditionCard({ tradition }: { tradition: Tradition }) {
  return (
    <Link href={`/traditions/${tradition.id}`}>
      <div
        className="group relative rounded-2xl p-6 hover:scale-[1.01] transition-all duration-300 h-full flex flex-col"
        style={{
          background: 'rgba(20, 14, 40, 0.65)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(124,58,237,0.18)',
          boxShadow: '0 2px 16px rgba(76,29,149,0.15)',
        }}
      >
        {/* Hover nebula glow */}
        <div
          className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
          style={{ background: 'radial-gradient(ellipse at top left, rgba(124,58,237,0.12), transparent 65%)' }}
        />

        <div className="relative z-10 flex items-start justify-between gap-2 mb-3">
          <h3 className="font-display text-xl text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors leading-tight">
            {tradition.name}
          </h3>
          {tradition.origin_period && (
            <Badge variant="gold" className="shrink-0 mt-0.5">{tradition.origin_period}</Badge>
          )}
        </div>

        {tradition.name_native && (
          <p className="relative z-10 font-display text-[#a89fc4] text-base italic mb-3">{tradition.name_native}</p>
        )}

        <div className="relative z-10 flex flex-wrap gap-1.5 mb-3">
          <Badge variant="teal">{tradition.region}</Badge>
          {tradition.subregion && <Badge variant="sage">{tradition.subregion}</Badge>}
        </div>

        {tradition.description && (
          <p className="relative z-10 text-sm text-[#a89fc4] leading-relaxed line-clamp-3 flex-1">
            {tradition.description}
          </p>
        )}

        <div
          className="relative z-10 mt-4 text-xs text-[#f59e0b] font-medium tracking-wide group-hover:translate-x-0.5 transition-transform"
          style={{ textShadow: '0 0 8px rgba(245,158,11,0.3)' }}
        >
          Explore →
        </div>
      </div>
    </Link>
  )
}
