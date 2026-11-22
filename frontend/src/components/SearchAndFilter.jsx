import { Search, X } from 'lucide-react';

const CATEGORIES = ['All', 'General', 'Respiratory', 'Digestive', 'Pain', 'Skin', 'Other'];

export default function SearchAndFilter({ query, onQueryChange, activeCategory, onCategoryChange }) {
  return (
    <div className="space-y-3">
      {/* Search input */}
      <div className="relative">
        <Search
          className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4"
          style={{ color: 'rgb(var(--text-muted))' }}
        />
        <input
          type="text"
          value={query}
          onChange={e => onQueryChange(e.target.value)}
          placeholder="Search symptoms..."
          className="w-full pl-10 pr-9 py-2.5 text-sm rounded-xl border outline-none transition-all duration-150"
          style={{
            backgroundColor: 'rgb(var(--card))',
            border: query
              ? '1.5px solid #2563EB'
              : '1.5px solid rgb(var(--border))',
            color: 'rgb(var(--text))',
          }}
          onFocus={e => { e.target.style.borderColor = '#2563EB'; e.target.style.boxShadow = '0 0 0 3px rgb(37 99 235 / 0.1)'; }}
          onBlur={e  => {
            e.target.style.borderColor = query ? '#2563EB' : 'rgb(var(--border))';
            e.target.style.boxShadow = 'none';
          }}
        />
        {query && (
          <button
            onClick={() => onQueryChange('')}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 w-6 h-6 rounded-full flex items-center justify-center transition-colors duration-150"
            style={{ backgroundColor: 'rgb(var(--border))', color: 'rgb(var(--text-muted))' }}
            aria-label="Clear search"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Category filter tabs */}
      <div className="flex gap-1.5 overflow-x-auto no-scrollbar pb-0.5">
        {CATEGORIES.map(cat => {
          const active = activeCategory === cat;
          return (
            <button
              key={cat}
              onClick={() => onCategoryChange(cat)}
              className="shrink-0 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 border"
              style={active ? {
                backgroundColor: '#2563EB',
                color: '#fff',
                borderColor: '#2563EB',
              } : {
                backgroundColor: 'rgb(var(--card))',
                color: 'rgb(var(--text-muted))',
                borderColor: 'rgb(var(--border))',
              }}
              onMouseEnter={e => { if (!active) { e.currentTarget.style.borderColor = '#2563EB'; e.currentTarget.style.color = '#2563EB'; }}}
              onMouseLeave={e => { if (!active) { e.currentTarget.style.borderColor = 'rgb(var(--border))'; e.currentTarget.style.color = 'rgb(var(--text-muted))'; }}}
            >
              {cat === 'All' ? 'All Symptoms' : cat}
            </button>
          );
        })}
      </div>
    </div>
  );
}
