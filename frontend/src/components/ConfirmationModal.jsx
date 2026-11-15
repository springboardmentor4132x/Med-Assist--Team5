import React from 'react';
import { CheckCircle, X } from 'lucide-react';

export default function ConfirmationModal({ symptoms, onClose }) {
  return (
    <div className="fixed inset-0 z-[70] flex items-center justify-center p-4">
      {/* backdrop */}
      <div
        className="absolute inset-0 anim-scale-in"
        style={{ backgroundColor: 'rgb(0 0 0 / 0.5)', backdropFilter: 'blur(4px)' }}
        onClick={onClose}
      />

      {/* Modal card */}
      <div
        className="relative w-full max-w-md rounded-2xl p-7 shadow-2xl anim-scale-in"
        style={{ backgroundColor: 'rgb(var(--card))', border: '1px solid rgb(var(--border))' }}
      >
        <button
          onClick={onClose}
          className="absolute top-4 right-4 w-7 h-7 rounded-lg flex items-center justify-center transition-colors duration-150"
          style={{ backgroundColor: 'rgb(var(--border))', color: 'rgb(var(--text-muted))' }}
          aria-label="Close"
        >
          <X className="w-3.5 h-3.5" />
        </button>

        {/* Success icon */}
        <div className="flex flex-col items-center text-center mb-5">
          <div
            className="w-14 h-14 rounded-full flex items-center justify-center mb-3"
            style={{ backgroundColor: 'rgb(22 163 74 / 0.1)' }}
          >
            <CheckCircle className="w-7 h-7" style={{ color: '#16A34A' }} />
          </div>
          <h3 className="text-lg font-bold mb-1" style={{ color: 'rgb(var(--text))' }}>
            Symptoms Submitted
          </h3>
          <p className="text-sm" style={{ color: 'rgb(var(--text-muted))' }}>
            {symptoms.length} {symptoms.length !== 1 ? 'symptoms' : 'symptom'} recorded successfully.
          </p>
        </div>

        {/* Symptom list */}
        <div
          className="rounded-xl p-3.5 mb-5 max-h-44 overflow-y-auto"
          style={{ backgroundColor: 'rgb(var(--bg))' }}
        >
          <p className="text-[11px] font-semibold uppercase tracking-wider mb-2.5" style={{ color: 'rgb(var(--text-muted))' }}>
            Recorded symptoms
          </p>
          <div className="flex flex-wrap gap-1.5">
            {symptoms.map(s => (
              <span
                key={s.id}
                className="text-xs font-medium px-2.5 py-1 rounded-full border"
                style={{
                  backgroundColor: 'rgb(var(--sel-bg))',
                  borderColor: 'rgb(var(--sel-border) / 0.3)',
                  color: 'rgb(var(--sel-border))',
                }}
              >
                {s.name}
              </span>
            ))}
          </div>
        </div>

        {/* Disclaimer inside modal */}
        <p className="text-[11px] text-center mb-4" style={{ color: 'rgb(var(--text-muted))' }}>
          This tool is for informational purposes and does not replace professional medical advice.
        </p>

        <button
          onClick={onClose}
          className="w-full py-2.5 rounded-xl text-sm font-semibold text-white transition-opacity duration-150 hover:opacity-90"
          style={{ backgroundColor: '#2563EB' }}
        >
          Done
        </button>
      </div>
    </div>
  );
}
