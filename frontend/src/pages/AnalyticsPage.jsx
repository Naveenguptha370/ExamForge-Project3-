import React from 'react';
import { Award, BarChart3, Users, BookOpen, Layers } from 'lucide-react';

export const AnalyticsPage = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div>
        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 5 — ANALYTICS</div>
        <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Institutional Examination Readiness & Reports</h1>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 24 }}>
        {/* Readiness Gauge */}
        <div className="card" style={{ padding: 28, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', gap: 16 }}>
          <Award size={48} color="#D4A72C" />
          <h3 style={{ fontSize: '1.3rem', color: '#14532D' }}>Overall Examination Readiness</h3>
          <div style={{ fontSize: '3.5rem', fontWeight: 800, color: '#14532D', fontFamily: 'var(--font-display)', lineHeight: 1 }}>
            92%
          </div>
          <span style={{ fontSize: '0.82rem', color: '#15803D', fontWeight: 700, backgroundColor: '#DCFCE7', padding: '4px 12px', borderRadius: 9999 }}>
            ✓ Ready for Autumn 2025 Examination Series
          </span>
        </div>

        {/* Readiness Breakdown */}
        <div className="card" style={{ padding: 28, display: 'flex', flexDirection: 'column', gap: 16 }}>
          <h3 style={{ fontSize: '1.2rem', color: '#14532D' }}>Lifecycle Stage Progress</h3>
          {[
            { name: '1. Curriculum & Subject Configuration', pct: 100, status: 'Completed (24/24 subjects configured)' },
            { name: '2. CSP Constraint Solver & Timetable', pct: 100, status: 'Completed (0 hard clashes, Validated)' },
            { name: '3. Room Allocation & Usable Capacity', pct: 85, status: '15 Halls allocated (640 capacity)' },
            { name: '4. Invigilator Workload Distribution', pct: 90, status: '16 Faculty duty rosters balanced' },
            { name: '5. Student Hall Tickets & Passes', pct: 85, status: '155 Admit cards compiled & verified' },
          ].map((item, idx) => (
            <div key={idx} style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', fontWeight: 700 }}>
                <span>{item.name}</span>
                <span style={{ color: '#15803D' }}>{item.pct}%</span>
              </div>
              <div style={{ width: '100%', height: 10, backgroundColor: '#FAF9F6', borderRadius: 9999, border: '1px solid #E7E5E4', overflow: 'hidden' }}>
                <div style={{ width: `${item.pct}%`, height: '100%', backgroundColor: '#15803D', borderRadius: 9999 }} />
              </div>
              <span style={{ fontSize: '0.75rem', color: '#6B7280' }}>{item.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
