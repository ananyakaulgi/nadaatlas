'use client'

import { ChevronLeft, ChevronRight } from 'lucide-react'
import clsx from 'clsx'

interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
}

export default function Pagination({ currentPage, totalPages, onPageChange }: PaginationProps) {
  if (totalPages <= 1) return null

  const pages = Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
    if (totalPages <= 7) return i + 1
    if (currentPage <= 4) return i + 1
    if (currentPage >= totalPages - 3) return totalPages - 6 + i
    return currentPage - 3 + i
  })

  return (
    <div className="flex items-center justify-center gap-1 mt-10">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 rounded-lg text-[#a89fc4] hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.15)] disabled:opacity-30 disabled:cursor-not-allowed transition-all"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>

      {pages.map((page) => (
        <button
          key={page}
          onClick={() => onPageChange(page)}
          className={clsx(
            'w-9 h-9 rounded-lg text-sm font-medium transition-all',
            page === currentPage
              ? 'text-[#f5f0ff]'
              : 'text-[#a89fc4] hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.15)]'
          )}
          style={page === currentPage ? {
            background: 'linear-gradient(135deg, #7c3aed, #6d28d9)',
            boxShadow: '0 0 12px rgba(124,58,237,0.4)',
          } : undefined}
        >
          {page}
        </button>
      ))}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 rounded-lg text-[#a89fc4] hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.15)] disabled:opacity-30 disabled:cursor-not-allowed transition-all"
      >
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  )
}
