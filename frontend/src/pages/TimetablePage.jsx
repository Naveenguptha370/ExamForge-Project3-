import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Sparkles, CheckCircle2, AlertTriangle, Calendar, Clock, RefreshCw, Send, ShieldCheck } from 'lucide-react';

export default function TimetablePage() {
  const [sessions, setSessions] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState('');
  const [timetable, setTimetable] = useState(null);
  const [solverResult, setSolverResult] = useState(null);
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

  const loadTimetable = async () => {
    if (!selectedSessionId) return;
    setLoading(true);
    try {
      const data = await api.getTimetables();
      const list = data.results || data;
      const current = list.find((t) => t.exam_session === Number(selectedSessionId) || t.exam_session?.id === Number(selectedSessionId));
      setTimetable(current || null);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (selectedSessionId) {
      loadTimetable();
    }
  }, [selectedSessionId]);

  const handleRunSolver = async () => {
    if (!selectedSessionId) return;
    setLoading(true);
    setSolverResult(null);
    try {
      const res = await api.generateTimetable(selectedSessionId);
      setSolverResult(res.solver_result);
      setTimetable(res.timetable);
    } catch (e) {
      alert('Solver execution failed: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    if (!timetable) return;
    try {
      await api.approveTimetable(timetable.id);
      alert('Timetable approved successfully by Controller of Examinations.');
      loadTimetable();
    } catch (e) {
      alert('Approval failed: ' + e.message);
    }
  };

  const handlePublish = async () => {
    if (!timetable) return;
    try {
      await api.publishTimetable(timetable.id);
      alert('Timetable published! Students & faculty can now view schedules.');
      loadTimetable();
    } catch (e) {
      alert('Publication failed: ' + e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Timetable Constraint Solver Engine
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 3 Module: Python backtracking heuristic solver, student conflict detection, and schedule publishing
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
            onClick={handleRunSolver}
            disabled={loading}
            className="btn btn-primary"
            style={{ backgroundColor: 'var(--color-forest)' }}
          >
            <Sparkles size={16} color="#D4A72C" /> {loading ? 'Solving Constraints...' : 'Run Constraint Solver'}
          </button>
        </div>
      </div>

      {/* Solver Outcome Alert Banner */}
      {solverResult && (
        <div style={{
          padding: '1rem 1.25rem',
          backgroundColor: solverResult.status === 'SUCCESS' ? 'var(--color-sage-light)' : '#fef3c7',
          border: `1px solid ${solverResult.status === 'SUCCESS' ? 'var(--color-emerald)' : 'var(--color-warning)'}`,
          borderRadius: '0.75rem',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem'
        }}>
          {solverResult.status === 'SUCCESS' ? (
            <CheckCircle2 size={24} color="var(--color-emerald)" />
          ) : (
            <AlertTriangle size={24} color="var(--color-warning)" />
          )}
          <div>
            <div style={{ fontWeight: 800, color: 'var(--color-forest)', fontSize: '0.9375rem' }}>
              Solver Outcome: {solverResult.status} ({solverResult.scheduled_count}/{solverResult.total_count} Subjects Scheduled)
            </div>
            <div style={{ fontSize: '0.8125rem', color: 'var(--color-charcoal)', marginTop: '0.125rem' }}>
              {solverResult.message}
            </div>
          </div>
        </div>
      )}

      {/* Timetable Status & Control Header */}
      {timetable && (
        <div className="card" style={{ marginBottom: '1.5rem', padding: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)' }}>
                  {timetable.session_name}
                </h3>
                <span className={timetable.status === 'PUBLISHED' ? 'badge badge-success' : 'badge badge-gold'}>
                  {timetable.status}
                </span>
                <span className="badge badge-neutral">Version {timetable.version}</span>
              </div>
              <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>
                Active Conflict Clashes: <b>{timetable.conflict_count}</b> • Scheduled Papers: <b>{timetable.scheduled_count}</b>
              </p>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              {timetable.status === 'VALIDATED' && (
                <button onClick={handleApprove} className="btn btn-secondary btn-sm">
                  <ShieldCheck size={14} /> Approve Timetable
                </button>
              )}
              {timetable.status === 'APPROVED' && (
                <button onClick={handlePublish} className="btn btn-primary btn-sm">
                  <Send size={14} /> Publish to Faculty & Students
                </button>
              )}
              {timetable.status === 'PUBLISHED' && (
                <span className="badge badge-success" style={{ padding: '0.5rem 0.75rem' }}>
                  ✓ Officially Published & Live
                </span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Scheduled Timetable Entries Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Examination Date</th>
              <th>Time Slot</th>
              <th>Subject Code</th>
              <th>Subject Title</th>
              <th>Department</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            {!timetable || !timetable.entries || timetable.entries.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-muted)' }}>
                  {loading ? 'Solving timetable constraints...' : 'No timetable generated yet. Click "Run Constraint Solver" above.'}
                </td>
              </tr>
            ) : (
              timetable.entries.map((ent) => (
                <tr key={ent.id}>
                  <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>
                    {ent.exam_date}
                  </td>
                  <td>
                    <span className="badge badge-neutral">
                      {ent.slot_name} ({ent.slot_time})
                    </span>
                  </td>
                  <td style={{ fontWeight: 700 }}>{ent.subject_code}</td>
                  <td>{ent.subject_name}</td>
                  <td>{ent.department_name}</td>
                  <td>{ent.duration_minutes} Minutes</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
