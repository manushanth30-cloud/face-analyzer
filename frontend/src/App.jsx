import React, { useState } from 'react'
import axios from 'axios'
import './index.css'
import UploadZone       from './components/UploadZone'
import ScanAnimation    from './components/ScanAnimation'
import ResultsDashboard from './components/ResultsDashboard'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const STATES = { UPLOAD: 'UPLOAD', SCANNING: 'SCANNING', RESULTS: 'RESULTS' }

export default function App() {
  const [screen,   setScreen]   = useState(STATES.UPLOAD)
  const [imageUrl, setImageUrl] = useState(null)
  const [results,  setResults]  = useState(null)
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
      setScreen(STATES.RESULTS)
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        err.message ||
        'Analysis failed. Please try a clearer front-facing photo.'
      setError(msg)
      setScreen(STATES.UPLOAD)
    }
  }

  const handleReset = () => {
    setScreen(STATES.UPLOAD)
    setResults(null)
    setImageUrl(null)
    setError('')
  }

  return (
    <>
      {screen === STATES.UPLOAD && (
        <UploadZone
          onAnalyze={handleAnalyze}
          loading={false}
          serverError={error}
        />
      )}
      {screen === STATES.SCANNING && (
        <ScanAnimation imageUrl={imageUrl} />
      )}
      {screen === STATES.RESULTS && results && (
        <ResultsDashboard
          data={results}
          imageUrl={imageUrl}
          onReset={handleReset}
        />
      )}
    </>
  )
}
