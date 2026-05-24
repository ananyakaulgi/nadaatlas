import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import LinkedBadge from '@/components/ui/LinkedBadge'
import type { Composer } from '@/lib/types'

export default function ComposerCard({ composer }: { composer: Composer }) {
  const birthYear = composer.born ? new Date(composer.born).getFullYear() : null
  const deathYear = composer.died ? new Date(composer.died).getFullYear() : null

  return (
    <Link href={`/composers/${composer.id}`}>
      <div
        className="group relative rounded-2xl p-6 hover:scale-[1.01] transition-all duration-300 h-full flex flex-col"
        style={{
          background: 'rgba(20,14,40,0.65)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(124,58,237,0.2)',
          boxShadow: '0 2px 16px rgba(76,29,149,0.15)',
        }}
      >
        <div
          className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
          style={{ background: 'radial-gradient(ellipse at top left, rgba(124,58,237,0.1), transparent 65%)' }}
        />

        {/* Name + verified */}
        <div className="relative z-10 flex items-start justify-between gap-2 mb-1">
          <h3 className="font-display text-xl text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors leading-tight">
            {composer.name}
          </h3>
          {composer.is_verified && (
            <span className="text-[#f59e0b] text-xs mt-1" title="Verified">✦</span>
          )}
        </div>

        {composer.name_native && (
          <p className="relative z-10 font-display text-[#a89fc4] text-base italic mb-3">{composer.name_native}</p>
        )}

        {/* Dates + tradition */}
        <div className="relative z-10 flex flex-wrap gap-1.5 mb-3">
          {composer.era && (
            <LinkedBadge href={`/composers?era=${encodeURIComponent(composer.era)}`} variant="gold">
              {composer.era}
            </LinkedBadge>
          )}
          {(birthYear || deathYear) && (
            <Badge variant="sage">
              {birthYear ?? '?'}{deathYear ? ` – ${deathYear}` : ''}
            </Badge>
          )}
          {composer.tradition && (
            <LinkedBadge href={`/traditions/${composer.tradition.id}`} variant="teal">
              {composer.tradition.name}
            </LinkedBadge>
          )}
        </div>

        {/* Nationality / birth place */}
        {(composer.nationality || composer.birth_place) && (
          <p className="relative z-10 text-xs text-[#6b5d8a] mb-3">
            {[composer.nationality, composer.birth_place].filter(Boolean).join(' · ')}
          </p>
        )}

        {/* Bio excerpt */}
        {composer.biography_short && (
          <p className="relative z-10 text-sm text-[#a89fc4] leading-relaxed line-clamp-3 flex-1">
            {composer.biography_short}
          </p>
        )}

        <div
          className="relative z-10 mt-4 text-xs text-[#f59e0b] font-medium tracking-wide group-hover:translate-x-0.5 transition-transform"
          style={{ textShadow: '0 0 8px rgba(245,158,11,0.3)' }}
        >
          View composer →
        </div>
      </div>
    </Link>
  )
}
