import { getArtists } from '@/lib/api'
import ArtistsClient from './ArtistsClient'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Artists',
  description: 'Discover artists and musicians from world music traditions',
}

export default async function ArtistsPage({
  searchParams,
}: {
  searchParams: Promise<{ musical_tradition?: string }>
}) {
  const { musical_tradition } = await searchParams
  let artists: Awaited<ReturnType<typeof getArtists>>['items'] = []

  try {
    const result = await getArtists({ limit: 100 })
    artists = result.items
  } catch (err) {
    console.error('[ArtistsPage] Failed to fetch:', err)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Artists</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          The living voices of ancient traditions — masters, innovators, and guardians of sound.
        </p>
      </div>

      {artists.length === 0 ? (
        <div className="text-center py-20">
          <div className="bg-[rgba(20,14,40,0.7)] rounded-2xl p-12 border border-[rgba(124,58,237,0.2)] inline-block">
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No artists yet</p>
            <p className="text-sm text-[#a89fc4]">
              The artist catalog is being assembled. Check back soon, or ensure the API is running.
            </p>
          </div>
        </div>
      ) : (
        <ArtistsClient artists={artists} initialTradition={musical_tradition} />
      )}
    </div>
  )
}
