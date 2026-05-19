'use client'

// ─── Constants ────────────────────────────────────────────────────────────────
const CX = 350
const CY = 350

// "Music" in 12 languages, one per clock-hour position
const MUSIC_LANGS = [
  { word: 'Music',    label: 'English'    },  //  0° — 12 o'clock
  { word: 'Musique',  label: 'French'     },  // 30° —  1 o'clock
  { word: 'Música',   label: 'Spanish'    },  // 60° —  2 o'clock
  { word: 'Musik',    label: 'German'     },  // 90° —  3 o'clock
  { word: '音楽',     label: 'Japanese'   },  // 120° —  4 o'clock
  { word: 'संगीत',   label: 'Hindi'      },  // 150° —  5 o'clock
  { word: 'موسيقى',  label: 'Arabic'     },  // 180° —  6 o'clock
  { word: '音乐',     label: 'Chinese'    },  // 210° —  7 o'clock
  { word: '음악',     label: 'Korean'     },  // 240° —  8 o'clock
  { word: 'Музыка',  label: 'Russian'    },  // 270° —  9 o'clock
  { word: 'Müzik',   label: 'Turkish'    },  // 300° — 10 o'clock
  { word: 'Μουσική', label: 'Greek'      },  // 330° — 11 o'clock
]

// ─── Helpers ──────────────────────────────────────────────────────────────────
function toRad(deg: number) {
  return (deg * Math.PI) / 180
}

/** Point on a circle, 0° = top (12 o'clock) */
function polar(r: number, deg: number) {
  const a = toRad(deg - 90)
  return { x: CX + r * Math.cos(a), y: CY + r * Math.sin(a) }
}

/** Diamond polygon centred on the ring at `deg` degrees, elongated radially */
function diamond(r: number, deg: number, radialHalf: number, tangHalf: number) {
  const a = toRad(deg - 90)
  const aT = a + Math.PI / 2
  const tip  = { x: CX + (r + radialHalf) * Math.cos(a),  y: CY + (r + radialHalf) * Math.sin(a)  }
  const base = { x: CX + (r - radialHalf) * Math.cos(a),  y: CY + (r - radialHalf) * Math.sin(a)  }
  const s1   = { x: CX + r * Math.cos(a) + tangHalf * Math.cos(aT), y: CY + r * Math.sin(a) + tangHalf * Math.sin(aT) }
  const s2   = { x: CX + r * Math.cos(a) - tangHalf * Math.cos(aT), y: CY + r * Math.sin(a) - tangHalf * Math.sin(aT) }
  return `${tip.x},${tip.y} ${s1.x},${s1.y} ${base.x},${base.y} ${s2.x},${s2.y}`
}

/** Generate tick marks around a ring */
function genTicks(r: number, count: number) {
  return Array.from({ length: count }, (_, i) => {
    const isMajor = i % (count / 12) === 0
    const a = (i / count) * 2 * Math.PI - Math.PI / 2
    const len = isMajor ? 13 : 6
    return {
      x1: CX + (r - len) * Math.cos(a),
      y1: CY + (r - len) * Math.sin(a),
      x2: CX + r * Math.cos(a),
      y2: CY + r * Math.sin(a),
      isMajor,
    }
  })
}

