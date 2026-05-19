import Link from 'next/link'
import { Compass } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="mt-auto border-t border-[rgba(124,58,237,0.2)] bg-[#0d0a1a]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="text-center md:text-left">
            <div className="flex items-center gap-2 mb-1 justify-center md:justify-start">
              <Compass className="w-5 h-5 text-[#f59e0b] drop-shadow-[0_0_6px_rgba(245,158,11,0.5)]" />
              <p className="font-display text-xl text-[#f5f0ff]">MusiCompass</p>
            </div>
            <p className="text-sm text-[#a89fc4]">Navigate the world&apos;s musical traditions</p>
          </div>

          <nav className="flex flex-wrap justify-center gap-x-6 gap-y-2">
            {[
              { href: '/traditions', label: 'Traditions' },
              { href: '/artists', label: 'Artists' },
              { href: '/albums', label: 'Albums' },
              { href: '/instruments', label: 'Instruments' },
              { href: '/regions', label: 'Regions' },
              { href: '/genres', label: 'Genres' },
            ].map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm text-[#a89fc4] hover:text-[#c4b5fd] transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="mt-8 pt-6 border-t border-[rgba(124,58,237,0.15)] text-center">
          <p className="text-xs text-[#6b5d8a]">
            MusiCompass · Navigate the world&apos;s musical traditions
          </p>
        </div>
      </div>
    </footer>
  )
}
