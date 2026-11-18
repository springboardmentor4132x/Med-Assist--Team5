import React, { useState, useEffect } from 'react';
import AdminSidebar from '../components/AdminSidebar';
import AdminNavbar from '../components/AdminNavbar';
import ConfirmationModal from '../components/ConfirmationModal';
import LoadingIndicator from '../components/LoadingIndicator';
import { adminService } from '../services/adminService';

export default function ManageDoctors() {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const [alertMessage, setAlertMessage] = useState({ text: '', type: '' });
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);

  const fetchDoctors = async () => {
    try {
      setLoading(true);
      const res = await adminService.getDoctors({
        page,
        limit: 10,
        search: search || undefined,
        status: statusFilter !== 'All' ? statusFilter : undefined
      });
      setDoctors(res.items);
      setTotalCount(res.total);
    } catch (err) {
      console.error(err);
      setAlertMessage({ text: 'Failed to retrieve doctors from PostgreSQL.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDoctors();
  }, [page, statusFilter]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchDoctors();
  };

  const handleToggleStatus = (doctor) => {
    setSelectedDoctor(doctor);
    setIsConfirmOpen(true);
  };

  const handleConfirmToggle = async () => {
    if (!selectedDoctor) return;
    try {
      setModalLoading(true);
      await adminService.updateUserStatus(selectedDoctor.id, !selectedDoctor.is_active);
      setIsConfirmOpen(false);
      setAlertMessage({
        text: `Doctor account #${selectedDoctor.id} has been ${!selectedDoctor.is_active ? 'activated' : 'deactivated'}.`,
        type: 'success'
      });
      fetchDoctors();
    } catch (err) {
      setAlertMessage({ text: 'Error updating doctor account status.', type: 'error' });
      setIsConfirmOpen(false);
    } finally {
      setModalLoading(false);
    }
  };

  return (
    <div className="app-container">
      <AdminSidebar />
      <div className="main-content">
        <AdminNavbar pageTitle="Manage Doctors" />

        <main className="page-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h1 className="page-title">Doctor & Practitioner Registry</h1>
              <p className="page-subtitle">
                Licensed healthcare providers, clinical specialties and account compliance ({totalCount} total doctors).
              </p>
            </div>
          </div>

          {alertMessage.text && (
            <div className={`alert ${alertMessage.type === 'error' ? 'alert-error' : 'alert-success'}`}>
              <span>{alertMessage.text}</span>
            </div>
          )}

          <div className="card" style={{ marginBottom: '1.5rem', padding: '1rem' }}>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'space-between' }}>
              <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', flex: '1 1 300px' }}>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Search doctor by name or email..."
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

          {loading ? (
            <LoadingIndicator message="Retrieving practitioner profiles..." />
          ) : (
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Doctor Name</th>
                    <th>Email</th>
                    <th>Specialization</th>
                    <th>Medical License</th>
                    <th>Experience</th>
                    <th>Status</th>
                    <th style={{ textAlign: 'right' }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {doctors.length === 0 ? (
                    <tr>
                      <td colSpan="8" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                        No doctor records found.
                      </td>
                    </tr>
                  ) : (
                    doctors.map((d) => (
                      <tr key={d.id}>
                        <td>#{d.id}</td>
                        <td style={{ fontWeight: 600 }}>{d.full_name}</td>
                        <td style={{ color: 'var(--text-secondary)' }}>{d.email}</td>
                        <td>
                          <span className="badge badge-doctor">{d.profile?.specialization || 'General Practitioner'}</span>
                        </td>
                        <td><code>{d.profile?.license_number || 'N/A'}</code></td>
                        <td>{d.profile?.years_of_experience || 0} years</td>
                        <td>
                          <span className={`badge ${d.is_active ? 'badge-active' : 'badge-inactive'}`}>
                            ● {d.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          <button
                            className={`btn btn-sm ${d.is_active ? 'btn-outline-danger' : 'btn-primary'}`}
                            onClick={() => handleToggleStatus(d)}
                          >
                            {d.is_active ? 'Deactivate' : 'Activate'}
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
            title={selectedDoctor?.is_active ? 'Deactivate Doctor' : 'Activate Doctor'}
            message={`Are you sure you want to ${selectedDoctor?.is_active ? 'deactivate' : 'activate'} the account for ${selectedDoctor?.full_name}?`}
            confirmText={selectedDoctor?.is_active ? 'Deactivate' : 'Activate'}
            isDanger={selectedDoctor?.is_active}
            isLoading={modalLoading}
            onConfirm={handleConfirmToggle}
            onCancel={() => setIsConfirmOpen(false)}
          />
        </main>
      </div>
    </div>
  );
}
