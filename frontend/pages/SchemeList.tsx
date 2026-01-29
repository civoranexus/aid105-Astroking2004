import React from 'react'
import { Link } from 'react-router-dom'
import { Scheme } from '../api'

export default function SchemeList({ schemes }: { schemes: Scheme[] }) {
  return (
    <div>
      {schemes.map((s) => (
        <div key={s.id} style={{ 
          marginBottom: '1.5rem', 
          padding: '1rem', 
          border: '1px solid #ddd', 
          borderRadius: '6px',
          background: '#f9f9f9'
        }}>
          <Link to={`/schemes/${s.id}`} style={{ textDecoration: 'none' }}>
            <h4 style={{ margin: '0 0 0.5rem 0', color: '#0066cc' }}>{s.title}</h4>
          </Link>
          
          <p style={{ fontSize: '0.9rem', color: '#555', marginBottom: '0.75rem' }}>
            {s.description}
          </p>
          
          <div style={{ marginBottom: '0.5rem' }}>
            {s.schemeCategory && (
              <span style={{ 
                fontSize: '0.75rem', 
                background: '#e0e0e0', 
                padding: '3px 8px', 
                borderRadius: '4px', 
                marginRight: '6px',
                display: 'inline-block'
              }}>
                📁 {s.schemeCategory}
              </span>
            )}
            {s.level && (
              <span style={{ 
                fontSize: '0.75rem', 
                background: '#d1e7dd', 
                padding: '3px 8px', 
                borderRadius: '4px',
                display: 'inline-block'
              }}>
                📍 {s.level}
              </span>
            )}
          </div>

          {(s.tags && s.tags.length > 0) && (
            <div style={{ marginTop: '0.5rem' }}>
              <small style={{ color: '#666', fontWeight: '600' }}>Tags: </small>
              {s.tags.map((tag: string, idx: number) => (
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

          {(s.benefits && s.benefits.length > 0) && (
            <div style={{ marginTop: '0.5rem' }}>
              <small style={{ color: '#666', fontWeight: '600' }}>Benefits: </small>
              {s.benefits.map((benefit: string, idx: number) => (
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
  )
}
