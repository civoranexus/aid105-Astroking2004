import React, { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { getSchemes, getRecommendations, Scheme } from './api'
import SchemeList from './pages/SchemeList'
import SchemeDetail from './pages/SchemeDetail'

export default function App() {
  const [schemes, setSchemes] = useState<Scheme[]>([])
  const [loading, setLoading] = useState(false)
  const [userAge, setUserAge] = useState<number | ''>('')
  const [results, setResults] = useState<Scheme[] | null>(null)

  useEffect(() => {
    getSchemes().then(setSchemes).catch(() => setSchemes([]))
  }, [])

  async function onRecommend(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    try {
      const user = { age: userAge === '' ? undefined : Number(userAge) }
      const recs = await getRecommendations(user)
      setResults(recs)
    } catch (err) {
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <BrowserRouter>
      <div className="app">
        <header>
          <h1>
            <Link to="/">SchemeAssist</Link>
          </h1>
          <p>Browse schemes and get recommendations.</p>
        </header>

        <Routes>
          <Route
            path="/"
            element={
              <main>
                <section>
                  <h2>Available schemes</h2>
                  <SchemeList schemes={schemes} />
                </section>

                <section>
                  <h2>Get Recommendations</h2>
                  <form onSubmit={onRecommend} className="form">
                    <label>
                      Age:
                      <input
                        type="number"
                        value={userAge}
                        onChange={(e) => setUserAge(e.target.value === '' ? '' : Number(e.target.value))}
                        min={0}
                      />
                    </label>
                    <button type="submit" disabled={loading}>
                      {loading ? 'Thinking...' : 'Recommend'}
                    </button>
                  </form>

                  {results && (
                    <div>
                      <h3>Recommendations</h3>
                      {results.length === 0 ? (
                        <p>No recommendations.</p>
                      ) : (
                        <ul>
                          {results.map((r) => (
                            <li key={r.id}>
                              <strong>{r.name}</strong>
                              <div className="muted">{r.description}</div>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  )}
                </section>
              </main>
            }
          />

          <Route path="/schemes/:id" element={<SchemeDetail schemes={schemes} />} />
        </Routes>

        <footer>
          <small>Local dev mode — proxy `/api` to backend.</small>
        </footer>
      </div>
    </BrowserRouter>
  )
}
