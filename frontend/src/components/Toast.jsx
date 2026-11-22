
import { useState, useEffect } from 'react';
import { subscribeToasts } from '../services/toastService';

export function ToastContainer() {
  const [list, setList] = useState([]);

  useEffect(() => {
    const unsubscribe = subscribeToasts((toasts) => {
      setList([...toasts]);
    });

    return unsubscribe;
  }, []);

  return (
    <div className="fixed bottom-24 right-4 z-[80] flex flex-col gap-2 items-end pointer-events-none">
      {list.map((toast) => (
        <ToastItem key={toast.id} {...toast} />
      ))}
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
