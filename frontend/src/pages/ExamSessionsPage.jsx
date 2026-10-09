import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Modal from '../components/Modal';
import { CalendarDays, Plus, CheckCircle2, AlertCircle, Clock } from 'lucide-react';

export default function ExamSessionsPage() {
  const [sessions, setSessions] = useState([]);
  const [timeSlots, setTimeSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [formData, setFormData] = useState({
    name: '', session_code: '', academic_year: '2025-2026', term: 'EVEN', session_type: 'REGULAR',
    start_date: '2026-05-11', end_date: '2026-05-23', instructions: 'Admit Card mandatory. No electronic devices.'
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const [sess, slots] = await Promise.all([
        api.getExamSessions(),
        api.getTimeSlots()
      ]);
      setSessions(sess.results || sess);
      setTimeSlots(slots.results || slots);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.createExamSession(formData);
      setIsModalOpen(false);
      loadData();
    } catch (e) {
      alert('Error: ' + e.message);
    }
  };

  const handleApprove = async (id) => {
    try {
      await api.approveExamSession(id);
      loadData();
    } catch (e) {
      alert(e.message);
    }
  };

  const handlePublish = async (id) => {
    try {
      await api.publishExamSession(id);
      loadData();
    } catch (e) {
      alert(e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Examination Sessions & Time Slots
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 3 Module: Examination terms, date boundaries, session types, and approval governance
          </p>
        </div>

        <button onClick={() => setIsModalOpen(true)} className="btn btn-primary">
          <Plus size={16} /> Configure Exam Session
        </button>
      </div>

      {/* Sessions Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem', marginBottom: '2.5rem' }}>
        {sessions.map((s) => (
          <div key={s.id} className="card" style={{ borderLeft: '4px solid var(--color-forest)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <span className="badge badge-gold">{s.session_code}</span>
              <span className={s.status === 'PUBLISHED' ? 'badge badge-success' : 'badge badge-neutral'}>
                {s.status}
              </span>
            </div>

            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--color-forest)', marginBottom: '0.5rem' }}>
              {s.name}
            </h3>

            <div style={{ fontSize: '0.8125rem', color: 'var(--color-charcoal)', display: 'flex', flexDirection: 'column', gap: '0.25rem', marginBottom: '1rem' }}>
              <div><b>Academic Term:</b> {s.academic_year} ({s.term})</div>
              <div><b>Duration:</b> {s.start_date} to {s.end_date}</div>
              <div><b>Exam Type:</b> {s.session_type}</div>
              <div><b>Enrolled Papers:</b> {s.subjects_count || 4} Subjects</div>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', borderTop: '1px solid var(--color-border-light)', paddingTop: '0.75rem' }}>
              {s.status === 'DRAFT' && (
                <button onClick={() => handleApprove(s.id)} className="btn btn-secondary btn-sm" style={{ flex: 1 }}>
                  Approve Session
                </button>
              )}
              {s.status === 'APPROVED' && (
                <button onClick={() => handlePublish(s.id)} className="btn btn-primary btn-sm" style={{ flex: 1 }}>
                  Publish Live
                </button>
              )}
              {s.status === 'PUBLISHED' && (
                <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  <CheckCircle2 size={14} /> Session Published & Active
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Time Slots Section */}
      <div className="card">
        <div className="card-header">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-forest)' }}>
            Official Examination Time Slots
          </h3>
          <span className="badge badge-success">Active Slots</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
          {timeSlots.map((ts) => (
            <div key={ts.id} style={{ padding: '1rem', border: '1px solid var(--color-border-light)', borderRadius: '0.5rem', backgroundColor: '#F8FAF7' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-forest)' }}>{ts.slot_code}</div>
              <div style={{ fontWeight: 700, fontSize: '0.9375rem', color: 'var(--color-charcoal)', margin: '0.25rem 0' }}>{ts.name}</div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>{ts.formatted_time || `${ts.start_time} - ${ts.end_time}`}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Create Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Configure New Examination Session">
        <form onSubmit={handleCreate}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div className="form-group" style={{ gridColumn: 'span 2' }}>
              <label className="form-label">Session Name</label>
              <input required className="form-input" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g. End Semester Examinations May 2026" />
            </div>
            <div className="form-group">
              <label className="form-label">Session Code</label>
              <input required className="form-input" value={formData.session_code} onChange={(e) => setFormData({ ...formData, session_code: e.target.value })} placeholder="e.g. ESE-MAY-2026" />
            </div>
            <div className="form-group">
              <label className="form-label">Academic Year</label>
              <input required className="form-input" value={formData.academic_year} onChange={(e) => setFormData({ ...formData, academic_year: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Start Date</label>
              <input required type="date" className="form-input" value={formData.start_date} onChange={(e) => setFormData({ ...formData, start_date: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">End Date</label>
              <input required type="date" className="form-input" value={formData.end_date} onChange={(e) => setFormData({ ...formData, end_date: e.target.value })} />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.25rem' }}>
            <button type="button" onClick={() => setIsModalOpen(false)} className="btn btn-outline">Cancel</button>
            <button type="submit" className="btn btn-primary">Create Session</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
