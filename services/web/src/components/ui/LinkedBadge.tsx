'use client'

/**
 * A Badge that navigates to `href` when clicked.
 * Stops click propagation so it works correctly inside card <Link> wrappers.
 */
import Link from 'next/link'
import Badge from './Badge'
import type { ComponentProps } from 'react'

type BadgeVariant = ComponentProps<typeof Badge>['variant']

interface Props {
  href: string
  variant?: BadgeVariant
  className?: string
  children: React.ReactNode
}

export default function LinkedBadge({ href, variant, className, children }: Props) {
  return (
    <Link
      href={href}
      onClick={(e) => e.stopPropagation()}
      className="hover:opacity-75 transition-opacity"
    >
      <Badge variant={variant} className={className}>
        {children}
      </Badge>
    </Link>
  )
}
