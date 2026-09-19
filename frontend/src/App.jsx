import { useState, useEffect } from 'react'
import FragranceCard from './FragranceCard'
import Stats from './Stats'
import { API_URL } from './config'
import './App.css'

function App() {
  const [fragrances, setFragrances] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_URL}/fragrances`)
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

  return (
    <>
      <header className="hero">
        <p className="eyebrow">Personal data project</p>
        <h1>FragBro</h1>
        <p className="hero-copy">
          I built FragBro to track what I actually wear, not just what sits in
          my fragrance collection.
        </p>
        <p className="hero-detail">
          It started as a local command-line tool and grew into a small
          full-stack app using FastAPI, React and SQLite. The public site is
          read-only; collection changes and wear logging stay local.
        </p>
        <div className="project-links">
          <a href="https://github.com/abdullahnyle/FragBro" target="_blank" rel="noreferrer">
            View source
          </a>
          <a href={`${API_URL}/docs`} target="_blank" rel="noreferrer">
            API docs
          </a>
        </div>
      </header>

      <section className="project-summary" aria-label="Project summary">
        <div>
          <span>Stack</span>
          <strong>FastAPI + React + SQLite</strong>
        </div>
        <div>
          <span>Data model</span>
          <strong>7 linked tables</strong>
        </div>
        <div>
          <span>Public demo</span>
          <strong>Read-only snapshot</strong>
        </div>
      </section>

      <main className="content">
        <section>
          <p className="section-label">Collection analytics</p>
          <Stats />
        </section>

        <section>
          <p className="catalog-label">Catalog</p>
          {loading && <p className="loading-state">Loading catalog...</p>}
          {error && <p className="error-state">Error loading catalog: {error}</p>}
          {!loading && !error && (
            <div className="frag-grid">
              {fragrances.map(frag => (
                <FragranceCard key={frag.id} frag={frag} />
              ))}
            </div>
          )}
        </section>
      </main>

      <footer className="site-footer">
        Built around a fixed demo snapshot of my own collection and wear history.
      </footer>
    </>
  )
}

export default App