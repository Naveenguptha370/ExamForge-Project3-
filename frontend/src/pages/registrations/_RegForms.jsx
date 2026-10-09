/** ExamForge M2 — Available Subjects, Subject Registration, Exam Registration, Registration Details, Bulk, History, Reports */

// ════════════════════════════════════════════════════════════════
// AVAILABLE SUBJECTS
// ════════════════════════════════════════════════════════════════
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { HiOutlineSearch, HiOutlineBookOpen, HiOutlineAcademicCap } from 'react-icons/hi'
import registrationService from '../../services/registrationService.js'
import academicService from '../../services/academicService.js'

export function AvailableSubjects() {
  const [studentId, setStudentId] = useState('')
  const [searched, setSearched] = useState('')

  const { data, isLoading } = useQuery({
    queryKey: ['available-subjects', searched],
    queryFn: () => registrationService.subjects.available(searched).then(r => r.data.data),
    enabled: !!searched,
  })

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="page-title"><HiOutlineBookOpen size={22} color="var(--color-emerald)" /> Available Subjects</div>
          <div className="page-subtitle">Look up subjects available for a student's current semester</div>
        </div>
      </div>
      <div className="card" style={{ marginBottom: 'var(--space-4)' }}>
        <div style={{ display: 'flex', gap: 12 }}>
          <input className="form-input" placeholder="Enter Student ID or Roll Number…" value={studentId} onChange={e => setStudentId(e.target.value)} style={{ flex: 1 }} />
          <button className="btn btn-primary" onClick={() => setSearched(studentId)} disabled={!studentId.trim()}>
            <HiOutlineSearch size={16} /> Find Subjects
          </button>
        </div>
      </div>

      {searched && (
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr><th>Code</th><th>Subject Name</th><th>Type</th><th>Credits</th><th>External</th><th>Internal</th></tr>
            </thead>
            <tbody>
              {isLoading
                ? Array.from({ length: 4 }).map((_, i) => (
                    <tr key={i}>{Array.from({ length: 6 }).map((_, j) => <td key={j}><div className="skeleton skeleton-text" style={{ width: '70%' }} /></td>)}</tr>
                  ))
                : (data || []).length === 0
                ? <tr><td colSpan={6} style={{ textAlign: 'center', padding: '32px', color: 'var(--color-gray)' }}>No subjects found for this student.</td></tr>
                : (data || []).map(s => (
                    <tr key={s.id}>
                      <td><code style={{ fontFamily: 'monospace', fontWeight: 700 }}>{s.code}</code></td>
                      <td><strong>{s.name}</strong></td>
                      <td><span className="badge badge-forest">{s.subject_type}</span></td>
                      <td><strong>{s.credits}</strong></td>
                      <td>{s.is_external_exam ? `✅ ${s.max_external_marks}` : '—'}</td>
                      <td>{s.is_internal_exam ? `✅ ${s.max_internal_marks}` : '—'}</td>
                    </tr>
                  ))
              }
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

// ════════════════════════════════════════════════════════════════
// SUBJECT REGISTRATION FORM
// ════════════════════════════════════════════════════════════════
import { useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { motion } from 'framer-motion'
import academicServiceImport from '../../services/academicService.js'
import registrationServiceImport from '../../services/registrationService.js'
import studentService from '../../services/studentService.js'

export function SubjectRegistration() {
  const [form, setForm] = useState({ student: '', subject: '', semester: '', academic_year: '' })
  const [errors, setErrors] = useState({})
  const qc = useQueryClient()
  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); if (errors[k]) setErrors(e => ({ ...e, [k]: undefined })) }

  const { data: years }    = useQuery({ queryKey: ['academic-years'], queryFn: () => academicServiceImport.years.list({ page_size: 50 }).then(r => r.data.results), staleTime: 300_000 })
  const { data: students } = useQuery({ queryKey: ['students-list'], queryFn: () => studentService.list({ page_size: 200, status: 'active' }).then(r => r.data.results), staleTime: 60_000 })
  const { data: semesters } = useQuery({ queryKey: ['semesters-active'], queryFn: () => academicServiceImport.semesters.list({ status: 'active', page_size: 100 }).then(r => r.data.results), staleTime: 300_000 })

  const { data: availSubjects } = useQuery({
    queryKey: ['available-subjects-form', form.student],
    queryFn: () => registrationServiceImport.subjects.available(form.student).then(r => r.data.data),
    enabled: !!form.student,
  })

  const mutation = useMutation({
    mutationFn: (data) => registrationServiceImport.subjects.create(data),
    onSuccess: () => {
      toast.success('Subject registered successfully.')
      setForm({ student: '', subject: '', semester: '', academic_year: '' })
      qc.invalidateQueries(['subject-registrations'])
      qc.invalidateQueries(['registration-dashboard'])
    },
    onError: (err) => {
      setErrors(err.response?.data?.details || {})
      toast.error(err.response?.data?.message || 'Registration failed.')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.student) { setErrors({ student: 'Student is required.' }); return }
    if (!form.subject) { setErrors({ subject: 'Subject is required.' }); return }
    if (!form.academic_year) { setErrors({ academic_year: 'Academic year is required.' }); return }
    mutation.mutate(form)
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="page-title"><HiOutlineBookOpen size={22} color="var(--color-emerald)" /> Subject Registration</div>
          <div className="page-subtitle">Register a student for a subject in the current semester</div>
        </div>
      </div>
      <motion.div className="card" style={{ maxWidth: 640 }} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 'var(--space-4)' }}>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label">Student <span className="required">*</span></label>
            <select className={`form-select${errors.student ? ' error' : ''}`} value={form.student} onChange={e => set('student', e.target.value)}>
              <option value="">— Select Student —</option>
              {(students || []).map(s => <option key={s.id} value={s.id}>{s.roll_number} — {s.full_name}</option>)}
            </select>
            {errors.student && <div className="form-error">⚠ {errors.student}</div>}
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label">Subject <span className="required">*</span></label>
            <select className={`form-select${errors.subject ? ' error' : ''}`} value={form.subject} onChange={e => set('subject', e.target.value)} disabled={!form.student}>
              <option value="">{form.student ? '— Select Subject —' : '— Select a student first —'}</option>
              {(availSubjects || []).map(s => <option key={s.id} value={s.id}>{s.code} — {s.name} ({s.credits} cr)</option>)}
            </select>
            {errors.subject && <div className="form-error">⚠ {errors.subject}</div>}
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label">Semester</label>
            <select className="form-select" value={form.semester} onChange={e => set('semester', e.target.value)}>
              <option value="">— Select Semester —</option>
              {(semesters || []).map(s => <option key={s.id} value={s.id}>Sem {s.semester_number} — {s.course_code}</option>)}
            </select>
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label">Academic Year <span className="required">*</span></label>
            <select className={`form-select${errors.academic_year ? ' error' : ''}`} value={form.academic_year} onChange={e => set('academic_year', e.target.value)}>
              <option value="">— Select Year —</option>
              {(years || []).map(y => <option key={y.id} value={y.id}>{y.label}{y.is_current ? ' (Current)' : ''}</option>)}
            </select>
            {errors.academic_year && <div className="form-error">⚠ {errors.academic_year}</div>}
          </div>
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12 }}>
            <button type="reset" className="btn btn-secondary" onClick={() => setForm({ student: '', subject: '', semester: '', academic_year: '' })}>Clear</button>
            <button type="submit" className={`btn btn-primary${mutation.isLoading ? ' btn-loading' : ''}`} disabled={mutation.isLoading}>
              {mutation.isLoading ? 'Registering…' : 'Register Subject'}
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  )
}

