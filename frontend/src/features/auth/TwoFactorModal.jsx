import React, { useState } from 'react';
import './authStyles.css';

export function TwoFactorModal({ isOpen, onVerify, onClose }) {
  const [otp, setOtp] = useState('');
  if (!isOpen) return null;

  return (
    <div className="ef-modal-backdrop">
      <div className="ef-modal-card">
        <h3 className="ef-modal-title">Two-Factor Authentication</h3>
        <p className="ef-auth-subtitle">Enter the 6-digit security token from your authenticator app.</p>
        <form onSubmit={(e) => { e.preventDefault(); onVerify && onVerify(otp); }} className="ef-auth-form">
          <input
            type="text" className="ef-form-input ef-otp-input" maxLength={6} placeholder="000000" required
            value={otp} onChange={e => setOtp(e.target.value)}
          />
          <div className="ef-btn-row">
            <button type="button" className="ef-btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="ef-btn-primary">Verify Token</button>
          </div>
        </form>
      </div>
    </div>
  );
}
