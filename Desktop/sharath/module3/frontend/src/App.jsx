import { useState } from 'react'
import { predictPatient, getPatients, savePatient, logoutUser } from './services/api'
import './App.css'
import Auth from './components/Auth'
import PredictionResults from './components/PredictionResults'

function App() {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)

  // 3 Distinct Pages: 'assessment' (default) | 'prediction' | 'records'
  const [activePage, setActivePage] = useState('assessment')

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
      setActivePage('assessment')
    }
  }

  const [form, setForm] = useState({
    patient_name: '',
    age: '',
    gender: '',
    symptoms: [],
    duration_days: '1',
    blood_pressure: 'Normal',
    cholesterol_level: 'Normal',
    severity: 'Moderate',
    onset: 'Gradual',
    additional_notes: ''
  })

  const [customSymptom, setCustomSymptom] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [patients, setPatients] = useState([])

  // Organized Clinical Symptom Blocks
  const symptomCategories = [
    {
      id: 'general',
      name: 'General & Constitutional',
      icon: '🌡️',
      description: 'Systemic signs of infection or generalized illness',
      symptoms: [
        'Fever and chills',
        'Fatigue and weakness',
        'Night sweats',
        'Unexplained weight loss',
        'Loss of appetite'
      ]
    },
    {
      id: 'head_throat',
      name: 'Head, Throat & Sensory',
      icon: '🧠',
      description: 'Cranial, pharyngeal, and neurological sensations',
      symptoms: [
        'Sore throat, headache, or muscle and joint aches',
        'Sore throat',
        'Headache',
        'Dizziness',
        'Vision changes',
        'Stiff neck'
      ]
    },
    {
      id: 'respiratory',
      name: 'Respiratory & Chest',
      icon: '🫁',
      description: 'Airway, pulmonary, and thoracic manifestations',
      symptoms: [
        'Cough',
        'Difficulty breathing',
        'Chest pain or tightness',
        'Wheezing'
      ]
    },
    {
      id: 'musculoskeletal',
      name: 'Musculoskeletal & Body Aches',
      icon: '🦴',
      description: 'Joint, muscle, and body-wide discomfort',
      symptoms: [
        'Muscle and joint aches',
        'Joint swelling and stiffness',
        'Back pain'
      ]
    },
    {
      id: 'skin_mucosal',
      name: 'Skin & Mucosal Manifestations',
      icon: '🔴',
      description: 'Dermatological and oral mucosal lesions',
      symptoms: [
        'Skin rash or mouth ulcers',
        'Skin rash',
        'Mouth ulcers',
        'Itching or pruritus'
      ]
    },
    {
      id: 'lymphatic',
      name: 'Lymphatic & Glandular',
      icon: '🛡️',
      description: 'Lymph node swelling and glandular inflammation',
      symptoms: [
        'Swollen lymph nodes (glands) and night sweats',
        'Swollen lymph nodes (glands)',
        'Swollen neck glands'
      ]
    },
    {
      id: 'gastrointestinal',
      name: 'Gastrointestinal & Digestive',
      icon: '🤢',
      description: 'Stomach, bowel, and digestive symptoms',
      symptoms: [
        'Nausea and vomiting',
        'Diarrhea',
        'Abdominal pain or cramps'
      ]
    },
    {
      id: 'urinary',
      name: 'Urinary & Renal',
      icon: '💧',
      description: 'Urological and excretory tract symptoms',
      symptoms: [
        'Painful urination',
        'Urinary frequency or urgency'
      ]
    }
  ]

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm({
      ...form,
      [name]: value
    })
  }

  const handleSymptomToggle = (symptom) => {
    setForm((previous) => ({
      ...previous,
      symptoms: previous.symptoms.includes(symptom)
        ? previous.symptoms.filter((item) => item !== symptom)
        : [...previous.symptoms, symptom]
    }))
  }

  const handleAddCustomSymptom = (e) => {
    e.preventDefault()
    const trimmed = customSymptom.trim()
    if (!trimmed) return

    if (!form.symptoms.includes(trimmed)) {
      setForm((prev) => ({
        ...prev,
        symptoms: [...prev.symptoms, trimmed]
      }))
    }
    setCustomSymptom('')
  }

  const handleRemoveSymptom = (symptomToRemove) => {
    setForm((prev) => ({
      ...prev,
      symptoms: prev.symptoms.filter((s) => s !== symptomToRemove)
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setPrediction(null)
    setError('')

    if (form.symptoms.length === 0) {
      setError('Please select or enter at least one symptom for analysis.')
      return
    }

    const patientData = {
      patient_name: form.patient_name.trim() || user?.full_name || 'Anonymous Patient',
      age: Number(form.age),
      gender: form.gender,
      symptoms: form.symptoms,
      duration_days: Number(form.duration_days),
      blood_pressure: form.blood_pressure,
      cholesterol_level: form.cholesterol_level,
      severity: form.severity,
      onset: form.onset,
      additional_notes: form.additional_notes
    }

    try {
      setLoading(true)
      setActivePage('prediction') // Immediately switch to Prediction page to show loading & results

      // 1. Save patient details in DB
      await savePatient(patientData, token)

      // 2. Obtain ML disease prediction
      const result = await predictPatient(patientData)
      setPrediction(result)

      // 3. Refresh patient records
      const data = await getPatients(token)
      setPatients(data.patients || [])
    } catch (err) {
      console.error('Error in prediction/saving:', err.message)
      setError(err.message || 'Failed to generate disease prediction.')
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
          setForm((prev) => ({
            ...prev,
            patient_name: result.user?.full_name || ''
          }))
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
      {/* Top Navbar with Page Tabs */}
      <header className="navbar">
        <div className="brand">
          <span className="brand-icon">✚</span>
          <div>
            <h2>MedAssist AI</h2>
            <p>Clinical Decision-Support & Diagnostic System</p>
          </div>
        </div>

        {/* Page Navigation Tabs */}
        <nav className="nav-pages-bar">
          <button
            type="button"
            className={`nav-tab-btn ${activePage === 'assessment' ? 'active' : ''}`}
            onClick={() => setActivePage('assessment')}
          >
            <span className="nav-tab-icon">📝</span>
            <span className="nav-tab-text">Patient Assessment Form</span>
          </button>

          <button
            type="button"
            className={`nav-tab-btn ${activePage === 'prediction' ? 'active' : ''}`}
            onClick={() => setActivePage('prediction')}
          >
            <span className="nav-tab-icon">🩺</span>
            <span className="nav-tab-text">AI Disease Prediction</span>
            {prediction && <span className="nav-ready-dot" title="Prediction Ready"></span>}
          </button>

          <button
            type="button"
            className={`nav-tab-btn ${activePage === 'records' ? 'active' : ''}`}
            onClick={() => setActivePage('records')}
          >
            <span className="nav-tab-icon">📋</span>
            <span className="nav-tab-text">My Patient Records</span>
            <span className="nav-count-pill">{patients.length}</span>
          </button>
        </nav>

        <div className="nav-status">
          <span className="status-dot"></span>
          <span className="user-label">{user.full_name || user.email}</span>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </header>

      <main className="main-content">
        {/* ================= PAGE 1: PATIENT ASSESSMENT FORM ================= */}
        {activePage === 'assessment' && (
          <div className="page-view animate-fade">
            <section className="welcome-section">
              <div>
                <p className="eyebrow">HSDN CLINICAL ASSESSMENT WORKFLOW</p>
                <h1>Patient Assessment <span>Form</span></h1>
                <p className="welcome-description">
                  Enter patient demographics, vitals, and select symptoms across organ system categories
                  to initiate the probabilistic disease prediction model.
                </p>
              </div>
              <div className="welcome-icon">📝</div>
            </section>

            <section className="dashboard-grid">
              <div className="form-card">
                <div className="card-heading">
                  <div>
                    <h2>Patient Intake & Symptoms</h2>
                    <p>Complete all sections below and click Generate Prediction</p>
                  </div>
                  <span className="card-icon">👤</span>
                </div>

                <form onSubmit={handleSubmit}>
                  {/* BLOCK 1: Patient Identity & Demographics */}
                  <div className="form-section-block">
                    <div className="block-title">
                      <span>1</span> Patient Identification & Demographics
                    </div>

                    <div className="form-group">
                      <label>Patient / User Full Name *</label>
                      <input
                        type="text"
                        name="patient_name"
                        placeholder="e.g. Karthikeya, John Doe"
                        value={form.patient_name}
                        onChange={handleChange}
                        required
                      />
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Patient Age *</label>
                        <input
                          type="number"
                          name="age"
                          placeholder="Enter age (years)"
                          min="0"
                          max="120"
                          value={form.age}
                          onChange={handleChange}
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label>Biological Gender *</label>
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
                  </div>

                  {/* BLOCK 2: Selected Symptoms Summary & Quick Custom Add */}
                  <div className="form-section-block">
                    <div className="block-title">
                      <span>2</span> Clinical Symptoms by Organ System
                    </div>

                    {/* Selected Symptoms Pill Bar */}
                    <div className="selected-symptoms-bar">
                      <div className="selected-bar-header">
                        <strong>Selected Symptoms:</strong> ({form.symptoms.length} chosen)
                        {form.symptoms.length > 0 && (
                          <button
                            type="button"
                            className="clear-symptoms-btn"
                            onClick={() => setForm((p) => ({ ...p, symptoms: [] }))}
                          >
                            Clear All
                          </button>
                        )}
                      </div>
                      {form.symptoms.length === 0 ? (
                        <p className="no-symptoms-hint">
                          No symptoms selected yet. Choose from the categories below or type a custom symptom.
                        </p>
                      ) : (
                        <div className="symptom-tag-container">
                          {form.symptoms.map((sym) => (
                            <span key={sym} className="selected-symptom-pill">
                              {sym}
                              <button
                                type="button"
                                onClick={() => handleRemoveSymptom(sym)}
                                title="Remove symptom"
                              >
                                ×
                              </button>
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Quick Add Custom Symptom */}
                    <div className="custom-symptom-adder">
                      <input
                        type="text"
                        placeholder="Type a specific symptom (e.g. chills, mouth ulcers, swollen glands)..."
                        value={customSymptom}
                        onChange={(e) => setCustomSymptom(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault()
                            handleAddCustomSymptom(e)
                          }
                        }}
                      />
                      <button
                        type="button"
                        className="add-symptom-btn"
                        onClick={handleAddCustomSymptom}
                      >
                        + Add Symptom
                      </button>
                    </div>

                    {/* Categorized Symptom Blocks */}
                    <div className="symptom-categories-wrapper">
                      {symptomCategories.map((cat) => (
                        <div key={cat.id} className="symptom-category-box">
                          <div className="category-header">
                            <span className="cat-icon">{cat.icon}</span>
                            <div>
                              <h4>{cat.name}</h4>
                              <span className="cat-desc">{cat.description}</span>
                            </div>
                          </div>

                          <div className="category-symptom-grid">
                            {cat.symptoms.map((symptom) => {
                              const isChecked = form.symptoms.includes(symptom)
                              return (
                                <label
                                  key={symptom}
                                  className={`category-symptom-item ${isChecked ? 'active' : ''}`}
                                >
                                  <input
                                    type="checkbox"
                                    checked={isChecked}
                                    onChange={() => handleSymptomToggle(symptom)}
                                  />
                                  <span>{symptom}</span>
                                </label>
                              )
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* BLOCK 3: Symptom Dynamics & Vitals */}
                  <div className="form-section-block">
                    <div className="block-title">
                      <span>3</span> Symptom Dynamics & Clinical Vitals
                    </div>

                    <div className="form-row-3">
                      <div className="form-group">
                        <label>Duration (Days) *</label>
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

                      <div className="form-group">
                        <label>Symptom Severity</label>
                        <select
                          name="severity"
                          value={form.severity}
                          onChange={handleChange}
                        >
                          <option value="Mild">Mild</option>
                          <option value="Moderate">Moderate</option>
                          <option value="Severe">Severe</option>
                        </select>
                      </div>

                      <div className="form-group">
                        <label>Onset Pattern</label>
                        <select
                          name="onset"
                          value={form.onset}
                          onChange={handleChange}
                        >
                          <option value="Gradual">Gradual / Progressive</option>
                          <option value="Acute">Sudden / Acute</option>
                        </select>
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Blood Pressure</label>
                        <select
                          name="blood_pressure"
                          value={form.blood_pressure}
                          onChange={handleChange}
                        >
                          <option value="Normal">Normal</option>
                          <option value="Low">Low</option>
                          <option value="High">High</option>
                        </select>
                      </div>

                      <div className="form-group">
                        <label>Cholesterol Level</label>
                        <select
                          name="cholesterol_level"
                          value={form.cholesterol_level}
                          onChange={handleChange}
                        >
                          <option value="Normal">Normal</option>
                          <option value="Low">Low</option>
                          <option value="High">High</option>
                        </select>
                      </div>
                    </div>

                    <div className="form-group">
                      <label>Additional Clinical Observations & Context</label>
                      <textarea
                        name="additional_notes"
                        placeholder="Enter any additional observations, known exposures, or medication notes..."
                        value={form.additional_notes}
                        onChange={handleChange}
                        maxLength="500"
                        rows="2"
                      />
                    </div>
                  </div>

                  <button type="submit" className="submit-button" disabled={loading}>
                    {loading ? 'Evaluating Symptoms & Modeling Probabilities...' : 'Generate Disease Prediction & Clinical Insights →'}
                  </button>
                </form>
              </div>

              <aside className="info-column">
                <div className="info-card">
                  <span className="info-icon">🌐</span>
                  <h3>HSDN Network Model</h3>
                  <p>
                    Evaluates multi-organ symptom constellations against literature co-occurrence networks
                    to calculate true multi-class disease probabilities.
                  </p>
                </div>

                <div className="info-card">
                  <span className="info-icon">🔬</span>
                  <h3>Reasons & Underlying Causes</h3>
                  <p>
                    Predictions explain both <strong>Why</strong> the patient matches this condition and
                    <strong>What</strong> biological / cellular mechanisms cause the disease.
                  </p>
                </div>

                <div className="notice-card">
                  <h3>⚠️ Healthcare Notice</h3>
                  <p>
                    MedAssist AI is an educational clinical decision-support tool. It is not a formal medical diagnosis.
                    Always consult a licensed physician.
                  </p>
                </div>
              </aside>
            </section>
          </div>
        )}

        {/* ================= PAGE 2: AI DISEASE PREDICTION & DIAGNOSTIC INSIGHTS ================= */}
        {activePage === 'prediction' && (
          <div className="page-view animate-fade">
            <section className="welcome-section prediction-hero">
              <div>
                <p className="eyebrow">DECISION-SUPPORT DIAGNOSTICS</p>
                <h1>AI Disease Prediction <span>& Diagnostic Insights</span></h1>
                <p className="welcome-description">
                  Comprehensive multi-class disease probability analysis, clinical reasoning,
                  underlying pathophysiological causes, and differential diagnoses.
                </p>
              </div>
              <div className="welcome-icon">🩺</div>
            </section>

            {loading && (
              <div className="loading-card">
                <div className="spinner"></div>
                <h2>Evaluating Clinical Constellation...</h2>
                <p>Computing disease probability distribution, cellular causes, and differential rankings.</p>
              </div>
            )}

            {error && (
              <div className="error-card">
                <h2>⚠️ Prediction Warning</h2>
                <p>{error}</p>
                <button
                  type="button"
                  className="tab-action-btn"
                  onClick={() => setActivePage('assessment')}
                  style={{ marginTop: '12px' }}
                >
                  ← Return to Assessment Form
                </button>
              </div>
            )}

            {!loading && prediction && (
              <div>
                <PredictionResults result={prediction} />
                <div className="prediction-actions-row">
                  <button
                    type="button"
                    className="tab-action-btn secondary"
                    onClick={() => setActivePage('assessment')}
                  >
                    ← Perform Another Assessment
                  </button>
                  <button
                    type="button"
                    className="tab-action-btn primary"
                    onClick={() => setActivePage('records')}
                  >
                    View My Patient Records →
                  </button>
                </div>
              </div>
            )}

            {!loading && !prediction && !error && (
              <div className="empty-page-card">
                <div className="empty-icon">🩺</div>
                <h2>No Prediction Generated Yet</h2>
                <p>
                  Please complete and submit the Patient Assessment Form with patient demographics
                  and clinical symptoms to view the AI prediction and diagnostic insights here.
                </p>
                <button
                  type="button"
                  className="tab-action-btn primary"
                  onClick={() => setActivePage('assessment')}
                >
                  Go to Patient Assessment Form →
                </button>
              </div>
            )}
          </div>
        )}

        {/* ================= PAGE 3: MY PATIENT RECORDS ================= */}
        {activePage === 'records' && (
          <div className="page-view animate-fade">
            <section className="welcome-section records-hero">
              <div>
                <p className="eyebrow">PATIENT DATABASE & HISTORY</p>
                <h1>My Patient <span>Records</span></h1>
                <p className="welcome-description">
                  View and manage historical patient symptom assessments, recorded vitals,
                  and diagnostic entries stored in your clinical workspace.
                </p>
              </div>
              <div className="welcome-icon">📋</div>
            </section>

            <section className="patient-records-section">
              <div className="records-header">
                <div>
                  <h2>Patient History Directory</h2>
                  <p className="records-sub">All patient intake and symptom records associated with your account</p>
                </div>
                <div className="records-actions">
                  <span className="records-count-badge">{patients.length} Total Records</span>
                  <button
                    type="button"
                    className="new-assessment-btn"
                    onClick={() => setActivePage('assessment')}
                  >
                    + New Patient Assessment
                  </button>
                </div>
              </div>

              {patients.length === 0 ? (
                <div className="empty-page-card" style={{ boxShadow: 'none', border: 'none' }}>
                  <div className="empty-icon">📋</div>
                  <h2>No Patient Records Available</h2>
                  <p>You have not submitted any patient symptom records yet.</p>
                  <button
                    type="button"
                    className="tab-action-btn primary"
                    onClick={() => setActivePage('assessment')}
                  >
                    Submit First Assessment →
                  </button>
                </div>
              ) : (
                <div className="records-grid">
                  {patients.map((patient) => (
                    <div key={patient.id} className="patient-record-card">
                      <div className="record-top">
                        <span className="record-id-badge">Record #{patient.id}</span>
                        <h3 className="patient-record-name">
                          {patient.patient_name || 'Anonymous Patient'}
                        </h3>
                        <span className="record-meta">
                          {patient.age} yrs • {patient.gender}
                        </span>
                      </div>

                      <div className="record-symptoms">
                        <strong>Reported Symptoms ({Array.isArray(patient.symptoms) ? patient.symptoms.length : 1}):</strong>
                        <div className="record-symptom-pills">
                          {Array.isArray(patient.symptoms)
                            ? patient.symptoms.map((s, idx) => (
                                <span key={idx} className="record-pill">
                                  {s}
                                </span>
                              ))
                            : <span>{patient.symptoms}</span>}
                        </div>
                      </div>

                      <div className="record-vitals-row">
                        <span><strong>Duration:</strong> {patient.duration_days} days</span>
                        <span><strong>BP:</strong> {patient.blood_pressure || 'Normal'}</span>
                        <span><strong>Cholesterol:</strong> {patient.cholesterol_level || 'Normal'}</span>
                      </div>

                      {patient.additional_notes && patient.additional_notes !== 'No additional notes' && (
                        <p className="record-notes">
                          <strong>Notes:</strong> {patient.additional_notes}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}

        <footer>
          © 2026 MedAssist AI | Clinical Decision-Support & Diagnostic Analytics
        </footer>
      </main>
    </div>
  )
}

export default App
