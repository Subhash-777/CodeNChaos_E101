"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Sparkles, Loader2 } from "lucide-react"
import { fetchTasks, type Task } from "@/lib/api"
import { useSync } from "@/lib/sync-context"
import { useUser } from "@/lib/user-context"

export default function RecommendedTasks() {
  const { refreshKey } = useSync()
  const { userId } = useUser()
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!userId) {
      setLoading(false)
      return
    }
    
    async function loadTasks() {
      try {
        setLoading(true)
        const data = await fetchTasks(userId)
        // Sort by priority score and take top 3
        const sortedTasks = data.sort((a, b) => b.priority_score - a.priority_score).slice(0, 3)
        setTasks(sortedTasks)
        setError(null)
      } catch (err) {
        setError("Failed to load tasks")
        console.error("Error fetching tasks:", err)
      } finally {
        setLoading(false)
      }
    }
    
    // Initial load
    loadTasks()
    
    // Auto-refresh every 30 seconds
    const autoRefreshInterval = setInterval(() => {
      console.log("🔄 Auto-refreshing recommended tasks for user:", userId.substring(0, 8) + "...")
      loadTasks()
    }, 30000)
    
    return () => clearInterval(autoRefreshInterval)
  }, [refreshKey, userId]) // Refetch when sync completes or user changes

  if (loading) {
    return (
      <Card className="border-slate-200 shadow-sm rounded-2xl">
        <CardHeader>
          <CardTitle className="text-slate-900">What Should I Work On Next?</CardTitle>
          <CardDescription>Top 3 recommended tasks</CardDescription>
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
          <CardTitle className="text-slate-900">What Should I Work On Next?</CardTitle>
          <CardDescription>Top 3 recommended tasks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center text-slate-500 text-sm py-8">{error}</div>
        </CardContent>
      </Card>
    )
  }

  // Show content even if empty initially (backend will provide mock data if Google data is empty)
  if (tasks.length === 0 && !loading) {
    return (
      <Card className="border-slate-200 shadow-sm rounded-2xl">
        <CardHeader>
          <CardTitle className="text-slate-900">What Should I Work On Next?</CardTitle>
          <CardDescription>Top 3 recommended tasks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center text-slate-500 text-sm py-8">
            No tasks available. Connect and sync your Google account to see recommended tasks.
          </div>
        </CardContent>
      </Card>
    )
  }

  if (tasks.length === 0) {
    return null // Still loading
  }

  const topTask = tasks[0]
  const isPriority = topTask && topTask.priority_score >= 80

  return (
    <Card className="border-slate-200 shadow-sm rounded-2xl">
      <CardHeader>
        <CardTitle className="text-slate-900">What Should I Work On Next?</CardTitle>
        <CardDescription>Top 3 recommended tasks</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {tasks.map((task, idx) => {
            const isTopPriority = idx === 0 && isPriority
            return (
              <div
                key={task.id}
                className={`p-4 rounded-xl border transition-colors ${
                  isTopPriority ? "bg-blue-50 border-blue-200 shadow-sm" : "bg-slate-50 border-slate-200"
                }`}
              >
                <div className="flex items-start gap-3">
                  {isTopPriority && <Sparkles className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />}
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className={`font-medium ${isTopPriority ? "text-blue-900" : "text-slate-900"}`}>
                        {task.title}
                      </h4>
                      {isTopPriority && <Badge className="bg-blue-600 text-white text-xs">Priority #1</Badge>}
                    </div>
                    <p className={`text-sm ${isTopPriority ? "text-blue-800" : "text-slate-600"}`}>
                      {task.explanation}
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
