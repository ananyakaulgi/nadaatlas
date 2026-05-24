import type { Metadata } from 'next'
import Link from 'next/link'
import {
  Database, ShieldCheck, AlertTriangle, Globe2,
  BookOpen, ExternalLink, MessageSquare, Layers,
} from 'lucide-react'

export const metadata: Metadata = {
  title: 'Methodology — नाद Atla𝄞',
  description: 'How we source, verify, and curate data — and where the atlas still has gaps.',
}

// ─── Data ─────────────────────────────────────────────────────────────────────

const SOURCES = [
  {
    name: 'Wikipedia / Wikidata',
    role: 'Biographical data, historical context, instrument classification, Wikipedia slugs for deep-links',
    reliability: 'Cross-referenced against primary sources where possible',
    href: 'https://www.wikidata.org',
  },
  {
    name: 'MusicBrainz',
    role: 'Artist discographies, album metadata, track listings, recording relationships',
    reliability: 'Community-maintained; reviewed for quality before import',
    href: 'https://musicbrainz.org',
  },
  {
    name: 'Smithsonian Institution',
    role: 'Instrument images (Smithsonian Open Access), ethnomusicological reference data',
    reliability: 'Primary institutional source — high confidence',
    href: 'https://www.si.edu/openaccess',
  },
  {
    name: 'Internet Archive',
    role: 'Public-domain audio recordings, historical performance documentation',
    reliability: 'Source quality varies; items are vetted before surfacing',
    href: 'https://archive.org/details/audio',
  },
  {
    name: 'Editorial research',
    role: 'Composer biographies, tradition histories, raga/tala descriptors, Native American and underrepresented traditions',
    reliability: 'Written or reviewed by human editors; subject to ongoing correction',
    href: null,
  },
]

type CoverageLevel = 'strong' | 'moderate' | 'sparse' | 'planned'

const COVERAGE: { region: string; traditions: string; level: CoverageLevel; note?: string }[] = [
  { region: 'South Asia',          traditions: 'Hindustani, Carnatic, Qawwali, Bhajan',          level: 'strong'   },
  { region: 'Western Europe',      traditions: 'Western Classical, Opera, Flamenco, Celtic',      level: 'strong'   },
  { region: 'North Africa / Levant', traditions: 'Maqam (Arabic), Egyptian, Andalusian',          level: 'moderate' },
  { region: 'West Africa',         traditions: 'Griot, Afrobeat, Highlife, Mbalax',               level: 'moderate' },
  { region: 'North America (Western)', traditions: 'Jazz, Blues, Bluegrass, Country',             level: 'moderate' },
  { region: 'East Asia',           traditions: 'Chinese Classical, Gagaku, Korean Jeongan',       level: 'sparse',  note: 'Expanding in v2' },
  { region: 'Southeast Asia',      traditions: 'Gamelan, Khmer, Thai Classical',                  level: 'sparse',  note: 'Expanding in v2' },
  { region: 'Central Asia / Iran', traditions: 'Persian Classical, Mugham, Uyghur Muqam',        level: 'sparse'   },
  { region: 'Latin America',       traditions: 'Tango, Samba, Cumbia, Son Cubano',                level: 'sparse'   },
  { region: 'North America (Indigenous)', traditions: 'Plains, Pueblo, Pacific Northwest, Haudenosaunee', level: 'planned', note: 'Active data work in progress' },
  { region: 'Eastern Europe',      traditions: 'Klezmer, Balkan, Roma, Byzantine',                level: 'sparse'   },
  { region: 'Oceania',             traditions: 'Aboriginal Australian, Māori, Pacific Islands',   level: 'planned', note: 'Planned for v3' },
]

