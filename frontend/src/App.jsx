import { useEffect, useState } from 'react'
import './App.css'

const API_BASE = 'http://localhost:8000/api'

const defaultStats = {
  totalUsers: 128,
  activeUsers: 116,
  inactiveUsers: 12,
  facultyUsers: 48,
  availableFaculty: 41,
  incompleteProfiles: 6,
}

const defaultUsers = [
  { id: 1, username: 'admin', email: 'admin@examforge.edu', role: 'ADMIN', status: 'ACTIVE' },
  { id: 2, username: 'n.kapoor', email: 'n.kapoor@examforge.edu', role: 'FACULTY', status: 'ACTIVE' },
  { id: 3, username: 'a.rao', email: 'a.rao@examforge.edu', role: 'EXAM_STAFF', status: 'ACTIVE' },
  { id: 4, username: 'r.sharma', email: 'r.sharma@examforge.edu', role: 'STUDENT', status: 'ACTIVE' },
]

const defaultFaculty = [
  { id: 1, faculty_id: 'FAC-101', user_name: 'Neeraj Kapoor', department: 'Computer Science', designation: 'Professor', status: 'ACTIVE', email: 'n.kapoor@examforge.edu', phone: '9876543210' },
  { id: 2, faculty_id: 'FAC-205', user_name: 'Meera Sen', department: 'Mathematics', designation: 'Associate Professor', status: 'ACTIVE', email: 'm.sen@examforge.edu', phone: '9876543211' },
  { id: 3, faculty_id: 'FAC-310', user_name: 'Amit Verma', department: 'Electronics', designation: 'Assistant Professor', status: 'ON_LEAVE', email: 'a.verma@examforge.edu', phone: '9876543212' },
]

const roleOptions = ['ADMIN', 'FACULTY', 'EXAM_STAFF', 'STUDENT']

