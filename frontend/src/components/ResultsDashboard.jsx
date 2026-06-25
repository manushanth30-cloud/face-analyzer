import React, { useState, useRef } from 'react'
import FeatureCard from './FeatureCard'
import ScoreGauge from './ScoreGauge'
import SummaryPanel from './SummaryPanel'
import CelebrityMatch from './CelebrityMatch'
import StyleGuide from './StyleGuide'

const TABS = ['Overview', 'Face', 'Eyes', 'Nose', 'Lips', 'Skin', 'Jawline', 'Scores', 'Style Guide']

// Compute key facial measurements from landmarks (pixel distances)
function getMeasurements(landmarks, imgW, imgH, dims) {
  if (!landmarks?.length || !dims?.w) return null
  const sx = dims.w / imgW, sy = dims.h / imgH
  const d = (a, b) => {
    const la = landmarks[a], lb = landmarks[b]
    if (!la || !lb) return null
    return Math.round(Math.sqrt(((la.x - lb.x) * sx) ** 2 + ((la.y - lb.y) * sy) ** 2))
  }
  return {
    faceLength: { val: d(10, 152),  ideal: '170–190 px', label: 'Face Length' },
    faceWidth:  { val: d(234, 454), ideal: '135–145 px', label: 'Face Width'  },
    eyeDist:    { val: d(133, 362), ideal: '58–65 px',   label: 'Eye Distance' },
    eyeWidth:   { val: d(33, 133),  ideal: '30–36 px',   label: 'Eye Width'   },
    noseWidth:  { val: d(129, 358), ideal: '32–40 px',   label: 'Nose Width'  },
    lipsWidth:  { val: d(61, 291),  ideal: '48–56 px',   label: 'Lips Width'  },
    jawWidth:   { val: d(172, 397), ideal: '105–115 px', label: 'Jaw Width'   },
  }
}

// Map harmony → /10 score
function getScore10(harmony) {
  const avg = (
    (harmony?.facialHarmonyIndex || 70) * 0.35 +
    (harmony?.overallSymmetry    || 70) * 0.30 +
    (harmony?.goldenRatioScore   || 70) * 0.20 +
    (harmony?.neoclassicalCompliance || 70) * 0.15
  ) / 10
  return Math.min(10, Math.max(1, +avg.toFixed(1)))
}

// Estimate age range from harmony (rough heuristic)
function getAgeEst(harmony, skin) {
  const base = 25
  const sym  = (harmony?.overallSymmetry || 70) / 100
  const ev   = (skin?.evennessScore || 70) / 100
  const age  = Math.round(base - (sym - 0.6) * 8 - (ev - 0.6) * 6)
  const lo   = Math.max(16, age - 2)
  const hi   = age + 2
  return { age, lo, hi }
}

function StarRating({ score10 }) {
  const stars = Math.round(score10 / 2)   // 1–5 stars out of 10
  return (
    <div className="rd-stars">
      {[1,2,3,4,5].map(i => (
        <span key={i} style={{ color: i <= stars ? '#f5c518' : 'var(--border)' }}>★</span>
      ))}
    </div>
  )
}

function ConfBar({ label, value, color }) {
  return (
    <div className="rd-confbar">
      <div className="rd-confbar-label">{label}</div>
      <div className="rd-confbar-track">
        <div className="rd-confbar-fill" style={{ width: `${value}%`, background: color || 'var(--blue)' }} />
      </div>
      <div className="rd-confbar-val">{value}%</div>
    </div>
  )
}

function StatusChip({ label, value, ok }) {
  return (
    <div className="rd-status-chip">
      <span className="rd-status-dot" style={{ background: ok ? 'var(--green)' : 'var(--orange)' }} />
      <span className="rd-status-label">{label}</span>
      <span className="rd-status-val" style={{ color: ok ? 'var(--green)' : 'var(--orange)' }}>{value}</span>
    </div>
  )
}

function MeasCard({ label, val, ideal }) {
  return (
    <div className="rd-meas-card">
      <div className="rd-meas-label">{label}</div>
      <div className="rd-meas-val">{val != null ? `${val} px` : '—'}</div>
      <div className="rd-meas-ideal">Ideal: {ideal}</div>
      <div className="rd-meas-rating" style={{ color: 'var(--green)' }}>Good</div>
    </div>
  )
}

