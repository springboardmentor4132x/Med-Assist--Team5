import React, { useState, useEffect } from 'react';
import AdminSidebar from '../components/AdminSidebar';
import AdminNavbar from '../components/AdminNavbar';
import DashboardCard from '../components/DashboardCard';
import LoadingIndicator from '../components/LoadingIndicator';
import { adminService } from '../services/adminService';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await adminService.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load dashboard statistics:', err);
      setError('Unable to retrieve live statistics from the backend server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <div className="app-container">
      <AdminSidebar />
      <div className="main-content">
        <AdminNavbar pageTitle="Healthcare Administration Dashboard" />

        <main className="page-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h1 className="page-title">System Overview</h1>
              <p className="page-subtitle">Real-time PostgreSQL metrics and user distribution.</p>
            </div>
            <button className="btn btn-secondary btn-sm" onClick={fetchStats} disabled={loading}>
              ↻ Refresh Data
            </button>
          </div>

          {error && (
            <div className="alert alert-error">
              <span>{error}</span>
            </div>
          )}

          {loading ? (
            <LoadingIndicator message="Connecting to PostgreSQL & compiling system metrics..." />
          ) : stats ? (
            <>
              {/* Top 5 Metric Cards */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                gap: '1.25rem',
                marginBottom: '2rem'
              }}>
                <DashboardCard
                  title="Total Registered Users"
                  value={stats.total_users}
                  icon="👥"
                  subtitle={`${stats.active_accounts} active accounts`}
                />
                <DashboardCard
                  title="Total Patients"
                  value={stats.total_patients}
                  icon="🩺"
                  subtitle="Primary healthcare recipients"
                />
                <DashboardCard
                  title="Total Doctors"
                  value={stats.total_doctors}
                  icon="👨‍⚕️"
                  subtitle="Licensed practitioners"
                />
                <DashboardCard
                  title="Total Clinics"
                  value={stats.total_clinics}
                  icon="🏥"
                  subtitle="Clinical wellness centers"
                />
                <DashboardCard
                  title="Total Administrators"
                  value={stats.total_admins}
                  icon="🛡️"
                  subtitle="System governance controllers"
                />
              </div>

              {/* Analytics Section: Role Distribution & Account Health */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))',
                gap: '1.5rem',
                marginBottom: '2rem'
              }}>
                {/* Role Distribution Card */}
                <div className="card">
                  <h3 style={{ fontSize: '1.1rem', marginBottom: '1.25rem', fontWeight: 600 }}>
                    User Distribution by Role
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {stats.role_distribution.map((item) => (
                      <div key={item.role}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.35rem' }}>
                          <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{item.role}</span>
                          <span style={{ color: 'var(--text-secondary)' }}>
                            {item.count} users ({item.percentage}%)
                          </span>
                        </div>
                        <div style={{ width: '100%', height: '8px', backgroundColor: '#E5ECE7', borderRadius: '4px', overflow: 'hidden' }}>
                          <div style={{
                            width: `${item.percentage}%`,
                            height: '100%',
                            backgroundColor:
                              item.role === 'Admin' ? '#7C3AED' :
                              item.role === 'Doctor' ? '#0284C7' :
                              item.role === 'Clinic' ? '#D97706' : 'var(--primary-green)',
                            borderRadius: '4px',
                            transition: 'width 0.6s ease'
                          }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Account Status Card */}
                <div className="card">
                  <h3 style={{ fontSize: '1.1rem', marginBottom: '1.25rem', fontWeight: 600 }}>
                    Account Health & Compliance
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                    <div style={{
                      padding: '1rem',
                      borderRadius: 'var(--radius-md)',
                      backgroundColor: 'var(--success-bg)',
                      border: '1px solid #C6F0DA',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between'
                    }}>
                      <div>
                        <div style={{ fontWeight: 600, color: 'var(--dark-green)' }}>Active Accounts</div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Full system access permitted</div>
                      </div>
                      <div style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--dark-green)' }}>
                        {stats.active_accounts}
                      </div>
                    </div>

                    <div style={{
                      padding: '1rem',
                      borderRadius: 'var(--radius-md)',
                      backgroundColor: 'var(--error-bg)',
                      border: '1px solid #FECACA',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between'
                    }}>
                      <div>
                        <div style={{ fontWeight: 600, color: '#B91C1C' }}>Deactivated Accounts</div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Blocked from authenticated APIs</div>
                      </div>
                      <div style={{ fontSize: '1.75rem', fontWeight: 700, color: '#B91C1C' }}>
                        {stats.inactive_accounts}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Registered Users */}
              <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>
                    Recent User Registrations
                  </h3>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    Displaying latest 5 records
                  </span>
                </div>

                <div className="table-responsive">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>User ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Status</th>
                        <th>Registered Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {stats.recent_registrations.map((u) => (
                        <tr key={u.id}>
                          <td style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>#{u.id}</td>
                          <td style={{ fontWeight: 600 }}>{u.full_name}</td>
                          <td style={{ color: 'var(--text-secondary)' }}>{u.email}</td>
                          <td>
                            <span className="badge badge-patient">{u.role}</span>
                          </td>
                          <td>
                            <span className={`badge ${u.is_active ? 'badge-active' : 'badge-inactive'}`}>
                              ● {u.is_active ? 'Active' : 'Inactive'}
                            </span>
                          </td>
                          <td style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                            {new Date(u.created_at).toLocaleDateString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          ) : null}
        </main>
      </div>
    </div>
  );
}
