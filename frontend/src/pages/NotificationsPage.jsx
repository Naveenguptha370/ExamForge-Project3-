import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { Bell, Plus, Pin, Megaphone } from 'lucide-react';
import { Modal } from '../components/Modal';

export const NotificationsPage = () => {
  const toast = useToast();
  const [announcements, setAnnouncements] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [targetRole, setTargetRole] = useState('ALL');

  useEffect(() => {
    loadAnnouncements();
  }, []);

  const loadAnnouncements = async () => {
    const data = await api.getAnnouncements();
    setAnnouncements(data || []);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!title || !content) return;
    const res = await api.createAnnouncement({ title, content, target_role: targetRole });
    toast.success('Campus announcement published.');
    setModalOpen(false);
    setTitle('');
    setContent('');
    loadAnnouncements();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 5 — NOTICES</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Campus Announcements & Noticeboard</h1>
        </div>

        <button onClick={() => setModalOpen(true)} className="btn btn-primary btn-sm">
          <Plus size={15} />
          <span>New Announcement</span>
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {announcements.map((a) => (
          <div
            key={a.id}
            className="card"
            style={{
              padding: '20px 24px',
              display: 'flex',
              flexDirection: 'column',
              gap: 8,
              borderLeft: a.is_pinned ? '4px solid #D4A72C' : '4px solid #15803D'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                {a.is_pinned && <Pin size={16} color="#D4A72C" />}
                <h3 style={{ fontSize: '1.15rem', color: '#14532D' }}>{a.title}</h3>
              </div>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, backgroundColor: '#FAF9F6', padding: '3px 8px', borderRadius: 6, border: '1px solid #E7E5E4' }}>
                {a.target_role_display || 'All Campus Users'}
              </span>
            </div>
            <p style={{ fontSize: '0.9rem', color: '#575E54', lineHeight: 1.55 }}>{a.content}</p>
          </div>
        ))}
      </div>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Publish Campus Notice" maxWidth={500}>
        <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div className="form-group">
            <label className="form-label">Notice Title *</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Schedule Revision for Autumn Exam"
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Target Audience</label>
            <select value={targetRole} onChange={(e) => setTargetRole(e.target.value)} className="form-select">
              <option value="ALL">All Campus Users</option>
              <option value="FACULTY">Faculty & Invigilators</option>
              <option value="STUDENTS">Students Only</option>
              <option value="STAFF">Examination Staff</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Content Body *</label>
            <textarea
              rows={4}
              required
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write notice instructions..."
              className="form-textarea"
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10 }}>
            <button type="button" onClick={() => setModalOpen(false)} className="btn btn-secondary btn-sm">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary btn-sm">
              Publish Notice
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
