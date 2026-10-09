import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { Layers, BookOpen, Filter } from 'lucide-react';

export const SubjectConfigPage = () => {
  const [subjects, setSubjects] = useState([]);
  const [selectedDept, setSelectedDept] = useState('ALL');

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    const data = await api.getSubjects();
    setSubjects(data || []);
  };

  const filtered = subjects.filter((s) => {
    if (selectedDept === 'ALL') return true;
    return s.department_code === selectedDept;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 3 — CONFIGURATION</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Exam Subject Configurations</h1>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#6B7280' }}>Filter Dept:</span>
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
        </div>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Subject Code</th>
              <th>Subject Title</th>
              <th>Department / Branch</th>
              <th>Semester</th>
              <th>Credits</th>
              <th>Difficulty Weighting</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((s) => (
              <tr key={s.id}>
                <td><b>{s.code}</b></td>
                <td>{s.name}</td>
                <td>{s.department_code} / {s.branch_code || 'General'}</td>
                <td>Sem {s.semester_number}</td>
                <td><b>{s.credits}</b></td>
                <td><StatusBadge status={s.difficulty} /></td>
                <td><span className="badge badge-validated">Active Config</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
