<<<<<<< HEAD
import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, setAuthToken, setStoredUser, getStoredUser } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(getStoredUser());
  const [token, setTokenState] = useState(localStorage.getItem('examforge_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const userData = await api.getCurrentUser();
          setUser(userData);
          setStoredUser(userData);
        } catch (e) {
          console.warn('Auth check failed:', e);
          setAuthToken(null);
          setStoredUser(null);
          setUser(null);
        }
      }
      setLoading(false);
    };
    checkAuth();
  }, [token]);

  const login = async (username, password) => {
    const res = await api.login(username, password);
    setAuthToken(res.token);
    setStoredUser(res.user);
    setTokenState(res.token);
    setUser(res.user);
    return res.user;
  };

  const logout = async () => {
    try {
      await api.logout();
    } catch (e) {
      // Continue client cleanup even if network fails
    }
    setAuthToken(null);
    setStoredUser(null);
    setTokenState(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    isAdmin: user?.role === 'ADMIN',
    isFaculty: user?.role === 'FACULTY',
    isStaff: user?.role === 'EXAM_STAFF',
    isStudent: user?.role === 'STUDENT',
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
=======
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
>>>>>>> origin/member1-work
