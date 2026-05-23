import { getArtists } from '@/lib/api'
import ArtistsClient from './ArtistsClient'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Artists — नाद Atla𝄞',
  description: 'Discover artists and musicians from world music traditions',
}

interface PageProps {
  searchParams: Promise<{
    search?: string
    musical_tradition?: string
    page?: string
  }>
}

export default async function ArtistsPage({ searchParams }: PageProps) {
  const params = await searchParams
  const page  = Number(params.page || 1)
  const limit = 40
  const skip  = (page - 1) * limit

  let result = { items: [], total: 0, skip: 0, limit }

  try {
    result = await getArtists({
      skip,
      limit,
      ...(params.search            && { search:            params.search }),
      ...(params.musical_tradition && { musical_tradition: params.musical_tradition }),
    })
  } catch (err) {
    console.error('[ArtistsPage] fetch failed:', err)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Artists</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          The living voices of ancient traditions — masters, innovators, and guardians of sound.
        </p>
      </div>

      <ArtistsClient
        initialItems={result.items}
        total={result.total}
        page={page}
        limit={limit}
        initialSearch={params.search || ''}
        initialTradition={params.musical_tradition || ''}
      />
    </div>
  )
}
