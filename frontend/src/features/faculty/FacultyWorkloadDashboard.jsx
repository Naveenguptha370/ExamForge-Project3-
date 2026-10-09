import React from 'react';
import './workloadStyles.css';

export function FacultyWorkloadDashboard({ workloadStats }) {
  return (
    <div className="ef-workload-container">
      <div className="ef-workload-header">
        <h2 className="ef-workload-title">Faculty Duty Equity & Workload Analytics</h2>
        <p className="ef-workload-desc">Institutional invigilation load distribution and balance metrics.</p>
      </div>

      <div className="ef-metrics-grid">
        <div className="ef-metric-card">
          <div className="ef-metric-label">Total Faculty Monitored</div>
          <div className="ef-metric-val">{workloadStats?.total || 148}</div>
        </div>
        <div className="ef-metric-card">
          <div className="ef-metric-label">Average Assigned Duties</div>
          <div className="ef-metric-val">{workloadStats?.avg || 5.2}</div>
        </div>
        <div className="ef-metric-card">
          <div className="ef-metric-label">Equity Variance Index</div>
          <div className="ef-metric-val success">0.42 (Optimal)</div>
        </div>
      </div>
    </div>
  );
}