const LEVEL_META: Record<CoverageLevel, { label: string; color: string; bg: string; bar: string; width: string }> = {
  strong:   { label: 'Strong',   color: '#34d399', bg: 'rgba(52,211,153,0.12)',  bar: '#34d399', width: '85%'  },
  moderate: { label: 'Moderate', color: '#60a5fa', bg: 'rgba(96,165,250,0.12)',  bar: '#60a5fa', width: '50%'  },
  sparse:   { label: 'Sparse',   color: '#f59e0b', bg: 'rgba(245,158,11,0.12)',  bar: '#f59e0b', width: '20%'  },
  planned:  { label: 'Planned',  color: '#a78bfa', bg: 'rgba(167,139,250,0.12)', bar: '#a78bfa', width: '5%'   },
}

const QUALITY_TIERS = [
  {
    icon: '✦',
    label: 'Verified',
    color: '#f59e0b',
    border: 'rgba(245,158,11,0.3)',
    bg: 'rgba(245,158,11,0.08)',
    description:
      'Entries marked ✦ have been cross-referenced against at least two independent sources. Biographical dates, works, and claims have been checked. These are the most reliable records in the atlas.',
  },
  {
    icon: '●',
    label: 'Reviewed',
    color: '#60a5fa',
    border: 'rgba(96,165,250,0.25)',
    bg: 'rgba(96,165,250,0.06)',
    description:
      'Editorial entries written or reviewed by a human editor from a single reliable source. Accurate to the best of our knowledge but not independently cross-referenced.',
  },
  {
    icon: '○',
    label: 'Imported',
    color: '#6b5d8a',
    border: 'rgba(107,93,138,0.25)',
    bg: 'rgba(107,93,138,0.06)',
    description:
      'Records imported from open databases (MusicBrainz, Wikidata) and not yet human-reviewed. May contain errors, gaps, or outdated information. We flag these and work through them over time.',
  },
]

const KNOWN_GAPS = [
  {
    title: 'Native & Indigenous American music',
    detail: 'The atlas launched with almost no coverage of Indigenous North American traditions — a significant omission we are actively correcting. Plains vocal traditions, Pueblo ceremonial music, Pacific Northwest song systems, and Haudenosaunee music are all being researched and seeded now.',
    status: 'In progress',
    statusColor: '#60a5fa',
  },
  {
    title: 'East and Southeast Asian classical traditions',
    detail: 'Chinese classical (qin, pipa), Gagaku, and Gamelan traditions are present but thin. We have the data model; we need more editorial work to fill them out accurately.',
    status: 'Planned v2',
    statusColor: '#a78bfa',
  },
  {
    title: 'Oral and non-notated traditions',
    detail: 'Many of the world\'s richest musical traditions have no written notation and are transmitted entirely through apprenticeship. Documenting these accurately without reducing them to Western frameworks is an ongoing methodological challenge.',
    status: 'Ongoing',
    statusColor: '#f59e0b',
  },
  {
    title: 'Living artists vs. historical figures',
    detail: 'We currently skew toward well-documented historical figures. Living artists — especially from underrepresented regions — are harder to verify accurately. We add them carefully.',
    status: 'Ongoing',
    statusColor: '#f59e0b',
  },
  {
    title: 'Audio and recordings',
    detail: 'We link to YouTube, Spotify, and public-domain Archive.org recordings where we have them. For many traditions and older recordings this data is missing or incomplete.',
    status: 'In progress',
    statusColor: '#60a5fa',
  },
]

// ─── Shared styles ─────────────────────────────────────────────────────────────

