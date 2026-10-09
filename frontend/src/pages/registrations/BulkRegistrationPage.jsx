/** ExamForge M2 — Bulk Registration Page */
import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { useMutation, useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { HiOutlineUpload, HiOutlineDownload, HiOutlineX, HiOutlineInformationCircle } from 'react-icons/hi'
import toast from 'react-hot-toast'
import registrationService from '../../services/registrationService.js'
import academicService from '../../services/academicService.js'

export default function BulkRegistrationPage() {
  const [file, setFile]       = useState(null)
  const [type, setType]       = useState('subject')
  const [acYear, setAcYear]   = useState('')
  const [result, setResult]   = useState(null)

  const { data: years } = useQuery({
    queryKey: ['academic-years'],
    queryFn: () => academicService.years.list({ page_size: 50 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const onDrop = useCallback((accepted) => {
    const f = accepted[0]
    if (!f) return
    if (!f.name.endsWith('.csv')) { toast.error('Only CSV files accepted.'); return }
    setFile(f); setResult(null)
  }, [])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: { 'text/csv': ['.csv'] }, maxFiles: 1 })

  const importMutation = useMutation({
    mutationFn: () => registrationService.bulk.importCsv(file, type, acYear),
    onSuccess: (res) => {
      setResult(res.data.data)
      toast.success(res.data.message || 'Bulk registration complete.')
    },
    onError: (err) => toast.error(err.response?.data?.message || 'Bulk import failed.'),
  })

  const handleTemplate = async () => {
    try {
      const res = await registrationService.bulk.template(type)
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const a = document.createElement('a'); a.href = url; a.download = `${type}_registration_template.csv`; a.click()
      window.URL.revokeObjectURL(url)
    } catch { toast.error('Template download failed.') }
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="page-title"><HiOutlineUpload size={22} color="var(--color-emerald)" /> Bulk Registration</div>
          <div className="page-subtitle">Upload a CSV to register multiple students at once</div>
        </div>
        <button className="btn btn-secondary" onClick={handleTemplate}>
          <HiOutlineDownload size={15} /> Download Template
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: 'var(--space-5)', alignItems: 'start' }}>
        <div>
          <div className="card">
            <div className="card-header"><span className="card-title">Upload Configuration</span></div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)', marginBottom: 'var(--space-5)' }}>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">Registration Type</label>
                <select className="form-select" value={type} onChange={e => setType(e.target.value)}>
                  <option value="subject">Subject Registration</option>
                  <option value="exam">Exam Registration</option>
                </select>
              </div>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">Academic Year</label>
                <select className="form-select" value={acYear} onChange={e => setAcYear(e.target.value)}>
                  <option value="">— Select Year —</option>
                  {(years || []).map(y => <option key={y.id} value={y.id}>{y.label}{y.is_current ? ' (Current)' : ''}</option>)}
                </select>
              </div>
            </div>

            <div {...getRootProps()} className="drop-zone" style={{ borderColor: isDragActive ? 'var(--color-emerald)' : undefined, background: isDragActive ? 'var(--color-sage-light)' : file ? 'var(--color-green-50)' : undefined }}>
              <input {...getInputProps()} />
              <div className="drop-zone-icon">{file ? '📄' : '📁'}</div>
              {file ? (
                <>
                  <div style={{ fontWeight: 600, color: 'var(--color-forest)' }}>{file.name}</div>
                  <div style={{ fontSize: '0.8125rem', color: 'var(--color-gray)' }}>{(file.size / 1024).toFixed(1)} KB</div>
                  <button className="btn btn-secondary btn-sm" style={{ marginTop: 10 }} onClick={e => { e.stopPropagation(); setFile(null); setResult(null) }}>
                    <HiOutlineX size={13} /> Remove
                  </button>
                </>
              ) : (
                <>
                  <div style={{ fontWeight: 600, color: 'var(--color-charcoal)' }}>{isDragActive ? 'Drop it here!' : 'Drag & drop CSV or click to browse'}</div>
                  <div style={{ fontSize: '0.8125rem', color: 'var(--color-gray)' }}>Max 10 MB · .csv only</div>
                </>
              )}
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12, marginTop: 'var(--space-4)' }}>
              <button className={`btn btn-primary${importMutation.isLoading ? ' btn-loading' : ''}`}
                disabled={!file || !acYear || importMutation.isLoading}
                onClick={() => importMutation.mutate()}>
                {importMutation.isLoading ? 'Processing…' : 'Start Bulk Registration'}
              </button>
            </div>
          </div>

          {result && (
            <motion.div className="card" style={{ marginTop: 'var(--space-4)' }} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
              <div className="card-header"><span className="card-title">Results</span></div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--space-3)' }}>
                {[
                  { label: 'Registered',  value: result.successful_rows, color: 'var(--color-success)' },
                  { label: 'Failed',      value: result.failed_rows,     color: 'var(--color-error)'   },
                  { label: 'Duplicates',  value: result.duplicate_rows,  color: 'var(--color-amber)'   },
                  { label: 'Total',       value: result.total_rows,      color: 'var(--color-gray)'    },
                ].map(s => (
                  <div key={s.label} style={{ textAlign: 'center', padding: 'var(--space-3)', background: 'var(--color-bg)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 800, color: s.color }}>{s.value}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--color-gray)' }}>{s.label}</div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title"><HiOutlineInformationCircle size={15} /> CSV Format</span></div>
          <div style={{ fontSize: '0.8125rem', color: 'var(--color-gray)' }}>
            <p style={{ fontWeight: 600, color: 'var(--color-charcoal)', marginBottom: 6 }}>Required columns (subject):</p>
            <ul style={{ paddingLeft: 16, marginBottom: 12 }}>
              {['student_roll', 'subject_code', 'semester_number', 'academic_year'].map(c => (
                <li key={c} style={{ marginBottom: 3 }}>
                  <code style={{ background: 'var(--color-sage)', padding: '1px 5px', borderRadius: 4, fontSize: '0.75rem', fontFamily: 'monospace' }}>{c}</code>
                </li>
              ))}
            </ul>
            <p style={{ fontWeight: 600, color: 'var(--color-charcoal)', marginBottom: 6 }}>Required columns (exam):</p>
            <ul style={{ paddingLeft: 16 }}>
              {['student_roll', 'subject_code', 'exam_session_id'].map(c => (
                <li key={c} style={{ marginBottom: 3 }}>
                  <code style={{ background: 'var(--color-border)', padding: '1px 5px', borderRadius: 4, fontSize: '0.75rem', fontFamily: 'monospace' }}>{c}</code>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
