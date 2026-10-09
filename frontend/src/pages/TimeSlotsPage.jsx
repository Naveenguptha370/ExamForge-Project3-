import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import { Clock, Plus, Check } from 'lucide-react';

export const TimeSlotsPage = () => {
  const toast = useToast();
  const [slots, setSlots] = useState([]);

  useEffect(() => {
    loadSlots();
  }, []);

  const loadSlots = async () => {
    const data = await api.getTimeSlots();
    setSlots(data || []);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#15803D', marginBottom: 4 }}>MEMBER 3 — TIME CONFIG</div>
          <h1 style={{ fontSize: '1.85rem', color: '#14532D' }}>Examination Time Slots & Shifts</h1>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20 }}>
        {slots.map((s) => (
          <div key={s.id} className="card" style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 12, borderTop: '4px solid #15803D' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#14532D', fontFamily: 'var(--font-display)' }}>
                Slot {s.code}
              </span>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, backgroundColor: '#DDEBDD', color: '#14532D', padding: '3px 8px', borderRadius: 6 }}>
                {s.shift}
              </span>
            </div>
            <h3 style={{ fontSize: '1.05rem', color: '#242923' }}>{s.name}</h3>
            <div style={{ fontSize: '0.9rem', color: '#575E54' }}>
              <b>Timings:</b> {s.start_time} - {s.end_time} ({s.duration_minutes} minutes)
            </div>
            <div style={{ fontSize: '0.78rem', color: '#15803D', fontWeight: 600 }}>
              ✓ Active constraint slot for CSP scheduling solver
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
