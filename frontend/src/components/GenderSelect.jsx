import React, { useState } from 'react'

export default function GenderSelect({ imageUrl, onSelect }) {
  const [hovered, setHovered] = useState(null)

  return (
    <div className="gender-page fade-up">

      {/* Header */}
      <div className="gender-header">
        <div className="gender-logo">✦</div>
        <h1 className="gender-title">One Quick Step</h1>
        <p className="gender-sub">
          Select your gender to personalise your Style Guide
        </p>
      </div>

      {/* Photo thumbnail */}
      {imageUrl && (
        <div className="gender-photo-wrap">
          <img src={imageUrl} alt="Your photo" className="gender-photo" />
          <div className="gender-photo-label">Analysis Complete</div>
        </div>
      )}

      {/* Gender cards */}
      <div className="gender-cards">

        {/* Male */}
        <button
          className={`gender-card gender-male ${hovered === 'male' ? 'hovered' : ''}`}
          onClick={() => onSelect('male')}
          onMouseEnter={() => setHovered('male')}
          onMouseLeave={() => setHovered(null)}
        >
          <div className="gender-card-icon">🧔</div>
          <div className="gender-card-label">Male</div>
          <div className="gender-card-features">
            <span>🧔 Beard Styles</span>
            <span>💈 Hairstyles</span>
            <span>👓 Glasses</span>
            <span>✨ Grooming Tips</span>
          </div>
          <div className="gender-card-cta">Select →</div>
        </button>

        {/* Female */}
        <button
          className={`gender-card gender-female ${hovered === 'female' ? 'hovered' : ''}`}
          onClick={() => onSelect('female')}
          onMouseEnter={() => setHovered('female')}
          onMouseLeave={() => setHovered(null)}
        >
          <div className="gender-card-icon">💄</div>
          <div className="gender-card-label">Female</div>
          <div className="gender-card-features">
            <span>💄 Makeup Guide</span>
            <span>🖊️ Eyebrow Shape</span>
            <span>💇‍♀️ Hairstyles</span>
            <span>🌈 Colour Palette</span>
          </div>
          <div className="gender-card-cta">Select →</div>
        </button>

      </div>

      <p className="gender-note">
        This is used only to personalise your style recommendations.
      </p>
    </div>
  )
}
