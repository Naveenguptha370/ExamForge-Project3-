import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon, color = 'forest', trend }) {
  const colorMap = {
    forest: { bg: 'var(--color-sage)', text: 'var(--color-forest)' },
    emerald: { bg: '#e8f5e9', text: 'var(--color-emerald)' },
    amber: { bg: '#fef3c7', text: 'var(--color-amber)' },
    gold: { bg: 'var(--color-gold-light)', text: '#92400e' },
  };

  const theme = colorMap[color] || colorMap.forest;

  return (
    <div className="card" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--color-muted)', marginBottom: '0.25rem' }}>
            {title}
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-forest)', fontFamily: 'var(--font-heading)' }}>
            {value}
          </div>
          {subtitle && (
            <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>
              {subtitle}
            </div>
          )}
        </div>

        {Icon && (
          <div style={{
            width: '2.75rem',
            height: '2.75rem',
            borderRadius: '0.75rem',
            backgroundColor: theme.bg,
            color: theme.text,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Icon size={22} />
          </div>
        )}
      </div>

      {trend && (
        <div style={{ marginTop: '0.75rem', paddingTop: '0.5rem', borderTop: '1px solid var(--color-border-light)', fontSize: '0.75rem', color: 'var(--color-emerald)', fontWeight: 600 }}>
          {trend}
        </div>
      )}
    </div>
  );
}
