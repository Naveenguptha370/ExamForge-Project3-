import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Modal from '../components/Modal';
import { ClipboardCheck, Download, CheckCircle2, AlertTriangle, ShieldAlert, History, Edit3 } from 'lucide-react';

export default function AttendancePage() {
  const [sheets, setSheets] = useState([]);
  const [activeSheet, setActiveSheet] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [auditModalOpen, setAuditModalOpen] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [correctionReason, setCorrectionReason] = useState('');
  const [newStatus, setNewStatus] = useState('ABSENT');

  const loadSheets = async () => {
    setLoading(true);
    try {
      const data = await api.getAttendanceSheets();
      const list = data.results || data;
      setSheets(list);
      if (list.length > 0 && !activeSheet) {
        setActiveSheet(list[0]);
        setRecords(list[0].records || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSheets();
  }, []);

  const handleSelectSheet = (sheet) => {
    setActiveSheet(sheet);
    setRecords(sheet.records || []);
  };

  const handleStatusChange = (recordId, status) => {
    setRecords(prev => prev.map(r => r.id === recordId ? { ...r, status } : r));
  };

  const handleBookletChange = (recordId, answer_booklet_no) => {
    setRecords(prev => prev.map(r => r.id === recordId ? { ...r, answer_booklet_no } : r));
  };

  const handleSaveBatch = async () => {
    if (!activeSheet) return;
    try {
      const res = await api.markBatchAttendance(activeSheet.id, records);
      alert('Attendance saved & locked successfully!');
      await loadSheets();
    } catch (e) {
      alert('Error saving attendance: ' + e.message);
    }
  };

  const openAuditCorrection = (rec) => {
    setSelectedRecord(rec);
    setNewStatus(rec.status === 'PRESENT' ? 'ABSENT' : 'PRESENT');
    setCorrectionReason('');
    setAuditModalOpen(true);
  };

  const handleExecuteCorrection = async (e) => {
    e.preventDefault();
    if (!selectedRecord || !correctionReason) {
      alert('Reason is required for correction audit trail.');
      return;
    }
    try {
      await api.correctAttendanceRecord(selectedRecord.id, newStatus, correctionReason);
      alert('Attendance status corrected and audit trail logged.');
      setAuditModalOpen(false);
      await loadSheets();
    } catch (e) {
      alert(e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Examination Attendance & Malpractice Audit
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 5 Module: Hall attendance sheets, booklet tracking, printable physical sheets, and correction audits
          </p>
        </div>

        {activeSheet && (
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <a
              href={api.getPrintableAttendancePdfUrl(activeSheet.id)}
              target="_blank"
              rel="noreferrer"
              className="btn btn-outline"
            >
              <Download size={16} /> Printable Hall Sheet PDF
            </a>
            <button
              onClick={handleSaveBatch}
              className="btn btn-primary"
            >
              <CheckCircle2 size={16} /> Submit & Lock Attendance
            </button>
          </div>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: '1.5rem', alignItems: 'start' }}>
        {/* Sheets Selector */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--color-forest)' }}>Attendance Sheets</h3>
            <span className="badge badge-neutral">{sheets.length} Sheets</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {sheets.length === 0 ? (
              <div style={{ fontSize: '0.8125rem', color: 'var(--color-muted)', textAlign: 'center', padding: '1rem' }}>
                No active sheets. Sheets are generated alongside exam seating plans.
              </div>
            ) : (
              sheets.map((s) => (
                <div
                  key={s.id}
                  onClick={() => handleSelectSheet(s)}
                  style={{
                    padding: '0.875rem',
                    borderRadius: '0.5rem',
                    cursor: 'pointer',
                    backgroundColor: activeSheet?.id === s.id ? 'var(--color-sage-light)' : '#FFFFFF',
                    border: `1px solid ${activeSheet?.id === s.id ? 'var(--color-forest)' : 'var(--color-border)'}`
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontWeight: 800, color: 'var(--color-forest)' }}>Room {s.room_number}</span>
                    <span className={s.is_submitted ? 'badge badge-success' : 'badge badge-warning'}>
                      {s.is_submitted ? 'Submitted' : 'Pending'}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>
                    {s.subject_code} • {s.exam_date}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-charcoal)', marginTop: '0.25rem' }}>
                    Present: <b>{s.present_count}</b> / {s.total_students}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Attendance Marking Table */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)' }}>
                {activeSheet ? `Candidate Headcount: Room ${activeSheet.room_number} (${activeSheet.subject_code})` : 'Select a Sheet'}
              </h3>
              <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>
                Invigilator: <b>{activeSheet?.invigilator_name || 'Dr. Assigned Invigilator'}</b> • Total Candidates: <b>{records.length}</b>
              </p>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <span className="badge badge-success">Present: {records.filter(r => r.status === 'PRESENT').length}</span>
              <span className="badge badge-danger">Absent: {records.filter(r => r.status === 'ABSENT').length}</span>
            </div>
          </div>

          <div className="table-container" style={{ border: 'none' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Seat</th>
                  <th>Roll Number</th>
                  <th>Student Name</th>
                  <th>Answer Booklet No</th>
                  <th>Attendance Status</th>
                  <th>Audit Action</th>
                </tr>
              </thead>
              <tbody>
                {records.length === 0 ? (
                  <tr>
                    <td colSpan="6" style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-muted)' }}>
                      No candidate records found in this attendance sheet.
                    </td>
                  </tr>
                ) : (
                  records.map((r) => (
                    <tr key={r.id}>
                      <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{r.seat_label}</td>
                      <td style={{ fontWeight: 700 }}>{r.student_roll}</td>
                      <td>{r.student_name}</td>
                      <td>
                        <input
                          type="text"
                          className="form-input"
                          style={{ padding: '0.25rem 0.5rem', fontSize: '0.8125rem', maxWidth: '140px' }}
                          value={r.answer_booklet_no || ''}
                          onChange={(e) => handleBookletChange(r.id, e.target.value)}
                          placeholder="BK-2026-..."
                        />
                      </td>
                      <td>
                        <select
                          className="form-select"
                          style={{ padding: '0.25rem 0.5rem', fontSize: '0.8125rem', width: 'auto' }}
                          value={r.status}
                          onChange={(e) => handleStatusChange(r.id, e.target.value)}
                        >
                          <option value="PRESENT">Present</option>
                          <option value="ABSENT">Absent</option>
                          <option value="LATE">Permitted Late</option>
                          <option value="MALPRACTICE">Malpractice</option>
                        </select>
                      </td>
                      <td>
                        <button
                          onClick={() => openAuditCorrection(r)}
                          className="btn btn-outline btn-sm"
                          style={{ fontSize: '0.6875rem', padding: '0.25rem 0.5rem' }}
                          title="Record Status Correction with Reason"
                        >
                          <Edit3 size={12} /> Correct Status
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Correction Audit Modal */}
      <Modal isOpen={auditModalOpen} onClose={() => setAuditModalOpen(false)} title="Authorized Attendance Correction">
        <form onSubmit={handleExecuteCorrection}>
          <div style={{ marginBottom: '1rem', padding: '0.75rem', backgroundColor: '#fef3c7', borderRadius: '0.5rem', fontSize: '0.8125rem', color: '#92400e' }}>
            Audited Action: Any modification to submitted examination attendance is permanently tracked with your user identity and timestamp.
          </div>

          <div className="form-group">
            <label className="form-label">Candidate</label>
            <div style={{ fontWeight: 700, fontSize: '0.9375rem', color: 'var(--color-forest)' }}>
              {selectedRecord?.student_roll} — {selectedRecord?.student_name} (Current: {selectedRecord?.status})
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">New Corrected Status</label>
            <select className="form-select" value={newStatus} onChange={(e) => setNewStatus(e.target.value)}>
              <option value="PRESENT">Present</option>
              <option value="ABSENT">Absent</option>
              <option value="LATE">Permitted Late Entry</option>
              <option value="MALPRACTICE">Booked for Malpractice</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Mandatory Correction Reason</label>
            <textarea
              required
              rows={3}
              className="form-textarea"
              placeholder="e.g. Verified candidate late entry with Chief Superintendent approval."
              value={correctionReason}
              onChange={(e) => setCorrectionReason(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.25rem' }}>
            <button type="button" onClick={() => setAuditModalOpen(false)} className="btn btn-outline">Cancel</button>
            <button type="submit" className="btn btn-primary">Commit Correction & Log Audit</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
