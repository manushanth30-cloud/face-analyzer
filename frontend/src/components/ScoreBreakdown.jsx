import React, { useState } from 'react'

/**
 * ScoreBreakdown — transparent score formula panel.
 * Shows each sub-score with its weight and contribution to the final /10 score.
 */
export default function ScoreBreakdown({ harmonyScores, score10 }) {
  const [open, setOpen] = useState(false)

  if (!harmonyScores) return null

  const breakdown = harmonyScores.scoreBreakdown
  const components = breakdown
    ? [
        { ...breakdown.goldenRatio,   score: harmonyScores.goldenRatioScore,       color: 'var(--yellow)' },
        { ...breakdown.symmetry,      score: harmonyScores.overallSymmetry,         color: 'var(--blue)'   },
        { ...breakdown.neoclassical,  score: harmonyScores.neoclassicalCompliance,  color: 'var(--purple)' },
      ]
    : [
        { label: 'Golden Ratio',       score: harmonyScores.goldenRatioScore,       weight: 0.35, color: 'var(--yellow)', description: 'How closely your facial proportions follow the golden ratio (φ≈1.618).' },
        { label: 'Facial Symmetry',    score: harmonyScores.overallSymmetry,        weight: 0.30, color: 'var(--blue)',   description: 'Left-to-right bilateral symmetry across eyes, lips, jaw, and cheekbones.' },
        { label: 'Classic Proportions',score: harmonyScores.neoclassicalCompliance, weight: 0.35, color: 'var(--purple)', description: 'Adherence to neoclassical canons (da Vinci): equal thirds, balanced inter-feature distances.' },
      ]

  const final100 = components.reduce((sum, c) => sum + c.score * c.weight, 0)

  return (
    <div className="sbd-wrap">
      <button className="sbd-toggle" onClick={() => setOpen(o => !o)}>
        <span className="sbd-toggle-icon">{open ? '▲' : '▼'}</span>
        <span>How is this score calculated?</span>
      </button>

      {open && (
        <div className="sbd-body fade-up">
          <div className="sbd-intro">
            Your <strong>Facial Harmony Score</strong> is computed from 3 scientific dimensions,
            each measured against established facial proportion studies.
          </div>

          {components.map((c, i) => {
            const contribution = Math.round(c.score * c.weight)
            const pct = c.score
            return (
              <div key={i} className="sbd-row">
                <div className="sbd-row-top">
                  <div className="sbd-row-left">
                    <span className="sbd-dot" style={{ background: c.color }} />
                    <div>
                      <div className="sbd-label">{c.label}</div>
                      <div className="sbd-desc">{c.description}</div>
                    </div>
                  </div>
                  <div className="sbd-row-right">
                    <span className="sbd-score" style={{ color: c.color }}>{c.score}</span>
                    <span className="sbd-denom">/100</span>
                    <span className="sbd-weight">×{Math.round(c.weight * 100)}%</span>
                    <span className="sbd-contrib" style={{ color: c.color }}>= {contribution}</span>
                  </div>
                </div>
                <div className="sbd-bar-track">
                  <div className="sbd-bar-fill" style={{ width: `${pct}%`, background: c.color }} />
                </div>

                {/* Sub-components if available */}
                {c.components && (
                  <div className="sbd-subcoms">
                    {c.components.map((sub, j) => (
                      <div key={j} className="sbd-subcom">
                        <span className="sbd-subcom-name">{sub.name}</span>
                        {sub.ideal && (
                          <span className="sbd-subcom-ideal">
                            yours: <strong>{sub.yours}</strong> · ideal: {sub.ideal}
                          </span>
                        )}
                        <div className="sbd-subcom-bar-track">
                          <div className="sbd-subcom-bar-fill" style={{ width: `${sub.score}%`, background: c.color + '99' }} />
                        </div>
                        <span className="sbd-subcom-score" style={{ color: c.color }}>{sub.score}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )
          })}

          {/* Final formula */}
          <div className="sbd-formula">
            <div className="sbd-formula-row">
              {components.map((c, i) => (
                <span key={i}>
                  <span style={{ color: c.color }}>{Math.round(c.score * c.weight)}</span>
                  {i < components.length - 1 && <span className="sbd-plus"> + </span>}
                </span>
              ))}
              <span className="sbd-equals"> = </span>
              <span className="sbd-final">{Math.round(final100)}</span>
              <span className="sbd-final-denom">/100 → {score10}/10</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
