/**
 * ExamForge M2 — Sidebar Navigation
 * Premium collapsible sidebar with ExamForge branding.
 * Green & ivory design — absolutely no blue.
 */

import { NavLink, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  HiOutlineHome,
  HiOutlineUsers,
  HiOutlineUserAdd,
  HiOutlineClipboardList,
  HiOutlineUpload,
  HiOutlineAcademicCap,
  HiOutlineOfficeBuilding,
  HiOutlineBookOpen,
  HiOutlineTemplate,
  HiOutlineCalendar,
  HiOutlineCollection,
  HiOutlinePencilAlt,
  HiOutlineClipboardCheck,
  HiOutlineDocumentReport,
  HiOutlineChevronDown,
  HiOutlineChevronLeft,
  HiOutlineChevronRight,
  HiOutlineMenuAlt2,
} from 'react-icons/hi'
import { useState } from 'react'
import { useAuth } from '../../context/AuthContext.jsx'

/* ── Nav sections ─────────────────────────────────────────── */
const NAV_SECTIONS = [
  {
    title: 'Students',
    icon: HiOutlineUsers,
    basePath: '/students',
    links: [
      { label: 'Dashboard',    to: '/students',            icon: HiOutlineHome },
      { label: 'All Students', to: '/students/list',       icon: HiOutlineUsers },
      { label: 'Add Student',  to: '/students/add',        icon: HiOutlineUserAdd, adminOnly: true },
      { label: 'Bulk Import',  to: '/students/import',     icon: HiOutlineUpload, adminOnly: true },
      { label: 'Enrollments',  to: '/students/enrollments',icon: HiOutlineClipboardList },
    ],
  },
  {
    title: 'Academics',
    icon: HiOutlineAcademicCap,
    basePath: '/academics',
    links: [
      { label: 'Overview',      to: '/academics',            icon: HiOutlineHome },
      { label: 'Departments',   to: '/academics/departments',icon: HiOutlineOfficeBuilding },
      { label: 'Courses',       to: '/academics/courses',    icon: HiOutlineBookOpen },
      { label: 'Branches',      to: '/academics/branches',   icon: HiOutlineTemplate },
      { label: 'Semesters',     to: '/academics/semesters',  icon: HiOutlineCalendar },
      { label: 'Academic Years',to: '/academics/years',      icon: HiOutlineCollection },
      { label: 'Subjects',      to: '/academics/subjects',   icon: HiOutlineBookOpen },
      { label: 'Structure',     to: '/academics/structure',  icon: HiOutlineTemplate },
    ],
  },
  {
    title: 'Registrations',
    icon: HiOutlinePencilAlt,
    basePath: '/registrations',
    links: [
      { label: 'Dashboard',      to: '/registrations',                 icon: HiOutlineHome },
      { label: 'Available Subj.',to: '/registrations/subjects/available',icon: HiOutlineBookOpen },
      { label: 'Subject Reg.',   to: '/registrations/subjects/register',icon: HiOutlineClipboardCheck, staffOnly: true },
      { label: 'Exam Reg.',      to: '/registrations/exams/register',  icon: HiOutlinePencilAlt, staffOnly: true },
      { label: 'All Registrations',to: '/registrations/list',          icon: HiOutlineClipboardList },
      { label: 'Bulk Register',  to: '/registrations/bulk',            icon: HiOutlineUpload, staffOnly: true },
      { label: 'History',        to: '/registrations/history',         icon: HiOutlineCalendar },
      { label: 'Reports',        to: '/registrations/reports',         icon: HiOutlineDocumentReport, staffOnly: true },
    ],
  },
]

