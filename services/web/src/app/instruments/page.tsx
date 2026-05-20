import { getInstruments } from '@/lib/api'
import InstrumentsClient from './InstrumentsClient'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Instruments',
  description: 'Musical instruments from traditions around the world',
}

export default async function InstrumentsPage() {
  let instruments: Awaited<ReturnType<typeof getInstruments>>['items'] = []

  try {
    const result = await getInstruments({ limit: 100 })
    instruments = result.items
  } catch (err) {
    console.error('[InstrumentsPage] Failed to fetch:', err)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Instruments</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          The physical poetry of music — from the oud to the koto, each instrument carries the memory of its land.
        </p>
      </div>

      {instruments.length === 0 ? (
        <div className="text-center py-20">
          <div className="bg-[rgba(20,14,40,0.7)] rounded-2xl p-12 border border-[rgba(124,58,237,0.2)] inline-block">
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No instruments yet</p>
            <p className="text-sm text-[#a89fc4]">
              The instrument catalog is being assembled. Check back soon.
            </p>
          </div>
        </div>
      ) : (
        <InstrumentsClient instruments={instruments} />
      )}
    </div>
  )
}
