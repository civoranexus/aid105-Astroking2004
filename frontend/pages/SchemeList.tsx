import React from 'react'
import { Link } from 'react-router-dom'
import { Scheme } from '../api'

export default function SchemeList({ schemes }: { schemes: Scheme[] }) {
  return (
    <div>
      <ul>
        {schemes.map((s) => (
          <li key={s.id}>
            <Link to={`/schemes/${s.id}`}>
              <strong>{s.title}</strong>
            </Link>
            <div className="muted">{s.description}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
