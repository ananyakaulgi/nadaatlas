import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import type { Artist } from '@/lib/types'

function formatYear(dateStr: string | null): string | null {
  if (!dateStr) return null
  try {
    return String(new Date(dateStr).getFullYear())
  } catch {
    return null
  }
}

export default function ArtistCard({ artist }: { artist: Artist }) {
  const bornYear = formatYear(artist.born)
  const diedYear = formatYear(artist.died)

  return (
    <Link href={`/artists/${artist.id}`}>
      <div
        className="group relative rounded-2xl p-6 hover:scale-[1.01] transition-all duration-300 h-full flex flex-col"
        style={{
          background: 'rgba(20, 14, 40, 0.65)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(20,184,166,0.18)',
          boxShadow: '0 2px 16px rgba(20,184,166,0.08)',
        }}
      >
        <div
          className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
          style={{ background: 'radial-gradient(ellipse at top left, rgba(20,184,166,0.08), transparent 65%)' }}
        />

        <div className="relative z-10 flex items-start justify-between gap-2 mb-2">
          <h3 className="font-display text-xl text-[#f5f0ff] group-hover:text-[#5eead4] transition-colors leading-tight">
            {artist.name}
          </h3>
          {artist.is_verified && (
            <span className="text-[#f59e0b] text-xs mt-1 drop-shadow-[0_0_6px_rgba(245,158,11,0.5)]" title="Verified">✦</span>
          )}
        </div>

        {artist.name_native && (
          <p className="relative z-10 font-display text-[#a89fc4] text-base italic mb-2">{artist.name_native}</p>
        )}

        {artist.musical_tradition && (
          <Badge variant="teal" className="mb-3 self-start relative z-10">{artist.musical_tradition}</Badge>
        )}

        {(bornYear || artist.nationality) && (
          <p className="relative z-10 text-xs text-[#6b5d8a] mb-3">
            {bornYear && diedYear ? `${bornYear} – ${diedYear}` : bornYear ? `b. ${bornYear}` : ''}
            {artist.nationality && bornYear ? ' · ' : ''}
            {artist.nationality}
          </p>
        )}

        {artist.biography_short && (
          <p className="relative z-10 text-sm text-[#a89fc4] leading-relaxed line-clamp-3 flex-1">
            {artist.biography_short}
          </p>
        )}

        <div
          className="relative z-10 mt-4 text-xs text-[#5eead4] font-medium tracking-wide group-hover:translate-x-0.5 transition-transform"
          style={{ textShadow: '0 0 8px rgba(94,234,212,0.3)' }}
        >
          View profile →
        </div>
      </div>
    </Link>
  )
}
