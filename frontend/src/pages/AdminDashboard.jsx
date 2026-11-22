
import { useEffect, useState } from 'react'
import '../admin.css'

import AdminSidebar from '../components/AdminSidebar'
import AdminNavbar from '../components/AdminNavbar'
import DashboardCard from '../components/DashboardCard'
import LoadingIndicator from '../components/LoadingIndicator'
import { adminService } from '../services/adminService'
import AdminDoctors from './AdminDoctors'
import AdminPatients from './AdminPatients'
import AdminUsers from './AdminUsers'
import AdminClinics from './AdminClinics'
import AdminRoles from './AdminRoles'
import AdminAccount from './AdminAccount'
import AdminAssignments from './AdminAssignments'

export default function AdminDashboard({
  user,
  token,
  onLogout,
  activePage = 'Dashboard',
  onNavigate,
}) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function fetchStats() {
    try {
      setLoading(true)
      setError('')
      const data = await adminService.getDashboardStats(token)
      setStats(data)
    } catch (err) {
      setError(err.message || 'Unable to load dashboard.')
    } finally {
      setLoading(false)
    }
  }

   useEffect(() => {
    let cancelled = false

    async function loadStats() {
      try {
        const data = await adminService.getDashboardStats(token)

        if (!cancelled) {
          setStats(data)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || 'Unable to load dashboard.')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadStats()

    return () => {
      cancelled = true
    }
  }, [token])

  return (
    <div className="admin-shell">
      <div className="app-container">
        <AdminSidebar
          activePage={activePage}
          onNavigate={onNavigate}
          onLogout={onLogout}
        />

        <div className="main-content">
          <AdminNavbar
            pageTitle={activePage}
            user={user}
            onLogout={onLogout}
          />

          <main className="page-body">
            {activePage === 'Dashboard' ? (
              <>
                <h1 className="page-title">System Overview</h1>
                <p className="page-subtitle">
                  MedAssist AI administration dashboard
                </p>

                <button
                  className="btn btn-secondary"
                  onClick={fetchStats}
                  disabled={loading}
                >
                  Refresh Data
                </button>

                {error && <p className="alert alert-error">{error}</p>}

                {loading ? (
                  <LoadingIndicator message="Loading dashboard..." />
                ) : stats ? (
                  <>
                    <div className="dashboard-grid">
                      <DashboardCard
                        title="Total Users"
                        value={stats.total_users ?? 0}
                        icon="Users"
                      />
                      <DashboardCard
                        title="Total Patients"
                        value={stats.total_patients ?? 0}
                        icon="Patients"
                      />
                      <DashboardCard
                        title="Total Doctors"
                        value={stats.total_doctors ?? 0}
                        icon="Doctors"
                      />
                      <DashboardCard
                        title="Total Clinics"
                        value={stats.total_clinics ?? 0}
                        icon="Clinics"
                      />
                      <DashboardCard
                        title="Active Accounts"
                        value={stats.active_accounts ?? 0}
                        icon="Active"
                      />
                    </div>

                    <section className="card">
                      <h3>Recent Registrations</h3>
                      <div className="table-responsive">
                        <table className="data-table">
                          <thead>
                            <tr>
                              <th>ID</th>
                              <th>Name</th>
                              <th>Email</th>
                              <th>Role</th>
                              <th>Status</th>
                            </tr>
                          </thead>
                          <tbody>
                            {(stats.recent_registrations || []).map(item => (
                              <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.full_name}</td>
                                <td>{item.email}</td>
                                <td>{item.role}</td>
                                <td>
                                  {item.is_active ? 'Active' : 'Inactive'}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </section>
                  </>
                ) : (
                  <p>No dashboard data available.</p>
                )}
              </>
                    ) : activePage === 'Manage Doctors' ? (
                      <AdminDoctors token={token} />
                  ) : activePage === 'Manage Patients' ? (
                     <AdminPatients token={token} />
                     ) : activePage === 'Manage Users' ? (
                       <AdminUsers token={token} />
                       ) : activePage === 'Manage Clinics' ? (
                        <AdminClinics token={token} />
                          ) : activePage === 'Manage Roles' ? (
                         <AdminRoles token={token} />
                         )  : activePage === 'Assignments' ? (
                            <AdminAssignments token={token} />
                         ) : activePage === 'Account Settings' ? (
                              <AdminAccount token={token} />

                      ) : (
              <section className="card">
                <h1 className="page-title">{activePage}</h1>
                <p>This section will be integrated next.</p>
              </section>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}
