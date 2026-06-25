import React, { useState } from 'react'
import axios from 'axios'
import './index.css'
import UploadZone       from './components/UploadZone'
import ScanAnimation    from './components/ScanAnimation'
import ResultsDashboard from './components/ResultsDashboard'
import CameraCapture    from './components/CameraCapture'
import GenderSelect     from './components/GenderSelect'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const STATES = {
  UPLOAD:  'UPLOAD',
  CAMERA:  'CAMERA',
  SCANNING:'SCANNING',
  GENDER:  'GENDER',
  RESULTS: 'RESULTS',
}

export default function App() {
  const [screen,   setScreen]   = useState(STATES.UPLOAD)
  const [imageUrl, setImageUrl] = useState(null)
  const [results,  setResults]  = useState(null)
  const [gender,   setGender]   = useState(null)   // 'male' | 'female'
  const [error,    setError]    = useState('')

  const handleAnalyze = async (file) => {
    setError('')
    setImageUrl(URL.createObjectURL(file))
    setScreen(STATES.SCANNING)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const { data } = await axios.post(`${API_URL}/analyze`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      })
      setResults(data)
      setScreen(STATES.GENDER)   // ← ask gender before showing results
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        err.message ||
        'Analysis failed. Please try a clearer front-facing photo.'
      setError(msg)
      setScreen(STATES.UPLOAD)
    }
  }

  const handleGenderSelect = (g) => {
    setGender(g)
    setScreen(STATES.RESULTS)
  }

  const handleReset = () => {
    setScreen(STATES.UPLOAD)
    setResults(null)
    setImageUrl(null)
    setGender(null)
    setError('')
  }

  return (
    <>
      {screen === STATES.UPLOAD && (
        <UploadZone
          onAnalyze={handleAnalyze}
          onOpenCamera={() => setScreen(STATES.CAMERA)}
          loading={false}
          serverError={error}
        />
      )}
      {screen === STATES.CAMERA && (
        <CameraCapture
          onCapture={(file) => handleAnalyze(file)}
          onCancel={() => setScreen(STATES.UPLOAD)}
        />
      )}
      {screen === STATES.SCANNING && (
        <ScanAnimation imageUrl={imageUrl} />
      )}
      {screen === STATES.GENDER && (
        <GenderSelect
          imageUrl={imageUrl}
          onSelect={handleGenderSelect}
        />
      )}
      {screen === STATES.RESULTS && (
        <ResultsDashboard
          data={results}
          imageUrl={imageUrl}
          gender={gender}
          onReset={handleReset}
        />
      )}
    </>
  )
}
