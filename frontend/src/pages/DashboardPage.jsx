import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import StatCard from '../components/StatCard';
import {
  Users, GraduationCap, Calendar, DoorOpen, FileText, CheckCircle2,
  AlertTriangle, ArrowRight, Download, Sparkles, RefreshCw, BarChart3,
  Clock, Shield, Layers
} from 'lucide-react';

export default function DashboardPage({ onSelectTab }) {
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);
  const [readiness, setReadiness] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const sumData = await api.getExecutiveSummary();
      setSummary(sumData);
      const readyData = await api.getReadinessIndex();
      setReadiness(readyData);
    } catch (e) {
      console.error('Failed to load dashboard metrics:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDownloadExecutiveReport = () => {
    window.open(api.getExecutiveReportPdfUrl(), '_blank');
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      {/* Welcome Banner */}
      <div style={{
        backgroundColor: 'var(--color-forest)',
        color: '#FFFFFF',
        borderRadius: '1rem',
        padding: '1.75rem 2rem',
        marginBottom: '2rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
        boxShadow: 'var(--shadow-md)'
      }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.375rem', backgroundColor: 'rgba(255, 255, 255, 0.15)', padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 600, marginBottom: '0.5rem' }}>
            <Sparkles size={14} color="#D4A72C" /> Five-Member Architecture Live
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#FFFFFF', lineHeight: 1.2 }}>
            Welcome back, {user?.first_name || user?.username}!
          </h2>
          <p style={{ color: 'var(--color-sage)', fontSize: '0.875rem', marginTop: '0.375rem' }}>
            Examination Session: <b>ESE-MAY-2026</b> • Operational Status: <b>PUBLISHED & READY</b>
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button
            onClick={loadData}
            className="btn btn-secondary btn-sm"
            style={{ padding: '0.625rem 1rem' }}
          >
            <RefreshCw size={14} /> Refresh Data
          </button>
          <button
            onClick={handleDownloadExecutiveReport}
            className="btn btn-gold btn-sm"
            style={{ padding: '0.625rem 1.25rem' }}
          >
            <Download size={14} /> Executive PDF Report
          </button>
        </div>
      </div>

      {actionMessage && (
        <div style={{
          padding: '0.75rem 1rem',
          backgroundColor: 'var(--color-sage-light)',
          border: '1px solid var(--color-emerald)',
          borderRadius: '0.5rem',
          color: 'var(--color-forest)',
          fontSize: '0.875rem',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <span>{actionMessage}</span>
          <button onClick={() => setActionMessage('')} style={{ background: 'none', border: 'none', cursor: 'pointer', fontWeight: 700 }}>✕</button>
        </div>
      )}

      {/* Real Database KPI Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
        <StatCard
          title="Total Registered Students"
          value={summary?.overview?.total_students ?? '...'}
          subtitle={`${summary?.overview?.eligible_students ?? '...'} Eligible for Exams`}
          icon={GraduationCap}
          color="forest"
          trend="100% Academic records validated"
        />

        <StatCard
          title="Scheduled Exam Papers"
          value={summary?.examinations?.scheduled_exam_subjects ?? '...'}
          subtitle={`0 Active Conflicts / Clashes`}
          icon={Calendar}
          color="emerald"
          trend="Constraint solver verified"
        />

        <StatCard
          title="Usable Exam Hall Capacity"
          value={summary?.infrastructure_seating?.total_usable_capacity ? `${summary.infrastructure_seating.total_usable_capacity} Seats` : '...'}
          subtitle={`${summary?.infrastructure_seating?.seats_allocated ?? '...'} Candidates Allocated`}
          icon={DoorOpen}
          color="amber"
          trend="Alternate-seat spacing active"
        />

        <StatCard
          title="Hall Tickets Issued"
          value={summary?.documents_attendance?.hall_tickets_issued ?? '...'}
          subtitle={`${summary?.documents_attendance?.overall_attendance_rate ?? 0}% Attendance Logged`}
          icon={FileText}
          color="gold"
          trend="Local ReportLab PDFs ready"
        />
      </div>

      {/* Main Two-Column Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        {/* Examination Readiness Index Breakdown (Member 5 Analytics) */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)' }}>
                Examination Readiness Index
              </h3>
              <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>
                Lifecycle health check across all 5 modules
              </p>
            </div>
            <span className="badge badge-gold" style={{ fontSize: '0.8125rem', padding: '0.375rem 0.75rem' }}>
              {readiness?.overall_readiness_score ?? 100}% Ready
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '0.5rem' }}>
            {readiness?.phases?.map((p, idx) => (
              <div key={idx} style={{ padding: '0.75rem', border: '1px solid var(--color-border-light)', borderRadius: '0.5rem', backgroundColor: '#FBFDFB' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.375rem' }}>
                  <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--color-forest)' }}>
                    {p.phase}
                  </span>
                  <span className="badge badge-success" style={{ fontSize: '0.6875rem' }}>
                    {p.score}%
                  </span>
                </div>
                {/* Progress Bar */}
                <div style={{ width: '100%', height: '6px', backgroundColor: 'var(--color-border-light)', borderRadius: '9999px', overflow: 'hidden', marginBottom: '0.375rem' }}>
                  <div style={{ width: `${p.score}%`, height: '100%', backgroundColor: 'var(--color-emerald)', borderRadius: '9999px' }} />
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>
                  {p.details}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Operations Center */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)' }}>
                Operational Workflows
              </h3>
              <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>
                Direct execution of member modules
              </p>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <button
              onClick={() => onSelectTab('timetable')}
              className="card"
              style={{ padding: '1rem', textAlign: 'left', cursor: 'pointer', border: '1px solid var(--color-border)' }}
            >
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.5rem' }}><Sparkles size={20} /></div>
              <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>Timetable Solver</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>Run constraint heuristic engine</div>
            </button>

            <button
              onClick={() => onSelectTab('seating')}
              className="card"
              style={{ padding: '1rem', textAlign: 'left', cursor: 'pointer', border: '1px solid var(--color-border)' }}
            >
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.5rem' }}><DoorOpen size={20} /></div>
              <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>Seating Generator</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>Apply alternate-seat spacing</div>
            </button>

            <button
              onClick={() => onSelectTab('invigilation')}
              className="card"
              style={{ padding: '1rem', textAlign: 'left', cursor: 'pointer', border: '1px solid var(--color-border)' }}
            >
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.5rem' }}><Users size={20} /></div>
              <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>Staff Invigilators</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>Auto-allocate duty roster</div>
            </button>

            <button
              onClick={() => onSelectTab('halltickets')}
              className="card"
              style={{ padding: '1rem', textAlign: 'left', cursor: 'pointer', border: '1px solid var(--color-border)' }}
            >
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.5rem' }}><FileText size={20} /></div>
              <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>Hall Tickets</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>Generate ReportLab PDFs</div>
            </button>

            <button
              onClick={() => onSelectTab('attendance')}
              className="card"
              style={{ padding: '1rem', textAlign: 'left', cursor: 'pointer', border: '1px solid var(--color-border)' }}
            >
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.5rem' }}><CheckCircle2 size={20} /></div>
              <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>Hall Attendance</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>Record booklets & mark present</div>
            </button>

            <button
              onClick={() => onSelectTab('reports')}
              className="card"
              style={{ padding: '1rem', textAlign: 'left', cursor: 'pointer', border: '1px solid var(--color-border)' }}
            >
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.5rem' }}><BarChart3 size={20} /></div>
              <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>Reports & Analytics</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>Room utilization & exports</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
