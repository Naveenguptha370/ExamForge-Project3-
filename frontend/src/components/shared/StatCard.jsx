/** ExamForge M2 — Reusable StatCard */
import { motion } from 'framer-motion'

export default function StatCard({ label, value, icon: Icon, variant = 'green', change, changeLabel, loading }) {
  const variants = {
    green:  { accent: 'var(--color-emerald)', bg: 'var(--color-sage)',      text: 'var(--color-emerald)' },
    amber:  { accent: 'var(--color-amber)',   bg: 'var(--color-amber-100)', text: 'var(--color-amber-600)' },
    error:  { accent: 'var(--color-error)',   bg: '#FEE2E2',                text: 'var(--color-error)' },
    forest: { accent: 'var(--color-forest)',  bg: 'var(--color-sage)',      text: 'var(--color-forest)' },
    gold:   { accent: 'var(--color-gold)',    bg: 'var(--color-amber-100)', text: 'var(--color-gold)' },
  }
  const v = variants[variant] || variants.green

  if (loading) {
    return (
      <div className="stat-card" style={{ borderLeft: `4px solid ${v.accent}` }}>
        <div className="skeleton" style={{ width: 48, height: 48, borderRadius: 10 }} />
        <div style={{ flex: 1 }}>
          <div className="skeleton skeleton-text lg" style={{ width: '60%' }} />
          <div className="skeleton skeleton-text sm" style={{ width: '80%', marginTop: 6 }} />
        </div>
      </div>
    )
  }

  return (
    <motion.div
      className="stat-card"
      style={{ borderLeft: `4px solid ${v.accent}` }}
      whileHover={{ y: -3, boxShadow: '0 8px 24px rgba(21,128,61,0.14)' }}
      transition={{ duration: 0.18 }}
    >
      {Icon && (
        <div className="stat-icon" style={{ background: v.bg, color: v.text }}>
          <Icon size={22} />
        </div>
      )}
      <div className="stat-content">
        <div className="stat-value">
          {typeof value === 'number' ? value.toLocaleString() : (value ?? '—')}
        </div>
        <div className="stat-label">{label}</div>
        {change !== undefined && (
          <div className={`stat-change ${change >= 0 ? 'up' : 'down'}`}>
            {change >= 0 ? '↑' : '↓'} {Math.abs(change)}% {changeLabel || 'vs last period'}
          </div>
        )}
      </div>
    </motion.div>
  )
}
