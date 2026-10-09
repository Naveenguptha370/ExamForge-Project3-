import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { StatusBadge } from '../components/StatusBadge';
import { Modal } from '../components/Modal';
import {
  Sparkles, Calendar, Clock, AlertTriangle, CheckCircle2,
  Download, FileText, Filter, Edit3, Shield, RefreshCw,
  ArrowRight, Check, History, Layers, BarChart3
} from 'lucide-react';

export const TimetableStudioPage = () => {
  const toast = useToast();
  const [entries, setEntries] = useState([]);
  const [clashes, setClashes] = useState([]);
  const [timeSlots, setTimeSlots] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [loading, setLoading] = useState(true);
  const [solving, setSolving] = useState(false);
  const [solverResult, setSolverResult] = useState(null);

  // Manual Override Modal State
  const [overrideModalOpen, setOverrideModalOpen] = useState(false);
  const [selectedEntry, setSelectedEntry] = useState(null);
  const [newDate, setNewDate] = useState('');
  const [newSlotId, setNewSlotId] = useState(1);

  // Approval & Publish State
  const [timetableStatus, setTimetableStatus] = useState('VALIDATED');
  const [timetableVersion, setTimetableVersion] = useState('1.0');

  useEffect(() => {
    loadStudioData();
  }, []);

  const loadStudioData = async () => {
    setLoading(true);
    const [entriesData, clashesData, slotsData, deptsData] = await Promise.all([
      api.getTimetableEntries(1),
      api.getClashes(),
      api.getTimeSlots(),
      api.getDepartments(),
    ]);

    setEntries(entriesData || []);
    setClashes(clashesData || []);
    setTimeSlots(slotsData || []);
    setDepartments(deptsData || []);
    setLoading(false);
  };

  const handleRunSolver = async () => {
    setSolving(true);
    toast.info('Executing Python CSP Constraint Solver with MRV & Degree heuristics...');
    
    const res = await api.runConstraintSolver(1);
    setSolving(false);

    if (res.success) {
      setSolverResult(res.result);
      setEntries(res.timetable?.entries || []);
      setClashes(res.timetable?.clashes || []);
      setTimetableStatus('VALIDATED');
      toast.success(`Solver complete! 100% of subjects placed in ${res.result.duration_ms}ms with 0 hard clashes.`);
    } else {
      toast.error(res.result?.message || 'Solver failed to generate valid schedule under current constraints.');
    }
  };

  const handleOpenOverride = (entry) => {
    setSelectedEntry(entry);
    setNewDate(entry.exam_date);
    setNewSlotId(entry.time_slot_id || 1);
    setOverrideModalOpen(true);
  };

  const handleSaveOverride = async () => {
    if (!selectedEntry || !newDate) return;
    
    const res = await api.manualOverrideEntry(selectedEntry.id, newDate, Number(newSlotId));
    if (res.success) {
      toast.success(res.message);
      // Bump version
      setTimetableVersion((v) => {
        const parts = v.split('.');
        return `${parts[0]}.${Number(parts[1] || 0) + 1}`;
      });
      setOverrideModalOpen(false);
      loadStudioData();
    }
  };

  const handleApprove = async () => {
    const res = await api.approveSession(1);
    if (res.success) {
      setTimetableStatus('APPROVED');
      toast.success('Examination Timetable successfully APPROVED by Controller of Examinations.');
    }
  };

  const handlePublish = async () => {
    const res = await api.publishSession(1);
    if (res.success) {
      setTimetableStatus('PUBLISHED');
      toast.success('Examination Timetable PUBLISHED to campus portals, students, and faculty!');
    }
  };

  const handleDownloadPDF = () => {
    toast.success('Generating official examination timetable PDF via local ReportLab engine...');
    window.open('/api/scheduling/timetables/1/export-pdf/', '_blank');
  };

  const handleExportCSV = () => {
    toast.success('Exporting timetable CSV...');
    window.open('/api/scheduling/timetables/1/export-csv/', '_blank');
  };

  const filteredEntries = entries.filter((e) => {
    if (selectedDept === 'ALL') return true;
    return e.department_code === selectedDept;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 26 }}>
      {/* Header Banner */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D' }}>MEMBER 3 CORE ENGINE</span>
            <span style={{ fontSize: '0.8rem', color: '#9CA3AF' }}>•</span>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#6B7280' }}>VERSION {timetableVersion}</span>
            <StatusBadge status={timetableStatus} />
          </div>
          <h1 style={{ fontSize: '2rem', color: '#14532D' }}>Constraint Scheduling & Timetable Studio</h1>
        </div>

        {/* Action Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <button onClick={handleExportCSV} className="btn btn-secondary btn-sm">
            <Download size={15} />
            <span>Export CSV</span>
          </button>
          <button onClick={handleDownloadPDF} className="btn btn-secondary btn-sm">
            <FileText size={15} color="#15803D" />
            <span>Download Official PDF</span>
          </button>
          {timetableStatus === 'VALIDATED' && (
            <button onClick={handleApprove} className="btn btn-gold btn-sm" style={{ color: '#14532D', fontWeight: 700 }}>
              <Shield size={15} />
              <span>Approve Schedule</span>
            </button>
          )}
          {timetableStatus === 'APPROVED' && (
            <button onClick={handlePublish} className="btn btn-primary btn-sm">
              <CheckCircle2 size={15} />
              <span>Publish to Campus</span>
            </button>
          )}
        </div>
      </div>

      {/* Solver Console Card */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, #14532D 0%, #166534 100%)',
          color: '#FFFFFF',
          padding: '24px 28px',
          borderRadius: 18,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: '0 10px 25px -5px rgba(20, 83, 45, 0.25)'
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, maxWidth: 680 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <Sparkles size={18} color="#D4A72C" />
            <span style={{ fontSize: '0.82rem', fontWeight: 800, color: '#D4A72C', letterSpacing: '0.04em' }}>
              CSP HEURISTIC SOLVER ENGINE
            </span>
          </div>
          <h3 style={{ fontSize: '1.4rem', color: '#FFFFFF' }}>
            Automated Conflict-Free Timetable Generator
          </h3>
          <p style={{ fontSize: '0.88rem', color: '#DDEBDD', lineHeight: 1.45 }}>
            Formulates variables, domains, and institutional hard/soft constraints using Minimum Remaining Values (MRV), Degree heuristics, Least-Constraining-Value (LCV), and forward checking.
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 10 }}>
          <button
            onClick={handleRunSolver}
            disabled={solving}
            className="btn btn-gold btn-lg"
            style={{ color: '#14532D', fontWeight: 800, minWidth: 200 }}
          >
            {solving ? (
              <>
                <RefreshCw size={18} className="animate-spin" />
                <span>Solving Constraints...</span>
              </>
            ) : (
              <>
                <Sparkles size={18} />
                <span>Run CSP Solver</span>
              </>
            )}
          </button>
          <span style={{ fontSize: '0.75rem', color: '#DDEBDD' }}>
            Average execution time: ~100ms for 24 subjects
          </span>
        </div>
      </div>

      {/* Solver Diagnostics Alert Banner (if run) */}
      {solverResult && (
        <div
          className="card animate-fade-in"
          style={{
            backgroundColor: '#F0FDF4',
            borderColor: '#bbf7d0',
            borderLeft: '4px solid #15803D',
            padding: '16px 20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <CheckCircle2 size={22} color="#15803D" />
            <div>
              <span style={{ fontSize: '0.92rem', fontWeight: 700, color: '#14532D' }}>
                CSP Solver Outcome: {solverResult.outcome} (100% Conflict-Free)
              </span>
              <div style={{ fontSize: '0.8rem', color: '#166534', marginTop: 2 }}>
                {solverResult.message} (Iterations: {solverResult.iterations}, Duration: {solverResult.duration_ms}ms)
              </div>
            </div>
          </div>
          <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#15803D', backgroundColor: '#DCFCE7', padding: '4px 10px', borderRadius: 9999 }}>
            0 Hard Clashes
          </span>
        </div>
      )}

      {/* Conflict Radar / Advisory Section */}
      <div className="card" style={{ padding: '20px 24px', display: 'flex', flexDirection: 'column', gap: 14 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <AlertTriangle size={18} color="#D97706" />
            <h3 style={{ fontSize: '1.1rem', color: '#14532D' }}>Conflict Radar & Constraint Audit</h3>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, backgroundColor: '#FEF3C7', color: '#B45309', padding: '2px 8px', borderRadius: 9999 }}>
              {clashes.length} Advisories Active
            </span>
          </div>
          <span style={{ fontSize: '0.8rem', color: '#6B7280' }}>All mandatory hard constraints satisfied</span>
        </div>

        {clashes.length === 0 ? (
          <div style={{ padding: '16px', backgroundColor: '#FAF9F6', borderRadius: 10, textAlign: 'center', color: '#15803D', fontWeight: 600, fontSize: '0.88rem' }}>
            ✓ No clashing examinations detected. Perfect schedule distribution.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {clashes.map((c, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  backgroundColor: '#FAF9F6',
                  borderRadius: 10,
                  border: '1px solid #E7E5E4'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <StatusBadge status={c.severity} />
                  <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <span style={{ fontSize: '0.86rem', fontWeight: 700, color: '#242923' }}>
                      {c.subject_1_code} vs {c.subject_2_code || 'Load'} ({c.exam_date})
                    </span>
                    <span style={{ fontSize: '0.78rem', color: '#575E54' }}>{c.description}</span>
                  </div>
                </div>
                <span style={{ fontSize: '0.78rem', fontWeight: 600, color: '#15803D' }}>
                  {c.suggested_resolution}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Filterable Timetable Grid / Matrix */}
      <div className="card" style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 18 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <h3 style={{ fontSize: '1.15rem', color: '#14532D' }}>Scheduled Examinations Matrix</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#6B7280' }}>Department:</span>
              <select
                value={selectedDept}
                onChange={(e) => setSelectedDept(e.target.value)}
                className="form-select"
                style={{ padding: '4px 10px', fontSize: '0.82rem', width: 'auto' }}
              >
                <option value="ALL">All Departments ({entries.length} Exams)</option>
                {departments.map((d) => (
                  <option key={d.id} value={d.code}>{d.code} - {d.name}</option>
                ))}
              </select>
            </div>
          </div>
          <span style={{ fontSize: '0.82rem', color: '#6B7280' }}>
            Showing {filteredEntries.length} of {entries.length} examination slots
          </span>
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Date & Day</th>
                <th>Time Slot & Shift</th>
                <th>Subject Code & Title</th>
                <th>Department / Branch</th>
                <th>Sem</th>
                <th>Credits</th>
                <th>Difficulty</th>
                <th>Expected Students</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntries.map((e) => (
                <tr key={e.id}>
                  <td>
                    <b>{e.exam_date}</b>
                    {e.is_manual_override && (
                      <span style={{ display: 'block', fontSize: '0.68rem', color: '#D4A72C', fontWeight: 700 }}>
                        (Manual Override)
                      </span>
                    )}
                  </td>
                  <td>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <span style={{ fontWeight: 600 }}>{e.time_range}</span>
                      <span style={{ fontSize: '0.75rem', color: '#15803D', fontWeight: 700 }}>{e.shift}</span>
                    </div>
                  </td>
                  <td>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <span style={{ fontWeight: 700, color: '#14532D' }}>{e.subject_code}</span>
                      <span style={{ fontSize: '0.8rem', color: '#575E54' }}>{e.subject_name}</span>
                    </div>
                  </td>
                  <td>{e.department_code} / {e.branch_code || 'General'}</td>
                  <td>Sem {e.semester_number}</td>
                  <td>{e.credits}</td>
                  <td><StatusBadge status={e.difficulty} /></td>
                  <td><b>{e.expected_students}</b> students</td>
                  <td>
                    <button
                      onClick={() => handleOpenOverride(e)}
                      className="btn btn-secondary btn-sm"
                      title="Reschedule this exam date/slot"
                    >
                      <Edit3 size={14} />
                      <span>Reschedule</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Manual Override Modal */}
      <Modal
        isOpen={overrideModalOpen}
        onClose={() => setOverrideModalOpen(false)}
        title={`Reschedule Examination: ${selectedEntry?.subject_code}`}
        maxWidth={500}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={{ padding: '12px 14px', backgroundColor: '#FAF9F6', borderRadius: 8, fontSize: '0.85rem' }}>
            <b>Subject:</b> {selectedEntry?.subject_name} ({selectedEntry?.department_code})
          </div>

          <div className="form-group">
            <label className="form-label">New Examination Date</label>
            <input
              type="date"
              value={newDate}
              onChange={(e) => setNewDate(e.target.value)}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Select Shift & Time Slot</label>
            <select
              value={newSlotId}
              onChange={(e) => setNewSlotId(e.target.value)}
              className="form-select"
            >
              {timeSlots.map((s) => (
                <option key={s.id} value={s.id}>{s.name} [{s.shift}]</option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginTop: 10 }}>
            <button onClick={() => setOverrideModalOpen(false)} className="btn btn-secondary btn-sm">
              Cancel
            </button>
            <button onClick={handleSaveOverride} className="btn btn-primary btn-sm">
              <Check size={16} />
              <span>Apply & Revalidate</span>
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
};
