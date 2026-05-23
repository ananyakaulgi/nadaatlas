import { getTalas } from '@/lib/api'
import TalaCard from '@/components/cards/TalaCard'
import type { Metadata } from 'next'
import type { Tala } from '@/lib/types'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Talas — नाद Atla𝄞',
  description: 'Explore rhythmic cycles of Indian classical music — Hindustani and Carnatic talas',
}

export default async function TalasPage() {
  let hindustani: Tala[] = [], carnatic: Tala[] = []

  try {
    const [h, c] = await Promise.all([
      getTalas({ tradition: 'hindustani', limit: 50 }),
      getTalas({ tradition: 'carnatic',   limit: 50 }),
    ])
    hindustani = h.items
    carnatic   = c.items
  } catch (err) {
    console.error('[TalasPage] fetch failed:', err)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Talas</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          The rhythmic cycles that hold Indian classical music in time — each tala a unique
          pattern of beats, silences, and subdivisions.
        </p>
      </div>

      {/* Hindustani */}
      {hindustani.length > 0 && (
        <section className="mb-14">
          <div className="flex items-center gap-3 mb-6">
            <h2 className="font-display text-2xl text-[#f5f0ff]">Hindustani</h2>
            <span
              className="px-2.5 py-0.5 rounded-full text-xs font-medium"
              style={{ background: 'rgba(245,158,11,0.15)', border: '1px solid rgba(245,158,11,0.3)', color: '#f59e0b' }}
            >
              {hindustani.length} talas
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {hindustani.map((t) => <TalaCard key={t.id} tala={t} />)}
          </div>
        </section>
      )}

      {/* Carnatic */}
      {carnatic.length > 0 && (
        <section>
          <div className="flex items-center gap-3 mb-6">
            <h2 className="font-display text-2xl text-[#f5f0ff]">Carnatic</h2>
            <span
              className="px-2.5 py-0.5 rounded-full text-xs font-medium"
              style={{ background: 'rgba(20,184,166,0.15)', border: '1px solid rgba(20,184,166,0.3)', color: '#2dd4bf' }}
            >
              {carnatic.length} talas
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {carnatic.map((t) => <TalaCard key={t.id} tala={t} />)}
          </div>
        </section>
      )}
    </div>
  )
}
