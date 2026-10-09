import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('examforge_user');
      if (saved) return JSON.parse(saved);
    } catch (e) {}
    return {
      username: 'admin',
      full_name: 'Dr. K. S. Ramanathan',
      role: 'ADMIN',
      email: 'admin@examforge.edu'
    };
  });

  const [activeSessionId, setActiveSessionId] = useState(1);

  const login = async (username, password) => {
    const res = await api.login(username, password);
    if (res.success && res.user) {
      setUser(res.user);
      localStorage.setItem('examforge_user', JSON.stringify(res.user));
      return { success: true };
    }
    return { success: false, message: 'Invalid credentials' };
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('examforge_user');
  };

  const switchRole = (newRole) => {
    const roleNames = {
      ADMIN: 'System Administrator (Controller of Exams)',
      FACULTY: 'Dr. Anand Krishnan (Faculty / Invigilator)',
      EXAM_STAFF: 'Rajesh Sharma (Exam Cell Superintendent)',
      STUDENT: 'Alice Smith (Student - 23CSE001)'
    };
    const updated = {
      username: newRole.toLowerCase(),
      full_name: roleNames[newRole] || newRole,
      role: newRole,
      email: `${newRole.toLowerCase()}@examforge.edu`
    };
    setUser(updated);
    localStorage.setItem('examforge_user', JSON.stringify(updated));
  };

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      switchRole,
      activeSessionId,
      setActiveSessionId,
      isAdmin: user?.role === 'ADMIN',
      isFaculty: user?.role === 'FACULTY',
      isStaff: user?.role === 'EXAM_STAFF',
      isStudent: user?.role === 'STUDENT'
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
