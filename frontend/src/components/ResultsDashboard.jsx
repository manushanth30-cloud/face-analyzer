import React from 'react'
import FeatureCard from './FeatureCard'
import ScoreGauge from './ScoreGauge'
import SummaryPanel from './SummaryPanel'

export default function ResultsDashboard({ data, imageUrl, onReset }) {
  const {
    faceStructure, eyes, eyebrows, nose,
    lips, jaw, skin, harmonyScores, confidenceOverall,
  } = data

  // Build image data URL from base64
  const imgSrc = imageUrl ||
    (data.imageBase64
      ? `data:${data.imageMime || 'image/jpeg'};base64,${data.imageBase64}`
      : null)

  const features = [
    {
      title: 'Face Shape',
      badge: faceStructure?.shape,
      score: faceStructure?.symmetryScore,
      scoreLabel: 'Symmetry',
      desc: `${faceStructure?.shape} faces are considered well-balanced and versatile. Facial thirds: ${faceStructure?.facialThirds}.`,
      delay: 0,
    },
    {
      title: 'Eyes',
      badge: eyes?.shape,
      metric: 'Canthal Tilt',
      metricValue: eyes?.canthalTilt,
      desc: `${eyes?.canthalTilt?.startsWith('+') ? 'Positive' : 'Negative'} tilt is generally associated with a ${eyes?.canthalTilt?.startsWith('+') ? 'youthful' : 'mature'} appearance. Spacing: ${eyes?.spacing}.`,
      delay: 50,
    },
    {
      title: 'Eyebrows',
      badge: eyebrows?.shape,
      score: eyebrows?.symmetryScore,
      scoreLabel: 'Symmetry',
      desc: `${eyebrows?.height === 'Ideal' ? 'Ideal brow height' : eyebrows?.height + ' brow height'}. Arch peak at ${eyebrows?.archPeakPosition?.toLowerCase()}.`,
      delay: 100,
    },
    {
      title: 'Nose',
      badge: nose?.widthRatio,
      metric: 'Proportion',
      metricValue: nose?.tipShape,
      desc: `Nasal length is ${nose?.length?.toLowerCase()} and tip is ${nose?.tipShape?.toLowerCase()}. Bridge: ${nose?.bridgeAlignment}.`,
      delay: 150,
    },
    {
      title: 'Lips',
      badge: lips?.cupidsBow !== 'Flat' ? 'Balanced' : 'Flat bow',
      metric: 'Proportion',
      metricValue: lips?.mouthWidthRatio,
      desc: `Lip thickness and symmetry are ${lips?.symmetryScore >= 80 ? 'well balanced' : 'slightly asymmetric'}. Upper/lower ratio: ${lips?.upperLowerRatio}.`,
      delay: 200,
    },
    {
      title: 'Jaw & Chin',
      badge: jaw?.type,
      metric: 'Definition',
      metricValue: jaw?.gonialAngle,
      desc: `Jawline can ${jaw?.type === 'Soft' || jaw?.type === 'Undefined' ? 'be more defined with styling or fitness.' : 'is well-defined and structured.'}`,
      delay: 250,
    },
    {
      title: 'Skin',
      badge: `Fitzpatrick ${skin?.fitzpatrick}`,
      metric: 'Evenness',
      metricValue: skin?.evennessScore >= 75 ? 'High ›' : skin?.evennessScore >= 50 ? 'Medium ›' : 'Low ›',
      desc: `Good overall skin evenness and tone. Undertone: ${skin?.undertone}. Dark circles: ${skin?.darkCircles}.`,
      delay: 300,
    },
    {
      title: 'Facial Symmetry',
      badge: null,
      score: harmonyScores?.overallSymmetry,
      scoreLabel: 'Symmetry Score',
      desc: `Your face is ${harmonyScores?.overallSymmetry >= 80 ? 'well balanced left to right.' : 'slightly asymmetric, which is completely normal.'}`,
      delay: 350,
    },
  ]

  const gauges = [
    {
      value: harmonyScores?.facialHarmonyIndex,
      label: 'Overall Balance',
      sublabel: 'Measures overall facial proportions and balance.',
      color: 'var(--gauge-balance)',
      delay: 200,
    },
    {
      value: harmonyScores?.overallSymmetry,
      label: 'Symmetry Score',
      sublabel: 'Measures left-right facial symmetry.',
      color: 'var(--gauge-symmetry)',
      delay: 350,
    },
    {
      value: harmonyScores?.neoclassicalCompliance,
      label: 'Proportion Score',
      sublabel: 'How close your proportions are to ideal ratios.',
      color: 'var(--gauge-proportion)',
      delay: 500,
    },
    {
      value: harmonyScores?.goldenRatioScore,
      label: 'Feature Harmony',
      sublabel: 'Harmony between different facial features.',
      color: 'var(--gauge-harmony)',
      delay: 650,
    },
  ]

  return (
    <div className="results-page">
      {/* ── Header ───────────────────────────────────── */}
      <header className="results-header">
        <div className="results-header-left">
          <button
            id="back-btn"
            className="btn btn-ghost"
            style={{ padding: '6px 10px' }}
            onClick={onReset}
            title="Analyze another photo"
          >
            ←
          </button>
          <div>
            <div className="results-header-title">Facial Feature Analysis</div>
            <div className="results-header-sub">AI-powered face insights for grooming &amp; style</div>
          </div>
        </div>
        <button
          id="export-btn"
          className="btn btn-outline"
          style={{ fontSize: '0.8rem', gap: 6 }}
          onClick={() => window.print()}
        >
          <span>↑</span> Export Report
        </button>
      </header>

      {/* ── Summary Panel ─────────────────────────────── */}
      <SummaryPanel data={data} imageUrl={imgSrc} />

      <div className="divider" style={{ margin: '0 20px' }} />

      {/* ── Feature Grid ──────────────────────────────── */}
      <div className="features-section section-gap fade-up">
        <div className="features-section-header">
          <div>
            <div className="features-section-title">Detailed Feature Analysis</div>
            <div className="features-section-sub">
              Measures are relative to ideal facial proportions and symmetry.
            </div>
          </div>
          <div className="confidence-badge">
            <span style={{ color: 'var(--green)' }}>✦</span>
            Confidence Overall: {confidenceOverall}%
            <span style={{ cursor: 'help', color: 'var(--text-dim)' }} title="Average confidence across all feature detections">ⓘ</span>
          </div>
        </div>

        <div className="features-grid">
          {features.map(f => (
            <FeatureCard key={f.title} {...f} />
          ))}
        </div>
      </div>

      <div className="divider" style={{ margin: '20px 20px 0' }} />

      {/* ── Overall Scores ────────────────────────────── */}
      <div className="scores-section fade-up">
        <div className="scores-title">Overall Scores</div>
        <div className="scores-sub">Higher score means better balance and harmony.</div>
        <div className="scores-grid">
          {gauges.map(g => (
            <ScoreGauge key={g.label} {...g} />
          ))}
        </div>
      </div>

      {/* ── Analyze Another ───────────────────────────── */}
      <div style={{ display: 'flex', justifyContent: 'center', padding: '28px 20px 0' }}>
        <button
          id="analyze-another-btn"
          className="btn btn-outline"
          onClick={onReset}
        >
          ↺ Analyze Another Photo
        </button>
      </div>

      {/* ── Disclaimer ────────────────────────────────── */}
      <div className="disclaimer">
        <span style={{ flexShrink: 0 }}>🛡</span>
        <span>
          Disclaimer: This report is for grooming and style guidance only, not medical or identity assessment.
          Results are approximations based on AI landmark detection and may vary with lighting and photo quality.
        </span>
      </div>
    </div>
  )
}
