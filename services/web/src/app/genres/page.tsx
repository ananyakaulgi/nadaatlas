import { getGenres } from '@/lib/api'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Genres — नाद Atla𝄞',
  description: 'Explore world music by genre — from Hindustani Classical and Carnatic to Jazz, Reggae, Gnawa, and beyond',
}

const GENRE_ACCENTS = [
  { border: 'rgba(124,58,237,0.3)',  glow: 'rgba(124,58,237,0.12)', accent: '#c4b5fd' },
  { border: 'rgba(245,158,11,0.28)', glow: 'rgba(245,158,11,0.1)',  accent: '#f59e0b' },
  { border: 'rgba(20,184,166,0.25)', glow: 'rgba(20,184,166,0.08)', accent: '#2dd4bf' },
  { border: 'rgba(236,72,153,0.25)', glow: 'rgba(236,72,153,0.08)', accent: '#f472b6' },
  { border: 'rgba(99,102,241,0.3)',  glow: 'rgba(99,102,241,0.1)',  accent: '#818cf8' },
  { border: 'rgba(217,119,6,0.28)',  glow: 'rgba(217,119,6,0.08)',  accent: '#fbbf24' },
]

export default async function GenresPage() {
  let genres: Awaited<ReturnType<typeof getGenres>>['items'] = []

  try {
    const result = await getGenres({ limit: 100 })
    genres = result.items
  } catch (err) {
    console.error('[GenresPage] fetch failed:', err)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-12">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Genres</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          {genres.length} musical genres — each one a living, evolving language of sound.
        </p>
      </div>

      {genres.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {genres.map((genre, idx) => {
            const accent = GENRE_ACCENTS[idx % GENRE_ACCENTS.length]
            return (
              <div
                key={genre.id}
                className="group relative rounded-2xl p-7 transition-all duration-300 hover:scale-[1.01]"
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
                <h3
                  className="relative z-10 font-display text-2xl mb-2 transition-colors"
                  style={{ color: accent.accent }}
                >
                  {genre.name}
                </h3>
                {genre.description && (
                  <p className="relative z-10 text-sm text-[#a89fc4] leading-relaxed line-clamp-3">
                    {genre.description}
                  </p>
                )}
              </div>
            )
          })}
        </div>
      ) : (
        <div className="text-center py-20">
          <div className="rounded-2xl p-12 inline-block" style={{ background: 'rgba(20,14,40,0.7)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}>
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No genres yet</p>
            <p className="text-sm text-[#a89fc4]">Genres will appear here as data is added.</p>
          </div>
        </div>
      )}
    </div>
  )
}
