import React, { useRef, useEffect, useState } from 'react'

// ── Color-coded feature groups ─────────────────────────────────────────────
const FEATURE_GROUPS = [
  {
    name: 'Face Outline',
    color: 'rgba(120,180,255,0.55)',
    glow: '#78b4ff',
    indices: [10,338,297,332,284,251,389,356,454,323,361,288,397,365,379,378,400,377,152,148,176,149,150,136,172,58,132,93,234,127,162,21,54,103,67,109,10],
    closed: true,
  },
  {
    name: 'Left Eye',
    color: 'rgba(0,230,200,0.85)',
    glow: '#00e6c8',
    indices: [33,160,158,133,153,144,33],
    closed: true,
  },
  {
    name: 'Right Eye',
    color: 'rgba(0,230,200,0.85)',
    glow: '#00e6c8',
    indices: [362,385,387,263,373,380,362],
    closed: true,
  },
  {
    name: 'Left Brow',
    color: 'rgba(255,200,60,0.85)',
    glow: '#ffc83c',
    indices: [70,63,105,66,107],
    closed: false,
  },
  {
    name: 'Right Brow',
    color: 'rgba(255,200,60,0.85)',
    glow: '#ffc83c',
    indices: [336,296,334,293,300],
    closed: false,
  },
  {
    name: 'Nose Bridge',
    color: 'rgba(180,100,255,0.75)',
    glow: '#b464ff',
    indices: [168,6,197,195,5,4],
    closed: false,
  },
  {
    name: 'Nose Width',
    color: 'rgba(180,100,255,0.75)',
    glow: '#b464ff',
    indices: [129,98,97,2,326,358],
    closed: false,
  },
  {
    name: 'Upper Lip',
    color: 'rgba(255,100,160,0.85)',
    glow: '#ff64a0',
    indices: [61,185,40,39,37,0,267,269,270,291],
    closed: false,
  },
  {
    name: 'Lower Lip',
    color: 'rgba(255,100,160,0.85)',
    glow: '#ff64a0',
    indices: [61,146,91,181,84,17,314,405,321,291],
    closed: false,
  },
]

// Key anchor dots to highlight
const KEY_DOTS = [
  { idx: 33,  color: '#00e6c8', label: null },        // L eye outer
  { idx: 263, color: '#00e6c8', label: null },        // R eye outer
  { idx: 4,   color: '#b464ff', label: null },        // nose tip
  { idx: 152, color: '#78b4ff', label: null },        // chin
  { idx: 10,  color: '#78b4ff', label: null },        // forehead
  { idx: 61,  color: '#ff64a0', label: null },        // L mouth corner
  { idx: 291, color: '#ff64a0', label: null },        // R mouth corner
  { idx: 107, color: '#ffc83c', label: null },        // L brow
  { idx: 336, color: '#ffc83c', label: null },        // R brow
  { idx: 234, color: '#78b4ff', label: null },        // L cheek
  { idx: 454, color: '#78b4ff', label: null },        // R cheek
  { idx: 172, color: '#78b4ff', label: null },        // L jaw corner
  { idx: 397, color: '#78b4ff', label: null },        // R jaw corner
]

// Feature callout labels
const CALLOUTS = [
  { idx: 159, dx: -60, dy: -12, label: 'Left Eye',   color: '#00e6c8' },
  { idx: 386, dx:  12, dy: -12, label: 'Right Eye',  color: '#00e6c8' },
  { idx: 66,  dx: -60, dy: -10, label: 'Eyebrows',   color: '#ffc83c' },
  { idx: 4,   dx:  14, dy:   0, label: 'Nose',       color: '#b464ff' },
  { idx: 0,   dx: -50, dy:  18, label: 'Lips',       color: '#ff64a0' },
  { idx: 234, dx: -70, dy:   0, label: 'Jaw',        color: '#78b4ff' },
]

