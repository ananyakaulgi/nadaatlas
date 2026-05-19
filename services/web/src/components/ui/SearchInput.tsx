'use client'

import { Search } from 'lucide-react'

interface SearchInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  className?: string
}

export default function SearchInput({ value, onChange, placeholder = 'Search...', className }: SearchInputProps) {
  return (
    <div className={`relative ${className}`}>
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#7c3aed] w-4 h-4 pointer-events-none" />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-10 pr-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] placeholder:text-[#6b5d8a] focus:outline-none transition-all"
        style={{
          background: 'rgba(20, 14, 40, 0.7)',
          border: '1px solid rgba(124,58,237,0.25)',
          backdropFilter: 'blur(12px)',
        }}
        onFocus={(e) => {
          e.currentTarget.style.borderColor = 'rgba(124,58,237,0.6)'
          e.currentTarget.style.boxShadow = '0 0 0 3px rgba(124,58,237,0.1)'
        }}
        onBlur={(e) => {
          e.currentTarget.style.borderColor = 'rgba(124,58,237,0.25)'
          e.currentTarget.style.boxShadow = 'none'
        }}
      />
    </div>
  )
}
