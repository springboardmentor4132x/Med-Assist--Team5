
import { useCallback, useEffect, useState } from 'react'
import { adminService } from '../services/adminService'

export default function AdminUsers({ token }) {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')

  const loadUsers = useCallback(async (showLoading = false) => {
    try {
      if (showLoading) setLoading(true)
      setError('')

      const data = await adminService.getUsers(token)
      setUsers(data.items || [])
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
      <h1 className="page-title">Manage Users</h1>
      <p className="page-subtitle">
        View and monitor all registered users.
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
                  <th>Role</th>
                  <th>Status</th>
                  <th>Registered On</th>
                </tr>
              </thead>

              <tbody>
                {filteredUsers.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.full_name || 'Not recorded'}</td>
                    <td>{user.email || 'Not recorded'}</td>
                    <td>{user.role || 'Not assigned'}</td>
                    <td>{user.is_active ? 'Active' : 'Inactive'}</td>
                    <td>
                      {user.created_at
                        ? new Date(user.created_at).toLocaleDateString()
                        : 'Not recorded'}
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
