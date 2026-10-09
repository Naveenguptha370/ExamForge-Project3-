/**
 * ExamForge M2 — Bulk Import Page
 * Drag & drop CSV upload with live validation feedback.
 */

import { useState, useCallback } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import {
  HiOutlineUpload, HiOutlineDocument, HiOutlineDownload,
  HiOutlineCheckCircle, HiOutlineXCircle, HiOutlineX,
  HiOutlineInformationCircle,
} from 'react-icons/hi'
import toast from 'react-hot-toast'

import studentService  from '../../services/studentService.js'
import academicService from '../../services/academicService.js'

export default function BulkImport() {
  const [file, setFile]         = useState(null)
  const [acYear, setAcYear]     = useState('')
  const [importResult, setImportResult] = useState(null)

  const { data: yearsData } = useQuery({
    queryKey: ['academic-years'],
    queryFn: () => academicService.years.list({ page_size: 50 }).then(r => r.data.results),
    staleTime: 300_000,
  })

  const { data: logsData, refetch: refetchLogs } = useQuery({
    queryKey: ['import-logs'],
    queryFn: () => studentService.importLogs().then(r => r.data.data),
    staleTime: 30_000,
  })

  /* ── Drop zone ───────────────────────────────────────── */
  const onDrop = useCallback((accepted) => {
    const f = accepted[0]
    if (!f) return
    if (!f.name.endsWith('.csv')) { toast.error('Only CSV files are accepted.'); return }
    if (f.size > 10 * 1024 * 1024) { toast.error('File must be smaller than 10 MB.'); return }
    setFile(f)
    setImportResult(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'text/csv': ['.csv'] }, maxFiles: 1,
  })

  /* ── Import mutation ─────────────────────────────────── */
  const importMutation = useMutation({
    mutationFn: () => studentService.import(file, acYear),
    onSuccess: (res) => {
      setImportResult(res.data.data)
      refetchLogs()
      if (res.data.data.failed_rows === 0) {
        toast.success(`Import complete! ${res.data.data.successful_rows} students created.`)
      } else {
        toast.success(res.data.message, { duration: 6000 })
      }
    },
    onError: (err) => {
      toast.error(err.response?.data?.message || 'Import failed. Check the file format.')
    },
  })

  /* ── Template download ───────────────────────────────── */
  const handleDownloadTemplate = async () => {
    try {
      const res = await studentService.downloadTemplate()
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const a   = document.createElement('a')
      a.href    = url
      a.download = 'student_import_template.csv'
      a.click()
      window.URL.revokeObjectURL(url)
    } catch { toast.error('Failed to download template.') }
  }

  const canImport = file && acYear && !importMutation.isLoading
  const successRate = importResult
    ? Math.round((importResult.successful_rows / importResult.total_rows) * 100)
    : 0

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="page-title">
            <HiOutlineUpload size={24} color="var(--color-emerald)" />
            Bulk Student Import
          </div>
          <div className="page-subtitle">
            Upload a CSV file to create multiple students at once
          </div>
        </div>
        <button className="btn btn-secondary" onClick={handleDownloadTemplate}>
          <HiOutlineDownload size={15} /> Download Template
        </button>
      </div>

      <div style={{ display:'grid', gridTemplateColumns:'1fr 380px', gap:'var(--space-5)', alignItems:'start' }}>
        {/* ── Left: Upload area ──────────────────────── */}
        <div>
          <div className="card">
            <div className="card-header">
              <span className="card-title">Upload CSV File</span>
            </div>

            {/* Academic year picker */}
            <div className="form-group" style={{ marginBottom: 'var(--space-5)' }}>
              <label className="form-label">
                Academic Year <span className="required">*</span>
              </label>
              <select
                className="form-select"
                value={acYear}
                onChange={e => setAcYear(e.target.value)}
              >
                <option value="">— Select Academic Year —</option>
                {(yearsData || []).map(y => (
                  <option key={y.id} value={y.id}>
                    {y.label}{y.is_current ? ' (Current)' : ''}
                  </option>
                ))}
              </select>
            </div>

            {/* Drop zone */}
            <div
              {...getRootProps()}
              className="drop-zone"
              style={{
                borderColor: isDragActive ? 'var(--color-emerald)' : 'var(--color-border)',
                background: isDragActive ? 'var(--color-sage-light)' : file ? 'var(--color-green-50)' : undefined,
              }}
            >
              <input {...getInputProps()} />
              <div className="drop-zone-icon">
                {file ? '📄' : '📁'}
              </div>
              {file ? (
                <>
                  <div style={{ fontWeight:600, color:'var(--color-forest)', marginBottom:4 }}>
                    {file.name}
                  </div>
                  <div style={{ fontSize:'0.8125rem', color:'var(--color-gray)' }}>
                    {(file.size / 1024).toFixed(1)} KB
                  </div>
                  <button
                    className="btn btn-secondary btn-sm"
                    style={{ marginTop:12 }}
                    onClick={e => { e.stopPropagation(); setFile(null); setImportResult(null) }}
                  >
                    <HiOutlineX size={14} /> Remove file
                  </button>
                </>
              ) : (
                <>
                  <div style={{ fontWeight:600, color:'var(--color-charcoal)', marginBottom:6 }}>
                    {isDragActive ? 'Drop the CSV file here' : 'Drag & drop your CSV file here'}
                  </div>
                  <div style={{ fontSize:'0.875rem', color:'var(--color-gray)', marginBottom:12 }}>
                    or click to browse files
                  </div>
                  <div style={{ fontSize:'0.8125rem', color:'var(--color-gray)' }}>
                    Accepted: .csv · Max size: 10 MB · Max rows: 5,000
                  </div>
                </>
              )}
            </div>

            {/* Start import */}
            <div style={{ marginTop:'var(--space-5)', display:'flex', justifyContent:'flex-end', gap:12 }}>
              {file && (
                <button className="btn btn-secondary" onClick={() => { setFile(null); setImportResult(null) }}>
                  Clear
                </button>
              )}
              <button
                className={`btn btn-primary${importMutation.isLoading ? ' btn-loading' : ''}`}
                disabled={!canImport}
                onClick={() => importMutation.mutate()}
              >
                {importMutation.isLoading ? 'Importing…' : 'Start Import'}
              </button>
            </div>
          </div>

          {/* ── Result card ───────────────────────────── */}
          <AnimatePresence>
            {importResult && (
              <motion.div
                className="card"
                initial={{ opacity:0, y:12 }}
                animate={{ opacity:1, y:0 }}
                exit={{ opacity:0 }}
                style={{ marginTop:'var(--space-4)' }}
              >
                <div className="card-header">
                  <span className="card-title">
                    {importResult.failed_rows === 0
                      ? <><HiOutlineCheckCircle color="var(--color-success)" /> Import Complete</>
                      : <><HiOutlineXCircle color="var(--color-amber)" /> Partial Import</>
                    }
                  </span>
                  <span style={{ fontSize:'0.8rem', color:'var(--color-gray)' }}>
                    {importResult.success_rate}% success rate
                  </span>
                </div>

                {/* Progress bar */}
                <div className="progress-bar-track" style={{ marginBottom:'var(--space-4)' }}>
                  <div
                    className={`progress-bar-fill${importResult.failed_rows > 0 ? ' warning' : ''}`}
                    style={{ width: `${successRate}%` }}
                  />
                </div>

                {/* Stats */}
                <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:'var(--space-3)' }}>
                  {[
                    { label:'Created',     value: importResult.successful_rows, color:'var(--color-success)' },
                    { label:'Failed',      value: importResult.failed_rows,     color:'var(--color-error)'   },
                    { label:'Duplicates',  value: importResult.duplicate_rows,  color:'var(--color-amber)'   },
                    { label:'Total Rows',  value: importResult.total_rows,      color:'var(--color-gray)'    },
                  ].map(stat => (
                    <div key={stat.label} style={{
                      textAlign:'center', padding:'var(--space-3)',
                      background:'var(--color-bg)', borderRadius:'var(--radius-md)',
                      border:'1px solid var(--color-border)',
                    }}>
                      <div style={{ fontSize:'1.5rem', fontWeight:800, color:stat.color }}>
                        {stat.value}
                      </div>
                      <div style={{ fontSize:'0.75rem', color:'var(--color-gray)', fontWeight:500 }}>
                        {stat.label}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Row-level errors */}
                {importResult.error_details?.length > 0 && (
                  <div style={{ marginTop:'var(--space-4)' }}>
                    <div style={{ fontWeight:600, fontSize:'0.875rem', marginBottom:8 }}>
                      Row Errors ({importResult.error_details.length})
                    </div>
                    <div style={{
                      maxHeight:240, overflowY:'auto',
                      border:'1px solid var(--color-border)', borderRadius:'var(--radius-md)',
                    }}>
                      {importResult.error_details.slice(0, 50).map((err, i) => (
                        <div key={i} style={{
                          padding:'8px 12px', fontSize:'0.8rem',
                          borderBottom:i < importResult.error_details.length - 1 ? '1px solid var(--color-border)' : 'none',
                          display:'flex', gap:8,
                        }}>
                          <span style={{ fontWeight:600, color:'var(--color-error)', whiteSpace:'nowrap' }}>
                            Row {err.row}
                          </span>
                          <span style={{ color:'var(--color-gray)' }}>
                            {err.roll && <strong style={{ color:'var(--color-charcoal)' }}>[{err.roll}] </strong>}
                            {err.errors?.map(e => e.error).join('; ')}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* ── Right: Instructions + Log ──────────────── */}
        <div style={{ display:'flex', flexDirection:'column', gap:'var(--space-4)' }}>
          {/* Instructions */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">
                <HiOutlineInformationCircle size={16} /> CSV Format Guide
              </span>
            </div>
            <div style={{ fontSize:'0.8125rem', color:'var(--color-gray)' }}>
              <p style={{ marginBottom:8, color:'var(--color-charcoal)', fontWeight:500 }}>Required columns:</p>
              <ul style={{ paddingLeft:16, marginBottom:12 }}>
                {['roll_number','full_name','email','department_code','course_code','semester_number','academic_year'].map(c => (
                  <li key={c} style={{ marginBottom:4 }}>
                    <code style={{
                      background:'var(--color-sage)', padding:'1px 5px',
                      borderRadius:4, fontSize:'0.75rem', fontFamily:'monospace',
                    }}>{c}</code>
                  </li>
                ))}
              </ul>
              <p style={{ marginBottom:8, color:'var(--color-charcoal)', fontWeight:500 }}>Optional columns:</p>
              <ul style={{ paddingLeft:16 }}>
                {['branch_code','phone','admission_date','gender','date_of_birth'].map(c => (
                  <li key={c} style={{ marginBottom:4 }}>
                    <code style={{
                      background:'var(--color-border)', padding:'1px 5px',
                      borderRadius:4, fontSize:'0.75rem', fontFamily:'monospace',
                    }}>{c}</code>
                  </li>
                ))}
              </ul>
              <div style={{
                marginTop:12, padding:'8px 10px',
                background:'var(--color-amber-50)',
                border:'1px solid var(--color-amber)',
                borderRadius:'var(--radius-md)', fontSize:'0.75rem',
                color:'#92400E',
              }}>
                ⚠ Date format: <strong>YYYY-MM-DD</strong><br />
                academic_year format: <strong>2024-2025</strong>
              </div>
            </div>
          </div>

          {/* Import history */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">Import History</span>
            </div>
            {(logsData || []).length === 0 ? (
              <div style={{ color:'var(--color-gray)', fontSize:'0.8125rem', textAlign:'center', padding:'16px 0' }}>
                No import history yet
              </div>
            ) : (
              (logsData || []).slice(0,5).map(log => (
                <div key={log.id} style={{
                  display:'flex', gap:8, alignItems:'center',
                  padding:'8px 0', borderBottom:'1px solid var(--color-border)',
                  fontSize:'0.8125rem',
                }}>
                  <span style={{
                    width:8, height:8, borderRadius:'50%', flexShrink:0,
                    background: log.status === 'completed' ? 'var(--color-success)'
                              : log.status === 'partial'   ? 'var(--color-amber)'
                              : log.status === 'failed'    ? 'var(--color-error)'
                              : 'var(--color-gray)',
                  }} />
                  <div style={{ flex:1, minWidth:0 }}>
                    <div style={{ overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap', fontWeight:500 }}>
                      {log.file_name}
                    </div>
                    <div style={{ color:'var(--color-gray)', fontSize:'0.75rem' }}>
                      {log.successful_rows}/{log.total_rows} created
                    </div>
                  </div>
                  <span className={`badge ${
                    log.status === 'completed' ? 'badge-success'
                    : log.status === 'partial' ? 'badge-warning'
                    : log.status === 'failed'  ? 'badge-error'
                    : 'badge-neutral'
                  }`}>
                    {log.status}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
