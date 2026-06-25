import React, { useState } from 'react'

/* ─── helpers ─────────────────────────────────────────────── */
function parseSkin(skinToneStr) {
  // "Fitzpatrick IV" → "IV"
  return (skinToneStr || '').replace('Fitzpatrick', '').trim() || 'IV'
}

const SKIN_HEX = {
  'I':'#F5E8D8','II':'#E8C9A0','III':'#C68642',
  'IV':'#8D5524','V':'#5C3317','VI':'#3B1F0A',
}

function resolveHex(name) {
  const map = {
    'Soft pink':'#F4A7B9','Light blue':'#AED9E0','Lavender':'#C9B1D9',
    'Warm white':'#FAF3E0','Mint green':'#B5EAD7','Peach':'#FFDAB9',
    'Coral':'#FF7F50','Warm yellow':'#FFD700','Sage green':'#B2AC88',
    'Sky blue':'#87CEEB','Terracotta':'#C67B5C','Olive green':'#708238',
    'Warm red':'#C23B22','Mustard':'#FFDB58','Deep teal':'#008080',
    'Burnt orange':'#CC5500','Rich purple':'#6B2A8B','Forest green':'#228B22',
    'Cobalt blue':'#0047AB','Bright white':'#FFFFFF','Rich gold':'#CFB53B',
    'Hot pink':'#FF69B4','Vibrant orange':'#FF8C00','Royal purple':'#7B2D8B',
    'Electric blue':'#007FFF','Bright red':'#FF3131','Emerald green':'#50C878',
    'Ash blonde':'#EEE0B1','Platinum':'#E5E4E2','Light golden brown':'#C8A97E',
    'Rose gold':'#B76E79','Golden blonde':'#F2C94C','Honey blonde':'#E8AA4B',
    'Warm brown':'#8B5E3C','Strawberry blonde':'#D4785A','Caramel':'#C68642',
    'Chestnut':'#954535','Rich brown':'#6B3A2A','Dark copper':'#A0522D',
    'Dark chocolate':'#3D1C02','Mahogany':'#5C2317','Deep auburn':'#6D1919',
    'Jet black':'#1A1A1A','Deep espresso':'#3B2314','Dark auburn':'#6B2A14',
    'Burgundy':'#800020','Natural black':'#0D0D0D','Blue-black':'#161624',
    'Deep plum':'#59063F','Chocolate brown':'#3B1F0A',
    'Natural Black':'#0D0D0D','Dark Brown':'#3B1F0A','Soft Black':'#1A1A1A',
    'Chestnut Brown':'#954535','Ash Brown':'#8B8878',
    'Off-white':'#FAF9F6','Light grey':'#D3D3D3','Blush beige':'#E8CFC4',
    'Cream':'#FFFDD0','Camel':'#C19A6B','Black':'#0D0D0D',
    'Dark navy':'#001F3F','Charcoal':'#36454F',
  }
  return map[name] || '#888888'
}

/* ─── SVG face card (beard/hair styles) ───────────────────── */
const BEARD_MAP = {
  Oval:    ['Full Beard','Goatee','Short Boxed','Light Stubble'],
  Round:   ['Goatee','Chin Strap','Short Boxed','Light Stubble'],
  Square:  ['Circle Beard','Short Stubble','Rounded Full','Light Stubble'],
  Heart:   ['Full Beard','Chinstrap','Short Boxed','Goatee'],
  Diamond: ['Full Beard','Short Boxed','Goatee','Light Stubble'],
  Oblong:  ['Short Full','Circle Beard','Goatee','Light Stubble'],
}

const GLASSES_MAP = {
  Oval:    ['Aviators','Round','Wayfarer','Clubmaster'],
  Round:   ['Rectangular','Square','Wayfarer','Clubmaster'],
  Square:  ['Round','Oval','Wayfarer','Rimless'],
  Heart:   ['Light Frame','Rectangular','Rimless','Clubmaster'],
  Diamond: ['Oval','Wayfarer','Clubmaster','Round'],
  Oblong:  ['Wide Frame','Wayfarer','Rectangular','Clubmaster'],
}

