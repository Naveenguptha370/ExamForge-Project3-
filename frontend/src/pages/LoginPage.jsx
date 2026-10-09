import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Lock, User, ArrowRight, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function LoginPage({ onNavigate }) {
  const { login } = useAuth();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      onNavigate('dashboard');
    } catch (err) {
      setError(err.message || 'Login failed. Please check credentials.');
    } finally {
      setLoading(false);
    }
  };

  const setDemoRole = (u, p) => {
    setUsername(u);
    setPassword(p);
    setError('');
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: 'var(--color-ivory)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '460px',
        backgroundColor: '#FFFFFF',
        borderRadius: '1.25rem',
        border: '1px solid var(--color-border)',
        boxShadow: 'var(--shadow-xl)',
        padding: '2.5rem 2rem'
      }}>
        {/* Brand Logo & Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '3.5rem',
            height: '3.5rem',
            borderRadius: '0.875rem',
            backgroundColor: 'var(--color-forest)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '1rem',
            boxShadow: '0 4px 6px -1px rgba(20, 83, 45, 0.25)'
          }}>
            <Shield size={28} color="#D4A72C" />
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            ExamForge
          </h2>
          <p style={{ fontSize: '0.875rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>
            Institutional Examination Operations System
          </p>
        </div>

        {error && (
          <div style={{
            padding: '0.75rem 1rem',
            backgroundColor: '#fee2e2',
            border: '1px solid #fca5a5',
            borderRadius: '0.5rem',
            color: 'var(--color-error)',
            fontSize: '0.8125rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            marginBottom: '1.25rem'
          }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username / Institutional ID</label>
            <div style={{ position: 'relative' }}>
              <User size={16} color="var(--color-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
              <input
                type="text"
                required
                className="form-input"
                style={{ paddingLeft: '2.25rem' }}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g. admin or roll number"
              />
            </div>
          </div>

          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <label className="form-label">Password</label>
            <div style={{ position: 'relative' }}>
              <Lock size={16} color="var(--color-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
              <input
                type="password"
                required
                className="form-input"
                style={{ paddingLeft: '2.25rem' }}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', padding: '0.75rem', fontSize: '0.9375rem', borderRadius: '0.5rem' }}
          >
            {loading ? 'Authenticating...' : 'Sign In to Console'} <ArrowRight size={16} />
          </button>
        </form>

        {/* 1-Click Demo Credentials Sandbox */}
        <div style={{
          marginTop: '2rem',
          paddingTop: '1.5rem',
          borderTop: '1px solid var(--color-border-light)'
        }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-muted)', textAlign: 'center', marginBottom: '0.75rem', letterSpacing: '0.05em' }}>
            ONE-CLICK EVALUATOR ROLES
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
            <button
              type="button"
              onClick={() => setDemoRole('admin', 'admin123')}
              className="btn btn-secondary btn-sm"
              style={{ justifyContent: 'flex-start', fontSize: '0.75rem' }}
            >
              👑 Admin (Dr. Rajeshwar)
            </button>
            <button
              type="button"
              onClick={() => setDemoRole('examstaff', 'staff123')}
              className="btn btn-secondary btn-sm"
              style={{ justifyContent: 'flex-start', fontSize: '0.75rem' }}
            >
              📋 Exam Staff (S. Verma)
            </button>
            <button
              type="button"
              onClick={() => setDemoRole('prof.sharma', 'faculty123')}
              className="btn btn-secondary btn-sm"
              style={{ justifyContent: 'flex-start', fontSize: '0.75rem' }}
            >
              🎓 Faculty (Prof. Sharma)
            </button>
            <button
              type="button"
              onClick={() => setDemoRole('student.24cs101', 'student123')}
              className="btn btn-secondary btn-sm"
              style={{ justifyContent: 'flex-start', fontSize: '0.75rem' }}
            >
              🎒 Student (Aarav - 24CS101)
            </button>
          </div>
        </div>

        {/* Back to Home Link */}
        <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
          <button
            type="button"
            onClick={() => onNavigate('landing')}
            style={{ background: 'none', border: 'none', color: 'var(--color-emerald)', fontSize: '0.8125rem', fontWeight: 600, cursor: 'pointer' }}
          >
            ← Back to Public Website
          </button>
        </div>
      </div>
    </div>
  );
}
