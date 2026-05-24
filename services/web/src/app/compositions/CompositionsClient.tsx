'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback } from 'react'
import Link from 'next/link'
import type { Composition } from '@/lib/types'
import SearchInput from '@/components/ui/SearchInput'
import Badge from '@/components/ui/Badge'

interface Props {
  initialItems: Composition[]
  total: number
  page: number
  limit: number
  compositionTypes: string[]
  initialType: string
  initialSearch: string
}

const SELECT_STYLE = {
  background: 'rgba(20,14,40,0.7)',
  border: '1px solid rgba(124,58,237,0.25)',
  backdropFilter: 'blur(12px)',
} as const

export default function CompositionsClient({
  initialItems, total, page, limit,
  compositionTypes, initialType, initialSearch,
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

  if (initialItems.length === 0 && total === 0 && !initialSearch && !initialType) {
    return (
      <div className="text-center py-24">
        <div
          className="inline-block rounded-2xl p-14 max-w-md mx-auto"
          style={{ background: 'rgba(20,14,40,0.7)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <p className="font-display text-3xl text-[#c4b5fd] mb-3">Coming soon</p>
          <p className="text-[#a89fc4] leading-relaxed">
            Compositions will be seeded here — kritis by the Carnatic Trinity,
            dhrupad compositions from the Tansen tradition, and beyond.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-2 text-xs text-[#6b5d8a]">
            {['Kriti', 'Dhrupad', 'Khayal', 'Ghazal', 'Varnam', 'Thumri'].map((t) => (
              <span
                key={t}
                className="px-3 py-1 rounded-full"
                style={{ border: '1px solid rgba(124,58,237,0.2)' }}
              >
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <>
      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6 min-w-0">
        <SearchInput
          value={initialSearch}
          onChange={(v) => push({ search: v })}
          placeholder="Search compositions…"
          className="flex-1"
        />
        <select
          value={initialType}
          onChange={(e) => push({ composition_type: e.target.value })}
          className="px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] focus:outline-none min-w-[180px] shrink-0 capitalize"
          style={SELECT_STYLE}
        >
          <option value="" style={{ background: '#130f25' }}>All types</option>
          {compositionTypes.map((t) => (
            <option key={t} value={t} style={{ background: '#130f25' }} className="capitalize">{t}</option>
          ))}
        </select>
      </div>

      {/* Stats */}
      <div className="flex items-center justify-between mb-8">
        <p className="text-sm text-[#6b5d8a]">
          <span className="text-[#c4b5fd] font-medium">{total.toLocaleString()}</span> compositions
          {initialType && ` · ${initialType}`}
          {initialSearch && ` matching "${initialSearch}"`}
        </p>
        {totalPages > 1 && (
          <p className="text-xs text-[#6b5d8a]">Page {page} of {totalPages}</p>
        )}
      </div>

      {/* List */}
      {initialItems.length > 0 ? (
        <div className="space-y-3 mb-10">
          {initialItems.map((c) => (
            <Link key={c.id} href={`/compositions/${c.id}`}>
              <div
                className="group flex items-start gap-5 rounded-2xl p-5 hover:scale-[1.005] transition-all duration-200"
                style={{
                  background: 'rgba(20,14,40,0.65)',
                  backdropFilter: 'blur(12px)',
                  border: '1px solid rgba(124,58,237,0.18)',
                }}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-baseline gap-2 mb-1">
                    <h3 className="font-display text-lg text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors">
                      {c.title}
                    </h3>
                    {c.title_native && (
                      <span className="font-display text-sm text-[#a89fc4] italic">{c.title_native}</span>
                    )}
                  </div>

                  <div className="flex flex-wrap gap-1.5 mt-1.5">
                    {c.composer && (
                      <Badge variant="gold">{c.composer.name}</Badge>
                    )}
                    {c.composition_type && (
                      <Badge variant="lavender" className="capitalize">{c.composition_type}</Badge>
                    )}
                    {c.raga && (
                      <Badge variant="teal">{c.raga.name}</Badge>
                    )}
                    {c.tala && (
                      <Badge variant="sage">{c.tala.name}</Badge>
                    )}
                    {c.language && (
                      <Badge variant="sage">{c.language}</Badge>
                    )}
                    {c.year_composed && (
                      <Badge variant="sage">{c.year_composed}</Badge>
                    )}
                  </div>

                  {c.description && (
                    <p className="text-sm text-[#a89fc4] mt-2 line-clamp-1">{c.description}</p>
                  )}
                </div>

                <span className="text-[#f59e0b] text-sm opacity-0 group-hover:opacity-100 transition-opacity shrink-0 mt-1">→</span>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="font-display text-xl text-[#c4b5fd] mb-2">No compositions found</p>
          <p className="text-sm text-[#a89fc4]">Try adjusting your filters</p>
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
    </>
  )
}
