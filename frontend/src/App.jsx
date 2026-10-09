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
}
