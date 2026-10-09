import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { UserCheck, Clock, Shield } from 'lucide-react';

export const FacultyPage = () => {
  const [faculty, setFaculty] = useState([]);

  useEffect(() => {
    loadFaculty();
  }, []);

  const loadFaculty = async () => {
    const data = await api.getFaculty();
    setFaculty(data || []);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div>
        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 1 — FACULTY MANAGEMENT</div>
        <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Faculty Directory & Invigilator Workload</h1>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Employee ID</th>
              <th>Faculty Name</th>
              <th>Department</th>
              <th>Designation</th>
              <th>Email</th>
              <th>Assigned Duties</th>
              <th>Duty Limit</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {faculty.map((f) => (
              <tr key={f.id}>
                <td><b>{f.employee_id}</b></td>
                <td><b>{f.full_name}</b></td>
                <td>{f.department_code}</td>
                <td>{f.designation_display}</td>
                <td>{f.email}</td>
                <td>
                  <span style={{ fontWeight: 800, color: '#15803D' }}>{f.current_duties_count} duties</span>
                </td>
                <td>Max {f.max_duties_per_session} / session</td>
                <td><StatusBadge status={f.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
