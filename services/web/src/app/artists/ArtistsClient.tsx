'use client'

import { useState, useMemo } from 'react'
import type { Artist } from '@/lib/types'
import ArtistCard from '@/components/cards/ArtistCard'
import SearchInput from '@/components/ui/SearchInput'
import Pagination from '@/components/ui/Pagination'

const PAGE_SIZE = 20

interface Props {
  artists: Artist[]
  initialTradition?: string
}

export default function ArtistsClient({ artists, initialTradition }: Props) {
  const [search, setSearch] = useState('')
  const [tradition, setTradition] = useState(initialTradition || '')
  const [page, setPage] = useState(1)

  const traditions = useMemo(() => {
    const set = new Set(artists.map((a) => a.musical_tradition).filter(Boolean) as string[])
    return Array.from(set).sort()
  }, [artists])

  const filtered = useMemo(() => {
    return artists.filter((a) => {
      const matchesSearch = !search || a.name.toLowerCase().includes(search.toLowerCase())
      const matchesTradition = !tradition || a.musical_tradition === tradition
      return matchesSearch && matchesTradition
    })
  }, [artists, search, tradition])

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE)
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  const handleSearch = (v: string) => { setSearch(v); setPage(1) }
  const handleTradition = (v: string) => { setTradition(v); setPage(1) }

  return (
    <div>
      <div className="flex flex-col sm:flex-row gap-3 mb-8">
        <SearchInput
          value={search}
          onChange={handleSearch}
          placeholder="Search artists..."
          className="flex-1"
        />
        <select
          value={tradition}
          onChange={(e) => handleTradition(e.target.value)}
          className="px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] focus:outline-none transition-all min-w-[180px]"
          style={{ background: 'rgba(20,14,40,0.7)', border: '1px solid rgba(124,58,237,0.25)', backdropFilter: 'blur(12px)' }}
        >
          <option value="">All traditions</option>
          {traditions.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
      </div>

      <p className="text-sm text-[#6b5d8a] mb-6">
        {filtered.length} {filtered.length === 1 ? 'artist' : 'artists'}
        {tradition ? ` in ${tradition}` : ''}
        {search ? ` matching "${search}"` : ''}
      </p>

      {paginated.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {paginated.map((a) => (
            <ArtistCard key={a.id} artist={a} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="font-display text-xl text-[#c4b5fd] mb-2">No artists found</p>
          <p className="text-sm text-[#a89fc4]">Try adjusting your search or filters</p>
        </div>
      )}

      <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
    </div>
  )
}
