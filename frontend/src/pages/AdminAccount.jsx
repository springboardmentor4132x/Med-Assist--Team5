
import { useCallback, useEffect, useState } from 'react'
import { adminService } from '../services/adminService'

export default function AdminAccount({ token }) {
  const [account, setAccount] = useState({
    full_name: '',
    email: '',
  })

  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

    const loadAccount = useCallback(async () => {
    try {
      const data = await adminService.getAccount(token)

      setAccount({
        full_name: data.full_name || '',
        email: data.email || '',
      })
      setError('')
    } catch (err) {
      setError(err.message || 'Unable to load account.')
    } finally {
      setLoading(false)
    }
  }, [token])

    useEffect(() => {
    const timer = setTimeout(() => {
      loadAccount()
    }, 0)

    return () => clearTimeout(timer)
  }, [loadAccount])

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setMessage('')

    if (newPassword && newPassword.length < 8) {
      setError('New password must contain at least 8 characters.')
      return
    }

    if (newPassword && !currentPassword) {
      setError('Enter your current password to change your password.')
      return
    }

    try {
      setSaving(true)

      const payload = {
        full_name: account.full_name.trim(),
        email: account.email.trim(),
      }

      if (newPassword) {
        payload.current_password = currentPassword
        payload.new_password = newPassword
      }

      const updated = await adminService.updateAccount(token, payload)

      setAccount({
        full_name: updated.full_name || '',
        email: updated.email || '',
      })

      setCurrentPassword('')
      setNewPassword('')
      setMessage('Account settings updated successfully.')
    } catch (err) {
      setError(err.message || 'Unable to update account.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return <section className="card">Loading account settings...</section>
  }

  return (
    <section className="card">
      <h1 className="page-title">Account Settings</h1>
      <p className="page-subtitle">
        View and update your administrator account.
      </p>

      {error && <p className="alert alert-error">{error}</p>}
      {message && <p className="alert">{message}</p>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Full Name</label>
          <input
            type="text"
            value={account.full_name}
            onChange={(event) =>
              setAccount({ ...account, full_name: event.target.value })
            }
            required
          />
        </div>

        <div className="form-group">
          <label>Email Address</label>
          <input
            type="email"
            value={account.email}
            onChange={(event) =>
              setAccount({ ...account, email: event.target.value })
            }
            required
          />
        </div>

        <h2>Change Password</h2>
        <p>Leave these fields empty if you do not want to change your password.</p>

        <div className="form-group">
          <label>Current Password</label>
          <input
            type="password"
            value={currentPassword}
            onChange={(event) => setCurrentPassword(event.target.value)}
            autoComplete="current-password"
          />
        </div>

        <div className="form-group">
          <label>New Password</label>
          <input
            type="password"
            value={newPassword}
            onChange={(event) => setNewPassword(event.target.value)}
            minLength={8}
            autoComplete="new-password"
          />
        </div>

        <button className="btn btn-primary" type="submit" disabled={saving}>
          {saving ? 'Saving...' : 'Save Changes'}
        </button>

        <button
          className="btn btn-secondary"
          type="button"
          onClick={loadAccount}
          disabled={saving || loading}
        >
          Refresh Account
        </button>
      </form>
    </section>
  )
}
