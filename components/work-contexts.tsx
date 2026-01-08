"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle2, Loader2 } from "lucide-react"
import { fetchContexts, type Context } from "@/lib/api"
import { useSync } from "@/lib/sync-context"
import { useUser } from "@/lib/user-context"

export default function WorkContexts() {
  const { refreshKey } = useSync()
  const { userId } = useUser()
  const [contexts, setContexts] = useState<Context[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!userId) {
      setLoading(false)
      return
    }
    
    async function loadContexts() {
      try {
        setLoading(true)
        console.log("🔄 Loading contexts for user:", userId.substring(0, 8) + "...", "refreshKey:", refreshKey)
        // Add timestamp to force fresh fetch
        const data = await fetchContexts(userId)
        console.log("✅ Loaded contexts:", data.length, "items for user", userId.substring(0, 8) + "...")
        if (data.length > 0) {
          console.log("   First context:", data[0].name)
        }
        setContexts(data)
        setError(null)
      } catch (err) {
        setError("Failed to load contexts")
        console.error("❌ Error fetching contexts:", err)
      } finally {
        setLoading(false)
      }
    }
    
    // Initial load
    loadContexts()
    
    // Auto-refresh every 30 seconds
    const autoRefreshInterval = setInterval(() => {
      console.log("🔄 Auto-refreshing contexts for user:", userId.substring(0, 8) + "...")
      loadContexts()
    }, 30000)
    
    return () => clearInterval(autoRefreshInterval)
  }, [refreshKey, userId]) // Refetch when sync completes or user changes

  if (loading) {
    return (
      <Card className="border-slate-200 shadow-sm rounded-2xl">
        <CardHeader>
          <CardTitle className="text-slate-900">Work Contexts</CardTitle>
          <CardDescription>Unified view of emails, documents, calendar, and tasks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="border-slate-200 shadow-sm rounded-2xl">
        <CardHeader>
          <CardTitle className="text-slate-900">Work Contexts</CardTitle>
          <CardDescription>Unified view of emails, documents, calendar, and tasks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center text-slate-500 text-sm py-8">{error}</div>
        </CardContent>
      </Card>
    )
  }

  // Show content even if empty (backend will provide mock data if Google data is empty)
  if (contexts.length === 0 && !loading) {
    return (
      <Card className="border-slate-200 shadow-sm rounded-2xl">
        <CardHeader>
          <CardTitle className="text-slate-900">Work Contexts</CardTitle>
          <CardDescription>Unified view of emails, documents, calendar, and tasks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center text-slate-500 text-sm py-8">
            No contexts available. Connect and sync your Google account to see your work contexts.
          </div>
        </CardContent>
      </Card>
    )
  }

  if (contexts.length === 0) {
    return null // Still loading
  }

  return (
    <Card className="border-slate-200 shadow-sm rounded-2xl">
      <CardHeader>
        <CardTitle className="text-slate-900">Work Contexts</CardTitle>
        <CardDescription>Unified view of emails, documents, calendar, and tasks</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {contexts.map((context) => (
            <div
              key={context.id}
              className="p-4 bg-slate-50 rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors"
            >
              <h3 className="font-semibold text-slate-900 mb-3">{context.name}</h3>
              <ul className="space-y-2">
                {context.tasks.map((task, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <CheckCircle2 className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-slate-700">{task}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
