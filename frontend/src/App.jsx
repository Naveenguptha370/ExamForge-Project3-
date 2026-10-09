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
}
