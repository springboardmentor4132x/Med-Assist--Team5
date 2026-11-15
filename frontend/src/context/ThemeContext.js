import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const ThemeContext = createContext();
export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(() => {
    try {
      const stored = localStorage.getItem('mediassist-theme');
      if (stored === 'dark' || stored === 'light') return stored === 'dark';
    } catch (_) {}
    return window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false;
  });

  useEffect(() => {
    const root = document.documentElement;
    if (isDark) root.classList.add('dark');
    else root.classList.remove('dark');
    try { localStorage.setItem('mediassist-theme', isDark ? 'dark' : 'light'); } catch (_) {}
  }, [isDark]);

  const toggle = useCallback(() => {
    const root = document.documentElement;
    root.classList.add('theme-switching');
    setIsDark(prev => !prev);
    setTimeout(() => root.classList.remove('theme-switching'), 400);
  }, []);

  return (
    <ThemeContext.Provider value={{ isDark, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
};
