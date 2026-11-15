import React, { useState, useEffect, useCallback } from 'react';

let toastId = 0;

/** Global toast state — simple singleton so any component can push */
const listeners = new Set();
let toasts = [];

export function pushToast(message, type = 'info') {
  // Defer state update outside React's render cycle to avoid the
  // "Cannot update a component while rendering a different component" warning.
  setTimeout(() => {
    const id = ++toastId;
    toasts = [...toasts, { id, message, type }];
    listeners.forEach(fn => fn(toasts));
    setTimeout(() => {
      toasts = toasts.filter(t => t.id !== id);
      listeners.forEach(fn => fn(toasts));
    }, 2400);
  }, 0);
}

export function ToastContainer() {
  const [list, setList] = useState([]);
  useEffect(() => {
    const fn = t => setList([...t]);
    listeners.add(fn);
    return () => listeners.delete(fn);
  }, []);

  return (
    <div className="fixed bottom-24 right-4 z-[80] flex flex-col gap-2 items-end pointer-events-none">
      {list.map(t => <ToastItem key={t.id} {...t} />)}
    </div>
  );
}

function ToastItem({ message, type }) {
  const [out, setOut] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setOut(true), 2000);
    return () => clearTimeout(timer);
  }, []);

  const bg = type === 'success'
    ? '#16A34A'
    : type === 'remove'
    ? '#64748B'
    : '#2563EB';

  return (
    <div
      className={`pointer-events-auto text-white text-[13px] font-medium px-3.5 py-2 rounded-lg shadow-lg flex items-center gap-2 ${out ? 'anim-toast-out' : 'anim-toast-in'}`}
      style={{ backgroundColor: bg, maxWidth: 240 }}
    >
      <span
        className="w-4 h-4 rounded-full flex items-center justify-center shrink-0"
        style={{ backgroundColor: 'rgba(255,255,255,0.22)' }}
      >
        {type === 'success' ? '✓' : type === 'remove' ? '−' : 'i'}
      </span>
      {message}
    </div>
  );
}
