
import { useCallback, useEffect, useState } from 'react'
import { adminService } from '../services/adminService'

export default function AdminPatients({ token }) {
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
  })

  const loadPatients = useCallback(async (showLoading = false) => {
    try {
      if (showLoading) {
        setLoading(true)
      }

      setError('')
      const data = await adminService.getPatients(token)
      setPatients(data.items || [])
    } catch (err) {
      setError(err.message || 'Unable to load patients.')
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    const timer = setTimeout(() => {
      loadPatients(true)
    }, 0)

    return () => clearTimeout(timer)
  }, [loadPatients])

  function handleInputChange(event) {
    const { name, value } = event.target
    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  async function handleAddPatient(event) {
    event.preventDefault()

    try {
      setSaving(true)
      setError('')
      setSuccess('')

      await adminService.createUser(token, {
        ...formData,
        role: 'patient',
      })

      setSuccess('Patient account created successfully!')
      setFormData({ full_name: '', email: '', password: '' })
      setShowForm(false)
      await loadPatients()
    } catch (err) {
      setError(err.message || 'Unable to create patient.')
    } finally {
      setSaving(false)
    }
  }

  async function handleDeletePatient(patient) {
    const confirmed = window.confirm(
      `Are you sure you want to permanently delete ${patient.full_name}? Patient symptom history will be preserved but unlinked from this account.`
    )

    if (!confirmed) return

    try {
      setError('')
      setSuccess('')

      await adminService.deleteUser(token, patient.id)

      setSuccess('Patient account deleted successfully.')
      await loadPatients()
    } catch (err) {
      setError(err.message || 'Unable to delete patient.')
    }
  }

  const filteredPatients = patients.filter((patient) => {
    const query = search.toLowerCase()
    return (
      String(patient.id).includes(query) ||
      patient.full_name?.toLowerCase().includes(query) ||
      patient.email?.toLowerCase().includes(query)
    )
  })

  return (
    <section className="card">
      <h1 className="page-title">Manage Patients</h1>
      <p className="page-subtitle">
        View, add and manage registered patients.
      </p>

      <button
        className="btn btn-primary"
        onClick={() => {
          setShowForm(!showForm)
          setError('')
          setSuccess('')
        }}
      >
        {showForm ? 'Cancel' : '+ Add Patient'}
      </button>

      {showForm && (
        <form onSubmit={handleAddPatient} className="admin-form">
          <h3>Add New Patient</h3>

          <input
            type="text"
            name="full_name"
            placeholder="Full name"
            value={formData.full_name}
            onChange={handleInputChange}
            minLength={2}
            maxLength={100}
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Email address"
            value={formData.email}
            onChange={handleInputChange}
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password (minimum 8 characters)"
            value={formData.password}
            onChange={handleInputChange}
            minLength={8}
            maxLength={128}
            required
          />

          <button
            type="submit"
            className="btn btn-primary"
            disabled={saving}
          >
            {saving ? 'Creating...' : 'Create Patient'}
          </button>
        </form>
      )}

      {success && <p className="alert alert-success">{success}</p>}
      {error && <p className="alert alert-error">{error}</p>}

      <input
        type="text"
        className="admin-search"
        placeholder="Search by name, email or ID..."
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        />

      <button
        className="btn btn-secondary"
        onClick={() => loadPatients(true)}
        disabled={loading}
      >
        Refresh Patients
      </button>

      {loading ? (
        <p>Loading patients...</p>
      ) : (
        <>
          <p>Total patients: {filteredPatients.length}</p>

          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Registered On</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredPatients.map((patient) => (
                  <tr key={patient.id}>
                    <td>{patient.id}</td>
                    <td>{patient.full_name || 'Not recorded'}</td>
                    <td>{patient.email || 'Not recorded'}</td>
                    <td>
                      {patient.is_active ? 'Active' : 'Inactive'}
                    </td>
                    <td>
                      {patient.created_at
                        ? new Date(patient.created_at).toLocaleDateString()
                        : 'Not recorded'}
                    </td>
                    <td>
                      <button
                        className="btn btn-danger"
                        onClick={() => handleDeletePatient(patient)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}

                {filteredPatients.length === 0 && (
                  <tr>
                    <td colSpan="6">No patients found.</td>
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
