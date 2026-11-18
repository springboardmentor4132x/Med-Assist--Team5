import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';

export default function AdminSidebar() {
  const navigate = useNavigate();

  const navItems = [
    { label: 'Dashboard', path: '/admin-dashboard', icon: '📊' },
    { label: 'Manage Users', path: '/manage-users', icon: '👥' },
    { label: 'Manage Patients', path: '/manage-patients', icon: '🩺' },
    { label: 'Manage Doctors', path: '/manage-doctors', icon: '👨‍⚕️' },
    { label: 'Manage Clinics', path: '/manage-clinics', icon: '🏥' },
    { label: 'Manage Roles', path: '/manage-roles', icon: '🛡️' },
    { label: 'Account Settings', path: '/account-settings', icon: '⚙️' },
  ];

  const handleLogout = () => {
    authService.logout();
  };

  return (
    <aside style={{
      width: '260px',
      backgroundColor: '#FFFFFF',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      flexShrink: 0,
      minHeight: '100vh',
    }}>
      {/* Brand Header */}
      <div style={{
        padding: '1.5rem',
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
      }}>
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '8px',
          backgroundColor: 'var(--primary-green)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#ffffff',
          fontWeight: 'bold',
          fontSize: '1.2rem'
        }}>
          +
        </div>
        <div>
          <h1 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
            MedAssist <span style={{ color: 'var(--primary-green)' }}>AI</span>
          </h1>
          <p style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Admin Portal
          </p>
        </div>
      </div>

      {/* Navigation List */}
      <nav style={{ padding: '1rem 0.75rem', flex: 1, display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              padding: '0.75rem 1rem',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.875rem',
              fontWeight: isActive ? 600 : 500,
              color: isActive ? 'var(--dark-green)' : 'var(--text-secondary)',
              backgroundColor: isActive ? 'var(--light-green)' : 'transparent',
              textDecoration: 'none',
              transition: 'var(--transition)',
              borderLeft: isActive ? '3px solid var(--primary-green)' : '3px solid transparent'
            })}
          >
            <span style={{ fontSize: '1.1rem' }}>{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer / Logout */}
      <div style={{ padding: '1rem', borderTop: '1px solid var(--border-color)' }}>
        <button
          onClick={handleLogout}
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            padding: '0.75rem 1rem',
            borderRadius: 'var(--radius-md)',
            border: 'none',
            background: 'transparent',
            color: 'var(--error)',
            fontSize: '0.875rem',
            fontWeight: 500,
            cursor: 'pointer',
            transition: 'var(--transition)'
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--error-bg)'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
        >
          <span style={{ fontSize: '1.1rem' }}>🚪</span>
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
