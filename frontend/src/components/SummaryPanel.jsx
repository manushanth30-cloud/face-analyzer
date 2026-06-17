import React, { useState } from 'react'
import LandmarkOverlay from './LandmarkOverlay'

export default function SummaryPanel({ data, imageUrl }) {
  const [showLandmarks, setShowLandmarks] = useState(true)

  const { faceStructure, skin, insights, confidenceOverall,
          landmarks, imageDimensions } = data

  const skinColors = {
    'I': '#F5E8D8', 'II': '#E8C9A0', 'III': '#C68642',
    'IV': '#8D5524', 'V': '#5C3317', 'VI': '#3B1F0A',
  }
  const skinColor = skinColors[skin?.fitzpatrick] || '#C68642'

  return (
    <div className="summary-section">
      {/* Left: Photo + Landmark toggle */}
      <div className="photo-panel">
        <div className="photo-wrap">
          <img src={imageUrl} alt="Your face" />
          <LandmarkOverlay
            landmarks={landmarks}
            imgW={imageDimensions?.width}
            imgH={imageDimensions?.height}
            visible={showLandmarks}
          />
        </div>
        <button
          id="toggle-landmarks-btn"
          className="btn btn-ghost"
          style={{ width: '100%', justifyContent: 'center', fontSize: '0.8rem' }}
          onClick={() => setShowLandmarks(v => !v)}
        >
          <span>{showLandmarks ? '✦' : '○'}</span>
          {showLandmarks ? 'Hide Landmarks' : 'View Landmarks'}
        </button>
      </div>

      {/* Right: Summary Card */}
      <div className="summary-card">
        {/* Header */}
        <div className="summary-header-label">
          <span>✦</span>
          Your Summary
        </div>

        {/* Face Shape + Skin Tone */}
        <div className="summary-top-row">
          <div className="summary-stat">
            <div className="summary-stat-icon" style={{ borderColor: 'var(--green)' }}>
              <span style={{ fontSize: '1.1rem', color: 'var(--green)' }}>◯</span>
            </div>
            <div className="summary-stat-text">
              <div className="summary-stat-label">Face Shape</div>
              <div className="summary-stat-value">{faceStructure?.shape}</div>
              <div className="summary-stat-conf">
                Confidence: {faceStructure?.confidence}%
              </div>
            </div>
          </div>

          <div className="summary-stat">
            <div
              className="summary-stat-icon"
              style={{
                backgroundColor: skinColor,
                borderColor: skinColor,
                boxShadow: `0 0 0 3px ${skinColor}44`,
              }}
            />
            <div className="summary-stat-text">
              <div className="summary-stat-label">Skin Tone</div>
              <div className="summary-stat-value">Fitzpatrick {skin?.fitzpatrick}</div>
              <div className="summary-stat-conf">
                Confidence: {skin?.confidence}%
              </div>
            </div>
          </div>
        </div>

        <div className="divider" style={{ margin: '4px 0' }} />

        {/* Key Strengths + Areas to Improve */}
        <div className="strengths-grid">
          <div className="strengths-col col-strengths">
            <h4>Key Strengths</h4>
            <ul className="strengths-list">
              {(insights?.keyStrengths || []).map((s, i) => (
                <li key={i}>
                  <span className="icon-check">✓</span>
                  {s}
                </li>
              ))}
            </ul>
          </div>
          <div className="strengths-col col-areas">
            <h4>Areas to Improve</h4>
            <ul className="strengths-list">
              {(insights?.areasToImprove || []).map((a, i) => (
                <li key={i}>
                  <span className="icon-warn">⚠</span>
                  {a}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="divider" style={{ margin: '4px 0' }} />

        {/* Overall Insight */}
        <div className="insight-box">
          <div className="insight-label">
            <span>✦</span>
            Overall Insight
          </div>
          <p className="insight-text">{insights?.overallInsight}</p>
        </div>
      </div>
    </div>
  )
}
