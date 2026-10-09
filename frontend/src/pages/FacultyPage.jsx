import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { UserCheck, Calendar, Shield, CheckCircle2, XCircle, Search, Filter } from 'lucide-react';

export default function FacultyPage() {
  const [faculty, setFaculty] = useState([]);
  const [leaves, setLeaves] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const facData = await api.getFacultyProfiles(`?search=${encodeURIComponent(search)}`);
      setFaculty(facData.results || facData);
      const sumData = await api.getFacultySummary();
      setSummary(sumData);
      const leaveData = await api.getFacultyLeaves();
      setLeaves(leaveData.results || leaveData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [search]);

  const handleApproveLeave = async (leaveId) => {
    try {
      await api.approveFacultyLeave(leaveId);
      loadData();
    } catch (e) {
      alert('Error approving leave: ' + e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
          Faculty Directory & Invigilator Availability
        </h2>
        <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
          Member 1 Module: Faculty profiles, department links, duty workloads, and leave schedules
        </p>
      </div>

      {/* Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Total Faculty</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>{summary?.total_faculty ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Available for Duty</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-emerald)' }}>{summary?.available_faculty ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Pending Leaves</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-amber)' }}>{summary?.pending_leaves ?? '...'}</div>
        </div>
      </div>

      {/* Faculty Directory Table */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-forest)' }}>Faculty Members</h3>
          <div style={{ width: '250px', position: 'relative' }}>
            <Search size={14} color="var(--color-muted)" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)' }} />
            <input
              type="text"
              className="form-input"
              style={{ paddingLeft: '2rem', padding: '0.375rem 2rem 0.375rem 2rem', fontSize: '0.8125rem' }}
              placeholder="Search faculty..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        <div className="table-container" style={{ border: 'none' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Employee ID</th>
                <th>Faculty Name</th>
                <th>Department</th>
                <th>Designation</th>
                <th>Max Duties / Term</th>
                <th>Duty Status</th>
              </tr>
            </thead>
            <tbody>
              {faculty.map((f) => (
                <tr key={f.id}>
                  <td style={{ fontWeight: 700, color: 'var(--color-forest)' }}>{f.employee_id}</td>
                  <td style={{ fontWeight: 600 }}>{f.full_name || f.user_details?.username}</td>
                  <td>{f.department_name} ({f.department_code})</td>
                  <td><span className="badge badge-neutral">{f.designation}</span></td>
                  <td>{f.max_duties_per_term} sessions</td>
                  <td>
                    <span className={f.is_available_for_duty ? 'badge badge-success' : 'badge badge-danger'}>
                      {f.is_available_for_duty ? 'Available' : 'Unavailable'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Leaves Section */}
      <div className="card">
        <div className="card-header">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-forest)' }}>
            Leave Applications & Availability Constraints
          </h3>
          <span className="badge badge-neutral">{leaves.length} Applications</span>
        </div>

        <div className="table-container" style={{ border: 'none' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Faculty</th>
                <th>Leave Duration</th>
                <th>Reason</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {leaves.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '1.5rem', color: 'var(--color-muted)' }}>
                    No pending leave applications. All faculty available for invigilation.
                  </td>
                </tr>
              ) : (
                leaves.map((l) => (
                  <tr key={l.id}>
                    <td style={{ fontWeight: 600 }}>{l.faculty_name} ({l.employee_id})</td>
                    <td>{l.start_date} to {l.end_date}</td>
                    <td style={{ maxWidth: '280px' }}>{l.reason}</td>
                    <td>
                      <span className={l.status === 'APPROVED' ? 'badge badge-success' : (l.status === 'PENDING' ? 'badge badge-warning' : 'badge badge-danger')}>
                        {l.status}
                      </span>
                    </td>
                    <td>
                      {l.status === 'PENDING' && (
                        <button
                          onClick={() => handleApproveLeave(l.id)}
                          className="btn btn-secondary btn-sm"
                        >
                          Approve Leave
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
