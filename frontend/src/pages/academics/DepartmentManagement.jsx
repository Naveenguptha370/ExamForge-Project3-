/**
 * ExamForge M2 — Department Management Page
 */
import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { HiOutlineX, HiOutlineSave, HiOutlineOfficeBuilding } from 'react-icons/hi'
import toast from 'react-hot-toast'
import academicService from '../../services/academicService.js'
import AcademicCrudPage from '../../components/academics/AcademicCrudPage.jsx'

/* ── Modal form ────────────────────────────────────────────── */
function DepartmentModal({ open, onClose, initialData, onSaved }) {
  const qc = useQueryClient()
  const isEdit = !!initialData
  const [form, setForm] = useState({
    code: initialData?.code || '',
    name: initialData?.name || '',
    email: initialData?.email || '',
    phone: initialData?.phone || '',
    established_year: initialData?.established_year || '',
    description: initialData?.description || '',
    status: initialData?.status || 'active',
    notes: initialData?.notes || '',
  })
  const [errors, setErrors] = useState({})
  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); if (errors[k]) setErrors(e => ({ ...e, [k]: undefined })) }

  const mutation = useMutation({
    mutationFn: (data) => isEdit
      ? academicService.departments.update(initialData.id, data)
      : academicService.departments.create(data),
    onSuccess: () => {
      toast.success(`Department ${isEdit ? 'updated' : 'created'} successfully.`)
      onSaved()
    },
    onError: (err) => {
      setErrors(err.response?.data?.details || {})
      toast.error(err.response?.data?.message || 'Failed to save department.')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.code.trim()) { setErrors({ code: 'Code is required.' }); return }
    if (!form.name.trim()) { setErrors({ name: 'Name is required.' }); return }
    mutation.mutate(form)
  }

  return (
    <AnimatePresence>
      {open && (
        <div className="modal-overlay" onClick={onClose}>
          <motion.div
            className="modal modal-md"
            onClick={e => e.stopPropagation()}
            initial={{ opacity: 0, scale: 0.94, y: 16 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.94, y: 16 }}
            transition={{ duration: 0.2 }}
          >
            <div className="modal-header">
              <span className="modal-title">
                <HiOutlineOfficeBuilding style={{ verticalAlign: 'middle', marginRight: 8 }} />
                {isEdit ? 'Edit Department' : 'New Department'}
              </span>
              <button className="modal-close" onClick={onClose}><HiOutlineX size={16} /></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 'var(--space-4)' }}>
                  <div className="form-group">
                    <label className="form-label">Code <span className="required">*</span></label>
                    <input className={`form-input${errors.code ? ' error' : ''}`}
                      placeholder="e.g. CSE" value={form.code}
                      onChange={e => set('code', e.target.value.toUpperCase())} />
                    {errors.code && <div className="form-error">⚠ {errors.code}</div>}
                  </div>
                  <div className="form-group">
                    <label className="form-label">Department Name <span className="required">*</span></label>
                    <input className={`form-input${errors.name ? ' error' : ''}`}
                      placeholder="e.g. Computer Science & Engineering" value={form.name}
                      onChange={e => set('name', e.target.value)} />
                    {errors.name && <div className="form-error">⚠ {errors.name}</div>}
                  </div>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)' }}>
                  <div className="form-group">
                    <label className="form-label">Email</label>
                    <input className="form-input" type="email" value={form.email} onChange={e => set('email', e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Phone</label>
                    <input className="form-input" type="tel" value={form.phone} onChange={e => set('phone', e.target.value)} />
                  </div>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)' }}>
                  <div className="form-group">
                    <label className="form-label">Established Year</label>
                    <input className="form-input" type="number" min="1900" max="2100" value={form.established_year} onChange={e => set('established_year', e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Status</label>
                    <select className="form-select" value={form.status} onChange={e => set('status', e.target.value)}>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Description</label>
                  <textarea className="form-textarea" rows={2} value={form.description} onChange={e => set('description', e.target.value)} />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Notes</label>
                  <textarea className="form-textarea" rows={2} value={form.notes} onChange={e => set('notes', e.target.value)} />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                <button type="submit" className={`btn btn-primary${mutation.isLoading ? ' btn-loading' : ''}`} disabled={mutation.isLoading}>
                  <HiOutlineSave size={15} />{mutation.isLoading ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Department'}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

/* ── Column definitions ──────────────────────────────────── */
const columns = [
  { key: 'code',  label: 'Code',  render: r => <span className="badge badge-forest">{r.code}</span> },
  { key: 'name',  label: 'Department Name', render: r => <strong>{r.name}</strong> },
  { key: 'email', label: 'Email', render: r => r.email || <span className="td-muted">—</span> },
  { key: 'established_year', label: 'Est. Year', render: r => r.established_year || '—' },
  { key: 'total_courses',  label: 'Courses',  render: r => <span style={{ fontWeight: 600 }}>{r.total_courses ?? 0}</span> },
  { key: 'total_students', label: 'Students', render: r => <span style={{ fontWeight: 600 }}>{r.total_students ?? 0}</span> },
  { key: 'status', label: 'Status', render: r => (
    <span className={`badge ${r.status === 'active' ? 'badge-success' : 'badge-neutral'}`}>{r.status}</span>
  )},
]

export default function DepartmentManagement() {
  return (
    <AcademicCrudPage
      title="Departments"
      subtitle="Manage all academic departments"
      queryKey="departments"
      queryFn={(p) => academicService.departments.list(p)}
      deleteFn={(id) => academicService.departments.delete(id)}
      archiveFn={(id) => academicService.departments.archive(id)}
      columns={columns}
      FormModal={DepartmentModal}
      entityName="Department"
    />
  )
}