/* ── Section group ────────────────────────────────────────── */
function NavSection({ section, collapsed, isAdmin, isExamStaff }) {
  const location = useLocation()
  const isActive = location.pathname.startsWith(section.basePath)
  const [open, setOpen] = useState(isActive)
  const Icon = section.icon

  const visibleLinks = section.links.filter(l => {
    if (l.adminOnly && !isAdmin) return false
    if (l.staffOnly && !isAdmin && !isExamStaff) return false
    return true
  })

  if (collapsed) {
    return (
      <div style={{ marginBottom: 4 }}>
        <div
          title={section.title}
          style={{
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            padding: '10px', borderRadius: 10,
            background: isActive ? 'var(--color-sage)' : 'transparent',
            color: isActive ? 'var(--color-emerald)' : 'var(--color-gray)',
            cursor: 'pointer', transition: 'all 0.15s',
          }}
        >
          <Icon size={22} />
        </div>
      </div>
    )
  }

  return (
    <div style={{ marginBottom: 4 }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          width: '100%', display: 'flex', alignItems: 'center',
          gap: 10, padding: '9px 12px', borderRadius: 10,
          background: isActive ? 'var(--color-sage)' : 'transparent',
          color: isActive ? 'var(--color-forest)' : 'var(--color-gray)',
          fontSize: '0.875rem', fontWeight: 600, cursor: 'pointer',
          border: 'none', transition: 'all 0.15s', fontFamily: 'var(--font-sans)',
        }}
        onMouseEnter={e => {
          if (!isActive) e.currentTarget.style.background = 'var(--color-sage-light)'
        }}
        onMouseLeave={e => {
          if (!isActive) e.currentTarget.style.background = 'transparent'
        }}
      >
        <Icon size={18} style={{ flexShrink: 0 }} />
        <span style={{ flex: 1, textAlign: 'left' }}>{section.title}</span>
        <HiOutlineChevronDown
          size={14}
          style={{
            transform: open ? 'rotate(180deg)' : 'rotate(0)',
            transition: 'transform 0.2s',
          }}
        />
      </button>

      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: 'easeInOut' }}
            style={{ overflow: 'hidden' }}
          >
            <div style={{ paddingLeft: 12, paddingTop: 2 }}>
              {visibleLinks.map(link => (
                <NavLink
                  key={link.to}
                  to={link.to}
                  end={link.to === section.basePath}
                  style={({ isActive: active }) => ({
                    display: 'flex', alignItems: 'center', gap: 8,
                    padding: '7px 10px', borderRadius: 8,
                    fontSize: '0.8125rem', fontWeight: active ? 600 : 400,
                    color: active ? 'var(--color-emerald)' : 'var(--color-gray)',
                    background: active ? 'rgba(21,128,61,0.08)' : 'transparent',
                    marginBottom: 1, textDecoration: 'none', transition: 'all 0.12s',
                    borderLeft: active ? '2px solid var(--color-emerald)' : '2px solid transparent',
                  })}
                  onMouseEnter={e => { e.currentTarget.style.color = 'var(--color-emerald)' }}
                  onMouseLeave={e => {}}
                >
                  <link.icon size={15} style={{ flexShrink: 0 }} />
                  {link.label}
                </NavLink>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

/* ── Main Sidebar ─────────────────────────────────────────── */
export default function Sidebar({ isOpen, onToggle, isMobileOpen, onMobileClose }) {
  const { user, isAdmin, isExamStaff } = useAuth()

  const sidebarStyle = {
    position: 'fixed', top: 0, left: 0, bottom: 0,
    width: isOpen ? 'var(--sidebar-width)' : 'var(--sidebar-collapsed)',
    background: 'var(--color-white)',
    borderRight: '1px solid var(--color-border)',
    display: 'flex', flexDirection: 'column',
    zIndex: 'var(--z-sidebar)',
    transition: 'width 0.25s ease',
    overflowX: 'hidden',
    boxShadow: '2px 0 12px rgba(36,41,35,0.05)',
  }

  return (
    <>
      {/* Desktop */}
      <aside style={sidebarStyle}>
        {/* Logo */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 10,
          padding: isOpen ? '20px 16px 16px' : '20px 14px 16px',
          borderBottom: '1px solid var(--color-border)',
          minHeight: 'var(--header-height)',
        }}>
          <div style={{
            width: 38, height: 38, borderRadius: 10, flexShrink: 0,
            background: 'linear-gradient(135deg, var(--color-forest), var(--color-emerald))',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'white', fontWeight: 800, fontSize: '1rem',
            boxShadow: 'var(--shadow-green)',
          }}>
            EF
          </div>
          <AnimatePresence>
            {isOpen && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                transition={{ duration: 0.15 }}
                style={{ overflow: 'hidden', whiteSpace: 'nowrap' }}
              >
                <div style={{
                  fontFamily: 'var(--font-display)', fontWeight: 800,
                  fontSize: '0.9375rem', color: 'var(--color-forest)', lineHeight: 1.2,
                }}>
                  ExamForge
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--color-gray)', fontWeight: 500 }}>
                  M2 · Student & Academic
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Nav */}
        <nav style={{ flex: 1, overflowY: 'auto', padding: '12px 8px' }}>
          {NAV_SECTIONS.map(section => (
            <NavSection
              key={section.title}
              section={section}
              collapsed={!isOpen}
              isAdmin={isAdmin}
              isExamStaff={isExamStaff}
            />
          ))}
        </nav>

        {/* User Footer */}
        <div style={{
          padding: isOpen ? '12px 16px' : '12px 8px',
          borderTop: '1px solid var(--color-border)',
        }}>
          <div style={{
            display: 'flex', alignItems: 'center', gap: 10,
            padding: '8px 10px', borderRadius: 10,
            background: 'var(--color-sage-light)',
          }}>
            <div style={{
              width: 32, height: 32, borderRadius: '50%', flexShrink: 0,
              background: 'var(--color-emerald)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              color: 'white', fontWeight: 700, fontSize: '0.8125rem',
            }}>
              {user?.first_name?.[0] || user?.username?.[0] || 'U'}
            </div>
            <AnimatePresence>
              {isOpen && (
                <motion.div
                  initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  style={{ overflow: 'hidden', minWidth: 0 }}
                >
                  <div style={{
                    fontSize: '0.8125rem', fontWeight: 600,
                    color: 'var(--color-charcoal)', overflow: 'hidden',
                    textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                  }}>
                    {user?.first_name || user?.username || 'User'}
                  </div>
                  <div style={{
                    fontSize: '0.7rem', color: 'var(--color-gray)',
                    textTransform: 'capitalize',
                  }}>
                    {user?.role || 'Guest'}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Toggle button */}
        <button
          onClick={onToggle}
          title={isOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          style={{
            position: 'absolute', top: 72, right: -14,
            width: 28, height: 28, borderRadius: '50%',
            background: 'var(--color-white)', border: '1.5px solid var(--color-border)',
            boxShadow: 'var(--shadow-md)', color: 'var(--color-gray)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            cursor: 'pointer', zIndex: 10, transition: 'all 0.15s',
          }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--color-emerald)'; e.currentTarget.style.color = 'var(--color-emerald)' }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--color-border)'; e.currentTarget.style.color = 'var(--color-gray)' }}
        >
          {isOpen ? <HiOutlineChevronLeft size={14} /> : <HiOutlineChevronRight size={14} />}
        </button>
      </aside>
    </>
  )
}
