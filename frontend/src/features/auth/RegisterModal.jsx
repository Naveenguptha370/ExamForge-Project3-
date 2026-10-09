import React, { useState } from 'react';
import './authStyles.css';

export function RegisterModal({ isOpen, onClose, onUserCreated }) {
  const [formData, setFormData] = useState({
    username: '', email: '', role: 'FACULTY', password: '', first_name: '', last_name: ''
  });
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('http://localhost:8000/api/auth/users/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        onUserCreated && onUserCreated();
        onClose();
      } else {
        const d = await res.json();
        setError(JSON.stringify(d));
      }
    } catch (err) {
      setError('Failed to create account.');
    }
  };

  return (
    <div className="ef-modal-backdrop">
      <div className="ef-modal-card">
        <h3 className="ef-modal-title">Provision New Academic User</h3>
        {error && <div className="ef-auth-alert error">{error}</div>}
        <form onSubmit={handleSubmit} className="ef-auth-form">
          <input
            className="ef-form-input" placeholder="Username" required
            value={formData.username} onChange={e => setFormData({...formData, username: e.target.value})}
          />
          <input
            className="ef-form-input" placeholder="Email" type="email" required
            value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})}
          />
          <select
            className="ef-form-input"
            value={formData.role} onChange={e => setFormData({...formData, role: e.target.value})}
          >
            <option value="FACULTY">Faculty / Invigilator</option>
            <option value="EXAM_STAFF">Examination Staff</option>
            <option value="ADMIN">Administrator</option>
          </select>
          <input
            className="ef-form-input" placeholder="Temporary Password" type="password" required
            value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})}
          />
          <div className="ef-btn-row">
            <button type="button" className="ef-btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="ef-btn-primary">Provision Account</button>
          </div>
        </form>
      </div>
    </div>
  );
}
