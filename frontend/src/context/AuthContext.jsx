/**
 * ExamForge M2 — Auth Context
 * ==============================
 * Reuses M1's JWT token stored in localStorage.
 * M1 is responsible for login/logout flows.
 * M2 reads the token to hydrate user state.
 */

import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import api from '../services/api.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser]       = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  const fetchMe = useCallback(async () => {
    const token = localStorage.getItem('examforge_access_token')
    if (!token) { setIsLoading(false); return }
    try {
      const { data } = await api.get('/auth/me/')
      setUser(data.data || data)
    } catch {
      localStorage.removeItem('examforge_access_token')
      localStorage.removeItem('examforge_refresh_token')
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => { fetchMe() }, [fetchMe])

  const logout = useCallback(() => {
    localStorage.removeItem('examforge_access_token')
    localStorage.removeItem('examforge_refresh_token')
    setUser(null)
    window.location.href = '/login'
  }, [])

  // For M2 dev mode — mock user when M1 isn't deployed yet
  const mockLogin = useCallback((role = 'admin') => {
    const mock = {
      id: 1,
      username: `${role}_user`,
      email: `${role}@examforge.dev`,
      role,
      first_name: role === 'admin' ? 'Admin' : 'Staff',
      last_name: 'User',
      is_staff: role !== 'student',
    }
    localStorage.setItem('examforge_access_token', 'mock-token-dev')
    setUser(mock)
  }, [])

  const value = {
    user,
    isLoading,
    isAuthenticated: !!user,
    isAdmin:      user?.role === 'admin',
    isExamStaff:  user?.role === 'exam_staff',
    isFaculty:    user?.role === 'faculty',
    isStudent:    user?.role === 'student',
    logout,
    mockLogin,
    refetch: fetchMe,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}
