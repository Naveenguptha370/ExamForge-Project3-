import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Modal from '../components/Modal';
import { DoorOpen, Plus, Search, Video, CheckCircle2, AlertTriangle, Building as BuildingIcon } from 'lucide-react';

export default function RoomsPage() {
  const [rooms, setRooms] = useState([]);
  const [buildings, setBuildings] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [formData, setFormData] = useState({
    room_number: '', building: '', floor: 1, room_type: 'LECTURE_HALL',
    total_capacity: 60, usable_capacity: 30, rows: 5, columns: 6, has_cctv: true
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const [rData, bData, sData] = await Promise.all([
        api.getRooms(),
        api.getBuildings(),
        api.getRoomSummary()
      ]);
      setRooms(rData.results || rData);
      setBuildings(bData.results || bData);
      setSummary(sData);
      if (bData.length > 0 && !formData.building) {
        setFormData(prev => ({ ...prev, building: bData[0].id }));
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.createRoom(formData);
      setIsModalOpen(false);
      loadData();
    } catch (e) {
      alert('Error: ' + e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Halls & Infrastructure Management
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 4 Module: Academic blocks, examination halls, usable capacity with exam spacing, and CCTV coverage
          </p>
        </div>

        <button onClick={() => setIsModalOpen(true)} className="btn btn-primary">
          <Plus size={16} /> Register Exam Room
        </button>
      </div>

      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Registered Halls</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>{summary?.total_rooms ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Available for Exams</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-emerald)' }}>{summary?.available_rooms ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Total Usable Exam Seats</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-amber)' }}>{summary?.total_usable_capacity ?? 0} Seats</div>
        </div>
      </div>

      {/* Rooms Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Room Number</th>
              <th>Building Complex</th>
              <th>Floor</th>
              <th>Hall Type</th>
              <th>Total Capacity</th>
              <th>Usable Exam Capacity</th>
              <th>Grid Dimensions</th>
              <th>CCTV Active</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rooms.map((r) => (
              <tr key={r.id}>
                <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{r.room_number}</td>
                <td>{r.building_name} ({r.building_code})</td>
                <td>Floor {r.floor}</td>
                <td><span className="badge badge-neutral">{r.room_type_display}</span></td>
                <td>{r.total_capacity} Desks</td>
                <td><span className="badge badge-gold">{r.usable_capacity} Exam Seats</span></td>
                <td>{r.rows}R × {r.columns}C</td>
                <td>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem', color: r.has_cctv ? 'var(--color-emerald)' : 'var(--color-muted)', fontWeight: 600 }}>
                    <Video size={14} /> {r.has_cctv ? 'Monitored' : 'No CCTV'}
                  </span>
                </td>
                <td>
                  <span className={r.status === 'AVAILABLE' ? 'badge badge-success' : 'badge badge-danger'}>
                    {r.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Register Examination Room">
        <form onSubmit={handleCreate}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div className="form-group">
              <label className="form-label">Room Number</label>
              <input required className="form-input" value={formData.room_number} onChange={(e) => setFormData({ ...formData, room_number: e.target.value })} placeholder="e.g. LH-201" />
            </div>
            <div className="form-group">
              <label className="form-label">Building</label>
              <select className="form-select" value={formData.building} onChange={(e) => setFormData({ ...formData, building: e.target.value })}>
                {buildings.map((b) => (
                  <option key={b.id} value={b.id}>{b.code} - {b.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Total Desks</label>
              <input required type="number" className="form-input" value={formData.total_capacity} onChange={(e) => setFormData({ ...formData, total_capacity: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Usable Exam Capacity</label>
              <input required type="number" className="form-input" value={formData.usable_capacity} onChange={(e) => setFormData({ ...formData, usable_capacity: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Rows</label>
              <input required type="number" className="form-input" value={formData.rows} onChange={(e) => setFormData({ ...formData, rows: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Columns</label>
              <input required type="number" className="form-input" value={formData.columns} onChange={(e) => setFormData({ ...formData, columns: e.target.value })} />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.25rem' }}>
            <button type="button" onClick={() => setIsModalOpen(false)} className="btn btn-outline">Cancel</button>
            <button type="submit" className="btn btn-primary">Save Hall</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
