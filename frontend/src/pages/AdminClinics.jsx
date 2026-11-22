
import { useCallback, useEffect, useState } from 'react'
import { adminService } from '../services/adminService'

export default function AdminClinics({ token }) {
  const [clinics, setClinics] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')

  const loadClinics = useCallback(async (showLoading = false) => {
    try {
      if (showLoading) {
        setLoading(true)
      }

      setError('')
      const data = await adminService.getClinics(token)
      setClinics(data.items || [])
    } catch (err) {
      setError(err.message || 'Unable to load clinics.')
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    const timer = setTimeout(() => {
      loadClinics(true)
    }, 0)

    return () => clearTimeout(timer)
  }, [loadClinics])

  const filteredClinics = clinics.filter((clinic) => {
    const query = search.toLowerCase()
    return (
      String(clinic.id).includes(query) ||
      clinic.full_name?.toLowerCase().includes(query) ||
      clinic.email?.toLowerCase().includes(query)
    )
  })

  return (
    <section className="card">
      <h1 className="page-title">Manage Clinics</h1>
      <p className="page-subtitle">
        View and monitor registered clinics.
      </p>

      <input
        type="text"
        className="admin-search"
        placeholder="Search by clinic name, email or ID..."
        value={search}
        onChange={(event) => setSearch(event.target.value)}
      />

      <button
        className="btn btn-secondary"
        onClick={() => loadClinics(true)}
        disabled={loading}
      >
        Refresh Clinics
      </button>

      {error && <p className="alert alert-error">{error}</p>}

      {loading ? (
        <p>Loading clinics...</p>
      ) : (
        <>
          <p>Total clinics: {filteredClinics.length}</p>

          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Clinic Name</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Registered On</th>
                </tr>
              </thead>

              <tbody>
                {filteredClinics.map((clinic) => (
                  <tr key={clinic.id}>
                    <td>{clinic.id}</td>
                    <td>{clinic.full_name || 'Not recorded'}</td>
                    <td>{clinic.email || 'Not recorded'}</td>
                    <td>{clinic.is_active ? 'Active' : 'Inactive'}</td>
                    <td>
                      {clinic.created_at
                        ? new Date(clinic.created_at).toLocaleDateString()
                        : 'Not recorded'}
                    </td>
                  </tr>
                ))}

                {filteredClinics.length === 0 && (
                  <tr>
                    <td colSpan="5">No clinics found.</td>
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
