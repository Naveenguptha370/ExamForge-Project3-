/**
<<<<<<< HEAD
 * ExamForge Internal API Client
 * Zero third-party cloud API dependencies; communicates strictly with local Django backend.
 */

const API_BASE = 'http://localhost:8000/api';

const getToken = () => localStorage.getItem('examforge_token');

export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('examforge_token', token);
  } else {
    localStorage.removeItem('examforge_token');
  }
};

export const getStoredUser = () => {
  const user = localStorage.getItem('examforge_user');
  try {
    return user ? JSON.parse(user) : null;
  } catch (e) {
    return null;
  }
};

export const setStoredUser = (user) => {
  if (user) {
    localStorage.setItem('examforge_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('examforge_user');
  }
};

async function request(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    ...(options.headers || {}),
  };

  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }

  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const config = {
    ...options,
    headers,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, config);

  if (response.status === 401 && !endpoint.includes('/accounts/auth/login/')) {
    setAuthToken(null);
    setStoredUser(null);
    window.location.href = '/login';
    throw new Error('Session expired. Please log in again.');
  }

  if (!response.ok) {
    let errorMsg = 'An error occurred';
    try {
      const errData = await response.json();
      errorMsg = errData.error || errData.detail || JSON.stringify(errData);
    } catch (e) {
      errorMsg = response.statusText;
    }
    throw new Error(errorMsg);
  }

  // Handle binary/file downloads
  if (options.isBlob) {
    return await response.blob();
  }

  return await response.json();
}

