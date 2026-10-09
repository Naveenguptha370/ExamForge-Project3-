/**
 * ExamForge M2 — Generic Academic CRUD Page Factory
 * Shared template used by Department, Course, Branch, Semester, Subject, AcademicYear pages.
 * Each page imports this and passes its configuration.
 */
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import {
  HiOutlineSearch, HiOutlinePlus, HiOutlinePencil,
  HiOutlineTrash, HiOutlineRefresh, HiOutlineArchive,
} from 'react-icons/hi'
import toast from 'react-hot-toast'
import ConfirmDialog from '../../components/shared/ConfirmDialog.jsx'
import { useAuth } from '../../context/AuthContext.jsx'
import { useDebounce } from '../../hooks/useDebounce.js'

/**
 * AcademicCrudPage — generic CRUD page
 * @param {string}   title        - Page title
 * @param {string}   subtitle     - Page subtitle
 * @param {Function} queryFn      - async fn that fetches list (receives params)
 * @param {Function} deleteFn     - async fn(id) for deletion
 * @param {Function} archiveFn    - optional async fn(id) for archive
 * @param {string}   queryKey     - React Query key prefix
 * @param {Array}    columns      - Table column definitions [{key, label, render?}]
 * @param {Function} FormModal    - Modal component for create/edit ({open, onClose, initialData, onSaved})
 * @param {string}   entityName   - Singular name of entity for toast messages
 * @param {boolean}  searchable   - Whether to show search bar
 * @param {Array}    extraFilters - Extra filter controls
 */
