import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Grid, Sparkles, AlertTriangle, CheckCircle2, DoorOpen, Users } from 'lucide-react';

export default function SeatingPlanPage() {
  const [examSubjects, setExamSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState('');
  const [seatingPlans, setSeatingPlans] = useState([]);
  const [activePlan, setActivePlan] = useState(null);
  const [spacingRule, setSpacingRule] = useState('ALTERNATE_COLS');
  const [generationResult, setGenerationResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadExamSubjects = async () => {
    try {
      const data = await api.getExamSubjects();
      const list = data.results || data;
      setExamSubjects(list);
      if (list.length > 0 && !selectedSubjectId) {
        setSelectedSubjectId(list[0].id);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const loadPlans = async () => {
    if (!selectedSubjectId) return;
    try {
      const data = await api.getSeatingPlans(`?exam_subject=${selectedSubjectId}`);
      const list = data.results || data;
      setSeatingPlans(list);
      setActivePlan(list.length > 0 ? list[0] : null);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadExamSubjects();
  }, []);

  useEffect(() => {
    if (selectedSubjectId) {
      loadPlans();
    }
  }, [selectedSubjectId]);

  const handleGenerate = async () => {
    if (!selectedSubjectId) return;
    setLoading(true);
    setGenerationResult(null);
    try {
      const res = await api.generateSeatingPlan(selectedSubjectId, [], spacingRule);
      setGenerationResult(res);
      await loadPlans();
    } catch (e) {
      alert('Seating generation failed: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  // Build grid map for visual layout (Row x Col)
  const renderVisualGrid = () => {
    if (!activePlan || !activePlan.allocations) return null;

    const allocationsMap = {};
    activePlan.allocations.forEach((alloc) => {
      allocationsMap[`${alloc.row_num}-${alloc.col_num}`] = alloc;
    });

    const rows = 5;
    const cols = 6;
    const gridRows = [];

    for (let r = 1; r <= rows; r++) {
      const rowLetter = String.fromCharCode(64 + r);
      const cells = [];
      for (let c = 1; c <= cols; c++) {
        const key = `${r}-${c}`;
        const alloc = allocationsMap[key];
        const isAlternateEmpty = spacingRule === 'ALTERNATE_COLS' && c % 2 === 0;

        cells.push(
          <div
            key={key}
            style={{
              padding: '0.625rem 0.375rem',
              borderRadius: '0.5rem',
              textAlign: 'center',
              backgroundColor: alloc ? 'var(--color-sage)' : (isAlternateEmpty ? '#f3f4f6' : '#FFFFFF'),
              border: alloc ? '1.5px solid var(--color-emerald)' : '1px dashed var(--color-border)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              minHeight: '64px',
              transition: 'all 0.2s ease'
            }}
            title={alloc ? `Seat ${alloc.seat_label}: ${alloc.student_roll} (${alloc.student_name})` : `Seat ${rowLetter}${c}: Empty`}
          >
            <div style={{ fontSize: '0.6875rem', fontWeight: 800, color: alloc ? 'var(--color-forest)' : 'var(--color-muted)' }}>
              {rowLetter}{c}
            </div>
            {alloc ? (
              <div style={{ fontSize: '0.6875rem', fontWeight: 700, color: 'var(--color-forest)', marginTop: '0.125rem', whiteSpace: 'nowrap' }}>
                {alloc.student_roll}
              </div>
            ) : (
              <div style={{ fontSize: '0.625rem', color: '#9ca3af', marginTop: '0.125rem' }}>
                {isAlternateEmpty ? 'Gap Seat' : 'Vacant'}
              </div>
            )}
          </div>
        );
      }
      gridRows.push(
        <div key={r} style={{ display: 'grid', gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: '0.625rem', marginBottom: '0.625rem' }}>
          {cells}
        </div>
      );
    }

    return (
      <div style={{
        padding: '1.5rem',
        backgroundColor: '#FFFFFF',
        borderRadius: '0.75rem',
        border: '1px solid var(--color-border)',
        boxShadow: 'var(--shadow-sm)'
      }}>
        {/* Hall Blackboard Front Indicator */}
        <div style={{
          backgroundColor: 'var(--color-forest)',
          color: '#FFFFFF',
          textAlign: 'center',
          padding: '0.375rem',
          borderRadius: '0.375rem',
          fontSize: '0.75rem',
          fontWeight: 700,
          letterSpacing: '0.05em',
          marginBottom: '1.5rem'
        }}>
          FRONT OF EXAMINATION HALL • INVIGILATOR DESK
        </div>

        {gridRows}
      </div>
    );
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Seating Arrangement & Visual Hall Grid
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 4 Module: Automated student-to-seat allocation, alternate spacing rules, and capacity warnings
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <select
            className="form-select"
            style={{ width: 'auto', minWidth: '220px' }}
            value={selectedSubjectId}
            onChange={(e) => setSelectedSubjectId(e.target.value)}
          >
            {examSubjects.map((es) => (
              <option key={es.id} value={es.id}>{es.subject_code}: {es.subject_name}</option>
            ))}
          </select>

          <select
            className="form-select"
            style={{ width: 'auto', minWidth: '180px' }}
            value={spacingRule}
            onChange={(e) => setSpacingRule(e.target.value)}
          >
            <option value="ALTERNATE_COLS">Alternate Columns (Cols 1, 3, 5)</option>
            <option value="CHECKERBOARD">Checkerboard Spacing</option>
          </select>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="btn btn-primary"
          >
            <Sparkles size={16} color="#D4A72C" /> {loading ? 'Allocating Seats...' : 'Generate Seating Plan'}
          </button>
        </div>
      </div>

      {/* Capacity Outcome Alert */}
      {generationResult && (
        <div style={{
          padding: '1rem 1.25rem',
          backgroundColor: generationResult.unallocated_count === 0 ? 'var(--color-sage-light)' : '#fee2e2',
          border: `1px solid ${generationResult.unallocated_count === 0 ? 'var(--color-emerald)' : 'var(--color-error)'}`,
          borderRadius: '0.75rem',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem'
        }}>
          {generationResult.unallocated_count === 0 ? (
            <CheckCircle2 size={24} color="var(--color-emerald)" />
          ) : (
            <AlertTriangle size={24} color="var(--color-error)" />
          )}
          <div>
            <div style={{ fontWeight: 800, color: 'var(--color-forest)', fontSize: '0.9375rem' }}>
              {generationResult.unallocated_count === 0 ? 'Optimal Seating Plan Created' : 'Capacity Shortage Alert'}
            </div>
            <div style={{ fontSize: '0.8125rem', color: 'var(--color-charcoal)', marginTop: '0.125rem' }}>
              {generationResult.message}
            </div>
          </div>
        </div>
      )}

      {/* Main Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '1.5rem', alignItems: 'start' }}>
        {/* Plans List / Hall Switcher */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--color-forest)' }}>Allocated Rooms</h3>
            <span className="badge badge-neutral">{seatingPlans.length} Halls</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {seatingPlans.length === 0 ? (
              <div style={{ fontSize: '0.8125rem', color: 'var(--color-muted)', textAlign: 'center', padding: '1rem' }}>
                No seating plans generated yet. Click "Generate Seating Plan" above.
              </div>
            ) : (
              seatingPlans.map((p) => (
                <div
                  key={p.id}
                  onClick={() => setActivePlan(p)}
                  style={{
                    padding: '0.875rem',
                    borderRadius: '0.5rem',
                    cursor: 'pointer',
                    backgroundColor: activePlan?.id === p.id ? 'var(--color-sage-light)' : '#FFFFFF',
                    border: `1px solid ${activePlan?.id === p.id ? 'var(--color-forest)' : 'var(--color-border)'}`
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontWeight: 800, color: 'var(--color-forest)' }}>Room {p.room_number}</span>
                    <span className="badge badge-success">{p.total_allocated} Students</span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', marginTop: '0.25rem' }}>
                    {p.building_name} • Spacing: {p.spacing_rule}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Visual Seating Grid Chart */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)' }}>
              Visual Layout: {activePlan ? `Room ${activePlan.room_number}` : 'Select a Hall'}
            </h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>
              Green: Assigned Student • Gray: Spacing Gap
            </span>
          </div>

          {renderVisualGrid()}
        </div>
      </div>
    </div>
  );
}
