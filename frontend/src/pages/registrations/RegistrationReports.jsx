/** ExamForge M2 — Registration Reports Page */
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from 'recharts'
import { HiOutlineDocumentReport, HiOutlineRefresh } from 'react-icons/hi'
import academicService from '../../services/academicService.js'
import registrationService from '../../services/registrationService.js'

const COLORS = ['#15803D','#D4A72C','#166534','#F59E0B','#14532D','#D97706']

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div style={{ background: 'var(--color-white)', border: '1px solid var(--color-border)', borderRadius: 10, padding: '8px 12px', fontSize: '0.8125rem', boxShadow: 'var(--shadow-md)' }}>
      <div style={{ fontWeight: 600 }}>{label}</div>
      {payload.map((p, i) => <div key={i} style={{ color: p.color }}>{p.name}: <strong>{p.value}</strong></div>)}
    </div>
  )
}

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.07 } } }
const fadeUp  = { hidden: { opacity: 0, y: 12 }, show: { opacity: 1, y: 0, transition: { duration: 0.25 } } }

export default function RegistrationReports() {
  const [acYear, setAcYear] = useState('')

  const { data: years } = useQuery({
    queryKey: ['academic-years'],
    queryFn: () => academicService.years.list({ page_size: 50 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const { data: summaryData, isLoading: summaryLoading, refetch } = useQuery({
    queryKey: ['reg-summary-report', acYear],
    queryFn: () => registrationService.reports.summary({ academic_year: acYear || undefined }).then(r => r.data.data),
    staleTime: 60_000,
  })

  const { data: deptData, isLoading: deptLoading } = useQuery({
    queryKey: ['reg-dept-report', acYear],
    queryFn: () => registrationService.reports.byDept({ academic_year: acYear || undefined }).then(r => r.data.data),
    staleTime: 60_000,
  })

  const deptBar = (deptData || []).map(r => ({
    name: r.department__code || r.dept,
    'Subject Reg.': r.subject_count || 0,
    'Exam Reg.':    r.exam_count    || 0,
  }))

  const statusPie = [
    { name: 'Registered',  value: summaryData?.by_status?.registered  || 0 },
    { name: 'Confirmed',   value: summaryData?.by_status?.confirmed   || 0 },
    { name: 'Cancelled',   value: summaryData?.by_status?.cancelled   || 0 },
  ].filter(s => s.value > 0)

  return (
    <motion.div variants={stagger} initial="hidden" animate="show">
      <motion.div variants={fadeUp} className="page-header">
        <div>
          <div className="page-title">
            <HiOutlineDocumentReport size={24} color="var(--color-emerald)" />
            Registration Reports
          </div>
          <div className="page-subtitle">Analytics and summaries for registration data</div>
        </div>
        <div className="page-actions">
          <select className="form-select" style={{ maxWidth: 200 }} value={acYear} onChange={e => setAcYear(e.target.value)}>
            <option value="">All Academic Years</option>
            {(years || []).map(y => <option key={y.id} value={y.id}>{y.label}</option>)}
          </select>
          <button className="btn btn-secondary btn-sm" onClick={() => refetch()}>
            <HiOutlineRefresh size={15} /> Refresh
          </button>
        </div>
      </motion.div>

      {/* Summary numbers */}
      <motion.div variants={fadeUp} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--space-4)', marginBottom: 'var(--space-5)' }}>
        {[
          { label: 'Total Subject Regs.', value: summaryData?.total_subject, color: 'var(--color-emerald)'  },
          { label: 'Total Exam Regs.',    value: summaryData?.total_exam,    color: 'var(--color-forest)'   },
          { label: 'Active Students',     value: summaryData?.unique_students, color: 'var(--color-gold)'   },
          { label: 'Subjects Covered',    value: summaryData?.unique_subjects, color: 'var(--color-amber)'  },
        ].map(s => (
          <div key={s.label} className="stat-card" style={{ borderLeft: `4px solid ${s.color}` }}>
            <div className="stat-content">
              <div className="stat-value" style={{ color: s.color }}>
                {summaryLoading ? <div className="skeleton skeleton-text lg" style={{ width: 60 }} /> : (s.value ?? '—')}
              </div>
              <div className="stat-label">{s.label}</div>
            </div>
          </div>
        ))}
      </motion.div>

      {/* Charts */}
      <motion.div variants={fadeUp} style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 'var(--space-4)' }}>
        <div className="card">
          <div className="card-header"><span className="card-title">Registrations by Department</span></div>
          {deptLoading
            ? <div className="skeleton" style={{ height: 260, borderRadius: 8 }} />
            : deptBar.length === 0
            ? <div className="empty-state" style={{ padding: '48px 0' }}><div style={{ color: 'var(--color-gray)' }}>No data for selected period</div></div>
            : (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={deptBar} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
                  <XAxis dataKey="name" tick={{ fontSize: 11, fill: 'var(--color-gray)' }} />
                  <YAxis tick={{ fontSize: 11, fill: 'var(--color-gray)' }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="Subject Reg." fill="var(--color-emerald)" radius={[3, 3, 0, 0]} />
                  <Bar dataKey="Exam Reg."    fill="var(--color-gold)"    radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )
          }
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Status Breakdown</span></div>
          {summaryLoading
            ? <div className="skeleton" style={{ height: 260, borderRadius: 8 }} />
            : statusPie.length === 0
            ? <div className="empty-state" style={{ padding: '48px 0' }}><div style={{ color: 'var(--color-gray)' }}>No data yet</div></div>
            : (
              <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                  <Pie data={statusPie} cx="50%" cy="50%" innerRadius={65} outerRadius={95} paddingAngle={3} dataKey="value">
                    {statusPie.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Legend formatter={(val) => <span style={{ fontSize: '0.8125rem' }}>{val}</span>} />
                  <Tooltip content={<CustomTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            )
          }
        </div>
      </motion.div>

      {/* Department table */}
      {(deptData || []).length > 0 && (
        <motion.div variants={fadeUp} className="card" style={{ marginTop: 'var(--space-4)' }}>
          <div className="card-header"><span className="card-title">Department-wise Breakdown</span></div>
          <div className="table-wrapper" style={{ border: 'none', boxShadow: 'none' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Department</th><th>Subject Registrations</th>
                  <th>Exam Registrations</th><th>Unique Students</th>
                </tr>
              </thead>
              <tbody>
                {(deptData || []).map((r, i) => (
                  <tr key={i}>
                    <td><span className="badge badge-forest">{r.department__code || r.dept}</span></td>
                    <td><strong>{r.subject_count || 0}</strong></td>
                    <td><strong>{r.exam_count || 0}</strong></td>
                    <td>{r.unique_students || 0}</td>
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
