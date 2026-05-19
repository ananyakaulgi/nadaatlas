'use client'

import { useState, useMemo } from 'react'
import type { Tradition } from '@/lib/types'
import TraditionCard from '@/components/cards/TraditionCard'
import SearchInput from '@/components/ui/SearchInput'
import Pagination from '@/components/ui/Pagination'

const PAGE_SIZE = 20

interface Props {
  traditions: Tradition[]
  initialRegion?: string
}

export default function TraditionsClient({ traditions, initialRegion }: Props) {
  const [search, setSearch] = useState('')
  const [region, setRegion] = useState(initialRegion || '')
  const [page, setPage] = useState(1)

  const regions = useMemo(() => {
    const set = new Set(traditions.map((t) => t.region).filter(Boolean))
    return Array.from(set).sort()
  }, [traditions])

  const filtered = useMemo(() => {
    return traditions.filter((t) => {
      const matchesSearch = !search || t.name.toLowerCase().includes(search.toLowerCase())
      const matchesRegion = !region || t.region === region
      return matchesSearch && matchesRegion
    })
  }, [traditions, search, region])

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE)
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  const handleSearch = (v: string) => { setSearch(v); setPage(1) }
  const handleRegion = (v: string) => { setRegion(v); setPage(1) }

  return (
    <div>
      {/* Filter bar */}
      <div className="flex flex-col sm:flex-row gap-3 mb-8">
        <SearchInput
          value={search}
          onChange={handleSearch}
          placeholder="Search traditions..."
          className="flex-1"
        />
        <select
          value={region}
          onChange={(e) => handleRegion(e.target.value)}
          className="px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] focus:outline-none transition-all min-w-[160px]"
          style={{
            background: 'rgba(20,14,40,0.7)',
            border: '1px solid rgba(124,58,237,0.25)',
            backdropFilter: 'blur(12px)',
          }}
        >
          <option value="" style={{ background: '#130f25' }}>All regions</option>
          {regions.map((r) => (
            <option key={r} value={r} style={{ background: '#130f25' }}>{r}</option>
          ))}
        </select>
      </div>

      {/* Count */}
      <p className="text-sm text-[#6b5d8a] mb-6">
        {filtered.length} {filtered.length === 1 ? 'tradition' : 'traditions'}
        {region ? ` in ${region}` : ''}
        {search ? ` matching "${search}"` : ''}
      </p>

      {/* Grid */}
      {paginated.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {paginated.map((t) => (
            <TraditionCard key={t.id} tradition={t} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="font-display text-xl text-[#c4b5fd] mb-2">No traditions found</p>
          <p className="text-sm text-[#a89fc4]">Try adjusting your search or filters</p>
        </div>
      )}

      <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
    </div>
  )
}
