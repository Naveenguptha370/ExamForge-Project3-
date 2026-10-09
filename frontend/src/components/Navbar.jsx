import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Sparkles, Menu, X, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function Navbar({ onNavigate }) {
  const { user } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { label: 'Home', id: 'hero' },
    { label: 'Features', id: 'features' },
    { label: 'Modules (15)', id: 'modules' },
    { label: '5-Member Architecture', id: 'team' },
    { label: 'Workflow', id: 'workflow' },
    { label: 'Benefits', id: 'benefits' },
    { label: 'FAQ', id: 'faq' },
  ];

  const handleScroll = (id) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav style={{
      position: 'sticky',
      top: 0,
      zIndex: 40,
      backgroundColor: 'rgba(250, 249, 246, 0.95)',
      backdropFilter: 'blur(8px)',
      borderBottom: '1px solid var(--color-border)',
      padding: '0.875rem 2rem',
      transition: 'all 0.3s ease'
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        {/* Brand Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', cursor: 'pointer' }} onClick={() => onNavigate('landing')}>
          <div style={{
            width: '2.5rem',
            height: '2.5rem',
            borderRadius: '0.625rem',
            backgroundColor: 'var(--color-forest)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFFFFF',
            boxShadow: '0 4px 6px -1px rgba(20, 83, 45, 0.25)'
          }}>
            <Shield size={22} color="#D4A72C" />
          </div>
          <div>
            <div style={{ fontFamily: 'var(--font-heading)', fontSize: '1.25rem', fontWeight: 800, color: 'var(--color-forest)', lineHeight: 1.1 }}>
              ExamForge
            </div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)', fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
              Operations System
            </div>
          </div>
        </div>

        {/* Desktop Navigation Links */}
        <div style={{ display: 'none', gap: '1.75rem', alignItems: 'center' }} className="desktop-nav">
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => handleScroll(link.id)}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '0.875rem',
                fontWeight: 600,
                color: 'var(--color-charcoal)',
                cursor: 'pointer',
                transition: 'color 0.2s ease',
              }}
              onMouseEnter={(e) => (e.target.style.color = 'var(--color-emerald)')}
              onMouseLeave={(e) => (e.target.style.color = 'var(--color-charcoal)')}
            >
              {link.label}
            </button>
          ))}
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {user ? (
            <button
              onClick={() => onNavigate('dashboard')}
              className="btn btn-primary"
              style={{ padding: '0.5rem 1.125rem' }}
            >
              Open Console <ArrowRight size={16} />
            </button>
          ) : (
            <>
              <button
                onClick={() => onNavigate('login')}
                className="btn btn-outline"
                style={{ padding: '0.5rem 1rem' }}
              >
                Sign In
              </button>
              <button
                onClick={() => onNavigate('dashboard')}
                className="btn btn-primary"
                style={{ padding: '0.5rem 1.125rem' }}
              >
                Launch Console <ArrowRight size={16} />
              </button>
            </>
          )}

          {/* Mobile hamburger */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            style={{
              background: 'none',
              border: 'none',
              padding: '0.375rem',
              cursor: 'pointer',
              color: 'var(--color-forest)',
              display: 'inline-flex'
            }}
            aria-label="Toggle Navigation"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div style={{
          marginTop: '0.75rem',
          paddingTop: '0.75rem',
          borderTop: '1px solid var(--color-border)',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem'
        }}>
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => handleScroll(link.id)}
              style={{
                background: 'none',
                border: 'none',
                textAlign: 'left',
                fontSize: '0.9375rem',
                fontWeight: 600,
                color: 'var(--color-forest)',
                padding: '0.375rem 0',
                cursor: 'pointer'
              }}
            >
              {link.label}
            </button>
          ))}
        </div>
      )}

      <style>{`
        @media (min-width: 900px) {
          .desktop-nav { display: flex !important; }
        }
      `}</style>
    </nav>
  );
}
