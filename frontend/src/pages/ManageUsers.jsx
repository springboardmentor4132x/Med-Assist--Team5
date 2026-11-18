import React, { useState, useEffect } from 'react';
import AdminSidebar from '../components/AdminSidebar';
import AdminNavbar from '../components/AdminNavbar';
import UserTable from '../components/UserTable';
import ConfirmationModal from '../components/ConfirmationModal';
import LoadingIndicator from '../components/LoadingIndicator';
import { adminService } from '../services/adminService';

export default function ManageUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  // Notifications
  const [alertMessage, setAlertMessage] = useState({ text: '', type: '' });

  // Modals state
  const [selectedUser, setSelectedUser] = useState(null);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
  const [editFormData, setEditFormData] = useState({ full_name: '', email: '' });
  const [modalLoading, setModalLoading] = useState(false);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const params = {
        page,
        limit: 8,
        search: search || undefined,
        role: roleFilter !== 'All' ? roleFilter : undefined,
        status: statusFilter !== 'All' ? statusFilter : undefined
      };
      const res = await adminService.getUsers(params);
      setUsers(res.items);
      setTotalPages(res.total_pages);
      setTotalCount(res.total);
    } catch (err) {
      console.error('Error fetching users:', err);
      setAlertMessage({ text: 'Failed to load user records from PostgreSQL.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [page, roleFilter, statusFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    fetchUsers();
  };

  // View Details
  const handleView = async (user) => {
    try {
      setModalLoading(true);
      const details = await adminService.getUserDetails(user.id);
      setSelectedUser(details);
      setIsViewModalOpen(true);
    } catch (err) {
      setAlertMessage({ text: 'Could not fetch detailed profile information.', type: 'error' });
    } finally {
      setModalLoading(false);
    }
  };

  // Edit User
  const handleEdit = (user) => {
    setSelectedUser(user);
    setEditFormData({ full_name: user.full_name, email: user.email });
    setIsEditModalOpen(true);
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      setModalLoading(true);
      await adminService.updateUserInfo(selectedUser.id, editFormData);
      setIsEditModalOpen(false);
      setAlertMessage({ text: `User account #${selectedUser.id} updated successfully.`, type: 'success' });
      fetchUsers();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to update user account.';
      setAlertMessage({ text: msg, type: 'error' });
    } finally {
      setModalLoading(false);
    }
  };

  // Status Toggle (Activate / Deactivate)
  const handleToggleStatus = (user) => {
    setSelectedUser(user);
    setIsConfirmModalOpen(true);
  };

  const handleConfirmStatusToggle = async () => {
    if (!selectedUser) return;
    const newStatus = !selectedUser.is_active;
    try {
      setModalLoading(true);
      await adminService.updateUserStatus(selectedUser.id, newStatus);
      setIsConfirmModalOpen(false);
      setAlertMessage({
        text: `Account for ${selectedUser.full_name} has been ${newStatus ? 'activated' : 'deactivated'}.`,
        type: 'success'
      });
      fetchUsers();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to update account status.';
      setAlertMessage({ text: msg, type: 'error' });
      setIsConfirmModalOpen(false);
    } finally {
      setModalLoading(false);
    }
  };

  return (
    <div className="app-container">
      <AdminSidebar />
      <div className="main-content">
        <AdminNavbar pageTitle="Manage Users" />

        <main className="page-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h1 className="page-title">User Directory & Governance</h1>
              <p className="page-subtitle">
                Manage registered accounts, roles, access permissions and compliance ({totalCount} total users).
              </p>
            </div>
          </div>

          {alertMessage.text && (
            <div className={`alert ${alertMessage.type === 'error' ? 'alert-error' : 'alert-success'}`}>
              <span>{alertMessage.text}</span>
            </div>
          )}

          {/* Search & Filters Bar */}
          <div className="card" style={{ marginBottom: '1.5rem', padding: '1rem 1.25rem' }}>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center', justifyContent: 'space-between' }}>
              <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '0.5rem', flex: '1 1 300px' }}>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Search by full name or email address..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
                <button type="submit" className="btn btn-primary btn-sm">
                  Search
                </button>
              </form>

              <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                <div>
                  <select
                    className="form-select"
                    value={roleFilter}
                    onChange={(e) => { setRoleFilter(e.target.value); setPage(1); }}
                    style={{ minWidth: '130px' }}
                  >
                    <option value="All">All Roles</option>
                    <option value="Patient">Patient</option>
                    <option value="Doctor">Doctor</option>
                    <option value="Clinic">Clinic</option>
                    <option value="Admin">Admin</option>
                  </select>
                </div>

                <div>
                  <select
                    className="form-select"
                    value={statusFilter}
                    onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
                    style={{ minWidth: '130px' }}
                  >
                    <option value="All">All Statuses</option>
                    <option value="active">Active Only</option>
                    <option value="inactive">Inactive Only</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* User Table Component */}
          {loading ? (
            <LoadingIndicator message="Fetching user records..." />
          ) : (
            <>
              <UserTable
                users={users}
                onViewDetails={handleView}
                onEditUser={handleEdit}
                onToggleStatus={handleToggleStatus}
              />

              {/* Pagination Controls */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginTop: '1.25rem',
                padding: '0.5rem 0'
              }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  Page {page} of {totalPages} ({totalCount} total results)
                </span>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button
                    className="btn btn-secondary btn-sm"
                    disabled={page <= 1}
                    onClick={() => setPage(page - 1)}
                  >
                    Previous
                  </button>
                  <button
                    className="btn btn-secondary btn-sm"
                    disabled={page >= totalPages}
                    onClick={() => setPage(page + 1)}
                  >
                    Next
                  </button>
                </div>
              </div>
            </>
          )}

          {/* View Details Modal */}
          {isViewModalOpen && selectedUser && (
            <div className="modal-overlay" onClick={() => setIsViewModalOpen(false)}>
              <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '1rem' }}>
                  User Account Details
                </h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                  <div><strong>Account ID:</strong> #{selectedUser.id}</div>
                  <div><strong>Full Name:</strong> {selectedUser.full_name}</div>
                  <div><strong>Email Address:</strong> {selectedUser.email}</div>
                  <div><strong>Role:</strong> <span className="badge badge-patient">{selectedUser.role}</span></div>
                  <div>
                    <strong>Status:</strong>{' '}
                    <span className={`badge ${selectedUser.is_active ? 'badge-active' : 'badge-inactive'}`}>
                      {selectedUser.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <div><strong>Registered On:</strong> {new Date(selectedUser.created_at).toLocaleString()}</div>

                  {selectedUser.patient_profile && (
                    <div style={{ marginTop: '0.5rem', padding: '0.75rem', backgroundColor: '#F8FAF9', borderRadius: '6px' }}>
                      <strong>Patient Profile Details:</strong>
                      <div>Gender: {selectedUser.patient_profile.gender || 'N/A'}</div>
                      <div>Date of Birth: {selectedUser.patient_profile.date_of_birth || 'N/A'}</div>
                      <div>Blood Group: {selectedUser.patient_profile.blood_group || 'N/A'}</div>
                      <div>Emergency Contact: {selectedUser.patient_profile.emergency_contact || 'N/A'}</div>
                    </div>
                  )}

                  {selectedUser.doctor_profile && (
                    <div style={{ marginTop: '0.5rem', padding: '0.75rem', backgroundColor: '#F8FAF9', borderRadius: '6px' }}>
                      <strong>Doctor Profile Details:</strong>
                      <div>Specialization: {selectedUser.doctor_profile.specialization}</div>
                      <div>License: {selectedUser.doctor_profile.license_number}</div>
                      <div>Experience: {selectedUser.doctor_profile.years_of_experience} years</div>
                    </div>
                  )}

                  {selectedUser.clinic_profile && (
                    <div style={{ marginTop: '0.5rem', padding: '0.75rem', backgroundColor: '#F8FAF9', borderRadius: '6px' }}>
                      <strong>Clinic Profile Details:</strong>
                      <div>Facility: {selectedUser.clinic_profile.clinic_name}</div>
                      <div>Address: {selectedUser.clinic_profile.address}</div>
                      <div>Contact: {selectedUser.clinic_profile.contact_number}</div>
                    </div>
                  )}
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <button className="btn btn-secondary" onClick={() => setIsViewModalOpen(false)}>
                    Close
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Edit User Modal */}
          {isEditModalOpen && (
            <div className="modal-overlay" onClick={() => setIsEditModalOpen(false)}>
              <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '1rem' }}>
                  Edit Permitted Account Information
                </h3>
                <form onSubmit={handleEditSubmit}>
                  <div className="form-group">
                    <label className="form-label">Full Name</label>
                    <input
                      type="text"
                      className="form-input"
                      value={editFormData.full_name}
                      onChange={(e) => setEditFormData({ ...editFormData, full_name: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Email Address</label>
                    <input
                      type="email"
                      className="form-input"
                      value={editFormData.email}
                      onChange={(e) => setEditFormData({ ...editFormData, email: e.target.value })}
                      required
                    />
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => setIsEditModalOpen(false)}
                      disabled={modalLoading}
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="btn btn-primary"
                      disabled={modalLoading}
                    >
                      {modalLoading ? 'Saving...' : 'Save Changes'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          {/* Confirm Status Toggle Modal */}
          <ConfirmationModal
            isOpen={isConfirmModalOpen}
            title={selectedUser?.is_active ? 'Deactivate Account' : 'Activate Account'}
            message={
              selectedUser?.is_active
                ? `Are you sure you want to deactivate the account for ${selectedUser?.full_name}? They will immediately be denied access to all protected healthcare APIs.`
                : `Are you sure you want to re-activate the account for ${selectedUser?.full_name}? Their system access will be restored.`
            }
            confirmText={selectedUser?.is_active ? 'Deactivate Account' : 'Activate Account'}
            isDanger={selectedUser?.is_active}
            isLoading={modalLoading}
            onConfirm={handleConfirmStatusToggle}
            onCancel={() => setIsConfirmModalOpen(false)}
          />
        </main>
      </div>
    </div>
  );
}
