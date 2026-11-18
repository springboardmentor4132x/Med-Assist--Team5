import React from 'react';

export default function UserTable({
  users = [],
  onViewDetails,
  onEditUser,
  onToggleStatus,
  onChangeRole,
  isLoading = false
}) {
  const getRoleBadgeClass = (role) => {
    switch (role?.toLowerCase()) {
      case 'admin': return 'badge-admin';
      case 'doctor': return 'badge-doctor';
      case 'clinic': return 'badge-clinic';
      default: return 'badge-patient';
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    } catch {
      return dateStr;
    }
  };

  if (isLoading) {
    return (
      <div className="table-responsive" style={{ padding: '3rem', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Loading user records...</p>
      </div>
    );
  }

  if (!users || users.length === 0) {
    return (
      <div className="table-responsive" style={{ padding: '3rem', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>No user records found matching criteria.</p>
      </div>
    );
  }

  return (
    <div className="table-responsive">
      <table className="data-table">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Full Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Registered</th>
            <th style={{ textAlign: 'right' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>#{user.id}</td>
              <td style={{ fontWeight: 600 }}>{user.full_name}</td>
              <td style={{ color: 'var(--text-secondary)' }}>{user.email}</td>
              <td>
                <span className={`badge ${getRoleBadgeClass(user.role)}`}>
                  {user.role}
                </span>
              </td>
              <td>
                <span className={`badge ${user.is_active ? 'badge-active' : 'badge-inactive'}`}>
                  ● {user.is_active ? 'Active' : 'Inactive'}
                </span>
              </td>
              <td style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                {formatDate(user.created_at)}
              </td>
              <td style={{ textAlign: 'right' }}>
                <div style={{ display: 'inline-flex', gap: '0.4rem', justifyContent: 'flex-end' }}>
                  {onViewDetails && (
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => onViewDetails(user)}
                      title="View Details"
                    >
                      View
                    </button>
                  )}
                  {onEditUser && (
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => onEditUser(user)}
                      title="Edit Account"
                    >
                      Edit
                    </button>
                  )}
                  {onToggleStatus && (
                    <button
                      className={`btn btn-sm ${user.is_active ? 'btn-outline-danger' : 'btn-primary'}`}
                      onClick={() => onToggleStatus(user)}
                      title={user.is_active ? 'Deactivate Account' : 'Activate Account'}
                    >
                      {user.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                  )}
                  {onChangeRole && (
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => onChangeRole(user)}
                      title="Change Role"
                    >
                      Role
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
