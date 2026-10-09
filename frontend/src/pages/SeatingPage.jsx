import React, { useState } from 'react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { Grid, Sparkles, CheckCircle2, User } from 'lucide-react';

export const SeatingPage = () => {
  const toast = useToast();
  const [selectedHall, setSelectedHall] = useState('NB-101');
  const [allocating, setAllocating] = useState(false);

  const handleAutoAllocate = async () => {
    setAllocating(true);
    toast.info('Auto-generating seating layout across examination halls with alternate seat spacing...');
    const res = await api.autoAllocateSeating(1, '2025-11-10', 1);
    setAllocating(false);
    toast.success(res.message || 'Seating plan generated successfully!');
  };

  // 6x5 Desk Matrix for NB-101
  const rows = 6;
  const cols = 5;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 4 — SEATING MATRIX</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Examination Seating Arrangement</h1>
        </div>

        <button onClick={handleAutoAllocate} disabled={allocating} className="btn btn-primary btn-sm">
          <Sparkles size={15} color="#D4A72C" />
          <span>Auto-Allocate All Halls</span>
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr', gap: 24 }}>
        {/* Hall Selector Sidebar */}
        <div className="card" style={{ padding: 18, display: 'flex', flexDirection: 'column', gap: 10 }}>
          <h3 style={{ fontSize: '1rem', color: '#14532D' }}>Examination Halls</h3>
          {['NB-101', 'NB-102', 'NB-201', 'SB-101', 'LH-AUDI-1'].map((hall) => (
            <button
              key={hall}
              onClick={() => setSelectedHall(hall)}
              style={{
                padding: '10px 14px',
                borderRadius: 8,
                border: selectedHall === hall ? '2px solid #15803D' : '1px solid #E7E5E4',
                backgroundColor: selectedHall === hall ? '#F0FDF4' : '#FFFFFF',
                color: selectedHall === hall ? '#14532D' : '#242923',
                fontWeight: selectedHall === hall ? 700 : 500,
                cursor: 'pointer',
                textAlign: 'left',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <span>{hall}</span>
              <span style={{ fontSize: '0.75rem', color: '#15803D' }}>30 Seats</span>
            </button>
          ))}
        </div>

        {/* Visual Seating Grid */}
        <div className="card" style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 18 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#14532D' }}>Seating Layout: {selectedHall}</h3>
              <span style={{ fontSize: '0.8rem', color: '#6B7280' }}>
                Spacing Rule: <b>Alternate Desks</b> • Exam Date: <b>10-Nov-2025 (Shift 1)</b>
              </span>
            </div>
            <div style={{ display: 'flex', gap: 12, fontSize: '0.78rem', fontWeight: 600 }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ width: 12, height: 12, backgroundColor: '#DDEBDD', border: '1px solid #15803D', borderRadius: 3 }} />
                Occupied (CSE)
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ width: 12, height: 12, backgroundColor: '#FAF9F6', border: '1px dashed #D1D5DB', borderRadius: 3 }} />
                Empty Spacing
              </span>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: 12, backgroundColor: '#FAF9F6', padding: 20, borderRadius: 14, border: '1px solid #E7E5E4' }}>
            {Array.from({ length: rows }).map((_, r) =>
              Array.from({ length: cols }).map((_, c) => {
                const isOccupied = (r + c) % 2 === 0;
                const seatNum = r * cols + c + 1;
                const regNo = `23CSE${String(seatNum).padStart(3, '0')}`;

                return (
                  <div
                    key={`${r}-${c}`}
                    style={{
                      padding: 12,
                      borderRadius: 10,
                      backgroundColor: isOccupied ? '#FFFFFF' : '#F4F3EE',
                      border: isOccupied ? '2px solid #15803D' : '1px dashed #D1D5DB',
                      boxShadow: isOccupied ? '0 2px 4px rgba(21,128,61,0.1)' : 'none',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      gap: 4
                    }}
                  >
                    <span style={{ fontSize: '0.7rem', fontWeight: 800, color: isOccupied ? '#15803D' : '#9CA3AF' }}>
                      R{r + 1}-C{c + 1}
                    </span>
                    {isOccupied ? (
                      <>
                        <User size={16} color="#14532D" />
                        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#242923' }}>{regNo}</span>
                        <span style={{ fontSize: '0.65rem', color: '#15803D', fontWeight: 700 }}>CS501</span>
                      </>
                    ) : (
                      <span style={{ fontSize: '0.7rem', color: '#9CA3AF', margin: '14px 0' }}>Empty</span>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
