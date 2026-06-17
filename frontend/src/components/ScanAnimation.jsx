import React from 'react'

export default function ScanAnimation({ imageUrl }) {
  return (
    <div className="scan-page fade-up">
      <div className="scan-container">
        <img src={imageUrl} alt="Scanning" />
        <div className="scan-glow" />
        <div className="scan-line" />
        <div className="scan-overlay" />
      </div>

      <div className="scan-info">
        <div className="scan-title">Analyzing Your Features</div>
        <div className="scan-subtitle">Scanning 54 facial features…</div>
        <div className="scan-dots">
          <div className="scan-dot" />
          <div className="scan-dot" />
          <div className="scan-dot" />
        </div>
      </div>

      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '8px',
        justifyContent: 'center',
        maxWidth: 400,
      }}>
        {[
          'Face Shape', 'Eye Analysis', 'Brow Mapping',
          'Nose Metrics', 'Lip Ratio', 'Jaw Structure',
          'Skin Tone', 'Golden Ratio',
        ].map((step, i) => (
          <span
            key={step}
            style={{
              fontSize: '0.72rem',
              padding: '3px 10px',
              borderRadius: '100px',
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-dim)',
              color: 'var(--text-muted)',
              animation: `pulse 1.5s ease ${i * 0.2}s infinite`,
            }}
          >
            {step}
          </span>
        ))}
      </div>
    </div>
  )
}
