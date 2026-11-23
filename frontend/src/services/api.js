
const API_URL = "http://127.0.0.1:8000";
// Convert backend validation errors into readable messages
const formatApiError = (detail) => {
  if (typeof detail === 'string') {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => item.msg || 'Invalid input')
      .join(' ');
  }

  return 'Something went wrong. Please try again.';
};

export const predictPatient = async (patientData) => {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(patientData),
    });

    const data = await response.json();

    if (!response.ok) {
  throw new Error(formatApiError(data.detail));
}

    return data;


  } catch (error) {
    console.error("Prediction API Error:", error);
    throw error;
  }
};


export const predictExpandedDiseases = async (patientData, token) => {
  const response = await fetch(`${API_URL}/predict-diseases`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(patientData),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(formatApiError(data.detail))
  }

  return data
}


export const getPatients = async (token) => {
  const response = await fetch(
    `${API_URL}/patients`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || 'Failed to fetch patients')
  }

  return data
}
export const savePatient = async (patientData, token) => {
  const response = await fetch(`${API_URL}/symptoms`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(patientData)
  })

  const data = await response.json()

 if (!response.ok) {
  throw new Error(formatApiError(data.detail));
}

  return data
}

export const logoutUser = async (token) => {
  const response = await fetch(`${API_URL}/auth/logout`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || 'Logout failed')
  }

  return data
}

// Get patients assigned to the logged-in doctor
export const getAssignedDoctorPatients = async (token) => {
  const response = await fetch(`${API_URL}/doctor/patients`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(formatApiError(data.detail))
  }

  return data
}

// Get details of one assigned patient
export const getAssignedPatientDetails = async (token, patientId) => {
  const response = await fetch(
    `${API_URL}/doctor/patients/${patientId}`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(formatApiError(data.detail))
  }

  return data
}
