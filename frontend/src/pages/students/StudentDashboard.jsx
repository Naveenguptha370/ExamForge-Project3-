/**
 * ExamForge M2 — Student Dashboard
 * Real data from /api/v1/students/dashboard/
 */

import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from 'recharts'
import {
  HiOutlineUsers, HiOutlineUserAdd, HiOutlineUserRemove,
  HiOutlineAcademicCap, HiOutlineCheckCircle, HiOutlineUpload,
  HiOutlineClock, HiOutlineChevronRight,
} from 'react-icons/hi'
import toast from 'react-hot-toast'

import studentService from '../../services/studentService.js'
import StatCard       from '../../components/shared/StatCard.jsx'

/* ── Color palette for charts — no blue ──────────────────── */
const CHART_COLORS = [
  '#15803D','#D4A72C','#16A34A','#D97706',
  '#14532D','#F59E0B','#166534','#92400E',
]

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.07 } },
}
const item = {
  hidden: { opacity: 0, y: 16 },
  show:   { opacity: 1, y: 0, transition: { duration: 0.3 } },
}

/* ── Custom Tooltip ──────────────────────────────────────── */
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'var(--color-white)', border: '1px solid var(--color-border)',
      borderRadius: 10, padding: '10px 14px', fontSize: '0.8125rem',
      boxShadow: 'var(--shadow-md)',
    }}>
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color }}>
          {p.name}: <strong>{p.value}</strong>
        </div>
      ))}
    </div>
  )
}

