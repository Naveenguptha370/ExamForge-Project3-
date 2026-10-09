import React from 'react';
import './facultyDirectoryStyles.css';

export function FacultyDirectoryView({ facultyList = [] }) {
  return (
    <div className="ef-faculty-directory-wrap">
      <h2 className="ef-dir-title">Faculty Roster & Invigilation Registry</h2>
      <div className="ef-faculty-grid">
        {facultyList.map(f => (
          <div key={f.id || f.faculty_id} className="ef-faculty-card">
            <h4>{f.user_name || f.faculty_id}</h4>
            <p>{f.department} - {f.designation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
