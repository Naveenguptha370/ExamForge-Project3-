import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Modal from '../components/Modal';
import { BookOpen, Plus, Layers, Award, CheckCircle2 } from 'lucide-react';

export default function AcademicsPage() {
  const [departments, setDepartments] = useState([]);
  const [courses, setCourses] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [semesters, setSemesters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('subjects');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [subjectForm, setSubjectForm] = useState({
    code: '', name: '', department: '', semester: '', credits: 4.0, min_attendance_pct: 75
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const [depts, crs, subs, sems] = await Promise.all([
        api.getDepartments(),
        api.getCourses(),
        api.getSubjects(),
        api.getSemesters()
      ]);
      setDepartments(depts.results || depts);
      setCourses(crs.results || crs);
      setSubjects(subs.results || subs);
      setSemesters(sems.results || sems);
      if (depts.length > 0 && !subjectForm.department) {
        setSubjectForm(prev => ({ ...prev, department: depts[0].id }));
      }
      if (sems.length > 0 && !subjectForm.semester) {
        setSubjectForm(prev => ({ ...prev, semester: sems[0].id }));
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

  const handleCreateSubject = async (e) => {
    e.preventDefault();
    try {
      await api.createSubject(subjectForm);
      setIsModalOpen(false);
      setSubjectForm({ code: '', name: '', department: departments[0]?.id || '', semester: semesters[0]?.id || '', credits: 4.0, min_attendance_pct: 75 });
      loadData();
    } catch (e) {
      alert('Error creating subject: ' + e.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Curriculum & Academic Structure
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 2 Module: Departments, Degree Courses, Semester Levels, and Subject Catalogs
          </p>
        </div>

        <button onClick={() => setIsModalOpen(true)} className="btn btn-primary">
          <Plus size={16} /> Add Subject Paper
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--color-border)', marginBottom: '1.5rem' }}>
        {['subjects', 'departments', 'courses'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: '0.625rem 1.25rem',
              fontWeight: 700,
              fontSize: '0.875rem',
              color: activeTab === tab ? 'var(--color-forest)' : 'var(--color-muted)',
              borderBottom: activeTab === tab ? '2px solid var(--color-forest)' : '2px solid transparent',
              background: 'none',
              borderTop: 'none',
              borderLeft: 'none',
              borderRight: 'none',
              cursor: 'pointer',
              textTransform: 'capitalize'
            }}
          >
            {tab} Catalog
          </button>
        ))}
      </div>

      {activeTab === 'subjects' && (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Subject Code</th>
                <th>Subject Title</th>
                <th>Department</th>
                <th>Semester</th>
                <th>Credits</th>
                <th>Min. Attendance Rule</th>
              </tr>
            </thead>
            <tbody>
              {subjects.map((s) => (
                <tr key={s.id}>
                  <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{s.code}</td>
                  <td style={{ fontWeight: 600 }}>{s.name}</td>
                  <td>{s.department_name}</td>
                  <td><span className="badge badge-neutral">{s.semester_label}</span></td>
                  <td><span className="badge badge-gold">{s.credits} Credits</span></td>
                  <td>{s.min_attendance_pct}% Mandatory</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'departments' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
          {departments.map((d) => (
            <div key={d.id} className="card">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span className="badge badge-success">{d.code}</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>{d.courses_count || 0} Courses</span>
              </div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)' }}>{d.name}</h3>
              <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)', marginTop: '0.375rem', lineHeight: 1.4 }}>{d.description}</p>
              <div style={{ marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid var(--color-border-light)', fontSize: '0.75rem', color: 'var(--color-charcoal)' }}>
                <b>Head of Dept:</b> {d.head_of_department || 'Dr. Department Chair'}
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'courses' && (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Course Code</th>
                <th>Degree Program</th>
                <th>Department</th>
                <th>Duration</th>
                <th>Degree Type</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((c) => (
                <tr key={c.id}>
                  <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{c.code}</td>
                  <td style={{ fontWeight: 600 }}>{c.name}</td>
                  <td>{c.department_name}</td>
                  <td>{c.duration_years} Years</td>
                  <td><span className="badge badge-neutral">{c.degree_type}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Add Subject Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Add Examination Subject Paper">
        <form onSubmit={handleCreateSubject}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div className="form-group">
              <label className="form-label">Subject Code</label>
              <input required className="form-input" value={subjectForm.code} onChange={(e) => setSubjectForm({ ...subjectForm, code: e.target.value })} placeholder="e.g. CS501" />
            </div>
            <div className="form-group">
              <label className="form-label">Credits</label>
              <input required type="number" step="0.5" className="form-input" value={subjectForm.credits} onChange={(e) => setSubjectForm({ ...subjectForm, credits: e.target.value })} />
            </div>
            <div className="form-group" style={{ gridColumn: 'span 2' }}>
              <label className="form-label">Subject Title</label>
              <input required className="form-input" value={subjectForm.name} onChange={(e) => setSubjectForm({ ...subjectForm, name: e.target.value })} placeholder="e.g. Theory of Computation" />
            </div>
            <div className="form-group">
              <label className="form-label">Department</label>
              <select className="form-select" value={subjectForm.department} onChange={(e) => setSubjectForm({ ...subjectForm, department: e.target.value })}>
                {departments.map((d) => (
                  <option key={d.id} value={d.id}>{d.code} - {d.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Semester</label>
              <select className="form-select" value={subjectForm.semester} onChange={(e) => setSubjectForm({ ...subjectForm, semester: e.target.value })}>
                {semesters.map((s) => (
                  <option key={s.id} value={s.id}>Sem {s.number} ({s.academic_year} {s.term})</option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.25rem' }}>
            <button type="button" onClick={() => setIsModalOpen(false)} className="btn btn-outline">Cancel</button>
            <button type="submit" className="btn btn-primary">Save Subject</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
