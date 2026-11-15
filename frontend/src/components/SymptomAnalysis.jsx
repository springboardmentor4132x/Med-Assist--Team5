import React, { useState, useMemo, useCallback, useEffect } from 'react';
import { Stethoscope, SearchX, AlertTriangle, Send, Loader2, Info } from 'lucide-react';

import symptomsData from '../data/symptomsData';
import SymptomCard from './SymptomCard';
import SelectedSymptoms from './SelectedSymptoms';
import SearchAndFilter from './SearchAndFilter';
import ConfirmationModal from './ConfirmationModal';
import { ToastContainer, pushToast } from './Toast';

const TOTAL = symptomsData.length;

/* ── Sticky bottom bar ─────────────────────────────────── */
function ActionBar({ count, onSubmit, loading }) {
  const enabled = count > 0 && !loading;

  return (
    <div
      className="fixed bottom-0 left-0 right-0 z-50 border-t"
      style={{
        backgroundColor: 'rgb(var(--header-bg) / 0.95)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        borderColor: 'rgb(var(--border))',
      }}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between gap-4">
        <p className="text-xs" style={{ color: 'rgb(var(--text-muted))' }}>
          {count === 0
            ? 'Select at least one symptom to continue.'
            : `${count} symptom${count !== 1 ? 's' : ''} selected.`}
        </p>

        <button
          onClick={onSubmit}
          disabled={!enabled}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold text-white transition-all duration-150"
          style={enabled ? {
            backgroundColor: '#2563EB',
            cursor: 'pointer',
          } : {
            backgroundColor: 'rgb(var(--border))',
            color: 'rgb(var(--text-muted))',
            cursor: 'not-allowed',
          }}
          onMouseEnter={e => { if (enabled) e.currentTarget.style.backgroundColor = '#1D4ED8'; }}
          onMouseLeave={e => { if (enabled) e.currentTarget.style.backgroundColor = '#2563EB'; }}
          onMouseDown={e  => { if (enabled) e.currentTarget.style.backgroundColor = '#1E40AF'; }}
          onMouseUp={e    => { if (enabled) e.currentTarget.style.backgroundColor = '#1D4ED8'; }}
        >
          {loading
            ? <Loader2 className="w-4 h-4 anim-spin" />
            : <Send className="w-4 h-4" />}
          {loading ? 'Submitting…' : 'Submit Symptoms'}
          {count > 0 && !loading && (
            <span
              className="text-[11px] font-bold px-1.5 py-0.5 rounded-full"
              style={{ backgroundColor: 'rgba(255,255,255,0.22)' }}
            >
              {count}
            </span>
          )}
        </button>
      </div>
    </div>
  );
}

/* ── Emergency warning banner ──────────────────────────── */
function EmergencyWarning() {
  return (
    <div
      className="rounded-xl border p-3.5 flex gap-3 items-start anim-fade-up"
      style={{
        backgroundColor: 'rgb(220 38 38 / 0.06)',
        borderColor: 'rgb(220 38 38 / 0.25)',
      }}
    >
      <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" style={{ color: '#DC2626' }} />
      <p className="text-xs leading-relaxed" style={{ color: '#DC2626' }}>
        <strong>Seek immediate medical attention</strong> if you are experiencing severe chest pain,
        difficulty breathing, or any symptom you consider a medical emergency. Do not rely on this
        tool in an emergency situation.
      </p>
    </div>
  );
}

/* ── Disclaimer bar ────────────────────────────────────── */
function Disclaimer() {
  return (
    <div
      className="rounded-xl border p-3 flex gap-2.5 items-center"
      style={{
        backgroundColor: 'rgb(var(--ai-hl))',
        borderColor: 'rgb(var(--cyan) / 0.2)',
      }}
    >
      <Info className="w-3.5 h-3.5 shrink-0" style={{ color: 'rgb(var(--cyan))' }} />
      <p className="text-xs" style={{ color: 'rgb(var(--text-muted))' }}>
        This tool is intended for <strong>informational purposes only</strong> and does not replace
        professional medical advice, diagnosis, or treatment.
      </p>
    </div>
  );
}

