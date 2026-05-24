'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState, useRef, useEffect } from 'react'
import { Menu, X, ChevronDown } from 'lucide-react'
import clsx from 'clsx'

const PRIMARY_NAV = [
  { href: '/traditions',   label: 'Traditions' },
  { href: '/ragas',        label: 'Ragas' },
  { href: '/talas',        label: 'Talas' },
  { href: '/composers',    label: 'Composers' },
  { href: '/compositions', label: 'Compositions' },
  { href: '/tracks',       label: 'Tracks' },
  { href: '/artists',      label: 'Artists' },
  { href: '/about',        label: 'About' },
]

const MORE_NAV = [
  { href: '/instruments', label: 'Instruments' },
  { href: '/genres',      label: 'Genres' },
  { href: '/regions',     label: 'Regions' },
  { href: '/feedback',    label: 'Feedback' },
]

const ALL_NAV = [...PRIMARY_NAV, ...MORE_NAV]

export default function Header() {
  const pathname   = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [moreOpen,   setMoreOpen]   = useState(false)
  const moreRef = useRef<HTMLDivElement>(null)

  // Close "More" dropdown on outside click
  useEffect(() => {
    function handle(e: MouseEvent) {
      if (moreRef.current && !moreRef.current.contains(e.target as Node)) {
        setMoreOpen(false)
      }
    }
    document.addEventListener('mousedown', handle)
    return () => document.removeEventListener('mousedown', handle)
  }, [])

  const moreActive = MORE_NAV.some((l) => pathname.startsWith(l.href))

  return (
    <header className="sticky top-0 z-50 bg-[#08060f]/80 backdrop-blur-md border-b border-[rgba(124,58,237,0.2)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">

          {/* Logo */}
          <Link href="/" className="group flex items-center gap-1 shrink-0">
            <span className="font-display text-2xl tracking-wide leading-none">
              <span className="text-[#f59e0b] group-hover:text-[#fbbf24] transition-colors drop-shadow-[0_0_8px_rgba(245,158,11,0.5)]">♪ नाद</span>
              <span className="text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors"> Atla𝄞</span>
            </span>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-0.5">
            {PRIMARY_NAV.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={clsx(
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 whitespace-nowrap',
                  pathname.startsWith(link.href)
                    ? 'bg-[rgba(124,58,237,0.2)] text-[#c4b5fd] border border-[rgba(124,58,237,0.3)]'
                    : 'text-[#a89fc4] hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.1)]'
                )}
              >
                {link.label}
              </Link>
            ))}

            {/* More dropdown */}
            <div ref={moreRef} className="relative">
              <button
                onClick={() => setMoreOpen((o) => !o)}
                className={clsx(
                  'flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200',
                  moreActive
                    ? 'bg-[rgba(124,58,237,0.2)] text-[#c4b5fd] border border-[rgba(124,58,237,0.3)]'
                    : 'text-[#a89fc4] hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.1)]'
                )}
              >
                More
                <ChevronDown className={clsx('w-3.5 h-3.5 transition-transform duration-200', moreOpen && 'rotate-180')} />
              </button>

              {moreOpen && (
                <div
                  className="absolute right-0 top-full mt-2 w-44 rounded-xl py-1.5 z-50"
                  style={{
                    background: 'rgba(13,10,26,0.97)',
                    border: '1px solid rgba(124,58,237,0.25)',
                    backdropFilter: 'blur(16px)',
                    boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
                  }}
                >
                  {MORE_NAV.map((link) => (
                    <Link
                      key={link.href}
                      href={link.href}
                      onClick={() => setMoreOpen(false)}
                      className={clsx(
                        'block px-4 py-2 text-sm font-medium transition-colors',
                        pathname.startsWith(link.href)
                          ? 'text-[#c4b5fd] bg-[rgba(124,58,237,0.15)]'
                          : 'text-[#a89fc4] hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.08)]'
                      )}
                    >
                      {link.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </nav>

          {/* Mobile hamburger */}
          <button
            className="md:hidden p-2 rounded-lg text-[#a89fc4] hover:bg-[rgba(124,58,237,0.15)] transition-colors"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu — all links */}
      {mobileOpen && (
        <div className="md:hidden border-t border-[rgba(124,58,237,0.2)] bg-[#0d0a1a]/95 backdrop-blur-md px-4 py-3 space-y-1">
          {ALL_NAV.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className={clsx(
                'block px-4 py-2.5 rounded-lg text-sm font-medium transition-all',
                pathname.startsWith(link.href)
                  ? 'bg-[rgba(124,58,237,0.2)] text-[#c4b5fd]'
                  : 'text-[#a89fc4] hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.1)]'
              )}
            >
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </header>
  )
}
