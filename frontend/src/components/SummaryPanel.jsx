import React, { useState, useRef } from 'react'
import LandmarkOverlay from './LandmarkOverlay'

// Photo view modes
const MODES = ['Original', 'Landmarks', 'Measurements', 'Heatmap']

// Heatmap overlay — blobs on key facial zones
function HeatmapOverlay({ landmarks, imgW, imgH, containerRef }) {
  const [dims, setDims] = useState({ w: 0, h: 0 })
  React.useEffect(() => {
    if (!containerRef?.current) return
    const measure = () => {
      const img = containerRef.current?.querySelector('img')
      if (img) setDims({ w: img.clientWidth, h: img.clientHeight })
    }
    const img = containerRef.current?.querySelector('img')
    if (img) { if (img.complete) measure(); else img.addEventListener('load', measure) }
    const t = setTimeout(measure, 80)
    window.addEventListener('resize', measure)
    return () => { clearTimeout(t); window.removeEventListener('resize', measure) }
  }, [containerRef])

  if (!landmarks?.length || !imgW || !dims.w) return null
  const sx = dims.w / imgW, sy = dims.h / imgH
  const mx = i => landmarks[i]?.x * sx
  const my = i => landmarks[i]?.y * sy

  // Key zone centers and radii
  const blobs = [
    { cx: mx(168), cy: my(168), r: dims.w * 0.08, color: '#ff5500' },  // nose
    { cx: mx(159), cy: my(159), r: dims.w * 0.07, color: '#ff8800' },  // L eye
    { cx: mx(386), cy: my(386), r: dims.w * 0.07, color: '#ff8800' },  // R eye
    { cx: mx(0),   cy: my(0),   r: dims.w * 0.07, color: '#ff4400' },  // lips
    { cx: mx(152), cy: my(152), r: dims.w * 0.09, color: '#ee3300' },  // chin
    { cx: mx(234), cy: my(234), r: dims.w * 0.10, color: '#dd6600' },  // L cheek
    { cx: mx(454), cy: my(454), r: dims.w * 0.10, color: '#dd6600' },  // R cheek
    { cx: mx(10),  cy: my(10),  r: dims.w * 0.10, color: '#cc4400' },  // forehead
    { cx: mx(66),  cy: my(66),  r: dims.w * 0.06, color: '#ff9900' },  // L brow
    { cx: mx(296), cy: my(296), r: dims.w * 0.06, color: '#ff9900' },  // R brow
  ]

  return (
    <svg width={dims.w} height={dims.h} style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none' }}>
      <defs>
        {blobs.map((b, i) => (
          <radialGradient key={i} id={`hg${i}`}>
            <stop offset="0%"   stopColor={b.color} stopOpacity="0.55" />
            <stop offset="100%" stopColor={b.color} stopOpacity="0"    />
          </radialGradient>
        ))}
      </defs>
      {blobs.map((b, i) => b.cx && b.cy ? (
        <ellipse key={i} cx={b.cx} cy={b.cy} rx={b.r} ry={b.r * 0.85}
          fill={`url(#hg${i})`} />
      ) : null)}
      {/* Cool blue tint for low-activity zones */}
      <rect x={0} y={0} width={dims.w} height={dims.h}
        fill="rgba(0,50,180,0.06)" />
    </svg>
  )
}

