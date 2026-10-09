import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { Bell, CheckCircle2, AlertTriangle, Shield, ArrowUpRight } from 'lucide-react';

export default function Header({ title, subtitle, onNavigateLanding }) {
  const { user } = useAuth();
  const [unreadCount, setUnreadCount] = useState(0);
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const countData = await api.getUnreadNotificationsCount();
        setUnreadCount(countData.unread_count || 0);
        const list = await api.getInAppNotifications();
        setNotifications(list.slice(0, 5));
      } catch (e) {
        // silent fail
      }
    };
    fetchNotifications();
  }, []);

  const handleMarkAllRead = async () => {
    try {
      await api.markAllNotificationsRead();
      setUnreadCount(0);
    } catch (e) {
      console.warn(e);
    }
  };

  return (
    <header style={{
      backgroundColor: '#FFFFFF',
      borderBottom: '1px solid var(--color-border)',
      padding: '1rem 2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'sticky',
      top: 0,
      zIndex: 20
    }}>
      <div>
        <h1 style={{ fontSize: '1.375rem', fontWeight: 800, color: 'var(--color-forest)', lineHeight: 1.2 }}>
          {title}
        </h1>
        {subtitle && (
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)', marginTop: '0.125rem' }}>
            {subtitle}
          </p>
        )}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {/* System Online Status Pill */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.375rem',
          backgroundColor: 'var(--color-sage-light)',
          border: '1px solid #cce2cc',
          padding: '0.375rem 0.75rem',
          borderRadius: '9999px',
          fontSize: '0.75rem',
          fontWeight: 600,
          color: 'var(--color-forest)'
        }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--color-emerald)', display: 'inline-block' }} />
          Local Engine Active
        </div>

        {/* Public Portal Button */}
        <button
          onClick={onNavigateLanding}
          className="btn btn-outline btn-sm"
          style={{ padding: '0.375rem 0.75rem', fontSize: '0.75rem' }}
        >
          Landing Page <ArrowUpRight size={14} />
        </button>

        {/* Notifications Icon Button */}
        <div style={{ position: 'relative' }}>
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            style={{
              background: 'none',
              border: '1px solid var(--color-border)',
              borderRadius: '0.5rem',
              padding: '0.5rem',
              cursor: 'pointer',
              color: 'var(--color-charcoal)',
              position: 'relative',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: showNotifications ? 'var(--color-sage-light)' : 'transparent'
            }}
            title="Notifications"
          >
            <Bell size={18} />
            {unreadCount > 0 && (
              <span style={{
                position: 'absolute',
                top: '-4px',
                right: '-4px',
                backgroundColor: 'var(--color-amber)',
                color: '#FFFFFF',
                fontSize: '0.625rem',
                fontWeight: 800,
                width: '16px',
                height: '16px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {unreadCount}
              </span>
            )}
          </button>

          {/* Notifications Dropdown */}
          {showNotifications && (
            <div style={{
              position: 'absolute',
              right: 0,
              top: 'calc(100% + 8px)',
              width: '320px',
              backgroundColor: '#FFFFFF',
              border: '1px solid var(--color-border)',
              borderRadius: '0.75rem',
              boxShadow: 'var(--shadow-xl)',
              padding: '1rem',
              zIndex: 50
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <span style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>Notifications</span>
                {unreadCount > 0 && (
                  <button
                    onClick={handleMarkAllRead}
                    style={{ background: 'none', border: 'none', color: 'var(--color-emerald)', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer' }}
                  >
                    Mark all read
                  </button>
                )}
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '240px', overflowY: 'auto' }}>
                {notifications.length === 0 ? (
                  <div style={{ fontSize: '0.8125rem', color: 'var(--color-muted)', textAlign: 'center', padding: '1rem 0' }}>
                    No recent notifications
                  </div>
                ) : (
                  notifications.map((n) => (
                    <div key={n.id} style={{
                      padding: '0.625rem',
                      borderRadius: '0.375rem',
                      backgroundColor: n.is_read ? '#FFFFFF' : 'var(--color-sage-light)',
                      border: '1px solid var(--color-border-light)'
                    }}>
                      <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--color-forest)' }}>{n.title}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--color-charcoal)', marginTop: '0.125rem' }}>{n.message}</div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