const CARD = {
  background: 'rgba(20,14,40,0.7)',
  border: '1px solid rgba(124,58,237,0.2)',
  backdropFilter: 'blur(12px)',
} as const

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function MethodologyPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">

      {/* ── Hero ── */}
      <div className="mb-16">
        <span className="inline-block text-[#f59e0b] text-xs font-medium tracking-[0.25em] uppercase opacity-70 mb-4">
          How the atlas is built
        </span>
        <h1 className="font-display text-5xl sm:text-6xl text-[#f5f0ff] mb-5 leading-tight">Methodology</h1>
        <p className="text-[#a89fc4] text-xl leading-relaxed max-w-3xl">
          An atlas is only as good as its sources. This page explains where our data comes from,
          how we decide what to include, how we grade confidence, and — just as importantly —
          where the map is still incomplete.
        </p>
      </div>

      {/* ── Data Sources ── */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-8">
          <Database className="w-5 h-5 text-[#c4b5fd]" />
          <h2 className="font-display text-3xl text-[#f5f0ff]">Data Sources</h2>
        </div>
        <div className="space-y-3">
          {SOURCES.map((source) => (
            <div key={source.name} className="rounded-2xl p-6" style={CARD}>
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-medium text-[#f5f0ff]">{source.name}</h3>
                    {source.href && (
                      <a href={source.href} target="_blank" rel="noopener noreferrer"
                        className="text-[#6b5d8a] hover:text-[#c4b5fd] transition-colors">
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>
                  <p className="text-sm text-[#a89fc4] leading-relaxed mb-2">{source.role}</p>
                  <p className="text-xs text-[#6b5d8a] italic">{source.reliability}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Quality Tiers ── */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-8">
          <ShieldCheck className="w-5 h-5 text-[#c4b5fd]" />
          <h2 className="font-display text-3xl text-[#f5f0ff]">Data Quality Tiers</h2>
        </div>
        <p className="text-[#a89fc4] leading-relaxed mb-6">
          Not all records are equally reliable. We use a three-tier system to be transparent
          about confidence levels.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {QUALITY_TIERS.map((tier) => (
            <div key={tier.label} className="rounded-2xl p-6" style={{ background: tier.bg, border: `1px solid ${tier.border}`, backdropFilter: 'blur(12px)' }}>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-lg" style={{ color: tier.color }}>{tier.icon}</span>
                <span className="font-display text-lg text-[#f5f0ff]">{tier.label}</span>
              </div>
              <p className="text-sm text-[#a89fc4] leading-relaxed">{tier.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Coverage ── */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-8">
          <Globe2 className="w-5 h-5 text-[#c4b5fd]" />
          <h2 className="font-display text-3xl text-[#f5f0ff]">Coverage by Region</h2>
        </div>
        <p className="text-[#a89fc4] leading-relaxed mb-6">
          The atlas does not cover all traditions equally — and we would rather be honest about
          that than pretend otherwise. Here is where we stand today.
        </p>

        {/* Legend */}
        <div className="flex flex-wrap gap-4 mb-6">
          {(Object.entries(LEVEL_META) as [CoverageLevel, typeof LEVEL_META[CoverageLevel]][]).map(([key, m]) => (
            <div key={key} className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ background: m.color }} />
              <span className="text-xs text-[#a89fc4]">{m.label}</span>
            </div>
          ))}
        </div>

        <div className="space-y-3">
          {COVERAGE.map((row) => {
            const m = LEVEL_META[row.level]
            return (
              <div key={row.region} className="rounded-2xl p-5" style={{ background: m.bg, border: `1px solid ${m.color}25`, backdropFilter: 'blur(12px)' }}>
                <div className="flex items-start justify-between gap-4 mb-2 flex-wrap">
                  <div>
                    <span className="text-sm font-medium text-[#f5f0ff]">{row.region}</span>
                    <span className="text-xs text-[#6b5d8a] ml-2">{row.traditions}</span>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    {row.note && (
                      <span className="text-xs italic text-[#6b5d8a]">{row.note}</span>
                    )}
                    <span className="text-xs font-medium px-2.5 py-0.5 rounded-full"
                      style={{ background: `${m.color}20`, color: m.color, border: `1px solid ${m.color}40` }}>
                      {m.label}
                    </span>
                  </div>
                </div>
                {/* Coverage bar */}
                <div className="h-1 rounded-full" style={{ background: 'rgba(255,255,255,0.06)' }}>
                  <div className="h-1 rounded-full transition-all" style={{ background: m.bar, width: m.width }} />
                </div>
              </div>
            )
          })}
        </div>
      </section>

      {/* ── Curation Standards ── */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-8">
          <Layers className="w-5 h-5 text-[#c4b5fd]" />
          <h2 className="font-display text-3xl text-[#f5f0ff]">Curation Standards</h2>
        </div>
        <div className="rounded-2xl p-8 space-y-6" style={CARD}>
          {[
            {
              title: 'We do not speculate',
              body: 'If a date, nationality, or biographical detail is uncertain, we omit it rather than guess. Partial information is clearly marked. We prefer honest gaps to confident errors.',
            },
            {
              title: 'We do not rank or rank-order traditions',
              body: 'The atlas treats a Carnatic kriti and a West African griot song as equally significant objects of study. No tradition is presented as more sophisticated, more evolved, or more worthy of attention than another.',
            },
            {
              title: 'We use the tradition\'s own terminology',
              body: 'Where a tradition has its own vocabulary — raga, tala, maqam, thaat, melakarta, anga — we use it. We provide explanations but do not replace native terms with approximations.',
            },
            {
              title: 'Living traditions get special care',
              body: 'For traditions that are still actively practiced and evolving, we are especially careful not to present descriptions as fixed or complete. Music is not a museum.',
            },
            {
              title: 'We link to primary sources',
              body: 'Where Wikipedia, Archive.org, Smithsonian, or another authoritative source has covered something well, we link out rather than reproduce it. The atlas is a map, not a destination.',
            },
          ].map((item) => (
            <div key={item.title}>
              <h3 className="font-display text-lg text-[#c4b5fd] mb-2">{item.title}</h3>
              <p className="text-[#a89fc4] leading-relaxed text-sm">{item.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Known Gaps ── */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="w-5 h-5 text-[#f59e0b]" />
          <h2 className="font-display text-3xl text-[#f5f0ff]">Known Gaps</h2>
        </div>
        <p className="text-[#a89fc4] leading-relaxed mb-8">
          We would rather show you the gaps than hide them. These are areas we know need work.
        </p>
        <div className="space-y-4">
          {KNOWN_GAPS.map((gap) => (
            <div key={gap.title} className="rounded-2xl p-6" style={{ ...CARD, border: '1px solid rgba(245,158,11,0.18)' }}>
              <div className="flex items-start justify-between gap-3 mb-2 flex-wrap">
                <h3 className="font-display text-lg text-[#f5f0ff]">{gap.title}</h3>
                <span className="text-xs font-medium px-2.5 py-0.5 rounded-full shrink-0"
                  style={{ background: `${gap.statusColor}18`, color: gap.statusColor, border: `1px solid ${gap.statusColor}40` }}>
                  {gap.status}
                </span>
              </div>
              <p className="text-sm text-[#a89fc4] leading-relaxed">{gap.detail}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── How to Help ── */}
      <section className="mb-10">
        <div className="flex items-center gap-3 mb-6">
          <MessageSquare className="w-5 h-5 text-[#c4b5fd]" />
          <h2 className="font-display text-3xl text-[#f5f0ff]">Help Us Improve</h2>
        </div>
        <div className="rounded-2xl p-8" style={{ ...CARD, border: '1px solid rgba(124,58,237,0.3)' }}>
          <p className="text-[#a89fc4] leading-relaxed text-lg mb-6">
            The atlas is a living document. If you notice a factual error, a missing tradition,
            a misattributed recording, or a gap that matters to you — please tell us.
            Every submission is read, and many have directly improved the data.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link
              href="/feedback"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-medium transition-all duration-200"
              style={{ background: 'linear-gradient(135deg,#7c3aed,#6d28d9)', boxShadow: '0 0 20px rgba(124,58,237,0.3)', color: '#f5f0ff' }}
            >
              <MessageSquare className="w-4 h-4" />
              Submit feedback
            </Link>
            <Link
              href="/about"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-medium transition-all duration-200 text-[#c4b5fd] border border-[rgba(124,58,237,0.3)] hover:border-[rgba(124,58,237,0.5)] hover:bg-[rgba(124,58,237,0.08)]"
            >
              <BookOpen className="w-4 h-4" />
              About the project
            </Link>
          </div>
        </div>
      </section>

      {/* ── Version note ── */}
      <p className="text-center text-xs text-[#6b5d8a]">
        Data model v1 · Last updated May 2026 · More regions and traditions added continuously
      </p>

    </div>
  )
}