/* ── Main component ────────────────────────────────────── */
export default function SymptomAnalysis() {
  const [selected, setSelected]           = useState([]);
  const [query, setQuery]                 = useState('');
  const [activeCategory, setActiveCategory] = useState('All');
  const [showModal, setShowModal]         = useState(false);
  const [loading, setLoading]             = useState(false);
  const [submitted, setSubmitted]         = useState(false); // prevent double-submit
  const [showEmergency, setShowEmergency] = useState(false);

  /* Warn if an emergency symptom is selected */
  useEffect(() => {
    setShowEmergency(selected.some(s => s.emergency));
  }, [selected]);

  /* Combined filter: search + category */
  const visible = useMemo(() => {
    return symptomsData.filter(s => {
      const matchSearch = s.name.toLowerCase().includes(query.trim().toLowerCase());
      const matchCat    = activeCategory === 'All' || s.category === activeCategory;
      return matchSearch && matchCat;
    });
  }, [query, activeCategory]);

  /* Toggle selection */
  const toggleSymptom = useCallback((symptom) => {
    setSelected(prev => {
      const exists = prev.find(s => s.id === symptom.id);
      if (exists) {
        pushToast(`Removed: ${symptom.name}`, 'remove');
        return prev.filter(s => s.id !== symptom.id);
      }
      pushToast(`Added: ${symptom.name}`, 'success');
      return [...prev, symptom];
    });
  }, []);

  const removeSymptom = useCallback((id) => {
    setSelected(prev => {
      const sym = prev.find(s => s.id === id);
      if (sym) pushToast(`Removed: ${sym.name}`, 'remove');
      return prev.filter(s => s.id !== id);
    });
  }, []);

  const clearAll = useCallback(() => {
    setSelected([]);
    pushToast('All symptoms cleared', 'remove');
  }, []);

  /* Submit */
  const handleSubmit = useCallback(() => {
    if (selected.length === 0 || loading || submitted) return;
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSubmitted(true);
      setShowModal(true);
    }, 900); // simulated latency
  }, [selected, loading, submitted]);

  const handleModalClose = useCallback(() => {
    setShowModal(false);
    setSubmitted(false);
  }, []);

  const isSelected = useCallback((id) => selected.some(s => s.id === id), [selected]);

  return (
    <>
      <div className="space-y-5 anim-fade-up">

        {/* ── Hero heading ── */}
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
              style={{ backgroundColor: 'rgb(var(--sel-bg))', border: '1px solid rgb(var(--border))' }}
            >
              <Stethoscope className="w-5 h-5" style={{ color: '#2563EB' }} />
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold leading-tight" style={{ color: 'rgb(var(--text))' }}>
                Symptom Analysis
              </h1>
              <p className="text-sm mt-0.5" style={{ color: 'rgb(var(--text-muted))' }}>
                Select all the symptoms you are currently experiencing.
              </p>
            </div>
          </div>

          {/* Available count */}
          <div
            className="hidden sm:flex flex-col items-end shrink-0"
          >
            <span className="text-2xl font-bold" style={{ color: '#2563EB' }}>{TOTAL}</span>
            <span className="text-[11px]" style={{ color: 'rgb(var(--text-muted))' }}>symptoms available</span>
          </div>
        </div>

        {/* ── Disclaimer ── */}
        <Disclaimer />

        {/* ── Emergency warning (conditional) ── */}
        {showEmergency && <EmergencyWarning />}

        {/* ── Search + filters ── */}
        <SearchAndFilter
          query={query}
          onQueryChange={setQuery}
          activeCategory={activeCategory}
          onCategoryChange={setActiveCategory}
        />

        {/* ── Selected symptoms panel ── */}
        <SelectedSymptoms
          selected={selected}
          onRemove={removeSymptom}
          onClearAll={clearAll}
        />

        {/* ── Symptom grid ── */}
        {visible.length > 0 ? (
          <div>
            <p className="text-xs mb-3" style={{ color: 'rgb(var(--text-muted))' }}>
              {visible.length === TOTAL
                ? `Showing all ${TOTAL} symptoms`
                : `${visible.length} of ${TOTAL} symptoms`}
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5">
              {visible.map(symptom => (
                <SymptomCard
                  key={symptom.id}
                  symptom={symptom}
                  isSelected={isSelected(symptom.id)}
                  onToggle={toggleSymptom}
                />
              ))}
            </div>
          </div>
        ) : (
          /* ── Empty state ── */
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div
              className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
              style={{ backgroundColor: 'rgb(var(--border))' }}
            >
              <SearchX className="w-6 h-6" style={{ color: 'rgb(var(--text-muted))' }} />
            </div>
            <p className="font-semibold text-sm mb-1" style={{ color: 'rgb(var(--text))' }}>
              No symptoms found
            </p>
            <p className="text-xs" style={{ color: 'rgb(var(--text-muted))' }}>
              Try a different keyword or select another category.
            </p>
          </div>
        )}

        {/* Spacer so sticky bar doesn't cover content */}
        <div className="h-4" />
      </div>

      {/* ── Sticky action bar ── */}
      <ActionBar
        count={selected.length}
        onSubmit={handleSubmit}
        loading={loading}
      />

      {/* ── Confirmation modal ── */}
      {showModal && (
        <ConfirmationModal
          symptoms={selected}
          onClose={handleModalClose}
        />
      )}

      {/* ── Toast portal ── */}
      <ToastContainer />
    </>
  );
}
