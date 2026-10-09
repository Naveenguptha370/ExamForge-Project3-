import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { FileText, Download, Sparkles, Search, Shield, Ban, Eye, CheckCircle2 } from 'lucide-react';

export default function HallTicketsPage() {
  const [tickets, setTickets] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState('');
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');

  const loadSessions = async () => {
    try {
      const data = await api.getExamSessions();
      const list = data.results || data;
      setSessions(list);
      if (list.length > 0 && !selectedSessionId) {
        setSelectedSessionId(list[0].id);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const loadTickets = async () => {
    setLoading(true);
    try {
      let q = `?search=${encodeURIComponent(search)}`;
      if (selectedSessionId) q += `&exam_session=${selectedSessionId}`;
      const data = await api.getHallTickets(q);
      setTickets(data.results || data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    loadTickets();
  }, [selectedSessionId, search]);

  const handleBulkGenerate = async () => {
    if (!selectedSessionId) return;
    setLoading(true);
    try {
      const res = await api.bulkGenerateHallTickets(selectedSessionId);
      alert(res.message);
      loadTickets();
    } catch (e) {
      alert('Error generating hall tickets: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleBlock = async (ticket) => {
    const reason = prompt('Enter administrative reason:', ticket.block_reason || 'Pending disciplinary inquiry');
    if (reason === null) return;
    try {
      await api.toggleBlockHallTicket(ticket.id, reason);
      loadTickets();
    } catch (e) {
      alert(e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Hall Ticket & Admit Card Subsystem
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 5 Module: Local ReportLab PDF generation, eligibility verification gate, and security hashes
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <select
            className="form-select"
            style={{ width: 'auto', minWidth: '220px' }}
            value={selectedSessionId}
            onChange={(e) => setSelectedSessionId(e.target.value)}
          >
            {sessions.map((s) => (
              <option key={s.id} value={s.id}>{s.session_code}: {s.name}</option>
            ))}
          </select>

          <button
            onClick={handleBulkGenerate}
            disabled={loading}
            className="btn btn-primary"
          >
            <Sparkles size={16} color="#D4A72C" /> {loading ? 'Compiling PDFs...' : 'Bulk Issue Hall Tickets'}
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="card" style={{ padding: '1rem', marginBottom: '1.5rem', display: 'flex', gap: '1rem' }}>
        <div style={{ flex: 1, position: 'relative' }}>
          <Search size={16} color="var(--color-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            className="form-input"
            style={{ paddingLeft: '2.25rem' }}
            placeholder="Search student roll, ticket number, candidate name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* Hall Tickets Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Ticket Number</th>
              <th>Roll Number</th>
              <th>Student Name</th>
              <th>Department</th>
              <th>Security Hash</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {tickets.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-muted)' }}>
                  {loading ? 'Compiling hall tickets...' : 'No hall tickets generated yet for this session. Click "Bulk Issue Hall Tickets" above.'}
                </td>
              </tr>
            ) : (
              tickets.map((t) => (
                <tr key={t.id}>
                  <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{t.ticket_number}</td>
                  <td style={{ fontWeight: 700 }}>{t.student_roll}</td>
                  <td>{t.student_name}</td>
                  <td>{t.department_name}</td>
                  <td>
                    <code style={{ fontSize: '0.6875rem', backgroundColor: '#F8FAF7', padding: '0.125rem 0.375rem', borderRadius: '0.25rem' }}>
                      {t.verification_hash ? String(t.verification_hash).substring(0, 16) : 'VERIFIED'}...
                    </code>
                  </td>
                  <td>
                    <span className={t.is_blocked ? 'badge badge-danger' : 'badge badge-success'}>
                      {t.is_blocked ? 'Blocked' : 'Active / Issued'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.375rem' }}>
                      <a
                        href={api.getHallTicketPdfUrl(t.id)}
                        target="_blank"
                        rel="noreferrer"
                        className="btn btn-secondary btn-sm"
                        title="Download Local ReportLab PDF"
                      >
                        <Download size={14} /> PDF
                      </a>
                      <button
                        onClick={() => handleToggleBlock(t)}
                        className={`btn btn-sm ${t.is_blocked ? 'btn-secondary' : 'btn-outline'}`}
                        style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
                        title={t.is_blocked ? 'Unblock Admit Card' : 'Block Admit Card'}
                      >
                        <Ban size={14} /> {t.is_blocked ? 'Unblock' : 'Block'}
                      </button>
                    </div>
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
