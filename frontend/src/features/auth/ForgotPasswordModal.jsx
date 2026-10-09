import React, { useState } from 'react';
import './authStyles.css';

export function ForgotPasswordModal({ isOpen, onClose }) {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

  if (!isOpen) return null;

  return (
    <div className="ef-modal-backdrop">
      <div className="ef-modal-card">
        <h3 className="ef-modal-title">Password Reset Dispatch</h3>
        <p className="ef-auth-subtitle">Submit your registered institutional email to trigger local credential dispatch.</p>
        {sent ? (
          <div className="ef-auth-alert success">
            A password reset notification has been recorded in the local console backend.
          </div>
        ) : (
          <form onSubmit={(e) => { e.preventDefault(); setSent(true); }} className="ef-auth-form">
            <input
              type="email" className="ef-form-input" placeholder="institutional.id@college.edu" required
              value={email} onChange={e => setEmail(e.target.value)}
            />
            <div className="ef-btn-row">
              <button type="button" className="ef-btn-secondary" onClick={onClose}>Close</button>
              <button type="submit" className="ef-btn-primary">Send Reset Link</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
