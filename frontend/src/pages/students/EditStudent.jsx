/** ExamForge M2 — Edit Student Page (reuses AddStudent form in edit mode) */
import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { HiOutlineChevronLeft, HiOutlineSave } from 'react-icons/hi'
import toast from 'react-hot-toast'
import studentService  from '../../services/studentService.js'
import academicService from '../../services/academicService.js'

function Field({ label, required, error, children }) {
  return (
    <div className="form-group">
      <label className="form-label">{label}{required && <span className="required"> *</span>}</label>
      {children}
      {error && <div className="form-error">⚠ {error}</div>}
    </div>
  )
}

export default function EditStudent() {
  const { id } = useParams()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [form, setForm] = useState(null)
  const [errors, setErrors] = useState({})

  const { data: student, isLoading } = useQuery({
    queryKey: ['student-detail', id],
    queryFn: () => studentService.get(id).then(r => r.data),
  })

  const { data: depts } = useQuery({
    queryKey: ['depts-active'],
    queryFn: () => academicService.departments.list({ status:'active', page_size:200 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const { data: courses } = useQuery({
    queryKey: ['courses-by-dept', form?.department],
    queryFn: () => academicService.courses.list({ department: form?.department, status:'active', page_size:100 }).then(r => r.data.results),
    enabled: !!form?.department,
  })

  const { data: semesters } = useQuery({
    queryKey: ['semesters-by-course', form?.course],
    queryFn: () => academicService.semesters.list({ course: form?.course, status:'active', page_size:50 }).then(r => r.data.results),
    enabled: !!form?.course,
  })

  const { data: branches } = useQuery({
    queryKey: ['branches-by-course', form?.course],
    queryFn: () => academicService.branches.list({ course: form?.course, status:'active', page_size:100 }).then(r => r.data.results),
    enabled: !!form?.course,
  })

  // Prefill form on load
  useEffect(() => {
    if (student) {
      setForm({
        roll_number: student.roll_number || '',
        full_name: student.full_name || '',
        institutional_email: student.institutional_email || '',
        personal_email: student.personal_email || '',
        phone: student.phone || '',
        alternate_phone: student.alternate_phone || '',
        department: student.department || '',
        course: student.course || '',
        branch: student.branch || '',
        current_semester: student.current_semester || '',
        academic_year: student.academic_year || '',
        admission_year: student.admission_year || new Date().getFullYear(),
        enrollment_date: student.enrollment_date || '',
        gender: student.gender || 'prefer_not_to_say',
        date_of_birth: student.date_of_birth || '',
        blood_group: student.blood_group || 'unknown',
        address: student.address || '',
        guardian_name: student.guardian_name || '',
        guardian_phone: student.guardian_phone || '',
        status: student.status || 'active',
        is_eligible_for_exam: student.is_eligible_for_exam ?? true,
        remarks: student.remarks || '',
      })
    }
  }, [student])

  const set = (k, v) => {
    setForm(f => ({ ...f, [k]: v }))
    if (errors[k]) setErrors(e => ({ ...e, [k]: undefined }))
  }

  const updateMutation = useMutation({
    mutationFn: (data) => studentService.update(id, data),
    onSuccess: () => {
      toast.success('Student updated successfully.')
      qc.invalidateQueries(['student-detail', id])
      qc.invalidateQueries(['student-summary', id])
      qc.invalidateQueries(['students'])
      navigate(`/students/${id}`)
    },
    onError: (err) => {
      const serverErrors = err.response?.data?.details || {}
      setErrors(serverErrors)
      toast.error(err.response?.data?.message || 'Update failed. Please check the form.')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.full_name.trim()) { setErrors({ full_name: 'Full name is required.' }); return }
    updateMutation.mutate(form)
  }

  if (isLoading || !form) {
    return <div className="skeleton" style={{ height: 600, borderRadius: 14 }} />
  }

  const isSubmitting = updateMutation.isLoading

  return (
    <div>
      <div className="page-header">
        <div>
          <Link to={`/students/${id}`} className="btn btn-secondary btn-sm" style={{ marginBottom: 8 }}>
            <HiOutlineChevronLeft size={14} /> Back to Profile
          </Link>
          <div className="page-title">Edit Student</div>
          <div className="page-subtitle">{student?.full_name} · {student?.roll_number}</div>
        </div>
        <div className="page-actions">
          <button onClick={() => navigate(-1)} className="btn btn-secondary" disabled={isSubmitting}>Cancel</button>
          <button
            type="submit" form="edit-student-form"
            className={`btn btn-primary${isSubmitting ? ' btn-loading' : ''}`}
            disabled={isSubmitting}
          >
            <HiOutlineSave size={16} />{isSubmitting ? 'Saving…' : 'Save Changes'}
          </button>
        </div>
      </div>

      <form id="edit-student-form" onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-5)' }}>
          <div className="card">
            <div className="card-header"><span className="card-title">Personal Info</span></div>
            <Field label="Full Name" required error={errors.full_name}>
              <input className="form-input" value={form.full_name} onChange={e => set('full_name', e.target.value)} />
            </Field>
            <Field label="Roll Number" required error={errors.roll_number}>
              <input className="form-input" value={form.roll_number} onChange={e => set('roll_number', e.target.value.toUpperCase())} />
            </Field>
            <Field label="Institutional Email" required error={errors.institutional_email}>
              <input className="form-input" type="email" value={form.institutional_email} onChange={e => set('institutional_email', e.target.value)} />
            </Field>
            <Field label="Phone">
              <input className="form-input" type="tel" value={form.phone} onChange={e => set('phone', e.target.value)} />
            </Field>
            <Field label="Gender">
              <select className="form-select" value={form.gender} onChange={e => set('gender', e.target.value)}>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="prefer_not_to_say">Prefer not to say</option>
              </select>
            </Field>
            <Field label="Date of Birth">
              <input className="form-input" type="date" value={form.date_of_birth} onChange={e => set('date_of_birth', e.target.value)} />
            </Field>
          </div>

          <div className="card">
            <div className="card-header"><span className="card-title">Academic Placement</span></div>
            <Field label="Department" required error={errors.department}>
              <select className="form-select" value={form.department} onChange={e => set('department', e.target.value)}>
                <option value="">— Select —</option>
                {(depts || []).map(d => <option key={d.id} value={d.id}>{d.code} — {d.name}</option>)}
              </select>
            </Field>
            <Field label="Course" required error={errors.course}>
              <select className="form-select" value={form.course} onChange={e => set('course', e.target.value)} disabled={!form.department}>
                <option value="">— Select —</option>
                {(courses || []).map(c => <option key={c.id} value={c.id}>{c.code} — {c.name}</option>)}
              </select>
            </Field>
            <Field label="Branch">
              <select className="form-select" value={form.branch} onChange={e => set('branch', e.target.value)} disabled={!form.course}>
                <option value="">— Common / No Branch —</option>
                {(branches || []).map(b => <option key={b.id} value={b.id}>{b.code} — {b.name}</option>)}
              </select>
            </Field>
            <Field label="Semester" required error={errors.current_semester}>
              <select className="form-select" value={form.current_semester} onChange={e => set('current_semester', e.target.value)} disabled={!form.course}>
                <option value="">— Select —</option>
                {(semesters || []).map(s => <option key={s.id} value={s.id}>Semester {s.semester_number}</option>)}
              </select>
            </Field>
            <Field label="Status">
              <select className="form-select" value={form.status} onChange={e => set('status', e.target.value)}>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="suspended">Suspended</option>
                <option value="graduated">Graduated</option>
                <option value="withdrawn">Withdrawn</option>
              </select>
            </Field>
            <Field label="Exam Eligibility">
              <select className="form-select" value={form.is_eligible_for_exam ? 'true' : 'false'} onChange={e => set('is_eligible_for_exam', e.target.value === 'true')}>
                <option value="true">Eligible</option>
                <option value="false">Not Eligible</option>
              </select>
            </Field>
            <Field label="Remarks">
              <textarea className="form-textarea" rows={3} value={form.remarks} onChange={e => set('remarks', e.target.value)} />
            </Field>
          </div>
        </div>
      </form>
    </div>
  )
}
