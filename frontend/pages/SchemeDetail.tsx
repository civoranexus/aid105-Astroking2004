import React from 'react'
import { Scheme } from '../api'
import { useParams, Link } from 'react-router-dom'

export default function SchemeDetail({ schemes }: { schemes: Scheme[] }) {
  const { id } = useParams()
  const sid = Number(id)
  const scheme = schemes.find((s) => s.id === sid)

  if (!scheme) return (
    <div>
      <p>Scheme not found.</p>
      <Link to="/">Back</Link>
    </div>
  )

  return (
    <div>
      <h3>{scheme.name}</h3>
      <p className="muted">{scheme.description}</p>
      <Link to="/">Back</Link>
    </div>
  )
}
