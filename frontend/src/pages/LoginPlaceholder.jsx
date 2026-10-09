/** ExamForge M2 — Login Placeholder (M1 provides real auth) */
import { useState } from 'react'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext.jsx'

export default function LoginPlaceholder() {
  const { mockLogin } = useAuth()
  const [role, setRole] = useState('admin')

  return (
    <div style={{
      minHeight: '100vh', background: 'linear-gradient(135deg, var(--color-forest) 0%, #0f4c25 60%, #0a2e16 100%)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24,
    }}>
      <motion.div
        initial={{ opacity: 0, scale: 0.94, y: 24 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.35, ease: 'easeOut' }}
        style={{
          background: 'var(--color-white)', borderRadius: 20, padding: '48px',
          width: '100%', maxWidth: 440, boxShadow: '0 32px 80px rgba(0,0,0,0.35)',
          textAlign: 'center',
        }}
      >
        {/* Logo */}
        <div style={{
          width: 64, height: 64, borderRadius: 16, margin: '0 auto 24px',
          background: 'linear-gradient(135deg, var(--color-forest), var(--color-emerald))',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          color: 'white', fontWeight: 900, fontSize: '1.25rem',
          boxShadow: 'var(--shadow-green)',
        }}>EF</div>

        <h1 style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: '1.5rem', color: 'var(--color-forest)', marginBottom: 6 }}>
          ExamForge
        </h1>
        <p style={{ color: 'var(--color-gray)', marginBottom: 32, fontSize: '0.875rem' }}>
          M2 — Student & Academic Module
        </p>

        {/* Dev notice */}
        <div style={{
          background: 'var(--color-amber-100)', border: '1px solid var(--color-amber)',
          borderRadius: 'var(--radius-md)', padding: '12px 16px', marginBottom: 28,
          fontSize: '0.8125rem', color: '#92400E', textAlign: 'left',
        }}>
          <strong>Developer Mode</strong> — M1 Auth is not yet integrated. Use the mock login below for M2 development.
        </div>

        <div className="form-group">
          <label className="form-label">Login as</label>
          <select className="form-select" value={role} onChange={e => setRole(e.target.value)}>
            <option value="admin">Admin</option>
            <option value="exam_staff">Exam Staff</option>
            <option value="faculty">Faculty</option>
            <option value="student">Student</option>
          </select>
        </div>

        <button
          className="btn btn-primary"
          style={{ width: '100%', marginTop: 8, justifyContent: 'center', padding: '12px' }}
          onClick={() => mockLogin(role)}
        >
          Continue as {role.replace('_', ' ')}
        </button>

        <p style={{ marginTop: 20, fontSize: '0.75rem', color: 'var(--color-gray)', lineHeight: 1.6 }}>
          In production, M1 handles authentication and injects the JWT token. This placeholder is for M2 standalone development only.
        </p>
      </motion.div>
    </div>
  )
}
