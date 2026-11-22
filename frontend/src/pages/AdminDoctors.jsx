
import { useCallback, useEffect, useState } from 'react'
import { adminService } from '../services/adminService'

export default function AdminDoctors({ token }) {
  const [doctors, setDoctors] = useState([])
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

  const loadDoctors = useCallback(async (showLoading = false) => {
    try {
      if (showLoading) {
        setLoading(true)
      }

      setError('')

      const data = await adminService.getDoctors(token)
      setDoctors(data.items || [])
    } catch (err) {
      setError(err.message || 'Unable to load doctors.')
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    const timer = setTimeout(() => {
      loadDoctors(true)
    }, 0)

    return () => clearTimeout(timer)
  }, [loadDoctors])

  function handleInputChange(event) {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  async function handleAddDoctor(event) {
    event.preventDefault()

    try {
      setSaving(true)
      setError('')
      setSuccess('')

      await adminService.createUser(token, {
        ...formData,
        role: 'doctor',
      })

      setSuccess('Doctor account created successfully!')
      setFormData({
        full_name: '',
        email: '',
        password: '',
      })
      setShowForm(false)

      await loadDoctors()
    } catch (err) {
      setError(err.message || 'Unable to create doctor.')
    } finally {
      setSaving(false)
    }
  }

  async function handleDeleteDoctor(doctor) {
    const confirmed = window.confirm(
      `Are you sure you want to permanently delete ${doctor.full_name}? All doctor-patient and clinic-doctor assignments will be removed.`
    )

    if (!confirmed) return

    try {
      setError('')
      setSuccess('')

      await adminService.deleteUser(token, doctor.id)

      setSuccess('Doctor account deleted successfully!')
      await loadDoctors()
    } catch (err) {
      setError(err.message || 'Unable to delete doctor.')
    }
  }

  const filteredDoctors = doctors.filter((doctor) => {
    const query = search.toLowerCase()

    return (
      doctor.full_name?.toLowerCase().includes(query) ||
      doctor.email?.toLowerCase().includes(query) ||
      String(doctor.id).includes(query)
    )
  })

  return (
    <section className="card">
      <h1 className="page-title">Manage Doctors</h1>
      <p className="page-subtitle">
        View, add and manage registered doctors.
      </p>

      <button
        className="btn btn-primary"
        onClick={() => {
          setShowForm(!showForm)
          setError('')
          setSuccess('')
        }}
      >
        {showForm ? 'Cancel' : '+ Add Doctor'}
      </button>

      {showForm && (
        <form onSubmit={handleAddDoctor} className="admin-form">
          <h3>Add New Doctor</h3>

          <input
            type="text"
            name="full_name"
            placeholder="Doctor full name"
            value={formData.full_name}
            onChange={handleInputChange}
            minLength={2}
            maxLength={100}
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Doctor email address"
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
            {saving ? 'Creating...' : 'Create Doctor'}
          </button>
        </form>
      )}

      {success && <p className="alert alert-success">{success}</p>}
      {error && <p className="alert alert-error">{error}</p>}

      <input
        type="text"
        placeholder="Search by name, email or ID..."
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        className="admin-search"
      />

      <button
        className="btn btn-secondary"
        onClick={() => loadDoctors(true)}
        disabled={loading}
      >
        Refresh Doctors
      </button>

      {loading ? (
        <p>Loading doctors...</p>
      ) : (
        <>
          <p>Total doctors: {filteredDoctors.length}</p>

          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Specialization</th>
                  <th>Experience</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredDoctors.map((doctor) => (
                  <tr key={doctor.id}>
                    <td>{doctor.id}</td>
                    <td>{doctor.full_name}</td>
                    <td>{doctor.email}</td>
                    <td>
                      {doctor.profile?.specialization || 'Not recorded'}
                    </td>
                    <td>
                      {doctor.profile?.years_of_experience ?? 0} years
                    </td>
                    <td>
                      {doctor.is_active ? 'Active' : 'Inactive'}
                    </td>
                    <td>
                      <button
                        className="btn btn-danger"
                        onClick={() => handleDeleteDoctor(doctor)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}

                {filteredDoctors.length === 0 && (
                  <tr>
                    <td colSpan="7">No doctors found.</td>
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
