import React, { useState } from 'react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { UserPlus, Sparkles, CheckCircle2, Shield } from 'lucide-react';

export const InvigilationPage = () => {
  const toast = useToast();
  const [duties, setDuties] = useState([
    { id: 1, faculty_name: 'Dr. Anand Krishnan', employee_id: 'FAC-CS-01', department_code: 'CSE', room_number: 'NB-101', date: '2025-11-10', shift: 'Morning', status: 'Assigned' },
    { id: 2, faculty_name: 'Mrs. Deepa Menon', employee_id: 'FAC-CS-02', department_code: 'CSE', room_number: 'NB-102', date: '2025-11-10', shift: 'Morning', status: 'Assigned' },
    { id: 3, faculty_name: 'Dr. Suresh Reddy', employee_id: 'FAC-EC-01', department_code: 'ECE', room_number: 'NB-201', date: '2025-11-10', shift: 'Afternoon', status: 'Assigned' },
    { id: 4, faculty_name: 'Dr. Rangarajan Iyer', employee_id: 'FAC-ME-01', department_code: 'MECH', room_number: 'SB-101', date: '2025-11-11', shift: 'Morning', status: 'Assigned' },
  ]);

  const handleAutoAssign = async () => {
    toast.info('Balancing and assigning faculty invigilation duties...');
    const res = await api.autoAssignInvigilators(1);
    toast.success(res.message || 'Invigilator duties balanced and assigned successfully.');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 4 — FACULTY DUTIES</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Invigilator Allocation & Duty Roster</h1>
        </div>

        <button onClick={handleAutoAssign} className="btn btn-primary btn-sm">
          <Sparkles size={15} color="#D4A72C" />
          <span>Fair Auto-Assign Duties</span>
        </button>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Duty Date & Shift</th>
              <th>Allocated Hall</th>
              <th>Assigned Faculty</th>
              <th>Employee ID</th>
              <th>Department</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {duties.map((d) => (
              <tr key={d.id}>
                <td><b>{d.date}</b> ({d.shift})</td>
                <td><span style={{ fontWeight: 800, color: '#14532D' }}>Hall {d.room_number}</span></td>
                <td><b>{d.faculty_name}</b></td>
                <td>{d.employee_id}</td>
                <td>{d.department_code}</td>
                <td><span className="badge badge-validated">{d.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
