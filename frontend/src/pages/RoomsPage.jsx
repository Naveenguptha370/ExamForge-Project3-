import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Layers, Grid, Shield } from 'lucide-react';

export const RoomsPage = () => {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    loadRooms();
  }, []);

  const loadRooms = async () => {
    const data = await api.getRooms();
    setRooms(data || []);
  };

  const totalCap = rooms.reduce((acc, r) => acc + (r.usable_exam_capacity || 0), 0);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 4 — INFRASTRUCTURE</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Examination Halls & Campus Rooms</h1>
        </div>
        <div style={{ padding: '8px 16px', backgroundColor: '#DDEBDD', borderRadius: 10, color: '#14532D', fontWeight: 700, fontSize: '0.85rem' }}>
          Total Usable Exam Capacity: {totalCap} Seats
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20 }}>
        {rooms.map((r) => (
          <div key={r.id} className="card card-hover" style={{ padding: 22, display: 'flex', flexDirection: 'column', gap: 10 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#14532D', fontFamily: 'var(--font-display)' }}>
                {r.block_code}-{r.room_number}
              </span>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, backgroundColor: '#FAF9F6', padding: '3px 8px', borderRadius: 6, border: '1px solid #E7E5E4' }}>
                {r.room_type_display}
              </span>
            </div>
            <div style={{ fontSize: '0.95rem', color: '#242923', fontWeight: 700 }}>
              Capacity: <span style={{ color: '#15803D' }}>{r.usable_exam_capacity} usable exam seats</span>
            </div>
            <div style={{ fontSize: '0.8rem', color: '#6B7280' }}>
              Grid Dimensions: {r.rows_count} rows × {r.columns_count} columns
            </div>
            <div style={{ display: 'flex', gap: 6, marginTop: 4 }}>
              <span style={{ fontSize: '0.72rem', backgroundColor: '#DCFCE7', color: '#15803D', padding: '2px 6px', borderRadius: 4, fontWeight: 700 }}>✓ CCTV Monitored</span>
              <span style={{ fontSize: '0.72rem', backgroundColor: '#FAF9F6', color: '#575E54', padding: '2px 6px', borderRadius: 4, fontWeight: 600 }}>Accessible</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
