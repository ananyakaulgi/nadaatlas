import { getArtists } from '@/lib/api'
import Link from 'next/link'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Browse by Genre',
  description: 'Explore world music by genre and musical tradition',
}

export default async function GenresPage() {
  let genreCounts: Record<string, number> = {}

  try {
    const result = await getArtists({ limit: 100 })
    for (const a of result.items) {
      if (a.musical_tradition) {
        genreCounts[a.musical_tradition] = (genreCounts[a.musical_tradition] || 0) + 1
      }
    }
  } catch (err) {
    console.error('[GenresPage] Failed to fetch:', err)
  }

  const genreEntries = Object.entries(genreCounts).sort((a, b) => b[1] - a[1])

  // Cycle through nebula accent colors
  const GENRE_ACCENTS = [
    { border: 'rgba(124,58,237,0.3)',  glow: 'rgba(124,58,237,0.15)' },
    { border: 'rgba(245,158,11,0.28)', glow: 'rgba(245,158,11,0.12)' },
    { border: 'rgba(20,184,166,0.25)', glow: 'rgba(20,184,166,0.1)'  },
    { border: 'rgba(236,72,153,0.25)', glow: 'rgba(236,72,153,0.1)'  },
    { border: 'rgba(99,102,241,0.3)',  glow: 'rgba(99,102,241,0.12)' },
    { border: 'rgba(217,119,6,0.28)',  glow: 'rgba(217,119,6,0.1)'   },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-12">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Browse by Genre</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          Musical traditions as genres — each one a living, evolving language of sound.
        </p>
      </div>

      {genreEntries.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {genreEntries.map(([genre, count], idx) => {
            const accent = GENRE_ACCENTS[idx % GENRE_ACCENTS.length]
            return (
              <Link key={genre} href={`/artists?musical_tradition=${encodeURIComponent(genre)}`}>
                <div
                  className="group relative rounded-2xl p-7 hover:scale-[1.02] transition-all duration-300"
                  style={{
                    background: 'rgba(20,14,40,0.65)',
                    backdropFilter: 'blur(12px)',
                    border: `1px solid ${accent.border}`,
                    boxShadow: `0 4px 20px ${accent.glow}`,
                  }}
                >
                  <div
                    className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                    style={{ background: `radial-gradient(ellipse at top left, ${accent.glow}, transparent 70%)` }}
                  />
                  <h3 className="relative z-10 font-display text-2xl text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors mb-2">
                    {genre}
                  </h3>
                  <p className="relative z-10 text-sm text-[#a89fc4]">
                    {count} {count === 1 ? 'artist' : 'artists'}
                  </p>
                </div>
              </Link>
            )
          })}
        </div>
      ) : (
        <div className="text-center py-20">
          <div
            className="rounded-2xl p-12 inline-block"
            style={{
              background: 'rgba(20,14,40,0.7)',
              border: '1px solid rgba(124,58,237,0.2)',
              backdropFilter: 'blur(12px)',
            }}
          >
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No genres yet</p>
            <p className="text-sm text-[#a89fc4]">
              Add artists with musical traditions to populate the genre browser.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
