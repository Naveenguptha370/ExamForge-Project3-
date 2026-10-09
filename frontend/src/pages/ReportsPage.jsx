import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { BarChart3, Download, DoorOpen, Users, FileText, CheckCircle2, TrendingUp } from 'lucide-react';

export default function ReportsPage() {
  const [summary, setSummary] = useState(null);
  const [rooms, setRooms] = useState([]);
  const [readiness, setReadiness] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [sData, rData, rdData] = await Promise.all([
        api.getExecutiveSummary(),
        api.getRoomUtilization(),
        api.getReadinessIndex()
      ]);
      setSummary(sData);
      setRooms(rData);
      setReadiness(rdData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDownloadPdf = () => {
    window.open(api.getExecutiveReportPdfUrl(), '_blank');
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Reports & Institutional Analytics
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 5 Module: Database-driven operational reporting, room utilization, and executive ReportLab PDF exports
          </p>
        </div>

        <button onClick={handleDownloadPdf} className="btn btn-gold">
          <Download size={16} /> Export Executive PDF Report
        </button>
      </div>

      {/* KPI Overview Summary Card */}
      <div className="card" style={{ marginBottom: '2rem', padding: '1.75rem' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)', marginBottom: '1.25rem' }}>
          Consolidated Examination Operations Status
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', fontWeight: 600 }}>Total Academic Departments</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)', marginTop: '0.25rem' }}>{summary?.overview?.departments ?? '...'}</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', marginTop: '0.25rem' }}>{summary?.overview?.courses ?? '...'} Degree Courses</div>
          </div>

          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', fontWeight: 600 }}>Scheduled Subjects</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)', marginTop: '0.25rem' }}>{summary?.examinations?.scheduled_exam_subjects ?? '...'} / {summary?.examinations?.total_exam_subjects ?? '...'}</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', marginTop: '0.25rem' }}>0 Active Conflicts</div>
          </div>

          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', fontWeight: 600 }}>Exam Hall Usable Capacity</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)', marginTop: '0.25rem' }}>{summary?.infrastructure_seating?.total_usable_capacity ?? '...'} Seats</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', marginTop: '0.25rem' }}>Alternate-Seat Spacing</div>
          </div>

          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', fontWeight: 600 }}>Overall Attendance Logged</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)', marginTop: '0.25rem' }}>{summary?.documents_attendance?.overall_attendance_rate ?? 0}%</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', marginTop: '0.25rem' }}>{summary?.documents_attendance?.present_count ?? 0} Candidates Present</div>
          </div>
        </div>
      </div>

      {/* Room & Infrastructure Utilization Report */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)' }}>
              Hall & Infrastructure Utilization Breakdown
            </h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>
              Real-time seat allocation vs maximum capacity
            </p>
          </div>
          <span className="badge badge-success">Optimal Spacing</span>
        </div>

        <div className="table-container" style={{ border: 'none' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Hall Number</th>
                <th>Building Complex</th>
                <th>Floor</th>
                <th>Usable Capacity</th>
                <th>Exams Hosted</th>
                <th>Students Seated</th>
                <th>Utilization %</th>
                <th>Hall Status</th>
              </tr>
            </thead>
            <tbody>
              {rooms.map((r, i) => (
                <tr key={i}>
                  <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{r.room_number}</td>
                  <td>{r.building}</td>
                  <td>Floor {r.floor}</td>
                  <td>{r.usable_capacity} Seats</td>
                  <td>{r.exams_hosted} Papers</td>
                  <td style={{ fontWeight: 700 }}>{r.total_students_seated} Candidates</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <div style={{ width: '80px', height: '6px', backgroundColor: 'var(--color-border-light)', borderRadius: '9999px', overflow: 'hidden' }}>
                        <div style={{ width: `${Math.min(r.utilization_rate, 100)}%`, height: '100%', backgroundColor: 'var(--color-emerald)', borderRadius: '9999px' }} />
                      </div>
                      <span style={{ fontWeight: 700, fontSize: '0.75rem' }}>{r.utilization_rate}%</span>
                    </div>
                  </td>
                  <td>
                    <span className={r.status === 'AVAILABLE' ? 'badge badge-success' : 'badge badge-danger'}>
                      {r.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
