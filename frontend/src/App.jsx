<<<<<<< HEAD
import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import UsersPage from './pages/UsersPage';
import FacultyPage from './pages/FacultyPage';
import AcademicsPage from './pages/AcademicsPage';
import StudentsPage from './pages/StudentsPage';
import RegistrationsPage from './pages/RegistrationsPage';
import ExamSessionsPage from './pages/ExamSessionsPage';
import TimetablePage from './pages/TimetablePage';
import RoomsPage from './pages/RoomsPage';
import SeatingPlanPage from './pages/SeatingPlanPage';
import InvigilationPage from './pages/InvigilationPage';
import HallTicketsPage from './pages/HallTicketsPage';
import AttendancePage from './pages/AttendancePage';
import NotificationsPage from './pages/NotificationsPage';
import ReportsPage from './pages/ReportsPage';
import AuditLogsPage from './pages/AuditLogsPage';
import SettingsPage from './pages/SettingsPage';

import Sidebar from './components/Sidebar';
import Header from './components/Header';

function MainApp() {
  const { user, loading } = useAuth();
  const [currentView, setCurrentView] = useState('landing'); // 'landing' | 'login' | 'app'
  const [activeTab, setActiveTab] = useState('dashboard');

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--color-ivory)' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ width: '40px', height: '40px', border: '3px solid var(--color-sage)', borderTopColor: 'var(--color-forest)', borderRadius: '50%', animation: 'spin 0.8s linear infinite', margin: '0 auto 1rem auto' }} />
          <div style={{ fontWeight: 700, color: 'var(--color-forest)' }}>Loading ExamForge Engine...</div>
        </div>
        <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  // Public Landing Page
  if (currentView === 'landing') {
    return (
      <LandingPage
        onNavigate={(view) => {
          if (view === 'dashboard') {
            setCurrentView('app');
            setActiveTab('dashboard');
          } else {
            setCurrentView(view);
          }
        }}
      />
    );
  }

  // Login Page
  if (currentView === 'login') {
    return (
      <LoginPage
        onNavigate={(view) => {
          if (view === 'dashboard') {
            setCurrentView('app');
            setActiveTab('dashboard');
          } else {
            setCurrentView(view);
          }
        }}
      />
    );
  }

  // Authenticated Application Shell
  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard': return <DashboardPage onSelectTab={setActiveTab} />;
      case 'users': return <UsersPage />;
      case 'faculty': return <FacultyPage />;
      case 'academics': return <AcademicsPage />;
      case 'students': return <StudentsPage />;
      case 'registrations': return <RegistrationsPage />;
      case 'sessions': return <ExamSessionsPage />;
      case 'timetable': return <TimetablePage />;
      case 'rooms': return <RoomsPage />;
      case 'seating': return <SeatingPlanPage />;
      case 'invigilation': return <InvigilationPage />;
      case 'halltickets': return <HallTicketsPage />;
      case 'attendance': return <AttendancePage />;
      case 'notifications': return <NotificationsPage />;
      case 'reports': return <ReportsPage />;
      case 'audit': return <AuditLogsPage />;
      case 'settings': return <SettingsPage />;
      default: return <DashboardPage onSelectTab={setActiveTab} />;
    }
  };

  const pageHeaders = {
    dashboard: { title: 'Overview Dashboard', sub: 'Central Operations Command' },
    users: { title: 'User Management', sub: 'Member 1 Subsystem' },
    faculty: { title: 'Faculty & Invigilators', sub: 'Member 1 Subsystem' },
    academics: { title: 'Academic Curriculum', sub: 'Member 2 Subsystem' },
    students: { title: 'Student Registry', sub: 'Member 2 Subsystem' },
    registrations: { title: 'Exam Registrations', sub: 'Member 2 Subsystem' },
    sessions: { title: 'Exam Sessions', sub: 'Member 3 Subsystem' },
    timetable: { title: 'Timetable Constraint Solver', sub: 'Member 3 Subsystem' },
    rooms: { title: 'Rooms & Halls', sub: 'Member 4 Subsystem' },
    seating: { title: 'Visual Seating Grid', sub: 'Member 4 Subsystem' },
    invigilation: { title: 'Invigilation Roster', sub: 'Member 4 Subsystem' },
    halltickets: { title: 'Hall Tickets & PDFs', sub: 'Member 5 Subsystem' },
    attendance: { title: 'Hall Attendance', sub: 'Member 5 Subsystem' },
    notifications: { title: 'Notifications Center', sub: 'Member 5 Subsystem' },
    reports: { title: 'Reports & Analytics', sub: 'Member 5 Subsystem' },
    audit: { title: 'System Audit Logs', sub: 'Member 5 Subsystem' },
    settings: { title: 'Institutional Settings', sub: 'Member 5 Subsystem' },
  };

  const currentHeader = pageHeaders[activeTab] || { title: 'ExamForge Console', sub: '' };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: 'var(--color-ivory)' }}>
      <Sidebar
        currentTab={activeTab}
        onSelectTab={setActiveTab}
        onNavigateLanding={() => setCurrentView('landing')}
      />

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <Header
          title={currentHeader.title}
          subtitle={currentHeader.sub}
          onNavigateLanding={() => setCurrentView('landing')}
        />

        <main style={{ flex: 1, overflowY: 'auto' }}>
          {renderTabContent()}
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
=======
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext.jsx'
import { useAuth } from './context/AuthContext.jsx'

// Layout
import AppLayout from './components/shared/Layout.jsx'