function FaceCard({ hairStyle, beardType, label, badge, badgeColor, skinCode = 'IV' }) {
  const skin = SKIN_HEX[skinCode] || '#8D5524'
  const hr = '#1a1205'
  const bd = '#251808'

  // ── Hair shapes ────────────────────────────────────────────
  const hairPaths = {
    fade:   <><ellipse cx="30" cy="8" rx="19" ry="8" fill={hr}/><rect x="11" y="8" width="38" height="9" fill={hr}/></>,
    quiff:  <><ellipse cx="30" cy="7" rx="18" ry="8" fill={hr}/><path d="M14 13 Q30 2 46 13" fill={hr}/></>,
    part:   <><ellipse cx="30" cy="9" rx="19" ry="8" fill={hr}/><rect x="11" y="9" width="38" height="8" fill={hr}/></>,
    pompa:  <><ellipse cx="30" cy="5" rx="17" ry="7" fill={hr}/><path d="M13 10 Q30 0 47 10" fill={hr}/></>,
    crop:   <><rect x="11" y="10" width="38" height="7" rx="2" fill={hr}/><ellipse cx="30" cy="10" rx="19" ry="6" fill={hr}/></>,
    buzz:   <ellipse cx="30" cy="11" rx="19" ry="6" fill={hr} opacity="0.72"/>,
    long:   <><ellipse cx="30" cy="9" rx="19" ry="8" fill={hr}/><rect x="11" y="9" width="38" height="8" fill={hr}/><rect x="9" y="17" width="6" height="32" rx="3" fill={hr}/><rect x="45" y="17" width="6" height="32" rx="3" fill={hr}/></>,
    lob:    <><ellipse cx="30" cy="9" rx="19" ry="8" fill={hr}/><rect x="11" y="9" width="38" height="8" fill={hr}/><rect x="9" y="17" width="6" height="20" rx="3" fill={hr}/><rect x="45" y="17" width="6" height="20" rx="3" fill={hr}/></>,
    default:<><ellipse cx="30" cy="9" rx="19" ry="8" fill={hr}/><rect x="11" y="9" width="38" height="7" fill={hr}/></>,
  }
  const hairKey = {
    'High Fade':'fade','High Fade w/ Volume':'fade','High fade':'fade',
    'Quiff':'quiff','Textured Undercut':'part','Undercut':'part',
    'Side Part':'part','Pompadour':'pompa','French Crop':'crop','Crop':'crop',
    'Buzz Cut':'buzz','Beach waves':'long','Long layers':'long',
    'Blunt bob':'lob','Lob':'lob','Shoulder-length lob':'lob',
    'Textured crop':'crop','Layered cut':'long','Side-swept bangs':'part',
    'Curtain bangs':'crop','Long waves':'long',
  }[hairStyle] || 'default'
  const hairEl = hairPaths[hairKey]

  // ── Beard shapes ───────────────────────────────────────────
  const beardPaths = {
    'Goatee':      <><ellipse cx="30" cy="42" rx="6.5" ry="3" fill={bd} opacity="0.85"/><ellipse cx="30" cy="49" rx="7" ry="6" fill={bd}/></>,
    'Chin Strap':  <path d="M15 36 Q30 60 45 36" stroke={bd} strokeWidth="4.5" fill="none" strokeLinecap="round"/>,
    'Chinstrap':   <path d="M15 36 Q30 60 45 36" stroke={bd} strokeWidth="4.5" fill="none" strokeLinecap="round"/>,
    'Short Boxed': <><ellipse cx="30" cy="42" rx="8" ry="3" fill={bd} opacity="0.8"/><path d="M17 41 Q17 58 30 60 Q43 58 43 41 L40 42 Q40 54 30 56 Q20 54 20 42Z" fill={bd}/></>,
    'Light Stubble':<ellipse cx="30" cy="47" rx="15" ry="11" fill={bd} opacity="0.32"/>,
    'Short Stubble':<ellipse cx="30" cy="47" rx="15" ry="11" fill={bd} opacity="0.32"/>,
    'Stubble':     <ellipse cx="30" cy="47" rx="15" ry="11" fill={bd} opacity="0.32"/>,
    'Full Beard':  <><ellipse cx="30" cy="42" rx="8" ry="3" fill={bd} opacity="0.85"/><ellipse cx="30" cy="50" rx="16" ry="13" fill={bd}/></>,
    'Rounded Full':<><ellipse cx="30" cy="42" rx="8" ry="3" fill={bd} opacity="0.8"/><ellipse cx="30" cy="50" rx="15" ry="12" fill={bd}/></>,
    'Short Full':  <ellipse cx="30" cy="48" rx="15" ry="11" fill={bd} opacity="0.75"/>,
    'Circle Beard':<><ellipse cx="30" cy="42" rx="7" ry="3" fill={bd}/><circle cx="30" cy="51" r="8" fill={bd}/></>,
  }
  const beardEl = beardType ? (beardPaths[beardType] || null) : null

  return (
    <div className="sg-face-card">
      {badge && (
        <div className="sg-face-badge" style={{ background: badgeColor === 'avoid' ? 'var(--red-bg)' : 'var(--green-bg)', color: badgeColor === 'avoid' ? 'var(--red)' : 'var(--green)' }}>
          {badgeColor === 'avoid' ? '✗ Avoid' : '✓ Best'}
        </div>
      )}
      <svg viewBox="0 0 60 65" className="sg-face-svg">
        {/* Background */}
        <rect x="0" y="0" width="60" height="65" fill="#0d1117" rx="6"/>
        {/* Hair (behind face) */}
        {hairEl}
        {/* Face */}
        <ellipse cx="30" cy="33" rx="19" ry="23" fill={skin}/>
        {/* Ears */}
        <ellipse cx="11" cy="32" rx="4" ry="5.5" fill={skin}/>
        <ellipse cx="49" cy="32" rx="4" ry="5.5" fill={skin}/>
        {/* Eyebrows */}
        <path d="M18 23 Q22 21 26 23" stroke={hr} strokeWidth="2" fill="none" strokeLinecap="round"/>
        <path d="M34 23 Q38 21 42 23" stroke={hr} strokeWidth="2" fill="none" strokeLinecap="round"/>
        {/* Eyes */}
        <ellipse cx="22" cy="27" rx="3.5" ry="2.5" fill="white"/>
        <ellipse cx="22" cy="27" rx="2" ry="2" fill="#18080a"/>
        <ellipse cx="38" cy="27" rx="3.5" ry="2.5" fill="white"/>
        <ellipse cx="38" cy="27" rx="2" ry="2" fill="#18080a"/>
        {/* Nose */}
        <circle cx="27.5" cy="34" r="1.8" fill={skin} stroke="#00000025" strokeWidth="1"/>
        <circle cx="32.5" cy="34" r="1.8" fill={skin} stroke="#00000025" strokeWidth="1"/>
        {/* Mouth */}
        <path d="M24 39.5 Q30 43.5 36 39.5" stroke="#7B2A1A" strokeWidth="2.2" fill="none" strokeLinecap="round"/>
        {/* Beard (on top) */}
        {beardEl}
        {/* Hair cap – draw the top of hair over any face bleed */}
        {hairEl && React.cloneElement(<g opacity="1">{hairEl}</g>)}
      </svg>
      <span className="sg-face-label">{label}</span>
    </div>
  )
}

