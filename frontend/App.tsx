import React, { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { getSchemes, getRecommendations, Scheme } from './api'
import SchemeList from './pages/SchemeList'
import SchemeDetail from './pages/SchemeDetail'

export default function App() {
  const [allSchemes, setAllSchemes] = useState<Scheme[]>([])
  const [displayedSchemes, setDisplayedSchemes] = useState<Scheme[]>([])
  const [loading, setLoading] = useState(false)
  const [userIncome, setUserIncome] = useState<number | ''>('')
  const [userState, setUserState] = useState<string>('')
  const [userNeedsText, setUserNeedsText] = useState<string>('')
  const [isFiltered, setIsFiltered] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const schemesPerPage = 20

  useEffect(() => {
    getSchemes().then((data) => {
      setAllSchemes(data)
      setDisplayedSchemes(data)
    }).catch(() => {
      setAllSchemes([])
      setDisplayedSchemes([])
    })
  }, [])

  async function onRecommend(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setCurrentPage(1)
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
      setDisplayedSchemes(recs)
      setIsFiltered(true)
    } catch (err) {
      setDisplayedSchemes([])
      setIsFiltered(true)
    } finally {
      setLoading(false)
    }
  }

  function clearFilters() {
    setUserIncome('')
    setUserState('')
    setUserNeedsText('')
    setDisplayedSchemes(allSchemes)
    setIsFiltered(false)
    setCurrentPage(1)
  }

  // Pagination logic
  const totalPages = Math.ceil(displayedSchemes.length / schemesPerPage)
  const startIndex = (currentPage - 1) * schemesPerPage
  const endIndex = startIndex + schemesPerPage
  const currentSchemes = displayedSchemes.slice(startIndex, endIndex)

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
                  <h2>Find Schemes</h2>
                  <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1rem' }}>
                    {isFiltered 
                      ? 'Showing filtered results. Clear filters to see all schemes.' 
                      : 'Browse all available schemes or use filters below to find personalized recommendations.'}
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
                    <div style={{ display: 'flex', gap: '1rem' }}>
                      <button type="submit" disabled={loading}>
                        {loading ? 'Filtering...' : 'Apply Filters'}
                      </button>
                      {isFiltered && (
                        <button type="button" onClick={clearFilters} style={{ background: '#6c757d' }}>
                          Clear Filters
                        </button>
                      )}
                    </div>
                  </form>

                  <div style={{ marginTop: '2rem' }}>
                    <h3>
                      {isFiltered ? 'Recommended Schemes' : `All Schemes (${displayedSchemes.length})`}
                    </h3>
                    
                    {displayedSchemes.length === 0 ? (
                      <div style={{ padding: '1rem', background: '#fff3cd', borderRadius: '4px', color: '#856404' }}>
                        <strong>No schemes found.</strong> Try adjusting your criteria or clearing filters.
                      </div>
                    ) : (
                      <>
                        <SchemeList schemes={currentSchemes} />
                        
                        {totalPages > 1 && (
                          <div style={{ 
                            display: 'flex', 
                            justifyContent: 'center', 
                            alignItems: 'center', 
                            gap: '1rem', 
                            marginTop: '2rem',
                            padding: '1rem'
                          }}>
                            <button 
                              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                              disabled={currentPage === 1}
                              style={{ padding: '0.5rem 1rem' }}
                            >
                              ← Previous
                            </button>
                            <span style={{ fontSize: '0.9rem', color: '#666' }}>
                              Page {currentPage} of {totalPages}
                            </span>
                            <button 
                              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                              disabled={currentPage === totalPages}
                              style={{ padding: '0.5rem 1rem' }}
                            >
                              Next →
                            </button>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </section>
              </main>
            }
          />

          <Route path="/schemes/:id" element={<SchemeDetail schemes={allSchemes} />} />
        </Routes>

        <footer>
          <small>Local dev mode — proxy `/api` to backend.</small>
        </footer>
      </div>
    </BrowserRouter>
  )
}
