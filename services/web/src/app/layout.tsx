import type { Metadata } from 'next'
import '@fontsource/cormorant-garamond/400.css'
import '@fontsource/cormorant-garamond/400-italic.css'
import '@fontsource/cormorant-garamond/600.css'
import '@fontsource/inter/400.css'
import '@fontsource/inter/500.css'
import './globals.css'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import CosmicCompass from '@/components/ui/CosmicCompass'

export const metadata: Metadata = {
  title: {
    default: 'नाद Atla𝄞 — Your Complete Encyclopedia for Musical Research',
    template: '%s · नाद Atla𝄞',
  },
  description: 'नाद Atla𝄞 (Nāda Atlas) — your complete encyclopedia for musical research and information. Explore traditions, artists, albums, and instruments from across the globe.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col bg-[#08060f] text-[#f5f0ff] antialiased">

        {/* ── Cosmic compass — fixed, floats behind every page ── */}
        <div
          className="fixed inset-0 flex items-center justify-center pointer-events-none z-0"
          aria-hidden="true"
        >
          <CosmicCompass className="w-[min(720px,92vw)] h-[min(720px,92vw)] opacity-[0.28]" />
        </div>

        {/* All foreground content sits above the compass */}
        <div className="relative z-10 flex flex-col min-h-full">
          <Header />
          <main className="flex-1">
            {children}
          </main>
          <Footer />
        </div>

      </body>
    </html>
  )
}
