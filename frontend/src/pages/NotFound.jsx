/** ExamForge M2 — 404 Not Found Page */
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function NotFound() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--color-bg)' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
        style={{ textAlign: 'center', padding: 48 }}
      >
        <div style={{ fontSize: '6rem', lineHeight: 1, marginBottom: 16 }}>🔍</div>
        <h1 style={{ fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: '3rem', color: 'var(--color-forest)', margin: '0 0 12px' }}>404</h1>
        <h2 style={{ fontWeight: 700, color: 'var(--color-charcoal)', marginBottom: 12 }}>Page Not Found</h2>
        <p style={{ color: 'var(--color-gray)', marginBottom: 32, maxWidth: 400 }}>
          The page you are looking for doesn't exist or has been moved.
        </p>
        <Link to="/students" className="btn btn-primary">
          ← Go to Dashboard
        </Link>
      </motion.div>
    </div>
  )
}
