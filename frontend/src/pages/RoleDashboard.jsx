import React from 'react';
import { authService } from '../services/authService';

export default function RoleDashboard({ title, description, icon }) {
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
      <div className="card" style={{ maxWidth: '540px', width: '100%', textAlign: 'center', padding: '3rem 2rem' }}>
        <div style={{
          width: '72px',
          height: '72px',
          borderRadius: '50%',
          backgroundColor: '#E9F8F0',
          fontSize: '2.25rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 1.5rem auto'
        }}>
          {icon}
        </div>

        <h1 style={{ fontSize: '1.75rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
          {title}
        </h1>

        <div style={{ marginBottom: '1.5rem' }}>
          <span className="badge badge-patient" style={{ fontSize: '0.85rem' }}>
            Logged in as {user?.full_name} ({user?.role})
          </span>
        </div>

        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '2rem' }}>
          {description}
        </p>

        <button className="btn btn-secondary" onClick={() => authService.logout()}>
          Sign Out of Account
        </button>
      </div>
    </div>
  );
}
