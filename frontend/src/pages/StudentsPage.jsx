import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Modal from '../components/Modal';
import { GraduationCap, Upload, Download, Search, CheckCircle2, AlertTriangle, FileSpreadsheet } from 'lucide-react';

export default function StudentsPage() {
  const [students, setStudents] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [isEligibleFilter, setIsEligibleFilter] = useState('');

  // CSV Import State
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [csvFile, setCsvFile] = useState(null);
  const [previewResult, setPreviewResult] = useState(null);
  const [importStatus, setImportStatus] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      let q = `?search=${encodeURIComponent(search)}`;
      if (isEligibleFilter) q += `&is_eligible=${isEligibleFilter}`;
      const data = await api.getStudents(q);
      setStudents(data.results || data);
      const sum = await api.getStudentsSummary();
      setSummary(sum);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [search, isEligibleFilter]);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setCsvFile(file);
    setPreviewResult(null);
    setImportStatus('Analyzing CSV structure & validating duplicate rolls...');

    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await api.previewStudentCSV(formData);
      setPreviewResult(res);
      setImportStatus('');
    } catch (err) {
      setImportStatus('Validation Error: ' + err.message);
    }
  };

  const handleExecuteImport = async () => {
    if (!csvFile) return;
    setImportStatus('Committing validated student records to database...');
    const formData = new FormData();
    formData.append('file', csvFile);
    try {
      const res = await api.importStudentCSV(formData);
      alert(res.message);
      setIsUploadModalOpen(false);
      setCsvFile(null);
      setPreviewResult(null);
      setImportStatus('');
      loadData();
    } catch (err) {
      setImportStatus('Import Failed: ' + err.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ padding: '1.75rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>
            Student Registry & Bulk CSV Engine
          </h2>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)' }}>
            Member 2 Module: Enrollment records, roll numbers, CSV preview/import, and examination eligibility
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <a href={api.exportStudentCSVUrl()} target="_blank" rel="noreferrer" className="btn btn-outline">
            <Download size={16} /> Export CSV
          </a>
          <button onClick={() => setIsUploadModalOpen(true)} className="btn btn-primary">
            <Upload size={16} /> Bulk CSV Import
          </button>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Total Students</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-forest)' }}>{summary?.total_students ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Eligible for Examinations</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-emerald)' }}>{summary?.eligible_students ?? '...'}</div>
        </div>
        <div className="card" style={{ padding: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Attendance Shortage / Ineligible</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-error)' }}>{summary?.ineligible_students ?? 0}</div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="card" style={{ padding: '1rem', marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: '220px', position: 'relative' }}>
          <Search size={16} color="var(--color-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            className="form-input"
            style={{ paddingLeft: '2.25rem' }}
            placeholder="Search roll number, registration no, name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <select
          className="form-select"
          style={{ width: 'auto', minWidth: '180px' }}
          value={isEligibleFilter}
          onChange={(e) => setIsEligibleFilter(e.target.value)}
        >
          <option value="">All Eligibility Statuses</option>
          <option value="true">Eligible Only</option>
          <option value="false">Ineligible Only</option>
        </select>
      </div>

      {/* Students Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Roll Number</th>
              <th>Registration No</th>
              <th>Full Name</th>
              <th>Department</th>
              <th>Course / Branch</th>
              <th>Semester</th>
              <th>Exam Eligibility</th>
            </tr>
          </thead>
          <tbody>
            {students.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-muted)' }}>
                  {loading ? 'Loading student registry...' : 'No students found matching filters.'}
                </td>
              </tr>
            ) : (
              students.map((s) => (
                <tr key={s.id}>
                  <td style={{ fontWeight: 800, color: 'var(--color-forest)' }}>{s.roll_no}</td>
                  <td>{s.registration_no}</td>
                  <td style={{ fontWeight: 600 }}>{s.full_name}</td>
                  <td>{s.department_code}</td>
                  <td>{s.course_code} {s.branch_name ? `• ${s.branch_name}` : ''}</td>
                  <td>Sem {s.semester_number}</td>
                  <td>
                    <span className={s.is_eligible_for_exam ? 'badge badge-success' : 'badge badge-danger'}>
                      {s.is_eligible_for_exam ? 'Eligible' : 'Attendance Shortage'}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Bulk CSV Upload Modal */}
      <Modal isOpen={isUploadModalOpen} onClose={() => setIsUploadModalOpen(false)} title="Bulk Student CSV Upload Engine" maxWidth="700px">
        <div>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)', marginBottom: '1rem' }}>
            Required columns: <code>registration_no, roll_no, first_name, last_name, email, department_code, course_code, semester_number</code>. Optional: <code>branch_code, phone, admission_year, academic_year, term</code>. Provide both academic year and term when semester numbers are ambiguous. Imports are all-or-nothing: correct every invalid row before committing.
          </p>

          <div style={{
            border: '2px dashed var(--color-border)',
            borderRadius: '0.75rem',
            padding: '2rem',
            textAlign: 'center',
            backgroundColor: '#FBFDFB',
            marginBottom: '1rem'
          }}>
            <FileSpreadsheet size={32} color="var(--color-forest)" style={{ margin: '0 auto 0.5rem auto' }} />
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              id="csv-file-input"
            />
            <label htmlFor="csv-file-input" className="btn btn-secondary btn-sm" style={{ cursor: 'pointer' }}>
              Select CSV File
            </label>
            {csvFile && <div style={{ marginTop: '0.5rem', fontWeight: 600, fontSize: '0.8125rem' }}>{csvFile.name}</div>}
          </div>

          {importStatus && (
            <div style={{ padding: '0.75rem', backgroundColor: 'var(--color-sage-light)', borderRadius: '0.5rem', fontSize: '0.8125rem', marginBottom: '1rem', color: 'var(--color-forest)' }}>
              {importStatus}
            </div>
          )}

          {previewResult && (
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ display: 'flex', gap: '1rem', marginBottom: '0.75rem' }}>
                <span className="badge badge-success">{previewResult.valid_count} Valid Rows</span>
                {previewResult.invalid_count > 0 && <span className="badge badge-danger">{previewResult.invalid_count} Invalid / Duplicates</span>}
              </div>

              {previewResult.errors?.length > 0 && (
                <div style={{ maxHeight: '120px', overflowY: 'auto', backgroundColor: '#fee2e2', padding: '0.5rem', borderRadius: '0.375rem', fontSize: '0.75rem', color: 'var(--color-error)', marginBottom: '0.75rem' }}>
                  {previewResult.errors.map((err, i) => <div key={i}>• {err}</div>)}
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
                <button type="button" onClick={() => setIsUploadModalOpen(false)} className="btn btn-outline">Cancel</button>
                <button
                  type="button"
                  disabled={previewResult.valid_count === 0 || previewResult.invalid_count > 0}
                  onClick={handleExecuteImport}
                  className="btn btn-primary"
                >
                  Import All Students ({previewResult.valid_count})
                </button>
              </div>
            </div>
          )}
        </div>
      </Modal>
    </div>
  );
}
