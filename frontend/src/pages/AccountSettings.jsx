import React, { useState, useEffect } from 'react';
import AdminSidebar from '../components/AdminSidebar';
import AdminNavbar from '../components/AdminNavbar';
import LoadingIndicator from '../components/LoadingIndicator';
import { adminService } from '../services/adminService';
import { authService } from '../services/authService';

export default function AccountSettings() {
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [alertMessage, setAlertMessage] = useState({ text: '', type: '' });

  // Form fields
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const fetchAccount = async () => {
    try {
      setLoading(true);
      const data = await adminService.getAccount();
      setAccount(data);
      setFullName(data.full_name);
      setEmail(data.email);
    } catch (err) {
      console.error(err);
      setAlertMessage({ text: 'Failed to retrieve administrator account information.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAccount();
  }, []);

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setAlertMessage({ text: '', type: '' });

    if (newPassword) {
      if (!currentPassword) {
        setAlertMessage({ text: 'Current password is required to set a new password.', type: 'error' });
        return;
      }
      if (newPassword.length < 6) {
        setAlertMessage({ text: 'New password must be at least 6 characters.', type: 'error' });
        return;
      }
      if (newPassword !== confirmPassword) {
        setAlertMessage({ text: 'New password and confirmation do not match.', type: 'error' });
        return;
      }
    }

    try {
      setSaving(true);
      const payload = {
        full_name: fullName,
        email: email,
        current_password: currentPassword || undefined,
        new_password: newPassword || undefined
      };
      const updated = await adminService.updateAccount(payload);
      setAccount(updated);
      
      // Update local storage user profile name/email
      const currentStored = authService.getCurrentUser();
      if (currentStored) {
        localStorage.setItem('medassist_user', JSON.stringify({
          ...currentStored,
          full_name: updated.full_name,
          email: updated.email
        }));
      }

      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setAlertMessage({ text: 'Your administrator profile was updated successfully.', type: 'success' });
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to update account.';
      setAlertMessage({ text: msg, type: 'error' });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="app-container">
      <AdminSidebar />
      <div className="main-content">
        <AdminNavbar pageTitle="Account Settings" />

        <main className="page-body">
          <div style={{ marginBottom: '1.5rem' }}>
            <h1 className="page-title">Administrator Account Settings</h1>
            <p className="page-subtitle">Manage personal profile details, authentication credentials and security preferences.</p>
          </div>

          {alertMessage.text && (
            <div className={`alert ${alertMessage.type === 'error' ? 'alert-error' : 'alert-success'}`}>
              <span>{alertMessage.text}</span>
            </div>
          )}

          {loading ? (
            <LoadingIndicator message="Loading administrator profile..." />
          ) : account ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
              {/* Account Summary Card */}
              <div className="card" style={{ height: 'fit-content' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '1.25rem' }}>
                  Account Summary
                </h3>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
                  <div style={{
                    width: '56px',
                    height: '56px',
                    borderRadius: '50%',
                    backgroundColor: 'var(--light-green)',
                    color: 'var(--dark-green)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.5rem',
                    fontWeight: 700
                  }}>
                    {account.full_name ? account.full_name.charAt(0).toUpperCase() : 'A'}
                  </div>
                  <div>
                    <h4 style={{ fontSize: '1rem', fontWeight: 600 }}>{account.full_name}</h4>
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{account.email}</span>
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>User Role</span>
                    <span className="badge badge-admin">{account.role}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Account Status</span>
                    <span className="badge badge-active">● Active</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Member Since</span>
                    <span>{new Date(account.created_at).toLocaleDateString()}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>User ID</span>
                    <span style={{ fontWeight: 600 }}>#{account.id}</span>
                  </div>
                </div>
              </div>

              {/* Edit Profile & Password Form */}
              <div className="card">
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '1.25rem' }}>
                  Update Credentials & Profile
                </h3>

                <form onSubmit={handleProfileSubmit}>
                  <div className="form-group">
                    <label className="form-label">Full Name</label>
                    <input
                      type="text"
                      className="form-input"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Email Address</label>
                    <input
                      type="email"
                      className="form-input"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>

                  <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '1.5rem 0' }} />

                  <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: '1rem', color: 'var(--text-primary)' }}>
                    Change Password (Optional)
                  </h4>

                  <div className="form-group">
                    <label className="form-label">Current Password</label>
                    <input
                      type="password"
                      className="form-input"
                      placeholder="Enter current password to authorize change"
                      value={currentPassword}
                      onChange={(e) => setCurrentPassword(e.target.value)}
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">New Password</label>
                    <input
                      type="password"
                      className="form-input"
                      placeholder="Minimum 6 characters"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Confirm New Password</label>
                    <input
                      type="password"
                      className="form-input"
                      placeholder="Repeat new password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.75rem' }}>
                    <button type="submit" className="btn btn-primary" disabled={saving}>
                      {saving ? 'Updating Account...' : 'Save Settings'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          ) : null}
        </main>
      </div>
    </div>
  );
}
