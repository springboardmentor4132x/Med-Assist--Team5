
const API_URL = "http://127.0.0.1:8000";

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
      throw new Error(data.detail || "Prediction failed");
    }

    return data;

  } catch (error) {
    console.error("Prediction API Error:", error);
    throw error;
  }
};
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
    throw new Error(data.detail || 'Failed to save patient')
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
