import React, { useState } from 'react'

// Key landmark groups for drawing connections
const CONNECTIONS = [
  // Face outline
  [10,338,297,332,284,251,389,356,454,323,361,288,397,365,379,378,400,377,152,148,176,149,150,136,172,58,132,93,234,127,162,21,54,103,67,109,10],
  // Left eye
  [33,160,158,133,153,144,33],
  // Right eye
  [362,385,387,263,373,380,362],
  // Left brow
  [70,63,105,66,107],
  // Right brow
  [336,296,334,293,300],
  // Nose bridge
  [168,6,197,195,5,4],
  // Nostrils
  [129,98,97,2,326,358],
  // Upper lip
  [61,185,40,39,37,0,267,269,270,291],
  // Lower lip
  [61,146,91,181,84,17,314,405,321,291],
]

const DOT_INDICES = [10,152,234,454,33,133,362,263,61,291,4,172,397,1,199]

export default function LandmarkOverlay({ landmarks, imgW, imgH, visible }) {
  if (!visible || !landmarks?.length) return null

  const vbW = imgW || 400
  const vbH = imgH || 500

  return (
    <svg
      viewBox={`0 0 ${vbW} ${vbH}`}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
      }}
    >
      {/* Connection lines */}
      {CONNECTIONS.map((group, gi) => {
        const pts = group.map(i => landmarks[i]).filter(Boolean)
        if (pts.length < 2) return null
        const d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')
        return (
          <path
            key={gi}
            d={d}
            fill="none"
            stroke="rgba(63,185,80,0.55)"
            strokeWidth="0.8"
          />
        )
      })}

      {/* Key landmark dots */}
      {DOT_INDICES.map(idx => {
        const p = landmarks[idx]
        if (!p) return null
        return (
          <circle
            key={idx}
            cx={p.x}
            cy={p.y}
            r="2.5"
            fill="var(--green)"
            opacity="0.85"
          />
        )
      })}

      {/* Symmetry axis */}
      {landmarks[10] && landmarks[152] && (
        <line
          x1={landmarks[10].x}  y1={landmarks[10].y}
          x2={landmarks[152].x} y2={landmarks[152].y}
          stroke="rgba(88,166,255,0.4)"
          strokeWidth="0.8"
          strokeDasharray="4 4"
        />
      )}
    </svg>
  )
}
