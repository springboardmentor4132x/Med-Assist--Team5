export default function AdminNavbar({
  pageTitle = 'Dashboard',
  user,
  onLogout,
}) {
  return (
    <header style={{
      minHeight: '70px',
      backgroundColor: '#FFFFFF',
      borderBottom: '1px solid var(--border-color)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: '1rem',
      padding: '0 2rem',
      position: 'sticky',
      top: 0,
      zIndex: 10,
    }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>
        {pageTitle}
      </h2>

      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
      }}>
        <div>
          <div style={{ fontWeight: 600, fontSize: '0.875rem' }}>
            {user?.full_name || 'Administrator'}
          </div>
          <div style={{
            color: 'var(--text-secondary)',
            fontSize: '0.75rem',
          }}>
            {user?.email || ''}
          </div>
        </div>

        <button
          type="button"
          onClick={onLogout}
          className="btn btn-secondary btn-sm"
        >
          Sign Out
        </button>
      </div>
    </header>
  )
}
