/**
 * ExamForge M2 — Student List Page
 * Full CRUD table with search, filters, pagination, bulk actions.
 */

import { useState, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  HiOutlineSearch, HiOutlineFunnel, HiOutlineUserAdd,
  HiOutlinePencil, HiOutlineEye, HiOutlineTrash,
  HiOutlineChevronDown, HiOutlineDownload, HiOutlineRefresh,
  HiOutlineCheckCircle, HiOutlineXCircle,
} from 'react-icons/hi'
import toast from 'react-hot-toast'

import studentService   from '../../services/studentService.js'
import academicService  from '../../services/academicService.js'
import ConfirmDialog    from '../../components/shared/ConfirmDialog.jsx'
import { useAuth }      from '../../context/AuthContext.jsx'
import { useDebounce }  from '../../hooks/useDebounce.js'

const STATUS_BADGE = {
  active:    { label: 'Active',    cls: 'badge-success' },
  inactive:  { label: 'Inactive',  cls: 'badge-neutral' },
  graduated: { label: 'Graduated', cls: 'badge-forest'  },
  suspended: { label: 'Suspended', cls: 'badge-warning' },
  withdrawn: { label: 'Withdrawn', cls: 'badge-error'   },
  detained:  { label: 'Detained',  cls: 'badge-warning' },
}

