import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { StatusBadge } from '../components/StatusBadge';
import { Modal } from '../components/Modal';
import { Users, Upload, FileSpreadsheet, CheckCircle2, AlertCircle } from 'lucide-react';

export const StudentsPage = () => {
  const toast = useToast();
  const [students, setStudents] = useState([]);
  const [csvModalOpen, setCsvModalOpen] = useState(false);
  const [csvContent, setCsvContent] = useState('');

  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    const data = await api.getStudents();
    setStudents(data || []);
  };

  const handleImportCSV = async () => {
    if (!csvContent.trim()) {
      toast.error('Please enter CSV content.');
      return;
    }
    const res = await api.importStudentsCSV(csvContent);
    if (res.success) {
      toast.success(res.message);
      setCsvModalOpen(false);
      setCsvContent('');
      loadStudents();
    }
  };

  const sampleCSV = `register_number,first_name,last_name,email,branch_code,semester
23CSE101,Aarav,Sharma,aarav.s@student.examforge.edu,CSE,5
23CSE102,Diya,Patel,diya.p@student.examforge.edu,CSE,5
23ECE101,Rohan,Verma,rohan.v@student.examforge.edu,ECE,5`;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 2 — STUDENT MANAGEMENT</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Student Directory & Exam Enrollments</h1>
        </div>

        <button onClick={() => setCsvModalOpen(true)} className="btn btn-primary btn-sm">
          <Upload size={15} />
          <span>Bulk CSV Import</span>
        </button>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Register Number</th>
              <th>Candidate Name</th>
              <th>Email Address</th>
              <th>Branch / Program</th>
              <th>Current Sem</th>
              <th>Examination Eligibility</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.id}>
                <td><b>{s.register_number}</b></td>
                <td><b>{s.full_name}</b></td>
                <td>{s.email}</td>
                <td>{s.branch_name}</td>
                <td>Sem {s.current_semester_number}</td>
                <td>
                  <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#15803D', backgroundColor: '#DCFCE7', padding: '3px 8px', borderRadius: 9999 }}>
                    ✓ Eligible (Cleared)
                  </span>
                </td>
                <td><StatusBadge status={s.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* CSV Import Modal */}
      <Modal isOpen={csvModalOpen} onClose={() => setCsvModalOpen(false)} title="Bulk Student CSV Import" maxWidth={600}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <p style={{ fontSize: '0.85rem', color: '#575E54' }}>
            Paste or upload student CSV records. The system will detect duplicate register numbers and validate branch codes.
          </p>

          <div className="form-group">
            <label className="form-label">CSV Content (Columns: register_number, first_name, last_name, email, branch_code, semester)</label>
            <textarea
              rows={6}
              value={csvContent}
              onChange={(e) => setCsvContent(e.target.value)}
              placeholder={sampleCSV}
              className="form-textarea"
              style={{ fontFamily: 'monospace', fontSize: '0.82rem' }}
            />
          </div>

          <button
            type="button"
            onClick={() => setCsvContent(sampleCSV)}
            className="btn btn-secondary btn-sm"
            style={{ alignSelf: 'flex-start' }}
          >
            Insert Sample CSV Template
          </button>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginTop: 10 }}>
            <button onClick={() => setCsvModalOpen(false)} className="btn btn-secondary btn-sm">
              Cancel
            </button>
            <button onClick={handleImportCSV} className="btn btn-primary btn-sm">
              Process & Validate Import
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
};
