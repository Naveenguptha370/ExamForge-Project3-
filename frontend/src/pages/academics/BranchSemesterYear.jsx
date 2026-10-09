/** ExamForge M2 — Branch, Semester, AcademicYear, Subject Management Pages */
import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { AnimatePresence, motion } from 'framer-motion'
import { HiOutlineX, HiOutlineSave } from 'react-icons/hi'
import toast from 'react-hot-toast'
import academicService from '../../services/academicService.js'
import AcademicCrudPage from '../../components/academics/AcademicCrudPage.jsx'

/* ─────────────────────────── BRANCHES ─────────────────────── */
function BranchModal({ open, onClose, initialData, onSaved }) {
  const isEdit = !!initialData
  const [form, setForm] = useState({
    course: initialData?.course || '',
    code: initialData?.code || '',
    name: initialData?.name || '',
    intake_capacity: initialData?.intake_capacity || 60,
    description: initialData?.description || '',
    status: initialData?.status || 'active',
  })
  const [errors, setErrors] = useState({})
  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); if (errors[k]) setErrors(e => ({ ...e, [k]: undefined })) }

  const { data: courses } = useQuery({
    queryKey: ['courses-active'],
    queryFn: () => academicService.courses.list({ status: 'active', page_size: 200 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const mutation = useMutation({
    mutationFn: (data) => isEdit
      ? academicService.branches.update(initialData.id, data)
      : academicService.branches.create(data),
    onSuccess: () => { toast.success(`Branch ${isEdit ? 'updated' : 'created'}.`); onSaved() },
    onError: (err) => { setErrors(err.response?.data?.details || {}); toast.error(err.response?.data?.message || 'Failed.') },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.course) { setErrors({ course: 'Course is required.' }); return }
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
              <span className="modal-title">{isEdit ? 'Edit Branch' : 'New Branch'}</span>
              <button className="modal-close" onClick={onClose}><HiOutlineX size={16} /></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body" style={{ display: 'grid', gap: 'var(--space-4)' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Course <span className="required">*</span></label>
                  <select className={`form-select${errors.course ? ' error' : ''}`} value={form.course} onChange={e => set('course', e.target.value)}>
                    <option value="">— Select Course —</option>
                    {(courses || []).map(c => <option key={c.id} value={c.id}>{c.code} — {c.name}</option>)}
                  </select>
                  {errors.course && <div className="form-error">⚠ {errors.course}</div>}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 'var(--space-4)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Code <span className="required">*</span></label>
                    <input className={`form-input${errors.code ? ' error' : ''}`} placeholder="CSE" value={form.code} onChange={e => set('code', e.target.value.toUpperCase())} />
                    {errors.code && <div className="form-error">⚠ {errors.code}</div>}
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Name <span className="required">*</span></label>
                    <input className={`form-input${errors.name ? ' error' : ''}`} placeholder="Computer Science & Engineering" value={form.name} onChange={e => set('name', e.target.value)} />
                    {errors.name && <div className="form-error">⚠ {errors.name}</div>}
                  </div>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Intake Capacity</label>
                    <input className="form-input" type="number" min="1" value={form.intake_capacity} onChange={e => set('intake_capacity', parseInt(e.target.value))} />
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
                  <label className="form-label">Description</label>
                  <textarea className="form-textarea" rows={2} value={form.description} onChange={e => set('description', e.target.value)} />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                <button type="submit" className={`btn btn-primary${mutation.isLoading ? ' btn-loading' : ''}`} disabled={mutation.isLoading}>
                  <HiOutlineSave size={15} />{mutation.isLoading ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Branch'}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

const branchColumns = [
  { key: 'code',  label: 'Code', render: r => <code style={{ fontFamily: 'monospace', fontWeight: 700 }}>{r.code}</code> },
  { key: 'name',  label: 'Branch Name', render: r => <strong>{r.name}</strong> },
  { key: 'course_code',    label: 'Course', render: r => <span className="badge badge-forest">{r.course_code}</span> },
  { key: 'department_code', label: 'Dept.', render: r => r.department_code || '—' },
  { key: 'intake_capacity', label: 'Intake', render: r => r.intake_capacity ?? '—' },
  { key: 'total_students',  label: 'Students', render: r => <strong>{r.total_students ?? 0}</strong> },
  { key: 'status', label: 'Status', render: r => <span className={`badge ${r.status === 'active' ? 'badge-success' : 'badge-neutral'}`}>{r.status}</span> },
]

export function BranchManagement() {
  return (
    <AcademicCrudPage
      title="Branches / Specializations"
      queryKey="branches"
      queryFn={(p) => academicService.branches.list(p)}
      deleteFn={(id) => academicService.branches.delete(id)}
      columns={branchColumns}
      FormModal={BranchModal}
      entityName="Branch"
    />
  )
}

/* ─────────────────────────── SEMESTERS ────────────────────── */
function SemesterModal({ open, onClose, initialData, onSaved }) {
  const isEdit = !!initialData
  const [form, setForm] = useState({
    course: initialData?.course || '',
    branch: initialData?.branch || '',
    semester_number: initialData?.semester_number || 1,
    name: initialData?.name || '',
    academic_year: initialData?.academic_year || '',
    start_date: initialData?.start_date || '',
    end_date: initialData?.end_date || '',
    status: initialData?.status || 'active',
    notes: initialData?.notes || '',
  })
  const [errors, setErrors] = useState({})
  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); if (errors[k]) setErrors(e => ({ ...e, [k]: undefined })) }

  const { data: courses } = useQuery({ queryKey: ['courses-active'], queryFn: () => academicService.courses.list({ status: 'active', page_size: 200 }).then(r => r.data.results), staleTime: 300_000 })
  const { data: branches } = useQuery({ queryKey: ['branches-by-course', form.course], queryFn: () => academicService.branches.list({ course: form.course, status: 'active', page_size: 100 }).then(r => r.data.results), enabled: !!form.course })
  const { data: years } = useQuery({ queryKey: ['academic-years'], queryFn: () => academicService.years.list({ page_size: 50 }).then(r => r.data.results), staleTime: 300_000 })

  const mutation = useMutation({
    mutationFn: (data) => isEdit ? academicService.semesters.update(initialData.id, data) : academicService.semesters.create(data),
    onSuccess: () => { toast.success(`Semester ${isEdit ? 'updated' : 'created'}.`); onSaved() },
    onError: (err) => { setErrors(err.response?.data?.details || {}); toast.error(err.response?.data?.message || 'Failed.') },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.course) { setErrors({ course: 'Course is required.' }); return }
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
              <span className="modal-title">{isEdit ? 'Edit Semester' : 'New Semester'}</span>
              <button className="modal-close" onClick={onClose}><HiOutlineX size={16} /></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body" style={{ display: 'grid', gap: 'var(--space-4)' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Course <span className="required">*</span></label>
                    <select className={`form-select${errors.course ? ' error' : ''}`} value={form.course} onChange={e => set('course', e.target.value)}>
                      <option value="">— Select —</option>
                      {(courses || []).map(c => <option key={c.id} value={c.id}>{c.code} — {c.name}</option>)}
                    </select>
                    {errors.course && <div className="form-error">⚠ {errors.course}</div>}
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Branch (optional)</label>
                    <select className="form-select" value={form.branch} onChange={e => set('branch', e.target.value)} disabled={!form.course}>
                      <option value="">All Branches / Common</option>
                      {(branches || []).map(b => <option key={b.id} value={b.id}>{b.code} — {b.name}</option>)}
                    </select>
                  </div>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 'var(--space-4)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Semester No.</label>
                    <input className="form-input" type="number" min="1" max="20" value={form.semester_number} onChange={e => set('semester_number', parseInt(e.target.value))} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Label (optional)</label>
                    <input className="form-input" placeholder="e.g. Odd Semester 2024" value={form.name} onChange={e => set('name', e.target.value)} />
                  </div>
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Academic Year</label>
                  <select className="form-select" value={form.academic_year} onChange={e => set('academic_year', e.target.value)}>
                    <option value="">— Select Year —</option>
                    {(years || []).map(y => <option key={y.id} value={y.id}>{y.label}{y.is_current ? ' (Current)' : ''}</option>)}
                  </select>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 'var(--space-4)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Start Date</label>
                    <input className="form-input" type="date" value={form.start_date} onChange={e => set('start_date', e.target.value)} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">End Date</label>
                    <input className="form-input" type="date" value={form.end_date} onChange={e => set('end_date', e.target.value)} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Status</label>
                    <select className="form-select" value={form.status} onChange={e => set('status', e.target.value)}>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                      <option value="completed">Completed</option>
                    </select>
                  </div>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                <button type="submit" className={`btn btn-primary${mutation.isLoading ? ' btn-loading' : ''}`} disabled={mutation.isLoading}>
                  <HiOutlineSave size={15} />{mutation.isLoading ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Semester'}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

const semesterColumns = [
  { key: 'semester_number', label: 'Sem#', render: r => <span style={{ fontWeight: 800, fontSize: '1rem', color: 'var(--color-emerald)' }}>{r.semester_number}</span> },
  { key: 'name',  label: 'Label', render: r => r.name || <span className="td-muted">—</span> },
  { key: 'course_code', label: 'Course', render: r => <span className="badge badge-forest">{r.course_code}</span> },
  { key: 'branch_code', label: 'Branch', render: r => r.branch_code || <span className="td-muted">All</span> },
  { key: 'academic_year_label', label: 'Year', render: r => r.academic_year_label || '—' },
  { key: 'total_subjects', label: 'Subjects', render: r => <strong>{r.total_subjects ?? 0}</strong> },
  { key: 'status', label: 'Status', render: r => <span className={`badge ${r.status === 'active' ? 'badge-success' : r.status === 'completed' ? 'badge-forest' : 'badge-neutral'}`}>{r.status}</span> },
]

export function SemesterManagement() {
  return (
    <AcademicCrudPage
      title="Semesters"
      queryKey="semesters"
      queryFn={(p) => academicService.semesters.list(p)}
      deleteFn={(id) => academicService.semesters.delete(id)}
      columns={semesterColumns}
      FormModal={SemesterModal}
      entityName="Semester"
    />
  )
}

/* ─────────────────────────── ACADEMIC YEAR ────────────────── */
function AcademicYearModal({ open, onClose, initialData, onSaved }) {
  const isEdit = !!initialData
  const [form, setForm] = useState({
    label: initialData?.label || '',
    start_date: initialData?.start_date || '',
    end_date: initialData?.end_date || '',
    is_current: initialData?.is_current || false,
    status: initialData?.status || 'active',
    notes: initialData?.notes || '',
  })
  const [errors, setErrors] = useState({})
  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); if (errors[k]) setErrors(e => ({ ...e, [k]: undefined })) }

  const mutation = useMutation({
    mutationFn: (data) => isEdit ? academicService.years.update(initialData.id, data) : academicService.years.create(data),
    onSuccess: () => { toast.success(`Academic year ${isEdit ? 'updated' : 'created'}.`); onSaved() },
    onError: (err) => { setErrors(err.response?.data?.details || {}); toast.error(err.response?.data?.message || 'Failed.') },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.label.trim()) { setErrors({ label: 'Label is required.' }); return }
    mutation.mutate(form)
  }

  return (
    <AnimatePresence>
      {open && (
        <div className="modal-overlay" onClick={onClose}>
          <motion.div className="modal modal-sm" onClick={e => e.stopPropagation()}
            initial={{ opacity: 0, scale: 0.94, y: 16 }} animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.94, y: 16 }} transition={{ duration: 0.2 }}>
            <div className="modal-header">
              <span className="modal-title">{isEdit ? 'Edit Academic Year' : 'New Academic Year'}</span>
              <button className="modal-close" onClick={onClose}><HiOutlineX size={16} /></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body" style={{ display: 'grid', gap: 'var(--space-4)' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Label <span className="required">*</span></label>
                  <input className={`form-input${errors.label ? ' error' : ''}`} placeholder="2024-2025" value={form.label} onChange={e => set('label', e.target.value)} />
                  <div className="form-hint">Format: YYYY-YYYY e.g. 2024-2025</div>
                  {errors.label && <div className="form-error">⚠ {errors.label}</div>}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Start Date</label>
                    <input className="form-input" type="date" value={form.start_date} onChange={e => set('start_date', e.target.value)} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">End Date</label>
                    <input className="form-input" type="date" value={form.end_date} onChange={e => set('end_date', e.target.value)} />
                  </div>
                </div>
                <div className="form-group" style={{ marginBottom: 0, display: 'flex', alignItems: 'center', gap: 10 }}>
                  <input type="checkbox" id="is_current" checked={form.is_current} onChange={e => set('is_current', e.target.checked)} style={{ accentColor: 'var(--color-emerald)', width: 16, height: 16 }} />
                  <label htmlFor="is_current" className="form-label" style={{ marginBottom: 0, cursor: 'pointer' }}>
                    Set as Current Academic Year
                  </label>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                <button type="submit" className={`btn btn-primary${mutation.isLoading ? ' btn-loading' : ''}`} disabled={mutation.isLoading}>
                  <HiOutlineSave size={15} />{mutation.isLoading ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Year'}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

const yearColumns = [
  { key: 'label', label: 'Academic Year', render: r => (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <strong style={{ fontSize: '1rem' }}>{r.label}</strong>
      {r.is_current && <span className="badge badge-amber">Current</span>}
    </div>
  )},
  { key: 'start_date', label: 'Start Date', render: r => r.start_date || '—' },
  { key: 'end_date',   label: 'End Date',   render: r => r.end_date || '—' },
  { key: 'total_semesters', label: 'Semesters', render: r => r.total_semesters ?? 0 },
  { key: 'total_students',  label: 'Students',  render: r => <strong>{r.total_students ?? 0}</strong> },
  { key: 'status', label: 'Status', render: r => <span className={`badge ${r.status === 'active' ? 'badge-success' : 'badge-neutral'}`}>{r.status}</span> },
]

export function AcademicYearManagement() {
  return (
    <AcademicCrudPage
      title="Academic Years"
      queryKey="academic-years-crud"
      queryFn={(p) => academicService.years.list(p)}
      deleteFn={(id) => academicService.years.delete(id)}
      columns={yearColumns}
      FormModal={AcademicYearModal}
      entityName="Academic Year"
    />
  )
}
