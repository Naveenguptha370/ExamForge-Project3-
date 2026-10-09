/** ExamForge M2 — Registration API Service */
import api, { buildParams } from './api.js'

const registrationService = {
  // ── Dashboard ────────────────────────────────────────
  dashboard: () => api.get('/registrations/dashboard/'),

  // ── Subject Registrations ────────────────────────────
  subjects: {
    list:       (p) => api.get('/registrations/subject-registrations/', { params: buildParams(p) }),
    get:        (id) => api.get(`/registrations/subject-registrations/${id}/`),
    create:     (d) => api.post('/registrations/subject-registrations/', d),
    cancel:     (id, reason) => api.post(`/registrations/subject-registrations/${id}/cancel/`, { reason }),
    available:  (studentId) => api.get(`/registrations/available-subjects/?student=${studentId}`),
    eligibility:(studentId, subjectId) =>
      api.get(`/registrations/eligibility/?student=${studentId}&subject=${subjectId}`),
  },

  // ── Exam Registrations ───────────────────────────────
  exams: {
    list:   (p) => api.get('/registrations/exam-registrations/', { params: buildParams(p) }),
    get:    (id) => api.get(`/registrations/exam-registrations/${id}/`),
    create: (d) => api.post('/registrations/exam-registrations/', d),
    cancel: (id, reason) =>
      api.post(`/registrations/exam-registrations/${id}/cancel/`, { reason }),
  },

  // ── Bulk Registration ────────────────────────────────
  bulk: {
    register:   (d) => api.post('/registrations/bulk/register/', d),
    jobs:       () => api.get('/registrations/bulk/jobs/'),
    jobDetail:  (id) => api.get(`/registrations/bulk/jobs/${id}/`),
    importCsv:  (file, type, academicYearId, examSessionId) => {
      const fd = new FormData()
      fd.append('file', file)
      fd.append('type', type)
      fd.append('academic_year_id', academicYearId)
      if (examSessionId) fd.append('exam_session_id', examSessionId)
      return api.post('/registrations/bulk/import/', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    },
    template: (type) =>
      api.get(`/registrations/bulk/template/?type=${type}`, { responseType: 'blob' }),
  },

  // ── Reports ───────────────────────────────────────────
  reports: {
    summary:    (p) => api.get('/registrations/reports/summary/', { params: buildParams(p) }),
    byDept:     (p) => api.get('/registrations/reports/by-department/', { params: buildParams(p) }),
    bySession:  (p) => api.get('/registrations/reports/by-session/', { params: buildParams(p) }),
  },
}

export default registrationService
