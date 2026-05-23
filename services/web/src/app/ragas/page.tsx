import { getRagas } from '@/lib/api'
import RagasClient from './RagasClient'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Ragas — नाद Atla𝄞',
  description: 'Explore 1,200+ ragas from Hindustani and Carnatic classical music traditions',
}

const HINDUSTANI_THAATS = [
  'Kalyan','Bilawal','Khamaj','Bhairav','Poorvi',
  'Marwa','Kafi','Asavari','Bhairavi','Todi',
]

interface PageProps {
  searchParams: Promise<{ tradition?: string; that?: string; search?: string; page?: string }>
}

export default async function RagasPage({ searchParams }: PageProps) {
  const params = await searchParams
  const tradition = params.tradition || ''
  const that      = params.that || ''
  const search    = params.search || ''
  const page      = Number(params.page || 1)
  const limit     = 60
  const skip      = (page - 1) * limit

  let result = { items: [], total: 0, skip: 0, limit }

  try {
    result = await getRagas({
      skip,
      limit,
      ...(tradition && { tradition }),
      ...(that && { that }),
      ...(search && { search }),
    })
  } catch (err) {
    console.error('[RagasPage] fetch failed:', err)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Ragas</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          The melodic frameworks of Indian classical music — each raga a precise set of notes,
          rules, and emotional colours woven over centuries.
        </p>
      </div>

      <RagasClient
        initialItems={result.items}
        total={result.total}
        page={page}
        limit={limit}
        thaats={HINDUSTANI_THAATS}
        initialTradition={tradition}
        initialThat={that}
        initialSearch={search}
      />
    </div>
  )
}
