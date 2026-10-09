import React, { useState } from 'react';
import './facultyDirectoryStyles.css';

export function FacultyDirectoryView({ facultyList }) {
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [search, setSearch] = useState('');

  const filtered = facultyList.filter(f => {
    const matchDept = selectedDept === 'ALL' || f.department === selectedDept;
    const matchSearch = !search || f.faculty_id.toLowerCase().includes(search.toLowerCase()) || f.user_name?.toLowerCase().includes(search.toLowerCase()) || f.department?.toLowerCase().includes(search.toLowerCase());
    return matchDept && matchSearch;
  });

  return (
    <div className="ef-faculty-directory-wrap">
      <div className="ef-dir-header">
        <h2 className="ef-dir-title">Faculty Roster & Invigilation Registry</h2>
        <div className="ef-dir-controls">
          <input
            className="ef-dir-search"
            placeholder="Search faculty by ID, name, department..."
            value={search} onChange={e => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="ef-faculty-grid">
        {filtered.map(f => (
          <div key={f.id || f.faculty_id} className="ef-faculty-card">
            <div className="ef-card-badge">{f.faculty_id}</div>
            <h4 className="ef-faculty-name">{f.user_name || f.name || 'Faculty Member'}</h4>
            <p className="ef-faculty-dept">{f.department}</p>
            <p className="ef-faculty-desig">{f.designation}</p>
            <div className="ef-card-meta">
              <span>Status: <strong>{f.status}</strong></span>
              <span>Email: {f.email}</span>
            </div>
            <button className="ef-btn-view-profile">View Availability Schedule</button>
          </div>
        ))}
      </div>
    </div>
  );
}
