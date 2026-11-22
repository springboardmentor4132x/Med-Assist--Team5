
import { useCallback, useEffect, useState } from 'react'
import { adminService } from '../services/adminService'

const ROLES = ['patient', 'doctor', 'clinic', 'admin']

export default function AdminRoles({ token }) {
  const [users, setUsers] = useState([])
  const [selectedRoles, setSelectedRoles] = useState({})
  const [loading, setLoading] = useState(true)
  const [savingId, setSavingId] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [search, setSearch] = useState('')

  const loadUsers = useCallback(async (showLoading = false) => {
    try {
      if (showLoading) {
        setLoading(true)
      }

      setError('')
      const data = await adminService.getUsers(token)
      const items = data.items || []
      setUsers(items)

      const roles = {}
      items.forEach((user) => {
        roles[user.id] = (user.role || 'patient').toLowerCase()
      })
      setSelectedRoles(roles)
    } catch (err) {
      setError(err.message || 'Unable to load users.')
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    const timer = setTimeout(() => {
      loadUsers(true)
    }, 0)

    return () => clearTimeout(timer)
  }, [loadUsers])

  async function handleRoleUpdate(user) {
    const newRole = selectedRoles[user.id]

    if (!newRole || newRole === user.role?.toLowerCase()) {
      setMessage('No role changes to save.')
      return
    }

    try {
      setSavingId(user.id)
      setError('')
      setMessage('')

      await adminService.updateUserRole(token, user.id, newRole)

      setMessage(`Role updated successfully for ${user.full_name}.`)
      await loadUsers()
    } catch (err) {
      setError(err.message || 'Unable to update role.')
    } finally {
      setSavingId(null)
    }
  }

  const filteredUsers = users.filter((user) => {
    const query = search.toLowerCase()
    return (
      String(user.id).includes(query) ||
      user.full_name?.toLowerCase().includes(query) ||
      user.email?.toLowerCase().includes(query) ||
      user.role?.toLowerCase().includes(query)
    )
  })

  return (
    <section className="card">
      <h1 className="page-title">Manage Roles</h1>
      <p className="page-subtitle">
        View and update roles assigned to registered users.
      </p>

      <input
        type="text"
        className="admin-search"
        placeholder="Search by name, email, role or ID..."
        value={search}
        onChange={(event) => setSearch(event.target.value)}
      />

      <button
        className="btn btn-secondary"
        onClick={() => loadUsers(true)}
        disabled={loading}
      >
        Refresh Users
      </button>

      {error && <p className="alert alert-error">{error}</p>}
      {message && <p className="alert">{message}</p>}

      {loading ? (
        <p>Loading users...</p>
      ) : (
        <>
          <p>Total users: {filteredUsers.length}</p>

          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Current Role</th>
                  <th>New Role</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredUsers.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.full_name}</td>
                    <td>{user.email}</td>
                    <td>{user.role}</td>
                    <td>
                      <select
                        value={selectedRoles[user.id] || 'patient'}
                        onChange={(event) =>
                          setSelectedRoles((previous) => ({
                            ...previous,
                            [user.id]: event.target.value,
                          }))
                        }
                      >
                        {ROLES.map((role) => (
                          <option key={role} value={role}>
                            {role.charAt(0).toUpperCase() + role.slice(1)}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td>
                      <button
                        className="btn btn-secondary"
                        onClick={() => handleRoleUpdate(user)}
                        disabled={savingId === user.id}
                      >
                        {savingId === user.id ? 'Saving...' : 'Update'}
                      </button>
                    </td>
                  </tr>
                ))}

                {filteredUsers.length === 0 && (
                  <tr>
                    <td colSpan="6">No users found.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}
    </section>
  )
}
