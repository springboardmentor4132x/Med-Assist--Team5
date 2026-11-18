import React, { useState, useEffect } from 'react';
import AdminSidebar from '../components/AdminSidebar';
import AdminNavbar from '../components/AdminNavbar';
import ConfirmationModal from '../components/ConfirmationModal';
import LoadingIndicator from '../components/LoadingIndicator';
import { adminService } from '../services/adminService';

export default function ManageRoles() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [alertMessage, setAlertMessage] = useState({ text: '', type: '' });

  // Role modification modal
  const [selectedUser, setSelectedUser] = useState(null);
  const [targetRole, setTargetRole] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);

  const availableRoles = ['Patient', 'Doctor', 'Clinic', 'Admin'];

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const res = await adminService.getUsers({ limit: 50, search: search || undefined });
      setUsers(res.items);
    } catch (err) {
      console.error(err);
      setAlertMessage({ text: 'Failed to load user roles from PostgreSQL.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleOpenRoleModal = (user) => {
    setSelectedUser(user);
    setTargetRole(user.role);
    setIsModalOpen(true);
  };

  const handleConfirmRoleChange = async () => {
    if (!selectedUser || !targetRole) return;
    if (selectedUser.role === targetRole) {
      setIsModalOpen(false);
      return;
    }

    try {
      setModalLoading(true);
      await adminService.updateUserRole(selectedUser.id, targetRole);
      setIsModalOpen(false);
      setAlertMessage({
        text: `Role for ${selectedUser.full_name} successfully updated to ${targetRole}.`,
        type: 'success'
      });
      fetchUsers();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to update user role.';
      setAlertMessage({ text: msg, type: 'error' });
      setIsModalOpen(false);
    } finally {
      setModalLoading(false);
    }
  };

  return (
    <div className="app-container">
      <AdminSidebar />
      <div className="main-content">
        <AdminNavbar pageTitle="Manage Roles & Governance" />

        <main className="page-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h1 className="page-title">Role-Based Access Control (RBAC)</h1>
              <p className="page-subtitle">
                Assign and govern user privilege levels (Patient, Doctor, Clinic, Admin) with audit safeguards.
              </p>
            </div>
          </div>

          {alertMessage.text && (
            <div className={`alert ${alertMessage.type === 'error' ? 'alert-error' : 'alert-success'}`}>
              <span>{alertMessage.text}</span>
            </div>
          )}

          {/* Info Banner on Security Rules */}
          <div style={{
            padding: '1rem 1.25rem',
            backgroundColor: '#E9F8F0',
            border: '1px solid #C6F0DA',
            borderRadius: 'var(--radius-md)',
            marginBottom: '1.5rem',
            fontSize: '0.85rem',
            color: 'var(--dark-green)'
          }}>
            <strong>🛡️ Role Governance Security Policy:</strong> All role changes are validated on the backend.
            Demoting or deactivating the last remaining active Administrator is strictly prohibited by security guards.
          </div>

          {/* Roles Table */}
          {loading ? (
            <LoadingIndicator message="Fetching role assignments..." />
          ) : (
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>User Name</th>
                    <th>Email Address</th>
                    <th>Current Role</th>
                    <th>Account Status</th>
                    <th style={{ textAlign: 'right' }}>Role Action</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr key={u.id}>
                      <td>#{u.id}</td>
                      <td style={{ fontWeight: 600 }}>{u.full_name}</td>
                      <td style={{ color: 'var(--text-secondary)' }}>{u.email}</td>
                      <td>
                        <span className={`badge ${
                          u.role === 'Admin' ? 'badge-admin' :
                          u.role === 'Doctor' ? 'badge-doctor' :
                          u.role === 'Clinic' ? 'badge-clinic' : 'badge-patient'
                        }`}>
                          {u.role}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${u.is_active ? 'badge-active' : 'badge-inactive'}`}>
                          ● {u.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={() => handleOpenRoleModal(u)}
                        >
                          Change Role
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Role Change Modal */}
          {isModalOpen && selectedUser && (
            <div className="modal-overlay" onClick={() => setIsModalOpen(false)}>
              <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.5rem' }}>
                  Update User Role
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1.25rem' }}>
                  Modifying role for <strong>{selectedUser.full_name}</strong> ({selectedUser.email}).
                </p>

                <div className="form-group">
                  <label className="form-label">Select Target Role</label>
                  <select
                    className="form-select"
                    value={targetRole}
                    onChange={(e) => setTargetRole(e.target.value)}
                  >
                    {availableRoles.map((role) => (
                      <option key={role} value={role}>{role}</option>
                    ))}
                  </select>
                </div>

                {targetRole !== selectedUser.role && targetRole === 'Admin' && (
                  <div style={{ padding: '0.75rem', backgroundColor: '#FEF3C7', color: '#B45309', borderRadius: '6px', fontSize: '0.85rem', marginBottom: '1rem' }}>
                    ⚠️ Promoting this user gives them full administrative and account governance access across the system.
                  </div>
                )}

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
                  <button
                    className="btn btn-secondary"
                    onClick={() => setIsModalOpen(false)}
                    disabled={modalLoading}
                  >
                    Cancel
                  </button>
                  <button
                    className="btn btn-primary"
                    onClick={handleConfirmRoleChange}
                    disabled={modalLoading || targetRole === selectedUser.role}
                  >
                    {modalLoading ? 'Applying...' : 'Apply Role Change'}
                  </button>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
