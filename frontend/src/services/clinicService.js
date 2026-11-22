
const API_BASE_URL = 'http://127.0.0.1:8000'

async function request(path, token) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.detail || data.message || 'Request failed.')
  }

  return data
}

export const clinicService = {
  getDashboard: (token) =>
    request('/clinic/dashboard', token),

  getDoctors: (token) =>
    request('/clinic/doctors', token),

  getPatients: (token) =>
    request('/clinic/patients', token),

  getPatientDetails: (token, patientId) =>
    request(`/clinic/patients/${patientId}`, token),

  getProfile: (token) =>
    request('/clinic/profile', token),
}