// ─── Component ────────────────────────────────────────────────────────────────
export default function CosmicCompass({ className = '' }: { className?: string }) {
  const R_OUTER = 298   // outer ring radius
  const R_INNER = 228   // inner ring radius
  const R_LANG  = 262   // language text sits between the two rings
  const R_ROSE  = 100   // compass rose tip radius

  const r1Ticks = genTicks(R_OUTER, 72)   // every 5° — major every 30°
  const r2Ticks = genTicks(R_INNER, 48)   // every 7.5° — major every 45°

  const langItems = MUSIC_LANGS.map(({ word }, i) => ({
    word,
    ...polar(R_LANG, i * 30),
  }))

  return (
    <div className={`pointer-events-none select-none ${className}`}>
      <style>{`
        @keyframes compass-cw  { from { transform: rotate(0deg);    } to { transform: rotate(360deg);  } }
        @keyframes compass-ccw { from { transform: rotate(0deg);    } to { transform: rotate(-360deg); } }
        .compass-cw  {
          transform-origin: ${CX}px ${CY}px;
          animation: compass-cw  48s linear infinite;
        }
        .compass-ccw {
          transform-origin: ${CX}px ${CY}px;
          animation: compass-ccw 34s linear infinite;
        }
      `}</style>

      <svg
        viewBox="0 0 700 700"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <defs>
          {/* Gold gradient for the ring circles */}
          <linearGradient id="goldRing1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%"   stopColor="#fbbf24" stopOpacity="0.9" />
            <stop offset="50%"  stopColor="#f59e0b" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#d97706" stopOpacity="0.7" />
          </linearGradient>
          <linearGradient id="goldRing2" x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%"   stopColor="#fcd34d" stopOpacity="0.85" />
            <stop offset="50%"  stopColor="#f59e0b" stopOpacity="0.75" />
            <stop offset="100%" stopColor="#b45309" stopOpacity="0.65" />
          </linearGradient>
          {/* Radial glow for the compass centre */}
          <radialGradient id="centreGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%"   stopColor="#f59e0b" stopOpacity="0.25" />
            <stop offset="100%" stopColor="#f59e0b" stopOpacity="0"   />
          </radialGradient>
        </defs>

        {/* ── Ambient halos (very faint) ── */}
        <circle cx={CX} cy={CY} r={R_OUTER + 2}
          stroke="rgba(245,158,11,0.06)" strokeWidth="40" />
        <circle cx={CX} cy={CY} r={R_INNER}
          stroke="rgba(245,158,11,0.05)" strokeWidth="28" />
        <circle cx={CX} cy={CY} r={140}
          fill="url(#centreGlow)" />

        {/* ── Language labels (FIXED — between the two rings) ── */}
        {langItems.map(({ word, x, y }, i) => (
          <text
            key={word}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="central"
            fontSize={13}
            fontFamily="Cormorant Garamond, Georgia, serif"
            fontStyle="italic"
            fill="rgba(251,191,36,0.82)"
            letterSpacing="0.04em"
            /* North position (English "Music") slightly brighter */
            opacity={i === 0 ? 1 : 0.82}
          >
            {word}
          </text>
        ))}

        {/* ══════════════════════════════════════════════════════════════
            OUTER RING — rotates CLOCKWISE
        ══════════════════════════════════════════════════════════════ */}
        <g className="compass-cw">
          {/* Ring stroke */}
          <circle cx={CX} cy={CY} r={R_OUTER}
            stroke="url(#goldRing1)" strokeWidth="2" />

          {/* Tick marks */}
          {r1Ticks.map((t, i) => (
            <line
              key={i}
              x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
              stroke={t.isMajor ? '#fbbf24' : '#f59e0b'}
              strokeWidth={t.isMajor ? 2 : 0.9}
              opacity={t.isMajor ? 0.9 : 0.45}
            />
          ))}

          {/* Large diamond ornaments at the 4 cardinal positions (N/E/S/W) */}
          {[0, 90, 180, 270].map((deg) => (
            <polygon
              key={deg}
              points={diamond(R_OUTER, deg, 16, 7)}
              fill={deg === 0 ? '#fbbf24' : '#f59e0b'}
              opacity={deg === 0 ? 1 : 0.85}
            />
          ))}

          {/* Small diamond ornaments at the 4 ordinal positions (NE/SE/SW/NW) */}
          {[45, 135, 225, 315].map((deg) => (
            <polygon
              key={deg}
              points={diamond(R_OUTER, deg, 9, 4)}
              fill="#fbbf24"
              opacity="0.65"
            />
          ))}

          {/* Second gold outline inset by 6px for the double-ring look */}
          <circle cx={CX} cy={CY} r={R_OUTER - 7}
            stroke="rgba(251,191,36,0.3)" strokeWidth="0.75" />
        </g>

        {/* ══════════════════════════════════════════════════════════════
            INNER RING — rotates COUNTER-CLOCKWISE
        ══════════════════════════════════════════════════════════════ */}
        <g className="compass-ccw">
          {/* Ring stroke */}
          <circle cx={CX} cy={CY} r={R_INNER}
            stroke="url(#goldRing2)" strokeWidth="2" />

          {/* Tick marks */}
          {r2Ticks.map((t, i) => (
            <line
              key={i}
              x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
              stroke={t.isMajor ? '#fcd34d' : '#fbbf24'}
              strokeWidth={t.isMajor ? 2 : 0.9}
              opacity={t.isMajor ? 0.85 : 0.38}
            />
          ))}

          {/* Circular jewel ornaments at 8 positions */}
          {Array.from({ length: 8 }, (_, i) => {
            const { x, y } = polar(R_INNER, i * 45)
            const isMajor = i % 2 === 0
            return (
              <circle
                key={i}
                cx={x} cy={y}
                r={isMajor ? 5 : 3}
                fill={isMajor ? '#f59e0b' : '#fbbf24'}
                opacity={isMajor ? 0.85 : 0.6}
              />
            )
          })}

          {/* Inner offset circle for the double-ring look */}
          <circle cx={CX} cy={CY} r={R_INNER + 7}
            stroke="rgba(245,158,11,0.25)" strokeWidth="0.75" />
        </g>

        {/* ══════════════════════════════════════════════════════════════
            COMPASS ROSE — fixed at centre
        ══════════════════════════════════════════════════════════════ */}
        <g>
          {/* Faint inner guide rings */}
          <circle cx={CX} cy={CY} r={118}
            stroke="rgba(245,158,11,0.1)" strokeWidth="1" />
          <circle cx={CX} cy={CY} r={R_ROSE + 8}
            stroke="rgba(245,158,11,0.08)" strokeWidth="0.75" />

          {/* 4 cardinal points — large diamonds along N/E/S/W */}
          {[0, 90, 180, 270].map((deg) => (
            <polygon
              key={deg}
              points={diamond(R_ROSE / 2, deg, R_ROSE / 2, 15)}
              fill={deg === 0 ? '#fbbf24' : '#f59e0b'}
              opacity={deg === 0 ? 0.95 : 0.8}
            />
          ))}

          {/* 4 ordinal points — smaller NE/SE/SW/NW */}
          {[45, 135, 225, 315].map((deg) => (
            <polygon
              key={deg}
              points={diamond(32, deg, 32, 9)}
              fill="#f59e0b"
              opacity="0.55"
            />
          ))}

          {/* Cardinal direction letters */}
          {[
            { label: 'N', deg: 0,   bright: true  },
            { label: 'E', deg: 90,  bright: false },
            { label: 'S', deg: 180, bright: false },
            { label: 'W', deg: 270, bright: false },
          ].map(({ label, deg, bright }) => {
            const { x, y } = polar(120, deg)
            return (
              <text
                key={label}
                x={x} y={y}
                textAnchor="middle"
                dominantBaseline="central"
                fontSize="11"
                fontFamily="Inter, system-ui, sans-serif"
                fontWeight="700"
                fill={bright ? '#fbbf24' : '#f59e0b'}
                opacity={bright ? 0.95 : 0.65}
                letterSpacing="0.12em"
              >
                {label}
              </text>
            )
          })}

          {/* Centre concentric circles */}
          <circle cx={CX} cy={CY} r={24}
            stroke="#f59e0b" strokeWidth="1.5" opacity="0.55"
            fill="rgba(245,158,11,0.05)"
          />
          <circle cx={CX} cy={CY} r={15}
            stroke="#fbbf24" strokeWidth="1" opacity="0.65"
            fill="rgba(245,158,11,0.08)"
          />
          {/* Centre jewel */}
          <circle cx={CX} cy={CY} r={6}
            fill="#f59e0b" opacity="0.9" />
          <circle cx={CX} cy={CY} r={2.5}
            fill="#fef3c7" />
        </g>
      </svg>
    </div>
  )
}