/* ─── Glasses SVG card ────────────────────────────────────── */
function GlassesCard({ type, label, badge }) {
  const frames = {
    'Rectangular': <><rect x="5"  y="18" width="20" height="13" rx="2" fill="none" stroke="currentColor" strokeWidth="2.5"/><rect x="35" y="18" width="20" height="13" rx="2" fill="none" stroke="currentColor" strokeWidth="2.5"/><line x1="25" y1="24" x2="35" y2="24" stroke="currentColor" strokeWidth="2"/></>,
    'Square':      <><rect x="5"  y="17" width="21" height="16" rx="2" fill="none" stroke="currentColor" strokeWidth="2.5"/><rect x="34" y="17" width="21" height="16" rx="2" fill="none" stroke="currentColor" strokeWidth="2.5"/><line x1="26" y1="25" x2="34" y2="25" stroke="currentColor" strokeWidth="2"/></>,
    'Round':       <><circle cx="16" cy="25" r="11" fill="none" stroke="currentColor" strokeWidth="2.5"/><circle cx="44" cy="25" r="11" fill="none" stroke="currentColor" strokeWidth="2.5"/><line x1="27" y1="25" x2="33" y2="25" stroke="currentColor" strokeWidth="2"/></>,
    'Oval':        <><ellipse cx="16" cy="25" rx="12" ry="9" fill="none" stroke="currentColor" strokeWidth="2.5"/><ellipse cx="44" cy="25" rx="12" ry="9" fill="none" stroke="currentColor" strokeWidth="2.5"/><line x1="28" y1="25" x2="32" y2="25" stroke="currentColor" strokeWidth="2"/></>,
    'Wayfarer':    <><path d="M5 17 L26 17 L26 31 Q26 33 16 33 Q6 33 5 31 Z" fill="none" stroke="currentColor" strokeWidth="2.5"/><path d="M34 17 L55 17 L55 31 Q55 33 44 33 Q34 33 34 31 Z" fill="none" stroke="currentColor" strokeWidth="2.5"/><line x1="26" y1="24" x2="34" y2="24" stroke="currentColor" strokeWidth="2"/></>,
    'Clubmaster':  <><path d="M5 20 L26 20 L26 31 Q16 35 5 31 Z" fill="none" stroke="currentColor" strokeWidth="2.5"/><rect x="5" y="19" width="21" height="5" rx="1" fill="currentColor" opacity="0.5"/><path d="M34 20 L55 20 L55 31 Q44 35 34 31 Z" fill="none" stroke="currentColor" strokeWidth="2.5"/><rect x="34" y="19" width="21" height="5" rx="1" fill="currentColor" opacity="0.5"/><line x1="26" y1="23" x2="34" y2="23" stroke="currentColor" strokeWidth="2"/></>,
    'Rimless':     <><ellipse cx="16" cy="25" rx="11" ry="8" fill="none" stroke="currentColor" strokeWidth="1.5" strokeDasharray="3 2"/><ellipse cx="44" cy="25" rx="11" ry="8" fill="none" stroke="currentColor" strokeWidth="1.5" strokeDasharray="3 2"/><line x1="27" y1="25" x2="33" y2="25" stroke="currentColor" strokeWidth="1.5"/></>,
    'Aviators':    <><path d="M4 19 Q16 15 28 24 Q16 33 4 29 Z" fill="none" stroke="currentColor" strokeWidth="2.5"/><path d="M32 24 Q44 15 56 19 L56 29 Q44 33 32 24 Z" fill="none" stroke="currentColor" strokeWidth="2.5"/><line x1="28" y1="24" x2="32" y2="24" stroke="currentColor" strokeWidth="2"/></>,
    'Light Frame': <><rect x="5" y="18" width="20" height="13" rx="3" fill="none" stroke="currentColor" strokeWidth="1.5"/><rect x="35" y="18" width="20" height="13" rx="3" fill="none" stroke="currentColor" strokeWidth="1.5"/><line x1="25" y1="24" x2="35" y2="24" stroke="currentColor" strokeWidth="1.5"/></>,
    'Wide Frame':  <><rect x="3" y="16" width="24" height="16" rx="3" fill="none" stroke="currentColor" strokeWidth="2.5"/><rect x="33" y="16" width="24" height="16" rx="3" fill="none" stroke="currentColor" strokeWidth="2.5"/><line x1="27" y1="24" x2="33" y2="24" stroke="currentColor" strokeWidth="2"/></>,
    'Cat-eye':     <><path d="M5 24 Q8 16 22 18 L26 30 Q16 34 5 28 Z" fill="none" stroke="currentColor" strokeWidth="2.5"/><path d="M34 30 L38 18 Q52 16 55 24 L55 28 Q44 34 34 30 Z" fill="none" stroke="currentColor" strokeWidth="2.5"/><line x1="26" y1="24" x2="34" y2="24" stroke="currentColor" strokeWidth="2"/></>,
  }
  const frame = frames[type] || frames['Rectangular']
  return (
    <div className="sg-face-card">
      {badge && <div className="sg-face-badge" style={{ background: 'var(--green-bg)', color: 'var(--green)' }}>✓ Best</div>}
      <div className="sg-glasses-wrap">
        <svg viewBox="0 0 60 48" width={80} height={64} color="var(--blue)" style={{ opacity: 0.9 }}>
          <rect x="0" y="0" width="60" height="48" fill="#0d1117" rx="6"/>
          {/* Temples */}
          <line x1="0" y1="24" x2="5" y2="24" stroke="currentColor" strokeWidth="2"/>
          <line x1="55" y1="24" x2="60" y2="24" stroke="currentColor" strokeWidth="2"/>
          {frame}
        </svg>
      </div>
      <span className="sg-face-label">{label}</span>
    </div>
  )
}