// ════════════════════════════════════════════════════════════════
// EXAM REGISTRATION
// ════════════════════════════════════════════════════════════════
export function ExamRegistration() {
  const [form, setForm] = useState({ student: '', subject: '', academic_year: '' })
  const [errors, setErrors] = useState({})
  const qc = useQueryClient()
  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); if (errors[k]) setErrors(e => ({ ...e, [k]: undefined })) }

  const { data: years }    = useQuery({ queryKey: ['academic-years'], queryFn: () => academicServiceImport.years.list({ page_size: 50 }).then(r => r.data.results), staleTime: 300_000 })
  const { data: students } = useQuery({ queryKey: ['students-list'], queryFn: () => studentService.list({ page_size: 200, status: 'active', is_eligible_for_exam: true }).then(r => r.data.results), staleTime: 60_000 })

  const mutation = useMutation({
    mutationFn: (data) => registrationServiceImport.exams.create(data),
    onSuccess: () => {
      toast.success('Exam registration successful.')
      setForm({ student: '', subject: '', academic_year: '' })
      qc.invalidateQueries(['exam-registrations'])
      qc.invalidateQueries(['registration-dashboard'])
    },
    onError: (err) => {
      setErrors(err.response?.data?.details || {})
      toast.error(err.response?.data?.message || 'Exam registration failed.')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.student) { setErrors({ student: 'Student is required.' }); return }
    if (!form.subject) { setErrors({ subject: 'Subject is required.' }); return }
    mutation.mutate(form)
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="page-title"><HiOutlineAcademicCap size={22} color="var(--color-emerald)" /> Exam Registration</div>
          <div className="page-subtitle">Register an eligible student for an examination</div>
        </div>
      </div>
      <motion.div className="card" style={{ maxWidth: 640 }} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <div style={{ padding: '10px 14px', background: 'var(--color-sage)', borderRadius: 'var(--radius-md)', marginBottom: 'var(--space-4)', fontSize: '0.8125rem', color: 'var(--color-forest)' }}>
          ℹ Only students marked as <strong>Exam Eligible</strong> are shown.
        </div>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 'var(--space-4)' }}>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label">Student <span className="required">*</span></label>
            <select className={`form-select${errors.student ? ' error' : ''}`} value={form.student} onChange={e => set('student', e.target.value)}>
              <option value="">— Select Eligible Student —</option>
              {(students || []).map(s => <option key={s.id} value={s.id}>{s.roll_number} — {s.full_name}</option>)}
            </select>
            {errors.student && <div className="form-error">⚠ {errors.student}</div>}
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label">Subject Code / ID <span className="required">*</span></label>
            <input className={`form-input${errors.subject ? ' error' : ''}`} placeholder="Subject ID or code" value={form.subject} onChange={e => set('subject', e.target.value)} />
            {errors.subject && <div className="form-error">⚠ {errors.subject}</div>}
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label">Academic Year</label>
            <select className="form-select" value={form.academic_year} onChange={e => set('academic_year', e.target.value)}>
              <option value="">— Select Year —</option>
              {(years || []).map(y => <option key={y.id} value={y.id}>{y.label}{y.is_current ? ' (Current)' : ''}</option>)}
            </select>
          </div>
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12 }}>
            <button type="reset" className="btn btn-secondary" onClick={() => setForm({ student: '', subject: '', academic_year: '' })}>Clear</button>
            <button type="submit" className={`btn btn-primary${mutation.isLoading ? ' btn-loading' : ''}`} disabled={mutation.isLoading}>
              {mutation.isLoading ? 'Registering…' : 'Register for Exam'}
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  )
}
