import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'
import { getSchemes } from './api'

vi.mock('./api', () => ({
  getSchemes: vi.fn(),
  getRecommendations: vi.fn()
}))

describe('App', () => {
  beforeEach(() => {
    ;(getSchemes as unknown as vi.Mock).mockResolvedValue([
      { id: 1, name: 'Scheme A', description: 'Desc A' },
      { id: 2, name: 'Scheme B', description: 'Desc B' }
    ])
  })

  it('renders schemes and navigates to detail', async () => {
    render(<App />)

    await waitFor(() => expect(getSchemes).toHaveBeenCalled())

    expect(screen.getByText('Scheme A')).toBeInTheDocument()
    expect(screen.getByText('Scheme B')).toBeInTheDocument()

    // click first scheme link
    const link = screen.getByText('Scheme A')
    await userEvent.click(link)

    await waitFor(() => {
      expect(screen.getByText('Desc A')).toBeInTheDocument()
    })
  })
})
