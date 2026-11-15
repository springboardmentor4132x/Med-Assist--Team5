import React from 'react';
import SymptomAnalysis from './components/SymptomAnalysis';
import Header from './components/Header';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: 'rgb(var(--bg))' }}>
      <Header />

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32">
        <SymptomAnalysis />
      </main>

      <footer
        className="border-t text-center py-5 text-xs"
        style={{
          borderColor: 'rgb(var(--border))',
          color: 'rgb(var(--text-muted))',
          backgroundColor: 'rgb(var(--header-bg))',
        }}
      >
        © 2026 MediAssist AI · AI-Powered Medical Symptom Analysis and Disease Prediction Intelligence Platform
      </footer>
    </div>
  );
}