// Student Pages
import StudentDashboard   from './pages/students/StudentDashboard.jsx'
import StudentList        from './pages/students/StudentList.jsx'
import AddStudent         from './pages/students/AddStudent.jsx'
import EditStudent        from './pages/students/EditStudent.jsx'
import StudentDetails     from './pages/students/StudentDetails.jsx'
import BulkImport         from './pages/students/BulkImport.jsx'
import EnrollmentOverview from './pages/students/EnrollmentOverview.jsx'

// Academic Pages
import AcademicDashboard        from './pages/academics/AcademicDashboard.jsx'
import DepartmentManagement     from './pages/academics/DepartmentManagement.jsx'
import CourseManagement         from './pages/academics/CourseManagement.jsx'
import BranchManagement         from './pages/academics/BranchManagement.jsx'
import SemesterManagement       from './pages/academics/SemesterManagement.jsx'
import AcademicYearManagement   from './pages/academics/AcademicYearManagement.jsx'
import SubjectManagement        from './pages/academics/SubjectManagement.jsx'
import AcademicStructure        from './pages/academics/AcademicStructureOverview.jsx'

// Registration Pages
import RegistrationDashboard    from './pages/registrations/RegistrationDashboard.jsx'
import AvailableSubjects        from './pages/registrations/AvailableSubjects.jsx'
import SubjectRegistration      from './pages/registrations/SubjectRegistration.jsx'
import ExamRegistration         from './pages/registrations/ExamRegistration.jsx'
import RegistrationList         from './pages/registrations/RegistrationList.jsx'
import RegistrationDetails      from './pages/registrations/RegistrationDetails.jsx'
import BulkRegistrationPage     from './pages/registrations/BulkRegistrationPage.jsx'
import RegistrationHistory      from './pages/registrations/RegistrationHistory.jsx'
import RegistrationReports      from './pages/registrations/RegistrationReports.jsx'

// Auth placeholder (M1 provides real auth)
import LoginPlaceholder from './pages/LoginPlaceholder.jsx'
import NotFound         from './pages/NotFound.jsx'
import AccessDenied     from './pages/AccessDenied.jsx'

/* ── Protected route wrapper ──────────────────────────────── */
function ProtectedRoute({ children, roles = [] }) {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div style={{ display:'flex', alignItems:'center', justifyContent:'center', minHeight:'100vh' }}>
        <div className="skeleton" style={{ width:48, height:48, borderRadius:'50%' }} />
      </div>
    )
  }

  if (!user) return <Navigate to="/login" replace />

  if (roles.length > 0 && !roles.includes(user.role)) {
    return <Navigate to="/access-denied" replace />
  }

  return children
}

/* ── App Root ─────────────────────────────────────────────── */
export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public */}
          <Route path="/login" element={<LoginPlaceholder />} />
          <Route path="/access-denied" element={<AccessDenied />} />

          {/* Protected — M2 modules inside AppLayout */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            {/* Default redirect */}
            <Route index element={<Navigate to="/students" replace />} />

            {/* ── Student Management ───────────────────────── */}
            <Route path="students">
              <Route index element={<StudentDashboard />} />
              <Route path="list" element={<StudentList />} />
              <Route path="add" element={
                <ProtectedRoute roles={['admin','exam_staff']}>
                  <AddStudent />
                </ProtectedRoute>
              } />
              <Route path=":id" element={<StudentDetails />} />
              <Route path=":id/edit" element={
                <ProtectedRoute roles={['admin','exam_staff']}>
                  <EditStudent />
                </ProtectedRoute>
              } />
              <Route path="import" element={
                <ProtectedRoute roles={['admin']}>
                  <BulkImport />
                </ProtectedRoute>
              } />
              <Route path="enrollments" element={<EnrollmentOverview />} />
            </Route>

            {/* ── Academic Management ──────────────────────── */}
            <Route path="academics">
              <Route index element={<AcademicDashboard />} />
              <Route path="departments" element={<DepartmentManagement />} />
              <Route path="courses" element={<CourseManagement />} />
              <Route path="branches" element={<BranchManagement />} />
              <Route path="semesters" element={<SemesterManagement />} />
              <Route path="years" element={<AcademicYearManagement />} />
              <Route path="subjects" element={<SubjectManagement />} />
              <Route path="structure" element={<AcademicStructure />} />
            </Route>

            {/* ── Subject & Exam Registration ──────────────── */}
            <Route path="registrations">
              <Route index element={<RegistrationDashboard />} />
              <Route path="subjects/available" element={<AvailableSubjects />} />
              <Route path="subjects/register" element={
                <ProtectedRoute roles={['admin','exam_staff']}>
                  <SubjectRegistration />
                </ProtectedRoute>
              } />
              <Route path="exams/register" element={
                <ProtectedRoute roles={['admin','exam_staff']}>
                  <ExamRegistration />
                </ProtectedRoute>
              } />
              <Route path="list" element={<RegistrationList />} />
              <Route path=":id" element={<RegistrationDetails />} />
              <Route path="bulk" element={
                <ProtectedRoute roles={['admin','exam_staff']}>
                  <BulkRegistrationPage />
                </ProtectedRoute>
              } />
              <Route path="history" element={<RegistrationHistory />} />
              <Route path="reports" element={
                <ProtectedRoute roles={['admin','exam_staff']}>
                  <RegistrationReports />
                </ProtectedRoute>
              } />
            </Route>
          </Route>

          {/* 404 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
>>>>>>> origin/member1-work
}
