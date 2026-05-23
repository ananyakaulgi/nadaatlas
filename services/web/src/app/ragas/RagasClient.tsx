'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback } from 'react'
import type { Raga } from '@/lib/types'
import RagaCard from '@/components/cards/RagaCard'
import SearchInput from '@/components/ui/SearchInput'

interface Props {
  initialItems: Raga[]
  total: number
  page: number
  limit: number
  thaats: string[]
  initialTradition: string
  initialThat: string
  initialSearch: string
}

const SELECT_STYLE = {
  background: 'rgba(20,14,40,0.7)',
  border: '1px solid rgba(124,58,237,0.25)',
  backdropFilter: 'blur(12px)',
} as const

export default function RagasClient({
  initialItems, total, page, limit,
  thaats, initialTradition, initialThat, initialSearch,
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

  // Tradition colour pills
  const TRADITIONS = [
    { value: '',            label: 'All' },
    { value: 'hindustani',  label: 'Hindustani' },
    { value: 'carnatic',    label: 'Carnatic' },
    { value: 'both',        label: 'Both' },
  ]

  return (
    <>
      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <SearchInput
          value={initialSearch}
          onChange={(v) => push({ search: v })}
          placeholder="Search ragas…"
          className="flex-1"
        />
        <select
          value={initialTradition}
          onChange={(e) => push({ tradition: e.target.value })}
          className="px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] focus:outline-none transition-all min-w-[160px]"
          style={SELECT_STYLE}
        >
          {TRADITIONS.map((t) => (
            <option key={t.value} value={t.value} style={{ background: '#130f25' }}>{t.label}</option>
          ))}
        </select>
        {(initialTradition === '' || initialTradition === 'hindustani') && (
          <select
            value={initialThat}
            onChange={(e) => push({ that: e.target.value })}
            className="px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] focus:outline-none transition-all min-w-[160px]"
            style={SELECT_STYLE}
          >
            <option value="" style={{ background: '#130f25' }}>All thaats</option>
            {thaats.map((t) => (
              <option key={t} value={t} style={{ background: '#130f25' }}>{t}</option>
            ))}
          </select>
        )}
      </div>

      {/* Stats bar */}
      <div className="flex items-center justify-between mb-8">
        <p className="text-sm text-[#6b5d8a]">
          <span className="text-[#c4b5fd] font-medium">{total.toLocaleString()}</span> ragas
          {initialTradition && ` · ${initialTradition}`}
          {initialThat && ` · ${initialThat} thaat`}
          {initialSearch && ` matching "${initialSearch}"`}
        </p>
        {totalPages > 1 && (
          <p className="text-xs text-[#6b5d8a]">Page {page} of {totalPages}</p>
        )}
      </div>

      {/* Grid */}
      {initialItems.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-10">
          {initialItems.map((r) => <RagaCard key={r.id} raga={r} />)}
        </div>
      ) : (
        <div className="text-center py-20">
          <p className="font-display text-xl text-[#c4b5fd] mb-2">No ragas found</p>
          <p className="text-sm text-[#a89fc4]">Try adjusting your filters</p>
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-4">
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
    </>
  )
}
