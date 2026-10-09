/** ExamForge M2 — Enrollment Overview Page */
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { HiOutlineClipboardList, HiOutlineSearch } from 'react-icons/hi'
import studentService from '../../services/studentService.js'
import academicService from '../../services/academicService.js'
import { useDebounce } from '../../hooks/useDebounce.js'

export default function EnrollmentOverview() {
  const [search, setSearch] = useState('')
  const [page, setPage]     = useState(1)
  const [acYear, setAcYear] = useState('')
  const db = useDebounce(search, 350)

  const { data, isLoading } = useQuery({
    queryKey: ['enrollments', page, db, acYear],
    queryFn: () => studentService.listEnrollments({
      page, student_roll: db || undefined, academic_year: acYear || undefined,
    }).then(r => r.data),
    keepPreviousData: true,
  })

  const { data: yearsData } = useQuery({
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
          <div className="page-title">
            <HiOutlineClipboardList size={22} color="var(--color-emerald)" />
            Enrollment Records
          </div>
          <div className="page-subtitle">{total} records found</div>
        </div>
      </div>

      {/* Toolbar */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 'var(--space-4)', flexWrap: 'wrap' }}>
        <div className="search-bar" style={{ flex: 1, minWidth: 240 }}>
          <HiOutlineSearch className="search-icon" />
          <input
            className="form-input"
            placeholder="Search by roll number or name…"
            value={search}
            onChange={e => { setSearch(e.target.value); setPage(1) }}
          />
        </div>
        <select
          className="form-select"
          style={{ maxWidth: 200 }}
          value={acYear}
          onChange={e => { setAcYear(e.target.value); setPage(1) }}
        >
          <option value="">All Academic Years</option>
          {(yearsData || []).map(y => (
            <option key={y.id} value={y.id}>{y.label}</option>
          ))}
        </select>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>Student</th>
              <th>Roll Number</th>
              <th>Semester</th>
              <th>Academic Year</th>
              <th>Status</th>
              <th>Enrolled Date</th>
            </tr>
          </thead>
          <tbody>
            {isLoading
              ? Array.from({ length: 6 }).map((_, i) => (
                  <tr key={i}>
                    {Array.from({ length: 6 }).map((_, j) => (
                      <td key={j}><div className="skeleton skeleton-text" style={{ width: '75%' }} /></td>
                    ))}
                  </tr>
                ))
              : records.length === 0
              ? (
                  <tr>
                    <td colSpan={6} style={{ textAlign: 'center', padding: '40px 0', color: 'var(--color-gray)' }}>
                      No enrollment records found
                    </td>
                  </tr>
                )
              : records.map(rec => (
                  <tr key={rec.id}>
                    <td style={{ fontWeight: 600 }}>{rec.student_name}</td>
                    <td><code style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{rec.student_roll}</code></td>
                    <td>{rec.semester_display}</td>
                    <td>{rec.academic_year_label}</td>
                    <td><span className="badge badge-success">{rec.status_display || rec.status}</span></td>
                    <td className="td-muted">{rec.enrolled_date || '—'}</td>
                  </tr>
                ))
            }
          </tbody>
        </table>

        {!isLoading && records.length > 0 && (
          <div className="pagination">
            <div className="pagination-info">
              Showing {((page - 1) * 20) + 1}–{Math.min(page * 20, total)} of {total}
            </div>
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
