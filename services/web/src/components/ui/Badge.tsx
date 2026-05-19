import clsx from 'clsx'

interface BadgeProps {
  children: React.ReactNode
  variant?: 'default' | 'gold' | 'teal' | 'rose' | 'sage' | 'lavender' | 'cream'
  className?: string
}

const variants = {
  default:  'bg-[rgba(124,58,237,0.15)] text-[#c4b5fd] border border-[rgba(124,58,237,0.25)]',
  gold:     'bg-[rgba(245,158,11,0.12)] text-[#fbbf24] border border-[rgba(245,158,11,0.25)]',
  teal:     'bg-[rgba(20,184,166,0.12)] text-[#5eead4] border border-[rgba(20,184,166,0.2)]',
  rose:     'bg-[rgba(236,72,153,0.12)] text-[#f9a8d4] border border-[rgba(236,72,153,0.2)]',
  sage:     'bg-[rgba(16,185,129,0.12)] text-[#6ee7b7] border border-[rgba(16,185,129,0.2)]',
  lavender: 'bg-[rgba(167,139,250,0.15)] text-[#ddd6fe] border border-[rgba(167,139,250,0.25)]',
  cream:    'bg-[rgba(245,158,11,0.1)]  text-[#fcd34d] border border-[rgba(245,158,11,0.18)]',
}

export default function Badge({ children, variant = 'default', className }: BadgeProps) {
  return (
    <span
      className={clsx(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium tracking-wide',
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  )
}
