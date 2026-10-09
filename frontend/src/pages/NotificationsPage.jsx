import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Modal from '../components/Modal';
import { Bell, Plus, Send, AlertTriangle, CheckCircle2, Megaphone, Clock } from 'lucide-react';

export default function NotificationsPage() {
  const [announcements, setAnnouncements] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [formData, setFormData] = useState({
    title: '', content: '', target_role: 'ALL', priority: 'NORMAL'
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const [annData, notifData] = await Promise.all([
        api.getAnnouncements(),
        api.getInAppNotifications()
      ]);
      setAnnouncements(annData.results || annData);
      setNotifications(notifData.results || notifData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateAnnouncement = async (e) => {
    e.preventDefault();
    try {
      await api.createAnnouncement(formData);
      setIsModalOpen(false);
      setFormData({ title: '', content: '', target_role: 'ALL', priority: 'NORMAL' });
      loadData();
    } catch (e) {
      alert('Error: ' + e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Announcements & In-App Notification Center
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 5 Module: Multi-channel institutional notices, role targeting, and internal student/faculty alerts
          </p>
        </div>

        <button onClick={() => setIsModalOpen(true)} className="btn btn-primary">
          <Plus size={16} /> Broadcast Notice
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem' }}>
        {/* Official Announcements */}
        <div>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Megaphone size={18} /> Official Examination Notices ({announcements.length})
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {announcements.map((a) => (
              <div key={a.id} className="card" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span className={a.priority === 'URGENT' ? 'badge badge-danger' : (a.priority === 'HIGH' ? 'badge badge-warning' : 'badge badge-success')}>
                    {a.priority}
                  </span>
                  <span className="badge badge-neutral">Audience: {a.target_role}</span>
                </div>
                <h4 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--color-forest)', marginBottom: '0.375rem' }}>
                  {a.title}
                </h4>
                <p style={{ fontSize: '0.8125rem', color: 'var(--color-charcoal)', lineHeight: 1.5, marginBottom: '0.75rem' }}>
                  {a.content}
                </p>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  <Clock size={12} /> Published on {new Date(a.created_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* In-App User Alerts */}
        <div>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Bell size={18} /> In-App Activity Messages ({notifications.length})
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {notifications.length === 0 ? (
              <div className="card" style={{ padding: '2rem', textAlign: 'center', color: 'var(--color-muted)' }}>
                No notifications logged for your account.
              </div>
            ) : (
              notifications.map((n) => (
                <div key={n.id} className="card" style={{ padding: '1rem', backgroundColor: n.is_read ? '#FFFFFF' : 'var(--color-sage-light)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>{n.title}</span>
                    <span className="badge badge-neutral" style={{ fontSize: '0.625rem' }}>{n.notification_type}</span>
                  </div>
                  <div style={{ fontSize: '0.8125rem', color: 'var(--color-charcoal)' }}>{n.message}</div>
                  <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)', marginTop: '0.375rem' }}>
                    {new Date(n.created_at).toLocaleString()}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Broadcast Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Broadcast Examination Notice">
        <form onSubmit={handleCreateAnnouncement}>
          <div className="form-group">
            <label className="form-label">Notice Title</label>
            <input required className="form-input" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} placeholder="e.g. Schedule Revision Notice" />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div className="form-group">
              <label className="form-label">Target Audience</label>
              <select className="form-select" value={formData.target_role} onChange={(e) => setFormData({ ...formData, target_role: e.target.value })}>
                <option value="ALL">Everyone</option>
                <option value="STUDENT">Students Only</option>
                <option value="FACULTY">Faculty Only</option>
                <option value="EXAM_STAFF">Staff Only</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Priority</label>
              <select className="form-select" value={formData.priority} onChange={(e) => setFormData({ ...formData, priority: e.target.value })}>
                <option value="LOW">Low</option>
                <option value="NORMAL">Normal</option>
                <option value="HIGH">High</option>
                <option value="URGENT">Urgent (Banners)</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Notice Content</label>
            <textarea required rows={4} className="form-textarea" value={formData.content} onChange={(e) => setFormData({ ...formData, content: e.target.value })} placeholder="Enter formal announcement details..." />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.25rem' }}>
            <button type="button" onClick={() => setIsModalOpen(false)} className="btn btn-outline">Cancel</button>
            <button type="submit" className="btn btn-primary"><Send size={14} /> Publish Notice</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
