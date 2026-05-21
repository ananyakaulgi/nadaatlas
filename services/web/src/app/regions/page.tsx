import { getTraditions } from '@/lib/api'
import RegionCard from '@/components/cards/RegionCard'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Regions',
  description: 'Browse musical traditions by world region',
}

export default async function RegionsPage() {
  const regions: Record<string, number> = {}

  try {
    const result = await getTraditions({ limit: 100 })
    for (const t of result.items) {
      if (t.region) {
        regions[t.region] = (regions[t.region] || 0) + 1
      }
    }
  } catch (err) {
    console.error('[RegionsPage] Failed to fetch:', err)
  }

  const regionEntries = Object.entries(regions).sort((a, b) => b[1] - a[1])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-12">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Browse by Region</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          Music is geography. Every mountain range, river delta, and desert crossing has shaped the sound of its people.
        </p>
      </div>

      {regionEntries.length > 0 ? (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
          {regionEntries.map(([region, count]) => (
            <RegionCard key={region} region={region} count={count} />
          ))}
        </div>
      ) : (
        <div className="text-center py-20">
          <div className="bg-[rgba(20,14,40,0.7)] rounded-2xl p-12 border border-[rgba(124,58,237,0.2)] inline-block">
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No regions yet</p>
            <p className="text-sm text-[#a89fc4]">
              Add traditions to the atlas to populate the regions map.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