export default function StudentDashboard() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['student-dashboard'],
    queryFn:  () => studentService.dashboard().then(r => r.data.data),
    staleTime: 60_000,
    onError:   () => toast.error('Failed to load dashboard data.'),
  })

  const d = data || {}

  /* ── Pie chart data for status breakdown ─────────────── */
  const statusPie = [
    { name: 'Active',     value: d.active_students    || 0 },
    { name: 'Inactive',   value: d.inactive_students  || 0 },
    { name: 'Graduated',  value: d.graduated_students || 0 },
  ].filter(s => s.value > 0)

  const deptBar = (d.students_by_department || []).map(r => ({
    name: r.department__code || r.dept,
    Students: r.count,
  }))

  const semBar = (d.students_by_semester || []).map(r => ({
    name: `Sem ${r.current_semester__semester_number}`,
    Students: r.count,
  }))

  return (
    <motion.div variants={container} initial="hidden" animate="show">

      {/* ── Page header ────────────────────────────────── */}
      <motion.div variants={item} className="page-header">
        <div>
          <div className="page-title">
            <HiOutlineUsers size={26} color="var(--color-emerald)" />
            Student Management
          </div>
          <div className="page-subtitle">
            Real-time enrollment statistics and recent activity
          </div>
        </div>
        <div className="page-actions">
          <Link to="/students/import" className="btn btn-secondary">
            <HiOutlineUpload size={16} />
            Import CSV
          </Link>
          <Link to="/students/add" className="btn btn-primary">
            <HiOutlineUserAdd size={16} />
            Add Student
          </Link>
        </div>
      </motion.div>

      {/* ── Stat cards ─────────────────────────────────── */}
      <motion.div
        variants={item}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: 'var(--space-4)', marginBottom: 'var(--space-6)',
        }}
      >
        <StatCard label="Total Students"    value={d.total_students}          icon={HiOutlineUsers}       variant="green"  loading={isLoading} />
        <StatCard label="Active Students"   value={d.active_students}         icon={HiOutlineCheckCircle} variant="forest" loading={isLoading} />
        <StatCard label="Exam Eligible"     value={d.exam_eligible_students}  icon={HiOutlineAcademicCap} variant="amber"  loading={isLoading} />
        <StatCard label="Inactive"          value={d.inactive_students}       icon={HiOutlineUserRemove}  variant="error"  loading={isLoading} />
        <StatCard label="This Year Intake"  value={d.this_year_enrollments}   icon={HiOutlineClock}       variant="gold"   loading={isLoading} />
      </motion.div>

      {/* ── Charts row ─────────────────────────────────── */}
      <motion.div
        variants={item}
        style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)', marginBottom: 'var(--space-4)' }}
      >
        {/* Students by Department */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Students by Department</span>
          </div>
          {isLoading ? (
            <div className="skeleton" style={{ height: 240, borderRadius: 8 }} />
          ) : deptBar.length === 0 ? (
            <div className="empty-state" style={{ padding: '40px 0' }}>
              <div style={{ color: 'var(--color-gray)', fontSize: '0.875rem' }}>No department data yet</div>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={deptBar} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
                <XAxis dataKey="name" tick={{ fontSize: 12, fill: 'var(--color-gray)' }} />
                <YAxis tick={{ fontSize: 12, fill: 'var(--color-gray)' }} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="Students" fill="var(--color-emerald)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Enrollment Status Pie */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Enrollment Status</span>
          </div>
          {isLoading ? (
            <div className="skeleton" style={{ height: 240, borderRadius: 8 }} />
          ) : statusPie.length === 0 ? (
            <div className="empty-state" style={{ padding: '40px 0' }}>
              <div style={{ color: 'var(--color-gray)', fontSize: '0.875rem' }}>No data yet</div>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie
                  data={statusPie} cx="50%" cy="50%"
                  innerRadius={60} outerRadius={90}
                  paddingAngle={3} dataKey="value"
                >
                  {statusPie.map((_, i) => (
                    <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                  ))}
                </Pie>
                <Legend
                  formatter={(val) => (
                    <span style={{ fontSize: '0.8125rem', color: 'var(--color-charcoal)' }}>{val}</span>
                  )}
                />
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
      </motion.div>

      {/* ── Semester distribution + Recent enrollments ── */}
      <motion.div
        variants={item}
        style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 'var(--space-4)' }}
      >
        {/* Semester bar */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Active Students by Semester</span>
          </div>
          {isLoading ? (
            <div className="skeleton" style={{ height: 200, borderRadius: 8 }} />
          ) : semBar.length === 0 ? (
            <div className="empty-state" style={{ padding: '30px 0' }}>
              <div style={{ color: 'var(--color-gray)', fontSize: '0.875rem' }}>No semester data yet</div>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={semBar} layout="vertical" margin={{ top: 0, right: 16, left: 8, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 11, fill: 'var(--color-gray)' }} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 11, fill: 'var(--color-gray)' }} width={52} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="Students" fill="var(--color-gold)" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Recent Enrollments */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Recent Enrollments</span>
            <Link to="/students/list" style={{
              fontSize: '0.8rem', color: 'var(--color-emerald)',
              display: 'flex', alignItems: 'center', gap: 2, fontWeight: 500,
            }}>
              View all <HiOutlineChevronRight size={14} />
            </Link>
          </div>
          <div>
            {isLoading ? (
              Array.from({ length: 4 }).map((_, i) => (
                <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 12, alignItems: 'center' }}>
                  <div className="skeleton" style={{ width: 34, height: 34, borderRadius: '50%' }} />
                  <div style={{ flex: 1 }}>
                    <div className="skeleton skeleton-text" style={{ width: '70%' }} />
                    <div className="skeleton skeleton-text sm" style={{ width: '50%' }} />
                  </div>
                </div>
              ))
            ) : (d.recent_enrollments || []).length === 0 ? (
              <div style={{ color: 'var(--color-gray)', fontSize: '0.875rem', textAlign: 'center', padding: '24px 0' }}>
                No recent enrollments
              </div>
            ) : (
              (d.recent_enrollments || []).slice(0, 6).map((s, i) => (
                <Link
                  key={i}
                  to={`/students/${s.id || i}`}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 10,
                    padding: '8px 0', textDecoration: 'none',
                    borderBottom: i < 5 ? '1px solid var(--color-border)' : 'none',
                  }}
                >
                  <div style={{
                    width: 34, height: 34, borderRadius: '50%', flexShrink: 0,
                    background: `hsl(${(i * 47) % 360},50%,88%)`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontWeight: 700, fontSize: '0.75rem', color: 'var(--color-charcoal)',
                  }}>
                    {s.full_name?.[0] || '?'}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{
                      fontSize: '0.8125rem', fontWeight: 600,
                      color: 'var(--color-charcoal)', overflow: 'hidden',
                      textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                    }}>
                      {s.full_name}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--color-gray)' }}>
                      {s.department__code} · {s.course__code}
                    </div>
                  </div>
                  <HiOutlineChevronRight size={14} color="var(--color-gray)" />
                </Link>
              ))
            )}
          </div>
        </div>
      </motion.div>

      {/* ── Import log warning ─────────────────────────── */}
      {!isLoading && d.import_logs_pending > 0 && (
        <motion.div variants={item} style={{ marginTop: 'var(--space-4)' }}>
          <div style={{
            background: 'var(--color-amber-100)', border: '1px solid var(--color-amber)',
            borderRadius: 'var(--radius-lg)', padding: 'var(--space-4)',
            display: 'flex', alignItems: 'center', gap: 12,
          }}>
            <HiOutlineClock size={20} color="var(--color-amber-600)" />
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 600, fontSize: '0.875rem', color: '#92400E' }}>
                {d.import_logs_pending} import job{d.import_logs_pending > 1 ? 's' : ''} pending
              </div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--color-gray)' }}>
                Some bulk import operations are still processing.
              </div>
            </div>
            <Link to="/students/import" className="btn btn-amber btn-sm">View Imports</Link>
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}
