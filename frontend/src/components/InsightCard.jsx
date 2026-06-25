import React, { useState } from 'react'

const SEVERITY_CONFIG = {
  Low:      { color: 'var(--blue)',   bg: 'var(--blue-bg)',   icon: 'ℹ' },
  Mild:     { color: 'var(--yellow)', bg: 'var(--yellow-bg)', icon: '◐' },
  Moderate: { color: 'var(--orange)', bg: 'var(--orange-bg)', icon: '⚠' },
  High:     { color: 'var(--red)',    bg: 'var(--red-bg)',    icon: '▲' },
}

/**
 * InsightCard — actionable insight card for an "Area to Improve".
 * Shows severity, causes, tips, and estimated improvement timeline.
 *
 * @param {object} area - The area object from backend insights.areasToImprove[]
 *   shape: { area, severity, causes[], tips[], timeline }
 */
export default function InsightCard({ area, delay = 0 }) {
  const [expanded, setExpanded] = useState(false)

  // Support both legacy string format and new object format
  if (typeof area === 'string') {
    return (
      <li className="insight-card insight-card-simple" style={{ animationDelay: `${delay}ms` }}>
        <span style={{ color: 'var(--orange)' }}>⚠</span> {area}
      </li>
    )
  }

  const { area: title, severity = 'Low', causes = [], tips = [], timeline } = area
  const cfg = SEVERITY_CONFIG[severity] || SEVERITY_CONFIG.Low

  return (
    <div
      className="insight-card"
      style={{ animationDelay: `${delay}ms`, borderColor: cfg.color + '44' }}
    >
      {/* Header */}
      <div className="insight-card-header" onClick={() => setExpanded(e => !e)}>
        <div className="insight-card-left">
          <span
            className="insight-severity-chip"
            style={{ background: cfg.bg, color: cfg.color }}
          >
            {cfg.icon} {severity}
          </span>
          <span className="insight-card-title">{title}</span>
        </div>
        <span className="insight-card-chevron" style={{ color: cfg.color }}>
          {expanded ? '▲' : '▼'}
        </span>
      </div>

      {/* Expandable body */}
      {expanded && (
        <div className="insight-card-body fade-up">
          {causes.length > 0 && (
            <div className="insight-section">
              <div className="insight-section-label">Possible Causes</div>
              <ul className="insight-causes-list">
                {causes.map((c, i) => (
                  <li key={i}><span style={{ color: 'var(--text-dim)' }}>•</span> {c}</li>
                ))}
              </ul>
            </div>
          )}

          {tips.length > 0 && (
            <div className="insight-section">
              <div className="insight-section-label">What You Can Do</div>
              <ul className="insight-tips-list">
                {tips.map((t, i) => (
                  <li key={i}>
                    <span style={{ color: cfg.color }}>▸</span> {t}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {timeline && (
            <div className="insight-timeline">
              <span className="insight-timeline-icon">🕐</span>
              <span className="insight-timeline-label">Timeline:</span>
              <span className="insight-timeline-val">{timeline}</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
