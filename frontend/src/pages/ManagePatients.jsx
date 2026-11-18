import React, { useState, useEffect } from 'react';
import AdminSidebar from '../components/AdminSidebar';
import AdminNavbar from '../components/AdminNavbar';
import ConfirmationModal from '../components/ConfirmationModal';
import LoadingIndicator from '../components/LoadingIndicator';
import { adminService } from '../services/adminService';

export default function ManagePatients() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const [alertMessage, setAlertMessage] = useState({ text: '', type: '' });
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);

  const fetchPatients = async () => {
    try {
      setLoading(true);
      const res = await adminService.getPatients({
        page,
        limit: 10,
        search: search || undefined,
        status: statusFilter !== 'All' ? statusFilter : undefined
      });
      setPatients(res.items);
      setTotalPages(res.total_pages);
      setTotalCount(res.total);
    } catch (err) {
      console.error(err);
      setAlertMessage({ text: 'Failed to retrieve patient registry from PostgreSQL.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, [page, statusFilter]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchPatients();
  };

  const handleToggleStatus = (patient) => {
    setSelectedPatient(patient);
    setIsConfirmOpen(true);
  };

  const handleConfirmToggle = async () => {
    if (!selectedPatient) return;
    try {
      setModalLoading(true);
      await adminService.updateUserStatus(selectedPatient.id, !selectedPatient.is_active);
      setIsConfirmOpen(false);
      setAlertMessage({
        text: `Patient account #${selectedPatient.id} has been ${!selectedPatient.is_active ? 'activated' : 'deactivated'}.`,
        type: 'success'
      });
      fetchPatients();
    } catch (err) {
      setAlertMessage({ text: 'Error updating patient account status.', type: 'error' });
      setIsConfirmOpen(false);
    } finally {
      setModalLoading(false);
    }
  };

  return (
    <div className="app-container">
      <AdminSidebar />
      <div className="main-content">
        <AdminNavbar pageTitle="Manage Patients" />

        <main className="page-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h1 className="page-title">Patient Directory</h1>
              <p className="page-subtitle">
                Registered patients profile and account status governance ({totalCount} total registered).
              </p>
            </div>
          </div>

          {alertMessage.text && (
            <div className={`alert ${alertMessage.type === 'error' ? 'alert-error' : 'alert-success'}`}>
              <span>{alertMessage.text}</span>
            </div>
          )}

          {/* Search bar */}
          <div className="card" style={{ marginBottom: '1.5rem', padding: '1rem' }}>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'space-between' }}>
              <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', flex: '1 1 300px' }}>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Search patient name or email..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
                <button type="submit" className="btn btn-primary btn-sm">Search</button>
              </form>

              <select
                className="form-select"
                value={statusFilter}
                onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
                style={{ width: '150px' }}
              >
                <option value="All">All Statuses</option>
                <option value="active">Active Only</option>
                <option value="inactive">Inactive Only</option>
              </select>
            </div>
          </div>

          {/* Patients Table */}
          {loading ? (
            <LoadingIndicator message="Retrieving patient records..." />
          ) : (
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Patient Name</th>
                    <th>Email</th>
                    <th>Gender</th>
                    <th>DOB</th>
                    <th>Blood Group</th>
                    <th>Status</th>
                    <th style={{ textAlign: 'right' }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {patients.length === 0 ? (
                    <tr>
                      <td colSpan="8" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                        No patient records found.
                      </td>
                    </tr>
                  ) : (
                    patients.map((p) => (
                      <tr key={p.id}>
                        <td>#{p.id}</td>
                        <td style={{ fontWeight: 600 }}>{p.full_name}</td>
                        <td style={{ color: 'var(--text-secondary)' }}>{p.email}</td>
                        <td>{p.profile?.gender || 'N/A'}</td>
                        <td>{p.profile?.date_of_birth || 'N/A'}</td>
                        <td>
                          <span style={{ fontWeight: 600, color: 'var(--primary-green)' }}>
                            {p.profile?.blood_group || 'N/A'}
                          </span>
                        </td>
                        <td>
                          <span className={`badge ${p.is_active ? 'badge-active' : 'badge-inactive'}`}>
                            ● {p.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          <button
                            className={`btn btn-sm ${p.is_active ? 'btn-outline-danger' : 'btn-primary'}`}
                            onClick={() => handleToggleStatus(p)}
                          >
                            {p.is_active ? 'Deactivate' : 'Activate'}
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}

          <ConfirmationModal
            isOpen={isConfirmOpen}
            title={selectedPatient?.is_active ? 'Deactivate Patient' : 'Activate Patient'}
            message={`Are you sure you want to ${selectedPatient?.is_active ? 'deactivate' : 'activate'} the patient account for ${selectedPatient?.full_name}?`}
            confirmText={selectedPatient?.is_active ? 'Deactivate' : 'Activate'}
            isDanger={selectedPatient?.is_active}
            isLoading={modalLoading}
            onConfirm={handleConfirmToggle}
            onCancel={() => setIsConfirmOpen(false)}
          />
        </main>
      </div>
    </div>
  );
}
