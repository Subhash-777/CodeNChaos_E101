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

export async function fetchDashboardData(userId?: string | null): Promise<DashboardData> {
  if (!userId) {
    throw new Error("User ID is required to fetch dashboard data")
  }
  console.log("📊 Fetching dashboard for user:", userId.substring(0, 8) + "...")
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    "X-User-Id": userId
  }
  const response = await fetch(`${API_URL}/api/dashboard?t=${Date.now()}`, { headers, cache: 'no-store' })
  if (!response.ok) {
    throw new Error(`Failed to fetch dashboard data: ${response.status}`)
  }
  const data = await response.json()
  console.log("📊 Dashboard data received for user:", userId.substring(0, 8) + "...", "contexts:", data.contexts?.length, "tasks:", data.tasks?.length)
  return data
}

export async function fetchContexts(userId?: string | null): Promise<Context[]> {
  if (!userId) {
    throw new Error("User ID is required to fetch contexts")
  }
  console.log("📡 Fetching contexts for user:", userId.substring(0, 8) + "...")
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    "X-User-Id": userId
  }
  const response = await fetch(`${API_URL}/api/contexts?t=${Date.now()}`, { headers, cache: 'no-store' })
  if (!response.ok) {
    console.error("❌ Failed to fetch contexts:", response.status, response.statusText)
    throw new Error(`Failed to fetch contexts: ${response.status}`)
  }
  const data = await response.json()
  console.log("✅ Received contexts:", data.contexts?.length || 0, "items for user", userId.substring(0, 8) + "...")
  if (data.contexts && data.contexts.length > 0) {
    console.log("   First context name:", data.contexts[0].name)
  }
  return data.contexts
}

export async function fetchTasks(userId?: string | null): Promise<Task[]> {
  if (!userId) {
    throw new Error("User ID is required to fetch tasks")
  }
  console.log("📋 Fetching tasks for user:", userId.substring(0, 8) + "...")
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    "X-User-Id": userId
  }
  const response = await fetch(`${API_URL}/api/tasks?t=${Date.now()}`, { headers, cache: 'no-store' })
  if (!response.ok) {
    throw new Error(`Failed to fetch tasks: ${response.status}`)
  }
  const data = await response.json()
  console.log("✅ Received tasks:", data.tasks?.length || 0, "items for user", userId.substring(0, 8) + "...")
  if (data.tasks && data.tasks.length > 0) {
    console.log("   Top task:", data.tasks[0].title, "score:", data.tasks[0].priority_score)
  }
  return data.tasks
}

export async function fetchCognitiveLoad(userId?: string | null): Promise<CognitiveLoad> {
  if (!userId) {
    throw new Error("User ID is required to fetch cognitive load")
  }
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    "X-User-Id": userId
  }
  const response = await fetch(`${API_URL}/api/cognitive-load?t=${Date.now()}`, { headers, cache: 'no-store' })
  if (!response.ok) {
    throw new Error(`Failed to fetch cognitive load: ${response.status}`)
  }
  const data = await response.json()
  return data.cognitive_load
}

export async function fetchInsights(userId?: string | null): Promise<Insight[]> {
  if (!userId) {
    throw new Error("User ID is required to fetch insights")
  }
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    "X-User-Id": userId
  }
  const response = await fetch(`${API_URL}/api/insights?t=${Date.now()}`, { headers, cache: 'no-store' })
  if (!response.ok) {
    throw new Error(`Failed to fetch insights: ${response.status}`)
  }
  const data = await response.json()
  return data.insights
}

export async function fetchRecommendations(userId?: string | null): Promise<Recommendation[]> {
  if (!userId) {
    throw new Error("User ID is required to fetch recommendations")
  }
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    "X-User-Id": userId
  }
  const response = await fetch(`${API_URL}/api/recommendations?t=${Date.now()}`, { headers, cache: 'no-store' })
  if (!response.ok) {
    throw new Error(`Failed to fetch recommendations: ${response.status}`)
  }
  const data = await response.json()
  return data.recommendations
}
