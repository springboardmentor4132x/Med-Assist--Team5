import api from './api';

export const adminService = {
  // Dashboard Analytics
  async getDashboardStats() {
    const res = await api.get('/admin/dashboard');
    return res.data;
  },

  // User Management
  async getUsers(params = {}) {
    const res = await api.get('/admin/users', { params });
    return res.data;
  },

  async getUserDetails(userId) {
    const res = await api.get(`/admin/users/${userId}`);
    return res.data;
  },

  async updateUserInfo(userId, data) {
    const res = await api.put(`/admin/users/${userId}`, data);
    return res.data;
  },

  async updateUserStatus(userId, isActive) {
    const res = await api.patch(`/admin/users/${userId}/status`, { is_active: isActive });
    return res.data;
  },

  async updateUserRole(userId, roleName) {
    const res = await api.put(`/admin/users/${userId}/role`, { role_name: roleName });
    return res.data;
  },

  // Specialized Lists
  async getPatients(params = {}) {
    const res = await api.get('/admin/patients', { params });
    return res.data;
  },

  async getDoctors(params = {}) {
    const res = await api.get('/admin/doctors', { params });
    return res.data;
  },

  async getClinics(params = {}) {
    const res = await api.get('/admin/clinics', { params });
    return res.data;
  },

  // Account Settings
  async getAccount() {
    const res = await api.get('/admin/account');
    return res.data;
  },

  async updateAccount(data) {
    const res = await api.put('/admin/account', data);
    return res.data;
  }
};
