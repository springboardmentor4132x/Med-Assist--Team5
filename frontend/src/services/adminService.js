const API_BASE_URL = 'http://127.0.0.1:8000'

async function request(path, token, options = {}) {
  const { params, ...fetchOptions } = options

  const query = params
    ? new URLSearchParams(
        Object.entries(params).filter(
          ([, value]) => value !== undefined && value !== null && value !== ''
        )
      ).toString()
    : ''

  const url = `${API_BASE_URL}${path}${query ? `?${query}` : ''}`

  const response = await fetch(url, {
    ...fetchOptions,
    headers: {
      ...(fetchOptions.body ? { 'Content-Type': 'application/json' } : {}),
      Authorization: `Bearer ${token}`,
      ...fetchOptions.headers,
    },
  })

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(
      typeof data.detail === 'string'
        ? data.detail
        : 'Admin API request failed.'
    )
  }

  return data
}

export const adminService = {
  getDashboardStats: (token) =>
    request('/admin/dashboard', token),

  getUsers: (token, params = {}) =>
    request('/admin/users', token, { params }),

  getUserDetails: (token, userId) =>
    request(`/admin/users/${userId}`, token),

  updateUserInfo: (token, userId, data) =>
    request(`/admin/users/${userId}`, token, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  updateUserStatus: (token, userId, isActive) =>
    request(`/admin/users/${userId}/status`, token, {
      method: 'PATCH',
      body: JSON.stringify({ is_active: isActive }),
    }),

  updateUserRole: (token, userId, roleName) =>
    request(`/admin/users/${userId}/role`, token, {
      method: 'PUT',
      body: JSON.stringify({ role_name: roleName }),
    }),

  getPatients: (token, params = {}) =>
    request('/admin/patients', token, { params }),

  getDoctors: (token, params = {}) =>
    request('/admin/doctors', token, { params }),

  getClinics: (token, params = {}) =>
    request('/admin/clinics', token, { params }),

  getAccount: (token) =>
    request('/admin/account', token),

  updateAccount: (token, data) =>
    request('/admin/account', token, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  getAssignments: (token) =>
    request('/admin/assignments', token),

  createAssignment: (token, doctorId, patientId) =>
    request('/admin/assignments', token, {
      method: 'POST',
      body: JSON.stringify({
        doctor_id: doctorId,
        patient_id: patientId,
      }),
    }),

  deleteAssignment: (token, assignmentId) =>
    request(`/admin/assignments/${assignmentId}`, token, {
      method: 'DELETE',
    }),

  getClinicAssignments: (token) =>
    request('/admin/clinic-assignments', token),

  createClinicAssignment: (token, clinicId, doctorId) =>
    request('/admin/clinic-assignments', token, {
      method: 'POST',
      body: JSON.stringify({
        clinic_id: clinicId,
        doctor_id: doctorId,
      }),
    }),

  deleteClinicAssignment: (token, assignmentId) =>
    request(`/admin/clinic-assignments/${assignmentId}`, token, {
      method: 'DELETE',
    }),
  createUser: (token, userData) =>
    request('/admin/users', token, {
      method: 'POST',
      body: JSON.stringify(userData),
    }),

  deleteUser: (token, userId) =>
    request(`/admin/users/${userId}`, token, {
      method: 'DELETE',
    }),
  }
