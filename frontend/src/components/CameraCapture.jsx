import React, { useRef, useState, useEffect, useCallback } from 'react'

export default function CameraCapture({ onCapture, onCancel }) {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const streamRef = useRef(null)

  const [facingMode, setFacingMode] = useState('user') // 'user' = front, 'environment' = back
  const [captured, setCaptured] = useState(null)       // base64 preview after snap
  const [cameraError, setCameraError] = useState('')
  const [countdown, setCountdown] = useState(null)
  const [flashActive, setFlashActive] = useState(false)

  // Start camera
  const startCamera = useCallback(async (mode) => {
    // Stop any existing stream
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop())
    }
    setCameraError('')
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: mode }, width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play().catch(e => console.error("Video play error:", e))
        }
      }
    } catch (err) {
      setCameraError('Camera access denied. Please allow camera permission and try again.')
    }
  }, [])

  useEffect(() => {
    startCamera(facingMode)
    return () => {
      if (streamRef.current) streamRef.current.getTracks().forEach(t => t.stop())
    }
  }, [facingMode, startCamera])

  // Capture frame from video
  const snapPhoto = useCallback(() => {
    const video  = videoRef.current
    const canvas = canvasRef.current
    if (!video || !canvas) return

    canvas.width  = video.videoWidth  || 640
    canvas.height = video.videoHeight || 480
    const ctx = canvas.getContext('2d')

    // Mirror for front camera
    if (facingMode === 'user') {
      ctx.translate(canvas.width, 0)
      ctx.scale(-1, 1)
    }
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    // Flash effect
    setFlashActive(true)
    setTimeout(() => setFlashActive(false), 200)

    const dataUrl = canvas.toDataURL('image/jpeg', 0.92)
    setCaptured(dataUrl)

    // Stop stream after capture
    if (streamRef.current) streamRef.current.getTracks().forEach(t => t.stop())
  }, [facingMode])

  // Countdown then snap
  const startCountdown = useCallback(() => {
    let count = 3
    setCountdown(count)
    const interval = setInterval(() => {
      count -= 1
      if (count === 0) {
        clearInterval(interval)
        setCountdown(null)
        snapPhoto()
      } else {
        setCountdown(count)
      }
    }, 1000)
  }, [snapPhoto])

  // Retake
  const retake = () => {
    setCaptured(null)
    startCamera(facingMode)
  }

  // Confirm — convert base64 to File and pass up
  const confirmCapture = () => {
    const byteStr = atob(captured.split(',')[1])
    const ab = new ArrayBuffer(byteStr.length)
    const ia = new Uint8Array(ab)
    for (let i = 0; i < byteStr.length; i++) ia[i] = byteStr.charCodeAt(i)
    const blob = new Blob([ab], { type: 'image/jpeg' })
    const file = new File([blob], 'selfie.jpg', { type: 'image/jpeg' })
    onCapture(file)
  }

  const flipCamera = () => {
    setFacingMode(m => m === 'user' ? 'environment' : 'user')
    setCaptured(null)
  }

  return (
    <div className="camera-page">
      <div className="camera-header">
        <button className="btn btn-ghost" onClick={onCancel} style={{ padding: '6px 12px' }}>
          ← Back
        </button>
        <div className="camera-title">Take a Selfie</div>
        <button className="btn btn-ghost" onClick={flipCamera} title="Flip camera" style={{ padding: '6px 12px' }}>
          🔄
        </button>
      </div>

      <div className="camera-body">
        {cameraError ? (
          <div className="camera-error">
            <div style={{ fontSize: '2.5rem', marginBottom: 12 }}>📷</div>
            <div>{cameraError}</div>
          </div>
        ) : !captured ? (
          /* Live viewfinder */
          <div className="viewfinder-wrap">
            {flashActive && <div className="camera-flash" />}

            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="viewfinder-video"
              style={{ transform: facingMode === 'user' ? 'scaleX(-1)' : 'none' }}
            />

            {/* Face guide oval */}
            <svg className="face-guide" viewBox="0 0 300 400" preserveAspectRatio="xMidYMid meet">
              <ellipse
                cx="150" cy="190" rx="110" ry="145"
                fill="none"
                stroke="rgba(63,185,80,0.6)"
                strokeWidth="2"
                strokeDasharray="8 4"
              />
            </svg>

            {/* Scan line animation */}
            <div className="camera-scan-line" />

            {/* Countdown overlay */}
            {countdown !== null && (
              <div className="countdown-overlay">{countdown}</div>
            )}

            {/* Corner brackets */}
            <div className="corner tl" /><div className="corner tr" />
            <div className="corner bl" /><div className="corner br" />
          </div>
        ) : (
          /* Preview after capture */
          <div className="preview-captured">
            <img src={captured} alt="Captured selfie" className="captured-img" />
            <div className="preview-badge">✦ Ready to Analyze</div>
          </div>
        )}

        <canvas ref={canvasRef} style={{ display: 'none' }} />

        {/* Controls */}
        {!captured ? (
          <div className="camera-controls">
            <button className="btn btn-ghost" onClick={startCountdown} disabled={countdown !== null} style={{ flex: 1 }}>
              ⏱ {countdown !== null ? `${countdown}…` : '3-sec Timer'}
            </button>
            <button className="shutter-btn" onClick={snapPhoto} title="Take photo">
              <span className="shutter-inner" />
            </button>
            <div style={{ flex: 1 }} />
          </div>
        ) : (
          <div className="camera-controls">
            <button className="btn btn-outline" onClick={retake} style={{ flex: 1 }}>
              ↩ Retake
            </button>
            <button className="btn btn-primary" onClick={confirmCapture} style={{ flex: 1 }}>
              ✦ Analyze →
            </button>
          </div>
        )}

        <p className="camera-hint">
          {captured
            ? 'Tap "Analyze" to run AI facial analysis'
            : 'Position your face inside the oval · Good lighting helps'}
        </p>
      </div>
    </div>
  )
}
