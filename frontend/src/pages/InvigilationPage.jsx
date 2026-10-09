import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { UserCheck, Sparkles, CheckCircle2, AlertTriangle, Shield, Clock } from 'lucide-react';

export default function InvigilationPage() {
  const [duties, setDuties] = useState([]);
  const [summary, setSummary] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState('');
  const [loading, setLoading] = useState(false);

  const loadSessions = async () => {
    try {
      const data = await api.getExamSessions();
      const list = data.results || data;
      setSessions(list);
      if (list.length > 0 && !selectedSessionId) {
        setSelectedSessionId(list[0].id);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const loadDuties = async () => {
    try {
      const [dData, sData] = await Promise.all([
        api.getInvigilatorDuties(),
        api.getInvigilationSummary()
      ]);
      setDuties(dData.results || dData);
      setSummary(sData);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadSessions();
    loadDuties();
  }, []);

  const handleAutoAllocate = async () => {
    if (!selectedSessionId) return;
    setLoading(true);
    try {
      const res = await api.autoAllocateInvigilators(selectedSessionId);
      alert(res.message);
      loadDuties();
    } catch (e) {
      alert('Allocation error: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Invigilator Allocation & Faculty Workload Roster
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 4 Module: Leave-aware duty assignments, fairness heuristics, and room staffing coverage
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <select
            className="form-select"
            style={{ width: 'auto', minWidth: '220px' }}
            value={selectedSessionId}
            onChange={(e) => setSelectedSessionId(e.target.value)}
          >
            {sessions.map((s) => (
              <option key={s.id} value={s.id}>{s.session_code}: {s.name}</option>
            ))}
          </select>

          <button
            onClick={handleAutoAllocate}
            disabled={loading}
            className="btn btn-primary"
          >
            <Sparkles size={16} color="#D4A72C" /> {loading ? 'Assigning Duties...' : 'Auto-Allocate Invigilators'}
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Total Assigned Duties</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>{summary?.total_duties ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Confirmed by Faculty</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-emerald)' }}>{summary?.confirmed_duties ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Workload Fairness</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>Balanced</div>
        </div>
      </div>

      {/* Duty Roster Table */}
      <div className="table-container" style={{ marginBottom: '2rem' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Time Slot</th>
              <th>Hall / Room</th>
              <th>Exam Paper</th>
              <th>Assigned Invigilator</th>
              <th>Duty Role</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {duties.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-muted)' }}>
                  No duties assigned yet. Click "Auto-Allocate Invigilators" above.
                </td>
              </tr>
            ) : (
              duties.map((d) => (
                <tr key={d.id}>
                  <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{d.exam_date}</td>
                  <td><span className="badge badge-neutral">{d.slot_name}</span></td>
                  <td style={{ fontWeight: 700 }}>{d.room_number}</td>
                  <td>{d.subject_code}: {d.subject_name}</td>
                  <td>
                    <div style={{ fontWeight: 600 }}>{d.faculty_name}</div>
                    <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)' }}>{d.employee_id} • {d.department_name}</div>
                  </td>
                  <td>{d.duty_role}</td>
                  <td>
                    <span className="badge badge-success">
                      {d.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Workload Distribution Grid */}
      {summary?.workload && (
        <div className="card">
          <div className="card-header">
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-forest)' }}>
              Faculty Workload Distribution Counter
            </h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>Fair Distribution Safeguard</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
            {summary.workload.map((w) => (
              <div key={w.id} style={{ padding: '0.75rem', border: '1px solid var(--color-border-light)', borderRadius: '0.5rem', backgroundColor: '#F8FAF7' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.8125rem', color: 'var(--color-forest)' }}>
                    {w.user__first_name} {w.user__last_name}
                  </span>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700 }}>
                    {w.assigned_duties} / {w.max_duties_per_term} Duties
                  </span>
                </div>
                {/* Progress bar */}
                <div style={{ width: '100%', height: '6px', backgroundColor: 'var(--color-border-light)', borderRadius: '9999px', overflow: 'hidden' }}>
                  <div style={{ width: `${Math.min((w.assigned_duties / w.max_duties_per_term) * 100, 100)}%`, height: '100%', backgroundColor: 'var(--color-emerald)', borderRadius: '9999px' }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
