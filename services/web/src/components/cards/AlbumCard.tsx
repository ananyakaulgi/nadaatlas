import Link from 'next/link'
import Badge from '@/components/ui/Badge'
import type { Album } from '@/lib/types'
import { Music } from 'lucide-react'

function formatYear(dateStr: string | null): string | null {
  if (!dateStr) return null
  try {
    return String(new Date(dateStr).getFullYear())
  } catch {
    return null
  }
}

export default function AlbumCard({ album }: { album: Album }) {
  const year = formatYear(album.release_date)

  return (
    <Link href={`/albums/${album.id}`}>
      <div
        className="group relative rounded-2xl overflow-hidden hover:scale-[1.01] transition-all duration-300 h-full flex flex-col"
        style={{
          background: 'rgba(20, 14, 40, 0.65)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(245,158,11,0.18)',
          boxShadow: '0 2px 16px rgba(245,158,11,0.06)',
        }}
      >
        {/* Cover image area */}
        <div
          className="aspect-square flex items-center justify-center relative overflow-hidden"
          style={{ background: 'linear-gradient(135deg, rgba(76,29,149,0.4), rgba(245,158,11,0.15))' }}
        >
          {album.cover_image_url ? (
            <img
              src={album.cover_image_url}
              alt={album.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <Music className="w-12 h-12 text-[#c4b5fd] opacity-30" />
          )}
          <div
            className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            style={{ background: 'radial-gradient(ellipse at center, rgba(245,158,11,0.1), transparent 70%)' }}
          />
        </div>

        <div className="p-5 flex flex-col flex-1">
          <h3 className="font-display text-lg text-[#f5f0ff] group-hover:text-[#fbbf24] transition-colors leading-tight mb-1">
            {album.title}
          </h3>

          {album.title_native && (
            <p className="font-display text-[#a89fc4] text-sm italic mb-2">{album.title_native}</p>
          )}

          {album.artist && (
            <p className="text-sm text-[#a89fc4] mb-2">{album.artist.name}</p>
          )}

          <div className="flex flex-wrap gap-1.5 mt-auto pt-2">
            {album.album_type && <Badge variant="gold">{album.album_type}</Badge>}
            {year && <Badge variant="default">{year}</Badge>}
          </div>
        </div>
      </div>
    </Link>
  )
}
