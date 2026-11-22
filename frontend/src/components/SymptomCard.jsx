import * as LucideIcons from 'lucide-react';

export default function SymptomCard({ symptom, isSelected, onToggle }) {
  const Icon = LucideIcons[symptom.icon] || LucideIcons.Activity;

  return (
    <button
      onClick={() => onToggle(symptom)}
      aria-pressed={isSelected}
      className="group relative w-full text-left rounded-xl border transition-all duration-150 outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
      style={{
        padding: '12px 14px',
        backgroundColor: isSelected ? 'rgb(var(--sel-bg))' : 'rgb(var(--card))',
        borderColor: isSelected ? 'rgb(var(--sel-border))' : 'rgb(var(--border))',
        borderWidth: isSelected ? '1.5px' : '1px',
        boxShadow: isSelected ? '0 0 0 0px transparent' : '0 1px 2px rgb(0 0 0 / 0.04)',
      }}
      onMouseEnter={e => {
        if (!isSelected) {
          e.currentTarget.style.borderColor = 'rgb(var(--sel-border))';
          e.currentTarget.style.boxShadow = '0 2px 8px rgb(37 99 235 / 0.08)';
        }
      }}
      onMouseLeave={e => {
        if (!isSelected) {
          e.currentTarget.style.borderColor = 'rgb(var(--border))';
          e.currentTarget.style.boxShadow = '0 1px 2px rgb(0 0 0 / 0.04)';
        }
      }}
    >
      {/* Checkmark badge */}
      <div
        className={`absolute top-2 right-2 w-4.5 h-4.5 rounded-full flex items-center justify-center transition-all duration-150 ${isSelected ? 'opacity-100 anim-check' : 'opacity-0 scale-50'}`}
        style={{ backgroundColor: '#2563EB', width: 18, height: 18 }}
        aria-hidden="true"
      >
        <LucideIcons.Check className="w-2.5 h-2.5 text-white" strokeWidth={3} />
      </div>

      <div className="flex items-center gap-2.5">
        {/* Icon container */}
        <div
          className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 transition-colors duration-150"
          style={{
            backgroundColor: isSelected
              ? 'rgb(37 99 235 / 0.12)'
              : 'rgb(var(--border) / 0.5)',
          }}
        >
          <Icon
            className="w-4 h-4"
            style={{ color: isSelected ? '#2563EB' : 'rgb(var(--text-muted))' }}
          />
        </div>

        {/* Name */}
        <span
          className="text-sm font-medium leading-tight pr-4"
          style={{ color: isSelected ? 'rgb(var(--sel-border))' : 'rgb(var(--text))' }}
        >
          {symptom.name}
        </span>
      </div>
    </button>
  );
}
