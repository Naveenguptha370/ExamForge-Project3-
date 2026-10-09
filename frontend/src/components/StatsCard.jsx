import React from 'react';

export const StatsCard = ({ title, value, subtitle, icon, trend, color = '#15803D' }) => {
  return (
    <div className="card card-hover" style={{ padding: '20px 22px', display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#6B7280' }}>{title}</span>
        <div style={{ padding: 8, borderRadius: 10, backgroundColor: '#FAF9F6', color: color, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {icon}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 10 }}>
        <span style={{ fontSize: '1.85rem', fontWeight: 800, color: '#242923', fontFamily: 'var(--font-display)' }}>
          {value}
        </span>
        {trend && (
          <span style={{ fontSize: '0.78rem', fontWeight: 600, color: '#16A34A', backgroundColor: '#DCFCE7', padding: '2px 6px', borderRadius: 4 }}>
            {trend}
          </span>
        )}
      </div>
      {subtitle && <span style={{ fontSize: '0.78rem', color: '#6B7280' }}>{subtitle}</span>}
    </div>
  );
};
