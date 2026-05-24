import type { Metadata } from 'next'
import FeedbackForm from './FeedbackForm'

export const metadata: Metadata = {
  title: 'Feedback — नाद Atla𝄞',
  description: 'Share a bug report, missing data, or a feature idea — help us build the world\'s best music encyclopedia.',
}

export default function FeedbackPage() {
  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-10">
        <h1 className="font-display text-5xl text-[#f5f0ff] mb-3">Feedback</h1>
        <p className="text-[#a89fc4] text-lg max-w-xl leading-relaxed">
          Found something broken? Noticed a missing raga, composer, or piece of history?
          Have an idea? We read everything.
        </p>
      </div>

      <FeedbackForm />
    </div>
  )
}
