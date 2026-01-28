import React, { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { getSchemes, getRecommendations, Scheme } from './api'
import SchemeList from './pages/SchemeList'
import SchemeDetail from './pages/SchemeDetail'

export default function App() {
  const [schemes, setSchemes] = useState<Scheme[]>([])
  const [loading, setLoading] = useState(false)
  const [userIncome, setUserIncome] = useState<number | ''>('')
  const [userState, setUserState] = useState<string>('')
  const [userNeedsText, setUserNeedsText] = useState<string>('')
  const [results, setResults] = useState<Scheme[] | null>(null)

  useEffect(() => {
    getSchemes().then(setSchemes).catch(() => setSchemes([]))
  }, [])

  async function onRecommend(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    try {
      const user = {
        income: userIncome === '' ? undefined : Number(userIncome),
        state: userState ? userState : undefined,
        needs: userNeedsText
          ? userNeedsText
              .split(',')
              .map((s) => s.trim())
              .filter(Boolean)
          : []
      }
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
          <div className="header-left">
            <img src="/logos/short_logo.png" alt="SchemeAssist" className="logo" />
            <h1>
              <Link to="/">SchemeAssist</Link>
            </h1>
          </div>
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
                  <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1rem' }}>
                    Fill in your details to find schemes that match your profile. All fields are optional.
                  </p>
                  <form onSubmit={onRecommend} className="form">
                    <label>
                      Annual Income (₹):
                      <input
                        type="number"
                        value={userIncome}
                        onChange={(e) => setUserIncome(e.target.value === '' ? '' : Number(e.target.value))}
                        min={0}
                        placeholder="e.g. 50000"
                      />
                      <small style={{ fontSize: '0.8rem', color: '#888' }}>Optional - helps filter by income eligibility</small>
                    </label>
                    <label>
                      State:
                      <input
                        type="text"
                        value={userState}
                        onChange={(e) => setUserState(e.target.value)}
                        placeholder="e.g. Karnataka, Tamil Nadu"
                      />
                      <small style={{ fontSize: '0.8rem', color: '#888' }}>Optional - filters schemes available in your state</small>
                    </label>
                    <label>
                      Your Needs (comma-separated):
                      <input
                        type="text"
                        value={userNeedsText}
                        onChange={(e) => setUserNeedsText(e.target.value)}
                        placeholder="e.g. training, housing, agriculture"
                      />
                      <small style={{ fontSize: '0.8rem', color: '#888' }}>Optional - helps prioritize relevant schemes</small>
                    </label>
                    <button type="submit" disabled={loading}>
                      {loading ? 'Finding Schemes...' : 'Get Recommendations'}
                    </button>
                  </form>

                  {Array.isArray(results) && (
                    <div>
                      <h3>Recommended Schemes ({results.length})</h3>
                      {results.length === 0 ? (
                        <div style={{ padding: '1rem', background: '#fff3cd', borderRadius: '4px', color: '#856404' }}>
                          <strong>No schemes found.</strong> Try adjusting your criteria or leaving some fields blank for broader results.
                        </div>
                      ) : (
                        <div>
                          {results.map((r) => (
                            <div key={r.id} style={{ 
                              marginBottom: '1.5rem', 
                              padding: '1rem', 
                              border: '1px solid #ddd', 
                              borderRadius: '6px',
                              background: '#f9f9f9'
                            }}>
                              <Link to={`/schemes/${r.id}`} style={{ textDecoration: 'none' }}>
                                <h4 style={{ margin: '0 0 0.5rem 0', color: '#0066cc' }}>{r.title}</h4>
                              </Link>
                              
                              <p style={{ fontSize: '0.9rem', color: '#555', marginBottom: '0.75rem' }}>
                                {r.description}
                              </p>
                              
                              <div style={{ marginBottom: '0.5rem' }}>
                                {r.schemeCategory && (
                                  <span style={{ 
                                    fontSize: '0.75rem', 
                                    background: '#e0e0e0', 
                                    padding: '3px 8px', 
                                    borderRadius: '4px', 
                                    marginRight: '6px',
                                    display: 'inline-block'
                                  }}>
                                    📁 {r.schemeCategory}
                                  </span>
                                )}
                                {r.level && (
                                  <span style={{ 
                                    fontSize: '0.75rem', 
                                    background: '#d1e7dd', 
                                    padding: '3px 8px', 
                                    borderRadius: '4px',
                                    display: 'inline-block'
                                  }}>
                                    📍 {r.level}
                                  </span>
                                )}
                              </div>

                              {(r.tags && r.tags.length > 0) && (
                                <div style={{ marginTop: '0.5rem' }}>
                                  <small style={{ color: '#666', fontWeight: '600' }}>Tags: </small>
                                  {r.tags.map((tag: string, idx: number) => (
                                    <span key={idx} style={{ 
                                      fontSize: '0.7rem', 
                                      background: '#fff', 
                                      border: '1px solid #ccc',
                                      padding: '2px 6px', 
                                      borderRadius: '3px', 
                                      marginRight: '4px',
                                      display: 'inline-block',
                                      marginTop: '3px'
                                    }}>
                                      {tag}
                                    </span>
                                  ))}
                                </div>
                              )}

                              {(r.benefits && r.benefits.length > 0) && (
                                <div style={{ marginTop: '0.5rem' }}>
                                  <small style={{ color: '#666', fontWeight: '600' }}>Benefits: </small>
                                  {r.benefits.map((benefit: string, idx: number) => (
                                    <span key={idx} style={{ 
                                      fontSize: '0.7rem', 
                                      background: '#d4edda', 
                                      border: '1px solid #c3e6cb',
                                      padding: '2px 6px', 
                                      borderRadius: '3px', 
                                      marginRight: '4px',
                                      display: 'inline-block',
                                      marginTop: '3px'
                                    }}>
                                      ✓ {benefit}
                                    </span>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
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
