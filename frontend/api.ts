import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export interface Scheme {
  id: number
  name: string
  description?: string
}

export interface UserInput {
  age?: number
  income?: number
  state?: string
  needs?: string[]
}

export async function getSchemes(): Promise<Scheme[]> {
  const res = await api.get('/schemes')
  return Array.isArray(res.data) ? res.data : (res.data?.schemes || [])
}

export async function getRecommendations(user: any): Promise<Scheme[]> {
  const res = await api.post('/recommendations', user)
  return Array.isArray(res.data) ? res.data : (res.data?.recommendations || [])
}
