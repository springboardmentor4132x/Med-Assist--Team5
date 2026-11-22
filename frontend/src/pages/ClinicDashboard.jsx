import { useCallback, useEffect, useState } from 'react'
import { clinicService } from '../services/clinicService'
import './ClinicDashboard.css'

function ClinicDashboard({ user, token, onLogout }) {
  const [activePage, setActivePage] = useState('Dashboard')
  const [dashboard, setDashboard] = useState(null)
  const [doctors, setDoctors] = useState([])
  const [patients, setPatients] = useState([])
  const [profile, setProfile] = useState(null)
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

    const loadDashboard = useCallback(async (showLoading = false) => {
    try {
      if (showLoading) setLoading(true)
      setError('')

      const data = await clinicService.getDashboard(token)
      setDashboard(data)
    } catch (err) {
      setError(err.message || 'Unable to load clinic dashboard.')
    } finally {
      setLoading(false)
    }
  }, [token])

  const loadDoctors = async () => {
    try {
      setLoading(true)
      setError('')
      const data = await clinicService.getDoctors(token)
      setDoctors(data.items || [])
    } catch (err) {
      setError(err.message || 'Unable to load doctors.')
    } finally {
      setLoading(false)
    }
  }

  const loadPatients = async () => {
    try {
      setLoading(true)
      setError('')
      const data = await clinicService.getPatients(token)
      setPatients(data.items || [])
    } catch (err) {
      setError(err.message || 'Unable to load patients.')
    } finally {
      setLoading(false)
    }
  }

  const loadProfile = async () => {
    try {
      setLoading(true)
      setError('')
      const data = await clinicService.getProfile(token)
      setProfile(data)
    } catch (err) {
      setError(err.message || 'Unable to load clinic profile.')
    } finally {
      setLoading(false)
    }
  }

  const viewPatient = async (patientId) => {
    try {
      setLoading(true)
      setError('')
      const data = await clinicService.getPatientDetails(token, patientId)
      setSelectedPatient(data)
      setActivePage('Patient Details')
    } catch (err) {
      setError(err.message || 'Unable to load patient details.')
    } finally {
      setLoading(false)
    }
  }
  useEffect(() => {
    const timer = setTimeout(() => {
      loadDashboard(true)
    }, 0)

    return () => clearTimeout(timer)
  }, [loadDashboard])
  const navigate = (page) => {
    setActivePage(page)
    setError('')

    if (page === 'Dashboard') loadDashboard()
    if (page === 'Doctors') loadDoctors()
    if (page === 'Patients') loadPatients()
    if (page === 'Profile') loadProfile()
  }

  const renderContent = () => {
    if (loading) {
      return <div className="clinic-card">Loading information...</div>
    }

    if (error) {
      return (
        <div className="clinic-card clinic-error">
          <p>{error}</p>
          <button onClick={() => navigate(activePage)}>
            Try Again
          </button>
        </div>
      )
    }

    if (activePage === 'Dashboard') {
      return (
        <>
          <div className="clinic-welcome">
            <h1>Welcome, {dashboard?.clinic?.name || user.full_name}</h1>
            <p>Here's your clinic overview.</p>
          </div>

          <div className="clinic-stats">
            <div className="clinic-card">
              <h3>Total Doctors</h3>
              <p>{dashboard?.total_doctors ?? 0}</p>
            </div>

            <div className="clinic-card">
              <h3>Total Patients</h3>
              <p>{dashboard?.total_patients ?? 0}</p>
            </div>
          </div>

          <div className="clinic-card">
            <h2>Clinic Information</h2>
            <p><strong>Name:</strong> {dashboard?.clinic?.name}</p>
            <p><strong>Email:</strong> {dashboard?.clinic?.email}</p>
          </div>
        </>
      )
    }

    if (activePage === 'Doctors') {
      return (
        <div className="clinic-card">
          <h2>Assigned Doctors</h2>

          {doctors.length === 0 ? (
            <p>No doctors assigned to this clinic yet.</p>
          ) : (
            <div className="clinic-table-wrapper">
              <table className="clinic-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {doctors.map((doctor) => (
                    <tr key={doctor.id}>
                      <td>{doctor.id}</td>
                      <td>{doctor.full_name}</td>
                      <td>{doctor.email}</td>
                      <td>{doctor.is_active ? 'Active' : 'Inactive'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )
    }

    if (activePage === 'Patients') {
      return (
        <div className="clinic-card">
          <h2>Clinic Patients</h2>

          {patients.length === 0 ? (
            <p>No patients are currently assigned to this clinic.</p>
          ) : (
            <div className="clinic-table-wrapper">
              <table className="clinic-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Assigned Doctor</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {patients.map((patient) => (
                    <tr key={patient.id}>
                      <td>{patient.id}</td>
                      <td>{patient.full_name}</td>
                      <td>{patient.email}</td>
                      <td>{patient.assigned_doctor_name || '-'}</td>
                      <td>
                        <button
                          className="clinic-button"
                          onClick={() => viewPatient(patient.id)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )
    }

    if (activePage === 'Patient Details') {
      const patient = selectedPatient?.patient
      const records = selectedPatient?.symptom_records || []

      return (
        <div className="clinic-card">
          <button
            className="clinic-button"
            onClick={() => navigate('Patients')}
          >
            Back to Patients
          </button>

          <h2>Patient Details</h2>

          {patient && (
            <>
              <p><strong>Patient ID:</strong> {patient.id}</p>
              <p><strong>Name:</strong> {patient.full_name}</p>
              <p><strong>Email:</strong> {patient.email}</p>
              <p>
                <strong>Status:</strong>
                {' '}{patient.is_active ? 'Active' : 'Inactive'}
              </p>
            </>
          )}

          <h3>Assigned Doctor</h3>
          <p>
            {selectedPatient?.assigned_doctor?.full_name || 'Not available'}
          </p>

          <h3>Symptom History</h3>

          {records.length === 0 ? (
            <p>No symptom records found for this patient.</p>
          ) : (
            records.map((record) => (
              <div className="clinic-record" key={record.id}>
                <h4>Record #{record.id}</h4>
                <p><strong>Age:</strong> {record.age}</p>
                <p><strong>Gender:</strong> {record.gender || '-'}</p>
                <p><strong>Symptoms:</strong> {record.symptoms}</p>
                <p><strong>Duration:</strong> {record.duration_days} days</p>
                <p><strong>Blood Pressure:</strong> {record.blood_pressure || '-'}</p>
                <p><strong>Cholesterol:</strong> {record.cholesterol_level || '-'}</p>
                <p><strong>Notes:</strong> {record.additional_notes || '-'}</p>
                <p>
                  <strong>Created:</strong>
                  {' '}
                  {record.created_at
                    ? new Date(record.created_at).toLocaleString()
                    : '-'}
                </p>
              </div>
            ))
          )}
        </div>
      )
    }

    if (activePage === 'Profile') {
      return (
        <div className="clinic-card">
          <h2>Clinic Profile</h2>
          {profile && (
            <>
              <p><strong>Clinic ID:</strong> {profile.id}</p>
              <p><strong>Name:</strong> {profile.full_name}</p>
              <p><strong>Email:</strong> {profile.email}</p>
              <p><strong>Role:</strong> {profile.role}</p>
              <p>
                <strong>Status:</strong>
                {' '}{profile.is_active ? 'Active' : 'Inactive'}
              </p>
              <p>
                <strong>Registered:</strong>
                {' '}
                {profile.created_at
                  ? new Date(profile.created_at).toLocaleString()
                  : '-'}
              </p>
            </>
          )}
          <p className="clinic-hint">
            Profile editing is not available yet.
          </p>
        </div>
      )
    }

    return null
  }

  return (
    <div className="clinic-layout">
      <aside className="clinic-sidebar">
        <div className="clinic-brand">
          <h2>MedAssist AI</h2>
          <p>Clinic Portal</p>
        </div>

        <nav>
          {['Dashboard', 'Doctors', 'Patients', 'Profile'].map((page) => (
            <button
              key={page}
              className={activePage === page ? 'active' : ''}
              onClick={() => navigate(page)}
            >
              {page}
            </button>
          ))}
        </nav>

        <button className="clinic-logout" onClick={onLogout}>
          Sign Out
        </button>
      </aside>

      <main className="clinic-main">
        <header className="clinic-header">
          <div>
            <h2>{activePage}</h2>
            <p>{user.full_name}</p>
          </div>
          <span className="clinic-status">Clinic Account</span>
        </header>

        {renderContent()}
      </main>
    </div>
  )
}

export default ClinicDashboard
