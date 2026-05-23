import { getComposers } from '@/lib/api'
import ComposerCard from '@/components/cards/ComposerCard'
import type { Metadata } from 'next'
import type { Composer } from '@/lib/types'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Composers — नाद Atla𝄞',
  description: 'The composers who shaped world music — from the Carnatic Trinity to the masters of the Ottoman court',
}

export default async function ComposersPage() {
  let composers: Composer[] = []

  try {
    const result = await getComposers({ limit: 100 })
    composers = result.items
  } catch (err) {
    console.error('[ComposersPage] fetch failed:', err)
  }

  // Group by tradition name
  const byTradition: Record<string, typeof composers> = {}
  for (const c of composers) {
    const key = c.tradition?.name ?? 'Other'
    if (!byTradition[key]) byTradition[key] = []
    byTradition[key].push(c)
  }

  const TRADITION_ORDER = [
    'Western Classical',
    'Jazz',
    'Carnatic Classical', 'Hindustani Classical',
    'Tango', 'Flamenco', 'Afrobeat', 'Blues',
    'Persian Classical', 'Maqam (Arabic)', 'Turkish Classical',
    'Griot', 'Griot Music',
    'Qawwali',
    'Other',
  ]
  const orderedGroups = TRADITION_ORDER
    .filter((t) => byTradition[t])
    .map((t) => ({ name: t, items: byTradition[t] }))

  // Any traditions not in our order list
  for (const key of Object.keys(byTradition)) {
    if (!TRADITION_ORDER.includes(key)) {
      orderedGroups.push({ name: key, items: byTradition[key] })
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Composers</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          The architects of form — composers who distilled tradition into works that
          outlived their era and still resonate centuries on.
        </p>
      </div>

      {orderedGroups.length > 0 ? (
        <div className="space-y-14">
          {orderedGroups.map(({ name, items }) => (
            <section key={name}>
              <div className="flex items-center gap-3 mb-6">
                <h2 className="font-display text-2xl text-[#f5f0ff]">{name}</h2>
                <span
                  className="px-2.5 py-0.5 rounded-full text-xs font-medium"
                  style={{ background: 'rgba(124,58,237,0.15)', border: '1px solid rgba(124,58,237,0.3)', color: '#c4b5fd' }}
                >
                  {items.length}
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {items.map((c) => <ComposerCard key={c.id} composer={c} />)}
              </div>
            </section>
          ))}
        </div>
      ) : (
        <div className="text-center py-20">
          <p className="font-display text-xl text-[#c4b5fd] mb-2">No composers yet</p>
          <p className="text-sm text-[#a89fc4]">Composers will appear here as data is added.</p>
        </div>
      )}
    </div>
  )
}
