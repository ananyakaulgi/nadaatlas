'use client'

import { useState, useMemo } from 'react'
import type { Instrument } from '@/lib/types'
import InstrumentCard from '@/components/cards/InstrumentCard'
import SearchInput from '@/components/ui/SearchInput'
import Pagination from '@/components/ui/Pagination'

const PAGE_SIZE = 20

export default function InstrumentsClient({ instruments }: { instruments: Instrument[] }) {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [page, setPage] = useState(1)

  const categories = useMemo(() => {
    const set = new Set(instruments.map((i) => i.hs_category).filter(Boolean) as string[])
    return Array.from(set).sort()
  }, [instruments])

  const filtered = useMemo(() => {
    return instruments.filter((i) => {
      const matchesSearch = !search || i.name.toLowerCase().includes(search.toLowerCase())
      const matchesCategory = !category || i.hs_category === category
      return matchesSearch && matchesCategory
    })
  }, [instruments, search, category])

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE)
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  const handleSearch = (v: string) => { setSearch(v); setPage(1) }
  const handleCategory = (v: string) => { setCategory(v); setPage(1) }

  return (
    <div>
      <div className="flex flex-col sm:flex-row gap-3 mb-8">
        <SearchInput
          value={search}
          onChange={handleSearch}
          placeholder="Search instruments..."
          className="flex-1"
        />
        <select
          value={category}
          onChange={(e) => handleCategory(e.target.value)}
          className="px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] focus:outline-none transition-all min-w-[180px]"
          style={{ background: 'rgba(20,14,40,0.7)', border: '1px solid rgba(124,58,237,0.25)', backdropFilter: 'blur(12px)' }}
        >
          <option value="">All categories</option>
          {categories.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      <p className="text-sm text-[#6b5d8a] mb-6">
        {filtered.length} {filtered.length === 1 ? 'instrument' : 'instruments'}
        {category ? ` in ${category}` : ''}
        {search ? ` matching "${search}"` : ''}
      </p>

      {paginated.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {paginated.map((i) => (
            <InstrumentCard key={i.id} instrument={i} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="font-display text-xl text-[#c4b5fd] mb-2">No instruments found</p>
          <p className="text-sm text-[#a89fc4]">Try adjusting your search or filters</p>
        </div>
      )}

      <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
    </div>
  )
}
