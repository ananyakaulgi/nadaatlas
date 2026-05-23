'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback } from 'react'
import Link from 'next/link'
import type { Track } from '@/lib/types'
import SearchInput from '@/components/ui/SearchInput'
import Badge from '@/components/ui/Badge'

interface Props {
  initialItems: Track[]
  total: number
  page: number
  limit: number
  initialTradition: string
  initialSearch: string
}

function formatDuration(seconds: number | null): string {
  if (!seconds) return ''
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${String(s).padStart(2, '0')}`
}

const CARD_STYLE = {
  background: 'rgba(20,14,40,0.65)',
  backdropFilter: 'blur(12px)',
  border: '1px solid rgba(124,58,237,0.18)',
} as const

export default function TracksClient({
  initialItems, total, page, limit,
  initialTradition, initialSearch,
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

  if (initialItems.length === 0 && total === 0 && !initialSearch && !initialTradition) {
    return (
      <div className="text-center py-24">
        <div
          className="inline-block rounded-2xl p-14 max-w-md mx-auto"
          style={{ background: 'rgba(20,14,40,0.7)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <p className="font-display text-3xl text-[#c4b5fd] mb-3">Coming soon</p>
          <p className="text-[#a89fc4] leading-relaxed">
            Track recordings will be added here — raga performances, jazz sessions,
            flamenco recitals, qawwali, and more.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-2 text-xs text-[#6b5d8a]">
            {['Ravi Shankar', 'Nina Simone', 'Miles Davis', 'Nusrat Fateh Ali Khan', 'Paco de Lucía'].map((n) => (
              <span key={n} className="px-3 py-1 rounded-full" style={{ border: '1px solid rgba(124,58,237,0.2)' }}>
                {n}
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
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <SearchInput
          value={initialSearch}
          onChange={(v) => push({ search: v })}
          placeholder="Search tracks…"
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
          <span className="text-[#c4b5fd] font-medium">{total.toLocaleString()}</span> tracks
          {initialTradition && ` · ${initialTradition}`}
          {initialSearch && ` matching "${initialSearch}"`}
        </p>
        {totalPages > 1 && (
          <p className="text-xs text-[#6b5d8a]">Page {page} of {totalPages}</p>
        )}
      </div>

      {/* List */}
      {initialItems.length > 0 ? (
        <div className="space-y-3 mb-10">
          {initialItems.map((t) => (
            <Link key={t.id} href={`/tracks/${t.id}`}>
              <div className="group flex items-center gap-4 rounded-2xl p-4 hover:scale-[1.003] transition-all duration-200" style={CARD_STYLE}>

                {/* Duration pill */}
                {t.duration_seconds && (
                  <span className="shrink-0 text-xs text-[#6b5d8a] font-mono w-10 text-right">
                    {formatDuration(t.duration_seconds)}
                  </span>
                )}

                {/* Main info */}
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-baseline gap-2 mb-1">
                    <h3 className="font-display text-base text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors truncate">
                      {t.title}
                    </h3>
                    {t.title_native && (
                      <span className="font-display text-sm text-[#a89fc4] italic">{t.title_native}</span>
                    )}
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    <Badge variant="gold">{t.artist.name}</Badge>
                    {t.musical_tradition && <Badge variant="lavender">{t.musical_tradition}</Badge>}
                    {t.raga && <Badge variant="teal">{t.raga}</Badge>}
                    {t.tala && <Badge variant="sage">{t.tala}</Badge>}
                    {t.maqam && <Badge variant="sage">{t.maqam}</Badge>}
                    {t.album && (
                      <Badge variant="sage">{t.album.title}</Badge>
                    )}
                  </div>
                </div>

                {/* External links */}
                <div className="shrink-0 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  {t.youtube_url && (
                    <a
                      href={t.youtube_url} target="_blank" rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="text-xs text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
                    >
                      ▶ YT
                    </a>
                  )}
                  {t.spotify_url && (
                    <a
                      href={t.spotify_url} target="_blank" rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="text-xs text-[#2dd4bf] hover:text-[#f5f0ff] transition-colors"
                    >
                      ♫ SP
                    </a>
                  )}
                  {!t.youtube_url && !t.spotify_url && (
                    <span className="text-[#f59e0b] text-sm">→</span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="font-display text-xl text-[#c4b5fd] mb-2">No tracks found</p>
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
