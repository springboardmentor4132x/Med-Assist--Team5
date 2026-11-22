

export default function LoadingIndicator({ message = 'Loading healthcare records...' }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '3rem 1rem',
      gap: '1rem',
      width: '100%'
    }}>
      <div style={{
        width: '42px',
        height: '42px',
        border: '3px solid #E9F8F0',
        borderTop: '3px solid #16A36A',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite'
      }} />
      <span style={{ fontSize: '0.9rem', color: '#728078', fontWeight: 500 }}>
        {message}
      </span>
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
