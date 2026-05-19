import { getTraditions } from '@/lib/api'
import TraditionsClient from './TraditionsClient'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Traditions',
  description: 'Explore musical traditions from every corner of the world',
}

export default async function TraditionsPage({
  searchParams,
}: {
  searchParams: Promise<{ region?: string }>
}) {
  const { region } = await searchParams
  let traditions: Awaited<ReturnType<typeof getTraditions>>['items'] = []

  try {
    const result = await getTraditions({ limit: 200 })
    traditions = result.items
  } catch {
    // API not available
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Musical Traditions</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          From ancient ceremonial music to living folk traditions — a window into how humanity has shaped sound across continents and centuries.
        </p>
      </div>

      {traditions.length === 0 ? (
        <div className="text-center py-20">
          <div
            className="rounded-2xl p-12 inline-block"
            style={{
              background: 'rgba(20,14,40,0.7)',
              border: '1px solid rgba(124,58,237,0.2)',
              backdropFilter: 'blur(12px)',
            }}
          >
            <p className="font-display text-xl text-[#c4b5fd] mb-2">The cosmos is quiet</p>
            <p className="text-sm text-[#a89fc4]">Unable to reach the API. Please ensure the server is running.</p>
          </div>
        </div>
      ) : (
        <TraditionsClient traditions={traditions} initialRegion={region} />
      )}
    </div>
  )
}
