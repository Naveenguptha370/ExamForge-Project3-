/**
 * ExamForge M2 — Academic Dashboard Page
 */
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  HiOutlineOfficeBuilding, HiOutlineBookOpen, HiOutlineTemplate,
  HiOutlineCalendar, HiOutlineCollection, HiOutlineAcademicCap,
  HiOutlineChevronRight,
} from 'react-icons/hi'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import academicService from '../../services/academicService.js'
import StatCard from '../../components/shared/StatCard.jsx'

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.07 } } }
const fadeUp  = { hidden: { opacity: 0, y: 14 }, show: { opacity: 1, y: 0, transition: { duration: 0.28 } } }

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div style={{ background: 'var(--color-white)', border: '1px solid var(--color-border)', borderRadius: 10, padding: '8px 12px', fontSize: '0.8125rem', boxShadow: 'var(--shadow-md)' }}>
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{label}</div>
      {payload.map((p, i) => <div key={i} style={{ color: p.color }}>{p.name}: <strong>{p.value}</strong></div>)}
    </div>
  )
}

const QUICK_LINKS = [
  { label: 'Departments',    to: '/academics/departments', icon: HiOutlineOfficeBuilding, desc: 'Manage departments'      },
  { label: 'Courses',        to: '/academics/courses',     icon: HiOutlineBookOpen,       desc: 'Programs & degrees'      },
  { label: 'Branches',       to: '/academics/branches',    icon: HiOutlineTemplate,       desc: 'Specializations'         },
  { label: 'Semesters',      to: '/academics/semesters',   icon: HiOutlineCalendar,       desc: 'Semester definitions'    },
  { label: 'Academic Years', to: '/academics/years',       icon: HiOutlineCollection,     desc: 'Year configuration'      },
  { label: 'Subjects',       to: '/academics/subjects',    icon: HiOutlineAcademicCap,    desc: 'Subject catalog'         },
]

export default function AcademicDashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ['academic-dashboard'],
    queryFn: () => academicService.dashboard().then(r => r.data.data),
    staleTime: 60_000,
  })

  const d = data || {}

  const typeBar = Object.entries(d.subjects_by_type || {}).map(([type, count]) => ({
    name: type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    Subjects: count,
  }))

  const deptBar = (d.departments_summary || []).map(dep => ({
    name: dep.code,
    Courses: dep.course_count,
    Students: dep.student_count,
  }))

  return (
    <motion.div variants={stagger} initial="hidden" animate="show">
      <motion.div variants={fadeUp} className="page-header">
        <div>
          <div className="page-title">
            <HiOutlineAcademicCap size={26} color="var(--color-emerald)" />
            Academic Management
          </div>
          <div className="page-subtitle">Structure, programs, and subject catalog</div>
        </div>
        <div className="page-actions">
          <Link to="/academics/structure" className="btn btn-secondary btn-sm">View Full Structure</Link>
          <Link to="/academics/subjects" className="btn btn-primary btn-sm">
            <HiOutlineBookOpen size={15} /> Add Subject
          </Link>
        </div>
      </motion.div>

      {/* Stat cards */}
      <motion.div variants={fadeUp} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--space-4)', marginBottom: 'var(--space-5)' }}>
        <StatCard label="Departments"   value={d.active_departments}  icon={HiOutlineOfficeBuilding} variant="green"  loading={isLoading} />
        <StatCard label="Courses"       value={d.active_courses}      icon={HiOutlineBookOpen}       variant="forest" loading={isLoading} />
        <StatCard label="Branches"      value={d.total_branches}      icon={HiOutlineTemplate}       variant="amber"  loading={isLoading} />
        <StatCard label="Semesters"     value={d.total_semesters}     icon={HiOutlineCalendar}       variant="gold"   loading={isLoading} />
        <StatCard label="Active Subjects" value={d.active_subjects}   icon={HiOutlineAcademicCap}    variant="green"  loading={isLoading} />
      </motion.div>

      {/* Charts */}
      <motion.div variants={fadeUp} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)', marginBottom: 'var(--space-4)' }}>
        <div className="card">
          <div className="card-header"><span className="card-title">Departments — Courses & Students</span></div>
          {isLoading
            ? <div className="skeleton" style={{ height: 220, borderRadius: 8 }} />
            : deptBar.length === 0
            ? <div className="empty-state" style={{ padding: '40px 0' }}><div style={{ color: 'var(--color-gray)' }}>No data yet</div></div>
            : (
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={deptBar} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
                  <XAxis dataKey="name" tick={{ fontSize: 11, fill: 'var(--color-gray)' }} />
                  <YAxis tick={{ fontSize: 11, fill: 'var(--color-gray)' }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="Courses"  fill="var(--color-emerald)" radius={[3, 3, 0, 0]} />
                  <Bar dataKey="Students" fill="var(--color-gold)"    radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )
          }
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Subjects by Type</span></div>
          {isLoading
            ? <div className="skeleton" style={{ height: 220, borderRadius: 8 }} />
            : typeBar.length === 0
            ? <div className="empty-state" style={{ padding: '40px 0' }}><div style={{ color: 'var(--color-gray)' }}>No subjects yet</div></div>
            : (
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={typeBar} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
                  <XAxis dataKey="name" tick={{ fontSize: 10, fill: 'var(--color-gray)' }} />
                  <YAxis tick={{ fontSize: 11, fill: 'var(--color-gray)' }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="Subjects" fill="var(--color-forest)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )
          }
        </div>
      </motion.div>

      {/* Quick navigation */}
      <motion.div variants={fadeUp} className="card">
        <div className="card-header"><span className="card-title">Quick Navigation</span></div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 'var(--space-3)' }}>
          {QUICK_LINKS.map(link => (
            <Link
              key={link.to}
              to={link.to}
              style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '14px', borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-border)',
                textDecoration: 'none', transition: 'all 0.15s',
                background: 'var(--color-bg)',
              }}
              onMouseEnter={e => {
                e.currentTarget.style.borderColor = 'var(--color-emerald)'
                e.currentTarget.style.background  = 'var(--color-sage-light)'
              }}
              onMouseLeave={e => {
                e.currentTarget.style.borderColor = 'var(--color-border)'
                e.currentTarget.style.background  = 'var(--color-bg)'
              }}
            >
              <div style={{
                width: 38, height: 38, borderRadius: 10, background: 'var(--color-sage)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: 'var(--color-emerald)', flexShrink: 0,
              }}>
                <link.icon size={18} />
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>{link.label}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-gray)' }}>{link.desc}</div>
              </div>
              <HiOutlineChevronRight size={14} color="var(--color-gray)" />
            </Link>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}
