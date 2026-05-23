'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback } from 'react'
import type { Artist } from '@/lib/types'
import ArtistCard from '@/components/cards/ArtistCard'
import SearchInput from '@/components/ui/SearchInput'

interface Props {
  initialItems: Artist[]
  total: number
  page: number
  limit: number
  initialSearch: string
  initialTradition: string
}

export default function ArtistsClient({
  initialItems, total, page, limit,
  initialSearch, initialTradition,
}: Props) {
  const router   = useRouter()
  const pathname = usePathname()
  const sp       = useSearchParams()

  const push = useCallback((updates: Record<string, string>) => {
    const p = new URLSearchParams(sp.toString())
    Object.entries(updates).forEach(([k, v]) => v ? p.set(k, v) : p.delete(k))
    p.delete('page')
    router.push(`${pathname}?${p.toString()}`)
  }, [router, pathname, sp])

  const pushPage = useCallback((p: number) => {
    const params = new URLSearchParams(sp.toString())
    params.set('page', String(p))
    router.push(`${pathname}?${params.toString()}`)
  }, [router, pathname, sp])

  const totalPages = Math.ceil(total / limit)

  return (
    <div>
      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <SearchInput
          value={initialSearch}
          onChange={(v) => push({ search: v })}
          placeholder="Search artists…"
          className="flex-1"
        />
        <SearchInput
          value={initialTradition}
          onChange={(v) => push({ musical_tradition: v })}
          placeholder="Filter by tradition…"
          className="sm:w-64"
        />
      </div>

      {/* Stats */}
      <div className="flex items-center justify-between mb-8">
        <p className="text-sm text-[#6b5d8a]">
          <span className="text-[#c4b5fd] font-medium">{total.toLocaleString()}</span> artists
          {initialTradition && ` · ${initialTradition}`}
          {initialSearch && ` matching "${initialSearch}"`}
        </p>
        {totalPages > 1 && (
          <p className="text-xs text-[#6b5d8a]">Page {page} of {totalPages}</p>
        )}
      </div>

      {/* Grid */}
      {initialItems.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-10">
          {initialItems.map((a) => <ArtistCard key={a.id} artist={a} />)}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="font-display text-xl text-[#c4b5fd] mb-2">No artists found</p>
          <p className="text-sm text-[#a89fc4]">Try adjusting your search or filters</p>
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center gap-2">
          <button
            onClick={() => pushPage(page - 1)}
            disabled={page <= 1}
            className="px-4 py-2 rounded-xl text-sm text-[#a89fc4] disabled:opacity-30 hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.15)] transition-all"
            style={{ border: '1px solid rgba(124,58,237,0.2)' }}
          >
            ← Prev
          </button>
          <span className="px-4 py-2 text-sm text-[#6b5d8a]">{page} / {totalPages}</span>
          <button
            onClick={() => pushPage(page + 1)}
            disabled={page >= totalPages}
            className="px-4 py-2 rounded-xl text-sm text-[#a89fc4] disabled:opacity-30 hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.15)] transition-all"
            style={{ border: '1px solid rgba(124,58,237,0.2)' }}
          >
            Next →
          </button>
        </div>
      )}
    </div>
  )
}
