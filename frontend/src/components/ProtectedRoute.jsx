import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { authService } from '../services/authService';

export default function ProtectedRoute({ children, requiredRole = 'Admin' }) {
  const location = useLocation();
  const isAuthenticated = authService.isAuthenticated();
  const currentUser = authService.getCurrentUser();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole && currentUser?.role !== requiredRole) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
}
