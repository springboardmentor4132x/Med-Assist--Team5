
let toastId = 0;

const listeners = new Set();
let toasts = [];

export function pushToast(message, type = 'info') {
  setTimeout(() => {
    const id = ++toastId;
    toasts = [...toasts, { id, message, type }];
    listeners.forEach((fn) => fn(toasts));

    setTimeout(() => {
      toasts = toasts.filter((toast) => toast.id !== id);
      listeners.forEach((fn) => fn(toasts));
    }, 2400);
  }, 0);
}

export function subscribeToasts(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}
