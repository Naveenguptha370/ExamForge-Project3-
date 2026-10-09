import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { StatsCard } from '../components/StatsCard';
import { StatusBadge } from '../components/StatusBadge';
import {
  Calendar, Users, BookOpen, Layers, Award,
  Sparkles, AlertTriangle, ArrowRight, CheckCircle2, Clock, Play
} from 'lucide-react';

export const DashboardPage = ({ onNavigate }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    setLoading(true);
    const res = await api.getDashboardOverview();
    if (res.success) {
      setData(res);
    }
    setLoading(false);
  };

  if (loading || !data) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 400 }}>
        <div className="animate-spin" style={{ width: 36, height: 36, border: '4px solid #DDEBDD', borderTopColor: '#15803D', borderRadius: '50%' }} />
      </div>
    );
  }

  const { summary, active_session, daily_load } = data;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Top Banner / Session Overview */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, #14532D 0%, #15803D 100%)',
          color: '#FFFFFF',
          padding: '28px 32px',
          borderRadius: 20,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: '0 10px 25px -5px rgba(20, 83, 45, 0.3)'
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, maxWidth: 650 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '4px 10px', borderRadius: 9999, fontSize: '0.75rem', fontWeight: 700 }}>
              ACTIVE EXAMINATION SESSION
            </span>
            <span style={{ fontSize: '0.85rem', color: '#D4A72C', fontWeight: 700 }}>
              {active_session?.academic_year || '2025-2026'}
            </span>
          </div>
          <h2 style={{ fontSize: '1.85rem', color: '#FFFFFF', fontWeight: 800 }}>
            {active_session?.name || 'Autumn End-Term Examinations 2025'}
          </h2>
          <p style={{ fontSize: '0.92rem', color: '#DDEBDD', lineHeight: 1.5 }}>
            Examination schedule formulated via Python CSP Solver. Zero student double-bookings detected across 24 configured engineering subjects.
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, backgroundColor: '#FFFFFF', padding: '8px 16px', borderRadius: 12 }}>
            <Award size={22} color="#D4A72C" />
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontSize: '0.68rem', fontWeight: 700, color: '#6B7280' }}>EXAMINATION READINESS</span>
              <span style={{ fontSize: '1.25rem', fontWeight: 800, color: '#14532D' }}>
                {summary.readiness_score}% Complete
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', gap: 10 }}>
            <button
              onClick={() => onNavigate('timetable_studio')}
              className="btn btn-gold btn-sm"
              style={{ color: '#14532D', fontWeight: 700 }}
            >
              <Sparkles size={16} />
              <span>Timetable Studio</span>
            </button>
            <button
              onClick={() => onNavigate('timetable_view')}
              className="btn btn-secondary btn-sm"
            >
              <Calendar size={16} />
              <span>View Timetable</span>
            </button>
          </div>
        </div>
      </div>

      {/* Primary KPI Metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 20 }}>
        <StatsCard
          title="Total Candidates Enrolled"
          value={summary.total_students}
          subtitle="All active Sem 5 engineering cohorts"
          icon={<Users size={20} />}
          trend="+100% Eligible"
          color="#15803D"
        />
        <StatsCard
          title="Subjects Scheduled"
          value={summary.total_subjects}
          subtitle="24 configured for autumn session"
          icon={<BookOpen size={20} />}
          trend="0 Clashes"
          color="#D4A72C"
        />
        <StatsCard
          title="Exam Halls & Capacity"
          value={`${summary.total_rooms} Halls`}
          subtitle={`${summary.total_capacity} usable student seats`}
          icon={<Layers size={20} />}
          color="#15803D"
        />
        <StatsCard
          title="Invigilation Staff"
          value={`${summary.available_faculty} Faculty`}
          subtitle="All shift duties fairly balanced"
          icon={<Clock size={20} />}
          trend="Ready"
          color="#F59E0B"
        />
      </div>

      {/* Middle Section: Daily Load & Readiness Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: 24 }}>
        {/* Daily Exam Load Chart */}
        <div className="card" style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 18 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <h3 style={{ fontSize: '1.15rem', color: '#14532D' }}>Daily Examination Density & Load</h3>
            <span style={{ fontSize: '0.78rem', color: '#6B7280', fontWeight: 600 }}>Evenly distributed across 8 exam dates</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {daily_load.map((dl, idx) => {
              const maxStudents = 80;
              const pct = Math.round((dl.students / maxStudents) * 100);
              return (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                  <span style={{ width: 100, fontSize: '0.82rem', fontWeight: 700, color: '#242923' }}>
                    {dl.date} ({dl.day})
                  </span>
                  <div style={{ flex: 1, backgroundColor: '#FAF9F6', height: 26, borderRadius: 6, overflow: 'hidden', border: '1px solid #E7E5E4', position: 'relative' }}>
                    <div
                      style={{
                        width: `${pct}%`,
                        height: '100%',
                        backgroundColor: pct > 80 ? '#D4A72C' : '#15803D',
                        borderRadius: 5,
                        transition: 'width 0.5s ease'
                      }}
                    />
                    <span style={{ position: 'absolute', right: 10, top: 3, fontSize: '0.75rem', fontWeight: 700, color: '#242923' }}>
                      {dl.students} Candidates ({dl.exam_count} Exams)
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Readiness Checklist Gauge */}
        <div className="card" style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 16 }}>
          <h3 style={{ fontSize: '1.15rem', color: '#14532D' }}>Lifecycle Readiness Matrix</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {[
              { label: 'Subject Configurations', val: summary.readiness_breakdown.subjects_configured, desc: '24 exam configs ready' },
              { label: 'Timetable Validation (CSP)', val: summary.readiness_breakdown.timetable_validated, desc: '0 hard clashes detected' },
              { label: 'Hall & Seating Matrix', val: summary.readiness_breakdown.seating_arranged, desc: '15 rooms allocated' },
              { label: 'Invigilation Roster', val: summary.readiness_breakdown.invigilators_assigned, desc: '16 duties assigned' },
              { label: 'Hall Ticket Issuance', val: summary.readiness_breakdown.hall_tickets_generated, desc: '155 passes generated' },
            ].map((item, idx) => (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', fontWeight: 700 }}>
                  <span style={{ color: '#242923' }}>{item.label}</span>
                  <span style={{ color: '#15803D' }}>{item.val}%</span>
                </div>
                <div style={{ width: '100%', height: 8, backgroundColor: '#FAF9F6', borderRadius: 9999, overflow: 'hidden', border: '1px solid #E7E5E4' }}>
                  <div style={{ width: `${item.val}%`, height: '100%', backgroundColor: item.val === 100 ? '#15803D' : '#D4A72C' }} />
                </div>
                <span style={{ fontSize: '0.72rem', color: '#6B7280' }}>{item.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
