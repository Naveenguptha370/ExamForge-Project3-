/** ExamForge M2 — Registration History Page */
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { HiOutlineSearch, HiOutlineClock } from 'react-icons/hi'
import registrationService from '../../services/registrationService.js'
import academicService from '../../services/academicService.js'
import { useDebounce } from '../../hooks/useDebounce.js'

export default function RegistrationHistory() {
  const [search, setSearch] = useState('')
  const [page, setPage]     = useState(1)
  const [acYear, setAcYear] = useState('')
  const [status, setStatus] = useState('')
  const db = useDebounce(search, 350)

  const { data, isLoading } = useQuery({
    queryKey: ['reg-history', page, db, acYear, status],
    queryFn: () => registrationService.subjects.list({
      page, search: db || undefined,
      academic_year: acYear || undefined,
      status: status || undefined,
    }).then(r => r.data),
    keepPreviousData: true,
  })

  const { data: years } = useQuery({
    queryKey: ['academic-years'],
    queryFn: () => academicService.years.list({ page_size: 50 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const records    = data?.results || []
  const pagination = data?.pagination || {}
  const total      = pagination.count || 0
  const totalPages = pagination.total_pages || 1

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="page-title"><HiOutlineClock size={22} color="var(--color-emerald)" /> Registration History</div>
          <div className="page-subtitle">Audit log of all registration actions — {total} records</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 'var(--space-4)', flexWrap: 'wrap' }}>
        <div className="search-bar" style={{ flex: 1, minWidth: 240 }}>
          <HiOutlineSearch className="search-icon" />
          <input className="form-input" placeholder="Search by student or subject…"
            value={search} onChange={e => { setSearch(e.target.value); setPage(1) }} />
        </div>
        <select className="form-select" style={{ maxWidth: 180 }} value={acYear} onChange={e => { setAcYear(e.target.value); setPage(1) }}>
          <option value="">All Academic Years</option>
          {(years || []).map(y => <option key={y.id} value={y.id}>{y.label}</option>)}
        </select>
        <select className="form-select" style={{ maxWidth: 160 }} value={status} onChange={e => { setStatus(e.target.value); setPage(1) }}>
          <option value="">All Statuses</option>
          <option value="registered">Registered</option>
          <option value="confirmed">Confirmed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>Student</th><th>Roll No.</th><th>Subject</th>
              <th>Semester</th><th>Academic Year</th>
              <th>Reg. Date</th><th>Registered By</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            {isLoading
              ? Array.from({ length: 8 }).map((_, i) => (
                  <tr key={i}>{Array.from({ length: 8 }).map((_, j) => <td key={j}><div className="skeleton skeleton-text" style={{ width: '70%' }} /></td>)}</tr>
                ))
              : records.length === 0
              ? <tr><td colSpan={8} style={{ textAlign: 'center', padding: '40px', color: 'var(--color-gray)' }}>No registration records found.</td></tr>
              : records.map(rec => (
                  <tr key={rec.id}>
                    <td style={{ fontWeight: 600 }}>{rec.student_name || '—'}</td>
                    <td><code style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{rec.student_roll || '—'}</code></td>
                    <td>
                      <div>{rec.subject_name}</div>
                      {rec.subject_code && <div className="td-muted">{rec.subject_code}</div>}
                    </td>
                    <td>{rec.semester_number ? `Sem ${rec.semester_number}` : '—'}</td>
                    <td className="td-muted">{rec.academic_year_label || '—'}</td>
                    <td className="td-muted">{rec.registration_date || '—'}</td>
                    <td className="td-muted">{rec.registered_by_username || '—'}</td>
                    <td>
                      <span className={`badge ${rec.status === 'registered' || rec.status === 'confirmed' ? 'badge-success' : rec.status === 'cancelled' ? 'badge-error' : 'badge-neutral'}`}>
                        {rec.status}
                      </span>
                    </td>
                  </tr>
                ))
            }
          </tbody>
        </table>

        {!isLoading && records.length > 0 && (
          <div className="pagination">
            <div className="pagination-info">Showing {((page - 1) * 20) + 1}–{Math.min(page * 20, total)} of {total}</div>
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
