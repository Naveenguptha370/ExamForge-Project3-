import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { StatusBadge } from '../components/StatusBadge';
import { Modal } from '../components/Modal';
import { Calendar, Plus, CheckCircle2, Shield, Play, Edit2, AlertCircle } from 'lucide-react';

export const ExamSessionsPage = () => {
  const toast = useToast();
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    code: '',
    academic_year: '2025-2026',
    term: 'ODD',
    session_type: 'END_TERM',
    start_date: '',
    end_date: '',
    description: ''
  });

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    setLoading(true);
    const data = await api.getSessions();
    setSessions(data || []);
    setLoading(false);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!formData.name || !formData.code || !formData.start_date || !formData.end_date) {
      toast.error('Please fill in all required fields.');
      return;
    }

    const res = await api.createSession(formData);
    toast.success(`Exam Session ${res.code} created successfully.`);
    setModalOpen(false);
    loadSessions();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 3 — CONFIGURATION</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Examination Sessions</h1>
        </div>
        <button onClick={() => setModalOpen(true)} className="btn btn-primary btn-sm">
          <Plus size={16} />
          <span>New Exam Session</span>
        </button>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Session Name & Code</th>
              <th>Academic Year & Term</th>
              <th>Session Type</th>
              <th>Examination Window</th>
              <th>Configured Subjects</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((s) => (
              <tr key={s.id}>
                <td>
                  <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <span style={{ fontWeight: 700, color: '#14532D' }}>{s.name}</span>
                    <span style={{ fontSize: '0.78rem', color: '#6B7280' }}>Code: {s.code}</span>
                  </div>
                </td>
                <td>{s.academic_year} ({s.term})</td>
                <td><b>{s.session_type}</b></td>
                <td>{s.start_date} to {s.end_date}</td>
                <td><b>{s.total_configured_subjects || 24}</b> subjects</td>
                <td><StatusBadge status={s.status} /></td>
                <td>
                  <span style={{ fontSize: '0.8rem', color: '#15803D', fontWeight: 700 }}>
                    {s.status === 'PUBLISHED' ? 'Live on Portal' : 'Configuring'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Create Examination Session" maxWidth={540}>
        <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div className="form-group">
            <label className="form-label">Session Name *</label>
            <input
              type="text"
              required
              placeholder="e.g. End Semester Examinations — Spring 2026"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="form-input"
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
            <div className="form-group">
              <label className="form-label">Session Code *</label>
              <input
                type="text"
                required
                placeholder="e.g. ESE-SPR-2026"
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Academic Year</label>
              <input
                type="text"
                value={formData.academic_year}
                onChange={(e) => setFormData({ ...formData, academic_year: e.target.value })}
                className="form-input"
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
            <div className="form-group">
              <label className="form-label">Start Date *</label>
              <input
                type="date"
                required
                value={formData.start_date}
                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label className="form-label">End Date *</label>
              <input
                type="date"
                required
                value={formData.end_date}
                onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                className="form-input"
              />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginTop: 10 }}>
            <button type="button" onClick={() => setModalOpen(false)} className="btn btn-secondary btn-sm">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary btn-sm">
              Create Session
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