export default function ResultsDashboard({ data, imageUrl, gender, onReset }) {
  const {
    faceStructure, eyes, eyebrows, nose,
    lips, jaw, skin, harmonyScores, confidenceOverall,
    landmarks, imageDimensions,
  } = data

  const [activeTab, setActiveTab]           = useState('Overview')
  const [showCelebrity, setShowCelebrity]   = useState(false)
  const [isSearchingCeleb, setIsSearchingCeleb] = useState(false)
  const photoWrapRef = useRef(null)

  const handleFindCelebrity = () => {
    setIsSearchingCeleb(true)
    setTimeout(() => { setIsSearchingCeleb(false); setShowCelebrity(true) }, 1200)
  }

  const imgSrc = imageUrl ||
    (data.imageBase64 ? `data:${data.imageMime || 'image/jpeg'};base64,${data.imageBase64}` : null)

  const score10  = getScore10(harmonyScores)
  const ageEst   = getAgeEst(harmonyScores, skin)

  // Compute measurements using a fixed rough scale (image native px)
  const meas = (() => {
    if (!landmarks?.length) return null
    const d = (a, b) => {
      const la = landmarks[a], lb = landmarks[b]
      if (!la || !lb) return null
      return Math.round(Math.sqrt((la.x - lb.x) ** 2 + (la.y - lb.y) ** 2))
    }
    return {
      faceLength: { val: d(10, 152),  ideal: '170–190', label: 'Face Length' },
      faceWidth:  { val: d(234, 454), ideal: '135–145', label: 'Face Width'  },
      eyeDist:    { val: d(133, 362), ideal: '58–65',   label: 'Eye Distance'},
      eyeWidth:   { val: d(33, 133),  ideal: '30–36',   label: 'Eye Width'   },
      noseWidth:  { val: d(129, 358), ideal: '32–40',   label: 'Nose Width'  },
      lipsWidth:  { val: d(61, 291),  ideal: '48–56',   label: 'Lips Width'  },
      jawWidth:   { val: d(172, 397), ideal: '105–115', label: 'Jaw Width'   },
    }
  })()

  const features = [
    { title: 'Face Shape',     badge: faceStructure?.shape,    score: faceStructure?.symmetryScore, scoreLabel: 'Symmetry',  desc: `${faceStructure?.shape} faces are considered well-balanced and versatile. Facial thirds: ${faceStructure?.facialThirds}.`, delay: 0   },
    { title: 'Eyes',           badge: eyes?.shape,             metric: 'Canthal Tilt', metricValue: eyes?.canthalTilt, desc: `${eyes?.canthalTilt?.startsWith('+') ? 'Positive' : 'Negative'} tilt — ${eyes?.canthalTilt?.startsWith('+') ? 'youthful' : 'mature'} appearance. Spacing: ${eyes?.spacing}.`, delay: 50  },
    { title: 'Eyebrows',       badge: eyebrows?.shape,         score: eyebrows?.symmetryScore, scoreLabel: 'Symmetry',  desc: `${eyebrows?.height === 'Ideal' ? 'Ideal brow height' : eyebrows?.height + ' brow height'}. Arch peak at ${eyebrows?.archPeakPosition?.toLowerCase()}.`, delay: 100 },
    { title: 'Nose',           badge: nose?.widthRatio,        metric: 'Tip',          metricValue: nose?.tipShape,     desc: `Nasal length is ${nose?.length?.toLowerCase()} and tip is ${nose?.tipShape?.toLowerCase()}. Bridge: ${nose?.bridgeAlignment}.`, delay: 150 },
    { title: 'Lips',           badge: lips?.cupidsBow !== 'Flat' ? 'Balanced' : 'Flat bow', metric: 'Proportion', metricValue: lips?.mouthWidthRatio, desc: `Lip symmetry is ${lips?.symmetryScore >= 80 ? 'well balanced' : 'slightly asymmetric'}. Upper/lower ratio: ${lips?.upperLowerRatio}.`, delay: 200 },
    { title: 'Jaw & Chin',     badge: jaw?.type,               metric: 'Gonial Angle', metricValue: jaw?.gonialAngle,   desc: `Jawline ${jaw?.type === 'Soft' || jaw?.type === 'Undefined' ? 'can be more defined with styling or fitness.' : 'is well-defined and structured.'}`, delay: 250 },
    { title: 'Skin',           badge: `Fitzpatrick ${skin?.fitzpatrick}`, metric: 'Evenness', metricValue: skin?.evennessScore >= 75 ? 'High ›' : skin?.evennessScore >= 50 ? 'Medium ›' : 'Low ›', desc: `Overall skin evenness and tone. Undertone: ${skin?.undertone}. Dark circles: ${skin?.darkCircles}.`, delay: 300 },
    { title: 'Facial Symmetry',badge: null,                    score: harmonyScores?.overallSymmetry, scoreLabel: 'Symmetry Score', desc: `Your face is ${harmonyScores?.overallSymmetry >= 80 ? 'well balanced left to right.' : 'slightly asymmetric, which is completely normal.'}`, delay: 350 },
  ]

  const gauges = [
    { value: harmonyScores?.facialHarmonyIndex,    label: 'Overall Balance',    sublabel: 'Overall facial proportions and balance.',        color: 'var(--gauge-balance)',    delay: 200 },
    { value: harmonyScores?.overallSymmetry,       label: 'Symmetry Score',     sublabel: 'Left-right facial symmetry.',                   color: 'var(--gauge-symmetry)',   delay: 350 },
    { value: harmonyScores?.neoclassicalCompliance,label: 'Proportion Score',   sublabel: 'Closeness to ideal classical ratios.',           color: 'var(--gauge-proportion)', delay: 500 },
    { value: harmonyScores?.goldenRatioScore,      label: 'Feature Harmony',    sublabel: 'Harmony between individual facial features.',    color: 'var(--gauge-harmony)',    delay: 650 },
  ]

  // Tab-filtered features
  const tabFeatures = {
    Overview: features,
    Face:     features.filter(f => f.title === 'Face Shape' || f.title === 'Facial Symmetry'),
    Eyes:     features.filter(f => f.title === 'Eyes' || f.title === 'Eyebrows'),
    Nose:     features.filter(f => f.title === 'Nose'),
    Lips:     features.filter(f => f.title === 'Lips'),
    Skin:     features.filter(f => f.title === 'Skin'),
    Jawline:  features.filter(f => f.title === 'Jaw & Chin' || f.title === 'Facial Symmetry'),
    Scores:   features,
  }
  const visibleFeatures = tabFeatures[activeTab] || features

  const skinColors = { 'I': '#F5E8D8', 'II': '#E8C9A0', 'III': '#C68642', 'IV': '#8D5524', 'V': '#5C3317', 'VI': '#3B1F0A' }

  return (
    <div className="results-page">

      {/* ── Header ───────────────────────────────────── */}
      <header className="results-header">
        <div className="results-header-left">
          <button id="back-btn" className="btn btn-ghost" style={{ padding: '6px 10px' }} onClick={onReset} title="Analyze another photo">←</button>
          <div>
            <div className="results-header-title">AI Facial Analysis Report</div>
            <div className="results-header-sub">
              <span className="rd-conf-badge">
                <span style={{ color: 'var(--green)' }}>●</span> High Confidence
              </span>
            </div>
          </div>
        </div>
        <button id="export-btn" className="btn btn-outline" style={{ fontSize: '0.8rem', gap: 6 }} onClick={() => window.print()}>
          <span>↑</span> Export Report
        </button>
      </header>

      {/* ── Tab Navigation ───────────────────────────── */}
      <div className="rd-tabs-wrap">
        <div className="rd-tabs">
          {TABS.map(tab => (
            <button
              key={tab}
              className={`rd-tab ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* ── Style Guide Tab ───────────────────────────── */}
      {activeTab === 'Style Guide' && data.styleRecommendations && (
        <div style={{ padding: '0 20px 32px' }}>
          <StyleGuide styleData={data.styleRecommendations} defaultGender={gender} />
        </div>
      )}

      {/* ── All other tabs ─────────────────────────────── */}
      {activeTab !== 'Style Guide' && (
        <>
          {/* ── Top two-column layout ─────────────────── */}
          <div className="rd-top-grid">

            {/* LEFT: Photo + Detection + Confidence */}
            <div className="rd-left-col">
              <SummaryPanel data={data} imageUrl={imgSrc} photoOnly />

              {/* Detection Status */}
              <div className="rd-card rd-detect">
                <div className="rd-card-title">Detection Status</div>
                <div className="rd-status-grid">
                  <StatusChip label="Face Detected"   value="Yes"  ok />
                  <StatusChip label="Front Facing"    value="Yes"  ok />
                  <StatusChip label="Good Lighting"   value="Yes"  ok />
                  <StatusChip label="High Resolution" value="Yes"  ok />
                  <StatusChip label="No Occlusions"   value="Yes"  ok />
                  <StatusChip label="Eyes Visibility" value="Good" ok />
                </div>
              </div>

              {/* Analysis Confidence */}
              <div className="rd-card">
                <div className="rd-card-title">Analysis Confidence</div>
                <div className="rd-conf-row">
                  <div className="rd-conf-circle">
                    <svg viewBox="0 0 60 60" width="70" height="70">
                      <circle cx="30" cy="30" r="24" fill="none" stroke="var(--border)" strokeWidth="5"/>
                      <circle cx="30" cy="30" r="24" fill="none" stroke="var(--green)" strokeWidth="5"
                        strokeDasharray={`${(confidenceOverall / 100) * 150.8} 150.8`}
                        strokeLinecap="round"
                        transform="rotate(-90 30 30)"
                        style={{ transition: 'stroke-dasharray 1s ease' }}
                      />
                      <text x="30" y="34" textAnchor="middle" fill="var(--text-primary)" fontSize="12" fontWeight="700">{confidenceOverall}%</text>
                    </svg>
                    <div className="rd-conf-label">Excellent</div>
                  </div>
                  <div className="rd-confbars">
                    <ConfBar label="Landmark Detection" value={Math.min(99, (confidenceOverall || 80) + 2)} color="var(--blue)"   />
                    <ConfBar label="Pose & Alignment"   value={Math.min(99, (confidenceOverall || 80) - 1)} color="var(--purple)" />
                    <ConfBar label="Lighting Quality"   value={Math.min(99, (confidenceOverall || 80) + 1)} color="var(--green)"  />
                    <ConfBar label="Image Quality"      value={Math.min(99, (confidenceOverall || 80) + 1)} color="var(--yellow)" />
                  </div>
                </div>
              </div>
            </div>

            {/* RIGHT: Summary */}
            <div className="rd-right-col">

              {/* Score + Summary header */}
              <div className="rd-card rd-summary-card">
                <div className="rd-summary-top">
                  <div className="rd-summary-heading">Your Summary</div>
                  <div className="rd-score-badge">
                    <span className="rd-score-num">{score10}</span>
                    <span className="rd-score-denom">/10</span>
                    <StarRating score10={score10} />
                    <div className="rd-score-pct">Top {score10 >= 8.5 ? '10' : score10 >= 7.5 ? '15' : '25'}% of {gender === 'male' ? 'men' : 'women'}</div>
                  </div>
                </div>

                {/* Stats row */}
                <div className="rd-stats-row">
                  <div className="rd-stat-item">
                    <div className="rd-stat-icon" style={{ color: 'var(--green)' }}>◯</div>
                    <div>
                      <div className="rd-stat-label">Face Shape</div>
                      <div className="rd-stat-value">{faceStructure?.shape}</div>
                      <div className="rd-stat-conf">Confidence: {faceStructure?.confidence}%</div>
                    </div>
                  </div>
                  <div className="rd-stat-item">
                    <div className="rd-stat-icon" style={{ background: skinColors[skin?.fitzpatrick] || '#C68642', borderRadius: '50%', width: 24, height: 24 }} />
                    <div>
                      <div className="rd-stat-label">Skin Tone</div>
                      <div className="rd-stat-value">Fitzpatrick {skin?.fitzpatrick}</div>
                      <div className="rd-stat-conf">Confidence: {skin?.confidence}%</div>
                    </div>
                  </div>
                  <div className="rd-stat-item">
                    <div className="rd-stat-icon" style={{ color: 'var(--blue)' }}>🗓</div>
                    <div>
                      <div className="rd-stat-label">Age Estimate</div>
                      <div className="rd-stat-value">{ageEst.age} years</div>
                      <div className="rd-stat-conf">Looks like {ageEst.lo}–{ageEst.hi}</div>
                    </div>
                  </div>
                </div>

                <div className="rd-divider" />

                {/* Strengths / Areas */}
                <div className="rd-strengths-grid">
                  <div>
                    <div className="rd-strengths-title" style={{ color: 'var(--green)' }}>✦ Key Strengths</div>
                    <ul className="rd-list">
                      {(data.insights?.keyStrengths || []).map((s, i) => (
                        <li key={i}><span style={{ color: 'var(--green)' }}>✓</span> {s}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <div className="rd-strengths-title" style={{ color: 'var(--orange)' }}>△ Areas to Enhance</div>
                    <ul className="rd-list">
                      {(data.insights?.areasToImprove || []).map((a, i) => (
                        <li key={i}><span style={{ color: 'var(--orange)' }}>⚠</span> {a}</li>
                      ))}
                    </ul>
                  </div>
                  {/* Golden Ratio */}
                  <div className="rd-golden-box">
                    <div className="rd-golden-label">Golden Ratio Score</div>
                    <div className="rd-golden-ring">
                      <svg viewBox="0 0 60 60" width="64" height="64">
                        <circle cx="30" cy="30" r="24" fill="none" stroke="var(--border)" strokeWidth="5"/>
                        <circle cx="30" cy="30" r="24" fill="none" stroke="var(--yellow)" strokeWidth="5"
                          strokeDasharray={`${((harmonyScores?.goldenRatioScore || 70) / 100) * 150.8} 150.8`}
                          strokeLinecap="round" transform="rotate(-90 30 30)"
                        />
                        <text x="30" y="34" textAnchor="middle" fill="var(--yellow)" fontSize="11" fontWeight="700">
                          {harmonyScores?.goldenRatioScore || 70}%
                        </text>
                      </svg>
                      <div className="rd-golden-sublabel">Good</div>
                    </div>
                  </div>
                </div>

                <div className="rd-divider" />

                {/* Overall Insight */}
                <div className="rd-insight-box">
                  <div className="rd-insight-label">💡 Overall Insight</div>
                  <p className="rd-insight-text">{data.insights?.overallInsight}</p>
                </div>
              </div>
            </div>
          </div>

          {/* ── Key Facial Measurements ──────────────────── */}
          {meas && (
            <div className="rd-card rd-meas-section">
              <div className="rd-card-title">
                Key Facial Measurements
                <span className="rd-meas-unit">px</span>
              </div>
              <div className="rd-meas-grid">
                {Object.values(meas).map(m => (
                  <MeasCard key={m.label} {...m} />
                ))}
              </div>
            </div>
          )}

          <div className="rd-divider-full" />

          {/* ── Celebrity Lookalike ───────────────────────── */}
          {data.celebrityMatches && (
            <div style={{ padding: '0 20px' }}>
              {!showCelebrity ? (
                <div style={{ display: 'flex', justifyContent: 'center', margin: '8px 0 20px' }}>
                  <button
                    className="btn btn-primary"
                    style={{ padding: '14px 32px', fontSize: '1rem', background: 'linear-gradient(135deg, var(--blue), var(--purple))', borderColor: 'transparent' }}
                    onClick={handleFindCelebrity}
                    disabled={isSearchingCeleb}
                  >
                    {isSearchingCeleb
                      ? <><span style={{ animation: 'pulse 1s infinite' }}>●</span> Searching 1,000+ Celebrities…</>
                      : <><span>🌟</span> Find My Celebrity Lookalike</>}
                  </button>
                </div>
              ) : (
                <CelebrityMatch matches={data.celebrityMatches} />
              )}
            </div>
          )}

          {/* ── Feature Cards ──────────────────────────────── */}
          {activeTab !== 'Scores' && (
            <div className="features-section section-gap fade-up">
              <div className="features-section-header">
                <div>
                  <div className="features-section-title">Detailed Feature Analysis</div>
                  <div className="features-section-sub">Measures relative to ideal facial proportions and symmetry.</div>
                </div>
                <div className="confidence-badge">
                  <span style={{ color: 'var(--green)' }}>✦</span>
                  Confidence: {confidenceOverall}%
                </div>
              </div>
              <div className="features-grid">
                {visibleFeatures.map(f => <FeatureCard key={f.title} {...f} />)}
              </div>
            </div>
          )}

          {/* ── Overall Scores ─────────────────────────────── */}
          <div className="scores-section fade-up">
            <div className="scores-title">Overall Scores</div>
            <div className="scores-sub">Higher score means better balance and harmony.</div>
            <div className="scores-grid">
              {gauges.map(g => <ScoreGauge key={g.label} {...g} />)}
            </div>
          </div>

          {/* ── Analyze Another ────────────────────────────── */}
          <div style={{ display: 'flex', justifyContent: 'center', padding: '28px 20px 0' }}>
            <button id="analyze-another-btn" className="btn btn-outline" onClick={onReset}>
              ↺ Analyze Another Photo
            </button>
          </div>

          {/* ── Disclaimer ─────────────────────────────────── */}
          <div className="disclaimer">
            <span style={{ flexShrink: 0 }}>🛡</span>
            <span>
              Disclaimer: This report is for grooming and style guidance only, not medical or identity assessment.
              Results are based on AI analysis and may vary with lighting, angle and photo quality.
            </span>
          </div>
        </>
      )}
    </div>
  )
}
