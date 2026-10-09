import React from 'react';
import { Settings, Shield, Lock, FileText, CheckCircle2 } from 'lucide-react';

export const AuditSettingsPage = () => {
  const auditLogs = [
    { timestamp: '2025-10-09 11:15:30', user: 'admin', action: 'RUN_CSP_SOLVER', resource: 'ESE-AUT-2025', details: 'CSP solver executed: 24 subjects scheduled in 104.7ms with 0 clashes.' },
    { timestamp: '2025-10-09 10:45:12', user: 'admin', action: 'POPULATE_SUBJECTS', resource: 'ESE-AUT-2025', details: 'Configured 24 active subjects from engineering catalog.' },
    { timestamp: '2025-10-08 16:20:05', user: 'staff1', action: 'BULK_CSV_IMPORT', resource: 'STUDENTS', details: 'Imported 155 student registration records.' },
    { timestamp: '2025-10-08 09:10:00', user: 'admin', action: 'SESSION_CREATED', resource: 'ESE-AUT-2025', details: 'Created session ESE-AUT-2025 in Draft state.' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div>
        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 5 — AUDIT & SETTINGS</div>
        <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>System Audit Trail & Settings</h1>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 24 }}>
        <div className="card" style={{ padding: 22, display: 'flex', flexDirection: 'column', gap: 14 }}>
          <h3 style={{ fontSize: '1.1rem', color: '#14532D' }}>Institutional Parameters</h3>
          <div className="form-group">
            <label className="form-label">Institution Name</label>
            <input type="text" readOnly value="National Institute of Engineering & Technology" className="form-input" />
          </div>
          <div className="form-group">
            <label className="form-label">Active Academic Year</label>
            <input type="text" readOnly value="2025-2026" className="form-input" />
          </div>
          <div className="form-group">
            <label className="form-label">Controller of Examinations</label>
            <input type="text" readOnly value="Dr. K. S. Ramanathan, Ph.D." className="form-input" />
          </div>
        </div>

        <div className="card" style={{ padding: 22, display: 'flex', flexDirection: 'column', gap: 14 }}>
          <h3 style={{ fontSize: '1.1rem', color: '#14532D' }}>Immutable Audit Activity Log</h3>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>User</th>
                  <th>Action</th>
                  <th>Resource</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                {auditLogs.map((log, idx) => (
                  <tr key={idx}>
                    <td><span style={{ fontSize: '0.78rem', color: '#6B7280' }}>{log.timestamp}</span></td>
                    <td><b>{log.user}</b></td>
                    <td><span className="badge badge-validated">{log.action}</span></td>
                    <td>{log.resource}</td>
                    <td><span style={{ fontSize: '0.82rem', color: '#575E54' }}>{log.details}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
