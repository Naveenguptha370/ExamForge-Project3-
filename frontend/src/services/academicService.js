/** ExamForge M2 — Academic API Service */
import api, { buildParams } from './api.js'

const academicService = {
  // ── Dashboard & Structure ────────────────────────────
  dashboard:  () => api.get('/academics/dashboard/'),
  structure:  () => api.get('/academics/structure/'),

  // ── Academic Years ───────────────────────────────────
  years: {
    list:       (p) => api.get('/academics/years/', { params: buildParams(p) }),
    get:        (id) => api.get(`/academics/years/${id}/`),
    create:     (d) => api.post('/academics/years/', d),
    update:     (id, d) => api.patch(`/academics/years/${id}/`, d),
    delete:     (id) => api.delete(`/academics/years/${id}/`),
    current:    () => api.get('/academics/years/current/'),
    setCurrent: (id) => api.post(`/academics/years/${id}/set-current/`),
  },

  // ── Departments ───────────────────────────────────────
  departments: {
    list:    (p) => api.get('/academics/departments/', { params: buildParams(p) }),
    get:     (id) => api.get(`/academics/departments/${id}/`),
    create:  (d) => api.post('/academics/departments/', d),
    update:  (id, d) => api.patch(`/academics/departments/${id}/`, d),
    delete:  (id) => api.delete(`/academics/departments/${id}/`),
    archive: (id) => api.post(`/academics/departments/${id}/archive/`),
    courses: (id) => api.get(`/academics/departments/${id}/courses/`),
  },

  // ── Courses ───────────────────────────────────────────
  courses: {
    list:     (p) => api.get('/academics/courses/', { params: buildParams(p) }),
    get:      (id) => api.get(`/academics/courses/${id}/`),
    create:   (d) => api.post('/academics/courses/', d),
    update:   (id, d) => api.patch(`/academics/courses/${id}/`, d),
    delete:   (id) => api.delete(`/academics/courses/${id}/`),
    branches: (id) => api.get(`/academics/courses/${id}/branches/`),
    semesters:(id) => api.get(`/academics/courses/${id}/semesters/`),
  },

  // ── Branches ──────────────────────────────────────────
  branches: {
    list:   (p) => api.get('/academics/branches/', { params: buildParams(p) }),
    get:    (id) => api.get(`/academics/branches/${id}/`),
    create: (d) => api.post('/academics/branches/', d),
    update: (id, d) => api.patch(`/academics/branches/${id}/`, d),
    delete: (id) => api.delete(`/academics/branches/${id}/`),
  },

  // ── Semesters ─────────────────────────────────────────
  semesters: {
    list:     (p) => api.get('/academics/semesters/', { params: buildParams(p) }),
    get:      (id) => api.get(`/academics/semesters/${id}/`),
    create:   (d) => api.post('/academics/semesters/', d),
    update:   (id, d) => api.patch(`/academics/semesters/${id}/`, d),
    delete:   (id) => api.delete(`/academics/semesters/${id}/`),
    subjects: (id) => api.get(`/academics/semesters/${id}/subjects/`),
  },

  // ── Subjects ──────────────────────────────────────────
  subjects: {
    list:    (p) => api.get('/academics/subjects/', { params: buildParams(p) }),
    get:     (id) => api.get(`/academics/subjects/${id}/`),
    create:  (d) => api.post('/academics/subjects/', d),
    update:  (id, d) => api.patch(`/academics/subjects/${id}/`, d),
    delete:  (id) => api.delete(`/academics/subjects/${id}/`),
    archive: (id) => api.post(`/academics/subjects/${id}/archive/`),
  },
}

export default academicService
