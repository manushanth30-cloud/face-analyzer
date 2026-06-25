import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'

const MAX_SIZE = 10 * 1024 * 1024  // 10 MB

export default function UploadZone({ onAnalyze, onOpenCamera, loading, serverError }) {
  const [preview, setPreview]   = useState(null)
  const [file,    setFile]      = useState(null)
  const [error,   setError]     = useState('')

  const onDrop = useCallback((accepted, rejected) => {
    setError('')
    if (rejected.length > 0) {
      const err = rejected[0].errors[0]
      if (err.code === 'file-too-large')    setError('File too large. Max 10 MB.')
      if (err.code === 'file-invalid-type') setError('Only JPG, PNG, or WEBP files allowed.')
      return
    }
    if (accepted.length > 0) {
      const f = accepted[0]
      setFile(f)
      setPreview(URL.createObjectURL(f))
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/jpeg': [], 'image/png': [], 'image/webp': [] },
    maxSize: MAX_SIZE,
    multiple: false,
  })

  const handleAnalyze = () => {
    if (!file) { setError('Please select a photo first.'); return }
    onAnalyze(file)
  }

  const displayError = error || serverError

  return (
    <div className="upload-page fade-up">
      {/* Title */}
      <div className="upload-title">
        <h1>Asthetica</h1>
        <p>AI-powered face insights for grooming &amp; style</p>
      </div>

      {/* Two input options */}
      {!preview && (
        <div className="upload-options">
          {/* Camera button */}
          <button
            id="open-camera-btn"
            className="camera-option-btn"
            onClick={onOpenCamera}
          >
            <span className="camera-option-icon">📷</span>
            <span className="camera-option-label">Take Selfie</span>
            <span className="camera-option-sub">Use your camera</span>
          </button>

          <div className="upload-or">
            <span>or</span>
          </div>

          {/* Drop zone */}
          <div
            {...getRootProps()}
            className={`dropzone-card ${isDragActive ? 'active' : ''}`}
            style={{ width: '100%', maxWidth: 380 }}
          >
            <input {...getInputProps()} id="photo-upload" />
            <svg className="dropzone-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.338-2.32 5.75 5.75 0 0 1 1.632 10.908" />
            </svg>
            <div className="dropzone-text">
              <strong>Drag &amp; drop your photo</strong>
              <p style={{ marginTop: 4 }}>or <strong>click to browse</strong></p>
            </div>
            <p className="dropzone-formats">JPG · PNG · WEBP · Max 10 MB</p>
          </div>
        </div>
      )}

      {/* Preview after file selected */}
      {preview && (
        <div className="preview-wrap" style={{ maxWidth: 380, width: '100%' }}>
          <img src={preview} alt="Preview" />
        </div>
      )}

      {displayError && <div className="upload-error">{displayError}</div>}

      {/* Analyze / Remove buttons */}
      {preview && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12, width: '100%', maxWidth: 380 }}>
          <button
            id="analyze-btn"
            className="btn btn-primary"
            style={{ width: '100%', justifyContent: 'center', padding: '12px', fontSize: '1rem' }}
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? (
              <><span style={{ animation: 'pulse 1s infinite' }}>●</span> Uploading…</>
            ) : (
              <><span>✦</span> Analyze My Features</>
            )}
          </button>
          <button
            className="btn btn-ghost"
            style={{ fontSize: '0.8rem', padding: '6px 14px' }}
            onClick={() => { setPreview(null); setFile(null); setError('') }}
          >
            Remove photo
          </button>
        </div>
      )}

      {/* Info */}
      {!preview && (
        <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textAlign: 'center', maxWidth: 380 }}>
          For best results use a clear front-facing photo with good lighting.
          No data is stored — analysis happens in real time.
        </p>
      )}
    </div>
  )
}
