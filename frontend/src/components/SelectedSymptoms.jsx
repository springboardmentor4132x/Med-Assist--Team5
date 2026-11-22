import { X, Trash2, ClipboardList } from 'lucide-react';

export default function SelectedSymptoms({ selected, onRemove, onClearAll }) {
  return (
    <div
      className="rounded-xl border p-4 transition-colors duration-200"
      style={{
        backgroundColor: 'rgb(var(--card))',
        borderColor: selected.length > 0 ? 'rgb(var(--sel-border) / 0.4)' : 'rgb(var(--border))',
      }}
    >
      {/* Header row */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <ClipboardList className="w-4 h-4" style={{ color: '#2563EB' }} />
          <span className="text-sm font-semibold" style={{ color: 'rgb(var(--text))' }}>
            Selected Symptoms
          </span>
          <span
            className="text-xs font-bold px-2 py-0.5 rounded-full"
            style={selected.length > 0 ? {
              backgroundColor: '#2563EB',
              color: '#fff',
            } : {
              backgroundColor: 'rgb(var(--border))',
              color: 'rgb(var(--text-muted))',
            }}
          >
            {selected.length} selected
          </span>
        </div>

        {selected.length > 0 && (
          <button
            onClick={onClearAll}
            className="flex items-center gap-1 text-xs font-medium transition-colors duration-150 px-2 py-1 rounded-lg"
            style={{ color: '#DC2626' }}
            onMouseEnter={e => { e.currentTarget.style.backgroundColor = 'rgb(220 38 38 / 0.08)'; }}
            onMouseLeave={e => { e.currentTarget.style.backgroundColor = 'transparent'; }}
          >
            <Trash2 className="w-3.5 h-3.5" />
            Clear All
          </button>
        )}
      </div>

      {/* Chips or empty state */}
      {selected.length === 0 ? (
        <p className="text-xs" style={{ color: 'rgb(var(--text-muted))' }}>
          No symptoms selected yet. Click any symptom card above to add it.
        </p>
      ) : (
        <div className="flex flex-wrap gap-1.5">
          {selected.map(symptom => (
            <span
              key={symptom.id}
              className="inline-flex items-center gap-1 pl-2.5 pr-1 py-1 rounded-full text-xs font-medium border anim-fade-up"
              style={{
                backgroundColor: 'rgb(var(--sel-bg))',
                borderColor: 'rgb(var(--sel-border) / 0.35)',
                color: 'rgb(var(--sel-border))',
              }}
            >
              {symptom.name}
              <button
                onClick={() => onRemove(symptom.id)}
                aria-label={`Remove ${symptom.name}`}
                className="w-4 h-4 rounded-full flex items-center justify-center transition-colors duration-150 ml-0.5"
                style={{ backgroundColor: 'rgb(var(--sel-border) / 0.15)' }}
                onMouseEnter={e => { e.currentTarget.style.backgroundColor = 'rgb(220 38 38 / 0.15)'; e.currentTarget.style.color = '#DC2626'; }}
                onMouseLeave={e => { e.currentTarget.style.backgroundColor = 'rgb(var(--sel-border) / 0.15)'; e.currentTarget.style.color = 'inherit'; }}
              >
                <X className="w-2.5 h-2.5" />
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
