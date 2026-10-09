/**
 * ExamForge M2 — Student Detail Page
 * Full profile view with tabs for registrations, enrollment history.
 */
import { useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  HiOutlineChevronLeft, HiOutlinePencil, HiOutlineCheckCircle,
  HiOutlineXCircle, HiOutlineUser, HiOutlineAcademicCap,
  HiOutlineClipboardList, HiOutlineMail, HiOutlinePhone,
} from 'react-icons/hi'
import toast from 'react-hot-toast'
import studentService from '../../services/studentService.js'
import { useAuth } from '../../context/AuthContext.jsx'

const STATUS_BADGE = {
  active:    'badge-success',
  inactive:  'badge-neutral',
  graduated: 'badge-forest',
  suspended: 'badge-warning',
  withdrawn: 'badge-error',
}

function InfoRow({ label, value }) {
  return (
    <div style={{
      display: 'flex', gap: 12, padding: '10px 0',
      borderBottom: '1px solid var(--color-border)',
    }}>
      <span style={{ minWidth: 160, fontSize: '0.8125rem', color: 'var(--color-gray)', fontWeight: 500 }}>
        {label}
      </span>
      <span style={{ fontSize: '0.875rem', color: 'var(--color-charcoal)', fontWeight: 500 }}>
        {value || '—'}
      </span>
    </div>
  )
}

