import api from './api';

export const authService = {
  /**
   * Common login handler for all roles (Patient, Doctor, Clinic, Admin)
   */
  async login(email, password) {
    const response = await api.post('/auth/login', { email, password });
    if (response.data && response.data.access_token) {
      localStorage.setItem('medassist_token', response.data.access_token);
      localStorage.setItem('medassist_user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  /**
   * Register a new user account (Patient, Doctor, Clinic)
   */
  async register(fullName, email, password, roleName = 'Patient') {
    const response = await api.post('/auth/register', {
      full_name: fullName,
      email,
      password,
      role_name: roleName
    });
    return response.data;
  },

  /**
   * Terminate active session
   */
  logout() {
    localStorage.removeItem('medassist_token');
    localStorage.removeItem('medassist_user');
    window.location.href = '/login';
  },

  /**
   * Get currently authenticated user details
   */
  getCurrentUser() {
    const userStr = localStorage.getItem('medassist_user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  },

  /**
   * Get raw JWT
   */
  getToken() {
    return localStorage.getItem('medassist_token');
  },

  /**
   * Check if a valid session exists
   */
  isAuthenticated() {
    return !!this.getToken() && !!this.getCurrentUser();
  },

  /**
   * Check if active user has Admin role
   */
  isAdmin() {
    const user = this.getCurrentUser();
    return user && user.role === 'Admin';
  }
};
