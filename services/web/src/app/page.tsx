import Link from 'next/link'
import { getTraditions } from '@/lib/api'

export const dynamic = 'force-dynamic'
import TraditionCard from '@/components/cards/TraditionCard'
import RegionCard from '@/components/cards/RegionCard'
import { Music2, Users, Disc3, Piano } from 'lucide-react'

const FEATURE_CARDS = [
  {
    href: '/traditions',
    icon: Music2,
    title: 'Traditions',
    description: 'Explore musical traditions from every corner of the world',
    glow: 'rgba(124,58,237,0.25)',
    iconColor: 'text-[#c4b5fd]',
    borderColor: 'rgba(124,58,237,0.3)',
  },
  {
    href: '/artists',
    icon: Users,
    title: 'Artists',
    description: 'Discover the masters who carry these traditions forward',
    glow: 'rgba(147,51,234,0.2)',
    iconColor: 'text-[#a78bfa]',
    borderColor: 'rgba(147,51,234,0.25)',
  },
  {
    href: '/instruments',
    icon: Piano,
    title: 'Instruments',
    description: 'The voices of wood, string, skin, and breath',
    glow: 'rgba(245,158,11,0.2)',
    iconColor: 'text-[#f59e0b]',
    borderColor: 'rgba(245,158,11,0.25)',
  },
  {
    href: '/albums',
    icon: Disc3,
    title: 'Albums',
    description: 'Recordings that capture the soul of each tradition',
    glow: 'rgba(217,119,6,0.2)',
    iconColor: 'text-[#fbbf24]',
    borderColor: 'rgba(217,119,6,0.25)',
  },
]

