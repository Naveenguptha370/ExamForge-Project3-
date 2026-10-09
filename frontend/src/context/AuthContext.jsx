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
