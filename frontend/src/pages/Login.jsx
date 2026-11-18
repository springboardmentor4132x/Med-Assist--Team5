import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../services/authService';

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  // Mode: true = Sign Up (Register first), false = Log In (Direct login for existing users)
  const [isSignUp, setIsSignUp] = useState(false);

  // Common Fields
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  // Sign Up Specific Fields
  const [fullName, setFullName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [selectedRole, setSelectedRole] = useState('Patient');

  // Status & Feedback
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Check if redirected due to expired token
  const queryParams = new URLSearchParams(location.search);
  const isExpired = queryParams.get('expired') === 'true';

  const handleRoleRedirection = (role) => {
    if (role === 'Admin') {
      navigate('/admin-dashboard', { replace: true });
    } else if (role === 'Doctor') {
      navigate('/doctor-dashboard', { replace: true });
    } else if (role === 'Clinic') {
      navigate('/clinic-dashboard', { replace: true });
    } else {
      navigate('/patient-dashboard', { replace: true });
    }
  };

  // Submit Login
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    if (!email || !password) {
      setErrorMessage('Please enter both your email address and password.');
      return;
    }

    try {
      setLoading(true);
      const data = await authService.login(email, password);
      handleRoleRedirection(data.user.role);
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

  // Submit Sign Up
  const handleSignUpSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    if (!fullName || !email || !password) {
      setErrorMessage('Please complete all required fields.');
      return;
    }

    if (password.length < 6) {
      setErrorMessage('Password must be at least 6 characters long.');
      return;
    }

    if (password !== confirmPassword) {
      setErrorMessage('Passwords do not match. Please re-enter.');
      return;
    }

    try {
      setLoading(true);
      // Register account
      await authService.register(fullName, email, password, selectedRole);

      // Automatically log in with new credentials
      const loginData = await authService.login(email, password);
      handleRoleRedirection(loginData.user.role);
    } catch (err) {
      console.error('Sign up error:', err);
      if (err.response && err.response.data && err.response.data.detail) {
        setErrorMessage(err.response.data.detail);
      } else {
        setErrorMessage('Account registration failed. Please try again.');
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
            Healthcare Administration & Clinical Care
          </div>

          <h2 style={{ fontSize: '2.4rem', fontWeight: 700, color: '#172B24', lineHeight: 1.2, marginBottom: '1.25rem' }}>
            Unified Health & User Management
          </h2>
          <p style={{ color: '#4B6358', fontSize: '1.05rem', lineHeight: 1.6, marginBottom: '2rem' }}>
            Secure authentication for patients, licensed medical doctors, clinical centers, and health administrators.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#2C493D' }}>
              <span style={{ color: 'var(--primary-green)', fontWeight: 'bold' }}>✓</span>
              <span style={{ fontSize: '0.95rem' }}>Sign up once to create your secure health identity</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#2C493D' }}>
              <span style={{ color: 'var(--primary-green)', fontWeight: 'bold' }}>✓</span>
              <span style={{ fontSize: '0.95rem' }}>Already registered? Log in directly with your email</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#2C493D' }}>
              <span style={{ color: 'var(--primary-green)', fontWeight: 'bold' }}>✓</span>
              <span style={{ fontSize: '0.95rem' }}>Automated role redirection to your designated workspace</span>
            </div>
          </div>
        </div>

        {/* Footer info */}
        <div style={{ fontSize: '0.8rem', color: '#728078' }}>
          © 2026 MedAssist AI Healthcare Systems. All rights reserved.
        </div>
      </div>

      {/* Right Column: Sign Up & Log In Portal */}
      <div style={{
        flex: 1,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '3rem 2rem',
        backgroundColor: '#FFFFFF'
      }}>
        <div style={{ width: '100%', maxWidth: '460px' }}>
          {/* Header Title */}
          <div style={{ marginBottom: '1.75rem' }}>
            <h1 style={{ fontSize: '1.85rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
              {isSignUp ? 'Create an Account' : 'Welcome Back'}
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
              {isSignUp
                ? 'Sign up below, or log in directly if you already have an account.'
                : 'Enter your credentials, or sign up first if you are new.'}
            </p>
          </div>

          {/* Mode Switcher Tabs */}
          <div style={{
            display: 'flex',
            backgroundColor: '#F0F5F2',
            padding: '4px',
            borderRadius: 'var(--radius-md)',
            marginBottom: '1.75rem'
          }}>
            <button
              type="button"
              onClick={() => {
                setIsSignUp(true);
                setErrorMessage('');
                setSuccessMessage('');
              }}
              style={{
                flex: 1,
                padding: '0.65rem 1rem',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: isSignUp ? '#FFFFFF' : 'transparent',
                color: isSignUp ? 'var(--dark-green)' : 'var(--text-secondary)',
                fontWeight: isSignUp ? 600 : 500,
                boxShadow: isSignUp ? '0 1px 4px rgba(0,0,0,0.08)' : 'none',
                cursor: 'pointer',
                transition: 'var(--transition)',
                fontSize: '0.875rem'
              }}
            >
              1. Sign Up (New User)
            </button>
            <button
              type="button"
              onClick={() => {
                setIsSignUp(false);
                setErrorMessage('');
                setSuccessMessage('');
              }}
              style={{
                flex: 1,
                padding: '0.65rem 1rem',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: !isSignUp ? '#FFFFFF' : 'transparent',
                color: !isSignUp ? 'var(--dark-green)' : 'var(--text-secondary)',
                fontWeight: !isSignUp ? 600 : 500,
                boxShadow: !isSignUp ? '0 1px 4px rgba(0,0,0,0.08)' : 'none',
                cursor: 'pointer',
                transition: 'var(--transition)',
                fontSize: '0.875rem'
              }}
            >
              2. Log In (Existing User)
            </button>
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

          {successMessage && (
            <div className="alert alert-success">
              <span>{successMessage}</span>
            </div>
          )}

          {/* FORM 1: SIGN UP */}
          {isSignUp ? (
            <form onSubmit={handleSignUpSubmit}>
              <div className="form-group">
                <label className="form-label" htmlFor="fullName">Full Name</label>
                <input
                  id="fullName"
                  type="text"
                  className="form-input"
                  placeholder="e.g. Sarah Jenkins"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="signup-email">Email Address</label>
                <input
                  id="signup-email"
                  type="email"
                  className="form-input"
                  placeholder="name@medassist.ai"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Account Role</label>
                <select
                  className="form-select"
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value)}
                >
                  <option value="Patient">Patient (Healthcare Recipient)</option>
                  <option value="Doctor">Doctor (Licensed Medical Practitioner)</option>
                  <option value="Clinic">Clinic (Healthcare Facility / Hospital)</option>
                </select>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.25rem', display: 'block' }}>
                  * Administrator accounts are provisioned via system governance.
                </span>
              </div>

              <div className="form-group">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                  <label className="form-label" htmlFor="signup-password" style={{ marginBottom: 0 }}>Password</label>
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
                  id="signup-password"
                  type={showPassword ? 'text' : 'password'}
                  className="form-input"
                  placeholder="Minimum 6 characters"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="confirm-password">Confirm Password</label>
                <input
                  id="confirm-password"
                  type={showPassword ? 'text' : 'password'}
                  className="form-input"
                  placeholder="Repeat your password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                style={{ width: '100%', padding: '0.8rem', fontSize: '0.95rem', marginTop: '0.5rem' }}
                disabled={loading}
              >
                {loading ? 'Creating Account & Signing In...' : 'Sign Up & Continue'}
              </button>

              <div style={{ textAlign: 'center', marginTop: '1.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                Already signed up before?{' '}
                <button
                  type="button"
                  onClick={() => {
                    setIsSignUp(false);
                    setErrorMessage('');
                    setSuccessMessage('');
                  }}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--primary-green)',
                    fontWeight: 600,
                    cursor: 'pointer',
                    textDecoration: 'underline'
                  }}
                >
                  Log In directly
                </button>
              </div>
            </form>
          ) : (
            /* FORM 2: DIRECT LOG IN */
            <form onSubmit={handleLoginSubmit}>
              <div className="form-group">
                <label className="form-label" htmlFor="login-email">Email Address</label>
                <input
                  id="login-email"
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
                  <label className="form-label" htmlFor="login-password" style={{ marginBottom: 0 }}>Password</label>
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
                  id="login-password"
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
                <a
                  href="#forgot"
                  onClick={(e) => {
                    e.preventDefault();
                    alert('Please contact your Healthcare System Administrator to reset your credentials.');
                  }}
                  style={{ color: 'var(--primary-green)', textDecoration: 'none', fontWeight: 500 }}
                >
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

              <div style={{ textAlign: 'center', marginTop: '1.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                Don't have an account yet?{' '}
                <button
                  type="button"
                  onClick={() => {
                    setIsSignUp(true);
                    setErrorMessage('');
                    setSuccessMessage('');
                  }}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--primary-green)',
                    fontWeight: 600,
                    cursor: 'pointer',
                    textDecoration: 'underline'
                  }}
                >
                  Sign Up first
                </button>
              </div>
            </form>
          )}

          {/* Quick Demo Credentials Assistant */}
          <div style={{
            marginTop: '2rem',
            padding: '1.25rem',
            borderRadius: 'var(--radius-md)',
            backgroundColor: '#F8FAF9',
            border: '1px solid var(--border-color)',
            fontSize: '0.8rem'
          }}>
            <strong style={{ color: 'var(--text-primary)', display: 'block', marginBottom: '0.5rem' }}>
              System Demo Accounts (Ready to Test):
            </strong>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.4rem', color: 'var(--text-secondary)' }}>
              <div><strong>Admin:</strong> admin@medassist.ai</div>
              <div><strong>Doctor:</strong> doctor@medassist.ai</div>
              <div><strong>Clinic:</strong> clinic@medassist.ai</div>
              <div><strong>Patient:</strong> patient@medassist.ai</div>
            </div>
            <div style={{ marginTop: '0.4rem', color: 'var(--text-secondary)' }}>
              Password: <code style={{ backgroundColor: '#E5ECE7', padding: '0.1rem 0.3rem', borderRadius: '4px' }}>Admin@123 / Doctor@123 / etc.</code>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
