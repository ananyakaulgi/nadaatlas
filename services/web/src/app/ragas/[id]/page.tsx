import { getRaga } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'

export const dynamic = 'force-dynamic'

interface Props { params: Promise<{ id: string }> }

export default async function RagaDetailPage({ params }: Props) {
  const { id } = await params
  let raga
  try {
    raga = await getRaga(id)
  } catch {
    notFound()
  }

  const TRADITION_COLORS = {
    hindustani: { border: 'rgba(245,158,11,0.3)', badge: 'gold' as const },
    carnatic:   { border: 'rgba(20,184,166,0.3)',  badge: 'teal' as const },
    both:       { border: 'rgba(124,58,237,0.3)',  badge: 'purple' as const },
  }
  const colors = TRADITION_COLORS[raga.tradition as keyof typeof TRADITION_COLORS] ?? TRADITION_COLORS.both

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Back */}
      <Link href="/ragas" className="text-sm text-[#6b5d8a] hover:text-[#a89fc4] transition-colors mb-8 inline-flex items-center gap-1">
        ← All ragas
      </Link>

      {/* Title block */}
      <div className="mt-6 mb-10">
        <div className="flex flex-wrap items-start gap-3 mb-3">
          <h1 className="font-display text-5xl text-[#f5f0ff]">{raga.name}</h1>
          <Badge variant={colors.badge} className="mt-2 capitalize">{raga.tradition === 'both' ? 'Both traditions' : raga.tradition}</Badge>
          {raga.is_verified && <span className="text-[#f59e0b] mt-2 text-lg" title="Verified">✦</span>}
        </div>
        {raga.name_native && (
          <p className="font-display text-2xl text-[#a89fc4] italic">{raga.name_native}</p>
        )}
        {raga.hindustani_name && raga.carnatic_name && (
          <p className="text-sm text-[#6b5d8a] mt-2">
            Hindustani: <span className="text-[#a89fc4]">{raga.hindustani_name}</span>
            {' · '}
            Carnatic: <span className="text-[#a89fc4]">{raga.carnatic_name}</span>
          </p>
        )}
      </div>

      {/* Classification */}
      <div
        className="rounded-2xl p-6 mb-8"
        style={{ background: 'rgba(20,14,40,0.65)', border: `1px solid ${colors.border}`, backdropFilter: 'blur(12px)' }}
      >
        <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Classification</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          {raga.that && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Thaat</p>
              <p className="text-[#f5f0ff]">{raga.that}</p>
            </div>
          )}
          {raga.melakarta_number && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Melakarta</p>
              <p className="text-[#f5f0ff]">#{raga.melakarta_number}</p>
            </div>
          )}
          {raga.time_of_day && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Time of Day</p>
              <p className="text-[#f5f0ff]">{raga.time_of_day}</p>
            </div>
          )}
          {raga.season && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Season</p>
              <p className="text-[#f5f0ff]">{raga.season}</p>
            </div>
          )}
          {raga.rasa && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Rasa</p>
              <p className="text-[#f5f0ff]">{raga.rasa}</p>
            </div>
          )}
        </div>
      </div>

      {/* Scale */}
      {(raga.arohana || raga.avarohana) && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Scale</h2>
          <div className="space-y-4">
            {raga.arohana && (
              <div>
                <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-2">Ārohana (Ascending)</p>
                <p className="font-mono text-lg text-[#c4b5fd] tracking-widest">{raga.arohana}</p>
              </div>
            )}
            {raga.avarohana && (
              <div>
                <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-2">Avarohana (Descending)</p>
                <p className="font-mono text-lg text-[#c4b5fd] tracking-widest">{raga.avarohana}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Characteristic notes */}
      {(raga.vadi || raga.samvadi || raga.pakad) && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Characteristic Notes</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            {raga.vadi && (
              <div>
                <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Vadi (King)</p>
                <p className="font-mono text-xl text-[#f59e0b]">{raga.vadi}</p>
              </div>
            )}
            {raga.samvadi && (
              <div>
                <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Samvadi (Queen)</p>
                <p className="font-mono text-xl text-[#c4b5fd]">{raga.samvadi}</p>
              </div>
            )}
            {raga.pakad && (
              <div className="col-span-full">
                <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Pakad (Characteristic phrase)</p>
                <p className="font-mono text-base text-[#f5f0ff]">{raga.pakad}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Description */}
      {raga.description && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-3">About</h2>
          <p className="text-[#a89fc4] leading-relaxed">{raga.description}</p>
        </div>
      )}

      {/* Wikipedia link */}
      {raga.wikipedia_slug && (
        <a
          href={`https://en.wikipedia.org/wiki/${raga.wikipedia_slug}`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
        >
          Read on Wikipedia ↗
        </a>
      )}
    </div>
  )
}
