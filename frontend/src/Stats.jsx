import { useState, useEffect } from 'react'
import { API_URL } from './config'
import demo from './demo.json'

function Stats() {
  const [stats, setStats] = useState(import.meta.env.PROD ? demo.stats : null)
  const [loading, setLoading] = useState(!import.meta.env.PROD)
  const [error, setError] = useState(null)
  const [openedAt] = useState(() => Date.now())
  useEffect(() => {
    if (import.meta.env.PROD) return

    fetch(`${API_URL}/wear-stats`)
      .then(res => {
        if (!res.ok) throw new Error(`API returned ${res.status}`)
        return res.json()
      })
      .then(data => {
        setStats(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])
  if (loading) return <p>Loading stats...</p>
  if (error) return <p>Error loading stats: {error}</p>
  const daysSinceLastWorn = stats.days_since_last_worn.map(f => ({
    ...f,
    days_ago: Math.max(0, Math.floor(
      (openedAt - Date.parse(`${f.last_worn}T00:00:00Z`)) / 86400000
    )),
  }))
  const topWorn = stats.most_worn_all_time[0]
  const mostNeglected = [...daysSinceLastWorn]
    .sort((a, b) => b.days_ago - a.days_ago)[0]
  return (
    <div className="stats-panel">
      <div className="stats-headline">
        <div className="stat-block">
          <span className="stat-number">{stats.total_wears}</span>
          <span className="stat-label">total wears logged</span>
        </div>
        {topWorn && (
          <div className="stat-block">
            <span className="stat-number">{topWorn.name}</span>
            <span className="stat-label">most worn · {topWorn.wear_count} wears</span>
          </div>
        )}
        {mostNeglected && (
          <div className="stat-block">
            <span className="stat-number">{mostNeglected.days_ago}d</span>
            <span className="stat-label">since {mostNeglected.name} was worn</span>
          </div>
        )}
      </div>
      <div className="stats-lists">
        <div className="stats-list">
          <h3>Most worn</h3>
          {stats.most_worn_all_time.length === 0 && <p>No wears logged yet.</p>}
          <ol>
            {stats.most_worn_all_time.map(f => (
              <li key={`${f.brand}-${f.name}`}>
                <span>{f.name}</span>
                <span className="stat-count">{f.wear_count}</span>
              </li>
            ))}
          </ol>
        </div>
        <div className="stats-list">
          <h3>Days since last logged wear</h3>
          {stats.days_since_last_worn.length === 0 && <p>No dated wear history yet.</p>}
          <ol>
            {[...daysSinceLastWorn]
              .sort((a, b) => b.days_ago - a.days_ago)
              .map(f => (
                <li key={`${f.brand}-${f.name}`}>
                  <span>{f.name}</span>
                  <span className="stat-count">{f.days_ago}d</span>
                </li>
              ))}
          </ol>
        </div>
      </div>
      {stats.owned_but_unworn.length > 0 && (
        <div className="stats-list">
          <h3>Owned with no logged wears</h3>
          <ul>
            {stats.owned_but_unworn.map(f => (
              <li key={`${f.brand}-${f.name}`}>{f.brand} {f.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
export default Stats