// Measurement lines overlay
function MeasurementOverlay({ landmarks, imgW, imgH, containerRef }) {
  const [dims, setDims] = useState({ w: 0, h: 0 })
  React.useEffect(() => {
    if (!containerRef?.current) return
    const measure = () => {
      const img = containerRef.current?.querySelector('img')
      if (img) setDims({ w: img.clientWidth, h: img.clientHeight })
    }
    const img = containerRef.current?.querySelector('img')
    if (img) { if (img.complete) measure(); else img.addEventListener('load', measure) }
    const t = setTimeout(measure, 80)
    window.addEventListener('resize', measure)
    return () => { clearTimeout(t); window.removeEventListener('resize', measure) }
  }, [containerRef])

  if (!landmarks?.length || !imgW || !dims.w) return null
  const sx = dims.w / imgW, sy = dims.h / imgH
  const mx = i => landmarks[i]?.x * sx
  const my = i => landmarks[i]?.y * sy
  const fs = Math.max(8, Math.min(10, dims.w / 40))

  const lines = [
    { x1: mx(10),  y1: my(10),  x2: mx(10),  y2: my(152), label: 'Face Length', color: '#58A6FF', lx: mx(10) - 4, ly: (my(10) + my(152)) / 2 },
    { x1: mx(234), y1: my(234), x2: mx(454), y2: my(234), label: 'Face Width',  color: '#3FB950', lx: (mx(234) + mx(454)) / 2, ly: my(234) - 8 },
    { x1: mx(133), y1: my(133), x2: mx(362), y2: my(362), label: 'Eye Dist',    color: '#00e6c8', lx: (mx(133) + mx(362)) / 2, ly: my(133) - 8 },
    { x1: mx(61),  y1: my(61),  x2: mx(291), y2: my(291), label: 'Lips',        color: '#ff64a0', lx: (mx(61) + mx(291)) / 2,  ly: my(61) + 14 },
    { x1: mx(129), y1: my(129), x2: mx(358), y2: my(358), label: 'Nose W',      color: '#b464ff', lx: (mx(129) + mx(358)) / 2, ly: my(129) - 8 },
    { x1: mx(172), y1: my(172), x2: mx(397), y2: my(397), label: 'Jaw W',       color: '#F78166', lx: (mx(172) + mx(397)) / 2, ly: my(172) + 14 },
  ]

  return (
    <svg width={dims.w} height={dims.h} style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none' }}>
      {/* Dark tint */}
      <rect x={0} y={0} width={dims.w} height={dims.h} fill="rgba(0,0,0,0.35)" />
      {lines.map((l, i) => !l.x1 || !l.y1 ? null : (
        <g key={i}>
          {/* Line */}
          <line x1={l.x1} y1={l.y1} x2={l.x2} y2={l.y2}
            stroke={l.color} strokeWidth={1.5} strokeDasharray="4 3" />
          {/* End caps */}
          <circle cx={l.x1} cy={l.y1} r={3} fill={l.color} />
          <circle cx={l.x2} cy={l.y2} r={3} fill={l.color} />
          {/* Label */}
          <rect x={l.lx - 22} y={l.ly - 9} width={44} height={13} rx={4}
            fill="rgba(10,12,20,0.8)" stroke={l.color} strokeWidth={0.5} />
          <text x={l.lx} y={l.ly} textAnchor="middle" dominantBaseline="middle"
            fill={l.color} fontSize={fs} fontFamily="Inter,sans-serif" fontWeight="700">
            {l.label}
          </text>
        </g>
      ))}
    </svg>
  )
}

export default function SummaryPanel({ data, imageUrl, photoOnly }) {
  const [viewMode, setViewMode] = useState('Landmarks')
  const photoWrapRef = useRef(null)

  const { landmarks, imageDimensions } = data

  const imgSrc = data.imageBase64
    ? `data:${data.imageMime || 'image/jpeg'};base64,${data.imageBase64}`
    : imageUrl

  const lmCount = landmarks?.length || 0

  return (
    <div className="sp-photo-block">
      {/* Landmark count badge */}
      <div className="sp-lm-badge">
        <span style={{ color: 'var(--green)' }}>●</span>
        {lmCount} / {lmCount} Landmarks
        <span className="sp-lm-check">✓</span>
      </div>

      {/* Photo */}
      <div className="photo-wrap" ref={photoWrapRef} style={{ position: 'relative' }}>
        <img src={imgSrc} alt="Your face" />

        {/* Overlays by mode */}
        {viewMode === 'Landmarks' && (
          <LandmarkOverlay
            landmarks={landmarks}
            imgW={imageDimensions?.width}
            imgH={imageDimensions?.height}
            visible={true}
            containerRef={photoWrapRef}
          />
        )}
        {viewMode === 'Heatmap' && (
          <HeatmapOverlay
            landmarks={landmarks}
            imgW={imageDimensions?.width}
            imgH={imageDimensions?.height}
            containerRef={photoWrapRef}
          />
        )}
        {viewMode === 'Measurements' && (
          <MeasurementOverlay
            landmarks={landmarks}
            imgW={imageDimensions?.width}
            imgH={imageDimensions?.height}
            containerRef={photoWrapRef}
          />
        )}
      </div>

      {/* View mode tabs */}
      <div className="sp-view-tabs">
        {MODES.map(m => (
          <button
            key={m}
            className={`sp-view-tab ${viewMode === m ? 'active' : ''}`}
            onClick={() => setViewMode(m)}
          >
            {m}
          </button>
        ))}
      </div>
    </div>
  )
}