export default function AcademicCrudPage({
  title, subtitle, queryFn, deleteFn, archiveFn,
  queryKey, columns, FormModal, entityName = 'record',
  searchable = true, extraFilters = [],
}) {
  const { isAdmin, isExamStaff } = useAuth()
  const qc = useQueryClient()
  const canWrite = isAdmin || isExamStaff

  const [search, setSearch]     = useState('')
  const [page, setPage]         = useState(1)
  const [filters, setFilters]   = useState({})
  const [modalOpen, setModalOpen] = useState(false)
  const [editTarget, setEditTarget] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const db = useDebounce(search, 350)

  const params = { page, search: db || undefined, ...filters }

  const { data, isLoading, isFetching } = useQuery({
    queryKey: [queryKey, page, db, filters],
    queryFn: () => queryFn(params).then(r => r.data),
    keepPreviousData: true,
  })

  const deleteMutation = useMutation({
    mutationFn: (id) => deleteFn(id),
    onSuccess: () => {
      toast.success(`${entityName} deleted successfully.`)
      qc.invalidateQueries([queryKey])
      setDeleteTarget(null)
    },
    onError: (err) => {
      toast.error(err.response?.data?.message || `Failed to delete ${entityName}.`)
      setDeleteTarget(null)
    },
  })

  const archiveMutation = useMutation({
    mutationFn: (id) => archiveFn(id),
    onSuccess: () => { toast.success(`${entityName} archived.`); qc.invalidateQueries([queryKey]) },
    onError: (err) => toast.error(err.response?.data?.message || `Failed to archive.`),
  })

  const records    = data?.results || []
  const pagination = data?.pagination || {}
  const total      = pagination.count || 0
  const totalPages = pagination.total_pages || 1

  const openCreate = () => { setEditTarget(null); setModalOpen(true) }
  const openEdit   = (rec) => { setEditTarget(rec); setModalOpen(true) }
  const closeModal = () => { setModalOpen(false); setEditTarget(null) }
  const onSaved    = () => { qc.invalidateQueries([queryKey]); closeModal() }

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div>
          <div className="page-title">{title}</div>
          <div className="page-subtitle">
            {total} records
            {isFetching && !isLoading && (
              <span style={{ marginLeft: 8, color: 'var(--color-emerald)', fontSize: '0.75rem' }}>refreshing…</span>
            )}
          </div>
        </div>
        <div className="page-actions">
          <button className="btn btn-secondary btn-sm" onClick={() => qc.invalidateQueries([queryKey])}>
            <HiOutlineRefresh size={15} />
          </button>
          {canWrite && (
            <button className="btn btn-primary btn-sm" onClick={openCreate}>
              <HiOutlinePlus size={15} /> Add {entityName}
            </button>
          )}
        </div>
      </div>

      {/* Toolbar */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 'var(--space-4)', flexWrap: 'wrap', alignItems: 'center' }}>
        {searchable && (
          <div className="search-bar" style={{ flex: 1, minWidth: 240 }}>
            <HiOutlineSearch className="search-icon" />
            <input
              className="form-input"
              placeholder={`Search ${entityName}s…`}
              value={search}
              onChange={e => { setSearch(e.target.value); setPage(1) }}
            />
          </div>
        )}
        {extraFilters.map((f, i) => (
          <div key={i}>{f({ filters, setFilters, setPage })}</div>
        ))}
      </div>

      {/* Table */}
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map(col => (
                <th key={col.key} style={col.style}>{col.label}</th>
              ))}
              {canWrite && <th style={{ textAlign: 'right', width: 120 }}>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {isLoading
              ? Array.from({ length: 6 }).map((_, i) => (
                  <tr key={i}>
                    {Array.from({ length: columns.length + (canWrite ? 1 : 0) }).map((_, j) => (
                      <td key={j}><div className="skeleton skeleton-text" style={{ width: '70%' }} /></td>
                    ))}
                  </tr>
                ))
              : records.length === 0
              ? (
                  <tr>
                    <td colSpan={columns.length + (canWrite ? 1 : 0)} style={{ textAlign: 'center', padding: '48px 24px' }}>
                      <div style={{ color: 'var(--color-gray)', fontSize: '0.9rem' }}>
                        No {entityName.toLowerCase()}s found{search ? ' matching your search' : ''}.
                      </div>
                      {canWrite && !search && (
                        <button className="btn btn-primary btn-sm" style={{ marginTop: 12 }} onClick={openCreate}>
                          <HiOutlinePlus size={14} /> Create first {entityName}
                        </button>
                      )}
                    </td>
                  </tr>
                )
              : records.map(rec => (
                  <tr key={rec.id}>
                    {columns.map(col => (
                      <td key={col.key} style={col.tdStyle}>
                        {col.render ? col.render(rec) : (rec[col.key] ?? '—')}
                      </td>
                    ))}
                    {canWrite && (
                      <td>
                        <div style={{ display: 'flex', gap: 6, justifyContent: 'flex-end' }}>
                          <button
                            className="btn btn-icon btn-secondary btn-sm"
                            title="Edit"
                            onClick={() => openEdit(rec)}
                          >
                            <HiOutlinePencil size={14} />
                          </button>
                          {archiveFn && (
                            <button
                              className="btn btn-icon btn-sm"
                              title="Archive"
                              onClick={() => archiveMutation.mutate(rec.id)}
                              style={{ background: 'var(--color-amber-100)', color: 'var(--color-amber-600)', border: '1px solid var(--color-amber-100)' }}
                            >
                              <HiOutlineArchive size={14} />
                            </button>
                          )}
                          <button
                            className="btn btn-icon btn-sm"
                            title="Delete"
                            onClick={() => setDeleteTarget(rec)}
                            style={{ background: '#FEE2E2', color: 'var(--color-error)', border: '1px solid #FECACA' }}
                          >
                            <HiOutlineTrash size={14} />
                          </button>
                        </div>
                      </td>
                    )}
                  </tr>
                ))
            }
          </tbody>
        </table>

        {/* Pagination */}
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

      {/* Modal */}
      <AnimatePresence>
        {modalOpen && FormModal && (
          <FormModal
            open={modalOpen}
            onClose={closeModal}
            initialData={editTarget}
            onSaved={onSaved}
          />
        )}
      </AnimatePresence>

      {/* Delete confirmation */}
      <ConfirmDialog
        isOpen={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={() => deleteMutation.mutate(deleteTarget.id)}
        title={`Delete ${entityName}`}
        message={`Are you sure you want to delete "${deleteTarget?.name || deleteTarget?.label || deleteTarget?.code}"? This cannot be undone.`}
        confirmLabel="Delete"
        loading={deleteMutation.isLoading}
        variant="danger"
      />
    </div>
  )
}
