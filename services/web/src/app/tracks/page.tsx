import { getTracks } from '@/lib/api'
import TracksClient from './TracksClient'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Tracks — नाद Atla𝄞',
  description: 'Recordings from across the world — sitar ragas, jazz standards, flamenco, qawwali, and more',
}

interface PageProps {
  searchParams: Promise<{
    musical_tradition?: string
    search?: string
    page?: string
  }>
}

export default async function TracksPage({ searchParams }: PageProps) {
  const params = await searchParams
  const page  = Number(params.page || 1)
  const limit = 40
  const skip  = (page - 1) * limit

  let result = { items: [], total: 0, skip: 0, limit }

  try {
    result = await getTracks({
      skip,
      limit,
      ...(params.musical_tradition && { musical_tradition: params.musical_tradition }),
      ...(params.search            && { search:            params.search }),
    })
  } catch (err) {
    console.error('[TracksPage] fetch failed:', err)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Tracks</h1>
        <p className="text-[#a89fc4] text-lg max-w-2xl">
          Recordings that capture music in the moment — from studio sessions to live
          concerts, spanning every tradition in the atlas.
        </p>
      </div>

      <TracksClient
        initialItems={result.items}
        total={result.total}
        page={page}
        limit={limit}
        initialTradition={params.musical_tradition || ''}
        initialSearch={params.search || ''}
      />
    </div>
  )
}
