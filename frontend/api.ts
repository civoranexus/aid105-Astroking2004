import axios from 'axios'
import { config } from './src/config'

const api = axios.create({ baseURL: config.apiUrl || '/api' })

export interface Scheme {
  id: string
  title: string
  description?: string
  eligibility?: string
  application?: string
  level?: string
  schemeCategory?: string
  tags?: string[]
  benefits?: string[]
  documents?: string[]
}

export interface UserInput {
  income?: number
  state?: string
  needs?: string[]
}

export async function getSchemes(): Promise<Scheme[]> {
  const res = await api.get('/schemes')
  return Array.isArray(res.data) ? res.data : (res.data?.schemes || [])
}

export async function getRecommendations(user: any, includeCentral: boolean = true): Promise<Scheme[]> {
  const res = await api.post(`/recommendations?top_k=200&include_central=${includeCentral}`, user)
  return Array.isArray(res.data) ? res.data : (res.data?.recommendations || [])
}
