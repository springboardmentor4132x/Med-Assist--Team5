import React from 'react';

export default function ConfirmationModal({
  isOpen,
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  isDanger = false,
  onConfirm,
  onCancel,
  isLoading = false
}) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            backgroundColor: isDanger ? '#FEEBEB' : '#E9F8F0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: isDanger ? '#DC5555' : '#16A36A',
            fontSize: '1.25rem',
            fontWeight: 'bold'
          }}>
            {isDanger ? '!' : '✓'}
          </div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 600 }}>{title}</h3>
        </div>

        <p style={{ color: '#728078', fontSize: '0.9rem', marginBottom: '1.5rem', lineHeight: 1.5 }}>
          {message}
        </p>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
            disabled={isLoading}
          >
            {cancelText}
          </button>
          <button
            type="button"
            className={`btn ${isDanger ? 'btn-danger' : 'btn-primary'}`}
            onClick={onConfirm}
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
