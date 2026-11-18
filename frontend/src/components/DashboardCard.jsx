import React from 'react';

export default function DashboardCard({ title, value, icon, subtitle, color = 'var(--primary-green)' }) {
  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          {title}
        </span>
        <div style={{
          width: '40px',
          height: '40px',
          borderRadius: 'var(--radius-md)',
          backgroundColor: 'var(--light-green)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.25rem'
        }}>
          {icon}
        </div>
      </div>

      <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.03em' }}>
        {value}
      </div>

      {subtitle && (
        <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
          {subtitle}
        </span>
      )}
    </div>
  );
}