function getCookie(name) {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`))
  return match ? decodeURIComponent(match[1]) : ''
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState(null)
  const [stats, setStats] = useState(defaultStats)
  const [users, setUsers] = useState(defaultUsers)
  const [faculty, setFaculty] = useState(defaultFaculty)
  const [loginForm, setLoginForm] = useState({ username: 'admin', password: 'Admin@123' })
  const [facultyForm, setFacultyForm] = useState({ faculty_id: 'FAC-401', user: '', department: 'Civil Engineering', designation: 'Professor', status: 'ACTIVE', email: 'p.mehta@examforge.edu', phone: '9876543219', qualification: 'Ph.D.', specialization: 'Structural Analysis' })
  const [message, setMessage] = useState('Ready to manage examinations securely.')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    checkSession()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const checkSession = async () => {
    try {
      const response = await fetch(`${API_BASE}/auth/me/`, { credentials: 'include' })
      if (response.status === 401 || response.status === 403) {
        return
      }
      if (response.ok) {
        const currentUser = await response.json()
        setUser(currentUser)
        setIsLoggedIn(true)
        await refreshDashboard()
      }
    } catch (error) {
      console.info('No active backend session yet.', error)
    }
  }

  const refreshDashboard = async () => {
    try {
      const [userResponse, statsResponse, facultyListResponse, facultyDashboardResponse] = await Promise.all([
        fetch(`${API_BASE}/auth/users/`, { credentials: 'include' }),
        fetch(`${API_BASE}/auth/dashboard/`, { credentials: 'include' }),
        fetch(`${API_BASE}/faculty/profiles/`, { credentials: 'include' }),
        fetch(`${API_BASE}/faculty/dashboard/`, { credentials: 'include' }),
      ])

      if (userResponse.ok) {
        const userData = await userResponse.json()
        setUsers(userData.results ?? userData)
      }

      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setStats({
          totalUsers: statsData.total_users ?? defaultStats.totalUsers,
          activeUsers: statsData.active_users ?? defaultStats.activeUsers,
          inactiveUsers: statsData.inactive_users ?? defaultStats.inactiveUsers,
          facultyUsers: statsData.faculty_users ?? defaultStats.facultyUsers,
          availableFaculty: statsData.available_faculty ?? defaultStats.availableFaculty,
          incompleteProfiles: statsData.incomplete_profiles ?? defaultStats.incompleteProfiles,
        })
      }

      if (facultyListResponse.ok) {
        const facultyData = await facultyListResponse.json()
        setFaculty(Array.isArray(facultyData) ? facultyData : facultyData.results ?? defaultFaculty)
      }

      if (facultyDashboardResponse.ok) {
        const facultyStats = await facultyDashboardResponse.json()
        setStats((current) => ({
          ...current,
          incompleteProfiles: facultyStats.incomplete_profiles ?? current.incompleteProfiles,
          availableFaculty: facultyStats.available_faculty ?? current.availableFaculty,
        }))
      }
    } catch (error) {
      console.info('Using demo dashboard data.', error)
    }
  }

  const handleLogin = async (event) => {
    event.preventDefault()
    setLoading(true)
    setMessage('Authenticating user session...')

    try {
      const csrfToken = getCookie('csrftoken')
      const response = await fetch(`${API_BASE}/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}),
        },
        credentials: 'include',
        body: JSON.stringify(loginForm),
      })

      const contentType = response.headers.get('content-type') || ''
      const data = contentType.includes('application/json') ? await response.json() : null

      if (!response.ok) {
        throw new Error(data?.detail || data?.non_field_errors?.[0] || 'Login failed')
      }

      setUser(data)
      setIsLoggedIn(true)
      setMessage(`Welcome back, ${data.first_name || data.username}.`)
      await refreshDashboard()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      const csrfToken = getCookie('csrftoken')
      await fetch(`${API_BASE}/auth/logout/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}) },
        credentials: 'include',
      })
    } catch (error) {
      console.warn('Logout call failed cleanly.', error)
    }

    setIsLoggedIn(false)
    setUser(null)
    setMessage('Session closed securely.')
  }

  const handleFacultyCreate = async (event) => {
    event.preventDefault()
    setLoading(true)
    setMessage('Saving faculty profile...')

    try {
      const csrfToken = getCookie('csrftoken')
      const response = await fetch(`${API_BASE}/faculty/profiles/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}),
        },
        credentials: 'include',
        body: JSON.stringify({
          ...facultyForm,
          user: facultyForm.user || 1,
        }),
      })

      if (!response.ok) {
        const data = await response.json().catch(() => ({}))
        throw new Error(data.detail || 'Faculty profile creation failed')
      }

      setMessage(`Faculty profile ${facultyForm.faculty_id} created successfully.`)
      setFacultyForm({
        faculty_id: 'FAC-402',
        user: '',
        department: 'Computer Science',
        designation: 'Assistant Professor',
        status: 'ACTIVE',
        email: 's.nair@examforge.edu',
        phone: '9876543220',
        qualification: 'M.Tech.',
        specialization: 'Database Systems',
      })
      await refreshDashboard()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  const summaryCards = [
    { label: 'Total users', value: stats.totalUsers, accent: 'forest' },
    { label: 'Active accounts', value: stats.activeUsers, accent: 'green' },
    { label: 'Faculty members', value: stats.facultyUsers, accent: 'amber' },
    { label: 'Available faculty', value: stats.availableFaculty, accent: 'gold' },
  ]

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-wrap">
          <div className="brand-mark">E</div>
          <div>
            <p className="eyebrow">Examination Operations System</p>
            <h1>ExamForge</h1>
          </div>
        </div>
        <nav className="nav">
          <a href="#overview">Overview</a>
          <a href="#security">Security</a>
          <a href="#faculty">Faculty</a>
          <a href="#audit">Audit</a>
        </nav>
        {isLoggedIn ? (
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        ) : (
          <span className="status-pill">Protected access</span>
        )}
      </header>

      <main className="page-grid">
        <section className="login-panel panel">
          <div className="panel-head">
            <span className="label-chip">Authentication</span>
            <h2>{isLoggedIn ? 'Mission control' : 'Secure login'}</h2>
          </div>

          {!isLoggedIn ? (
            <form onSubmit={handleLogin} className="login-form">
              <label>
                Username
                <input
                  type="text"
                  value={loginForm.username}
                  onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
                  placeholder="admin"
                />
              </label>
              <label>
                Password
                <input
                  type="password"
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                  placeholder="••••••••"
                />
              </label>
              <button type="submit" disabled={loading}>
                {loading ? 'Authenticating...' : 'Login'}
              </button>
            </form>
          ) : (
            <div className="user-card">
              <div className="avatar">{user?.first_name?.[0] || user?.username?.[0] || 'A'}</div>
              <div>
                <strong>{user?.first_name && user?.last_name ? `${user.first_name} ${user.last_name}` : user?.username}</strong>
                <p>{user?.role}</p>
                <small>{user?.email}</small>
              </div>
            </div>
          )}

          <div className="notice-box">
            <strong>System message</strong>
            <p>{message}</p>
          </div>
        </section>

        <section id="overview" className="overview panel">
          <div className="panel-head">
            <span className="label-chip">Operations</span>
            <h2>Member 1 overview</h2>
          </div>

          <div className="stats-grid">
            {summaryCards.map((card) => (
              <article key={card.label} className={`stat-card ${card.accent}`}>
                <span>{card.label}</span>
                <strong>{card.value}</strong>
              </article>
            ))}
          </div>
        </section>

        <section className="panel user-panel">
          <div className="panel-head">
            <span className="label-chip">Access control</span>
            <h2>User management</h2>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                {users.map((entry) => (
                  <tr key={entry.id}>
                    <td>{entry.username}</td>
                    <td>{entry.role}</td>
                    <td><span className="status-dot active">{entry.status}</span></td>
                    <td>{entry.email}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section id="faculty" className="panel faculty-panel">
          <div className="panel-head">
            <span className="label-chip">Faculty management</span>
            <h2>Faculty profiles</h2>
          </div>

          <form className="faculty-form" onSubmit={handleFacultyCreate}>
            <input value={facultyForm.faculty_id} onChange={(e) => setFacultyForm({ ...facultyForm, faculty_id: e.target.value })} placeholder="Faculty ID" />
            <input value={facultyForm.user} onChange={(e) => setFacultyForm({ ...facultyForm, user: e.target.value })} placeholder="User ID" />
            <input value={facultyForm.department} onChange={(e) => setFacultyForm({ ...facultyForm, department: e.target.value })} placeholder="Department" />
            <input value={facultyForm.designation} onChange={(e) => setFacultyForm({ ...facultyForm, designation: e.target.value })} placeholder="Designation" />
            <select value={facultyForm.status} onChange={(e) => setFacultyForm({ ...facultyForm, status: e.target.value })}>
              <option value="ACTIVE">Active</option>
              <option value="INACTIVE">Inactive</option>
              <option value="ON_LEAVE">On Leave</option>
            </select>
            <input value={facultyForm.email} onChange={(e) => setFacultyForm({ ...facultyForm, email: e.target.value })} placeholder="Email" />
            <input value={facultyForm.phone} onChange={(e) => setFacultyForm({ ...facultyForm, phone: e.target.value })} placeholder="Phone" />
            <input value={facultyForm.qualification} onChange={(e) => setFacultyForm({ ...facultyForm, qualification: e.target.value })} placeholder="Qualification" />
            <input value={facultyForm.specialization} onChange={(e) => setFacultyForm({ ...facultyForm, specialization: e.target.value })} placeholder="Specialization" />
            <button type="submit">Create faculty profile</button>
          </form>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Faculty ID</th>
                  <th>Name</th>
                  <th>Department</th>
                  <th>Status</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                {faculty.map((entry) => (
                  <tr key={entry.id}>
                    <td>{entry.faculty_id}</td>
                    <td>{entry.user_name}</td>
                    <td>{entry.department}</td>
                    <td><span className="status-dot" data-tone={entry.status.toLowerCase()}>{entry.status}</span></td>
                    <td>{entry.email}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section id="security" className="panel security-panel">
          <div className="panel-head">
            <span className="label-chip">Security</span>
            <h2>Policy checks</h2>
          </div>
          <ul className="feature-list">
            <li>Duplicate username and institutional email validation</li>
            <li>Secure password hashing and administrative reset flow</li>
            <li>Role-based permissions enforced on backend and UI</li>
            <li>Account activation, deactivation, and audit trails</li>
            <li>Faculty leave and availability tracking</li>
          </ul>
        </section>

        <section id="audit" className="panel audit-panel">
          <div className="panel-head">
            <span className="label-chip">Audit</span>
            <h2>Activity summary</h2>
          </div>
          <div className="audit-grid">
            <div>
              <strong>{stats.incompleteProfiles}</strong>
              <span>Incomplete faculty profiles</span>
            </div>
            <div>
              <strong>{stats.inactiveUsers}</strong>
              <span>Inactive accounts</span>
            </div>
            <div>
              <strong>{roleOptions.length}</strong>
              <span>Protected roles</span>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
