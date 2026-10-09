import React, { useState } from 'react';
import './userManagementStyles.css';

export function UserManagementView({ users, onRefresh }) {
  const [filterRole, setFilterRole] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredUsers = users.filter(u => {
    const matchesRole = filterRole === 'ALL' || u.role === filterRole;
    const matchesSearch = !searchTerm || u.username.toLowerCase().includes(searchTerm.toLowerCase()) || (u.email && u.email.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesRole && matchesSearch;
  });

  return (
    <div className="ef-user-mgmt-container">
      <div className="ef-user-header">
        <div>
          <h2 className="ef-section-title">Institutional User Governance</h2>
          <p className="ef-section-desc">Manage system access, roles, and status for university accounts.</p>
        </div>
        <div className="ef-user-actions">
          <input
            type="text"
            className="ef-search-bar"
            placeholder="Search by username or email..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
          <select className="ef-select-filter" value={filterRole} onChange={e => setFilterRole(e.target.value)}>
            <option value="ALL">All Roles</option>
            <option value="ADMIN">Administrator</option>
            <option value="FACULTY">Faculty</option>
            <option value="EXAM_STAFF">Exam Staff</option>
            <option value="STUDENT">Student</option>
          </select>
        </div>
      </div>

      <div className="ef-table-card">
        <table className="ef-data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map(u => (
              <tr key={u.id}>
                <td>#{u.id}</td>
                <td className="ef-font-medium">{u.username}</td>
                <td>{u.email}</td>
                <td><span className={`ef-role-pill ${u.role.toLowerCase()}`}>{u.role}</span></td>
                <td><span className={`ef-status-pill ${u.status ? u.status.toLowerCase() : 'active'}`}>{u.status || 'ACTIVE'}</span></td>
                <td>
                  <button className="ef-action-btn">Edit</button>
                  <button className="ef-action-btn danger">Deactivate</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
