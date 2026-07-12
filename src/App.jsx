import { useState, useEffect } from 'react'
import FragranceCard from './FragranceCard'
import './App.css'

function App() {
  const [fragrances, setFragrances] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/fragrances')
      .then(res => {
        if (!res.ok) throw new Error(`API returned ${res.status}`)
        return res.json()
      })
      .then(data => {
        setFragrances(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <p>Loading fragrances...</p>
  if (error) return <p>Error loading fragrances: {error}</p>

  return (
    <>
      <h1>FragBro</h1>
      <p>Catalog</p>
      {fragrances.map(frag => (
        <FragranceCard key={frag.id} frag={frag} />
      ))}
    </>
  )
}

export default App