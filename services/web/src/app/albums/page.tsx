import { getAlbums } from '@/lib/api'
import AlbumsClient from './AlbumsClient'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Albums',
  description: 'Recordings from world music traditions',
}

export default async function AlbumsPage({
  searchParams,
}: {
  searchParams: Promise<{ musical_tradition?: string }>
}) {
  const { musical_tradition } = await searchParams
  let albums: Awaited<ReturnType<typeof getAlbums>>['items'] = []

  try {
    const result = await getAlbums({ limit: 200 })
    albums = result.items
  } catch {
    // API not available
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Albums</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          Recordings that capture the living essence of musical traditions from across the world.
        </p>
      </div>

      {albums.length === 0 ? (
        <div className="text-center py-20">
          <div className="bg-[rgba(20,14,40,0.7)] rounded-2xl p-12 border border-[rgba(124,58,237,0.2)] inline-block">
            <p className="font-display text-xl text-[#c4b5fd] mb-2">No albums yet</p>
            <p className="text-sm text-[#a89fc4]">
              The discography is being assembled. Check back soon.
            </p>
          </div>
        </div>
      ) : (
        <AlbumsClient albums={albums} initialTradition={musical_tradition} />
      )}
    </div>
  )
}
