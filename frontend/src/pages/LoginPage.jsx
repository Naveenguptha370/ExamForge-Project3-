import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { Shield, Lock, User, Sparkles, ArrowRight } from 'lucide-react';

export const LoginPage = ({ onLoginSuccess, onBackToLanding }) => {
  const { login, switchRole } = useAuth();
  const toast = useToast();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await login(username, password);
    setLoading(false);

    if (res.success) {
      toast.success(`Welcome back, ${username}!`);
      onLoginSuccess();
    } else {
      toast.error('Invalid credentials.');
    }
  };

  const handleQuickRole = (role, userVal, passVal) => {
    switchRole(role);
    toast.success(`Logged in as ${role}`);
    onLoginSuccess();
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: 'var(--color-bg)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 20
      }}
    >
      <div
        className="card animate-fade-in"
        style={{
          width: '100%',
          maxWidth: 480,
          padding: 36,
          backgroundColor: '#FFFFFF',
          borderRadius: 24,
          boxShadow: '0 25px 50px -12px rgba(20, 83, 45, 0.2)',
          border: '1px solid #DDEBDD'
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <div
            style={{
              width: 52,
              height: 52,
              borderRadius: 14,
              backgroundColor: '#14532D',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#D4A72C',
              fontWeight: 800,
              fontSize: '1.5rem',
              marginBottom: 12
            }}
          >
            EF
          </div>
          <h2 style={{ fontSize: '1.75rem', color: '#14532D', fontWeight: 800 }}>Sign In to ExamForge</h2>
          <p style={{ fontSize: '0.88rem', color: '#6B7280', marginTop: 4 }}>
            Centralized Examination Operations Portal
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="form-group">
            <label className="form-label">Username or Institutional Email</label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-input"
            />
          </div>

          <button type="submit" disabled={loading} className="btn btn-primary btn-lg" style={{ marginTop: 8 }}>
            <span>Sign In to System</span>
            <ArrowRight size={18} />
          </button>
        </form>

        <div style={{ marginTop: 28, paddingTop: 20, borderTop: '1px solid #E7E5E4' }}>
          <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#6B7280', textTransform: 'uppercase', display: 'block', textAlign: 'center', marginBottom: 12 }}>
            Instant Role Switch Shortcuts:
          </span>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            <button
              onClick={() => handleQuickRole('ADMIN', 'admin', 'admin123')}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.78rem' }}
            >
              👑 Administrator
            </button>
            <button
              onClick={() => handleQuickRole('FACULTY', 'faculty_cs1', 'faculty123')}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.78rem' }}
            >
              👨‍🏫 Faculty / Invigilator
            </button>
            <button
              onClick={() => handleQuickRole('EXAM_STAFF', 'staff1', 'staff123')}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.78rem' }}
            >
              📋 Exam Cell Staff
            </button>
            <button
              onClick={() => handleQuickRole('STUDENT', 'student1', 'student123')}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.78rem' }}
            >
              🎓 Student (Admit Pass)
            </button>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: 24 }}>
          <button
            onClick={onBackToLanding}
            style={{ background: 'none', border: 'none', color: '#15803D', fontWeight: 600, fontSize: '0.85rem', cursor: 'pointer' }}
          >
            ← Back to Public Portal
          </button>
        </div>
      </div>
    </div>
  );
};
