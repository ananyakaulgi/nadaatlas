'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import clsx from 'clsx'

const NAV_LINKS = [
  { href: '/traditions', label: 'Traditions' },
  { href: '/artists', label: 'Artists' },
  { href: '/albums', label: 'Albums' },
  { href: '/instruments', label: 'Instruments' },
  { href: '/regions', label: 'Regions' },
]

export default function Header() {
  const pathname = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 bg-[#08060f]/80 backdrop-blur-md border-b border-[rgba(124,58,237,0.2)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="group flex items-center gap-1">
            <span className="font-display text-2xl tracking-wide leading-none">
              <span className="text-[#f59e0b] group-hover:text-[#fbbf24] transition-colors drop-shadow-[0_0_8px_rgba(245,158,11,0.5)]">♪ नाद</span>
              <span className="text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors"> Atla𝄞</span>
            </span>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={clsx(
                  'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                  pathname.startsWith(link.href)
                    ? 'bg-[rgba(124,58,237,0.2)] text-[#c4b5fd] border border-[rgba(124,58,237,0.3)]'
                    : 'text-[#a89fc4] hover:text-[#f5f0ff] hover:bg-[rgba(124,58,237,0.1)]'
                )}
              >
                {link.label}
              </Link>
            ))}
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

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-[rgba(124,58,237,0.2)] bg-[#0d0a1a]/95 backdrop-blur-md px-4 py-3 space-y-1">
          {NAV_LINKS.map((link) => (
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
