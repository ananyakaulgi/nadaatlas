'use client'

import { useState } from 'react'
import { CheckCircle2, AlertCircle, Loader2 } from 'lucide-react'

const CATEGORIES = [
  { value: 'bug_report',      label: '🐛  Bug report',      desc: 'Something is broken or behaving wrong' },
  { value: 'missing_data',    label: '📚  Missing data',    desc: 'A raga, composer, artist, or piece is missing or incorrect' },
  { value: 'feature_request', label: '✨  Feature request', desc: 'Something you\'d like to see added' },
  { value: 'general',         label: '💬  General',         desc: 'Comments, questions, or anything else' },
]

const INPUT_STYLE = {
  background: 'rgba(20, 14, 40, 0.7)',
  border: '1px solid rgba(124,58,237,0.25)',
  backdropFilter: 'blur(12px)',
  boxSizing: 'border-box' as const,
  transition: 'border-color 150ms ease, box-shadow 150ms ease',
}

const INPUT_FOCUS = {
  borderColor: 'rgba(124,58,237,0.6)',
  boxShadow: '0 0 0 3px rgba(124,58,237,0.1)',
}

const INPUT_BLUR = {
  borderColor: 'rgba(124,58,237,0.25)',
  boxShadow: 'none',
}

type Status = 'idle' | 'submitting' | 'success' | 'error'

export default function FeedbackForm() {
  const [category, setCategory]   = useState('general')
  const [name, setName]           = useState('')
  const [email, setEmail]         = useState('')
  const [subject, setSubject]     = useState('')
  const [message, setMessage]     = useState('')
  const [status, setStatus]       = useState<Status>('idle')
  const [errorMsg, setErrorMsg]   = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (message.trim().length < 10) {
      setErrorMsg('Please write at least 10 characters in your message.')
      return
    }

    setStatus('submitting')
    setErrorMsg('')

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const res = await fetch(`${apiBase}/api/v1/feedback/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category,
          name:    name.trim()    || null,
          email:   email.trim()   || null,
          subject: subject.trim() || null,
          message: message.trim(),
          page_context: typeof window !== 'undefined' ? document.referrer || null : null,
        }),
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data?.detail || `Server error ${res.status}`)
      }

      setStatus('success')
    } catch (err) {
      setStatus('error')
      setErrorMsg(err instanceof Error ? err.message : 'Something went wrong. Please try again.')
    }
  }

  if (status === 'success') {
    return (
      <div
        className="rounded-2xl p-10 text-center"
        style={{ background: 'rgba(20,14,40,0.65)', border: '1px solid rgba(34,197,94,0.3)', backdropFilter: 'blur(12px)' }}
      >
        <CheckCircle2 className="w-12 h-12 text-[#34d399] mx-auto mb-4" />
        <h2 className="font-display text-2xl text-[#f5f0ff] mb-2">Thank you!</h2>
        <p className="text-[#a89fc4] leading-relaxed max-w-sm mx-auto">
          Your feedback has been received. We genuinely read every submission and use
          it to make नाद Atla𝄞 better.
        </p>
        <button
          onClick={() => {
            setStatus('idle')
            setMessage('')
            setSubject('')
            setName('')
            setEmail('')
          }}
          className="mt-6 text-sm text-[#f59e0b] hover:text-[#fbbf24] transition-colors"
        >
          Submit another →
        </button>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* Category pills */}
      <div className="mb-7">
        <p className="text-sm text-[#a89fc4] mb-3 font-medium">What kind of feedback is this?</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.value}
              type="button"
              onClick={() => setCategory(cat.value)}
              className="text-left rounded-xl px-4 py-3 transition-all duration-150"
              style={{
                background: category === cat.value
                  ? 'rgba(124,58,237,0.2)'
                  : 'rgba(20,14,40,0.6)',
                border: category === cat.value
                  ? '1px solid rgba(124,58,237,0.5)'
                  : '1px solid rgba(124,58,237,0.15)',
                backdropFilter: 'blur(12px)',
              }}
            >
              <span className="block text-sm font-medium text-[#f5f0ff] mb-0.5">{cat.label}</span>
              <span className="block text-xs text-[#6b5d8a]">{cat.desc}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Name + Email row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-xs text-[#6b5d8a] uppercase tracking-wide mb-1.5">
            Name <span className="normal-case">(optional)</span>
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Your name"
            className="w-full px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] placeholder:text-[#6b5d8a] focus:outline-none"
            style={INPUT_STYLE}
            onFocus={(e) => Object.assign(e.currentTarget.style, INPUT_FOCUS)}
            onBlur={(e)  => Object.assign(e.currentTarget.style, INPUT_BLUR)}
          />
        </div>
        <div>
          <label className="block text-xs text-[#6b5d8a] uppercase tracking-wide mb-1.5">
            Email <span className="normal-case">(optional — for follow-up)</span>
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="w-full px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] placeholder:text-[#6b5d8a] focus:outline-none"
            style={INPUT_STYLE}
            onFocus={(e) => Object.assign(e.currentTarget.style, INPUT_FOCUS)}
            onBlur={(e)  => Object.assign(e.currentTarget.style, INPUT_BLUR)}
          />
        </div>
      </div>

      {/* Subject */}
      <div className="mb-4">
        <label className="block text-xs text-[#6b5d8a] uppercase tracking-wide mb-1.5">
          Subject <span className="normal-case">(optional)</span>
        </label>
        <input
          type="text"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="Brief summary…"
          className="w-full px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] placeholder:text-[#6b5d8a] focus:outline-none"
          style={INPUT_STYLE}
          onFocus={(e) => Object.assign(e.currentTarget.style, INPUT_FOCUS)}
          onBlur={(e)  => Object.assign(e.currentTarget.style, INPUT_BLUR)}
        />
      </div>

      {/* Message */}
      <div className="mb-6">
        <label className="block text-xs text-[#6b5d8a] uppercase tracking-wide mb-1.5">
          Message <span className="text-[#7c3aed]">*</span>
        </label>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Tell us what you found, what's missing, or what you'd love to see…"
          rows={6}
          className="w-full px-4 py-3 rounded-xl text-sm text-[#f5f0ff] placeholder:text-[#6b5d8a] focus:outline-none resize-none"
          style={INPUT_STYLE}
          onFocus={(e) => Object.assign(e.currentTarget.style, INPUT_FOCUS)}
          onBlur={(e)  => Object.assign(e.currentTarget.style, INPUT_BLUR)}
        />
        <p className="text-xs text-[#6b5d8a] mt-1 text-right">{message.length} / 5000</p>
      </div>

      {/* Error message */}
      {(status === 'error' || errorMsg) && (
        <div
          className="flex items-start gap-3 rounded-xl px-4 py-3 mb-5"
          style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)' }}
        >
          <AlertCircle className="w-4 h-4 text-[#fca5a5] shrink-0 mt-0.5" />
          <p className="text-sm text-[#fca5a5]">{errorMsg || 'Something went wrong. Please try again.'}</p>
        </div>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={status === 'submitting'}
        className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-medium transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed"
        style={{
          background: 'linear-gradient(135deg, #7c3aed, #6d28d9)',
          boxShadow: '0 0 20px rgba(124,58,237,0.35)',
          color: '#f5f0ff',
        }}
      >
        {status === 'submitting' ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Sending…
          </>
        ) : (
          'Send feedback'
        )}
      </button>

      <p className="text-xs text-[#6b5d8a] text-center mt-4">
        Your email is never shared. We use it only to follow up if needed.
      </p>
    </form>
  )
}
