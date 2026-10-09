import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { BookOpen, Layers } from 'lucide-react';

export const AcademicsPage = () => {
  const [departments, setDepartments] = useState([]);
  const [subjects, setSubjects] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const [depts, subs] = await Promise.all([api.getDepartments(), api.getSubjects()]);
    setDepartments(depts || []);
    setSubjects(subs || []);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      <div>
        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 2 — CURRICULUM</div>
        <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Academic Departments & Curriculum</h1>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20 }}>
        {departments.map((d) => (
          <div key={d.id} className="card" style={{ padding: 22, display: 'flex', flexDirection: 'column', gap: 10, borderLeft: '4px solid #15803D' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#15803D' }}>CODE: {d.code}</span>
            <h3 style={{ fontSize: '1.1rem', color: '#14532D' }}>{d.name}</h3>
            <span style={{ fontSize: '0.85rem', color: '#575E54' }}><b>HOD:</b> {d.head_of_department}</span>
          </div>
        ))}
      </div>

      <div className="card" style={{ padding: 24 }}>
        <h3 style={{ fontSize: '1.15rem', color: '#14532D', marginBottom: 16 }}>Academic Subjects Registry</h3>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Subject Name</th>
                <th>Department / Branch</th>
                <th>Semester</th>
                <th>Credits</th>
                <th>Difficulty</th>
              </tr>
            </thead>
            <tbody>
              {subjects.map((s) => (
                <tr key={s.id}>
                  <td><b>{s.code}</b></td>
                  <td>{s.name}</td>
                  <td>{s.department_code} / {s.branch_code || 'Core'}</td>
                  <td>Sem {s.semester_number}</td>
                  <td><b>{s.credits}</b></td>
                  <td><span className="badge badge-validated">{s.difficulty}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
