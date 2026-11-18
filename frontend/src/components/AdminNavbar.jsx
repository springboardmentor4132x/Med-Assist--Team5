import React from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';

export default function AdminNavbar({ pageTitle = 'Dashboard' }) {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();

  const handleLogout = () => {
    authService.logout();
  };

  return (
    <header style={{
      height: '70px',
      backgroundColor: '#FFFFFF',
      borderBottom: '1px solid var(--border-color)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 2rem',
      position: 'sticky',
      top: 0,
      zIndex: 10
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-primary)' }}>
          {pageTitle}
        </h2>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            backgroundColor: 'var(--light-green)',
            color: 'var(--dark-green)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 700,
            fontSize: '0.95rem'
          }}>
            {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'A'}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              {user?.full_name || 'Administrator'}
            </span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              {user?.email || 'admin@medassist.ai'}
            </span>
          </div>
        </div>

        <button
          onClick={handleLogout}
          className="btn btn-secondary btn-sm"
          style={{ border: '1px solid var(--border-color)' }}
          title="Sign Out"
        >
          Sign Out
        </button>
      </div>
    </header>
  );
}