export const api = {
  // 1. Auth & Users (Member 1)
  login: (username, password) => request('/accounts/auth/login/', { method: 'POST', body: JSON.stringify({ username, password }) }),
  logout: () => request('/accounts/auth/logout/', { method: 'POST' }),
  getCurrentUser: () => request('/accounts/auth/me/'),
  getUsers: (params = '') => request(`/accounts/users/${params}`),
  createUser: (data) => request('/accounts/users/', { method: 'POST', body: JSON.stringify(data) }),
  updateUser: (id, data) => request(`/accounts/users/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  getUserActivities: () => request('/accounts/activity/'),

  // Faculty (Member 1)
  getFacultyProfiles: (params = '') => request(`/faculty/profiles/${params}`),
  getFacultySummary: () => request('/faculty/profiles/summary/'),
  getFacultyLeaves: () => request('/faculty/leaves/'),
  approveFacultyLeave: (id) => request(`/faculty/leaves/${id}/approve/`, { method: 'POST' }),
  getFacultyAvailability: () => request('/faculty/availability/'),

  // 2. Academics & Students (Member 2)
  getDepartments: () => request('/academics/departments/'),
  getCourses: () => request('/academics/courses/'),
  getBranches: () => request('/academics/branches/'),
  getSemesters: () => request('/academics/semesters/'),
  getSubjects: (params = '') => request(`/academics/subjects/${params}`),
  createSubject: (data) => request('/academics/subjects/', { method: 'POST', body: JSON.stringify(data) }),

  getStudents: (params = '') => request(`/students/profiles/${params}`),
  getStudentsSummary: () => request('/students/profiles/summary/'),
  createStudent: (data) => request('/students/profiles/', { method: 'POST', body: JSON.stringify(data) }),
  previewStudentCSV: (formData) => request('/students/profiles/csv_preview/', { method: 'POST', body: formData }),
  importStudentCSV: (formData) => request('/students/profiles/csv_import/', { method: 'POST', body: formData }),
  exportStudentCSVUrl: () => `${API_BASE}/students/profiles/export_csv/`,

  getSubjectRegistrations: (params = '') => request(`/registration/subjects/${params}`),
  getRegistrationSummary: () => request('/registration/subjects/summary/'),

  // 3. Examinations & Scheduling (Member 3)
  getExamSessions: () => request('/examinations/sessions/'),
  createExamSession: (data) => request('/examinations/sessions/', { method: 'POST', body: JSON.stringify(data) }),
  getTimeSlots: () => request('/examinations/timeslots/'),
  getExamSubjects: (params = '') => request(`/examinations/subjects/${params}`),
  addSubjectsToSession: (sessionId, subjectIds) => request(`/examinations/sessions/${sessionId}/add_subjects/`, { method: 'POST', body: JSON.stringify({ subject_ids: subjectIds }) }),
  approveExamSession: (sessionId) => request(`/examinations/sessions/${sessionId}/approve/`, { method: 'POST' }),
  publishExamSession: (sessionId) => request(`/examinations/sessions/${sessionId}/publish/`, { method: 'POST' }),

  getTimetables: () => request('/scheduling/timetables/'),
  generateTimetable: (sessionId) => request('/scheduling/timetables/generate/', { method: 'POST', body: JSON.stringify({ exam_session_id: sessionId }) }),
  approveTimetable: (id) => request(`/scheduling/timetables/${id}/approve/`, { method: 'POST' }),
  publishTimetable: (id) => request(`/scheduling/timetables/${id}/publish/`, { method: 'POST' }),
  getTimetableEntries: (params = '') => request(`/scheduling/entries/${params}`),
  manualAdjustEntry: (timetableId, entryId, newDate, newSlotId) => request(`/scheduling/timetables/${timetableId}/manual_adjust/`, { method: 'POST', body: JSON.stringify({ entry_id: entryId, exam_date: newDate, time_slot_id: newSlotId }) }),

  // 4. Infrastructure & Seating & Invigilation (Member 4)
  getBuildings: () => request('/infrastructure/buildings/'),
  getRooms: (params = '') => request(`/infrastructure/rooms/${params}`),
  getRoomSummary: () => request('/infrastructure/rooms/summary/'),
  createRoom: (data) => request('/infrastructure/rooms/', { method: 'POST', body: JSON.stringify(data) }),

  getSeatingPlans: (params = '') => request(`/seating/plans/${params}`),
  generateSeatingPlan: (examSubjectId, roomIds, spacingRule) => request('/seating/plans/generate_plan/', { method: 'POST', body: JSON.stringify({ exam_subject_id: examSubjectId, room_ids: roomIds, spacing_rule: spacingRule }) }),
  getSeatAllocations: (params = '') => request(`/seating/allocations/${params}`),

  getInvigilatorDuties: (params = '') => request(`/invigilation/duties/${params}`),
  getInvigilationSummary: () => request('/invigilation/duties/summary/'),
  autoAllocateInvigilators: (sessionId) => request('/invigilation/duties/auto_allocate/', { method: 'POST', body: JSON.stringify({ exam_session_id: sessionId }) }),

  // 5. Hall Tickets, Attendance, Analytics, Audit & Settings (Member 5)
  getHallTickets: (params = '') => request(`/halltickets/tickets/${params}`),
  generateIndividualHallTicket: (studentId, sessionId) => request('/halltickets/tickets/generate_individual/', { method: 'POST', body: JSON.stringify({ student_id: studentId, exam_session_id: sessionId }) }),
  bulkGenerateHallTickets: (sessionId, deptId) => request('/halltickets/tickets/bulk_generate/', { method: 'POST', body: JSON.stringify({ exam_session_id: sessionId, department_id: deptId }) }),
  getHallTicketPdfUrl: (ticketId) => `${API_BASE}/halltickets/tickets/${ticketId}/download_pdf/`,
  toggleBlockHallTicket: (ticketId, reason) => request(`/halltickets/tickets/${ticketId}/toggle_block/`, { method: 'POST', body: JSON.stringify({ reason }) }),

  getAttendanceSheets: (params = '') => request(`/attendance/sheets/${params}`),
  initAttendanceSheet: (examSubjectId, roomId) => request('/attendance/sheets/init_from_seating/', { method: 'POST', body: JSON.stringify({ exam_subject_id: examSubjectId, room_id: roomId }) }),
  markBatchAttendance: (sheetId, records) => request(`/attendance/sheets/${sheetId}/mark_batch/`, { method: 'POST', body: JSON.stringify({ records }) }),
  correctAttendanceRecord: (recordId, status, reason) => request(`/attendance/records/${recordId}/correct_status/`, { method: 'POST', body: JSON.stringify({ status, reason }) }),
  getPrintableAttendancePdfUrl: (sheetId) => `${API_BASE}/attendance/sheets/${sheetId}/printable_sheet/`,

  getAnnouncements: () => request('/notifications/announcements/'),
  createAnnouncement: (data) => request('/notifications/announcements/', { method: 'POST', body: JSON.stringify(data) }),
  getInAppNotifications: () => request('/notifications/messages/'),
  markAllNotificationsRead: () => request('/notifications/messages/mark_all_read/', { method: 'POST' }),
  getUnreadNotificationsCount: () => request('/notifications/messages/unread_count/'),

  getExecutiveSummary: () => request('/analytics/reports/executive_summary/'),
  getReadinessIndex: (sessionId) => request(`/analytics/reports/readiness_index/${sessionId ? `?exam_session=${sessionId}` : ''}`),
  getRoomUtilization: () => request('/analytics/reports/room_utilization/'),
  getExecutiveReportPdfUrl: () => `${API_BASE}/analytics/reports/export_summary_pdf/`,

  getAuditLogs: (params = '') => request(`/audit/logs/${params}`),
  getSystemSettings: () => request('/settings/config/'),
  updateSystemSettings: (data) => request('/settings/config/', { method: 'PUT', body: JSON.stringify(data) }),
};
=======
 * ExamForge M2 — Axios API Client
 * ================================
 * Centralized HTTP client that reuses M1's JWT token system.
 * All M2 services import from this file.
 */

import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
})

/* ── Request interceptor: attach JWT from localStorage ── */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('examforge_access_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error),
)

/* ── Response interceptor: handle 401 token refresh ──── */
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      try {
        const refresh = localStorage.getItem('examforge_refresh_token')
        if (!refresh) throw new Error('No refresh token')
        const { data } = await axios.post(`${BASE_URL}/auth/token/refresh/`, { refresh })
        localStorage.setItem('examforge_access_token', data.access)
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original)
      } catch {
        localStorage.removeItem('examforge_access_token')
        localStorage.removeItem('examforge_refresh_token')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

/* ── Helper to build query strings ───────────────────── */
export function buildParams(filters = {}) {
  const params = {}
  Object.entries(filters).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') params[k] = v
  })
  return params
}

export default api
>>>>>>> origin/member1-work
