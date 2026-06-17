import React, { useEffect, useRef } from 'react'

/**
 * ScoreGauge — SVG circular arc gauge with animation.
 * @param {number}  value     - Score 0–100
 * @param {string}  label     - e.g. "Overall Balance"
 * @param {string}  sublabel  - e.g. "Measures overall facial proportions"
 * @param {string}  color     - CSS color string for the arc
 * @param {number}  delay     - Animation delay in ms
 */
export default function ScoreGauge({ value, label, sublabel, color, delay = 0 }) {
  const arcRef = useRef(null)

  const SIZE   = 110
  const STROKE = 8
  const R      = (SIZE - STROKE) / 2
  // Arc spans 240° (starts at 150°, ends at 390° = 30°)
  const ARC_DEGREES = 240
  const CIRCUM = 2 * Math.PI * R
  const arcLen = (ARC_DEGREES / 360) * CIRCUM

  const pct    = Math.min(100, Math.max(0, value))
  const filled = (pct / 100) * arcLen
  const gap    = arcLen - filled

  // Convert start angle to SVG coordinates
  // 0° = 3 o'clock, rotate to start at bottom-left (150° from 3 o'clock)
  const startAngle = 150  // degrees from top (SVG)
  const startRad   = ((startAngle - 90) * Math.PI) / 180
  const cx = SIZE / 2
  const cy = SIZE / 2

  const rating =
    value >= 85 ? 'Excellent' :
    value >= 75 ? 'Very Good' :
    value >= 60 ? 'Good'      :
    value >= 45 ? 'Fair'      : 'Developing'

  const ratingColor =
    value >= 85 ? 'var(--green)'  :
    value >= 75 ? 'var(--green)'  :
    value >= 60 ? 'var(--yellow)' :
    value >= 45 ? 'var(--orange)' : 'var(--red)'

  useEffect(() => {
    const arc = arcRef.current
    if (!arc) return
    // Start with empty arc then animate
    arc.style.strokeDasharray  = `0 ${arcLen}`
    arc.style.strokeDashoffset = '0'
    const timer = setTimeout(() => {
      arc.style.transition       = 'stroke-dasharray 1.2s cubic-bezier(.4,0,.2,1)'
      arc.style.strokeDasharray  = `${filled} ${gap + CIRCUM - arcLen}`
    }, delay)
    return () => clearTimeout(timer)
  }, [filled, gap, arcLen, delay])

  return (
    <div className="gauge-card">
      <div className="gauge-svg-wrap">
        <svg width={SIZE} height={SIZE} viewBox={`0 0 ${SIZE} ${SIZE}`}>
          {/* Track arc */}
          <circle
            cx={cx} cy={cy} r={R}
            fill="none"
            stroke="var(--bg-hover)"
            strokeWidth={STROKE}
            strokeDasharray={`${arcLen} ${CIRCUM - arcLen}`}
            strokeLinecap="round"
            transform={`rotate(${startAngle} ${cx} ${cy})`}
          />
          {/* Filled arc */}
          <circle
            ref={arcRef}
            cx={cx} cy={cy} r={R}
            fill="none"
            stroke={color}
            strokeWidth={STROKE}
            strokeDasharray={`0 ${arcLen}`}
            strokeLinecap="round"
            transform={`rotate(${startAngle} ${cx} ${cy})`}
            style={{ filter: `drop-shadow(0 0 4px ${color}66)` }}
          />
        </svg>
        <div className="gauge-center-text">
          <span className="gauge-number" style={{ color }}>{value}</span>
          <span className="gauge-denom">/100</span>
        </div>
      </div>

      <div className="gauge-label">{label}</div>

      <span
        className="rating-badge"
        style={{
          background: `${ratingColor}22`,
          color: ratingColor,
          border: `1px solid ${ratingColor}44`,
        }}
      >
        {rating}
      </span>

      {sublabel && <div className="gauge-sub">{sublabel}</div>}
    </div>
  )
}
