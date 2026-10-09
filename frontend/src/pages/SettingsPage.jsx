import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Settings, Save, Shield, CheckCircle2 } from 'lucide-react';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    institution_name: 'ExamForge Institute of Technology',
    institution_code: 'EFIT-HYD',
    academic_year: '2025-2026',
    current_term: 'EVEN',
    contact_email: 'controller.exams@examforge.edu',
    contact_phone: '+91 40 2345 6789',
    address: 'Campus Park, Tech Boulevard, Hyderabad, Telangana 500081',
    min_attendance_threshold: 75,
    default_exam_duration_mins: 180,
    default_spacing_rule: 'ALTERNATE_COLS',
    hall_ticket_instructions: '1. Carry this Hall Ticket and ID card.\n2. Arrive 20 mins early.\n3. Electronic gadgets strictly prohibited.\n4. Comply with all invigilator instructions.',
    malpractice_policy: 'Any malpractice will lead to debarment and disciplinary committee inquiry.'
  });
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const data = await api.getSystemSettings();
        setSettings(data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMsg('');
    try {
      const updated = await api.updateSystemSettings(settings);
      setSettings(updated);
      setSuccessMsg('Institutional parameters successfully saved.');
    } catch (e) {
      alert('Error saving settings: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
          Institutional Governance & System Settings
        </h2>
        <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
          Member 5 Module: Academic calendar parameters, examination thresholds, document guidelines, and security policies
        </p>
      </div>

      {successMsg && (
        <div style={{
          padding: '0.75rem 1rem',
          backgroundColor: 'var(--color-sage-light)',
          border: '1px solid var(--color-emerald)',
          borderRadius: '0.5rem',
          color: 'var(--color-forest)',
          fontSize: '0.875rem',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          <CheckCircle2 size={16} /> {successMsg}
        </div>
      )}

      <form onSubmit={handleSave} className="card" style={{ maxWidth: '800px', padding: '2rem' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)', marginBottom: '1.25rem' }}>
          Institution & Academic Configuration
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
          <div className="form-group">
            <label className="form-label">Institution Name</label>
            <input required className="form-input" value={settings.institution_name} onChange={(e) => setSettings({ ...settings, institution_name: e.target.value })} />
          </div>

          <div className="form-group">
            <label className="form-label">Institution Code</label>
            <input required className="form-input" value={settings.institution_code} onChange={(e) => setSettings({ ...settings, institution_code: e.target.value })} />
          </div>

          <div className="form-group">
            <label className="form-label">Current Academic Year</label>
            <input required className="form-input" value={settings.academic_year} onChange={(e) => setSettings({ ...settings, academic_year: e.target.value })} />
          </div>

          <div className="form-group">
            <label className="form-label">Current Term</label>
            <select className="form-select" value={settings.current_term} onChange={(e) => setSettings({ ...settings, current_term: e.target.value })}>
              <option value="EVEN">Even Semester</option>
              <option value="ODD">Odd Semester</option>
            </select>
          </div>
        </div>

        <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)', marginBottom: '1.25rem', borderTop: '1px solid var(--color-border-light)', paddingTop: '1.5rem' }}>
          Examination Rules & Thresholds
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
          <div className="form-group">
            <label className="form-label">Minimum Attendance Required (%)</label>
            <input required type="number" className="form-input" value={settings.min_attendance_threshold} onChange={(e) => setSettings({ ...settings, min_attendance_threshold: Number(e.target.value) })} />
          </div>

          <div className="form-group">
            <label className="form-label">Default Paper Duration (Minutes)</label>
            <input required type="number" className="form-input" value={settings.default_exam_duration_mins} onChange={(e) => setSettings({ ...settings, default_exam_duration_mins: Number(e.target.value) })} />
          </div>

          <div className="form-group" style={{ gridColumn: 'span 2' }}>
            <label className="form-label">Default Seating Spacing Strategy</label>
            <select className="form-select" value={settings.default_spacing_rule} onChange={(e) => setSettings({ ...settings, default_spacing_rule: e.target.value })}>
              <option value="ALTERNATE_COLS">Alternate Columns (Cols 1, 3, 5)</option>
              <option value="CHECKERBOARD">Checkerboard (Alternating Rows & Columns)</option>
            </select>
          </div>

          <div className="form-group" style={{ gridColumn: 'span 2' }}>
            <label className="form-label">Mandatory Hall Ticket Instructions (Printed on PDF)</label>
            <textarea rows={4} className="form-textarea" value={settings.hall_ticket_instructions} onChange={(e) => setSettings({ ...settings, hall_ticket_instructions: e.target.value })} />
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', borderTop: '1px solid var(--color-border-light)', paddingTop: '1.25rem' }}>
          <button type="submit" disabled={loading} className="btn btn-primary" style={{ padding: '0.75rem 1.75rem' }}>
            <Save size={16} /> {loading ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </form>
    </div>
  );
}
