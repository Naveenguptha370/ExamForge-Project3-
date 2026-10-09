/** ExamForge M2 — Confirm Dialog */
import { motion, AnimatePresence } from 'framer-motion'
import { HiOutlineExclamation, HiOutlineX } from 'react-icons/hi'

export default function ConfirmDialog({
  isOpen, onClose, onConfirm,
  title = 'Are you sure?',
  message = 'This action cannot be undone.',
  confirmLabel = 'Confirm',
  cancelLabel  = 'Cancel',
  variant = 'danger',
  loading = false,
  children,
}) {
  if (!isOpen) return null

  const colors = {
    danger:  { bg: '#FEE2E2', color: 'var(--color-error)', btn: 'btn-danger' },
    warning: { bg: 'var(--color-amber-100)', color: 'var(--color-amber-600)', btn: 'btn-amber' },
    success: { bg: 'var(--color-green-100)', color: 'var(--color-success)', btn: 'btn-primary' },
  }
  const c = colors[variant] || colors.danger

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="modal-overlay" onClick={onClose}>
          <motion.div
            className="confirm-dialog"
            onClick={e => e.stopPropagation()}
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
          >
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 8 }}>
              <button className="modal-close" onClick={onClose}>
                <HiOutlineX size={16} />
              </button>
            </div>

            <div className="confirm-icon" style={{ background: c.bg, color: c.color }}>
              <HiOutlineExclamation size={26} />
            </div>

            <h3 style={{ marginBottom: 8, fontSize: '1.0625rem' }}>{title}</h3>
            <p style={{ color: 'var(--color-gray)', fontSize: '0.875rem', marginBottom: 16, lineHeight: 1.6 }}>
              {message}
            </p>

            {children && (
              <div style={{ marginBottom: 16 }}>{children}</div>
            )}

            <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
              <button className="btn btn-secondary" onClick={onClose} disabled={loading}>
                {cancelLabel}
              </button>
              <button
                className={`btn ${c.btn}${loading ? ' btn-loading' : ''}`}
                onClick={onConfirm}
                disabled={loading}
              >
                {loading ? 'Processing…' : confirmLabel}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
