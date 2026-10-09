import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Calendar, Clock, Shield, Users, BookOpen, UserCheck,
  Layers, Grid, UserPlus, FileText, CheckSquare, Bell,
  BarChart3, Settings, LogOut, ChevronLeft, ChevronRight,
  Sparkles, AlertTriangle, Search, CheckCircle2, Award, Download
} from 'lucide-react';

export const AppLayout = ({ activeTab, onSelectTab, children }) => {
  const { user, logout, switchRole, activeSessionId, setActiveSessionId } = useAuth();
  const [collapsed, setCollapsed] = useState(false);

  const menuSections = [
    {
      title: 'OPERATIONS',
      items: [
        { id: 'dashboard', label: 'Operations Hub', icon: <BarChart3 size={18} /> },
        { id: 'landing', label: 'Public Portal', icon: <Sparkles size={18} color="#D4A72C" /> },
      ]
    },
    {
      title: 'MEMBER 3 — EXAM & TIMETABLE',
      items: [
        { id: 'timetable_studio', label: 'Timetable Studio (CSP)', icon: <Sparkles size={18} />, highlight: true },
        { id: 'exam_sessions', label: 'Exam Sessions', icon: <Calendar size={18} /> },
        { id: 'time_slots', label: 'Time Slots & Shifts', icon: <Clock size={18} /> },
        { id: 'subject_config', label: 'Subject Configurations', icon: <Layers size={18} /> },
        { id: 'conflict_radar', label: 'Conflict Radar', icon: <AlertTriangle size={18} /> },
        { id: 'timetable_view', label: 'Published Timetable', icon: <Calendar size={18} /> },
      ]
    },
    {
      title: 'MEMBER 2 — ACADEMICS & STUDENTS',
      items: [
        { id: 'academics', label: 'Departments & Subjects', icon: <BookOpen size={18} /> },
        { id: 'students', label: 'Students & CSV Import', icon: <Users size={18} /> },
      ]
    },
    {
      title: 'MEMBER 1 — USERS & FACULTY',
      items: [
        { id: 'faculty', label: 'Faculty Directory & Leaves', icon: <UserCheck size={18} /> },
      ]
    },
    {
      title: 'MEMBER 4 — ROOMS & LOGISTICS',
      items: [
        { id: 'rooms', label: 'Examination Halls', icon: <Layers size={18} /> },
        { id: 'seating', label: 'Seating Arrangement', icon: <Grid size={18} /> },
        { id: 'invigilation', label: 'Invigilation Roster', icon: <UserPlus size={18} /> },
      ]
    },
    {
      title: 'MEMBER 5 — PASSES & AUDIT',
      items: [
        { id: 'halltickets', label: 'Hall Tickets (PDF)', icon: <FileText size={18} /> },
        { id: 'attendance', label: 'Exam Attendance', icon: <CheckSquare size={18} /> },
        { id: 'analytics', label: 'Readiness & Analytics', icon: <Award size={18} /> },
        { id: 'notifications', label: 'Campus Notices', icon: <Bell size={18} /> },
        { id: 'audit', label: 'Audit Trail & Settings', icon: <Settings size={18} /> },
      ]
    }
  ];

  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: 'var(--color-bg)' }}>
      {/* Sidebar */}
      <aside
        style={{
          width: collapsed ? 80 : 280,
          backgroundColor: '#FFFFFF',
          borderRight: '1px solid #E7E5E4',
          display: 'flex',
          flexDirection: 'column',
          transition: 'width 0.25s ease',
          zIndex: 100,
          position: 'sticky',
          top: 0,
          height: '100vh',
          flexShrink: 0
        }}
      >
        {/* Brand Header */}
        <div
          style={{
            height: 70,
            padding: '0 20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: collapsed ? 'center' : 'space-between',
            borderBottom: '1px solid #E7E5E4'
          }}
        >
          <div
            onClick={() => onSelectTab('landing')}
            style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}
          >
            <div
              style={{
                width: 38,
                height: 38,
                borderRadius: 10,
                backgroundColor: '#14532D',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#D4A72C',
                fontWeight: 800,
                fontSize: '1.2rem',
                boxShadow: '0 2px 8px rgba(20, 83, 45, 0.25)'
              }}
            >
              EF
            </div>
            {!collapsed && (
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span style={{ fontSize: '1.15rem', fontWeight: 800, color: '#14532D', fontFamily: 'var(--font-display)', letterSpacing: '-0.02em' }}>
                  Exam<span style={{ color: '#D4A72C' }}>Forge</span>
                </span>
                <span style={{ fontSize: '0.68rem', fontWeight: 600, color: '#6B7280', letterSpacing: '0.04em' }}>
                  OPERATIONS SYSTEM
                </span>
              </div>
            )}
          </div>
          <button
            onClick={() => setCollapsed(!collapsed)}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: '#6B7280',
              padding: 6,
              borderRadius: 6,
              display: collapsed ? 'none' : 'flex'
            }}
          >
            <ChevronLeft size={18} />
          </button>
        </div>

        {/* Navigation Menu */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px 12px' }}>
          {menuSections.map((sec, sIdx) => (
            <div key={sIdx} style={{ marginBottom: 18 }}>
              {!collapsed && (
                <div style={{ fontSize: '0.68rem', fontWeight: 700, color: '#9CA3AF', letterSpacing: '0.06em', padding: '0 12px 6px' }}>
                  {sec.title}
                </div>
              )}
              {sec.items.map((item) => {
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => onSelectTab(item.id)}
                    style={{
                      width: '100%',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 12,
                      padding: collapsed ? '12px 0' : '10px 14px',
                      justifyContent: collapsed ? 'center' : 'flex-start',
                      borderRadius: 10,
                      border: 'none',
                      backgroundColor: isActive ? '#14532D' : (item.highlight ? '#F0FDF4' : 'transparent'),
                      color: isActive ? '#FFFFFF' : (item.highlight ? '#15803D' : '#242923'),
                      fontWeight: isActive ? 700 : (item.highlight ? 600 : 500),
                      fontSize: '0.86rem',
                      cursor: 'pointer',
                      marginBottom: 3,
                      transition: 'all 0.15s ease',
                      borderLeft: item.highlight && !isActive ? '3px solid #15803D' : 'none'
                    }}
                  >
                    <span style={{ color: isActive ? '#D4A72C' : 'inherit' }}>{item.icon}</span>
                    {!collapsed && <span>{item.label}</span>}
                  </button>
                );
              })}
            </div>
          ))}
        </div>

        {/* User Footer */}
        <div
          style={{
            padding: '14px 16px',
            borderTop: '1px solid #E7E5E4',
            display: 'flex',
            alignItems: 'center',
            justifyContent: collapsed ? 'center' : 'space-between',
            backgroundColor: '#FAF9F6'
          }}
        >
          {!collapsed && (
            <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <span style={{ fontSize: '0.82rem', fontWeight: 700, color: '#14532D', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                {user?.full_name || 'System Admin'}
              </span>
              <span style={{ fontSize: '0.7rem', color: '#15803D', fontWeight: 600 }}>
                {user?.role || 'ADMIN'}
              </span>
            </div>
          )}
          <button
            onClick={() => onSelectTab('login')}
            title="Switch User / Logout"
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: '#DC2626',
              padding: 6,
              borderRadius: 6
            }}
          >
            <LogOut size={18} />
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        {/* Top Header Bar */}
        <header
          style={{
            height: 70,
            backgroundColor: '#FFFFFF',
            borderBottom: '1px solid #E7E5E4',
            padding: '0 32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            position: 'sticky',
            top: 0,
            zIndex: 90
          }}
        >
          {/* Active Session Badge */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#6B7280', textTransform: 'uppercase' }}>
              ACTIVE EXAMINATION SESSION:
            </span>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                padding: '6px 14px',
                borderRadius: 9999,
                backgroundColor: '#DDEBDD',
                border: '1px solid #b8d6b8',
                fontSize: '0.82rem',
                fontWeight: 700,
                color: '#14532D'
              }}
            >
              <CheckCircle2 size={14} color="#15803D" />
              <span>ESE-AUT-2025 (Autumn Term 2025)</span>
            </div>
          </div>

          {/* Role Switcher & Action shortcuts */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, backgroundColor: '#FAF9F6', padding: '4px 8px', borderRadius: 8, border: '1px solid #E7E5E4' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#6B7280' }}>Role Simulation:</span>
              <select
                value={user?.role || 'ADMIN'}
                onChange={(e) => switchRole(e.target.value)}
                style={{
                  padding: '4px 8px',
                  borderRadius: 6,
                  border: '1px solid #D1D5DB',
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  backgroundColor: '#FFFFFF',
                  color: '#14532D',
                  cursor: 'pointer'
                }}
              >
                <option value="ADMIN">Administrator (Full Access)</option>
                <option value="FACULTY">Faculty / Invigilator</option>
                <option value="EXAM_STAFF">Examination Staff</option>
                <option value="STUDENT">Student View</option>
              </select>
            </div>

            <button
              onClick={() => onSelectTab('timetable_studio')}
              className="btn btn-primary btn-sm"
            >
              <Sparkles size={15} color="#D4A72C" />
              <span>Run CSP Solver</span>
            </button>
          </div>
        </header>

        {/* Dynamic Page Content */}
        <main style={{ flex: 1, padding: 32 }}>
          {children}
        </main>
      </div>
    </div>
  );
};
