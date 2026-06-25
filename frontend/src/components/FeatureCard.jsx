import React from 'react'

// Feature icon map (emoji or SVG char per feature type)
const ICONS = {
  'Face Shape':      { icon: '◯', color: 'var(--green)',  bg: 'var(--green-bg)' },
  'Eyes':            { icon: '👁', color: 'var(--blue)',   bg: 'var(--blue-bg)'  },
  'Eyebrows':        { icon: '〜', color: 'var(--orange)', bg: 'var(--orange-bg)'},
  'Nose':            { icon: '▽', color: 'var(--orange)', bg: 'var(--orange-bg)'},
  'Lips':            { icon: '❧', color: 'var(--red)',    bg: 'var(--red-bg)'   },
  'Jaw & Chin':      { icon: '⌒', color: 'var(--yellow)', bg: 'var(--yellow-bg)'},
  'Skin':            { icon: '◈', color: 'var(--teal)',   bg: 'var(--teal-bg)'  },
  'Facial Symmetry': { icon: '⇔', color: 'var(--blue)',   bg: 'var(--blue-bg)'  },
}

function getBadgeClass(value) {
  if (typeof value === 'number') return 'badge-green'
  const v = String(value).toLowerCase()
  if (['oval','almond','balanced','ideal','visible','defined','refined','centered','normal','medium','straight','arched'].some(k => v.includes(k))) return 'badge-green'
  if (['wide','broad','prominent','thick'].some(k => v.includes(k))) return 'badge-orange'
  if (['narrow','thin','flat','recessed','minimal','close'].some(k => v.includes(k))) return 'badge-blue'
  if (['soft','slight','mild'].some(k => v.includes(k))) return 'badge-yellow'
  return 'badge-default'
}

function ScoreBar({ label, value, color = 'var(--green)' }) {
  return (
    <div>
      <div className="score-bar-wrap" style={{ marginTop: 8 }}>
        <div className="score-bar-track">
          <div
            className="score-bar-fill"
            style={{ width: `${value}%`, background: color }}
          />
        </div>
        <span className="score-bar-label" style={{ color }}>{value}%</span>
      </div>
    </div>
  )
}

function MetricRow({ label, value, color }) {
  return (
    <div className="metric-row">
      <span className="metric-label">{label}</span>
      <span className="metric-value" style={{ color: color || 'var(--green)' }}>
        {value}
        <span style={{ color: 'var(--text-dim)', fontWeight: 400, fontSize: '0.7rem' }}> ›</span>
      </span>
    </div>
  )
}

/**
 * FeatureCard
 * @param {string} title       - Feature section name
 * @param {string} badge       - Main classification label
 * @param {number} score       - Optional 0-100 score to show as bar
 * @param {string} scoreLabel  - Label for the score bar
 * @param {string} metric      - Optional metric label (e.g. "Canthal Tilt")
 * @param {string} metricValue - Optional metric value (e.g. "+3.2°")
 * @param {string} desc        - Description text
 * @param {number} delay       - Animation delay
 * @param {number} confidence  - Optional 0-100 confidence score for this feature
 */
export default function FeatureCard({
  title,
  badge,
  score,
  scoreLabel,
  metric,
  metricValue,
  desc,
  delay = 0,
  confidence,
}) {
  const theme = ICONS[title] || { icon: '◆', color: 'var(--green)', bg: 'var(--green-bg)' }

  return (
    <div
      className="feature-card"
      style={{
        borderColor: `${theme.color}33`,
        animationDelay: `${delay}ms`,
      }}
    >
      {/* Header */}
      <div className="feature-card-header">
        <div
          className="feature-card-icon"
          style={{ background: theme.bg, color: theme.color }}
        >
          {theme.icon}
        </div>
        <span className="feature-card-name">{title}</span>
        {confidence !== undefined && (
          <span
            className="feature-card-conf"
            title={`Analysis confidence: ${confidence}%`}
          >
            {confidence}%
          </span>
        )}
      </div>

      {/* Badge */}
      {badge && (
        <span className={`badge ${getBadgeClass(badge)}`}>{badge}</span>
      )}

      {/* Score bar */}
      {score !== undefined && (
        <ScoreBar label={scoreLabel} value={score} color={theme.color} />
      )}

      {/* Metric row */}
      {metric && metricValue && (
        <MetricRow label={metric} value={metricValue} color={theme.color} />
      )}

      {/* Description */}
      {desc && <p className="feature-card-desc">{desc}</p>}
    </div>
  )
}
