import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import type { Instrument } from '@/lib/types'

export default function InstrumentCard({ instrument }: { instrument: Instrument }) {
  return (
    <Link href={`/instruments/${instrument.id}`}>
      <div
        className="group relative rounded-2xl p-6 hover:scale-[1.01] transition-all duration-300 h-full flex flex-col"
        style={{
          background: 'rgba(20, 14, 40, 0.65)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(167,139,250,0.18)',
          boxShadow: '0 2px 16px rgba(124,58,237,0.1)',
        }}
      >
        <div
          className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
          style={{ background: 'radial-gradient(ellipse at top left, rgba(167,139,250,0.1), transparent 65%)' }}
        />

        <div className="relative z-10 flex items-start justify-between gap-2 mb-2">
          <h3 className="font-display text-xl text-[#f5f0ff] group-hover:text-[#ddd6fe] transition-colors leading-tight">
            {instrument.name}
          </h3>
          {instrument.hs_category && (
            <Badge variant="lavender" className="shrink-0 mt-0.5">{instrument.hs_category}</Badge>
          )}
        </div>

        {instrument.name_native && (
          <p className="relative z-10 font-display text-[#a89fc4] text-base italic mb-3">{instrument.name_native}</p>
        )}

        {instrument.origin_region && (
          <p className="relative z-10 text-xs text-[#6b5d8a] mb-3">{instrument.origin_region}</p>
        )}

        {instrument.description && (
          <p className="relative z-10 text-sm text-[#a89fc4] leading-relaxed line-clamp-3 flex-1">
            {instrument.description}
          </p>
        )}

        <div
          className="relative z-10 mt-4 text-xs text-[#a78bfa] font-medium tracking-wide group-hover:translate-x-0.5 transition-transform"
          style={{ textShadow: '0 0 8px rgba(167,139,250,0.3)' }}
        >
          Learn more →
        </div>
      </div>
    </Link>
  )
}
