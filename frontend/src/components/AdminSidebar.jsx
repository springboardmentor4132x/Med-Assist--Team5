const navItems = [
  { label: 'Dashboard', icon: '▦' },
  { label: 'Manage Users', icon: '♙' },
  { label: 'Manage Patients', icon: '♡' },
  { label: 'Manage Doctors', icon: '⚕' },
  { label: 'Manage Clinics', icon: '⌂' },
  { label: 'Manage Roles', icon: '⚙' },
  { label: 'Assignments', icon: '⇄' },
  { label: 'Account Settings', icon: '⚙' },
]

export default function AdminSidebar({
  activePage,
  onNavigate,
  onLogout,
}) {
  return (
    <aside style={{
      width: '260px',
      backgroundColor: '#FFFFFF',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      flexShrink: 0,
      minHeight: '100vh',
    }}>
      <div style={{
        padding: '1.5rem',
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
      }}>
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '8px',
          backgroundColor: 'var(--primary-green)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#ffffff',
          fontWeight: 'bold',
          fontSize: '1.2rem',
        }}>
          +
        </div>
        <div>
          <h1 style={{ fontSize: '1.15rem', fontWeight: 700 }}>
            MedAssist AI
          </h1>
          <p style={{
            fontSize: '0.7rem',
            color: 'var(--text-secondary)',
            textTransform: 'uppercase',
          }}>
            Admin Portal
          </p>
        </div>
      </div>

      <nav style={{
        padding: '1rem 0.75rem',
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        gap: '0.35rem',
      }}>
        {navItems.map((item) => (
          <button
            key={item.label}
            type="button"
            onClick={() => onNavigate(item.label)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              padding: '0.75rem 1rem',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.875rem',
              fontWeight: activePage === item.label ? 600 : 500,
              color: activePage === item.label
                ? 'var(--dark-green)'
                : 'var(--text-secondary)',
              backgroundColor: activePage === item.label
                ? 'var(--light-green)'
                : 'transparent',
              border: 'none',
              borderLeft: activePage === item.label
                ? '3px solid var(--primary-green)'
                : '3px solid transparent',
              textAlign: 'left',
              cursor: 'pointer',
            }}
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div style={{
        padding: '1rem',
        borderTop: '1px solid var(--border-color)',
      }}>
        <button
          type="button"
          onClick={onLogout}
          className="btn btn-outline-danger"
          style={{ width: '100%' }}
        >
          Sign Out
        </button>
      </div>
    </aside>
  )
}
