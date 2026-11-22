
import { useEffect, useState } from 'react'
import {
  getAssignedDoctorPatients,
  getAssignedPatientDetails,
} from '../services/api'
import './DoctorDashboard.css'

function DoctorDashboard({ user, token, onLogout }) {
  const [patients, setPatients] = useState([])
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [loading, setLoading] = useState(true)
  const [detailsLoading, setDetailsLoading] = useState(false)
  const [error, setError] = useState('')

  const loadPatients = async () => {
    try {
      setLoading(true)
      setError('')

      const data = await getAssignedDoctorPatients(token)
      setPatients(data.patients || [])
    } catch (err) {
      setError(err.message || 'Unable to load assigned patients.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let cancelled = false

    async function fetchPatients() {
      try {
        const data = await getAssignedDoctorPatients(token)

        if (!cancelled) {
          setPatients(data.patients || [])
          setError('')
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || 'Unable to load assigned patients.')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    fetchPatients()

    return () => {
      cancelled = true
    }
  }, [token])

  const viewPatient = async (patientId) => {
    try {
      setDetailsLoading(true)
      setError('')
      setSelectedPatient(null)

      const data = await getAssignedPatientDetails(token, patientId)
      setSelectedPatient(data)
    } catch (err) {
      setError(err.message || 'Unable to load patient details.')
    } finally {
      setDetailsLoading(false)
    }
  }

  return (
    <div className="doctor-dashboard">
      <header className="doctor-header">
        <div>
          <h1>MedAssist AI</h1>
          <p>Doctor Clinical Workspace</p>
        </div>

        <button className="doctor-logout" onClick={onLogout}>
          Logout
        </button>
      </header>

      <main className="doctor-main">
        <section className="doctor-welcome">
          <div>
            <h2>Welcome, Dr. {user?.full_name}</h2>
            <p>
              Manage your assigned patients and review their clinical records.
            </p>
          </div>

          <div className="patient-count">
            <strong>{patients.length}</strong>
            <span>Assigned Patients</span>
          </div>
        </section>

        {error && (
          <div className="doctor-error" role="alert">
            {error}
          </div>
        )}

        <div className="doctor-content">
          <section className="assigned-patients">
            <div className="section-heading">
              <h2>My Assigned Patients</h2>
              <button onClick={loadPatients} disabled={loading}>
                {loading ? 'Loading...' : 'Refresh'}
              </button>
            </div>

            {loading ? (
              <p>Loading assigned patients...</p>
            ) : patients.length === 0 ? (
              <p>No patients have been assigned to you yet.</p>
            ) : (
              patients.map((patient) => (
                <button
                  className="patient-item"
                  key={patient.patient_id}
                  onClick={() => viewPatient(patient.patient_id)}
                >
                  <span>
                    <strong>{patient.full_name}</strong>
                    <small>{patient.email}</small>
                  </span>

                  <span className="record-count">
                    {patient.records_count} records
                  </span>
                </button>
              ))
            )}
          </section>

          <section className="patient-details">
            <h2>Patient Details</h2>

            {detailsLoading ? (
              <p>Loading patient details...</p>
            ) : !selectedPatient ? (
              <p>Select an assigned patient to view their details.</p>
            ) : (
              <>
                <div className="detail-card">
                  <h3>{selectedPatient.patient.full_name}</h3>
                  <p>{selectedPatient.patient.email}</p>
                </div>

                <h3>Patient Profile</h3>

                {selectedPatient.profile ? (
                  <div className="detail-card">
                    <p><strong>Age:</strong> {selectedPatient.profile.age ?? 'Not provided'}</p>
                    <p><strong>Gender:</strong> {selectedPatient.profile.gender || 'Not provided'}</p>
                    <p><strong>Contact:</strong> {selectedPatient.profile.contact_number || 'Not provided'}</p>
                    <p><strong>Address:</strong> {selectedPatient.profile.address || 'Not provided'}</p>
                    <p><strong>Blood Group:</strong> {selectedPatient.profile.blood_group || 'Not provided'}</p>
                    <p><strong>Emergency Contact:</strong> {selectedPatient.profile.emergency_contact || 'Not provided'}</p>
                  </div>
                ) : (
                  <p>Patient profile has not been completed.</p>
                )}

                <h3>Clinical Records ({selectedPatient.records_count})</h3>

                {(selectedPatient.clinical_records || []).length === 0 ? (
                  <p>No clinical records available.</p>
                ) : (
                  selectedPatient.clinical_records.map((record) => (
                    <div className="clinical-record" key={record.id}>
                      <p><strong>Date:</strong> {new Date(record.created_at).toLocaleString()}</p>
                      <p><strong>Age:</strong> {record.age}</p>
                      <p><strong>Gender:</strong> {record.gender}</p>
                      <p><strong>Symptoms:</strong> {record.symptoms}</p>
                      <p><strong>Duration:</strong> {record.duration_days} days</p>
                      <p><strong>Blood Pressure:</strong> {record.blood_pressure || 'Not provided'}</p>
                      <p><strong>Cholesterol:</strong> {record.cholesterol_level || 'Not provided'}</p>
                      <p><strong>Notes:</strong> {record.additional_notes || 'None'}</p>
                    </div>
                  ))
                )}
              </>
            )}
          </section>
        </div>
      </main>
    </div>
  )
}

export default DoctorDashboard
