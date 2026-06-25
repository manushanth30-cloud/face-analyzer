import React, { useState } from 'react'
import axios from 'axios'
import { AnimatePresence, motion } from 'framer-motion'
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

const pageVariants = {
  initial: { opacity: 0, y: 15, scale: 0.98 },
  animate: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] } },
  exit:    { opacity: 0, y: -10, scale: 0.98, transition: { duration: 0.3, ease: [0.22, 1, 0.36, 1] } }
}

const PageWrapper = ({ children, keyName }) => (
  <motion.div
    key={keyName}
    variants={pageVariants}
    initial="initial"
    animate="animate"
    exit="exit"
    style={{ width: '100%', display: 'flex', justifyContent: 'center' }}
  >
    {children}
  </motion.div>
)

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
    <AnimatePresence mode="wait">
      {screen === STATES.UPLOAD && (
        <PageWrapper keyName="upload">
          <UploadZone
            onAnalyze={handleAnalyze}
            onOpenCamera={() => setScreen(STATES.CAMERA)}
            loading={false}
            serverError={error}
          />
        </PageWrapper>
      )}
      {screen === STATES.CAMERA && (
        <PageWrapper keyName="camera">
          <CameraCapture
            onCapture={(file) => handleAnalyze(file)}
            onCancel={() => setScreen(STATES.UPLOAD)}
          />
        </PageWrapper>
      )}
      {screen === STATES.SCANNING && (
        <PageWrapper keyName="scanning">
          <ScanAnimation imageUrl={imageUrl} />
        </PageWrapper>
      )}
      {screen === STATES.GENDER && (
        <PageWrapper keyName="gender">
          <GenderSelect
            imageUrl={imageUrl}
            onSelect={handleGenderSelect}
          />
        </PageWrapper>
      )}
      {screen === STATES.RESULTS && (
        <PageWrapper keyName="results">
          <ResultsDashboard
            data={results}
            imageUrl={imageUrl}
            gender={gender}
            onReset={handleReset}
          />
        </PageWrapper>
      )}
    </AnimatePresence>
  )
}