export default function StudentDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isAdmin, isExamStaff } = useAuth()
  const qc = useQueryClient()
  const [tab, setTab] = useState('profile')

  const { data: summary, isLoading } = useQuery({
    queryKey: ['student-summary', id],
    queryFn: () => studentService.summary(id).then(r => r.data.data),
  })

  const { data: regsData } = useQuery({
    queryKey: ['student-registrations', id],
    queryFn: () => studentService.registrations(id).then(r => r.data.data),
    enabled: tab === 'registrations',
  })

  const activateMutation = useMutation({
    mutationFn: () => studentService.activate(id),
    onSuccess: () => { toast.success('Student activated.'); qc.invalidateQueries(['student-summary', id]) },
  })

  const deactivateMutation = useMutation({
    mutationFn: () => studentService.deactivate(id, 'Deactivated by administrator.'),
    onSuccess: () => { toast.success('Student deactivated.'); qc.invalidateQueries(['student-summary', id]) },
  })

  if (isLoading) {
    return (
      <div>
        <div className="skeleton" style={{ height: 200, borderRadius: 14, marginBottom: 16 }} />
        <div className="skeleton" style={{ height: 400, borderRadius: 14 }} />
      </div>
    )
  }

  const s = summary || {}
  const statusCls = STATUS_BADGE[s.status] || 'badge-neutral'

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div>
          <Link to="/students/list" className="btn btn-secondary btn-sm" style={{ marginBottom: 8 }}>
            <HiOutlineChevronLeft size={14} /> Back
          </Link>
          <div className="page-title">
            <HiOutlineUser size={22} color="var(--color-emerald)" />
            {s.full_name || 'Student'}
          </div>
          <div className="page-subtitle">{s.roll_number} · {s.student_id}</div>
        </div>
        <div className="page-actions">
          {(isAdmin || isExamStaff) && (
            <>
              {s.status === 'active' ? (
                <button className="btn btn-secondary btn-sm"
                  onClick={() => deactivateMutation.mutate()}
                  disabled={deactivateMutation.isLoading}
                >
                  <HiOutlineXCircle size={15} /> Deactivate
                </button>
              ) : (
                <button className="btn btn-secondary btn-sm"
                  onClick={() => activateMutation.mutate()}
                  disabled={activateMutation.isLoading}
                >
                  <HiOutlineCheckCircle size={15} /> Activate
                </button>
              )}
              <Link to={`/students/${id}/edit`} className="btn btn-primary btn-sm">
                <HiOutlinePencil size={14} /> Edit
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Profile banner */}
      <motion.div
        initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
        className="card"
        style={{ marginBottom: 'var(--space-4)', background: 'linear-gradient(135deg, var(--color-forest) 0%, var(--color-emerald) 100%)' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
          <div style={{
            width: 72, height: 72, borderRadius: '50%',
            background: 'rgba(255,255,255,0.2)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '1.75rem', fontWeight: 800, color: 'white',
            border: '3px solid rgba(255,255,255,0.4)',
          }}>
            {s.full_name?.[0] || '?'}
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ color: 'white', fontWeight: 800, fontSize: '1.25rem', marginBottom: 4 }}>
              {s.full_name}
            </div>
            <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: '0.875rem', display: 'flex', gap: 16, flexWrap: 'wrap' }}>
              <span><HiOutlineMail size={13} style={{ verticalAlign: 'middle' }} /> {s.institutional_email}</span>
              {s.phone && <span><HiOutlinePhone size={13} style={{ verticalAlign: 'middle' }} /> {s.phone}</span>}
            </div>
          </div>
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <span className={`badge ${statusCls}`}>{s.status_display || s.status}</span>
            {s.is_eligible_for_exam && (
              <span className="badge badge-amber">Exam Eligible</span>
            )}
          </div>
        </div>

        {/* Quick stats */}
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
          gap: 16, marginTop: 20,
        }}>
          {[
            { label: 'Department',  value: s.department_code || '—' },
            { label: 'Course',      value: s.course_code || '—' },
            { label: 'Semester',    value: s.semester_number ? `Sem ${s.semester_number}` : '—' },
            { label: 'Year',        value: s.academic_year_label || '—' },
          ].map(stat => (
            <div key={stat.label} style={{
              background: 'rgba(255,255,255,0.12)', borderRadius: 10, padding: '10px 14px',
            }}>
              <div style={{ color: 'rgba(255,255,255,0.65)', fontSize: '0.7rem', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 3 }}>
                {stat.label}
              </div>
              <div style={{ color: 'white', fontWeight: 700 }}>{stat.value}</div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Tabs */}
      <div className="tab-bar">
        {[
          { id: 'profile', label: 'Profile', icon: HiOutlineUser },
          { id: 'academic', label: 'Academic', icon: HiOutlineAcademicCap },
          { id: 'registrations', label: `Registrations (${s.subject_registrations_count || 0})`, icon: HiOutlineClipboardList },
        ].map(t => (
          <button
            key={t.id}
            className={`tab-btn${tab === t.id ? ' active' : ''}`}
            onClick={() => setTab(t.id)}
          >
            <t.icon size={15} /> {t.label}
          </button>
        ))}
      </div>

      {/* Tab panels */}
      <div className="card">
        {tab === 'profile' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-6)' }}>
            <div>
              <h4 style={{ marginBottom: 12, color: 'var(--color-forest)' }}>Personal Information</h4>
              <InfoRow label="Student ID"    value={s.student_id} />
              <InfoRow label="Roll Number"   value={s.roll_number} />
              <InfoRow label="Full Name"     value={s.full_name} />
              <InfoRow label="Gender"        value={s.gender_display} />
              <InfoRow label="Date of Birth" value={s.date_of_birth} />
              <InfoRow label="Blood Group"   value={s.blood_group_display} />
              <InfoRow label="Address"       value={s.address} />
            </div>
            <div>
              <h4 style={{ marginBottom: 12, color: 'var(--color-forest)' }}>Contact & Guardian</h4>
              <InfoRow label="Institutional Email" value={s.institutional_email} />
              <InfoRow label="Personal Email"      value={s.personal_email} />
              <InfoRow label="Phone"               value={s.phone} />
              <InfoRow label="Alternate Phone"     value={s.alternate_phone} />
              <InfoRow label="Guardian Name"       value={s.guardian_name} />
              <InfoRow label="Guardian Phone"      value={s.guardian_phone} />
            </div>
          </div>
        )}

        {tab === 'academic' && (
          <div>
            <h4 style={{ marginBottom: 12, color: 'var(--color-forest)' }}>Academic Placement</h4>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-6)' }}>
              <div>
                <InfoRow label="Department"      value={`${s.department_code} — ${s.department_name || ''}`} />
                <InfoRow label="Course"          value={`${s.course_code} — ${s.course_name || ''}`} />
                <InfoRow label="Branch"          value={s.branch_code ? `${s.branch_code} — ${s.branch_name || ''}` : 'Common / No Branch'} />
                <InfoRow label="Semester"        value={s.semester_number ? `Semester ${s.semester_number}` : '—'} />
                <InfoRow label="Academic Year"   value={s.academic_year_label} />
              </div>
              <div>
                <InfoRow label="Admission Year"  value={s.admission_year} />
                <InfoRow label="Enrollment Date" value={s.enrollment_date} />
                <InfoRow label="Status"          value={s.status_display} />
                <InfoRow label="Exam Eligibility" value={s.exam_eligibility?.eligible ? '✅ Eligible' : `❌ ${s.exam_eligibility?.reason || 'Not eligible'}`} />
                <InfoRow label="Remarks"         value={s.remarks} />
              </div>
            </div>

            {/* Enrollment history */}
            {s.enrollment_history?.length > 0 && (
              <div style={{ marginTop: 'var(--space-5)' }}>
                <h4 style={{ marginBottom: 12, color: 'var(--color-forest)' }}>Enrollment History</h4>
                <div className="table-wrapper">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Semester</th>
                        <th>Academic Year</th>
                        <th>Status</th>
                        <th>Enrolled Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {s.enrollment_history.map((rec, i) => (
                        <tr key={i}>
                          <td>Sem {rec['semester__semester_number']}</td>
                          <td>{rec['academic_year__label']}</td>
                          <td><span className="badge badge-success">{rec.status}</span></td>
                          <td>{rec.enrolled_date || '—'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {tab === 'registrations' && (
          <div>
            <h4 style={{ marginBottom: 12, color: 'var(--color-forest)' }}>
              Subject Registrations ({s.subject_registrations_count || 0})
            </h4>
            {!regsData ? (
              <div className="skeleton" style={{ height: 200, borderRadius: 8 }} />
            ) : regsData.subject_registrations?.length === 0 ? (
              <div className="empty-state" style={{ padding: '32px 0' }}>
                <div className="empty-state-text">No subject registrations yet.</div>
              </div>
            ) : (
              <div className="table-wrapper" style={{ marginBottom: 'var(--space-5)' }}>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Subject Code</th><th>Subject Name</th>
                      <th>Semester</th><th>Year</th><th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(regsData?.subject_registrations || []).map((r, i) => (
                      <tr key={i}>
                        <td><code style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{r.subject_code}</code></td>
                        <td>{r.subject_name}</td>
                        <td>Sem {r.semester_number}</td>
                        <td>{r.academic_year_label}</td>
                        <td><span className="badge badge-success">{r.status}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            <h4 style={{ marginBottom: 12, color: 'var(--color-forest)' }}>
              Exam Registrations ({s.exam_registrations_count || 0})
            </h4>
            {!regsData ? null : regsData.exam_registrations?.length === 0 ? (
              <div className="empty-state" style={{ padding: '24px 0' }}>
                <div className="empty-state-text">No exam registrations yet.</div>
              </div>
            ) : (
              <div className="table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Subject Code</th><th>Subject Name</th>
                      <th>Session</th><th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(regsData?.exam_registrations || []).map((r, i) => (
                      <tr key={i}>
                        <td><code style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{r.subject_code}</code></td>
                        <td>{r.subject_name}</td>
                        <td>{r.exam_session || '—'}</td>
                        <td><span className="badge badge-forest">{r.status}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
