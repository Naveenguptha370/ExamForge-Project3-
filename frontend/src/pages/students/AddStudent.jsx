/**
 * ExamForge M2 — Add Student Page
 * Full form with cascade dropdowns and real-time validation.
 */

import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { HiOutlineChevronLeft, HiOutlineSave } from 'react-icons/hi'
import toast from 'react-hot-toast'

import studentService  from '../../services/studentService.js'
import academicService from '../../services/academicService.js'

function Field({ label, required, error, hint, children }) {
  return (
    <div className="form-group">
      <label className="form-label">
        {label} {required && <span className="required">*</span>}
      </label>
      {children}
      {hint  && <div className="form-hint">{hint}</div>}
      {error && <div className="form-error">⚠ {error}</div>}
    </div>
  )
}

export default function AddStudent() {
  const navigate = useNavigate()
  const qc       = useQueryClient()

  const [form, setForm] = useState({
    roll_number:'', full_name:'', institutional_email:'', personal_email:'',
    phone:'', alternate_phone:'',
    department:'', course:'', branch:'', current_semester:'', academic_year:'',
    admission_year: new Date().getFullYear(), enrollment_date: new Date().toISOString().split('T')[0],
    gender:'prefer_not_to_say', date_of_birth:'', blood_group:'unknown',
    address:'', guardian_name:'', guardian_phone:'',
    status:'active', is_eligible_for_exam:true, remarks:'',
  })
  const [errors, setErrors] = useState({})

  /* ── Cascade selectors ───────────────────────────────── */
  const { data: depts } = useQuery({
    queryKey: ['depts-active'],
    queryFn: () => academicService.departments.list({ status:'active', page_size:200 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const { data: courses } = useQuery({
    queryKey: ['courses-by-dept', form.department],
    queryFn: () => academicService.courses.list({ department: form.department, status:'active', page_size:100 }).then(r => r.data.results),
    enabled: !!form.department,
  })

  const { data: branches } = useQuery({
    queryKey: ['branches-by-course', form.course],
    queryFn: () => academicService.branches.list({ course: form.course, status:'active', page_size:100 }).then(r => r.data.results),
    enabled: !!form.course,
  })

  const { data: semesters } = useQuery({
    queryKey: ['semesters-by-course', form.course],
    queryFn: () => academicService.semesters.list({ course: form.course, status:'active', page_size:50 }).then(r => r.data.results),
    enabled: !!form.course,
  })

  const { data: acYears } = useQuery({
    queryKey: ['academic-years'],
    queryFn: () => academicService.years.list({ status:'active', page_size:50 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  // Reset downstream when parent changes
  useEffect(() => { setForm(f => ({ ...f, course:'', branch:'', current_semester:'' })) }, [form.department])
  useEffect(() => { setForm(f => ({ ...f, branch:'', current_semester:'' })) }, [form.course])

  const set = (k, v) => {
    setForm(f => ({ ...f, [k]: v }))
    if (errors[k]) setErrors(e => ({ ...e, [k]: undefined }))
  }

  /* ── Validation ────────────────────────────────────────── */
  function validate() {
    const errs = {}
    if (!form.roll_number.trim()) errs.roll_number = 'Roll number is required.'
    if (!form.full_name.trim())   errs.full_name   = 'Full name is required.'
    if (!form.institutional_email.trim()) errs.institutional_email = 'Institutional email is required.'
    else if (!/\S+@\S+\.\S+/.test(form.institutional_email)) errs.institutional_email = 'Enter a valid email address.'
    if (!form.department)      errs.department       = 'Department is required.'
    if (!form.course)          errs.course           = 'Course is required.'
    if (!form.current_semester)errs.current_semester = 'Semester is required.'
    if (!form.academic_year)   errs.academic_year    = 'Academic year is required.'
    if (!form.admission_year)  errs.admission_year   = 'Admission year is required.'
    return errs
  }

  const createMutation = useMutation({
    mutationFn: (data) => studentService.create(data),
    onSuccess: (res) => {
      toast.success(`Student "${form.full_name}" created successfully!`)
      qc.invalidateQueries(['students'])
      qc.invalidateQueries(['student-dashboard'])
      navigate(`/students/${res.data.data.id}`)
    },
    onError: (err) => {
      const serverErrors = err.response?.data?.details || {}
      setErrors(serverErrors)
      toast.error(err.response?.data?.message || 'Failed to create student. Please check the form.')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length) { setErrors(errs); return }
    const payload = { ...form }
    if (!payload.branch) delete payload.branch
    if (!payload.personal_email) delete payload.personal_email
    if (!payload.date_of_birth) delete payload.date_of_birth
    createMutation.mutate(payload)
  }

  const isSubmitting = createMutation.isLoading

  return (
    <div>
      {/* ── Page header ───────────────────────────────── */}
      <div className="page-header">
        <div>
          <Link to="/students/list" className="btn btn-secondary btn-sm" style={{ marginBottom: 8 }}>
            <HiOutlineChevronLeft size={14} /> Back to Students
          </Link>
          <div className="page-title">Add New Student</div>
          <div className="page-subtitle">Fill in the student's academic and personal details</div>
        </div>
        <div className="page-actions">
          <button type="button" onClick={() => navigate(-1)} className="btn btn-secondary">
            Cancel
          </button>
          <button
            type="submit" form="add-student-form"
            className={`btn btn-primary${isSubmitting ? ' btn-loading' : ''}`}
            disabled={isSubmitting}
          >
            <HiOutlineSave size={16} />
            {isSubmitting ? 'Saving…' : 'Save Student'}
          </button>
        </div>
      </div>

      <form id="add-student-form" onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-5)' }}>

          {/* ── Identity ──────────────────────────────── */}
          <motion.div className="card" initial={{ opacity:0, y:12 }} animate={{ opacity:1, y:0 }} transition={{ delay:0.05 }}>
            <div className="card-header">
              <span className="card-title">🪪 Identity</span>
            </div>
            <Field label="Roll Number" required error={errors.roll_number}>
              <input className={`form-input${errors.roll_number ? ' error' : ''}`}
                placeholder="e.g. CSE2024001"
                value={form.roll_number} onChange={e => set('roll_number', e.target.value.toUpperCase())} />
            </Field>
            <Field label="Full Name" required error={errors.full_name}>
              <input className={`form-input${errors.full_name ? ' error' : ''}`}
                placeholder="Student's legal full name"
                value={form.full_name} onChange={e => set('full_name', e.target.value)} />
            </Field>
            <Field label="Gender">
              <select className="form-select" value={form.gender} onChange={e => set('gender', e.target.value)}>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="prefer_not_to_say">Prefer not to say</option>
              </select>
            </Field>
            <Field label="Date of Birth" error={errors.date_of_birth}>
              <input className="form-input" type="date"
                value={form.date_of_birth} onChange={e => set('date_of_birth', e.target.value)} />
            </Field>
            <Field label="Blood Group">
              <select className="form-select" value={form.blood_group} onChange={e => set('blood_group', e.target.value)}>
                {['A+','A-','B+','B-','O+','O-','AB+','AB-','unknown'].map(g => (
                  <option key={g} value={g}>{g}</option>
                ))}
              </select>
            </Field>
          </motion.div>

          {/* ── Contact ──────────────────────────────── */}
          <motion.div className="card" initial={{ opacity:0, y:12 }} animate={{ opacity:1, y:0 }} transition={{ delay:0.1 }}>
            <div className="card-header">
              <span className="card-title">📧 Contact</span>
            </div>
            <Field label="Institutional Email" required error={errors.institutional_email}
              hint="Must be the college-issued email address">
              <input className={`form-input${errors.institutional_email ? ' error' : ''}`}
                type="email" placeholder="student@college.edu"
                value={form.institutional_email} onChange={e => set('institutional_email', e.target.value.toLowerCase())} />
            </Field>
            <Field label="Personal Email" error={errors.personal_email}>
              <input className="form-input" type="email" placeholder="personal@gmail.com"
                value={form.personal_email} onChange={e => set('personal_email', e.target.value)} />
            </Field>
            <Field label="Phone" error={errors.phone}>
              <input className="form-input" type="tel" placeholder="+91 9876543210"
                value={form.phone} onChange={e => set('phone', e.target.value)} />
            </Field>
            <Field label="Guardian Name">
              <input className="form-input" placeholder="Parent / Guardian name"
                value={form.guardian_name} onChange={e => set('guardian_name', e.target.value)} />
            </Field>
            <Field label="Guardian Phone">
              <input className="form-input" type="tel"
                value={form.guardian_phone} onChange={e => set('guardian_phone', e.target.value)} />
            </Field>
          </motion.div>

          {/* ── Academic Info ─────────────────────────── */}
          <motion.div className="card" initial={{ opacity:0, y:12 }} animate={{ opacity:1, y:0 }} transition={{ delay:0.15 }}>
            <div className="card-header">
              <span className="card-title">🎓 Academic Details</span>
            </div>
            <Field label="Department" required error={errors.department}>
              <select className={`form-select${errors.department ? ' error' : ''}`}
                value={form.department} onChange={e => set('department', e.target.value)}>
                <option value="">— Select Department —</option>
                {(depts || []).map(d => (
                  <option key={d.id} value={d.id}>{d.code} — {d.name}</option>
                ))}
              </select>
            </Field>
            <Field label="Course / Program" required error={errors.course}>
              <select className={`form-select${errors.course ? ' error' : ''}`}
                value={form.course} onChange={e => set('course', e.target.value)}
                disabled={!form.department}>
                <option value="">— Select Course —</option>
                {(courses || []).map(c => (
                  <option key={c.id} value={c.id}>{c.code} — {c.name}</option>
                ))}
              </select>
            </Field>
            <Field label="Branch / Specialization">
              <select className="form-select" value={form.branch} onChange={e => set('branch', e.target.value)}
                disabled={!form.course}>
                <option value="">— No Branch / Common —</option>
                {(branches || []).map(b => (
                  <option key={b.id} value={b.id}>{b.code} — {b.name}</option>
                ))}
              </select>
            </Field>
            <Field label="Current Semester" required error={errors.current_semester}>
              <select className={`form-select${errors.current_semester ? ' error' : ''}`}
                value={form.current_semester} onChange={e => set('current_semester', e.target.value)}
                disabled={!form.course}>
                <option value="">— Select Semester —</option>
                {(semesters || []).map(s => (
                  <option key={s.id} value={s.id}>Semester {s.semester_number} {s.name ? `— ${s.name}` : ''}</option>
                ))}
              </select>
            </Field>
            <Field label="Academic Year" required error={errors.academic_year}>
              <select className={`form-select${errors.academic_year ? ' error' : ''}`}
                value={form.academic_year} onChange={e => set('academic_year', e.target.value)}>
                <option value="">— Select Year —</option>
                {(acYears || []).map(y => (
                  <option key={y.id} value={y.id}>{y.label}{y.is_current ? ' (Current)' : ''}</option>
                ))}
              </select>
            </Field>
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'var(--space-4)' }}>
              <Field label="Admission Year" required error={errors.admission_year}>
                <input className="form-input" type="number" min="2000" max="2100"
                  value={form.admission_year} onChange={e => set('admission_year', parseInt(e.target.value))} />
              </Field>
              <Field label="Enrollment Date">
                <input className="form-input" type="date"
                  value={form.enrollment_date} onChange={e => set('enrollment_date', e.target.value)} />
              </Field>
            </div>
          </motion.div>

          {/* ── Status & Notes ─────────────────────────── */}
          <motion.div className="card" initial={{ opacity:0, y:12 }} animate={{ opacity:1, y:0 }} transition={{ delay:0.2 }}>
            <div className="card-header">
              <span className="card-title">⚙ Status & Notes</span>
            </div>
            <Field label="Enrollment Status">
              <select className="form-select" value={form.status} onChange={e => set('status', e.target.value)}>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="suspended">Suspended</option>
              </select>
            </Field>
            <Field label="Exam Eligibility">
              <select className="form-select"
                value={form.is_eligible_for_exam ? 'true' : 'false'}
                onChange={e => set('is_eligible_for_exam', e.target.value === 'true')}>
                <option value="true">Eligible for Examinations</option>
                <option value="false">Not Eligible</option>
              </select>
            </Field>
            <Field label="Address">
              <textarea className="form-textarea" placeholder="Residential or permanent address"
                rows={3} value={form.address} onChange={e => set('address', e.target.value)} />
            </Field>
            <Field label="Remarks / Notes">
              <textarea className="form-textarea" placeholder="Any administrative notes…"
                rows={3} value={form.remarks} onChange={e => set('remarks', e.target.value)} />
            </Field>
          </motion.div>
        </div>

        {/* ── Submit bar ───────────────────────────────── */}
        <motion.div
          initial={{ opacity:0 }} animate={{ opacity:1 }} transition={{ delay:0.25 }}
          style={{
            display:'flex', justifyContent:'flex-end', gap:'var(--space-3)',
            marginTop:'var(--space-5)', padding:'var(--space-4) var(--space-6)',
            background:'var(--color-white)', borderRadius:'var(--radius-lg)',
            border:'1px solid var(--color-border)', boxShadow:'var(--shadow-card)',
          }}
        >
          <button type="button" onClick={() => navigate(-1)} className="btn btn-secondary" disabled={isSubmitting}>
            Cancel
          </button>
          <button
            type="submit"
            className={`btn btn-primary${isSubmitting ? ' btn-loading' : ''}`}
            disabled={isSubmitting}
          >
            <HiOutlineSave size={16} />
            {isSubmitting ? 'Saving…' : 'Create Student'}
          </button>
        </motion.div>
      </form>
    </div>
  )
}
