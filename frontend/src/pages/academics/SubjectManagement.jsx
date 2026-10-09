/** ExamForge M2 — Subject Management Page */
import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { AnimatePresence, motion } from 'framer-motion'
import { HiOutlineX, HiOutlineSave } from 'react-icons/hi'
import toast from 'react-hot-toast'
import academicService from '../../services/academicService.js'
import AcademicCrudPage from '../../components/academics/AcademicCrudPage.jsx'

function SubjectModal({ open, onClose, initialData, onSaved }) {
  const isEdit = !!initialData
  const [form, setForm] = useState({
    department: initialData?.department || '',
    course: initialData?.course || '',
    branch: initialData?.branch || '',
    semester: initialData?.semester || '',
    code: initialData?.code || '',
    name: initialData?.name || '',
    short_name: initialData?.short_name || '',
    subject_type: initialData?.subject_type || 'theory',
    credits: initialData?.credits || 3,
    lecture_hours_per_week: initialData?.lecture_hours_per_week || 3,
    lab_hours_per_week: initialData?.lab_hours_per_week || 0,
    is_external_exam: initialData?.is_external_exam ?? true,
    is_internal_exam: initialData?.is_internal_exam ?? true,
    max_external_marks: initialData?.max_external_marks || 100,
    max_internal_marks: initialData?.max_internal_marks || 50,
    pass_marks_external: initialData?.pass_marks_external || 35,
    is_elective_group: initialData?.is_elective_group || false,
    status: initialData?.status || 'active',
  })
  const [errors, setErrors] = useState({})
  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); if (errors[k]) setErrors(e => ({ ...e, [k]: undefined })) }

  const { data: depts } = useQuery({ queryKey: ['depts-active'], queryFn: () => academicService.departments.list({ status: 'active', page_size: 200 }).then(r => r.data.results), staleTime: 300_000 })
  const { data: courses } = useQuery({ queryKey: ['courses-by-dept', form.department], queryFn: () => academicService.courses.list({ department: form.department, status: 'active', page_size: 100 }).then(r => r.data.results), enabled: !!form.department })
  const { data: branches } = useQuery({ queryKey: ['branches-by-course', form.course], queryFn: () => academicService.branches.list({ course: form.course, status: 'active', page_size: 100 }).then(r => r.data.results), enabled: !!form.course })
  const { data: semesters } = useQuery({ queryKey: ['semesters-by-course', form.course], queryFn: () => academicService.semesters.list({ course: form.course, status: 'active', page_size: 50 }).then(r => r.data.results), enabled: !!form.course })

  const mutation = useMutation({
    mutationFn: (data) => isEdit ? academicService.subjects.update(initialData.id, data) : academicService.subjects.create(data),
    onSuccess: () => { toast.success(`Subject ${isEdit ? 'updated' : 'created'}.`); onSaved() },
    onError: (err) => { setErrors(err.response?.data?.details || {}); toast.error(err.response?.data?.message || 'Failed.') },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.department) { setErrors({ department: 'Department is required.' }); return }
    if (!form.course) { setErrors({ course: 'Course is required.' }); return }
    if (!form.semester) { setErrors({ semester: 'Semester is required.' }); return }
    if (!form.code.trim()) { setErrors({ code: 'Subject code is required.' }); return }
    if (!form.name.trim()) { setErrors({ name: 'Subject name is required.' }); return }
    mutation.mutate(form)
  }

  return (
    <AnimatePresence>
      {open && (
        <div className="modal-overlay" onClick={onClose}>
          <motion.div className="modal modal-lg" onClick={e => e.stopPropagation()}
            initial={{ opacity: 0, scale: 0.94, y: 16 }} animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.94, y: 16 }} transition={{ duration: 0.2 }}>
            <div className="modal-header">
              <span className="modal-title">{isEdit ? 'Edit Subject' : 'New Subject'}</span>
              <button className="modal-close" onClick={onClose}><HiOutlineX size={16} /></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body" style={{ display: 'grid', gap: 'var(--space-4)' }}>
                {/* Hierarchy */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 'var(--space-3)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Department <span className="required">*</span></label>
                    <select className={`form-select${errors.department ? ' error' : ''}`} value={form.department} onChange={e => { set('department', e.target.value); setForm(f => ({ ...f, course: '', branch: '', semester: '' })) }}>
                      <option value="">— Dept —</option>
                      {(depts || []).map(d => <option key={d.id} value={d.id}>{d.code}</option>)}
                    </select>
                    {errors.department && <div className="form-error" style={{ fontSize: '0.7rem' }}>⚠ {errors.department}</div>}
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Course <span className="required">*</span></label>
                    <select className={`form-select${errors.course ? ' error' : ''}`} value={form.course} onChange={e => { set('course', e.target.value); setForm(f => ({ ...f, branch: '', semester: '' })) }} disabled={!form.department}>
                      <option value="">— Course —</option>
                      {(courses || []).map(c => <option key={c.id} value={c.id}>{c.code}</option>)}
                    </select>
                    {errors.course && <div className="form-error" style={{ fontSize: '0.7rem' }}>⚠ {errors.course}</div>}
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Branch</label>
                    <select className="form-select" value={form.branch} onChange={e => set('branch', e.target.value)} disabled={!form.course}>
                      <option value="">All Branches</option>
                      {(branches || []).map(b => <option key={b.id} value={b.id}>{b.code}</option>)}
                    </select>
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Semester <span className="required">*</span></label>
                    <select className={`form-select${errors.semester ? ' error' : ''}`} value={form.semester} onChange={e => set('semester', e.target.value)} disabled={!form.course}>
                      <option value="">— Sem —</option>
                      {(semesters || []).map(s => <option key={s.id} value={s.id}>Sem {s.semester_number}</option>)}
                    </select>
                    {errors.semester && <div className="form-error" style={{ fontSize: '0.7rem' }}>⚠ {errors.semester}</div>}
                  </div>
                </div>

                {/* Identity */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 1fr', gap: 'var(--space-3)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Code <span className="required">*</span></label>
                    <input className={`form-input${errors.code ? ' error' : ''}`} placeholder="CS301" value={form.code} onChange={e => set('code', e.target.value.toUpperCase())} />
                    {errors.code && <div className="form-error" style={{ fontSize: '0.7rem' }}>⚠ {errors.code}</div>}
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Subject Name <span className="required">*</span></label>
                    <input className={`form-input${errors.name ? ' error' : ''}`} placeholder="Data Structures and Algorithms" value={form.name} onChange={e => set('name', e.target.value)} />
                    {errors.name && <div className="form-error" style={{ fontSize: '0.7rem' }}>⚠ {errors.name}</div>}
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Short Name</label>
                    <input className="form-input" placeholder="DSA" value={form.short_name} onChange={e => set('short_name', e.target.value)} />
                  </div>
                </div>

                {/* Type & Credits */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr 1fr', gap: 'var(--space-3)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Type</label>
                    <select className="form-select" value={form.subject_type} onChange={e => set('subject_type', e.target.value)}>
                      <option value="theory">Theory</option>
                      <option value="lab">Lab / Practical</option>
                      <option value="theory_cum_lab">Theory + Lab</option>
                      <option value="project">Project</option>
                      <option value="seminar">Seminar</option>
                      <option value="elective">Elective</option>
                    </select>
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Credits</label>
                    <input className="form-input" type="number" min="0" max="10" value={form.credits} onChange={e => set('credits', parseFloat(e.target.value))} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Lecture Hrs/Wk</label>
                    <input className="form-input" type="number" min="0" max="20" value={form.lecture_hours_per_week} onChange={e => set('lecture_hours_per_week', parseInt(e.target.value))} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Lab Hrs/Wk</label>
                    <input className="form-input" type="number" min="0" max="20" value={form.lab_hours_per_week} onChange={e => set('lab_hours_per_week', parseInt(e.target.value))} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Status</label>
                    <select className="form-select" value={form.status} onChange={e => set('status', e.target.value)}>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </div>
                </div>

                {/* Marks */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 'var(--space-3)' }}>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Max External Marks</label>
                    <input className="form-input" type="number" min="0" value={form.max_external_marks} onChange={e => set('max_external_marks', parseInt(e.target.value))} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Max Internal Marks</label>
                    <input className="form-input" type="number" min="0" value={form.max_internal_marks} onChange={e => set('max_internal_marks', parseInt(e.target.value))} />
                  </div>
                  <div className="form-group" style={{ marginBottom: 0 }}>
                    <label className="form-label">Pass Marks (Ext)</label>
                    <input className="form-input" type="number" min="0" value={form.pass_marks_external} onChange={e => set('pass_marks_external', parseInt(e.target.value))} />
                  </div>
                </div>

                {/* Flags */}
                <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
                  {[
                    { key: 'is_external_exam', label: 'External Examination' },
                    { key: 'is_internal_exam', label: 'Internal Examination' },
                    { key: 'is_elective_group', label: 'Elective Group Subject' },
                  ].map(flag => (
                    <label key={flag.key} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.875rem', cursor: 'pointer' }}>
                      <input type="checkbox" checked={form[flag.key]} onChange={e => set(flag.key, e.target.checked)} style={{ accentColor: 'var(--color-emerald)', width: 16, height: 16 }} />
                      {flag.label}
                    </label>
                  ))}
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                <button type="submit" className={`btn btn-primary${mutation.isLoading ? ' btn-loading' : ''}`} disabled={mutation.isLoading}>
                  <HiOutlineSave size={15} />{mutation.isLoading ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Subject'}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

const subjectColumns = [
  { key: 'code',  label: 'Code', render: r => <code style={{ fontFamily: 'monospace', fontWeight: 700 }}>{r.code}</code> },
  { key: 'name',  label: 'Subject Name', render: r => <strong>{r.name}</strong> },
  { key: 'department_code', label: 'Dept.', render: r => <span className="badge badge-forest">{r.department_code}</span> },
  { key: 'course_code',     label: 'Course', render: r => r.course_code || '—' },
  { key: 'semester_number', label: 'Sem.', render: r => r.semester_number ? `Sem ${r.semester_number}` : '—' },
  { key: 'subject_type', label: 'Type', render: r => {
    const cls = { theory: 'badge-forest', lab: 'badge-amber', project: 'badge-success', elective: 'badge-neutral' }
    return <span className={`badge ${cls[r.subject_type] || 'badge-neutral'}`}>{r.subject_type?.replace(/_/g,' ')}</span>
  }},
  { key: 'credits', label: 'Credits', render: r => <strong>{r.credits}</strong> },
  { key: 'total_registered_students', label: 'Registered', render: r => r.total_registered_students ?? 0 },
  { key: 'status', label: 'Status', render: r => <span className={`badge ${r.status === 'active' ? 'badge-success' : 'badge-neutral'}`}>{r.status}</span> },
]

export default function SubjectManagement() {
  return (
    <AcademicCrudPage
      title="Subject Catalog"
      queryKey="subjects"
      queryFn={(p) => academicService.subjects.list(p)}
      deleteFn={(id) => academicService.subjects.delete(id)}
      archiveFn={(id) => academicService.subjects.archive(id)}
      columns={subjectColumns}
      FormModal={SubjectModal}
      entityName="Subject"
    />
  )
}
