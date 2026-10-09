import React, { useState } from 'react';
import './authStyles.css';

export function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage('');
    try {
      const res = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.ok) {
        onLoginSuccess && onLoginSuccess(data.user);
      } else {
        setErrorMessage(data.detail || 'Invalid credentials');
      }
    } catch (err) {
      setErrorMessage('Network error communicating with authentication service.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="ef-auth-card">
      <div className="ef-auth-header">
        <div className="ef-auth-badge">EXAMFORGE SECURE AUTH</div>
        <h2 className="ef-auth-title">Institutional Portal Login</h2>
        <p className="ef-auth-subtitle">Examination Operations & Faculty Governance</p>
      </div>
      {errorMessage && <div className="ef-auth-alert error">{errorMessage}</div>}
      <form onSubmit={handleSubmit} className="ef-auth-form">
        <div className="ef-form-group">
          <label className="ef-form-label">Username or Institutional ID</label>
          <input
            type="text" className="ef-form-input" value={username}
            onChange={(e) => setUsername(e.target.value)} required
          />
        </div>
        <div className="ef-form-group">
          <label className="ef-form-label">Password</label>
          <input
            type="password" className="ef-form-input" value={password}
            onChange={(e) => setPassword(e.target.value)} required
          />
        </div>
        <button type="submit" className="ef-btn-primary" disabled={isLoading}>
          {isLoading ? 'Verifying...' : 'Sign In'}
        </button>
      </form>
    </div>
  );
}
