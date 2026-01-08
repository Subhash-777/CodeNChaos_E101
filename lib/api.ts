const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface Context {
  id: string
  name: string
  related_items?: string[]
  urgency: string
  deadline: string
  tasks: string[]
}

export interface Task {
  id: string
  title: string
  context: string
  deadline: string | null
  priority_score: number
  status: string
  explanation: string
}

export interface CognitiveLoad {
  score: number
  status: string
  active_contexts: number
  urgent_tasks: number
  switches: number
  breakdown: string
}

export interface Insight {
  type: string
  severity: string
  count?: number
  task?: string
  tasks?: string[]
  message: string
}

export interface Recommendation {
  action: string
  reason: string
  expected_impact: string
}

export interface DashboardData {
  contexts: Context[]
  tasks: Task[]
  cognitive_load: CognitiveLoad
  insights: Insight[]
  recommendations: Recommendation[]
}

export async function fetchDashboardData(): Promise<DashboardData> {
  const response = await fetch(`${API_URL}/api/dashboard`)
  if (!response.ok) {
    throw new Error(`Failed to fetch dashboard data: ${response.status}`)
  }
  return response.json()
}

export async function fetchContexts(): Promise<Context[]> {
  const response = await fetch(`${API_URL}/api/contexts`)
  if (!response.ok) {
    throw new Error(`Failed to fetch contexts: ${response.status}`)
  }
  const data = await response.json()
  return data.contexts
}

export async function fetchTasks(): Promise<Task[]> {
  const response = await fetch(`${API_URL}/api/tasks`)
  if (!response.ok) {
    throw new Error(`Failed to fetch tasks: ${response.status}`)
  }
  const data = await response.json()
  return data.tasks
}

export async function fetchCognitiveLoad(): Promise<CognitiveLoad> {
  const response = await fetch(`${API_URL}/api/cognitive-load`)
  if (!response.ok) {
    throw new Error(`Failed to fetch cognitive load: ${response.status}`)
  }
  const data = await response.json()
  return data.cognitive_load
}

export async function fetchInsights(): Promise<Insight[]> {
  const response = await fetch(`${API_URL}/api/insights`)
  if (!response.ok) {
    throw new Error(`Failed to fetch insights: ${response.status}`)
  }
  const data = await response.json()
  return data.insights
}

export async function fetchRecommendations(): Promise<Recommendation[]> {
  const response = await fetch(`${API_URL}/api/recommendations`)
  if (!response.ok) {
    throw new Error(`Failed to fetch recommendations: ${response.status}`)
  }
  const data = await response.json()
  return data.recommendations
}
