import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
import { AppLayout } from './components/AppLayout';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { TimetableStudioPage } from './pages/TimetableStudioPage';
import { ExamSessionsPage } from './pages/ExamSessionsPage';
import { TimeSlotsPage } from './pages/TimeSlotsPage';
import { SubjectConfigPage } from './pages/SubjectConfigPage';
import { ConflictRadarPage } from './pages/ConflictRadarPage';
import { TimetableViewPage } from './pages/TimetableViewPage';
import { AcademicsPage } from './pages/AcademicsPage';
import { StudentsPage } from './pages/StudentsPage';
import { FacultyPage } from './pages/FacultyPage';
import { RoomsPage } from './pages/RoomsPage';
import { SeatingPage } from './pages/SeatingPage';
import { InvigilationPage } from './pages/InvigilationPage';
import { HallTicketsPage } from './pages/HallTicketsPage';
import { AttendancePage } from './pages/AttendancePage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { NotificationsPage } from './pages/NotificationsPage';
import { AuditSettingsPage } from './pages/AuditSettingsPage';
import { LoginPage } from './pages/LoginPage';

const MainRouter = () => {
  const [activeTab, setActiveTab] = useState('landing');
  const { user } = useAuth();

  if (activeTab === 'landing') {
    return (
      <LandingPage
        onGetStarted={() => setActiveTab('timetable_studio')}
        onLogin={() => setActiveTab('login')}
      />
    );
  }

  if (activeTab === 'login') {
    return (
      <LoginPage
        onLoginSuccess={() => setActiveTab('dashboard')}
        onBackToLanding={() => setActiveTab('landing')}
      />
    );
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardPage onNavigate={setActiveTab} />;
      case 'timetable_studio':
        return <TimetableStudioPage />;
      case 'exam_sessions':
        return <ExamSessionsPage />;
      case 'time_slots':
        return <TimeSlotsPage />;
      case 'subject_config':
        return <SubjectConfigPage />;
      case 'conflict_radar':
        return <ConflictRadarPage />;
      case 'timetable_view':
        return <TimetableViewPage />;
      case 'academics':
        return <AcademicsPage />;
      case 'students':
        return <StudentsPage />;
      case 'faculty':
        return <FacultyPage />;
      case 'rooms':
        return <RoomsPage />;
      case 'seating':
        return <SeatingPage />;
      case 'invigilation':
        return <InvigilationPage />;
      case 'halltickets':
        return <HallTicketsPage />;
      case 'attendance':
        return <AttendancePage />;
      case 'analytics':
        return <AnalyticsPage />;
      case 'notifications':
        return <NotificationsPage />;
      case 'audit':
        return <AuditSettingsPage />;
      default:
        return <DashboardPage onNavigate={setActiveTab} />;
    }
  };

  return (
    <AppLayout activeTab={activeTab} onSelectTab={setActiveTab}>
      {renderContent()}
    </AppLayout>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <MainRouter />
      </ToastProvider>
    </AuthProvider>
  );
}
