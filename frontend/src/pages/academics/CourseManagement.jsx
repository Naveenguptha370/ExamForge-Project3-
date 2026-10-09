/** ExamForge M2 — Course Management Page */
import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { AnimatePresence, motion } from 'framer-motion'
import { HiOutlineX, HiOutlineSave } from 'react-icons/hi'
import toast from 'react-hot-toast'
import academicService from '../../services/academicService.js'
import AcademicCrudPage from '../../components/academics/AcademicCrudPage.jsx'

function CourseModal({ open, onClose, initialData, onSaved }) {
  const isEdit = !!initialData
  const [form, setForm] = useState({
    department: initialData?.department || '',
    code: initialData?.code || '',
    name: initialData?.name || '',
    short_name: initialData?.short_name || '',
    duration_years: initialData?.duration_years || 4,
    total_semesters: initialData?.total_semesters || 8,
    is_postgraduate: initialData?.is_postgraduate || false,
    description: initialData?.description || '',
    status: initialData?.status || 'active',
    notes: initialData?.notes || '',
  })
  const [errors, setErrors] = useState({})
  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); if (errors[k]) setErrors(e => ({ ...e, [k]: undefined })) }

  const { data: depts } = useQuery({
    queryKey: ['depts-active'],
    queryFn: () => academicService.departments.list({ status: 'active', page_size: 200 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const mutation = useMutation({
    mutationFn: (data) => isEdit
      ? academicService.courses.update(initialData.id, data)
      : academicService.courses.create(data),
    onSuccess: () => { toast.success(`Course ${isEdit ? 'updated' : 'created'}.`); onSaved() },
    onError: (err) => { setErrors(err.response?.data?.details || {}); toast.error(err.response?.data?.message || 'Failed.') },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.department) { setErrors({ department: 'Department is required.' }); return }
    if (!form.code.trim()) { setErrors({ code: 'Code is required.' }); return }
    if (!form.name.trim()) { setErrors({ name: 'Name is required.' }); return }
    mutation.mutate(form)
  }

  return (
    <AnimatePresence>
      {open && (
        <div className="modal-overlay" onClick={onClose}>
          <motion.div className="modal modal-md" onClick={e => e.stopPropagation()}
            initial={{ opacity: 0, scale: 0.94, y: 16 }} animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.94, y: 16 }} transition={{ duration: 0.2 }}>
            <div className="modal-header">
              <span className="modal-title">{isEdit ? 'Edit Course' : 'New Course / Program'}</span>
              <button className="modal-close" onClick={onClose}><HiOutlineX size={16} /></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body" style={{ display: 'grid', gap: 'var(--space-4)' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Department <span className="required">*</span></label>
                  <select className={`form-select${errors.department ? ' error' : ''}`} value={form.department} onChange={e => set('department', e.target.value)}>
                    <option value="">— Select Department —</option>
                    {(depts || []).map(d => <option key={d.id} value={d.id}>{d.code} — {d.name}</option>)}
                  </select>
                  {errors.department && <div className="form-error">⚠ {errors.department}</div>}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 'var(--space-4)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Code <span className="required">*</span></label>
                    <input className={`form-input${errors.code ? ' error' : ''}`} placeholder="BTECH" value={form.code} onChange={e => set('code', e.target.value.toUpperCase())} />
                    {errors.code && <div className="form-error">⚠ {errors.code}</div>}
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Name <span className="required">*</span></label>
                    <input className={`form-input${errors.name ? ' error' : ''}`} placeholder="Bachelor of Technology" value={form.name} onChange={e => set('name', e.target.value)} />
                    {errors.name && <div className="form-error">⚠ {errors.name}</div>}
                  </div>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 'var(--space-4)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Duration (Years)</label>
                    <input className="form-input" type="number" min="1" max="10" value={form.duration_years} onChange={e => set('duration_years', parseInt(e.target.value))} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Total Semesters</label>
                    <input className="form-input" type="number" min="1" max="20" value={form.total_semesters} onChange={e => set('total_semesters', parseInt(e.target.value))} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Status</label>
                    <select className="form-select" value={form.status} onChange={e => set('status', e.target.value)}>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </div>
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <input type="checkbox" checked={form.is_postgraduate} onChange={e => set('is_postgraduate', e.target.checked)}
                      style={{ accentColor: 'var(--color-emerald)', width: 16, height: 16 }} />
                    Is Postgraduate Programme (PG)
                  </label>
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Description</label>
                  <textarea className="form-textarea" rows={2} value={form.description} onChange={e => set('description', e.target.value)} />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                <button type="submit" className={`btn btn-primary${mutation.isLoading ? ' btn-loading' : ''}`} disabled={mutation.isLoading}>
                  <HiOutlineSave size={15} />{mutation.isLoading ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Course'}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

const columns = [
  { key: 'code',  label: 'Code', render: r => <code style={{ fontFamily: 'monospace', fontWeight: 700 }}>{r.code}</code> },
  { key: 'name',  label: 'Course Name', render: r => <strong>{r.name}</strong> },
  { key: 'department_code', label: 'Dept.', render: r => <span className="badge badge-forest">{r.department_code}</span> },
  { key: 'duration_years', label: 'Duration', render: r => `${r.duration_years}Y / ${r.total_semesters} Semesters` },
  { key: 'is_postgraduate', label: 'Level', render: r => r.is_postgraduate ? <span className="badge badge-amber">PG</span> : <span className="badge badge-neutral">UG</span> },
  { key: 'total_students', label: 'Students', render: r => <strong>{r.total_students ?? 0}</strong> },
  { key: 'status', label: 'Status', render: r => <span className={`badge ${r.status === 'active' ? 'badge-success' : 'badge-neutral'}`}>{r.status}</span> },
]

export default function CourseManagement() {
  return (
    <AcademicCrudPage
      title="Courses & Programs"
      queryKey="courses"
      queryFn={(p) => academicService.courses.list(p)}
      deleteFn={(id) => academicService.courses.delete(id)}
      columns={columns}
      FormModal={CourseModal}
      entityName="Course"
    />
  )
}
