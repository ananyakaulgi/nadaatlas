import { getRegions } from '@/lib/api'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Regions — नाद Atla𝄞',
  description: 'Browse music traditions and cultures by world region',
}

const CONTINENT_COLORS: Record<string, { border: string; glow: string; accent: string }> = {
  'Asia':     { border: 'rgba(245,158,11,0.3)',  glow: 'rgba(245,158,11,0.1)',  accent: '#f59e0b' },
  'Africa':   { border: 'rgba(20,184,166,0.3)',  glow: 'rgba(20,184,166,0.1)',  accent: '#2dd4bf' },
  'Americas': { border: 'rgba(236,72,153,0.25)', glow: 'rgba(236,72,153,0.08)', accent: '#f472b6' },
  'Europe':   { border: 'rgba(99,102,241,0.3)',  glow: 'rgba(99,102,241,0.1)',  accent: '#818cf8' },
}

export default async function RegionsPage() {
  let regions: Awaited<ReturnType<typeof getRegions>>['items'] = []

  try {
    const result = await getRegions({ limit: 100 })
    regions = result.items
  } catch (err) {
    console.error('[RegionsPage] fetch failed:', err)
  }

  // Group by continent
  const byContinent: Record<string, typeof regions> = {}
  for (const r of regions) {
    const key = r.continent ?? 'Other'
    if (!byContinent[key]) byContinent[key] = []
    byContinent[key].push(r)
  }

  const continentOrder = ['Asia', 'Africa', 'Americas', 'Europe', 'Other']
  const groups = continentOrder
    .filter((c) => byContinent[c])
    .map((c) => ({ continent: c, items: byContinent[c] }))

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-12">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Regions</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          Music is geography. Every mountain range, river delta, and desert crossing has
          shaped the sound of its people across {regions.length} distinct musical regions.
        </p>
      </div>

      {groups.length > 0 ? (
        <div className="space-y-12">
          {groups.map(({ continent, items }) => {
            const colors = CONTINENT_COLORS[continent] ?? { border: 'rgba(124,58,237,0.3)', glow: 'rgba(124,58,237,0.1)', accent: '#c4b5fd' }
            return (
              <section key={continent}>
                <div className="flex items-center gap-3 mb-6">
                  <h2 className="font-display text-2xl text-[#f5f0ff]">{continent}</h2>
                  <span
                    className="px-2.5 py-0.5 rounded-full text-xs font-medium"
                    style={{ background: colors.glow, border: `1px solid ${colors.border}`, color: colors.accent }}
                  >
                    {items.length} regions
                  </span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {items.map((region) => (
                    <div
                      key={region.id}
                      className="rounded-2xl p-5 transition-all duration-300"
                      style={{
                        background: 'rgba(20,14,40,0.65)',
                        backdropFilter: 'blur(12px)',
                        border: `1px solid ${colors.border}`,
                        boxShadow: `0 2px 12px ${colors.glow}`,
                      }}
                    >
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <h3 className="font-display text-lg text-[#f5f0ff]">{region.name}</h3>
                        {region.country_name && (
                          <span className="text-xs text-[#6b5d8a] shrink-0 mt-1">{region.country_name}</span>
                        )}
                      </div>
                      {region.state && (
                        <p className="text-xs text-[#6b5d8a] mb-2">{region.state}</p>
                      )}
                      {region.description && (
                        <p className="text-sm text-[#a89fc4] leading-relaxed line-clamp-3">
                          {region.description}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </section>
            )
          })}
        </div>
      ) : (
        <div className="text-center py-20">
          <div className="bg-[rgba(20,14,40,0.7)] rounded-2xl p-12 border border-[rgba(124,58,237,0.2)] inline-block">
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No regions yet</p>
            <p className="text-sm text-[#a89fc4]">Regions will appear here as data is added.</p>
          </div>
        </div>
      )}
    </div>
  )
}
