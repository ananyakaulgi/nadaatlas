import type { Metadata } from 'next'
import Link from 'next/link'
import { Music2, Users, Disc3, Piano, Globe2, BookOpen, Search, ExternalLink } from 'lucide-react'

export const metadata: Metadata = {
  title: 'About',
  description: 'नाद Atla𝄞 is your complete encyclopedia for musical research — discover traditions, artists, albums, and instruments from every corner of the world.',
}

const PILLARS = [
  {
    icon: Music2,
    title: 'Traditions',
    description: 'Every musical tradition has a story — a geography, a history, a set of rules it follows and rules it breaks. We document them all, from Hindustani classical to Gnawa trance to Appalachian bluegrass.',
    color: 'text-[#c4b5fd]',
    glow: 'rgba(124,58,237,0.2)',
    border: 'rgba(124,58,237,0.25)',
  },
  {
    icon: Users,
    title: 'Artists',
    description: 'The masters, the innovators, the custodians of sound. We profile musicians across every tradition — their lineage, their instruments, their recordings, and their place in the larger story of world music.',
    color: 'text-[#a78bfa]',
    glow: 'rgba(147,51,234,0.18)',
    border: 'rgba(147,51,234,0.22)',
  },
  {
    icon: Disc3,
    title: 'Albums & Recordings',
    description: 'Music lives in recordings. We catalogue albums, live performances, and archival recordings — linking you to where you can listen, always respecting the original source.',
    color: 'text-[#fbbf24]',
    glow: 'rgba(245,158,11,0.18)',
    border: 'rgba(245,158,11,0.22)',
  },
  {
    icon: Piano,
    title: 'Instruments',
    description: 'Wood, string, skin, breath, metal, stone. Over 400 instruments catalogued with their Hornbostel-Sachs classification, regional origins, native names, and the traditions they belong to.',
    color: 'text-[#f59e0b]',
    glow: 'rgba(217,119,6,0.18)',
    border: 'rgba(217,119,6,0.22)',
  },
]