export default function LandmarkOverlay({ landmarks, imgW, imgH, visible, containerRef }) {
  const [dims, setDims]   = useState({ w: 0, h: 0 })
  const [phase, setPhase] = useState(0)  // animation phase 0=dots 1=lines 2=callouts

  // Measure rendered image size
  useEffect(() => {
    if (!containerRef?.current || !imgW || !imgH) return
    const measure = () => {
      const img = containerRef.current?.querySelector('img')
      if (!img) return
      setDims({ w: img.clientWidth, h: img.clientHeight })
    }
    const img = containerRef.current?.querySelector('img')
    if (img) {
      if (img.complete) measure()
      else img.addEventListener('load', measure)
    }
    window.addEventListener('resize', measure)
    const t = setTimeout(measure, 80)
    return () => {
      window.removeEventListener('resize', measure)
      clearTimeout(t)
      img?.removeEventListener('load', measure)
    }
  }, [containerRef, imgW, imgH, visible])

  // Staggered animation reveal
  useEffect(() => {
    if (!visible) { setPhase(0); return }
    setPhase(0)
    const t1 = setTimeout(() => setPhase(1), 100)
    const t2 = setTimeout(() => setPhase(2), 500)
    const t3 = setTimeout(() => setPhase(3), 900)
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3) }
  }, [visible, dims.w])

  if (!visible || !landmarks?.length || !imgW || !imgH || dims.w === 0) return null

  const scaleX = dims.w / imgW
  const scaleY = dims.h / imgH
  const mx = (x) => x * scaleX
  const my = (y) => y * scaleY

  const dotR  = Math.max(2, Math.min(4.5, dims.w / 100))
  const sw    = Math.max(0.8, Math.min(1.8, dims.w / 300))
  const glowR = dotR * 2.5
  const uid   = 'lmo'  // unique ID prefix for filters

  return (
    <svg
      width={dims.w}
      height={dims.h}
      style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none', overflow: 'visible' }}
    >
      <defs>
        {/* Glow filter for dots */}
        <filter id={`${uid}-glow-teal`} x="-100%" y="-100%" width="300%" height="300%">
          <feGaussianBlur stdDeviation="2.5" result="blur" />
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id={`${uid}-glow-yellow`} x="-100%" y="-100%" width="300%" height="300%">
          <feGaussianBlur stdDeviation="2" result="blur" />
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id={`${uid}-glow-line`} x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="1.5" result="blur" />
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>

        {/* Scan line gradient */}
        <linearGradient id={`${uid}-scan`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%"   stopColor="rgba(0,230,200,0)" />
          <stop offset="50%"  stopColor="rgba(0,230,200,0.18)" />
          <stop offset="100%" stopColor="rgba(0,230,200,0)" />
        </linearGradient>
      </defs>

      {/* ── Symmetry axis (always shown first) ─────────────────── */}
      {landmarks[10] && landmarks[152] && (
        <line
          x1={mx(landmarks[10].x)}  y1={my(landmarks[10].y)}
          x2={mx(landmarks[152].x)} y2={my(landmarks[152].y)}
          stroke="rgba(120,180,255,0.30)"
          strokeWidth={sw * 0.8}
          strokeDasharray="5 5"
          style={{ transition: 'opacity 0.4s', opacity: phase >= 1 ? 1 : 0 }}
        />
      )}

      {/* ── Color-coded feature lines ───────────────────────────── */}
      {phase >= 1 && FEATURE_GROUPS.map((grp, gi) => {
        const pts = grp.indices.map(i => landmarks[i]).filter(Boolean)
        if (pts.length < 2) return null
        const d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${mx(p.x)} ${my(p.y)}`).join(' ')
          + (grp.closed ? ' Z' : '')

        return (
          <g key={gi}>
            {/* Glow copy */}
            <path
              d={d}
              fill="none"
              stroke={grp.glow}
              strokeWidth={sw * 2.5}
              opacity="0.15"
              filter={`url(#${uid}-glow-line)`}
              style={{
                transition: `opacity 0.5s ${gi * 30}ms`,
                opacity: phase >= 1 ? 0.15 : 0,
              }}
            />
            {/* Crisp line */}
            <path
              d={d}
              fill="none"
              stroke={grp.color}
              strokeWidth={sw}
              strokeLinejoin="round"
              strokeLinecap="round"
              style={{
                transition: `opacity 0.4s ${gi * 40}ms`,
                opacity: phase >= 1 ? 1 : 0,
              }}
            />
          </g>
        )
      })}

      {/* ── Glowing key dots ────────────────────────────────────── */}
      {phase >= 2 && KEY_DOTS.map(({ idx, color }) => {
        const p = landmarks[idx]
        if (!p) return null
        return (
          <g key={idx}>
            {/* Outer glow ring */}
            <circle
              cx={mx(p.x)} cy={my(p.y)} r={glowR}
              fill={color}
              opacity="0.12"
            />
            {/* Mid glow */}
            <circle
              cx={mx(p.x)} cy={my(p.y)} r={dotR * 1.6}
              fill={color}
              opacity="0.22"
            />
            {/* Core dot */}
            <circle
              cx={mx(p.x)} cy={my(p.y)} r={dotR}
              fill={color}
              opacity="0.95"
              style={{ transition: `opacity 0.3s ${(idx % 10) * 30}ms` }}
            />
            {/* White center sparkle */}
            <circle
              cx={mx(p.x)} cy={my(p.y)} r={dotR * 0.4}
              fill="white"
              opacity="0.8"
            />
          </g>
        )
      })}

      {/* ── Feature callout labels ───────────────────────────────── */}
      {phase >= 3 && CALLOUTS.map(({ idx, dx, dy, label, color }) => {
        const p = landmarks[idx]
        if (!p) return null
        const lx = mx(p.x) + dx
        const ly = my(p.y) + dy

        // Only show if within bounds
        if (lx < 5 || lx > dims.w - 5) return null

        return (
          <g key={`callout-${idx}`} style={{ transition: 'opacity 0.5s', opacity: phase >= 3 ? 1 : 0 }}>
            {/* connector dot */}
            <line
              x1={mx(p.x)} y1={my(p.y)}
              x2={lx + (dx < 0 ? 28 : 0)} y2={ly + 5}
              stroke={color}
              strokeWidth={0.7}
              opacity="0.5"
              strokeDasharray="2 2"
            />
            {/* label pill */}
            <rect
              x={lx - 4}
              y={ly - 9}
              width={label.length * 6.2 + 8}
              height={14}
              rx={4}
              fill="rgba(10,12,20,0.75)"
              stroke={color}
              strokeWidth={0.6}
              opacity="0.9"
            />
            <text
              x={lx}
              y={ly + 1}
              fill={color}
              fontSize={Math.max(8, Math.min(10, dims.w / 40))}
              fontFamily="'Inter', sans-serif"
              fontWeight="600"
              letterSpacing="0.3"
              opacity="0.95"
            >
              {label}
            </text>
          </g>
        )
      })}

      {/* ── Subtle scan overlay line ─────────────────────────────── */}
      {phase >= 1 && (
        <rect
          x={0} y={0}
          width={dims.w} height={Math.max(40, dims.h * 0.12)}
          fill={`url(#${uid}-scan)`}
          style={{
            animation: 'lmoScan 2.2s ease-in-out forwards',
          }}
        />
      )}

      <style>{`
        @keyframes lmoScan {
          0%   { transform: translateY(0); opacity: 0.9; }
          80%  { transform: translateY(${dims.h - 40}px); opacity: 0.6; }
          100% { transform: translateY(${dims.h}px); opacity: 0; }
        }
      `}</style>
    </svg>
  )
}
