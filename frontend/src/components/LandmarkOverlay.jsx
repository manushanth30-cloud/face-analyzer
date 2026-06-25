import React, { useEffect, useState } from 'react'

// MediaPipe 478-landmark region index ranges
// These are approximate groupings based on the face mesh topology
const REGION_DOTS = [
  // Face silhouette / jaw
  { indices: [10,338,297,332,284,251,389,356,454,323,361,288,397,365,379,378,400,377,152,148,176,149,150,136,172,58,132,93,234,127,162,21,54,103,67,109], color: 'rgba(120,160,255,0.75)' },

  // Left eye region
  { indices: [33,246,161,160,159,158,157,173,133,155,154,153,145,144,163,7,
               112,26,22,23,24,110,25,226,31,228,229,230,231,232,233,244,245], color: 'rgba(0,220,200,0.85)' },

  // Right eye region
  { indices: [362,398,384,385,386,387,388,466,263,249,390,373,374,380,381,382,
               341,256,252,253,254,339,255,446,261,448,449,450,451,452,453,464,465], color: 'rgba(0,220,200,0.85)' },

  // Left eyebrow
  { indices: [70,63,105,66,107,55,65,52,53,46], color: 'rgba(255,200,60,0.85)' },

  // Right eyebrow
  { indices: [300,293,334,296,336,285,295,282,283,276], color: 'rgba(255,200,60,0.85)' },

  // Nose bridge + tip + nostrils
  { indices: [168,6,197,195,5,4,1,19,94,2,164,0,11,12,13,14,15,16,17,18,200,199,
              129,98,97,96,95,88,178,87,86,85,84,83,182,106,43,204,183,42,41,38,12,
              358,327,326,325,324,317,402,318,316,315,314,313,406,335,271,432,424,
              273,272,269,268,267,291,375,321,405,314,17,84,181,91,146,61], color: 'rgba(180,100,255,0.80)' },

  // Lips / mouth
  { indices: [61,185,40,39,37,0,267,269,270,291,375,321,405,314,17,84,181,91,146,
              76,77,90,180,85,16,315,404,320,307,306,408,304,303,302,11,72,73,74,
              184,42,74,73,72,11,302,303,304,408,306,307,320,404,315], color: 'rgba(255,100,155,0.85)' },

  // Left cheek / mid face
  { indices: [116,117,118,119,120,121,126,142,36,205,187,123,50,101,100,47,114,
              207,206,203,177,137,215,138,135,169,170,140,171,208,32,194,211,210,214,
              192,213,212,216,186,92,165,167,166,108,69,104,68,71], color: 'rgba(120,160,255,0.55)' },

  // Right cheek / mid face
  { indices: [345,346,347,348,349,350,357,372,266,425,416,352,280,330,329,277,343,
              427,426,423,401,366,435,362,364,394,395,369,396,428,262,418,431,430,434,
              416,433,432,436,410,322,391,393,392,338,299,333,298,301], color: 'rgba(120,160,255,0.55)' },

  // Forehead / upper face
  { indices: [10,9,8,168,107,66,105,63,70,156,143,35,31,228,229,230,231,232,233,
              244,245,122,111,117,118,119,120,121,128,232,233,244,
              337,299,333,298,301,368,372,264,261,448,449,450,451,452,453,464,465,
              351,340,345,346,347,348,349,350,357], color: 'rgba(80,140,255,0.55)' },

  // Chin / lower jaw
  { indices: [152,377,400,378,379,365,397,288,361,323,454,356,389,251,284,332,297,338,
              175,171,396,369,395,394,430,431,418,262,369], color: 'rgba(120,160,255,0.65)' },

  // Hair-line dots (highest points of forehead landmarks)
  { indices: [10,67,109,103,54,21,162,127,234,93,132,58,172,136,150,149,176,148,152,
              377,400,378,379,365,397,288,361,323,454,356,389,251,284,332,297,338,10], color: 'rgba(100,200,255,0.45)' },
]

// All remaining landmark indices (0-477) not in above groups — render as faint white dots
function getAllIndices() {
  const all = new Set()
  for (let i = 0; i < 478; i++) all.add(i)
  return [...all]
}
const ALL_IDX = getAllIndices()

export default function LandmarkOverlay({ landmarks, imgW, imgH, visible, containerRef }) {
  const [dims, setDims] = useState({ w: 0, h: 0 })

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

  if (!visible || !landmarks?.length || !imgW || !imgH || dims.w === 0) return null

  const scaleX = dims.w / imgW
  const scaleY = dims.h / imgH
  const mx = (x) => x * scaleX
  const my = (y) => y * scaleY

  // Dot size scales with image
  const r = Math.max(1.0, Math.min(2.2, dims.w / 180))

  // Build a color map — region dots take priority over base dots
  const colorMap = {}
  REGION_DOTS.forEach(({ indices, color }) => {
    indices.forEach(idx => { colorMap[idx] = color })
  })

  return (
    <svg
      width={dims.w}
      height={dims.h}
      style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none' }}
    >
      {/* All 478 landmarks — base layer faint */}
      {ALL_IDX.map(idx => {
        const p = landmarks[idx]
        if (!p) return null
        const color = colorMap[idx] || 'rgba(180,210,255,0.30)'
        return (
          <circle
            key={idx}
            cx={mx(p.x)}
            cy={my(p.y)}
            r={colorMap[idx] ? r : r * 0.75}
            fill={color}
          />
        )
      })}
    </svg>
  )
}
