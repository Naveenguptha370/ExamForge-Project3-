/** ExamForge M2 — Registration List Page */
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { HiOutlineSearch, HiOutlineEye, HiOutlinePencilAlt, HiOutlineBookOpen } from 'react-icons/hi'
import registrationService from '../../services/registrationService.js'
import { useDebounce } from '../../hooks/useDebounce.js'

export default function RegistrationList() {
  const [tab, setTab]       = useState('subject')
  const [search, setSearch] = useState('')
  const [page, setPage]     = useState(1)
  const db = useDebounce(search, 350)

  const { data: subjData, isLoading: subjLoading } = useQuery({
    queryKey: ['subject-registrations', page, db],
    queryFn: () => registrationService.subjects.list({ page, search: db || undefined }).then(r => r.data),
    keepPreviousData: true,
    enabled: tab === 'subject',
  })

  const { data: examData, isLoading: examLoading } = useQuery({
    queryKey: ['exam-registrations', page, db],
    queryFn: () => registrationService.exams.list({ page, search: db || undefined }).then(r => r.data),
    keepPreviousData: true,
    enabled: tab === 'exam',
  })

  const activeData    = tab === 'subject' ? subjData : examData
  const isLoading     = tab === 'subject' ? subjLoading : examLoading
  const records       = activeData?.results || []
  const pagination    = activeData?.pagination || {}
  const total         = pagination.count || 0
  const totalPages    = pagination.total_pages || 1

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="page-title">All Registrations</div>
          <div className="page-subtitle">{total} records</div>
        </div>
        <div className="page-actions">
          <Link to="/registrations/subjects/register" className="btn btn-secondary btn-sm">
            <HiOutlineBookOpen size={15} /> Subject Reg.
          </Link>
          <Link to="/registrations/exams/register" className="btn btn-primary btn-sm">
            <HiOutlinePencilAlt size={15} /> Exam Reg.
          </Link>
        </div>
      </div>

      <div className="tab-bar" style={{ marginBottom: 'var(--space-4)' }}>
        <button className={`tab-btn${tab === 'subject' ? ' active' : ''}`} onClick={() => { setTab('subject'); setPage(1) }}>
          <HiOutlineBookOpen size={15} /> Subject Registrations
        </button>
        <button className={`tab-btn${tab === 'exam' ? ' active' : ''}`} onClick={() => { setTab('exam'); setPage(1) }}>
          <HiOutlinePencilAlt size={15} /> Exam Registrations
        </button>
      </div>

      <div style={{ marginBottom: 'var(--space-4)' }}>
        <div className="search-bar" style={{ maxWidth: 360 }}>
          <HiOutlineSearch className="search-icon" />
          <input className="form-input" placeholder="Search by student name or roll…"
            value={search} onChange={e => { setSearch(e.target.value); setPage(1) }} />
        </div>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>Student</th>
              <th>Roll Number</th>
              <th>Subject</th>
              <th>Semester</th>
              <th>Academic Year</th>
              <th>Reg. Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {isLoading
              ? Array.from({ length: 6 }).map((_, i) => (
                  <tr key={i}>
                    {Array.from({ length: 8 }).map((_, j) => (
                      <td key={j}><div className="skeleton skeleton-text" style={{ width: '70%' }} /></td>
                    ))}
                  </tr>
                ))
              : records.length === 0
              ? (
                  <tr>
                    <td colSpan={8} style={{ textAlign: 'center', padding: '40px 24px', color: 'var(--color-gray)' }}>
                      No {tab} registrations found.
                    </td>
                  </tr>
                )
              : records.map(rec => (
                  <tr key={rec.id}>
                    <td style={{ fontWeight: 600 }}>{rec.student_name || '—'}</td>
                    <td><code style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{rec.student_roll || '—'}</code></td>
                    <td>
                      <div style={{ fontWeight: 500 }}>{rec.subject_name || rec.subject_code}</div>
                      {rec.subject_code && <div className="td-muted">{rec.subject_code}</div>}
                    </td>
                    <td>{rec.semester_number ? `Sem ${rec.semester_number}` : '—'}</td>
                    <td className="td-muted">{rec.academic_year_label || '—'}</td>
                    <td className="td-muted">{rec.registration_date || '—'}</td>
                    <td>
                      <span className={`badge ${rec.status === 'registered' || rec.status === 'confirmed' ? 'badge-success' : rec.status === 'cancelled' ? 'badge-error' : 'badge-neutral'}`}>
                        {rec.status}
                      </span>
                    </td>
                    <td>
                      <Link to={`/registrations/${rec.id}`} className="btn btn-icon btn-secondary btn-sm" title="View">
                        <HiOutlineEye size={14} />
                      </Link>
                    </td>
                  </tr>
                ))
            }
          </tbody>
        </table>

        {!isLoading && records.length > 0 && (
          <div className="pagination">
            <div className="pagination-info">Showing page {page} of {totalPages} · {total} total</div>
            <div className="pagination-controls">
              <button className="page-btn" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>‹</button>
              {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => i + 1).map(p => (
                <button key={p} className={`page-btn${page === p ? ' active' : ''}`} onClick={() => setPage(p)}>{p}</button>
              ))}
              <button className="page-btn" disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>›</button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
