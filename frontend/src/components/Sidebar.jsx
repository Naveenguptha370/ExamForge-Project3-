import React from 'react';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Users,
  GraduationCap,
  BookOpen,
  CalendarDays,
  DoorOpen,
  Grid,
  UserCheck,
  FileText,
  ClipboardCheck,
  Bell,
  BarChart3,
  History,
  Settings,
  LogOut,
  Shield,
  Layers,
  Sparkles,
  ChevronRight
} from 'lucide-react';

export default function Sidebar({ currentTab, onSelectTab, onNavigateLanding }) {
  const { user, logout, login } = useAuth();

  const navigationSections = [
    {
      title: 'COMMAND CENTER',
      items: [
        { id: 'dashboard', label: 'Overview Dashboard', icon: LayoutDashboard, badge: 'Live' }
      ]
    },
    {
      title: 'MEMBER 1: AUTH & FACULTY',
      items: [
        { id: 'users', label: 'User & Account Mgmt', icon: Users },
        { id: 'faculty', label: 'Faculty Directory & Leaves', icon: UserCheck }
      ]
    },
    {
      title: 'MEMBER 2: ACADEMICS & STUDENTS',
      items: [
        { id: 'academics', label: 'Departments & Subjects', icon: BookOpen },
        { id: 'students', label: 'Students & CSV Import', icon: GraduationCap },
        { id: 'registrations', label: 'Exam Registrations', icon: Layers }
      ]
    },
    {
      title: 'MEMBER 3: EXAMS & TIMETABLE',
      items: [
        { id: 'sessions', label: 'Exam Sessions & Slots', icon: CalendarDays },
        { id: 'timetable', label: 'Timetable Solver Engine', icon: Sparkles, badge: 'Solver' }
      ]
    },
    {
      title: 'MEMBER 4: ROOMS & SEATING',
      items: [
        { id: 'rooms', label: 'Halls & Infrastructure', icon: DoorOpen },
        { id: 'seating', label: 'Visual Seating Grid', icon: Grid },
        { id: 'invigilation', label: 'Invigilation Roster', icon: UserCheck }
      ]
    },
    {
      title: 'MEMBER 5: DOCUMENTS & ANALYTICS',
      items: [
        { id: 'halltickets', label: 'Hall Tickets (ReportLab)', icon: FileText, badge: 'PDF' },
        { id: 'attendance', label: 'Exam Hall Attendance', icon: ClipboardCheck },
        { id: 'notifications', label: 'Announcements & Alerts', icon: Bell },
        { id: 'reports', label: 'Reports & Analytics', icon: BarChart3 },
        { id: 'audit', label: 'System Audit Logs', icon: History },
        { id: 'settings', label: 'Institutional Settings', icon: Settings }
      ]
    }
  ];

  const handleQuickSwitch = async (roleName, uName, pass) => {
    try {
      await login(uName, pass);
      onSelectTab('dashboard');
    } catch (e) {
      alert(`Could not switch to demo role ${roleName}: ` + e.message);
    }
  };

  return (
    <aside style={{
      width: '280px',
      backgroundColor: '#FFFFFF',
      borderRight: '1px solid var(--color-border)',
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      position: 'sticky',
      top: 0,
      zIndex: 30,
      flexShrink: 0
    }}>
      {/* Brand Header */}
      <div style={{
        padding: '1.25rem 1.25rem 1rem 1.25rem',
        borderBottom: '1px solid var(--color-border-light)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div
          style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', cursor: 'pointer' }}
          onClick={onNavigateLanding}
          title="Return to Public Landing Page"
        >
          <div style={{
            width: '2.25rem',
            height: '2.25rem',
            borderRadius: '0.5rem',
            backgroundColor: 'var(--color-forest)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFFFFF'
          }}>
            <Shield size={18} color="#D4A72C" />
          </div>
          <div>
            <div style={{ fontFamily: 'var(--font-heading)', fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)', lineHeight: 1.1 }}>
              ExamForge
            </div>
            <div style={{ fontSize: '0.625rem', color: 'var(--color-muted)', fontWeight: 600, letterSpacing: '0.05em' }}>
              EXAMINATION OPS
            </div>
          </div>
        </div>

        <span className="badge badge-success" style={{ fontSize: '0.6875rem' }}>
          {user?.role || 'GUEST'}
        </span>
      </div>

      {/* Navigation Menus with Scroll */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '0.75rem 0.75rem'
      }}>
        {navigationSections.map((sec, idx) => (
          <div key={idx} style={{ marginBottom: '1.125rem' }}>
            <div style={{
              fontSize: '0.6875rem',
              fontWeight: 700,
              color: 'var(--color-muted)',
              padding: '0.25rem 0.625rem',
              letterSpacing: '0.05em'
            }}>
              {sec.title}
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem', marginTop: '0.25rem' }}>
              {sec.items.map((item) => {
                const Icon = item.icon;
                const isActive = currentTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => onSelectTab(item.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      width: '100%',
                      padding: '0.5rem 0.625rem',
                      borderRadius: '0.5rem',
                      border: 'none',
                      backgroundColor: isActive ? 'var(--color-sage)' : 'transparent',
                      color: isActive ? 'var(--color-forest)' : 'var(--color-charcoal)',
                      fontWeight: isActive ? 700 : 500,
                      fontSize: '0.8125rem',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.15s ease'
                    }}
                    onMouseEnter={(e) => {
                      if (!isActive) e.currentTarget.style.backgroundColor = 'var(--color-sage-light)';
                    }}
                    onMouseLeave={(e) => {
                      if (!isActive) e.currentTarget.style.backgroundColor = 'transparent';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
                      <Icon size={16} color={isActive ? 'var(--color-forest)' : '#6B7280'} />
                      <span>{item.label}</span>
                    </div>

                    {item.badge && (
                      <span className={item.badge === 'Solver' ? 'badge badge-gold' : 'badge badge-success'} style={{ fontSize: '0.625rem', padding: '0.125rem 0.375rem' }}>
                        {item.badge}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}

        {/* Demo Fast Role Switcher Box for Reviewers */}
        <div style={{
          backgroundColor: '#F8FAF7',
          border: '1px dashed var(--color-border)',
          borderRadius: '0.625rem',
          padding: '0.75rem',
          margin: '0.5rem 0 1rem 0'
        }}>
          <div style={{ fontSize: '0.6875rem', fontWeight: 700, color: 'var(--color-forest)', marginBottom: '0.5rem' }}>
            DEMO ROLE SIMULATOR
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.375rem' }}>
            <button
              onClick={() => handleQuickSwitch('Admin', 'admin', 'admin123')}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.6875rem', padding: '0.25rem' }}
            >
              Admin
            </button>
            <button
              onClick={() => handleQuickSwitch('Staff', 'examstaff', 'staff123')}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.6875rem', padding: '0.25rem' }}
            >
              Staff
            </button>
            <button
              onClick={() => handleQuickSwitch('Faculty', 'prof.sharma', 'faculty123')}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.6875rem', padding: '0.25rem' }}
            >
              Faculty
            </button>
            <button
              onClick={() => handleQuickSwitch('Student', 'student.24cs101', 'student123')}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.6875rem', padding: '0.25rem' }}
            >
              Student
            </button>
          </div>
        </div>
      </div>

      {/* User Footer Profile */}
      <div style={{
        padding: '0.875rem 1rem',
        borderTop: '1px solid var(--color-border-light)',
        backgroundColor: '#FFFFFF',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', overflow: 'hidden' }}>
          <div style={{
            width: '2rem',
            height: '2rem',
            borderRadius: '9999px',
            backgroundColor: 'var(--color-sage)',
            color: 'var(--color-forest)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 700,
            fontSize: '0.8125rem'
          }}>
            {user?.first_name ? user.first_name[0] : (user?.username ? user.username[0].toUpperCase() : 'U')}
          </div>
          <div style={{ overflow: 'hidden' }}>
            <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--color-charcoal)', textOverflow: 'ellipsis', whiteSpace: 'nowrap', overflow: 'hidden' }}>
              {user ? (user.first_name ? `${user.first_name} ${user.last_name || ''}` : user.username) : 'Guest User'}
            </div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--color-muted)' }}>
              {user?.role || 'Read Only'}
            </div>
          </div>
        </div>

        <button
          onClick={logout}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--color-muted)',
            cursor: 'pointer',
            padding: '0.375rem',
            borderRadius: '0.375rem'
          }}
          title="Sign Out"
          onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--color-error)')}
          onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--color-muted)')}
        >
          <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
}
