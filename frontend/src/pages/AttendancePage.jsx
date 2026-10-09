import React, { useState } from 'react';
import { useToast } from '../context/ToastContext';
import { CheckSquare, Save, Check } from 'lucide-react';

export const AttendancePage = () => {
  const toast = useToast();
  const [records, setRecords] = useState([
    { id: 1, regNo: '23CSE001', name: 'Alice Smith', branch: 'CSE', subject: 'CS501', hall: 'NB-101', status: 'PRESENT', booklet: 'BK-5011' },
    { id: 2, regNo: '23CSE002', name: 'Bob Jones', branch: 'CSE', subject: 'CS501', hall: 'NB-101', status: 'PRESENT', booklet: 'BK-5012' },
    { id: 3, regNo: '23CSE003', name: 'Charlie Brown', branch: 'CSE', subject: 'CS501', hall: 'NB-101', status: 'ABSENT', booklet: '' },
    { id: 4, regNo: '23CSE004', name: 'David Clark', branch: 'CSE', subject: 'CS501', hall: 'NB-101', status: 'PRESENT', booklet: 'BK-5014' },
    { id: 5, regNo: '23CSE005', name: 'Elena Gilbert', branch: 'CSE', subject: 'CS501', hall: 'NB-101', status: 'PRESENT', booklet: 'BK-5015' },
  ]);

  const handleStatusChange = (id, newStatus) => {
    setRecords((prev) =>
      prev.map((r) => (r.id === id ? { ...r, status: newStatus } : r))
    );
  };

  const handleBookletChange = (id, val) => {
    setRecords((prev) =>
      prev.map((r) => (r.id === id ? { ...r, booklet: val } : r))
    );
  };

  const handleSave = () => {
    toast.success('Attendance records and answer booklet numbers saved to database.');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 5 — ATTENDANCE</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Examination Attendance & Answer Booklets</h1>
        </div>

        <button onClick={handleSave} className="btn btn-primary btn-sm">
          <Save size={15} />
          <span>Save Attendance Sheet</span>
        </button>
      </div>

      <div className="card" style={{ padding: 18, display: 'flex', alignItems: 'center', gap: 20, backgroundColor: '#FAF9F6' }}>
        <span><b>Selected Hall:</b> NB-101</span>
        <span><b>Exam:</b> CS501 - Operating Systems</span>
        <span><b>Date & Shift:</b> 10-Nov-2025 (Morning)</span>
        <span><b>Total Present:</b> <font color="#15803D">4/5 (80%)</font></span>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Register No</th>
              <th>Candidate Name</th>
              <th>Branch</th>
              <th>Allocated Hall</th>
              <th>Attendance Status</th>
              <th>Answer Booklet Serial No</th>
            </tr>
          </thead>
          <tbody>
            {records.map((r) => (
              <tr key={r.id}>
                <td><b>{r.regNo}</b></td>
                <td><b>{r.name}</b></td>
                <td>{r.branch}</td>
                <td>Hall {r.hall}</td>
                <td>
                  <select
                    value={r.status}
                    onChange={(e) => handleStatusChange(r.id, e.target.value)}
                    style={{
                      padding: '4px 8px',
                      borderRadius: 6,
                      fontSize: '0.82rem',
                      fontWeight: 700,
                      backgroundColor: r.status === 'PRESENT' ? '#DCFCE7' : '#FEE2E2',
                      color: r.status === 'PRESENT' ? '#14532D' : '#991B1B',
                      border: '1px solid #D1D5DB'
                    }}
                  >
                    <option value="PRESENT">PRESENT</option>
                    <option value="ABSENT">ABSENT</option>
                    <option value="MALPRACTICE">MALPRACTICE</option>
                  </select>
                </td>
                <td>
                  <input
                    type="text"
                    value={r.booklet}
                    placeholder="Enter Serial No..."
                    onChange={(e) => handleBookletChange(r.id, e.target.value)}
                    style={{ padding: '4px 8px', fontSize: '0.82rem', borderRadius: 6, border: '1px solid #D1D5DB', width: 140 }}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