export default async function HomePage() {
  let traditions: Awaited<ReturnType<typeof getTraditions>>['items'] = []
  const regions: Record<string, number> = {}

  try {
    const result = await getTraditions({ limit: 100 })
    traditions = result.items

    for (const t of traditions) {
      if (t.region) {
        regions[t.region] = (regions[t.region] || 0) + 1
      }
    }
  } catch (err) {
    console.error('[HomePage] Failed to fetch traditions:', err)
  }

  const featuredTraditions = traditions.slice(0, 6)
  const regionEntries = Object.entries(regions).sort((a, b) => b[1] - a[1])

  return (
    <div>
      {/* ── Hero ──────────────────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden py-32 px-4 min-h-[80vh] flex items-center">

        {/* Nebula soft-light layers */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-[-10%] right-[-5%] w-[70vw] h-[70vw] max-w-[900px] max-h-[900px] rounded-full opacity-25"
            style={{ background: 'radial-gradient(ellipse, rgba(109,40,217,0.5) 0%, rgba(76,29,149,0.25) 40%, transparent 70%)' }}
          />
          <div className="absolute bottom-[-15%] left-[-10%] w-[60vw] h-[60vw] max-w-[700px] max-h-[700px] rounded-full opacity-18"
            style={{ background: 'radial-gradient(ellipse, rgba(147,51,234,0.55) 0%, rgba(124,58,237,0.18) 40%, transparent 70%)' }}
          />
        </div>

        {/* Hero text */}
        <div className="relative z-10 max-w-4xl mx-auto text-center">
          <div className="mb-3">
            <span className="inline-block text-[#f59e0b] text-sm font-medium tracking-[0.2em] uppercase opacity-80">
              ♪ &nbsp; Your musical compass &nbsp; ♪
            </span>
          </div>
          <h1
            className="font-display text-7xl sm:text-8xl md:text-9xl text-[#f5f0ff] mb-6 leading-none tracking-tight"
            style={{ textShadow: '0 0 60px rgba(124,58,237,0.35), 0 0 120px rgba(124,58,237,0.12)' }}
          >
            MusiCompass
          </h1>
          <p className="font-display text-2xl sm:text-3xl text-[#c4b5fd] italic font-light mb-8 leading-relaxed">
            Navigate the world&apos;s musical traditions
          </p>
          <p className="text-[#a89fc4] text-lg max-w-2xl mx-auto leading-relaxed mb-12">
            Journey through centuries of sound — from the highlands of Ethiopia to the rivers of Bengal,
            from the steppes of Central Asia to the shores of the Pacific.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="/traditions"
              className="group px-8 py-3.5 text-sm font-medium rounded-xl transition-all duration-300 relative overflow-hidden"
              style={{
                background: 'linear-gradient(135deg, #7c3aed, #6d28d9)',
                boxShadow: '0 0 20px rgba(124,58,237,0.4), 0 0 40px rgba(124,58,237,0.15)',
                color: '#f5f0ff',
              }}
            >
              <span className="relative z-10">Explore Traditions</span>
              <div className="absolute inset-0 bg-gradient-to-r from-[#9333ea] to-[#7c3aed] opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </Link>
            <Link
              href="/regions"
              className="px-8 py-3.5 text-[#c4b5fd] text-sm font-medium rounded-xl border border-[rgba(124,58,237,0.35)] hover:border-[rgba(124,58,237,0.6)] hover:bg-[rgba(124,58,237,0.1)] transition-all duration-300 backdrop-blur-sm"
            >
              Browse by Region
            </Link>
          </div>
        </div>
      </section>

      {/* ── Feature Cards ─────────────────────────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="font-display text-3xl text-[#f5f0ff] text-center mb-3">
          What would you like to explore?
        </h2>
        <p className="text-[#a89fc4] text-center mb-12 max-w-xl mx-auto">
          Every tradition, every artist, every instrument — charted.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {FEATURE_CARDS.map((card) => {
            const Icon = card.icon
            return (
              <Link key={card.href} href={card.href}>
                <div
                  className="group relative rounded-2xl p-7 h-full transition-all duration-300 hover:scale-[1.02]"
                  style={{
                    background: 'rgba(20, 14, 40, 0.7)',
                    backdropFilter: 'blur(12px)',
                    border: `1px solid ${card.borderColor}`,
                    boxShadow: `0 4px 24px ${card.glow}`,
                  }}
                >
                  <div
                    className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                    style={{ background: `radial-gradient(ellipse at top left, ${card.glow}, transparent 60%)` }}
                  />
                  <Icon className={`relative z-10 w-7 h-7 ${card.iconColor} mb-4 group-hover:scale-110 transition-transform duration-200`} />
                  <h3 className="relative z-10 font-display text-xl text-[#f5f0ff] mb-2">{card.title}</h3>
                  <p className="relative z-10 text-sm text-[#a89fc4] leading-relaxed">{card.description}</p>
                </div>
              </Link>
            )
          })}
        </div>
      </section>

      {/* ── Explore by Region ─────────────────────────────────────────────────── */}
      {regionEntries.length > 0 && (
        <section className="py-20" style={{ background: 'linear-gradient(180deg, #0d0a1a 0%, #130f25 50%, #0d0a1a 100%)' }}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="font-display text-3xl text-[#f5f0ff] text-center mb-3">
              Explore by Region
            </h2>
            <p className="text-[#a89fc4] text-center mb-12 max-w-xl mx-auto">
              Music is geography. Discover how landscape shapes sound.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {regionEntries.map(([region, count]) => (
                <RegionCard key={region} region={region} count={count} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ── Featured Traditions ───────────────────────────────────────────────── */}
      {featuredTraditions.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="flex items-end justify-between mb-10">
            <div>
              <h2 className="font-display text-3xl text-[#f5f0ff] mb-2">Featured Traditions</h2>
              <p className="text-[#a89fc4]">A selection from the compass</p>
            </div>
            <Link
              href="/traditions"
              className="text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
              style={{ textShadow: '0 0 10px rgba(245,158,11,0.3)' }}
            >
              View all →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {featuredTraditions.map((tradition) => (
              <TraditionCard key={tradition.id} tradition={tradition} />
            ))}
          </div>
        </section>
      )}

      {/* ── Empty state ───────────────────────────────────────────────────────── */}
      {traditions.length === 0 && (
        <section className="max-w-xl mx-auto px-4 py-20 text-center">
          <div
            className="rounded-2xl p-12"
            style={{
              background: 'rgba(20, 14, 40, 0.7)',
              border: '1px solid rgba(124,58,237,0.2)',
              backdropFilter: 'blur(12px)',
            }}
          >
            <p className="font-display text-2xl text-[#c4b5fd] mb-3">The cosmos is quiet</p>
            <p className="text-[#a89fc4] text-sm">
              We&apos;re unable to reach the library at the moment. Please ensure the API server is running.
            </p>
          </div>
        </section>
      )}
    </div>
  )
}
