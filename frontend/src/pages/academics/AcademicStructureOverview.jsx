/** ExamForge M2 — Academic Structure Tree Overview */
import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { HiOutlineChevronDown, HiOutlineChevronRight, HiOutlineOfficeBuilding, HiOutlineBookOpen, HiOutlineTemplate, HiOutlineCalendar, HiOutlineAcademicCap } from 'react-icons/hi'
import academicService from '../../services/academicService.js'

function SubjectRow({ subject }) {
  const typeColors = { theory: 'badge-forest', lab: 'badge-amber', project: 'badge-success', elective: 'badge-neutral', seminar: 'badge-warning' }
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '5px 0', marginLeft: 8 }}>
      <HiOutlineAcademicCap size={13} color="var(--color-gray)" />
      <code style={{ fontFamily: 'monospace', fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-forest)', minWidth: 64 }}>{subject.code}</code>
      <span style={{ fontSize: '0.8125rem' }}>{subject.name}</span>
      <span className={`badge ${typeColors[subject.type] || 'badge-neutral'}`} style={{ fontSize: '0.65rem', marginLeft: 'auto' }}>{subject.type}</span>
      <span style={{ fontSize: '0.75rem', color: 'var(--color-gray)', width: 40 }}>{subject.credits}cr</span>
    </div>
  )
}

function SemesterNode({ semester, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div style={{ marginBottom: 4 }}>
      <button onClick={() => setOpen(o => !o)}
        style={{
          display: 'flex', alignItems: 'center', gap: 8, width: '100%',
          padding: '6px 10px', borderRadius: 8, border: 'none',
          background: open ? 'var(--color-green-50)' : 'transparent',
          color: 'var(--color-charcoal)', cursor: 'pointer', fontSize: '0.8125rem', fontFamily: 'var(--font-sans)',
        }}>
        {open ? <HiOutlineChevronDown size={13} /> : <HiOutlineChevronRight size={13} />}
        <HiOutlineCalendar size={13} color="var(--color-emerald)" />
        <span style={{ fontWeight: 600 }}>Semester {semester.number}</span>
        {semester.name && <span style={{ color: 'var(--color-gray)', fontWeight: 400 }}>— {semester.name}</span>}
        <span style={{ marginLeft: 'auto', color: 'var(--color-gray)', fontSize: '0.75rem' }}>{semester.subjects?.length || 0} subjects</span>
      </button>
      <AnimatePresence>
        {open && semester.subjects?.length > 0 && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.15 }} style={{ overflow: 'hidden', paddingLeft: 28 }}>
            {semester.subjects.map(sub => <SubjectRow key={sub.id} subject={sub} />)}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

function CourseNode({ course }) {
  const [open, setOpen] = useState(false)
  return (
    <div style={{ marginBottom: 4 }}>
      <button onClick={() => setOpen(o => !o)}
        style={{
          display: 'flex', alignItems: 'center', gap: 8, width: '100%',
          padding: '8px 12px', borderRadius: 10, border: 'none',
          background: open ? 'var(--color-sage-light)' : 'var(--color-bg)',
          color: 'var(--color-charcoal)', cursor: 'pointer', fontSize: '0.875rem', fontFamily: 'var(--font-sans)',
        }}>
        {open ? <HiOutlineChevronDown size={14} /> : <HiOutlineChevronRight size={14} />}
        <HiOutlineBookOpen size={14} color="var(--color-emerald)" />
        <span style={{ fontWeight: 700 }}>{course.code}</span>
        <span style={{ color: 'var(--color-gray)', fontWeight: 400 }}>{course.name}</span>
        <span style={{ marginLeft: 'auto', color: 'var(--color-gray)', fontSize: '0.75rem' }}>
          {course.duration_years}Y · {course.semesters?.length || 0} sems
        </span>
        {course.branches?.length > 0 && (
          <span style={{ fontSize: '0.7rem', color: 'var(--color-amber-600)' }}>{course.branches.length} branches</span>
        )}
      </button>
      <AnimatePresence>
        {open && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.18 }} style={{ overflow: 'hidden', paddingLeft: 24 }}>
            {course.branches?.length > 0 && (
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', padding: '8px 0 4px' }}>
                {course.branches.map(b => (
                  <span key={b.id} style={{ display: 'flex', alignItems: 'center', gap: 4, padding: '2px 8px', borderRadius: 'var(--radius-full)', background: 'var(--color-amber-100)', color: '#92400E', fontSize: '0.75rem' }}>
                    <HiOutlineTemplate size={11} />{b.code} — {b.name}
                  </span>
                ))}
              </div>
            )}
            {(course.semesters || []).map(sem => <SemesterNode key={sem.id} semester={sem} />)}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

function DeptNode({ dept }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="card" style={{ marginBottom: 'var(--space-3)' }}>
      <button onClick={() => setOpen(o => !o)}
        style={{
          display: 'flex', alignItems: 'center', gap: 12, width: '100%',
          background: 'none', border: 'none', cursor: 'pointer', padding: 0, fontFamily: 'var(--font-sans)',
        }}>
        <div style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--color-sage)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          <HiOutlineOfficeBuilding size={18} color="var(--color-emerald)" />
        </div>
        <div style={{ flex: 1, textAlign: 'left' }}>
          <div style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--color-charcoal)' }}>{dept.code} — {dept.name}</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--color-gray)' }}>{dept.courses?.length || 0} courses</div>
        </div>
        {open ? <HiOutlineChevronDown size={18} color="var(--color-gray)" /> : <HiOutlineChevronRight size={18} color="var(--color-gray)" />}
      </button>
      <AnimatePresence>
        {open && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }} style={{ overflow: 'hidden', marginTop: 12 }}>
            {dept.courses?.length === 0 ? (
              <div style={{ color: 'var(--color-gray)', fontSize: '0.875rem', padding: '8px 0' }}>No courses in this department.</div>
            ) : (
              (dept.courses || []).map(course => <CourseNode key={course.id} course={course} />)
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default function AcademicStructureOverview() {
  const { data, isLoading } = useQuery({
    queryKey: ['academic-structure'],
    queryFn: () => academicService.structure().then(r => r.data.data),
    staleTime: 120_000,
  })

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="page-title">Academic Structure</div>
          <div className="page-subtitle">Full hierarchy: Departments → Courses → Branches → Semesters → Subjects</div>
        </div>
      </div>
      {isLoading ? (
        Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="skeleton" style={{ height: 80, borderRadius: 14, marginBottom: 12 }} />
        ))
      ) : !data?.length ? (
        <div className="empty-state">
          <div className="empty-state-icon">🏛️</div>
          <div className="empty-state-title">No academic structure yet</div>
          <div className="empty-state-text">Start by adding departments and courses.</div>
        </div>
      ) : (
        data.map(dept => <DeptNode key={dept.id} dept={dept} />)
      )}
    </div>
  )
}
