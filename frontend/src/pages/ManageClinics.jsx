import React, { useState, useEffect } from 'react';
import AdminSidebar from '../components/AdminSidebar';
import AdminNavbar from '../components/AdminNavbar';
import ConfirmationModal from '../components/ConfirmationModal';
import LoadingIndicator from '../components/LoadingIndicator';
import { adminService } from '../services/adminService';

export default function ManageClinics() {
  const [clinics, setClinics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const [alertMessage, setAlertMessage] = useState({ text: '', type: '' });
  const [selectedClinic, setSelectedClinic] = useState(null);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);

  const fetchClinics = async () => {
    try {
      setLoading(true);
      const res = await adminService.getClinics({
        page,
        limit: 10,
        search: search || undefined,
        status: statusFilter !== 'All' ? statusFilter : undefined
      });
      setClinics(res.items);
      setTotalCount(res.total);
    } catch (err) {
      console.error(err);
      setAlertMessage({ text: 'Failed to retrieve clinics from PostgreSQL.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClinics();
  }, [page, statusFilter]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchClinics();
  };

  const handleToggleStatus = (clinic) => {
    setSelectedClinic(clinic);
    setIsConfirmOpen(true);
  };

  const handleConfirmToggle = async () => {
    if (!selectedClinic) return;
    try {
      setModalLoading(true);
      await adminService.updateUserStatus(selectedClinic.id, !selectedClinic.is_active);
      setIsConfirmOpen(false);
      setAlertMessage({
        text: `Clinic account #${selectedClinic.id} has been ${!selectedClinic.is_active ? 'activated' : 'deactivated'}.`,
        type: 'success'
      });
      fetchClinics();
    } catch (err) {
      setAlertMessage({ text: 'Error updating clinic account status.', type: 'error' });
      setIsConfirmOpen(false);
    } finally {
      setModalLoading(false);
    }
  };

  return (
    <div className="app-container">
      <AdminSidebar />
      <div className="main-content">
        <AdminNavbar pageTitle="Manage Clinics" />

        <main className="page-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h1 className="page-title">Clinic & Facility Registry</h1>
              <p className="page-subtitle">
                Accredited clinical wellness centers, healthcare organizations and facility accounts ({totalCount} total clinics).
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
                  placeholder="Search clinic by name or email..."
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
            <LoadingIndicator message="Retrieving clinic facilities..." />
          ) : (
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Representative</th>
                    <th>Email</th>
                    <th>Clinic Facility Name</th>
                    <th>Address</th>
                    <th>Contact Phone</th>
                    <th>Status</th>
                    <th style={{ textAlign: 'right' }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {clinics.length === 0 ? (
                    <tr>
                      <td colSpan="8" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                        No clinic records found.
                      </td>
                    </tr>
                  ) : (
                    clinics.map((c) => (
                      <tr key={c.id}>
                        <td>#{c.id}</td>
                        <td style={{ fontWeight: 600 }}>{c.full_name}</td>
                        <td style={{ color: 'var(--text-secondary)' }}>{c.email}</td>
                        <td>
                          <span className="badge badge-clinic">{c.profile?.clinic_name || c.full_name}</span>
                        </td>
                        <td style={{ fontSize: '0.85rem' }}>{c.profile?.address || 'N/A'}</td>
                        <td><code>{c.profile?.contact_number || 'N/A'}</code></td>
                        <td>
                          <span className={`badge ${c.is_active ? 'badge-active' : 'badge-inactive'}`}>
                            ● {c.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          <button
                            className={`btn btn-sm ${c.is_active ? 'btn-outline-danger' : 'btn-primary'}`}
                            onClick={() => handleToggleStatus(c)}
                          >
                            {c.is_active ? 'Deactivate' : 'Activate'}
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
            title={selectedClinic?.is_active ? 'Deactivate Clinic' : 'Activate Clinic'}
            message={`Are you sure you want to ${selectedClinic?.is_active ? 'deactivate' : 'activate'} the facility account for ${selectedClinic?.full_name}?`}
            confirmText={selectedClinic?.is_active ? 'Deactivate' : 'Activate'}
            isDanger={selectedClinic?.is_active}
            isLoading={modalLoading}
            onConfirm={handleConfirmToggle}
            onCancel={() => setIsConfirmOpen(false)}
          />
        </main>
      </div>
    </div>
  );
}
