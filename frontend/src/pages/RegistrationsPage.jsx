import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Layers, AlertTriangle, CheckCircle2, Search, Filter } from 'lucide-react';

export default function RegistrationsPage() {
  const [registrations, setRegistrations] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [eligibilityFilter, setEligibilityFilter] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      let q = '';
      if (eligibilityFilter) q = `?eligibility_status=${eligibilityFilter}`;
      const data = await api.getSubjectRegistrations(q);
      setRegistrations(data.results || data);
      const sum = await api.getRegistrationSummary();
      setSummary(sum);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [eligibilityFilter]);

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
          Subject Registrations & Examination Eligibility
        </h2>
        <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
          Member 2 Module: Student-subject enrollments, attendance % tracking, and automatic hall ticket eligibility gatekeeping
        </p>
      </div>

      {/* Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Total Registrations</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>{summary?.total_registrations ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Eligible to Write Exam</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-emerald)' }}>{summary?.eligible_registrations ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Attendance Shortage (&lt;75%)</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-error)' }}>{summary?.attendance_shortage ?? 0}</div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="card" style={{ padding: '1rem', marginBottom: '1.5rem', display: 'flex', gap: '1rem' }}>
        <select
          className="form-select"
          style={{ width: 'auto', minWidth: '240px' }}
          value={eligibilityFilter}
          onChange={(e) => setEligibilityFilter(e.target.value)}
        >
          <option value="">All Eligibility Categories</option>
          <option value="ELIGIBLE">Eligible (Attendance ≥ 75%)</option>
          <option value="ATTENDANCE_SHORTAGE">Attendance Shortage (&lt; 75%)</option>
          <option value="FEES_DUE">Institutional Fees Pending</option>
        </select>
      </div>

      {/* Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Roll Number</th>
              <th>Student Name</th>
              <th>Subject Paper</th>
              <th>Semester</th>
              <th>Attendance %</th>
              <th>Internal Marks</th>
              <th>Eligibility Status</th>
            </tr>
          </thead>
          <tbody>
            {registrations.map((r) => (
              <tr key={r.id}>
                <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{r.student_roll}</td>
                <td style={{ fontWeight: 600 }}>{r.student_name}</td>
                <td>{r.subject_code}: {r.subject_name}</td>
                <td>{r.semester_name}</td>
                <td>
                  <span style={{ fontWeight: 700, color: Number(r.attendance_percentage) >= 75 ? 'var(--color-emerald)' : 'var(--color-error)' }}>
                    {r.attendance_percentage}%
                  </span>
                </td>
                <td>{r.internal_marks} / 30</td>
                <td>
                  <span className={r.eligibility_status === 'ELIGIBLE' ? 'badge badge-success' : 'badge badge-danger'}>
                    {r.eligibility_status === 'ELIGIBLE' ? 'Eligible' : 'Attendance Shortage'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
