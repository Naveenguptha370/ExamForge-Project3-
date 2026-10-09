/** ExamForge M2 — Top Header */
import { useLocation } from 'react-router-dom'
import {
  HiOutlineMenuAlt2, HiOutlineBell, HiOutlineLogout,
  HiOutlineSearch,
} from 'react-icons/hi'
import { useAuth } from '../../context/AuthContext.jsx'

const PAGE_TITLES = {
  '/students': 'Student Dashboard',
  '/students/list': 'All Students',
  '/students/add': 'Add Student',
  '/students/import': 'Bulk Import',
  '/students/enrollments': 'Enrollments',
  '/academics': 'Academic Dashboard',
  '/academics/departments': 'Departments',
  '/academics/courses': 'Courses',
  '/academics/branches': 'Branches',
  '/academics/semesters': 'Semesters',
  '/academics/years': 'Academic Years',
  '/academics/subjects': 'Subjects',
  '/academics/structure': 'Academic Structure',
  '/registrations': 'Registration Dashboard',
  '/registrations/subjects/available': 'Available Subjects',
  '/registrations/subjects/register': 'Subject Registration',
  '/registrations/exams/register': 'Exam Registration',
  '/registrations/list': 'All Registrations',
  '/registrations/bulk': 'Bulk Registration',
  '/registrations/history': 'Registration History',
  '/registrations/reports': 'Registration Reports',
}

export default function Header({ onMobileMenuClick }) {
  const { user, logout } = useAuth()
  const location = useLocation()
  const title = PAGE_TITLES[location.pathname] || 'ExamForge'

  return (
    <header style={{
      position: 'fixed', top: 0, left: 0, right: 0,
      height: 'var(--header-height)',
      background: 'rgba(250,249,246,0.92)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--color-border)',
      display: 'flex', alignItems: 'center',
      padding: '0 var(--space-6)',
      zIndex: 'var(--z-header)',
      gap: 'var(--space-4)',
    }}>
      {/* Mobile menu button */}
      <button
        onClick={onMobileMenuClick}
        className="btn btn-icon btn-secondary"
        style={{ display: 'none' }}
      >
        <HiOutlineMenuAlt2 size={20} />
      </button>

      {/* Page title */}
      <div style={{ flex: 1 }}>
        <h1 style={{
          fontSize: '1rem', fontWeight: 700,
          color: 'var(--color-charcoal)', margin: 0,
        }}>
          {title}
        </h1>
        <div style={{ fontSize: '0.75rem', color: 'var(--color-gray)' }}>
          ExamForge · Examination Operations System
        </div>
      </div>

      {/* Right actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        {/* Notification bell */}
        <button
          className="btn btn-icon btn-secondary"
          title="Notifications"
          style={{ position: 'relative' }}
        >
          <HiOutlineBell size={18} />
          <span style={{
            position: 'absolute', top: 6, right: 6,
            width: 7, height: 7, borderRadius: '50%',
            background: 'var(--color-amber)',
            border: '1.5px solid var(--color-white)',
          }} />
        </button>

        {/* User chip */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          padding: '6px 12px', borderRadius: 'var(--radius-full)',
          background: 'var(--color-white)',
          border: '1px solid var(--color-border)',
          boxShadow: 'var(--shadow-sm)',
        }}>
          <div style={{
            width: 28, height: 28, borderRadius: '50%',
            background: 'linear-gradient(135deg, var(--color-forest), var(--color-emerald))',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'white', fontWeight: 700, fontSize: '0.75rem',
          }}>
            {user?.first_name?.[0] || 'U'}
          </div>
          <div style={{ lineHeight: 1.3 }}>
            <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>
              {user?.first_name || user?.username || 'User'}
            </div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--color-gray)', textTransform: 'capitalize' }}>
              {user?.role || 'guest'}
            </div>
          </div>
        </div>

        {/* Logout */}
        <button
          onClick={logout}
          className="btn btn-icon btn-secondary"
          title="Sign out"
        >
          <HiOutlineLogout size={18} />
        </button>
      </div>
    </header>
  )
}
