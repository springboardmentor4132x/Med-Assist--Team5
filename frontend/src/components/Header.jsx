import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function Header() {
  const { isDark, toggle } = useTheme();

  return (
    <header
      className="sticky top-0 z-50 border-b"
      style={{
        backgroundColor: 'rgb(var(--header-bg) / 0.92)',
        borderColor: 'rgb(var(--border))',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
      }}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

        {/* ── Brand ── */}
        <div className="flex items-center gap-3">
          {/* Medical cross logo */}
          <div
            className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
            style={{ backgroundColor: '#2563EB' }}
            aria-hidden="true"
          >
            <svg viewBox="0 0 24 24" fill="none" className="w-5 h-5 text-white" stroke="white" strokeWidth="2.5" strokeLinecap="round">
              <path d="M12 5v14M5 12h14" />
            </svg>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-base tracking-tight" style={{ color: 'rgb(var(--text))' }}>
                MediAssist AI
              </span>
              {/* System online dot */}
              <span className="hidden sm:inline-flex items-center gap-1.5 text-[11px] font-medium px-2 py-0.5 rounded-full border"
                style={{
                  backgroundColor: 'rgb(22 163 74 / 0.08)',
                  borderColor: 'rgb(22 163 74 / 0.25)',
                  color: '#16A34A',
                }}>
                <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                Online
              </span>
            </div>
            <p className="hidden sm:block text-[11px] leading-none mt-0.5" style={{ color: 'rgb(var(--text-muted))' }}>
              AI-Powered Medical Symptom Analysis Platform
            </p>
          </div>
        </div>

        {/* ── Right: theme toggle ── */}
        <button
          onClick={toggle}
          aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
          className="w-9 h-9 rounded-lg flex items-center justify-center transition-colors duration-200 border"
          style={{
            backgroundColor: 'rgb(var(--card))',
            borderColor: 'rgb(var(--border))',
            color: 'rgb(var(--text-muted))',
          }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = '#2563EB'; e.currentTarget.style.color = '#2563EB'; }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgb(var(--border))'; e.currentTarget.style.color = 'rgb(var(--text-muted))'; }}
        >
          {isDark
            ? <Sun  className="w-4 h-4" />
            : <Moon className="w-4 h-4" />}
        </button>
      </div>
    </header>
  );
}
