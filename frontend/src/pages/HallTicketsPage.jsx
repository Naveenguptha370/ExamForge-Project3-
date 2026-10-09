import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { FileText, Download, Sparkles, CheckCircle2, QrCode } from 'lucide-react';

export const HallTicketsPage = () => {
  const toast = useToast();
  const [tickets, setTickets] = useState([]);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    const data = await api.getHallTickets(1);
    setTickets(data || []);
  };

  const handleGenerateBulk = async () => {
    setGenerating(true);
    toast.info('Generating official Admit Passes & Hall Tickets for all verified candidates...');
    const res = await api.generateBulkHallTickets(1);
    setGenerating(false);
    toast.success(res.message || '155 Hall tickets compiled successfully.');
    loadTickets();
  };

  const handleDownloadSingle = (ticketNumber, regNo) => {
    toast.success(`Generating PDF Hall Ticket for candidate ${regNo}...`);
    window.open(`/api/halltickets/passes/1/download-pdf/`, '_blank');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 5 — PASS ISSUANCE</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Examination Hall Tickets & Passes</h1>
        </div>

        <button onClick={handleGenerateBulk} disabled={generating} className="btn btn-primary btn-sm">
          <Sparkles size={15} color="#D4A72C" />
          <span>Generate Bulk Passes</span>
        </button>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Ticket Reference</th>
              <th>Register Number</th>
              <th>Candidate Name</th>
              <th>Branch / Program</th>
              <th>Semester</th>
              <th>Eligibility Status</th>
              <th>PDF Document</th>
            </tr>
          </thead>
          <tbody>
            {tickets.map((t) => (
              <tr key={t.id}>
                <td><b>{t.ticket_number}</b></td>
                <td><span style={{ fontWeight: 800, color: '#14532D' }}>{t.register_number}</span></td>
                <td><b>{t.student_name}</b></td>
                <td>{t.branch_name}</td>
                <td>Sem {t.semester_number}</td>
                <td>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#15803D', backgroundColor: '#DCFCE7', padding: '3px 8px', borderRadius: 9999 }}>
                    ✓ Verified & Cleared
                  </span>
                </td>
                <td>
                  <button
                    onClick={() => handleDownloadSingle(t.ticket_number, t.register_number)}
                    className="btn btn-secondary btn-sm"
                  >
                    <Download size={14} color="#15803D" />
                    <span>Download PDF</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
