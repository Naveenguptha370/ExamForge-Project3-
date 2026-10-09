/** ExamForge M2 — Student API Service */
import api, { buildParams } from './api.js'

const BASE = '/students'

const studentService = {
  // ── List & Fetch ─────────────────────────────────────
  list: (params = {}) =>
    api.get(`${BASE}/`, { params: buildParams(params) }),

  get: (id) => api.get(`${BASE}/${id}/`),

  dashboard: () => api.get(`${BASE}/dashboard/`),

  summary: (id) => api.get(`${BASE}/${id}/summary/`),

  registrations: (id) => api.get(`${BASE}/${id}/registrations/`),

  // ── Write ────────────────────────────────────────────
  create: (data) => api.post(`${BASE}/`, data),

  update: (id, data) => api.patch(`${BASE}/${id}/`, data),

  delete: (id, reason) => api.delete(`${BASE}/${id}/`, { data: { reason } }),

  deactivate: (id, reason) =>
    api.post(`${BASE}/${id}/deactivate/`, { reason }),

  activate: (id) => api.post(`${BASE}/${id}/activate/`),

  // ── CSV Import ───────────────────────────────────────
  downloadTemplate: () =>
    api.get(`${BASE}/import/template/`, { responseType: 'blob' }),

  import: (file, academicYearId) => {
    const fd = new FormData()
    fd.append('file', file)
    fd.append('academic_year_id', academicYearId)
    return api.post(`${BASE}/import/`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  importLogs: () => api.get(`${BASE}/import/logs/`),

  // ── Enrollment Records ───────────────────────────────
  listEnrollments: (params = {}) =>
    api.get('/students/enrollments/', { params: buildParams(params) }),

  createEnrollment: (data) => api.post('/students/enrollments/', data),
}

export default studentService
