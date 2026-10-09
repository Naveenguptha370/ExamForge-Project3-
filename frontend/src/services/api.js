/**
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
