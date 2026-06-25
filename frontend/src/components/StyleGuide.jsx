import React, { useState } from 'react'

const SKIN_SWATCH_COLORS = {
  'I': '#F5E8D8', 'II': '#E8C9A0', 'III': '#C68642',
  'IV': '#8D5524', 'V': '#5C3317', 'VI': '#3B1F0A',
}

function Section({ emoji, title, children }) {
  return (
    <div className="style-section">
      <div className="style-section-title">
        <span>{emoji}</span> {title}
      </div>
      {children}
    </div>
  )
}

function TagList({ items, color }) {
  return (
    <div className="style-tag-list">
      {items.map((item, i) => (
        <span key={i} className="style-tag" style={{ '--tag-color': color || 'var(--green)' }}>
          {item}
        </span>
      ))}
    </div>
  )
}

function ColorSwatches({ colors, title }) {
  return (
    <div className="style-swatches-wrap">
      {title && <div className="style-swatches-label">{title}</div>}
      <div className="style-swatches">
        {colors.map((c, i) => (
          <div key={i} className="style-swatch-item">
            <div className="style-swatch-dot" style={{ background: c.hex || '#888' }} />
            <span className="style-swatch-name">{c.name || c}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

// Map color names to approximate hex values for visual swatches
function resolveHex(name) {
  const map = {
    'Soft pink': '#F4A7B9', 'Light blue': '#AED9E0', 'Lavender': '#C9B1D9',
    'Warm white': '#FAF3E0', 'Mint green': '#B5EAD7', 'Peach': '#FFDAB9',
    'Coral': '#FF7F50', 'Warm yellow': '#FFD700', 'Sage green': '#B2AC88',
    'Sky blue': '#87CEEB', 'Terracotta': '#C67B5C', 'Olive green': '#708238',
    'Warm red': '#C23B22', 'Mustard': '#FFDB58', 'Deep teal': '#008080',
    'Burnt orange': '#CC5500', 'Rich purple': '#6B2A8B', 'Forest green': '#228B22',
    'Cobalt blue': '#0047AB', 'Bright white': '#FFFFFF', 'Rich gold': '#CFB53B',
    'Hot pink': '#FF69B4', 'Vibrant orange': '#FF8C00', 'Royal purple': '#7B2D8B',
    'Electric blue': '#007FFF', 'Bright red': '#FF3131', 'Emerald green': '#50C878',
    'Ash blonde': '#EEE0B1', 'Platinum': '#E5E4E2', 'Light golden brown': '#C8A97E',
    'Rose gold': '#B76E79', 'Golden blonde': '#F2C94C', 'Honey blonde': '#E8AA4B',
    'Warm brown': '#8B5E3C', 'Strawberry blonde': '#D4785A', 'Caramel': '#C68642',
    'Chestnut': '#954535', 'Rich brown': '#6B3A2A', 'Dark copper': '#A0522D',
    'Dark chocolate': '#3D1C02', 'Mahogany': '#5C2317', 'Deep auburn': '#6D1919',
    'Jet black': '#1A1A1A', 'Deep espresso': '#3B2314', 'Dark auburn': '#6B2A14',
    'Burgundy': '#800020', 'Natural black': '#0D0D0D', 'Blue-black': '#161624',
    'Deep plum': '#59063F', 'Chocolate brown': '#3B1F0A',
    'Off-white': '#FAF9F6', 'Light grey': '#D3D3D3', 'Blush beige': '#E8CFC4',
    'Cream': '#FFFDD0', 'Camel': '#C19A6B', 'Light khaki': '#C3B091',
    'Warm beige': '#D4B896', 'Chocolate brown ': '#3B1F0A', 'Tan': '#D2B48C',
    'Dark olive': '#5C5C1A', 'Charcoal': '#36454F', 'Black': '#0D0D0D',
    'Dark navy': '#001F3F', 'Deep grey': '#444444',
  }
  return map[name] || '#888888'
}

function WomenGuide({ data }) {
  const { women } = data
  const { makeup, eyebrowShape, hairstyles, hairColors, glasses, colorPalette, basedOn } = women

  const hairColorItems = hairColors.map(c => ({ name: c, hex: resolveHex(c) }))
  const bestItems      = colorPalette.best.map(c => ({ name: c, hex: resolveHex(c) }))
  const neutralItems   = colorPalette.neutrals.map(c => ({ name: c, hex: resolveHex(c) }))

  return (
    <div className="style-guide-content fade-up">
      {/* Based on */}
      <div className="style-based-on">
        <span>✦</span> Based on your <strong>{basedOn.faceShape}</strong> face shape ·{' '}
        <strong>{basedOn.skinTone}</strong> · <strong>{basedOn.eyeShape}</strong> eyes
      </div>

      {/* Makeup */}
      <Section emoji="💄" title="Makeup Recommendations">
        <div className="style-makeup-grid">
          {Object.entries(makeup).map(([key, val]) => (
            <div key={key} className="style-makeup-card">
              <div className="style-makeup-key">{key.charAt(0).toUpperCase() + key.slice(1)}</div>
              <div className="style-makeup-val">{val}</div>
            </div>
          ))}
        </div>
      </Section>

      {/* Eyebrows */}
      <Section emoji="🖊️" title="Eyebrow Shape">
        <p className="style-text">{eyebrowShape}</p>
      </Section>

      {/* Hairstyles */}
      <Section emoji="💇‍♀️" title="Hairstyle Recommendations">
        <TagList items={hairstyles} color="var(--purple)" />
      </Section>

      {/* Hair Color */}
      <Section emoji="🎨" title="Hair Color Suggestions">
        <ColorSwatches colors={hairColorItems} />
      </Section>

      {/* Glasses */}
      <Section emoji="👓" title="Glasses Recommendations">
        <p className="style-text">{glasses}</p>
      </Section>

      {/* Color Palette */}
      <Section emoji="🌈" title="Clothing Color Palette">
        <p className="style-tip">💡 {colorPalette.tip}</p>
        <ColorSwatches colors={bestItems} title="Best Colors" />
        <ColorSwatches colors={neutralItems} title="Your Neutrals" />
        {colorPalette.avoid?.length > 0 && (
          <div className="style-avoid">
            <span>⚠</span> Avoid: {colorPalette.avoid.join(', ')}
          </div>
        )}
      </Section>
    </div>
  )
}

function MenGuide({ data }) {
  const { men } = data
  const { beardStyle, hairstyles, glasses, groomingTips, colorPalette, hairColors, basedOn } = men

  const hairColorItems = hairColors.map(c => ({ name: c, hex: resolveHex(c) }))
  const bestItems      = colorPalette.best.map(c => ({ name: c, hex: resolveHex(c) }))
  const neutralItems   = colorPalette.neutrals.map(c => ({ name: c, hex: resolveHex(c) }))

  return (
    <div className="style-guide-content fade-up">
      {/* Based on */}
      <div className="style-based-on">
        <span>✦</span> Based on your <strong>{basedOn.faceShape}</strong> face shape ·{' '}
        <strong>{basedOn.skinTone}</strong> · Symmetry: <strong>{basedOn.symmetry}%</strong>
      </div>

      {/* Beard */}
      <Section emoji="🧔" title="Beard Style">
        <p className="style-text">{beardStyle}</p>
      </Section>

      {/* Hairstyles */}
      <Section emoji="💈" title="Hairstyle Recommendations">
        <TagList items={hairstyles} color="var(--blue)" />
      </Section>

      {/* Glasses */}
      <Section emoji="👓" title="Glasses Recommendations">
        <p className="style-text">{glasses}</p>
      </Section>

      {/* Grooming Tips */}
      <Section emoji="✨" title="Grooming Suggestions">
        <ul className="style-tips-list">
          {groomingTips.map((tip, i) => (
            <li key={i}>{tip}</li>
          ))}
        </ul>
      </Section>

      {/* Hair Color */}
      <Section emoji="🎨" title="Hair Color Suggestions">
        <ColorSwatches colors={hairColorItems} />
      </Section>

      {/* Color Palette */}
      <Section emoji="🌈" title="Clothing Color Palette">
        <p className="style-tip">💡 {colorPalette.tip}</p>
        <ColorSwatches colors={bestItems} title="Best Colors" />
        <ColorSwatches colors={neutralItems} title="Your Neutrals" />
        {colorPalette.avoid?.length > 0 && (
          <div className="style-avoid">
            <span>⚠</span> Avoid: {colorPalette.avoid.join(', ')}
          </div>
        )}
      </Section>
    </div>
  )
}

export default function StyleGuide({ styleData, defaultGender }) {
  // Convert 'male'/'female' from App to 'men'/'women' for internal mode
  const initialMode = defaultGender === 'male' ? 'men' : defaultGender === 'female' ? 'women' : null
  const [mode, setMode]       = useState(initialMode)
  const [loading, setLoading] = useState(false)

  if (!styleData) return null

  const handleSelect = (gender) => {
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
      setMode(gender)
    }, 600)
  }

  return (
    <div className="style-guide-section">
      {/* Header */}
      <div className="style-guide-header">
        <div className="style-guide-title">✦ Personalized Style Guide</div>
        <div className="style-guide-sub">AI-curated recommendations based on your facial analysis</div>
      </div>

      {/* Gender selector buttons */}
      {!mode && !loading && (
        <div className="style-gender-btns">
          <button
            className="style-gender-btn style-women-btn"
            onClick={() => handleSelect('women')}
          >
            <div className="style-gender-icon">💄</div>
            <div className="style-gender-label">Women's Guide</div>
            <div className="style-gender-sub">Makeup · Hair · Glasses · Colors</div>
          </button>
          <button
            className="style-gender-btn style-men-btn"
            onClick={() => handleSelect('men')}
          >
            <div className="style-gender-icon">🧔</div>
            <div className="style-gender-label">Men's Guide</div>
            <div className="style-gender-sub">Beard · Hair · Glasses · Grooming</div>
          </button>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="style-loading">
          <div className="style-loading-spinner" />
          <span>Crafting your style guide…</span>
        </div>
      )}

      {/* Content */}
      {mode && !loading && (
        <div className="style-content-wrap">
          {/* Switch gender tabs */}
          <div className="style-tabs">
            <button
              className={`style-tab ${mode === 'women' ? 'active' : ''}`}
              onClick={() => setMode('women')}
            >💄 Women</button>
            <button
              className={`style-tab ${mode === 'men' ? 'active' : ''}`}
              onClick={() => setMode('men')}
            >🧔 Men</button>
          </div>

          {mode === 'women' && <WomenGuide data={styleData} />}
          {mode === 'men'   && <MenGuide   data={styleData} />}
        </div>
      )}
    </div>
  )
}
