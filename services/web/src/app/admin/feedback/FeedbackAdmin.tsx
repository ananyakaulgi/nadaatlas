'use client'

import { useState, useEffect, useCallback } from 'react'
import { Loader2, LogIn, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react'

// ─── Types ────────────────────────────────────────────────────────────────────

type FeedbackStatus = 'new' | 'in_progress' | 'fixed' | 'wont_fix' | 'duplicate'

interface FeedbackItem {
  id: string
  category: string
  name: string | null
  email: string | null
  subject: string | null
  message: string
  page_context: string | null
  status: FeedbackStatus
  resolved_at: string | null
  resolution_note: string | null
  created_at: string
}

// ─── Constants ────────────────────────────────────────────────────────────────

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const STATUS_META: Record<FeedbackStatus, { label: string; color: string; bg: string }> = {
  new:         { label: 'New',         color: '#f59e0b', bg: 'rgba(245,158,11,0.15)'  },
  in_progress: { label: 'In Progress', color: '#60a5fa', bg: 'rgba(96,165,250,0.15)'  },
  fixed:       { label: 'Fixed',       color: '#34d399', bg: 'rgba(52,211,153,0.15)'  },
  wont_fix:    { label: "Won't Fix",   color: '#f87171', bg: 'rgba(248,113,113,0.15)' },
  duplicate:   { label: 'Duplicate',   color: '#a78bfa', bg: 'rgba(167,139,250,0.15)' },
}

const CATEGORY_META: Record<string, { label: string; emoji: string }> = {
  bug_report:      { label: 'Bug',     emoji: '🐛' },
  missing_data:    { label: 'Data',    emoji: '📚' },
  feature_request: { label: 'Feature', emoji: '✨' },
  general:         { label: 'General', emoji: '💬' },
}

const STATUS_FLOW: FeedbackStatus[] = ['new', 'in_progress', 'fixed', 'wont_fix', 'duplicate']

const CARD_STYLE = {
  background: 'rgba(20,14,40,0.7)',
  border: '1px solid rgba(124,58,237,0.2)',
  backdropFilter: 'blur(12px)',
}

// ─── Login ────────────────────────────────────────────────────────────────────

function LoginForm({ onToken }: { onToken: (t: string) => void }) {
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState('')
  const [loading, setLoading]   = useState(false)

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const body = new URLSearchParams({ username: email, password })
      const res  = await fetch(`${API_BASE}/api/v1/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString(),
      })
      if (!res.ok) throw new Error('Invalid credentials')
      const data = await res.json()
      if (!data.access_token) throw new Error('No token returned')
      sessionStorage.setItem('admin_token', data.access_token)
      onToken(data.access_token)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const inputCls = 'w-full px-4 py-2.5 rounded-xl text-sm text-[#f5f0ff] placeholder:text-[#6b5d8a] focus:outline-none'
  const inputStyle = {
    background: 'rgba(20,14,40,0.8)',
    border: '1px solid rgba(124,58,237,0.3)',
    backdropFilter: 'blur(12px)',
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4"
      style={{ background: 'linear-gradient(135deg, #08060f 0%, #12093a 100%)' }}>
      <div className="w-full max-w-sm rounded-2xl p-8" style={CARD_STYLE}>
        <h1 className="font-display text-2xl text-[#f5f0ff] mb-1">Admin Login</h1>
        <p className="text-sm text-[#6b5d8a] mb-6">Feedback dashboard — superuser only</p>

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            required
            className={inputCls}
            style={inputStyle}
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
            className={inputCls}
            style={inputStyle}
          />
          {error && <p className="text-sm text-[#fca5a5]">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl text-sm font-medium transition-all disabled:opacity-60"
            style={{ background: 'linear-gradient(135deg,#7c3aed,#6d28d9)', color: '#f5f0ff' }}
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <LogIn className="w-4 h-4" />}
            Sign in
          </button>
        </form>
      </div>
    </div>
  )
}

// ─── Status badge ─────────────────────────────────────────────────────────────

function StatusBadge({ status }: { status: FeedbackStatus }) {
  const m = STATUS_META[status] ?? STATUS_META.new
  return (
    <span
      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
      style={{ background: m.bg, color: m.color, border: `1px solid ${m.color}40` }}
    >
      {m.label}
    </span>
  )
}

// ─── Status picker ────────────────────────────────────────────────────────────

function StatusPicker({
  current,
  onSelect,
  loading,
}: {
  current: FeedbackStatus
  onSelect: (s: FeedbackStatus) => void
  loading: boolean
}) {
  const [open, setOpen] = useState(false)
  return (
    <div className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        disabled={loading}
        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-50"
        style={{ background: 'rgba(124,58,237,0.15)', border: '1px solid rgba(124,58,237,0.3)', color: '#c4b5fd' }}
      >
        {loading ? <Loader2 className="w-3 h-3 animate-spin" /> : 'Change status'}
        {open ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
      </button>
      {open && (
        <div
          className="absolute left-0 top-full mt-1 w-40 rounded-xl py-1 z-20"
          style={{ background: 'rgba(13,10,26,0.98)', border: '1px solid rgba(124,58,237,0.25)', boxShadow: '0 8px 32px rgba(0,0,0,0.5)' }}
        >
          {STATUS_FLOW.map((s) => (
            <button
              key={s}
              onClick={() => { onSelect(s); setOpen(false) }}
              className="w-full text-left px-4 py-2 text-xs transition-colors hover:bg-[rgba(124,58,237,0.1)]"
              style={{ color: s === current ? STATUS_META[s].color : '#a89fc4' }}
            >
              {s === current && '✓ '}{STATUS_META[s].label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── Feedback row ─────────────────────────────────────────────────────────────

function FeedbackRow({
  item,
  token,
  onUpdate,
}: {
  item: FeedbackItem
  token: string
  onUpdate: (updated: FeedbackItem) => void
}) {
  const [expanded, setExpanded]   = useState(false)
  const [updating, setUpdating]   = useState(false)
  const [note, setNote]           = useState(item.resolution_note ?? '')
  const [editNote, setEditNote]   = useState(false)

  const cat = CATEGORY_META[item.category] ?? { emoji: '?', label: item.category }

  async function changeStatus(newStatus: FeedbackStatus) {
    setUpdating(true)
    try {
      const res = await fetch(`${API_BASE}/api/v1/feedback/${item.id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ status: newStatus }),
      })
      if (!res.ok) throw new Error('Update failed')
      onUpdate(await res.json())
    } finally {
      setUpdating(false)
    }
  }

  async function saveNote() {
    setUpdating(true)
    try {
      const res = await fetch(`${API_BASE}/api/v1/feedback/${item.id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ status: item.status, resolution_note: note }),
      })
      if (!res.ok) throw new Error('Update failed')
      onUpdate(await res.json())
      setEditNote(false)
    } finally {
      setUpdating(false)
    }
  }

  const date = new Date(item.created_at).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  })

  return (
    <div className="rounded-xl overflow-hidden" style={CARD_STYLE}>
      {/* Header row */}
      <button
        className="w-full text-left px-5 py-4 flex items-start gap-3"
        onClick={() => setExpanded((x) => !x)}
      >
        <span className="text-xl mt-0.5 shrink-0">{cat.emoji}</span>
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <StatusBadge status={item.status} />
            <span className="text-xs text-[#6b5d8a]">{cat.label}</span>
            <span className="text-xs text-[#6b5d8a]">·</span>
            <span className="text-xs text-[#6b5d8a]">{date}</span>
            {item.name && (
              <>
                <span className="text-xs text-[#6b5d8a]">·</span>
                <span className="text-xs text-[#a89fc4]">{item.name}</span>
              </>
            )}
          </div>
          <p className="text-sm font-medium text-[#f5f0ff] truncate">
            {item.subject || item.message.slice(0, 80)}
          </p>
          {item.subject && (
            <p className="text-xs text-[#6b5d8a] truncate mt-0.5">{item.message.slice(0, 80)}</p>
          )}
        </div>
        <span className="text-[#6b5d8a] shrink-0 ml-2 mt-1">
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </span>
      </button>

      {/* Expanded detail */}
      {expanded && (
        <div className="px-5 pb-5 border-t border-[rgba(124,58,237,0.15)]">
          {/* Full message */}
          <div className="mt-4 mb-4 p-4 rounded-xl" style={{ background: 'rgba(0,0,0,0.3)' }}>
            <p className="text-sm text-[#c4b5fd] whitespace-pre-wrap leading-relaxed">{item.message}</p>
          </div>

          {/* Meta */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4 text-xs">
            {item.email && (
              <div>
                <p className="text-[#6b5d8a] mb-0.5">Email</p>
                <p className="text-[#a89fc4]">{item.email}</p>
              </div>
            )}
            {item.page_context && (
              <div>
                <p className="text-[#6b5d8a] mb-0.5">Page</p>
                <p className="text-[#a89fc4] truncate">{item.page_context}</p>
              </div>
            )}
            {item.resolved_at && (
              <div>
                <p className="text-[#6b5d8a] mb-0.5">Resolved</p>
                <p className="text-[#34d399]">
                  {new Date(item.resolved_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </p>
              </div>
            )}
          </div>

          {/* Resolution note */}
          <div className="mb-4">
            {editNote ? (
              <div>
                <textarea
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  rows={3}
                  placeholder="Add a resolution note…"
                  className="w-full px-3 py-2 rounded-xl text-sm text-[#f5f0ff] placeholder:text-[#6b5d8a] focus:outline-none resize-none mb-2"
                  style={{ background: 'rgba(20,14,40,0.8)', border: '1px solid rgba(124,58,237,0.3)' }}
                />
                <div className="flex gap-2">
                  <button
                    onClick={saveNote}
                    disabled={updating}
                    className="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-60"
                    style={{ background: 'rgba(52,211,153,0.15)', color: '#34d399', border: '1px solid rgba(52,211,153,0.3)' }}
                  >
                    {updating ? 'Saving…' : 'Save note'}
                  </button>
                  <button
                    onClick={() => { setNote(item.resolution_note ?? ''); setEditNote(false) }}
                    className="px-3 py-1.5 rounded-lg text-xs text-[#6b5d8a] transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex items-start gap-2">
                {item.resolution_note ? (
                  <p className="text-xs text-[#a89fc4] italic flex-1">📝 {item.resolution_note}</p>
                ) : (
                  <p className="text-xs text-[#6b5d8a] flex-1">No resolution note</p>
                )}
                <button
                  onClick={() => setEditNote(true)}
                  className="text-xs text-[#7c3aed] hover:text-[#a78bfa] transition-colors shrink-0"
                >
                  {item.resolution_note ? 'Edit note' : '+ Add note'}
                </button>
              </div>
            )}
          </div>

          {/* Status actions */}
          <div className="flex items-center gap-3 flex-wrap">
            <StatusPicker current={item.status} onSelect={changeStatus} loading={updating} />

            {/* Quick-action buttons */}
            {item.status !== 'fixed' && (
              <button
                onClick={() => changeStatus('fixed')}
                disabled={updating}
                className="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-60"
                style={{ background: 'rgba(52,211,153,0.15)', color: '#34d399', border: '1px solid rgba(52,211,153,0.3)' }}
              >
                ✓ Mark fixed
              </button>
            )}
            {item.status !== 'in_progress' && item.status !== 'fixed' && (
              <button
                onClick={() => changeStatus('in_progress')}
                disabled={updating}
                className="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-60"
                style={{ background: 'rgba(96,165,250,0.15)', color: '#60a5fa', border: '1px solid rgba(96,165,250,0.3)' }}
              >
                → In progress
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

// ─── Main dashboard ───────────────────────────────────────────────────────────

export default function FeedbackAdmin() {
  const [token, setToken]           = useState<string | null>(null)
  const [items, setItems]           = useState<FeedbackItem[]>([])
  const [loading, setLoading]       = useState(false)
  const [error, setError]           = useState('')
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [filterCategory, setFilterCategory] = useState<string>('all')

  // Restore token from sessionStorage on mount
  useEffect(() => {
    const saved = sessionStorage.getItem('admin_token')
    if (saved) setToken(saved)
  }, [])

  const fetchItems = useCallback(async (tok: string) => {
    setLoading(true)
    setError('')
    try {
      const params = new URLSearchParams()
      if (filterStatus !== 'all') params.set('status', filterStatus)
      if (filterCategory !== 'all') params.set('category', filterCategory)
      params.set('limit', '200')

      const res = await fetch(`${API_BASE}/api/v1/feedback/?${params}`, {
        headers: { Authorization: `Bearer ${tok}` },
      })
      if (res.status === 401 || res.status === 403) {
        sessionStorage.removeItem('admin_token')
        setToken(null)
        return
      }
      if (!res.ok) throw new Error('Failed to load feedback')
      setItems(await res.json())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error loading feedback')
    } finally {
      setLoading(false)
    }
  }, [filterStatus, filterCategory])

  useEffect(() => {
    if (token) fetchItems(token)
  }, [token, fetchItems])

  if (!token) return <LoginForm onToken={setToken} />

  const ALL_STATUSES: FeedbackStatus[] = ['new', 'in_progress', 'fixed', 'wont_fix', 'duplicate']

  // ── Counts ──
  const counts = ALL_STATUSES.reduce((acc, s) => {
    acc[s] = items.filter((i) => i.status === s).length
    return acc
  }, {} as Record<string, number>)

  return (
    <div
      className="min-h-screen px-4 py-8"
      style={{ background: 'linear-gradient(135deg, #08060f 0%, #12093a 100%)' }}
    >
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="font-display text-3xl text-[#f5f0ff]">Feedback</h1>
            <p className="text-[#6b5d8a] text-sm mt-1">{items.length} submissions total</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => fetchItems(token)}
              disabled={loading}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs text-[#a89fc4] transition-colors hover:text-[#f5f0ff] disabled:opacity-50"
              style={{ border: '1px solid rgba(124,58,237,0.2)' }}
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <button
              onClick={() => { sessionStorage.removeItem('admin_token'); setToken(null) }}
              className="text-xs text-[#6b5d8a] hover:text-[#fca5a5] transition-colors"
            >
              Sign out
            </button>
          </div>
        </div>

        {/* Status summary chips */}
        <div className="flex flex-wrap gap-2 mb-6">
          <button
            onClick={() => setFilterStatus('all')}
            className="px-3 py-1.5 rounded-full text-xs font-medium transition-colors"
            style={{
              background: filterStatus === 'all' ? 'rgba(124,58,237,0.25)' : 'rgba(124,58,237,0.08)',
              border: `1px solid ${filterStatus === 'all' ? 'rgba(124,58,237,0.5)' : 'rgba(124,58,237,0.2)'}`,
              color: filterStatus === 'all' ? '#c4b5fd' : '#6b5d8a',
            }}
          >
            All ({items.length})
          </button>
          {ALL_STATUSES.map((s) => (
            <button
              key={s}
              onClick={() => setFilterStatus(s === filterStatus ? 'all' : s)}
              className="px-3 py-1.5 rounded-full text-xs font-medium transition-colors"
              style={{
                background: filterStatus === s ? STATUS_META[s].bg : 'rgba(124,58,237,0.05)',
                border: `1px solid ${filterStatus === s ? STATUS_META[s].color + '60' : 'rgba(124,58,237,0.15)'}`,
                color: filterStatus === s ? STATUS_META[s].color : '#6b5d8a',
              }}
            >
              {STATUS_META[s].label} ({counts[s] ?? 0})
            </button>
          ))}
        </div>

        {/* Category filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          {['all', 'bug_report', 'missing_data', 'feature_request', 'general'].map((cat) => {
            const meta = cat === 'all' ? { emoji: '📋', label: 'All categories' } : CATEGORY_META[cat]
            const active = filterCategory === cat
            return (
              <button
                key={cat}
                onClick={() => setFilterCategory(cat)}
                className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs transition-colors"
                style={{
                  background: active ? 'rgba(124,58,237,0.2)' : 'rgba(124,58,237,0.05)',
                  border: `1px solid ${active ? 'rgba(124,58,237,0.4)' : 'rgba(124,58,237,0.15)'}`,
                  color: active ? '#c4b5fd' : '#6b5d8a',
                }}
              >
                <span>{meta.emoji}</span>
                <span>{meta.label}</span>
              </button>
            )
          })}
        </div>

        {/* Error */}
        {error && (
          <div className="mb-4 px-4 py-3 rounded-xl text-sm text-[#fca5a5]"
            style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)' }}>
            {error}
          </div>
        )}

        {/* List */}
        {loading && items.length === 0 ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-8 h-8 text-[#7c3aed] animate-spin" />
          </div>
        ) : items.length === 0 ? (
          <div className="text-center py-20 text-[#6b5d8a]">No feedback found.</div>
        ) : (
          <div className="space-y-3">
            {items.map((item) => (
              <FeedbackRow
                key={item.id}
                item={item}
                token={token}
                onUpdate={(updated) =>
                  setItems((prev) => prev.map((i) => (i.id === updated.id ? updated : i)))
                }
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
