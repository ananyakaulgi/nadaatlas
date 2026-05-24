import type { Metadata } from 'next'
import FeedbackAdmin from './FeedbackAdmin'

export const metadata: Metadata = {
  title: 'Feedback Admin — नाद Atla𝄞',
  robots: { index: false, follow: false },
}

export default function FeedbackAdminPage() {
  return <FeedbackAdmin />
}
