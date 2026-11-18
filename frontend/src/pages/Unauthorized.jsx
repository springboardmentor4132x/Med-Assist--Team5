import React from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';

export default function Unauthorized() {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#F7FAF8',
      padding: '2rem',
      fontFamily: 'Inter, sans-serif'
    }}>
      <div className="card" style={{ maxWidth: '480px', width: '100%', textAlign: 'center', padding: '2.5rem 2rem' }}>
        <div style={{
          width: '64px',
          height: '64px',
          borderRadius: '50%',
          backgroundColor: '#FEEBEB',
          color: '#DC5555',
          fontSize: '2rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 1.5rem auto',
          fontWeight: 'bold'
        }}>
          !
        </div>

        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.75rem', color: 'var(--text-primary)' }}>
          Access Denied
        </h1>

        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '2rem' }}>
          You are signed in as <strong>{user?.full_name || 'User'}</strong> with the role of{' '}
          <span className="badge badge-patient">{user?.role || 'Guest'}</span>.
          This area is strictly restricted to authorized system Administrators.
        </p>

        <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
          <button className="btn btn-secondary" onClick={() => authService.logout()}>
            Sign Out
          </button>
          <button className="btn btn-primary" onClick={() => navigate('/login')}>
            Return to Login
          </button>
        </div>
      </div>
    </div>
  );
}