export default function StudentList() {
  const { isAdmin, isExamStaff } = useAuth()
  const navigate    = useNavigate()
  const qc          = useQueryClient()

  const [search, setSearch]         = useState('')
  const [page, setPage]             = useState(1)
  const [pageSize]                  = useState(20)
  const [filters, setFilters]       = useState({})
  const [showFilters, setShowFilters] = useState(false)
  const [selected, setSelected]     = useState(new Set())
  const [deleteTarget, setDeleteTarget] = useState(null)

  const debouncedSearch = useDebounce(search, 350)

  const { data, isLoading, isFetching } = useQuery({
    queryKey: ['students', page, pageSize, debouncedSearch, filters],
    queryFn: () => studentService.list({
      page, page_size: pageSize,
      search: debouncedSearch || undefined,
      ...filters,
    }).then(r => r.data),
    keepPreviousData: true,
  })

  const { data: deptsData } = useQuery({
    queryKey: ['departments-list'],
    queryFn: () => academicService.departments.list({ status: 'active', page_size: 100 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const deleteMutation = useMutation({
    mutationFn: ({ id, reason }) => studentService.delete(id, reason),
    onSuccess: () => {
      toast.success('Student removed successfully.')
      qc.invalidateQueries(['students'])
      qc.invalidateQueries(['student-dashboard'])
      setDeleteTarget(null)
    },
    onError: (err) => {
      const msg = err.response?.data?.message || 'Failed to remove student.'
      toast.error(msg)
    },
  })

  const students    = data?.results || []
  const pagination  = data?.pagination || {}
  const totalPages  = pagination.total_pages || 1

  /* ── Selection helpers ───────────────────────────────── */
  const toggleSelect = (id) => {
    setSelected(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }
  const toggleAll = () => {
    if (selected.size === students.length) setSelected(new Set())
    else setSelected(new Set(students.map(s => s.id)))
  }

  /* ── Filter helpers ───────────────────────────────────── */
  const applyFilter = (key, val) =>
    setFilters(prev => ({ ...prev, [key]: val || undefined }))

  const clearFilters = () => { setFilters({}); setSearch('') }

  const hasFilters = Object.keys(filters).length > 0 || search

  return (
    <div>
      {/* ── Page header ─────────────────────────────── */}
      <div className="page-header">
        <div>
          <div className="page-title">All Students</div>
          <div className="page-subtitle">
            {pagination.count ?? '…'} student records
            {isFetching && !isLoading && (
              <span style={{ marginLeft: 8, color: 'var(--color-emerald)', fontSize: '0.75rem' }}>
                refreshing…
              </span>
            )}
          </div>
        </div>
        <div className="page-actions">
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => qc.invalidateQueries(['students'])}
            title="Refresh"
          >
            <HiOutlineRefresh size={16} />
          </button>
          {(isAdmin || isExamStaff) && (
            <>
              <Link to="/students/import" className="btn btn-secondary btn-sm">
                <HiOutlineDownload size={15} /> Import
              </Link>
              <Link to="/students/add" className="btn btn-primary btn-sm">
                <HiOutlineUserAdd size={15} /> Add Student
              </Link>
            </>
          )}
        </div>
      </div>

      {/* ── Toolbar ─────────────────────────────────── */}
      <div style={{
        display: 'flex', gap: 'var(--space-3)', alignItems: 'center',
        marginBottom: 'var(--space-4)', flexWrap: 'wrap',
      }}>
        {/* Search */}
        <div className="search-bar" style={{ flex: 1, minWidth: 240 }}>
          <HiOutlineSearch className="search-icon" />
          <input
            className="form-input"
            placeholder="Search by name, roll number, email…"
            value={search}
            onChange={e => { setSearch(e.target.value); setPage(1) }}
          />
        </div>

        {/* Filter toggle */}
        <button
          className={`btn btn-secondary btn-sm${showFilters ? ' btn-outline' : ''}`}
          onClick={() => setShowFilters(o => !o)}
          style={{ borderColor: showFilters ? 'var(--color-emerald)' : undefined }}
        >
          <HiOutlineFunnel size={15} />
          Filters
          {hasFilters && (
            <span style={{
              background: 'var(--color-emerald)', color: 'white',
              borderRadius: 'var(--radius-full)', padding: '1px 6px', fontSize: '0.7rem',
            }}>
              {Object.keys(filters).length + (search ? 1 : 0)}
            </span>
          )}
          <HiOutlineChevronDown
            size={13}
            style={{ transform: showFilters ? 'rotate(180deg)' : 'none', transition: '0.15s' }}
          />
        </button>

        {hasFilters && (
          <button className="btn btn-secondary btn-sm" onClick={clearFilters}>
            Clear filters
          </button>
        )}
      </div>

      {/* ── Filter panel ────────────────────────────── */}
      {showFilters && (
        <motion.div
          initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
          exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }}
          className="filter-panel"
        >
          <div className="filter-grid">
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Department</label>
              <select
                className="form-select"
                value={filters.department || ''}
                onChange={e => { applyFilter('department', e.target.value); setPage(1) }}
              >
                <option value="">All Departments</option>
                {(deptsData || []).map(d => (
                  <option key={d.id} value={d.id}>{d.code} — {d.name}</option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Status</label>
              <select
                className="form-select"
                value={filters.status || ''}
                onChange={e => { applyFilter('status', e.target.value); setPage(1) }}
              >
                <option value="">All Statuses</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="graduated">Graduated</option>
                <option value="suspended">Suspended</option>
                <option value="withdrawn">Withdrawn</option>
              </select>
            </div>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Exam Eligible</label>
              <select
                className="form-select"
                value={filters.is_eligible_for_exam ?? ''}
                onChange={e => { applyFilter('is_eligible_for_exam', e.target.value); setPage(1) }}
              >
                <option value="">All</option>
                <option value="true">Eligible Only</option>
                <option value="false">Ineligible Only</option>
              </select>
            </div>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Admission Year</label>
              <input
                className="form-input"
                type="number"
                min="2000" max="2100"
                placeholder="e.g. 2023"
                value={filters.admission_year || ''}
                onChange={e => { applyFilter('admission_year', e.target.value); setPage(1) }}
              />
            </div>
          </div>
        </motion.div>
      )}

      {/* ── Bulk action bar ──────────────────────────── */}
      {selected.size > 0 && (isAdmin || isExamStaff) && (
        <motion.div
          initial={{ y: -10, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
          style={{
            background: 'var(--color-sage)', border: '1px solid var(--color-emerald)',
            borderRadius: 'var(--radius-md)', padding: '10px 16px',
            display: 'flex', alignItems: 'center', gap: 12,
            marginBottom: 'var(--space-3)',
          }}
        >
          <span style={{ fontWeight: 600, fontSize: '0.875rem', color: 'var(--color-forest)' }}>
            {selected.size} selected
          </span>
          <button
            className="btn btn-sm btn-secondary"
            onClick={() => setSelected(new Set())}
          >
            Clear selection
          </button>
        </motion.div>
      )}

      {/* ── Table ───────────────────────────────────── */}
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {(isAdmin || isExamStaff) && (
                <th style={{ width: 44, textAlign: 'center' }}>
                  <input
                    type="checkbox"
                    checked={selected.size === students.length && students.length > 0}
                    onChange={toggleAll}
                    style={{ accentColor: 'var(--color-emerald)' }}
                  />
                </th>
              )}
              <th>Roll No.</th>
              <th>Student Name</th>
              <th>Department</th>
              <th>Course / Branch</th>
              <th>Semester</th>
              <th>Year</th>
              <th>Status</th>
              <th>Eligible</th>
              <th style={{ textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {isLoading
              ? Array.from({ length: 8 }).map((_, i) => (
                  <tr key={i}>
                    {Array.from({ length: 10 }).map((_, j) => (
                      <td key={j}>
                        <div className="skeleton skeleton-text" style={{ width: '80%' }} />
                      </td>
                    ))}
                  </tr>
                ))
              : students.length === 0
              ? (
                  <tr>
                    <td colSpan={10} style={{ textAlign: 'center', padding: '48px 24px' }}>
                      <div className="empty-state-icon" style={{ margin: '0 auto 12px', width: 56, height: 56, fontSize: '1.5rem' }}>👤</div>
                      <div className="empty-state-title">No students found</div>
                      <div className="empty-state-text" style={{ marginTop: 6 }}>
                        {hasFilters ? 'Try adjusting your filters.' : 'Get started by adding your first student.'}
                      </div>
                    </td>
                  </tr>
                )
              : students.map(student => {
                  const badge = STATUS_BADGE[student.status] || { label: student.status, cls: 'badge-neutral' }
                  const isSelected = selected.has(student.id)
                  return (
                    <tr
                      key={student.id}
                      style={{ background: isSelected ? 'var(--color-sage-light)' : undefined }}
                    >
                      {(isAdmin || isExamStaff) && (
                        <td style={{ textAlign: 'center' }}>
                          <input
                            type="checkbox"
                            checked={isSelected}
                            onChange={() => toggleSelect(student.id)}
                            style={{ accentColor: 'var(--color-emerald)' }}
                          />
                        </td>
                      )}
                      <td>
                        <span style={{ fontWeight: 600, fontFamily: 'monospace', fontSize: '0.8rem' }}>
                          {student.roll_number}
                        </span>
                      </td>
                      <td>
                        <div style={{ fontWeight: 600 }}>{student.full_name}</div>
                        <div className="td-muted">{student.institutional_email}</div>
                      </td>
                      <td>
                        <span className="badge badge-forest">{student.department_code}</span>
                      </td>
                      <td>
                        <div style={{ fontSize: '0.8125rem' }}>{student.course_code}</div>
                        {student.branch_code && (
                          <div className="td-muted">{student.branch_code}</div>
                        )}
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <span style={{ fontWeight: 600 }}>Sem {student.semester_number}</span>
                      </td>
                      <td className="td-muted">{student.academic_year_label}</td>
                      <td>
                        <span className={`badge ${badge.cls}`}>{badge.label}</span>
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        {student.is_eligible_for_exam
                          ? <HiOutlineCheckCircle size={18} color="var(--color-success)" />
                          : <HiOutlineXCircle    size={18} color="var(--color-error)" />
                        }
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: 6, justifyContent: 'flex-end' }}>
                          <button
                            className="btn btn-icon btn-secondary btn-sm"
                            title="View details"
                            onClick={() => navigate(`/students/${student.id}`)}
                          >
                            <HiOutlineEye size={15} />
                          </button>
                          {(isAdmin || isExamStaff) && (
                            <>
                              <button
                                className="btn btn-icon btn-secondary btn-sm"
                                title="Edit"
                                onClick={() => navigate(`/students/${student.id}/edit`)}
                              >
                                <HiOutlinePencil size={15} />
                              </button>
                              <button
                                className="btn btn-icon btn-sm"
                                title="Remove"
                                onClick={() => setDeleteTarget(student)}
                                style={{
                                  background: '#FEE2E2', color: 'var(--color-error)',
                                  border: '1px solid #FECACA',
                                }}
                              >
                                <HiOutlineTrash size={15} />
                              </button>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  )
                })
            }
          </tbody>
        </table>

        {/* ── Pagination ───────────────────────────── */}
        {!isLoading && students.length > 0 && (
          <div className="pagination">
            <div className="pagination-info">
              Showing {((page - 1) * pageSize) + 1}–{Math.min(page * pageSize, pagination.count || 0)} of{' '}
              {(pagination.count || 0).toLocaleString()} students
            </div>
            <div className="pagination-controls">
              <button
                className="page-btn" disabled={page <= 1}
                onClick={() => setPage(p => p - 1)}
              >‹</button>
              {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
                const p = i + 1
                return (
                  <button
                    key={p}
                    className={`page-btn${page === p ? ' active' : ''}`}
                    onClick={() => setPage(p)}
                  >{p}</button>
                )
              })}
              {totalPages > 7 && (
                <span style={{ padding: '0 4px', color: 'var(--color-gray)' }}>…</span>
              )}
              <button
                className="page-btn" disabled={page >= totalPages}
                onClick={() => setPage(p => p + 1)}
              >›</button>
            </div>
          </div>
        )}
      </div>

      {/* ── Delete confirmation ──────────────────────── */}
      <ConfirmDialog
        isOpen={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={() => deleteMutation.mutate({ id: deleteTarget.id, reason: 'Removed by administrator.' })}
        title="Remove Student"
        message={`Remove "${deleteTarget?.full_name}" (${deleteTarget?.roll_number})? If they have registration records, they will be deactivated instead of permanently deleted.`}
        confirmLabel="Remove"
        loading={deleteMutation.isLoading}
        variant="danger"
      />
    </div>
  )
}
