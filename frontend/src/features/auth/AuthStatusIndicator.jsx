import React from 'react';
import './authStyles.css';

export function AuthStatusIndicator({ user, onLogout }) {
  if (!user) return null;

  return (
    <div className="ef-auth-status-bar">
      <div className="ef-user-avatar">
        {(user.first_name?.[0] || user.username?.[0] || 'U').toUpperCase()}
      </div>
      <div className="ef-user-info">
        <span className="ef-user-name">{user.first_name ? `${user.first_name} ${user.last_name}` : user.username}</span>
        <span className="ef-user-role-badge">{user.role}</span>
      </div>
      <button onClick={onLogout} className="ef-btn-logout">Logout</button>
    </div>
  );
}
