
import { useCallback, useEffect, useState } from 'react'
import { adminService } from '../services/adminService'

function AdminAssignments({ token }) {
  const [doctors, setDoctors] = useState([])
  const [patients, setPatients] = useState([])
  const [clinics, setClinics] = useState([])
  const [patientAssignments, setPatientAssignments] = useState([])
  const [clinicAssignments, setClinicAssignments] = useState([])

  const [doctorId, setDoctorId] = useState('')
  const [patientId, setPatientId] = useState('')
  const [clinicId, setClinicId] = useState('')
  const [clinicDoctorId, setClinicDoctorId] = useState('')

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const loadData = useCallback(async () => {
    try {
      const [
        doctorData,
        patientData,
        clinicData,
        assignmentData,
        clinicAssignmentData,
      ] = await Promise.all([
        adminService.getDoctors(token),
        adminService.getPatients(token),
        adminService.getClinics(token),
        adminService.getAssignments(token),
        adminService.getClinicAssignments(token),
      ])

      setDoctors(doctorData.items || [])
      setPatients(patientData.items || [])
      setClinics(clinicData.items || [])
      setPatientAssignments(assignmentData.items || [])
      setClinicAssignments(clinicAssignmentData.items || [])
      setError('')
    } catch (err) {
      setError(err.message || 'Unable to load assignments.')
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    const timer = setTimeout(() => {
      loadData()
    }, 0)

    return () => clearTimeout(timer)
  }, [loadData])

  const handlePatientAssignment = async (event) => {
    event.preventDefault()
    setError('')
    setMessage('')

    if (!doctorId || !patientId) {
      setError('Please select both a doctor and a patient.')
      return
    }

    setSaving(true)

    try {
      await adminService.createAssignment(
        token,
        Number(doctorId),
        Number(patientId),
      )
      setMessage('Doctor assigned to patient successfully.')
      setDoctorId('')
      setPatientId('')
      await loadData()
    } catch (err) {
      setError(err.message || 'Unable to create assignment.')
    } finally {
      setSaving(false)
    }
  }

  const handleClinicAssignment = async (event) => {
    event.preventDefault()
    setError('')
    setMessage('')

    if (!clinicId || !clinicDoctorId) {
      setError('Please select both a clinic and a doctor.')
      return
    }

    setSaving(true)

    try {
      await adminService.createClinicAssignment(
        token,
        Number(clinicId),
        Number(clinicDoctorId),
      )
      setMessage('Doctor assigned to clinic successfully.')
      setClinicId('')
      setClinicDoctorId('')
      await loadData()
    } catch (err) {
      setError(err.message || 'Unable to create clinic assignment.')
    } finally {
      setSaving(false)
    }
  }

  const handleDeletePatientAssignment = async (assignmentId) => {
    if (!window.confirm('Remove this doctor-patient assignment?')) return

    setError('')
    setMessage('')

    try {
      await adminService.deleteAssignment(token, assignmentId)
      setMessage('Doctor-patient assignment removed.')
      await loadData()
    } catch (err) {
      setError(err.message || 'Unable to remove assignment.')
    }
  }

  const handleDeleteClinicAssignment = async (assignmentId) => {
    if (!window.confirm('Remove this doctor from the clinic?')) return

    setError('')
    setMessage('')

    try {
      await adminService.deleteClinicAssignment(token, assignmentId)
      setMessage('Clinic-doctor assignment removed.')
      await loadData()
    } catch (err) {
      setError(err.message || 'Unable to remove clinic assignment.')
    }
  }

  if (loading) {
    return (
      <section className="card">
        <h1 className="page-title">Assignments</h1>
        <p>Loading assignment information...</p>
      </section>
    )
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Assignments</h1>
          <p className="page-subtitle">
            Manage doctor-patient and clinic-doctor associations.
          </p>
        </div>

        <button
          type="button"
          className="btn btn-secondary"
          onClick={loadData}
        >
          Refresh
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {message && <div className="alert alert-success">{message}</div>}

      <section className="card">
        <h2>Doctor–Patient Assignment</h2>
        <p>Assign a doctor to a patient.</p>

        <form onSubmit={handlePatientAssignment}>
          <div className="form-group">
            <label htmlFor="assignment-doctor">Select Doctor</label>
            <select
              id="assignment-doctor"
              value={doctorId}
              onChange={(event) => setDoctorId(event.target.value)}
              required
            >
              <option value="">Choose a doctor</option>
              {doctors.filter((doctor) => doctor.is_active).map((doctor) => (
                <option key={doctor.id} value={doctor.id}>
                  {doctor.full_name} (ID: {doctor.id})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="assignment-patient">Select Patient</label>
            <select
              id="assignment-patient"
              value={patientId}
              onChange={(event) => setPatientId(event.target.value)}
              required
            >
              <option value="">Choose a patient</option>
              {patients.filter((patient) => patient.is_active).map((patient) => (
                <option key={patient.id} value={patient.id}>
                  {patient.full_name} (ID: {patient.id})
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="btn" disabled={saving}>
            {saving ? 'Assigning...' : 'Assign Doctor to Patient'}
          </button>
        </form>

        <h3>Existing Doctor–Patient Assignments</h3>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Doctor</th>
                <th>Patient</th>
                <th>Assigned At</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {patientAssignments.length === 0 ? (
                <tr>
                  <td colSpan="5">No doctor-patient assignments found.</td>
                </tr>
              ) : (
                patientAssignments.map((assignment) => (
                  <tr key={assignment.id}>
                    <td>{assignment.id}</td>
                    <td>
                      {assignment.doctor_name}
                      <br />
                      <small>ID: {assignment.doctor_id}</small>
                    </td>
                    <td>
                      {assignment.patient_name}
                      <br />
                      <small>ID: {assignment.patient_id}</small>
                    </td>
                    <td>
                      {assignment.assigned_at
                        ? new Date(assignment.assigned_at).toLocaleString()
                        : '-'}
                    </td>
                    <td>
                      <button
                        type="button"
                        className="btn btn-outline-danger"
                        onClick={() =>
                          handleDeletePatientAssignment(assignment.id)
                        }
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h2>Clinic–Doctor Assignment</h2>
        <p>Associate a doctor with a clinic.</p>

        <form onSubmit={handleClinicAssignment}>
          <div className="form-group">
            <label htmlFor="assignment-clinic">Select Clinic</label>
            <select
              id="assignment-clinic"
              value={clinicId}
              onChange={(event) => setClinicId(event.target.value)}
              required
            >
              <option value="">Choose a clinic</option>
              {clinics.filter((clinic) => clinic.is_active).map((clinic) => (
                <option key={clinic.id} value={clinic.id}>
                  {clinic.full_name} (ID: {clinic.id})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="assignment-clinic-doctor">Select Doctor</label>
            <select
              id="assignment-clinic-doctor"
              value={clinicDoctorId}
              onChange={(event) => setClinicDoctorId(event.target.value)}
              required
            >
              <option value="">Choose a doctor</option>
              {doctors.filter((doctor) => doctor.is_active).map((doctor) => (
                <option key={doctor.id} value={doctor.id}>
                  {doctor.full_name} (ID: {doctor.id})
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="btn" disabled={saving}>
            {saving ? 'Assigning...' : 'Assign Doctor to Clinic'}
          </button>
        </form>

        <h3>Existing Clinic–Doctor Assignments</h3>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Clinic</th>
                <th>Doctor</th>
                <th>Assigned At</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {clinicAssignments.length === 0 ? (
                <tr>
                  <td colSpan="5">No clinic-doctor assignments found.</td>
                </tr>
              ) : (
                clinicAssignments.map((assignment) => (
                  <tr key={assignment.id}>
                    <td>{assignment.id}</td>
                    <td>
                      {assignment.clinic_name}
                      <br />
                      <small>ID: {assignment.clinic_id}</small>
                    </td>
                    <td>
                      {assignment.doctor_name}
                      <br />
                      <small>ID: {assignment.doctor_id}</small>
                    </td>
                    <td>
                      {assignment.assigned_at
                        ? new Date(assignment.assigned_at).toLocaleString()
                        : '-'}
                    </td>
                    <td>
                      <button
                        type="button"
                        className="btn btn-outline-danger"
                        onClick={() =>
                          handleDeleteClinicAssignment(assignment.id)
                        }
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

export default AdminAssignments
