import React, { useState, useEffect } from 'react'

const CATEGORY_EMOJIS = {
  'Hollywood':    '🎬',
  'Bollywood':    '🎭',
  'K-Pop':        '🎤',
  'K-Drama':      '📺',
  'Music':        '🎵',
  'Cricket':      '🏏',
  'Football':     '⚽',
  'Sports':       '🏆',
  'Model':        '💎',
  'TV':           '📺',
  'Historical':   '⭐',
  'Tech':         '💻',
  'South Indian': '🎬',
}

function getCategoryEmoji(category) {
  for (const [key, emoji] of Object.entries(CATEGORY_EMOJIS)) {
    if (category?.toLowerCase().includes(key.toLowerCase())) return emoji
  }
  return '⭐'
}

function getMatchColor(percent) {
  if (percent >= 85) return 'var(--green)'
  if (percent >= 70) return 'var(--blue)'
  if (percent >= 55) return 'var(--purple)'
  return 'var(--orange)'
}

function getMatchLabel(percent) {
  if (percent >= 90) return 'Stunning Match'
  if (percent >= 80) return 'Strong Match'
  if (percent >= 70) return 'Good Match'
  if (percent >= 60) return 'Similar'
  return 'Partial Match'
}

export default function CelebrityMatch({ matches }) {
  const [revealedCount, setRevealedCount] = useState(0)

  useEffect(() => {
    if (!matches?.length) return
    setRevealedCount(0)
    const timers = matches.map((_, i) =>
      setTimeout(() => setRevealedCount(c => c + 1), 300 + i * 400)
    )
    return () => timers.forEach(clearTimeout)
  }, [matches])

  if (!matches?.length) return null

  const topMatch = matches[0]
  const runners  = matches.slice(1)

  return (
    <div className="celeb-section fade-up">
      {/* Section header */}
      <div className="celeb-section-header">
        <div>
          <div className="celeb-section-title">🌟 Celebrity Lookalike</div>
          <div className="celeb-section-sub">
            Matched from 1,000+ celebrities based on your facial proportions
          </div>
        </div>
      </div>

      {/* Top match — hero card */}
      <div
        className={`celeb-hero ${revealedCount >= 1 ? 'revealed' : ''}`}
        style={{ '--match-color': getMatchColor(topMatch.matchPercent) }}
      >
        <div className="celeb-hero-glow" />
        <div className="celeb-hero-content">
          <div className="celeb-hero-top">
            <div className="celeb-hero-badge">
              <span>#1 Match</span>
            </div>
            <div className="celeb-hero-percent" style={{ color: getMatchColor(topMatch.matchPercent) }}>
              {topMatch.matchPercent}%
            </div>
          </div>

          <div className="celeb-hero-name">{topMatch.name}</div>
          <div className="celeb-hero-meta">
            <span>{getCategoryEmoji(topMatch.category)} {topMatch.category}</span>
            <span className="celeb-dot">·</span>
            <span>{topMatch.faceShape} face</span>
          </div>

          <div className="celeb-hero-label" style={{ color: getMatchColor(topMatch.matchPercent) }}>
            {getMatchLabel(topMatch.matchPercent)}
          </div>

          {/* Why you match */}
          <div className="celeb-similarities">
            {(topMatch.similarities || []).map((s, i) => (
              <span key={i} className="celeb-sim-tag">✓ {s}</span>
            ))}
          </div>

          {topMatch.funFact && (
            <div className="celeb-fun-fact">
              <span>💡</span> {topMatch.funFact}
            </div>
          )}
        </div>
      </div>

      {/* Runner-up matches */}
      {runners.length > 0 && (
        <div className="celeb-runners-grid">
          {runners.map((m, i) => (
            <div
              key={m.name}
              className={`celeb-runner-card ${revealedCount >= i + 2 ? 'revealed' : ''}`}
              style={{ '--match-color': getMatchColor(m.matchPercent) }}
            >
              <div className="celeb-runner-rank">#{i + 2}</div>
              <div className="celeb-runner-info">
                <div className="celeb-runner-name">{m.name}</div>
                <div className="celeb-runner-meta">
                  {getCategoryEmoji(m.category)} {m.category} · {m.faceShape}
                </div>
                {m.similarities?.length > 0 && (
                  <div className="celeb-runner-sims">
                    {m.similarities.slice(0, 2).map((s, j) => (
                      <span key={j} className="celeb-sim-tag-sm">✓ {s}</span>
                    ))}
                  </div>
                )}
              </div>
              <div className="celeb-runner-percent" style={{ color: getMatchColor(m.matchPercent) }}>
                {m.matchPercent}%
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
