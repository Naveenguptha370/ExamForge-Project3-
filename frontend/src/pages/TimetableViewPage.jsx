import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { Download, FileText, Printer } from 'lucide-react';

export const TimetableViewPage = () => {
  const [entries, setEntries] = useState([]);
  const [selectedDept, setSelectedDept] = useState('ALL');

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    const data = await api.getTimetableEntries(1);
    setEntries(data || []);
  };

  const filtered = entries.filter((e) => {
    if (selectedDept === 'ALL') return true;
    return e.department_code === selectedDept;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div className="no-print" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>OFFICIAL TIMETABLE</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Published Examination Schedule</h1>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="form-select"
            style={{ padding: '6px 12px', fontSize: '0.85rem', width: 'auto' }}
          >
            <option value="ALL">All Departments</option>
            <option value="CSE">CSE</option>
            <option value="ECE">ECE</option>
            <option value="MECH">MECH</option>
            <option value="EEE">EEE</option>
            <option value="CIVIL">CIVIL</option>
          </select>
          <button onClick={() => window.print()} className="btn btn-secondary btn-sm">
            <Printer size={15} />
            <span>Print View</span>
          </button>
          <button onClick={() => window.open('/api/scheduling/timetables/1/export-pdf/', '_blank')} className="btn btn-primary btn-sm">
            <FileText size={15} color="#D4A72C" />
            <span>Download Official PDF</span>
          </button>
        </div>
      </div>

      <div className="card" style={{ padding: 28, backgroundColor: '#FFFFFF' }}>
        <div style={{ textAlign: 'center', marginBottom: 24, borderBottom: '2px solid #14532D', paddingBottom: 16 }}>
          <h2 style={{ fontSize: '1.4rem', color: '#14532D', textTransform: 'uppercase' }}>
            National Institute of Engineering & Technology
          </h2>
          <h3 style={{ fontSize: '1.1rem', color: '#15803D', marginTop: 4 }}>
            OFFICIAL EXAMINATION TIMETABLE — AUTUMN TERM 2025
          </h3>
          <span style={{ fontSize: '0.82rem', color: '#6B7280' }}>
            Session Code: ESE-AUT-2025 • Version: v1.0 • Approved & Published
          </span>
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Date & Day</th>
                <th>Shift & Timings</th>
                <th>Subject Code</th>
                <th>Subject Title</th>
                <th>Department / Branch</th>
                <th>Sem</th>
                <th>Credits</th>
                <th>Candidates</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((e) => (
                <tr key={e.id}>
                  <td><b>{e.exam_date}</b></td>
                  <td>
                    <span style={{ fontWeight: 600 }}>{e.time_range}</span>
                    <span style={{ display: 'block', fontSize: '0.75rem', color: '#15803D', fontWeight: 700 }}>{e.shift}</span>
                  </td>
                  <td><b>{e.subject_code}</b></td>
                  <td><b>{e.subject_name}</b></td>
                  <td>{e.department_code} / {e.branch_code || 'General'}</td>
                  <td>Sem {e.semester_number}</td>
                  <td>{e.credits}</td>
                  <td>{e.expected_students}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
