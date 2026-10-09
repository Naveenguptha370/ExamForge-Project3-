/** ExamForge M2 — Registration Details */
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { HiOutlineChevronLeft, HiOutlineX } from 'react-icons/hi'
import toast from 'react-hot-toast'
import registrationService from '../../services/registrationService.js'

function InfoRow({ label, value }) {
  return (
    <div style={{ display: 'flex', gap: 12, padding: '10px 0', borderBottom: '1px solid var(--color-border)' }}>
      <span style={{ minWidth: 180, fontSize: '0.8125rem', color: 'var(--color-gray)', fontWeight: 500 }}>{label}</span>
      <span style={{ fontSize: '0.875rem', color: 'var(--color-charcoal)', fontWeight: 500 }}>{value || '—'}</span>
    </div>
  )
}

export default function RegistrationDetails() {
  const { id } = useParams()
  const qc = useQueryClient()

  const { data: reg, isLoading } = useQuery({
    queryKey: ['registration-detail', id],
    queryFn: () => registrationService.subjects.get(id).then(r => r.data),
  })

  const cancelMutation = useMutation({
    mutationFn: () => registrationService.subjects.cancel(id, 'Cancelled by staff'),
    onSuccess: () => {
      toast.success('Registration cancelled.')
      qc.invalidateQueries(['registration-detail', id])
      qc.invalidateQueries(['subject-registrations'])
    },
    onError: (err) => toast.error(err.response?.data?.message || 'Cancellation failed.'),
  })

  if (isLoading) return <div className="skeleton" style={{ height: 400, borderRadius: 14 }} />

  const r = reg || {}
  const statusColors = { registered: 'badge-success', confirmed: 'badge-forest', cancelled: 'badge-error', pending: 'badge-neutral' }

  return (
    <div>
      <div className="page-header">
        <div>
          <Link to="/registrations/list" className="btn btn-secondary btn-sm" style={{ marginBottom: 8 }}>
            <HiOutlineChevronLeft size={14} /> Back
          </Link>
          <div className="page-title">Registration #{id}</div>
          <div className="page-subtitle">Subject registration detail view</div>
        </div>
        <div className="page-actions">
          {r.status !== 'cancelled' && (
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => cancelMutation.mutate()}
              disabled={cancelMutation.isLoading}
            >
              <HiOutlineX size={14} /> {cancelMutation.isLoading ? 'Cancelling…' : 'Cancel Registration'}
            </button>
          )}
        </div>
      </div>

      <motion.div className="card" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-5)' }}>
          <h3 style={{ margin: 0 }}>Registration Information</h3>
          <span className={`badge ${statusColors[r.status] || 'badge-neutral'}`} style={{ fontSize: '0.875rem', padding: '4px 12px' }}>
            {r.status_display || r.status}
          </span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-6)' }}>
          <div>
            <h4 style={{ marginBottom: 12, color: 'var(--color-forest)' }}>Student Information</h4>
            <InfoRow label="Student Name"  value={r.student_name} />
            <InfoRow label="Roll Number"   value={r.student_roll} />
            <InfoRow label="Department"    value={r.department_code} />
            <InfoRow label="Course"        value={r.course_code} />
          </div>
          <div>
            <h4 style={{ marginBottom: 12, color: 'var(--color-forest)' }}>Subject Information</h4>
            <InfoRow label="Subject Code"     value={r.subject_code} />
            <InfoRow label="Subject Name"     value={r.subject_name} />
            <InfoRow label="Semester"         value={r.semester_number ? `Semester ${r.semester_number}` : '—'} />
            <InfoRow label="Academic Year"    value={r.academic_year_label} />
            <InfoRow label="Registration Date" value={r.registration_date} />
            <InfoRow label="Registered By"    value={r.registered_by_username} />
          </div>
        </div>
        {r.remarks && (
          <div style={{ marginTop: 'var(--space-4)', padding: 'var(--space-3)', background: 'var(--color-bg)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.8125rem', fontWeight: 600, marginBottom: 4, color: 'var(--color-forest)' }}>Remarks</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--color-charcoal)' }}>{r.remarks}</div>
          </div>
        )}
      </motion.div>
    </div>
  )
}
