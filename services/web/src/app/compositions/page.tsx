import { getCompositions } from '@/lib/api'
import CompositionsClient from './CompositionsClient'
import type { Metadata } from 'next'
import type { Composition } from '@/lib/types'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Compositions — नाद Atla𝄞',
  description: 'Explore classical compositions — kritis, dhrupad, khayal, ghazal, and more',
}

const COMPOSITION_TYPES = [
  // Western Classical
  'symphony', 'concerto', 'sonata', 'opera', 'oratorio', 'mass', 'requiem',
  'ballet', 'suite', 'prelude', 'toccata', 'fugue', 'nocturne', 'ballade',
  'caprice', 'bagatelle', 'serenade', 'dance', 'variation',
  // Jazz & Popular
  'jazz', 'blues',
  // Tango / Latin
  'tango',
  // African
  'afrobeat', 'epic',
  // Flamenco
  'flamenco',
  // Indian Classical (Carnatic)
  'kriti', 'varnam', 'javali', 'tillana', 'padam',
  // Indian Classical (Hindustani)
  'dhrupad', 'khayal', 'thumri', 'ghazal', 'tarana', 'dadra', 'chaiti', 'kajri',
  // Arabic / Turkish / Sufi
  'qawwali', 'muwashshah', 'ayin', 'tasnif', 'maqam',
]

interface PageProps {
  searchParams: Promise<{
    composer_id?: string
    tradition_id?: string
    raga_id?: string
    composition_type?: string
    search?: string
    page?: string
  }>
}

export default async function CompositionsPage({ searchParams }: PageProps) {
  const params = await searchParams
  const page   = Number(params.page || 1)
  const limit  = 40
  const skip   = (page - 1) * limit

  let result: { items: Composition[]; total: number; skip: number; limit: number } = { items: [], total: 0, skip: 0, limit }

  try {
    result = await getCompositions({
      skip,
      limit,
      ...(params.composer_id      && { composer_id:      params.composer_id }),
      ...(params.tradition_id     && { tradition_id:     params.tradition_id }),
      ...(params.raga_id          && { raga_id:          params.raga_id }),
      ...(params.composition_type && { composition_type: params.composition_type }),
      ...(params.search           && { search:           params.search }),
    })
  } catch (err) {
    console.error('[CompositionsPage] fetch failed:', err)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Compositions</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          The works themselves — kritis, dhrupad, khayal, ghazal, and the full canon of
          Indian and world classical composition.
        </p>
      </div>

      <CompositionsClient
        initialItems={result.items}
        total={result.total}
        page={page}
        limit={limit}
        compositionTypes={COMPOSITION_TYPES}
        initialType={params.composition_type || ''}
        initialSearch={params.search || ''}
      />
    </div>
  )
}
