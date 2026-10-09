/** ExamForge M2 — 403 Access Denied Page */
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext.jsx'

export default function AccessDenied() {
  const { user } = useAuth()
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--color-bg)' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
        style={{ textAlign: 'center', padding: 48 }}
      >
        <div style={{ fontSize: '5rem', lineHeight: 1, marginBottom: 16 }}>🚫</div>
        <h1 style={{ fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: '2.5rem', color: 'var(--color-error)', margin: '0 0 12px' }}>Access Denied</h1>
        <h2 style={{ fontWeight: 700, color: 'var(--color-charcoal)', marginBottom: 12 }}>You don't have permission</h2>
        <p style={{ color: 'var(--color-gray)', marginBottom: 8, maxWidth: 420 }}>
          Your current role ({user?.role || 'guest'}) does not have access to this page.
        </p>
        <p style={{ color: 'var(--color-gray)', marginBottom: 32, fontSize: '0.875rem' }}>
          Contact your administrator if you believe this is a mistake.
        </p>
        <Link to="/students" className="btn btn-primary">← Back to Dashboard</Link>
      </motion.div>
    </div>
  )
}
