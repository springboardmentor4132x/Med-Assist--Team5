import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../services/authService';

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Check if redirected due to expired token
  const queryParams = new URLSearchParams(location.search);
  const isExpired = queryParams.get('expired') === 'true';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!email || !password) {
      setErrorMessage('Please enter both email address and password.');
      return;
    }

    try {
      setLoading(true);
      const data = await authService.login(email, password);
      
      const role = data.user.role;
      // Backend-determined role redirection
      if (role === 'Admin') {
        navigate('/admin-dashboard', { replace: true });
      } else if (role === 'Doctor') {
        navigate('/doctor-dashboard', { replace: true });
      } else if (role === 'Clinic') {
        navigate('/clinic-dashboard', { replace: true });
      } else {
        navigate('/patient-dashboard', { replace: true });
      }
    } catch (err) {
      console.error('Login error:', err);
      if (err.response && err.response.data && err.response.data.detail) {
        setErrorMessage(err.response.data.detail);
      } else {
        setErrorMessage('Unable to connect to the authentication server. Please check your network.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      minHeight: '100vh',
      width: '100vw',
      backgroundColor: '#FFFFFF',
      fontFamily: 'Inter, sans-serif'
    }}>
      {/* Left Column: Healthcare Brand & Showcase */}
      <div style={{
        flex: 1,
        backgroundColor: '#E9F8F0',
        padding: '3.5rem',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        borderRight: '1px solid #D5EFE2',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Brand Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '10px',
            backgroundColor: 'var(--primary-green)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFFFFF',
            fontSize: '1.4rem',
            fontWeight: 700
          }}>
            +
          </div>
          <span style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
            MedAssist <span style={{ color: 'var(--primary-green)' }}>AI</span>
          </span>
        </div>

        {/* Center Illustration & Message */}
        <div style={{ maxWidth: '520px', margin: '2rem 0' }}>
          <div style={{
            display: 'inline-block',
            padding: '0.35rem 0.85rem',
            borderRadius: '9999px',
            backgroundColor: '#D1F2DF',
            color: 'var(--dark-green)',
            fontSize: '0.8rem',
            fontWeight: 600,
            marginBottom: '1.25rem'
          }}>
            Intelligent Healthcare Governance
          </div>

          <h2 style={{ fontSize: '2.4rem', fontWeight: 700, color: '#172B24', lineHeight: 1.2, marginBottom: '1.25rem' }}>
            Unified Clinical & Administration Portal
          </h2>
          <p style={{ color: '#4B6358', fontSize: '1.05rem', lineHeight: 1.6, marginBottom: '2rem' }}>
            Empowering healthcare providers, administrators, clinics and patients with secure role-based access, real-time analytics, and auditable account governance.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#2C493D' }}>
              <span style={{ color: 'var(--primary-green)', fontWeight: 'bold' }}>✓</span>
              <span style={{ fontSize: '0.95rem' }}>HIPAA & Role-Based Access Control (RBAC)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#2C493D' }}>
              <span style={{ color: 'var(--primary-green)', fontWeight: 'bold' }}>✓</span>
              <span style={{ fontSize: '0.95rem' }}>Centralized user, doctor, clinic & patient management</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#2C493D' }}>
              <span style={{ color: 'var(--primary-green)', fontWeight: 'bold' }}>✓</span>
              <span style={{ fontSize: '0.95rem' }}>Real-time PostgreSQL analytics & auditable operations</span>
            </div>
          </div>
        </div>

        {/* Footer info */}
        <div style={{ fontSize: '0.8rem', color: '#728078' }}>
          © 2026 MedAssist AI Healthcare Systems. All rights reserved.
        </div>
      </div>

      {/* Right Column: Common Login Form */}
      <div style={{
        flex: 1,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '3rem 2rem',
        backgroundColor: '#FFFFFF'
      }}>
        <div style={{ width: '100%', maxWidth: '440px' }}>
          <div style={{ marginBottom: '2rem' }}>
            <h1 style={{ fontSize: '1.85rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
              Welcome back
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
              Please enter your credentials to access your dashboard.
            </p>
          </div>

          {isExpired && (
            <div className="alert alert-error">
              <span>Your session has expired. Please log in again to continue.</span>
            </div>
          )}

          {errorMessage && (
            <div className="alert alert-error">
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label" htmlFor="email">Email Address</label>
              <input
                id="email"
                type="email"
                className="form-input"
                placeholder="name@medassist.ai"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
                required
              />
            </div>

            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                <label className="form-label" htmlFor="password" style={{ marginBottom: 0 }}>Password</label>
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--primary-green)',
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    fontWeight: 500
                  }}
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                className="form-input"
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                required
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', fontSize: '0.85rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-secondary)' }}>
                <input type="checkbox" style={{ accentColor: 'var(--primary-green)' }} />
                <span>Remember this workstation</span>
              </label>
              <a href="#forgot" onClick={(e) => { e.preventDefault(); alert('Please contact the IT Healthcare System Administrator to reset your credentials.'); }} style={{ color: 'var(--primary-green)', textDecoration: 'none', fontWeight: 500 }}>
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              style={{ width: '100%', padding: '0.8rem', fontSize: '0.95rem' }}
              disabled={loading}
            >
              {loading ? 'Authenticating...' : 'Sign In to Dashboard'}
            </button>
          </form>

          {/* Quick Demo Credentials Assistant */}
          <div style={{
            marginTop: '2.5rem',
            padding: '1.25rem',
            borderRadius: 'var(--radius-md)',
            backgroundColor: '#F8FAF9',
            border: '1px solid var(--border-color)',
            fontSize: '0.8rem'
          }}>
            <strong style={{ color: 'var(--text-primary)', display: 'block', marginBottom: '0.5rem' }}>
              System Demo Credentials (Pre-seeded):
            </strong>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.4rem', color: 'var(--text-secondary)' }}>
              <div><strong>Admin:</strong> admin@medassist.ai</div>
              <div><strong>Doctor:</strong> doctor@medassist.ai</div>
              <div><strong>Clinic:</strong> clinic@medassist.ai</div>
              <div><strong>Patient:</strong> patient@medassist.ai</div>
            </div>
            <div style={{ marginTop: '0.4rem', color: 'var(--text-secondary)' }}>
              Default Password for all: <code style={{ backgroundColor: '#E5ECE7', padding: '0.1rem 0.3rem', borderRadius: '4px' }}>Admin@123 / Doctor@123 / etc.</code>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
