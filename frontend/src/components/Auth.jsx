
import { useState } from 'react'

function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true)

  const [form, setForm] = useState({
    full_name: '',
    email: '',
    password: '',
    role: 'patient',
  })

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm((previous) => ({
      ...previous,
      [e.target.name]: e.target.value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const endpoint = isLogin ? 'login' : 'register'

      const payload = isLogin
        ? {
            email: form.email,
            password: form.password,
          }
        : form

      const response = await fetch(
        `http://127.0.0.1:8000/auth/${endpoint}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        }
      )

      const result = await response.json()

      if (!response.ok) {
        const message = Array.isArray(result.detail)
          ? result.detail.map((item) => item.msg).join(', ')
          : result.detail || 'Authentication failed.'

        throw new Error(message)
      }

      if (isLogin) {
        onLogin(result)
      } else {
        setIsLogin(true)
        setForm({
          full_name: '',
          email: form.email,
          password: '',
          role: 'patient',
        })
        setError('Registration successful! Please log in.')
      }
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  const switchMode = () => {
    setIsLogin((previous) => !previous)
    setError('')
    setForm({
      full_name: '',
      email: '',
      password: '',
      role: 'patient',
    })
  }

  return (
    <div className="auth-container">
      <div className="auth-card">

        <div className="auth-brand">
          <div className="auth-logo">✚</div>
          <h1>MedAssist AI</h1>
          <p>Intelligent Healthcare Assistant</p>
        </div>

        <div className="auth-heading">
          <h2>{isLogin ? 'Welcome Back!' : 'Create Your Account'}</h2>
          <p>
            {isLogin
              ? 'Sign in to access your healthcare dashboard.'
              : 'Join MedAssist AI and get started today.'}
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>

          {!isLogin && (
            <>
              <div className="auth-field">
                <label htmlFor="full_name">Full Name</label>
                <input
                  id="full_name"
                  type="text"
                  name="full_name"
                  placeholder="Enter your full name"
                  value={form.full_name}
                  onChange={handleChange}
                  required
                  minLength="2"
                  maxLength="100"
                />
              </div>

              <div className="auth-field">
                <label htmlFor="role">Register As</label>
                <select
                  id="role"
                  name="role"
                  value={form.role}
                  onChange={handleChange}
                  required
                >
                  <option value="patient">Patient</option>
                  <option value="doctor">Doctor</option>
                  <option value="clinic">Clinic</option>
                </select>
                <small>Select the account type you want to create.</small>
              </div>
            </>
          )}

          <div className="auth-field">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              name="email"
              placeholder="Enter your email address"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="auth-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              name="password"
              placeholder="Enter your password"
              value={form.password}
              onChange={handleChange}
              required
              minLength="8"
              maxLength="128"
            />
            {!isLogin && (
              <small>Password must contain at least 8 characters.</small>
            )}
          </div>

          {error && (
            <div
              className={`auth-message ${
                error.startsWith('Registration successful')
                  ? 'auth-success'
                  : 'auth-error'
              }`}
              role="alert"
            >
              {error}
            </div>
          )}

          <button
            type="submit"
            className="auth-submit"
            disabled={loading}
          >
            {loading
              ? 'Please wait...'
              : isLogin
                ? 'Sign In'
                : 'Create Account'}
          </button>

        </form>

        <div className="auth-footer">
          <span>
            {isLogin
              ? "Don't have an account?"
              : 'Already have an account?'}
          </span>

          <button
            type="button"
            className="auth-toggle"
            onClick={switchMode}
          >
            {isLogin ? 'Create Account' : 'Sign In'}
          </button>
        </div>

        <div className="auth-security">
          <span>🔒</span>
          Secure Authentication | MedAssist AI
        </div>

      </div>
    </div>
  )
}

export default Auth
