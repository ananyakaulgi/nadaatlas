'use client'

import { Search, X } from 'lucide-react'
import { useState, useEffect, useRef } from 'react'

interface SearchInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  className?: string
  debounceMs?: number
}

export default function SearchInput({
  value,
  onChange,
  placeholder = 'Search...',
  className = '',
  debounceMs = 350,
}: SearchInputProps) {
  // Local state so the input stays responsive while typing;
  // the debounced version is what triggers the URL/fetch update.
  const [local, setLocal] = useState(value)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  // Keep local in sync if the parent resets value (e.g. page navigation)
  useEffect(() => {
    setLocal(value)
  }, [value])

  function handleChange(raw: string) {
    setLocal(raw)
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => onChange(raw), debounceMs)
  }

  function handleClear() {
    setLocal('')
    if (timerRef.current) clearTimeout(timerRef.current)
    onChange('')
  }

  // Clean up on unmount
  useEffect(() => () => { if (timerRef.current) clearTimeout(timerRef.current) }, [])

  return (
    <div className={`relative min-w-0 ${className}`}>
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#7c3aed] w-4 h-4 pointer-events-none z-10" />
      <input
        type="text"
        value={local}
        onChange={(e) => handleChange(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-10 pr-8 py-2.5 rounded-xl text-sm text-[#f5f0ff] placeholder:text-[#6b5d8a] focus:outline-none"
        style={{
          background: 'rgba(20, 14, 40, 0.7)',
          border: '1px solid rgba(124,58,237,0.25)',
          backdropFilter: 'blur(12px)',
          boxSizing: 'border-box',
          transition: 'border-color 150ms ease, box-shadow 150ms ease',
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
      {/* Clear button — only shown when there's text */}
      {local && (
        <button
          type="button"
          onClick={handleClear}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-[#6b5d8a] hover:text-[#a89fc4] transition-colors"
          aria-label="Clear search"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  )
}
