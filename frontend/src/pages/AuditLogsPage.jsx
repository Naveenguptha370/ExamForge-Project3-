import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { History, Shield, Clock, Search, Filter } from 'lucide-react';

export default function AuditLogsPage() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionFilter, setActionFilter] = useState('');

  const loadLogs = async () => {
    setLoading(true);
    try {
      let q = '';
      if (actionFilter) q = `?action=${actionFilter}`;
      const data = await api.getAuditLogs(q);
      setLogs(data.results || data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [actionFilter]);

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            System Audit Trail & Security Logs
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 5 Module: Immutable activity records, administrative actions, and operational governance
          </p>
        </div>

        <select
          className="form-select"
          style={{ width: 'auto', minWidth: '180px' }}
          value={actionFilter}
          onChange={(e) => setActionFilter(e.target.value)}
        >
          <option value="">All Operations</option>
          <option value="PUBLISH">Publish</option>
          <option value="GENERATE">Generate</option>
          <option value="APPROVE">Approve</option>
          <option value="UPDATE">Update</option>
          <option value="CREATE">Create</option>
          <option value="BLOCK">Block</option>
        </select>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Operation</th>
              <th>Resource Type</th>
              <th>Resource ID</th>
              <th>Actor Username</th>
              <th>Operational Details</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-muted)' }}>
                  No audit logs recorded matching filter.
                </td>
              </tr>
            ) : (
              logs.map((l) => (
                <tr key={l.id}>
                  <td style={{ fontSize: '0.75rem', color: 'var(--color-muted)', whiteSpace: 'nowrap' }}>
                    {new Date(l.timestamp).toLocaleString()}
                  </td>
                  <td>
                    <span className="badge badge-gold" style={{ fontSize: '0.6875rem' }}>
                      {l.action}
                    </span>
                  </td>
                  <td style={{ fontWeight: 700, color: 'var(--color-forest)' }}>{l.resource_type}</td>
                  <td><code>{l.resource_id || '—'}</code></td>
                  <td>
                    <span style={{ fontWeight: 600 }}>{l.actor_username}</span> ({l.actor_role})
                  </td>
                  <td style={{ fontSize: '0.75rem', color: 'var(--color-charcoal)', maxWidth: '320px' }}>
                    {JSON.stringify(l.details)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
