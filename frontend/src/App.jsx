import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import AdminDashboard from './pages/AdminDashboard';
import ManageUsers from './pages/ManageUsers';
import ManagePatients from './pages/ManagePatients';
import ManageDoctors from './pages/ManageDoctors';
import ManageClinics from './pages/ManageClinics';
import ManageRoles from './pages/ManageRoles';
import AccountSettings from './pages/AccountSettings';
import Unauthorized from './pages/Unauthorized';
import RoleDashboard from './pages/RoleDashboard';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Common Login Route */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />

        {/* Protected Administrative Routes (Member 5) */}
        <Route
          path="/admin-dashboard"
          element={
            <ProtectedRoute requiredRole="Admin">
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/manage-users"
          element={
            <ProtectedRoute requiredRole="Admin">
              <ManageUsers />
            </ProtectedRoute>
          }
        />
        <Route
          path="/manage-patients"
          element={
            <ProtectedRoute requiredRole="Admin">
              <ManagePatients />
            </ProtectedRoute>
          }
        />
        <Route
          path="/manage-doctors"
          element={
            <ProtectedRoute requiredRole="Admin">
              <ManageDoctors />
            </ProtectedRoute>
          }
        />
        <Route
          path="/manage-clinics"
          element={
            <ProtectedRoute requiredRole="Admin">
              <ManageClinics />
            </ProtectedRoute>
          }
        />
        <Route
          path="/manage-roles"
          element={
            <ProtectedRoute requiredRole="Admin">
              <ManageRoles />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account-settings"
          element={
            <ProtectedRoute requiredRole="Admin">
              <AccountSettings />
            </ProtectedRoute>
          }
        />

        {/* Role Redirection Landing Portals */}
        <Route
          path="/doctor-dashboard"
          element={
            <ProtectedRoute requiredRole="Doctor">
              <RoleDashboard
                title="Doctor Clinical Workspace"
                description="Welcome to your clinical dashboard. Review patient appointments and medical histories."
                icon="👨‍⚕️"
              />
            </ProtectedRoute>
          }
        />
        <Route
          path="/clinic-dashboard"
          element={
            <ProtectedRoute requiredRole="Clinic">
              <RoleDashboard
                title="Clinic Administration Facility"
                description="Welcome to the clinic management portal. Manage facility registrations, doctors and appointments."
                icon="🏥"
              />
            </ProtectedRoute>
          }
        />
        <Route
          path="/patient-dashboard"
          element={
            <ProtectedRoute requiredRole="Patient">
              <RoleDashboard
                title="Patient Personal Health Portal"
                description="Welcome to your personal health portal. View your appointments, profiles, and medical history."
                icon="🩺"
              />
            </ProtectedRoute>
          }
        />

        {/* Security & Access Denied */}
        <Route path="/unauthorized" element={<Unauthorized />} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