/* ─── Shared section card wrapper ────────────────────────── */
function SCard({ title, badge, conf, desc, children, tip }) {
  return (
    <div className="sg2-card">
      <div className="sg2-card-head">
        <div className="sg2-card-title">{title}</div>
        <div className="sg2-card-badges">
          {badge && <span className="sg2-best-badge">✦ Best Match</span>}
          {conf && <span className="sg2-conf">{conf}</span>}
        </div>
      </div>
      {desc && <p className="sg2-card-desc">{desc}</p>}
      <div className="sg2-card-body">{children}</div>
      {tip && (
        <div className="sg2-tip">
          <span>💡</span> {tip}
        </div>
      )}
    </div>
  )
}

/* ─── Men's Guide ─────────────────────────────────────────── */
function MenGuide({ men, faceShape, skinCode }) {
  const hairList = (men.hairstyles || []).slice(0, 5)
  const beardList = BEARD_MAP[faceShape] || BEARD_MAP.Oval
  const glassList = GLASSES_MAP[faceShape] || GLASSES_MAP.Oval
  const hairColors = men.hairColors || []
  const colorPalette = men.colorPalette || {}
  const bestColors  = colorPalette.best || []
  const neutrals    = colorPalette.neutrals || []
  const avoid       = colorPalette.avoid || []

  const proTips = [
    { icon: '⚖️', title: 'Enhance Balance', color: 'var(--green)',  text: (men.groomingTips || [])[0] || 'Strategic grooming can enhance balance — a well-shaped beard can compensate for asymmetry.' },
    { icon: '🧔', title: 'Add Definition',  color: 'var(--blue)',   text: (men.groomingTips || [])[1] || 'A shaped beard or goatee can add definition and structure to your jawline.' },
    { icon: '👁️', title: 'Eye Focus',       color: 'var(--purple)', text: (men.groomingTips || [])[2] || 'A subtle center brow groom helps draw eyes inward for a balanced appearance.' },
    { icon: '💧', title: 'Stay Hydrated',   color: 'var(--teal)',   text: 'Daily moisturizing keeps skin healthy and enhances your natural complexion.' },
    { icon: '☀️', title: 'Sun Protection',  color: 'var(--yellow)', text: 'Daily SPF protects your skin and helps maintain a youthful, healthy appearance.' },
  ]

  return (
    <div className="sg2-men-wrap">
      {/* Row 1: Beard + Hair */}
      <div className="sg2-two-col">
        <SCard
          title="🧔 Beard Style"
          badge conf="Confidence 92%"
          desc={men.beardStyle}
          tip="Keeps the face looking sharper and more defined."
        >
          <div className="sg2-thumb-row">
            {beardList.map((b, i) => (
              <FaceCard key={b} hairStyle="High Fade" beardType={b} label={b} badge={i === 0} skinCode={skinCode} />
            ))}
          </div>
        </SCard>

        <SCard
          title="💈 Hairstyle Recommendations"
          badge conf="Confidence 94%"
          desc={`Styles that work best for your ${faceShape} face shape.`}
          tip="Adds height and definition, creating a more balanced look."
        >
          <div className="sg2-thumb-row">
            {hairList.map((h, i) => (
              <FaceCard
                key={h}
                hairStyle={h}
                beardType={null}
                label={h}
                badge={i === 0}
                badgeColor={i === hairList.length - 1 && hairList.length === 5 ? 'avoid' : null}
                skinCode={skinCode}
              />
            ))}
          </div>
        </SCard>
      </div>

      {/* Row 2: Glasses + Grooming */}
      <div className="sg2-two-col">
        <SCard
          title="👓 Glasses Recommendations"
          badge conf="Confidence 90%"
          desc={men.glasses}
          tip="Stronger frame shapes add contrast and structure to your face."
        >
          <div className="sg2-thumb-row">
            {glassList.map((g, i) => (
              <GlassesCard key={g} type={g} label={g} badge={i === 0} />
            ))}
          </div>
        </SCard>

        <SCard
          title="✨ Grooming Suggestions"
          conf="Confidence 93%"
          tip="Consistent grooming enhances your natural features."
        >
          <div className="sg2-grooming-grid">
            {(men.groomingTips || []).map((tip, i) => (
              <div key={i} className="sg2-grooming-item">
                <span className="sg2-groom-icon">
                  {['🧔','🪥','💧','🛡','💦','😴'][i] || '✦'}
                </span>
                <span>{tip}</span>
              </div>
            ))}
          </div>
        </SCard>
      </div>

      {/* Row 3: Hair Color + Clothing */}
      <div className="sg2-two-col">
        <SCard
          title="🎨 Hair Color Suggestions"
          conf="Confidence 88%"
          desc="Natural shades that complement your skin tone."
          tip="Choose colors that enhance your overall appearance."
        >
          <div className="sg2-hair-colors">
            {hairColors.map((c, i) => (
              <div key={c} className="sg2-hair-color-item">
                <div className="sg2-hair-swatch" style={{ background: resolveHex(c) }}>
                  {i === 0 && <div className="sg2-swatch-best">Best ✓</div>}
                </div>
                <span className="sg2-hair-color-name">{c}</span>
              </div>
            ))}
          </div>
        </SCard>

        <SCard
          title="🌈 Clothing Color Palette"
          conf="Confidence 91%"
          desc={colorPalette.tip || 'Colors that enhance your natural look and skin tone.'}
          tip="Wear these colors to look your best and stand out."
        >
          <div className="sg2-colors-section">
            <div className="sg2-colors-label">Best Colors</div>
            <div className="sg2-colors-dots">
              {bestColors.map(c => (
                <div key={c} className="sg2-color-dot-wrap">
                  <div className="sg2-color-dot" style={{ background: resolveHex(c) }} title={c}/>
                  <span className="sg2-color-dot-name">{c}</span>
                </div>
              ))}
            </div>
            <div className="sg2-colors-label" style={{ marginTop: 10 }}>Neutrals</div>
            <div className="sg2-colors-dots">
              {neutrals.map(c => (
                <div key={c} className="sg2-color-dot-wrap">
                  <div className="sg2-color-dot" style={{ background: resolveHex(c) }} title={c}/>
                  <span className="sg2-color-dot-name">{c}</span>
                </div>
              ))}
            </div>
            {avoid.length > 0 && (
              <div className="sg2-avoid-row">
                <span className="sg2-avoid-badge">Avoid</span>
                <span className="sg2-avoid-text">{avoid.join(', ')}</span>
              </div>
            )}
          </div>
        </SCard>
      </div>

      {/* Pro Tips */}
      <div className="sg2-pro-tips-section">
        <div className="sg2-pro-tips-title">⭐ Additional Pro Tips</div>
        <div className="sg2-pro-tips-grid">
          {proTips.map(pt => (
            <div key={pt.title} className="sg2-pro-tip-card">
              <div className="sg2-pro-tip-icon" style={{ color: pt.color }}>{pt.icon}</div>
              <div className="sg2-pro-tip-name" style={{ color: pt.color }}>{pt.title}</div>
              <div className="sg2-pro-tip-text">{pt.text}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

/* ─── Women's Guide ───────────────────────────────────────── */
function WomenGuide({ women, faceShape, skinCode }) {
  const makeup       = women.makeup || {}
  const hairstyles   = women.hairstyles || []
  const hairColors   = women.hairColors || []
  const colorPalette = women.colorPalette || {}
  const bestColors   = colorPalette.best || []
  const neutrals     = colorPalette.neutrals || []
  const avoid        = colorPalette.avoid || []

  const WOMEN_GLASSES_MAP = {
    Oval:'Cat-eye', Round:'Rectangular', Square:'Round',
    Heart:'Light Frame', Diamond:'Oval', Oblong:'Wide Frame',
  }
  const wGlassList = [WOMEN_GLASSES_MAP[faceShape] || 'Oval', 'Round', 'Cat-eye', 'Rimless']

  return (
    <div className="sg2-men-wrap">
      {/* Row 1: Makeup + Eyebrows+Hair */}
      <div className="sg2-two-col">
        <SCard
          title="💄 Makeup Recommendations"
          badge conf="Confidence 92%"
          desc={`Tailored for your ${faceShape} face shape.`}
          tip="Start with a good base that matches your skin tone perfectly."
        >
          <div className="sg2-makeup-grid">
            {Object.entries(makeup).map(([k, v]) => (
              <div key={k} className="sg2-makeup-item">
                <div className="sg2-makeup-key">{k.charAt(0).toUpperCase() + k.slice(1)}</div>
                <div className="sg2-makeup-val">{v}</div>
              </div>
            ))}
          </div>
        </SCard>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          <SCard
            title="🖊️ Eyebrow Shape"
            conf="Confidence 90%"
            tip="Well-shaped brows frame the face beautifully."
          >
            <p className="sg2-card-desc" style={{ marginTop: 0 }}>{women.eyebrowShape}</p>
          </SCard>

          <SCard
            title="💇‍♀️ Hairstyle Recommendations"
            badge conf="Confidence 94%"
            desc={`Best styles for your ${faceShape} face shape.`}
            tip="Layers around the face can enhance your natural bone structure."
          >
            <div className="sg2-thumb-row">
              {hairstyles.slice(0, 4).map((h, i) => (
                <FaceCard key={h} hairStyle={h} beardType={null} label={h} badge={i === 0} skinCode={skinCode} />
              ))}
            </div>
          </SCard>
        </div>
      </div>

      {/* Row 2: Glasses + Hair Color */}
      <div className="sg2-two-col">
        <SCard
          title="👓 Glasses Recommendations"
          badge conf="Confidence 90%"
          desc={women.glasses}
          tip="Choose frames that contrast with your face shape."
        >
          <div className="sg2-thumb-row">
            {wGlassList.map((g, i) => (
              <GlassesCard key={g} type={g} label={g} badge={i === 0} />
            ))}
          </div>
        </SCard>

        <SCard
          title="🎨 Hair Color Suggestions"
          conf="Confidence 88%"
          desc="Shades that complement your skin tone beautifully."
          tip="Choose colors that enhance your overall appearance."
        >
          <div className="sg2-hair-colors">
            {hairColors.map((c, i) => (
              <div key={c} className="sg2-hair-color-item">
                <div className="sg2-hair-swatch" style={{ background: resolveHex(c) }}>
                  {i === 0 && <div className="sg2-swatch-best">Best ✓</div>}
                </div>
                <span className="sg2-hair-color-name">{c}</span>
              </div>
            ))}
          </div>
        </SCard>
      </div>

      {/* Row 3: Color Palette */}
      <SCard
        title="🌈 Clothing Color Palette"
        conf="Confidence 91%"
        desc={colorPalette.tip}
        tip="Wear these colors to look your best and let your features shine."
      >
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 24 }}>
          <div>
            <div className="sg2-colors-label">Best Colors</div>
            <div className="sg2-colors-dots">
              {bestColors.map(c => (
                <div key={c} className="sg2-color-dot-wrap">
                  <div className="sg2-color-dot" style={{ background: resolveHex(c) }}/>
                  <span className="sg2-color-dot-name">{c}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <div className="sg2-colors-label">Neutrals</div>
            <div className="sg2-colors-dots">
              {neutrals.map(c => (
                <div key={c} className="sg2-color-dot-wrap">
                  <div className="sg2-color-dot" style={{ background: resolveHex(c) }}/>
                  <span className="sg2-color-dot-name">{c}</span>
                </div>
              ))}
            </div>
          </div>
          {avoid.length > 0 && (
            <div>
              <div className="sg2-avoid-row">
                <span className="sg2-avoid-badge">Avoid</span>
                <span className="sg2-avoid-text">{avoid.join(', ')}</span>
              </div>
            </div>
          )}
        </div>
      </SCard>
    </div>
  )
}

/* ─── Main export ─────────────────────────────────────────── */
export default function StyleGuide({ styleData, defaultGender }) {
  const initialMode = defaultGender === 'male' ? 'men' : defaultGender === 'female' ? 'women' : null
  const [mode, setMode] = useState(initialMode)

  if (!styleData) return null

  const { men, women } = styleData
  const faceShape = (mode === 'men' ? men?.basedOn?.faceShape : women?.basedOn?.faceShape) || 'Oval'
  const skinToneStr = (mode === 'men' ? men?.basedOn?.skinTone : women?.basedOn?.skinTone) || 'Fitzpatrick IV'
  const skinCode = parseSkin(skinToneStr)
  const symmetry = (mode === 'men' ? men?.basedOn?.symmetry : null)

  return (
    <div className="sg2-wrap fade-up">
      {/* Header */}
      <div className="sg2-header">
        <div>
          <div className="sg2-title">✨ Personalized Style Guide</div>
          <div className="sg2-sub">AI-curated recommendations based on your facial analysis</div>
        </div>
      </div>

      {/* Gender toggle */}
      <div className="sg2-gender-row">
        <button className={`sg2-gender-btn ${mode === 'women' ? 'active women' : ''}`} onClick={() => setMode('women')}>
          👩 Women
        </button>
        <button className={`sg2-gender-btn ${mode === 'men' ? 'active men' : ''}`} onClick={() => setMode('men')}>
          🧔 Men
        </button>
      </div>

      {/* Based-on banner */}
      {mode && (
        <div className="sg2-based-banner">
          <span>🎯 Based on your</span>
          <strong> {faceShape} </strong> face shape ·
          <strong> {skinToneStr} </strong>
          {symmetry ? <>· Symmetry: <strong>{symmetry}%</strong></> : null}
          <span className="sg2-hmc-badge">✦ High Match Confidence</span>
        </div>
      )}

      {/* Gender prompt */}
      {!mode && (
        <div className="sg2-prompt">Select Women or Men above to reveal your personalised guide.</div>
      )}

      {/* Content */}
      {mode === 'men'   && men   && <MenGuide   men={men}     faceShape={faceShape} skinCode={skinCode} />}
      {mode === 'women' && women && <WomenGuide  women={women} faceShape={faceShape} skinCode={skinCode} />}

      {/* Disclaimer */}
      <p className="sg2-disclaimer">
        ℹ️ Disclaimer: This report is for style and grooming guidance only. Not medical or identity assessment.
        Results are based on AI analysis and may vary with lighting, angle and photo quality.
      </p>
    </div>
  )
}
