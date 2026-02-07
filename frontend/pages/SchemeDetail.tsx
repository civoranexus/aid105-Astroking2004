import React from 'react'
import { Scheme } from '../api'
import { useParams, Link } from 'react-router-dom'

export default function SchemeDetail({ schemes }: { schemes: Scheme[] }) {
  const { id } = useParams()
  const scheme = schemes.find((s) => s.id === id)

  if (!scheme) return (
    <div>
      <p>Scheme not found.</p>
      <Link to="/">Back</Link>
    </div>
  )

  return (
    <div>
      <h3>{scheme.title}</h3>
      <p className="muted">{scheme.description}</p>
      
      {scheme.level && (
        <div>
          <strong>Level:</strong> {scheme.level}
        </div>
      )}
      
      {scheme.schemeCategory && (
        <div>
          <strong>Category:</strong> {scheme.schemeCategory}
        </div>
      )}
      
      {scheme.eligibility && (
        <div>
          <h4>Eligibility</h4>
          <p>{scheme.eligibility}</p>
        </div>
      )}
      
      {scheme.benefits && scheme.benefits.length > 0 && (
        <div>
          <h4>Benefits</h4>
          <ul>
            {scheme.benefits.map((benefit, idx) => (
              <li key={idx}>{benefit}</li>
            ))}
          </ul>
        </div>
      )}
      
      {scheme.application && (
        <div>
          <h4>How to Apply</h4>
          <p>{scheme.application}</p>
        </div>
      )}
      
      {scheme.documents && scheme.documents.length > 0 && (
        <div>
          <h4>Required Documents</h4>
          <ul>
            {scheme.documents.map((doc, idx) => (
              <li key={idx}>{doc}</li>
            ))}
          </ul>
        </div>
      )}
      
      {scheme.tags && scheme.tags.length > 0 && (
        <div>
          <strong>Tags:</strong> {scheme.tags.join(', ')}
        </div>
      )}
      
      <Link to="/">Back</Link>
    </div>
  )
}
