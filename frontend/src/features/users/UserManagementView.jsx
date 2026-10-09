import React, { useState } from 'react';
import './userManagementStyles.css';

export function UserManagementView({ users = [] }) {
  const [filterRole, setFilterRole] = useState('ALL');
  return (
    <div className="ef-user-mgmt-container">
      <h2 className="ef-section-title">Institutional User Governance</h2>
      <p className="ef-section-desc">Manage system access, roles, and status for university accounts.</p>
      <div className="ef-table-card">
        <table className="ef-data-table">
          <thead>
            <tr><th>Username</th><th>Email</th><th>Role</th><th>Status</th></tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id || u.username}>
                <td>{u.username}</td><td>{u.email}</td><td>{u.role}</td><td>{u.status || 'ACTIVE'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
