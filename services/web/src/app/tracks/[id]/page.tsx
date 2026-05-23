import { getTrack } from '@/lib/api'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import Badge from '@/components/ui/Badge'

export const dynamic = 'force-dynamic'

interface Props { params: Promise<{ id: string }> }

function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${String(s).padStart(2, '0')}`
}

export default async function TrackDetailPage({ params }: Props) {
  const { id } = await params
  let track
  try {
    track = await getTrack(id)
  } catch {
    notFound()
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link href="/tracks" className="text-sm text-[#6b5d8a] hover:text-[#a89fc4] transition-colors mb-8 inline-flex items-center gap-1">
        ← All tracks
      </Link>

      {/* Title */}
      <div className="mt-6 mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-2">{track.title}</h1>
        {track.title_native && (
          <p className="font-display text-2xl text-[#a89fc4] italic mb-4">{track.title_native}</p>
        )}
        <div className="flex flex-wrap gap-2">
          {track.musical_tradition && <Badge variant="lavender">{track.musical_tradition}</Badge>}
          {track.raga && <Badge variant="teal">{track.raga}</Badge>}
          {track.tala && <Badge variant="sage">{track.tala}</Badge>}
          {track.maqam && <Badge variant="sage">{track.maqam}</Badge>}
          {track.duration_seconds && (
            <Badge variant="gold">{formatDuration(track.duration_seconds)}</Badge>
          )}
        </div>
      </div>

      {/* Key info */}
      <div
        className="rounded-2xl p-6 mb-8"
        style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(124,58,237,0.2)', backdropFilter: 'blur(12px)' }}
      >
        <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Details</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <div>
            <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Artist</p>
            <Link
              href={`/artists/${track.artist.id}`}
              className="text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
            >
              {track.artist.name}
            </Link>
          </div>

          {track.album && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Album</p>
              <p className="text-[#f5f0ff]">{track.album.title}</p>
            </div>
          )}

          {track.musical_tradition && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Tradition</p>
              <p className="text-[#f5f0ff]">{track.musical_tradition}</p>
            </div>
          )}

          {track.raga && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Raga</p>
              <p className="text-[#c4b5fd]">{track.raga}</p>
            </div>
          )}

          {track.tala && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Tala</p>
              <p className="text-[#2dd4bf]">{track.tala}</p>
            </div>
          )}

          {track.maqam && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Maqam</p>
              <p className="text-[#f5f0ff]">{track.maqam}</p>
            </div>
          )}

          {track.duration_seconds && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Duration</p>
              <p className="text-[#f5f0ff] font-mono">{formatDuration(track.duration_seconds)}</p>
            </div>
          )}

          {track.track_number && (
            <div>
              <p className="text-xs text-[#6b5d8a] uppercase tracking-wide mb-1">Track No.</p>
              <p className="text-[#f5f0ff]">{track.track_number}</p>
            </div>
          )}
        </div>
      </div>

      {/* Listen */}
      {(track.youtube_url || track.spotify_url) && (
        <div
          className="rounded-2xl p-6 mb-8"
          style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(245,158,11,0.2)', backdropFilter: 'blur(12px)' }}
        >
          <h2 className="font-display text-xl text-[#f5f0ff] mb-4">Listen</h2>
          <div className="flex flex-wrap gap-4">
            {track.youtube_url && (
              <a
                href={track.youtube_url}
                target="_blank" rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all"
                style={{ background: 'rgba(239,68,68,0.15)', border: '1px solid rgba(239,68,68,0.3)', color: '#fca5a5' }}
              >
                ▶ Watch on YouTube
              </a>
            )}
            {track.spotify_url && (
              <a
                href={track.spotify_url}
                target="_blank" rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all"
                style={{ background: 'rgba(34,197,94,0.12)', border: '1px solid rgba(34,197,94,0.3)', color: '#86efac' }}
              >
                ♫ Listen on Spotify
              </a>
            )}
          </div>
        </div>
      )}

    </div>
  )
}
