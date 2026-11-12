import { useState } from 'react'
import { predictPatient, getPatients, savePatient, logoutUser } from './services/api'
import './App.css'
import Auth from './components/Auth'

function App() {
const [user, setUser] = useState(null)
const [token, setToken] = useState(null)

const handleLogout = async () => {
  try {
    if (token) {
      await logoutUser(token)
    }
  } catch (error) {
    console.error('Logout API Error:', error)
  } finally {
    setUser(null)
    setToken(null)
    setPatients([])
    setPrediction(null)
    setError('')
  }
}

  const [form, setForm] = useState({
    age: '',
    gender: '',
    symptoms: [],
    duration_days: '1',
    blood_pressure: 'Normal',
    cholesterol_level: 'Normal',
    additional_notes: ''
  })
const [prediction, setPrediction] = useState(null)
const [loading, setLoading] = useState(false)
const [error, setError] = useState('')
const [patients, setPatients] = useState([])



  const symptomOptions = [
    'fever',
    'cough',
    'fatigue',
    'difficulty breathing'
  ]

  const handleChange = (e) => {
    const { name, value } = e.target

    setForm({
      ...form,
      [name]: value
    })
  }

  const handleSymptomChange = (symptom) => {
    setForm((previous) => ({
      ...previous,
      symptoms: previous.symptoms.includes(symptom)
        ? previous.symptoms.filter((item) => item !== symptom)
        : [...previous.symptoms, symptom]
    }))
  }

 const handleSubmit = async (e) => {
  e.preventDefault()

  setPrediction(null)
  setError('')

  if (form.symptoms.length === 0) {
    setError('Please select at least one symptom.')
    return
  }

  const patientData = {
    age: Number(form.age),
    gender: form.gender,
    symptoms: form.symptoms,
    duration_days: Number(form.duration_days),
    blood_pressure: form.blood_pressure,
    cholesterol_level: form.cholesterol_level,
    additional_notes: form.additional_notes
  }
try {
  setLoading(true)

  // Save patient details
  await savePatient(patientData, token)

  // Get disease prediction
  const result = await predictPatient(patientData)
  setPrediction(result)

  // Refresh patient records
const data = await getPatients(token)
setPatients(data.patients || [])

} catch (err) {
  console.error('Error loading patients:', err.message)
} finally {
  setLoading(false)
}
 }
if (!user) {
    return (
      <Auth
        
  onLogin={async (result) => {
  setUser(result.user)
  setToken(result.access_token)

  try {
    const data = await getPatients(result.access_token)
setPatients(data.patients || [])
  } catch (err) {
    console.error('Error loading patients:', err.message)
  }
}}
      />
    )
  }
  return (
    <div className="app-container">

      <header className="navbar">
        <div className="brand">
          <span className="brand-icon">✚</span>
          <div>
            <h2>MedAssist AI</h2>
            <p>Intelligent Healthcare Assistant</p>
          </div>
        </div>

        <div className="nav-status">
          <span className="status-dot"></span>
          System Online
           <button onClick={handleLogout} className="logout-button">
    Logout
  </button>
        </div>
      </header>

      <main className="main-content">

        <section className="welcome-section">
          <div>
            <p className="eyebrow">AI POWERED HEALTHCARE</p>
            <h1>Your Health, <span>Our Priority.</span></h1>
            <p className="welcome-description">
              Enter patient information and symptoms to receive
              an AI-generated prediction from our demonstration model.
            </p>
          </div>

          <div className="welcome-icon">🩺</div>
        </section>

        <section className="dashboard-grid">

          <div className="form-card">
            <div className="card-heading">
              <div>
                <h2>Patient Information</h2>
                <p>Enter the details below</p>
              </div>
              <span className="card-icon">👤</span>
            </div>

            <form onSubmit={handleSubmit}>

              <div className="form-row">
                <div className="form-group">
                  <label>Patient Age</label>
                  <input
                    type="number"
                    name="age"
                    placeholder="Enter age"
                    min="0"
                    max="120"
                    value={form.age}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Gender</label>
                  <select
                    name="gender"
                    value={form.gender}
                    onChange={handleChange}
                    required
                  >
                    <option value="">Select gender</option>
                    <option value="Female">Female</option>
                    <option value="Male">Male</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Symptoms</label>
                <p className="field-hint">Select all applicable symptoms</p>

                <div className="symptom-grid">
                  {symptomOptions.map((symptom) => (
                    <label className="symptom-option" key={symptom}>
                      <input
                        type="checkbox"
                        checked={form.symptoms.includes(symptom)}
                        onChange={() => handleSymptomChange(symptom)}
                      />
                      <span>
                        {symptom.charAt(0).toUpperCase() + symptom.slice(1)}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="form-group">
                <label>Symptom Duration (Days)</label>
                <input
                  type="number"
                  name="duration_days"
                  min="1"
                  max="365"
                  value={form.duration_days}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Blood Pressure</label>
                  <select
                    name="blood_pressure"
                    value={form.blood_pressure}
                    onChange={handleChange}
                  >
                    <option>Normal</option>
                    <option>Low</option>
                    <option>High</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Cholesterol</label>
                  <select
                    name="cholesterol_level"
                    value={form.cholesterol_level}
                    onChange={handleChange}
                  >
                    <option>Normal</option>
                    <option>Low</option>
                    <option>High</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Additional Notes</label>
                <textarea
                  name="additional_notes"
                  placeholder="Enter any additional information..."
                  value={form.additional_notes}
                  onChange={handleChange}
                  maxLength="500"
                  rows="3"
                />
              </div>

              <button type="submit" className="submit-button">
                Generate Prediction →
              </button>

            </form>
          </div>

          <aside className="info-column">

            <div className="info-card">
              <span className="info-icon">🤖</span>
              <h3>AI-Powered Analysis</h3>
              <p>
                The machine learning model processes the submitted
                patient features to generate a prediction.
              </p>
            </div>

            <div className="info-card">
              <span className="info-icon">🔒</span>
              <h3>Patient Information</h3>
              <p>
                Enter accurate information. Avoid including
                unnecessary personal identifiers.
              </p>
            </div>

            <div className="notice-card">
              <h3>⚠️ Medical Disclaimer</h3>
              <p>
                MedAssist AI is an educational demonstration.
                Predictions are not medical diagnoses or treatment
                recommendations. Always consult a qualified healthcare
                professional.
              </p>
            </div>

          </aside>

        </section>
        {loading && (
          <div className="result-card">
            <h2>Processing your information...</h2>
            <p>Please wait while the model generates a prediction.</p>
          </div>
        )}

        {error && (
          <div className="result-card">
            <h2>Something went wrong</h2>
            <p>{error}</p>
          </div>
        )}
<section className="result-card">
  <h2>My Patient Records</h2>

  {patients.length === 0 ? (
    <p>No patient records available yet.</p>
  ) : (
    patients.map((patient) => (
      <div key={patient.id} className="patient-record">

        <h3>Patient Record #{patient.id}</h3>

        <p>
          <strong>Age:</strong> {patient.age}
        </p>

        <p>
          <strong>Gender:</strong> {patient.gender}
        </p>

        <p>
          <strong>Symptoms:</strong>{' '}
          {Array.isArray(patient.symptoms)
            ? patient.symptoms.join(', ')
            : patient.symptoms}
        </p>

       <p>
  <strong>Duration:</strong> {patient.duration_days} days
</p>

<p>
  <strong>Blood Pressure:</strong> {patient.blood_pressure || 'Not available'}
</p>

<p>
  <strong>Cholesterol:</strong> {patient.cholesterol_level || 'Not available'}
</p>

<p>
  <strong>Additional Notes:</strong>{' '}
  {patient.additional_notes || 'No additional notes'}
</p>

        <hr />

      </div>
    ))
  )}
</section>




        {prediction && (
          <div className="result-card">
            <h2>Prediction Results</h2>

            <p>
              <strong>Prediction:</strong>{' '}
              {prediction.prediction_result?.prediction}
            </p>

            <p>
              <strong>Patient Age:</strong> {prediction.patient_age}
            </p>

            <p>
              <strong>Symptoms:</strong>{' '}
              {prediction.symptoms?.join(', ')}
            </p>

            <p className="medical-notice">
              {prediction.notice}
            </p>
          </div>
        )}

        <footer>
          © 2026 MedAssist AI | Educational Healthcare Project
        </footer>

      </main>
    </div>
  )
}

export default App