const SOURCES = [
  { name: 'MusicBrainz', description: 'Open music encyclopedia for artist and discography data', href: 'https://musicbrainz.org' },
  { name: 'Wikidata', description: 'Structured knowledge base for instruments and cultural context', href: 'https://wikidata.org' },
  { name: 'Wikipedia', description: 'Biographical and historical information', href: 'https://wikipedia.org' },
  { name: 'Spotify', description: 'Audio previews and artist imagery, where available', href: 'https://spotify.com' },
]

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">

      {/* ── Hero ── */}
      <div className="mb-20 text-center">
        <div className="mb-4">
          <span className="inline-block text-[#f59e0b] text-xs font-medium tracking-[0.25em] uppercase opacity-70">
            𝄞 &nbsp; What is नाद Atla𝄞? &nbsp; 𝄞
          </span>
        </div>
        <h1 className="font-display text-6xl sm:text-7xl text-[#f5f0ff] mb-4 leading-none">
          <span className="text-[#f59e0b]">नाद</span> Atla𝄞
        </h1>
        <p className="text-[#a89fc4] text-sm tracking-[0.15em] uppercase mb-10">Nāda Atlas</p>
        <p className="font-display text-2xl sm:text-3xl text-[#c4b5fd] italic font-light leading-relaxed max-w-3xl mx-auto mb-6">
          Your complete encyclopedia for musical research and information.
        </p>
        <p className="text-[#a89fc4] text-lg leading-relaxed max-w-2xl mx-auto">
          नाद <span className="text-[#f5f0ff]/60 text-sm">(Nāda)</span> is the Sanskrit and Hindi word for sound —
          the primordial vibration from which all music flows. An Atlas maps the world.
          Together, नाद Atla𝄞 maps the world of sound.
        </p>
      </div>

      {/* ── Mission ── */}
      <div
        className="rounded-2xl p-10 mb-16"
        style={{
          background: 'rgba(20,14,40,0.7)',
          border: '1px solid rgba(124,58,237,0.2)',
          backdropFilter: 'blur(12px)',
        }}
      >
        <div className="flex items-center gap-3 mb-5">
          <BookOpen className="w-5 h-5 text-[#c4b5fd]" />
          <h2 className="font-display text-2xl text-[#f5f0ff]">Our Mission</h2>
        </div>
        <div className="space-y-4 text-[#a89fc4] leading-relaxed text-lg">
          <p>
            The world&apos;s musical heritage is vast, diverse, and largely undiscovered by most listeners.
            A raga from Varanasi, a griot song from Mali, a gagaku ensemble from Kyoto —
            each carries centuries of culture, yet most of the world has never heard of them.
          </p>
          <p>
            नाद Atla𝄞 exists to change that. We are building the most comprehensive,
            carefully researched encyclopedia of world music — traditions, artists, instruments,
            and recordings — all in one place, free to explore.
          </p>
          <p>
            We don&apos;t host audio. We don&apos;t replace the original sources.
            We connect you to them, with the context to understand what you&apos;re hearing.
          </p>
        </div>
      </div>

      {/* ── What We Cover ── */}
      <div className="mb-16">
        <div className="flex items-center gap-3 mb-8">
          <Globe2 className="w-5 h-5 text-[#c4b5fd]" />
          <h2 className="font-display text-3xl text-[#f5f0ff]">What We Cover</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {PILLARS.map((pillar) => {
            const Icon = pillar.icon
            return (
              <div
                key={pillar.title}
                className="rounded-2xl p-7"
                style={{
                  background: 'rgba(20,14,40,0.6)',
                  border: `1px solid ${pillar.border}`,
                  boxShadow: `0 4px 20px ${pillar.glow}`,
                  backdropFilter: 'blur(10px)',
                }}
              >
                <div className="flex items-center gap-3 mb-3">
                  <Icon className={`w-5 h-5 ${pillar.color}`} />
                  <h3 className="font-display text-xl text-[#f5f0ff]">{pillar.title}</h3>
                </div>
                <p className="text-[#a89fc4] text-sm leading-relaxed">{pillar.description}</p>
              </div>
            )
          })}
        </div>
      </div>

      {/* ── How We Work ── */}
      <div
        className="rounded-2xl p-10 mb-16"
        style={{
          background: 'rgba(20,14,40,0.7)',
          border: '1px solid rgba(124,58,237,0.15)',
          backdropFilter: 'blur(12px)',
        }}
      >
        <div className="flex items-center gap-3 mb-5">
          <Search className="w-5 h-5 text-[#c4b5fd]" />
          <h2 className="font-display text-2xl text-[#f5f0ff]">How We Work</h2>
        </div>
        <p className="text-[#a89fc4] leading-relaxed text-lg mb-6">
          नाद Atla𝄞 aggregates data from trusted open sources, curated and cross-referenced
          by region, tradition, and instrument. Our data comes from:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {SOURCES.map((source) => (
            <a
              key={source.name}
              href={source.href}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-start gap-3 p-4 rounded-xl transition-all duration-200 hover:bg-[rgba(124,58,237,0.08)]"
              style={{ border: '1px solid rgba(124,58,237,0.12)' }}
            >
              <ExternalLink className="w-4 h-4 text-[#6b5d8a] group-hover:text-[#c4b5fd] transition-colors mt-0.5 shrink-0" />
              <div>
                <p className="text-[#f5f0ff] text-sm font-medium group-hover:text-[#c4b5fd] transition-colors">{source.name}</p>
                <p className="text-[#6b5d8a] text-xs leading-relaxed mt-0.5">{source.description}</p>
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* ── CTA ── */}
      <div className="text-center">
        <p className="font-display text-2xl text-[#c4b5fd] italic mb-8">
          Ready to explore?
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link
            href="/traditions"
            className="px-8 py-3.5 text-sm font-medium rounded-xl transition-all duration-300"
            style={{
              background: 'linear-gradient(135deg, #7c3aed, #6d28d9)',
              boxShadow: '0 0 20px rgba(124,58,237,0.4)',
              color: '#f5f0ff',
            }}
          >
            Browse Traditions
          </Link>
          <Link
            href="/instruments"
            className="px-8 py-3.5 text-[#c4b5fd] text-sm font-medium rounded-xl border border-[rgba(124,58,237,0.35)] hover:border-[rgba(124,58,237,0.6)] hover:bg-[rgba(124,58,237,0.1)] transition-all duration-300"
          >
            Explore Instruments
          </Link>
        </div>
      </div>

    </div>
  )
}
