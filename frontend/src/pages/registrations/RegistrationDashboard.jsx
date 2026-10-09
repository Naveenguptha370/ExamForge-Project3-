/** ExamForge M2 — Registration Dashboard */
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { HiOutlinePencilAlt, HiOutlineClipboardCheck, HiOutlineBookOpen, HiOutlineClipboardList, HiOutlineDocumentReport, HiOutlineChevronRight } from 'react-icons/hi'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import registrationService from '../../services/registrationService.js'
import StatCard from '../../components/shared/StatCard.jsx'

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.07 } } }
const fadeUp  = { hidden: { opacity: 0, y: 12 }, show: { opacity: 1, y: 0, transition: { duration: 0.25 } } }

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
  { label: 'Register Subjects', to: '/registrations/subjects/register',  icon: HiOutlineBookOpen,       desc: 'Assign subjects to students' },
  { label: 'Register for Exam',  to: '/registrations/exams/register',    icon: HiOutlinePencilAlt,      desc: 'Exam registrations'         },
  { label: 'All Registrations',  to: '/registrations/list',              icon: HiOutlineClipboardList,  desc: 'View and manage all records' },
  { label: 'Bulk Register',      to: '/registrations/bulk',              icon: HiOutlineClipboardCheck, desc: 'CSV bulk registration'       },
  { label: 'History',            to: '/registrations/history',           icon: HiOutlineClipboardList,  desc: 'Past registration logs'      },
  { label: 'Reports',            to: '/registrations/reports',           icon: HiOutlineDocumentReport, desc: 'Registration analytics'      },
]

export default function RegistrationDashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ['registration-dashboard'],
    queryFn: () => registrationService.dashboard().then(r => r.data.data),
    staleTime: 60_000,
  })
  const d = data || {}

  const deptBar = (d.registrations_by_department || []).map(r => ({
    name: r.department__code || r.dept,
    Registrations: r.count,
  }))

  return (
    <motion.div variants={stagger} initial="hidden" animate="show">
      <motion.div variants={fadeUp} className="page-header">
        <div>
          <div className="page-title">
            <HiOutlinePencilAlt size={24} color="var(--color-emerald)" />
            Registration Management
          </div>
          <div className="page-subtitle">Subject and exam registrations overview</div>
        </div>
        <div className="page-actions">
          <Link to="/registrations/subjects/register" className="btn btn-primary btn-sm">
            <HiOutlineBookOpen size={15} /> Register Subjects
          </Link>
        </div>
      </motion.div>

      {/* Stats */}
      <motion.div variants={fadeUp} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--space-4)', marginBottom: 'var(--space-5)' }}>
        <StatCard label="Total Subject Regs."  value={d.total_subject_registrations} icon={HiOutlineBookOpen}       variant="green"  loading={isLoading} />
        <StatCard label="Total Exam Regs."     value={d.total_exam_registrations}    icon={HiOutlinePencilAlt}      variant="forest" loading={isLoading} />
        <StatCard label="Active This Session"  value={d.active_registrations}        icon={HiOutlineClipboardCheck} variant="amber"  loading={isLoading} />
        <StatCard label="Pending Bulk Jobs"    value={d.pending_bulk_jobs}           icon={HiOutlineClipboardList}  variant="error"  loading={isLoading} />
      </motion.div>

      {/* Chart + Quick links */}
      <motion.div variants={fadeUp} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)', marginBottom: 'var(--space-4)' }}>
        <div className="card">
          <div className="card-header"><span className="card-title">Registrations by Department</span></div>
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
                  <Bar dataKey="Registrations" fill="var(--color-forest)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )
          }
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Quick Actions</span></div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-3)' }}>
            {QUICK_LINKS.map(link => (
              <Link key={link.to} to={link.to}
                style={{
                  display: 'flex', alignItems: 'center', gap: 10, padding: '12px',
                  borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)',
                  textDecoration: 'none', transition: 'all 0.15s', background: 'var(--color-bg)',
                }}
                onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--color-emerald)'; e.currentTarget.style.background = 'var(--color-sage-light)' }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--color-border)'; e.currentTarget.style.background = 'var(--color-bg)' }}
              >
                <div style={{ width: 34, height: 34, borderRadius: 8, background: 'var(--color-sage)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-emerald)', flexShrink: 0 }}>
                  <link.icon size={16} />
                </div>
                <div>
                  <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>{link.label}</div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--color-gray)' }}>{link.desc}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Recent registrations */}
      {!isLoading && (d.recent_registrations || []).length > 0 && (
        <motion.div variants={fadeUp} className="card">
          <div className="card-header">
            <span className="card-title">Recent Registrations</span>
            <Link to="/registrations/list" style={{ fontSize: '0.8rem', color: 'var(--color-emerald)', display: 'flex', alignItems: 'center', gap: 2 }}>
              View all <HiOutlineChevronRight size={14} />
            </Link>
          </div>
          <div className="table-wrapper" style={{ border: 'none', boxShadow: 'none' }}>
            <table className="data-table">
              <thead>
                <tr><th>Student</th><th>Subject</th><th>Type</th><th>Status</th><th>Date</th></tr>
              </thead>
              <tbody>
                {d.recent_registrations.map((r, i) => (
                  <tr key={i}>
                    <td style={{ fontWeight: 500 }}>{r.student_name || '—'}</td>
                    <td>{r.subject_code} — {r.subject_name}</td>
                    <td><span className="badge badge-forest">{r.type}</span></td>
                    <td><span className="badge badge-success">{r.status}</span></td>
                    <td className="td-muted">{r.registration_date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}
