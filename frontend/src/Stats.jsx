import { useState, useEffect } from 'react'
import { API_URL } from './config'
function Stats() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  useEffect(() => {
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
  const topWorn = stats.most_worn_all_time[0]
  const mostNeglected = [...stats.days_since_last_worn]
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
          <h3>Longest untouched</h3>
          <ol>
            {[...stats.days_since_last_worn]
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
    </div>
  )
}
export default Stats