import Link from 'next/link'

// Region → nebula accent colour
const REGION_ACCENTS: Record<string, { glow: string; border: string; dot: string }> = {
  'South Asia':          { glow: 'rgba(245,158,11,0.2)',  border: 'rgba(245,158,11,0.3)',  dot: '#f59e0b' },
  'East Asia':           { glow: 'rgba(124,58,237,0.2)',  border: 'rgba(124,58,237,0.35)', dot: '#c4b5fd' },
  'Southeast Asia':      { glow: 'rgba(147,51,234,0.2)', border: 'rgba(147,51,234,0.3)',  dot: '#a78bfa' },
  'Central Asia':        { glow: 'rgba(217,119,6,0.2)',  border: 'rgba(217,119,6,0.3)',   dot: '#fbbf24' },
  'Middle East & North Africa': { glow: 'rgba(245,158,11,0.2)', border: 'rgba(245,158,11,0.28)', dot: '#fbbf24' },
  'West Africa':         { glow: 'rgba(234,88,12,0.2)',  border: 'rgba(234,88,12,0.28)',  dot: '#fb923c' },
  'East Africa':         { glow: 'rgba(16,185,129,0.15)', border: 'rgba(16,185,129,0.25)', dot: '#6ee7b7' },
  'Southern Africa':     { glow: 'rgba(20,184,166,0.15)', border: 'rgba(20,184,166,0.25)', dot: '#5eead4' },
  'Central Africa':      { glow: 'rgba(245,158,11,0.15)', border: 'rgba(245,158,11,0.2)', dot: '#fcd34d' },
  'South America':       { glow: 'rgba(236,72,153,0.15)', border: 'rgba(236,72,153,0.25)', dot: '#f9a8d4' },
  'Caribbean':           { glow: 'rgba(6,182,212,0.15)', border: 'rgba(6,182,212,0.25)',  dot: '#67e8f9' },
  'North America':       { glow: 'rgba(59,130,246,0.15)', border: 'rgba(59,130,246,0.25)', dot: '#93c5fd' },
  'Western Europe':      { glow: 'rgba(124,58,237,0.18)', border: 'rgba(124,58,237,0.3)',  dot: '#c4b5fd' },
  'Northern Europe':     { glow: 'rgba(99,102,241,0.18)', border: 'rgba(99,102,241,0.3)', dot: '#a5b4fc' },
  'Eastern Europe':      { glow: 'rgba(139,92,246,0.18)', border: 'rgba(139,92,246,0.3)', dot: '#ddd6fe' },
  'Southern Europe':     { glow: 'rgba(239,68,68,0.15)', border: 'rgba(239,68,68,0.25)',  dot: '#fca5a5' },
  'Oceania':             { glow: 'rgba(6,182,212,0.15)', border: 'rgba(6,182,212,0.22)',  dot: '#7dd3fc' },
  'Global':              { glow: 'rgba(245,158,11,0.15)', border: 'rgba(245,158,11,0.22)', dot: '#fef08a' },
}

const DEFAULT_ACCENT = { glow: 'rgba(124,58,237,0.15)', border: 'rgba(124,58,237,0.25)', dot: '#c4b5fd' }

export default function RegionCard({ region, count }: { region: string; count: number }) {
  const accent = REGION_ACCENTS[region] ?? DEFAULT_ACCENT

  return (
    <Link href={`/traditions?region=${encodeURIComponent(region)}`}>
      <div
        className="group relative rounded-2xl p-6 hover:scale-[1.02] transition-all duration-300 text-center"
        style={{
          background: 'rgba(20, 14, 40, 0.65)',
          backdropFilter: 'blur(12px)',
          border: `1px solid ${accent.border}`,
          boxShadow: `0 4px 20px ${accent.glow}`,
        }}
      >
        <div
          className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
          style={{ background: `radial-gradient(ellipse at center, ${accent.glow}, transparent 70%)` }}
        />

        {/* Accent dot */}
        <div
          className="relative z-10 w-2 h-2 rounded-full mx-auto mb-3"
          style={{ background: accent.dot, boxShadow: `0 0 8px 3px ${accent.glow}` }}
        />

        <h3 className="relative z-10 font-display text-xl text-[#f5f0ff] group-hover:text-[#c4b5fd] transition-colors mb-1 leading-tight">
          {region}
        </h3>
        <p className="relative z-10 text-xs text-[#a89fc4]">
          {count} {count === 1 ? 'tradition' : 'traditions'}
        </p>
      </div>
    </Link>
  )
}
