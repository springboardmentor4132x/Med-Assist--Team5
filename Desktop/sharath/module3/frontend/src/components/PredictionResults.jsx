import React from 'react'
import './PredictionResults.css'

function PredictionResults({ result }) {
  if (!result) return null

  // Extract primary prediction data defensively
  const primary = result.primary_prediction || {}
  const diseaseName = result.predicted_disease || primary.disease || result.prediction_result?.prediction || 'Undetermined Condition'
  const confidenceTier = result.confidence || primary.confidence_tier || 'Clinical Screening'
  const probabilityPercent = primary.probability_percent || (primary.probability ? `${(primary.probability * 100).toFixed(1)}%` : '75.0%')
  const probabilityNum = primary.probability ? primary.probability * 100 : 75
  const category = primary.category || 'General Medical Condition'
  const clinicalReason = result.clinical_reason || primary.clinical_reason || 'Symptom pattern matches known disease correlations.'
  const diseaseCause = result.cause_of_disease || primary.cause || 'Underlying physiological dysregulation.'
  const pathophysiology = result.pathophysiology || primary.pathophysiology || ''
  const recommendedAction = result.recommended_action || primary.recommended_action || 'Consult a healthcare physician for formal examination and diagnosis.'
  const topPredictions = result.top_predictions || []

  // Determine confidence badge style
  let badgeClass = 'confidence-high'
  if (confidenceTier.includes('Moderate')) {
    badgeClass = 'confidence-moderate'
  } else if (confidenceTier.includes('Screening') || confidenceTier.includes('Low')) {
    badgeClass = 'confidence-screening'
  }

  return (
    <div className="prediction-results-card">
      <div className="results-header">
        <h2>
          <span>🩺</span> AI Disease Prediction & Diagnostic Insights
        </h2>
        <span className="results-tag">HSDN Network Model</span>
      </div>

      {/* Primary Predicted Disease Banner */}
      <div className="primary-prediction-box">
        <div className="primary-top-row">
          <div className="disease-title-area">
            <div className="category-label">{category}</div>
            <h3>{diseaseName}</h3>
          </div>
          <div className={`confidence-badge ${badgeClass}`}>
            <span>●</span> {confidenceTier} ({probabilityPercent})
          </div>
        </div>

        {/* Probability Progress Bar */}
        <div className="probability-bar-container">
          <div className="probability-bar-label">
            <span>Model Association Strength</span>
            <span>{probabilityPercent}</span>
          </div>
          <div className="probability-bar-track">
            <div
              className="probability-bar-fill"
              style={{ width: `${Math.min(probabilityNum, 100)}%` }}
            />
          </div>
        </div>
      </div>

      {/* 2-Column Insights Grid: Reason & Cause */}
      <div className="insights-grid">
        {/* Why this prediction (Clinical Reason) */}
        <div className="insight-card reason-card">
          <div className="insight-header">
            <span>📋</span> Clinical Reason (Why this was predicted)
          </div>
          <p className="insight-content">
            {clinicalReason}
          </p>
        </div>

        {/* Cause of Disease (Underlying Etiology) */}
        <div className="insight-card cause-card">
          <div className="insight-header">
            <span>🔬</span> Underlying Cause & Etiology
          </div>
          <p className="insight-content">
            {diseaseCause}
          </p>
          {pathophysiology && (
            <p className="insight-content" style={{ marginTop: '8px', fontSize: '13px', color: '#607282' }}>
              <strong>Mechanism:</strong> {pathophysiology}
            </p>
          )}
        </div>
      </div>

      {/* Top 3 Differential Diagnoses */}
      {topPredictions.length > 0 && (
        <div className="differential-section">
          <div className="section-title">
            <span>📊</span> Top Ranked Differential Diagnoses
          </div>
          <div className="differential-list">
            {topPredictions.map((pred, index) => (
              <div key={pred.disease || index} className="differential-item">
                <div className="diff-rank-disease">
                  <div className={`diff-rank-badge rank-${pred.rank || index + 1}`}>
                    {pred.rank || index + 1}
                  </div>
                  <div className="diff-info">
                    <div className="diff-name">{pred.disease}</div>
                    <div className="diff-category">{pred.category}</div>
                  </div>
                </div>
                <div className="diff-score-badge">
                  {pred.probability_percent} Match
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Clinical Next Steps & Recommendations */}
      <div className="recommendations-box">
        <h4>
          <span>⚕️</span> Recommended Clinical Next Steps
        </h4>
        <p>{recommendedAction}</p>
      </div>

      {/* Medical Safety Disclaimer */}
      <div className="results-disclaimer">
        <strong>⚠️ Healthcare Safety Notice:</strong> {result.notice || 'MedAssist AI is an educational clinical decision-support tool. Predictions are not medical diagnoses. Always seek advice from a licensed physician.'}
      </div>
    </div>
  )
}

export default PredictionResults
