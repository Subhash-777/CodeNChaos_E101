"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
import { fetchTasks, type Task } from "@/lib/api"
import { useSync } from "@/lib/sync-context"
import { useUser } from "@/lib/user-context"

export default function PriorityExplanation() {
  const { refreshKey } = useSync()
  const { userId } = useUser()
  const [topTask, setTopTask] = useState<Task | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!userId) {
      setLoading(false)
      return
    }
    
    async function loadTopTask() {
      try {
        setLoading(true)
        const data = await fetchTasks(userId)
        // Get the highest priority task
        const sortedTasks = data.sort((a, b) => b.priority_score - a.priority_score)
        setTopTask(sortedTasks[0] || null)
        setError(null)
      } catch (err) {
        setError("Failed to load task data")
        console.error("Error fetching tasks:", err)
      } finally {
        setLoading(false)
      }
    }
    
    // Initial load
    loadTopTask()
    
    // Auto-refresh every 30 seconds
    const autoRefreshInterval = setInterval(() => {
      console.log("🔄 Auto-refreshing priority explanation for user:", userId.substring(0, 8) + "...")
      loadTopTask()
    }, 30000)
    
    return () => clearInterval(autoRefreshInterval)
  }, [refreshKey, userId]) // Refetch when sync completes or user changes

  if (loading) {
    return (
      <Card className="border-slate-200 shadow-sm rounded-2xl">
        <CardHeader>
          <CardTitle className="text-slate-900">Why This Task Is Priority #1</CardTitle>
          <CardDescription>Explainable AI breakdown</CardDescription>
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
          <CardTitle className="text-slate-900">Why This Task Is Priority #1</CardTitle>
          <CardDescription>Explainable AI breakdown</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center text-slate-500 text-sm py-8">{error}</div>
        </CardContent>
      </Card>
    )
  }

  // Show content when available (backend will provide mock data if Google data is empty)
  if (!topTask && !loading) {
    return (
      <Card className="border-slate-200 shadow-sm rounded-2xl">
        <CardHeader>
          <CardTitle className="text-slate-900">Why This Task Is Priority #1</CardTitle>
          <CardDescription>Explainable AI breakdown</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center text-slate-500 text-sm py-8">
            No priority task available. Connect and sync your Google account to see task explanations.
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!topTask) {
    return null // Still loading
  }

  // Determine factors based on task data
  const deadlineProximity = topTask.deadline ? "High" : "Medium"
  const contextImportance = topTask.context
  const activitySignals = topTask.status === "in_progress" ? "Active" : "Pending"
  const delayRisk = topTask.priority_score >= 80 ? "High impact if missed" : "Medium impact"

  const factors = [
    { label: "Deadline Proximity", value: deadlineProximity },
    { label: "Context Importance", value: contextImportance },
    { label: "User Activity Signals", value: activitySignals },
    { label: "Delay Risk", value: delayRisk },
  ]

  return (
    <Card className="border-slate-200 shadow-sm rounded-2xl">
      <CardHeader>
        <CardTitle className="text-slate-900">Why This Task Is Priority #1</CardTitle>
        <CardDescription>Explainable AI breakdown</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          {factors.map((factor, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200"
            >
              <span className="text-sm font-medium text-slate-900">{factor.label}</span>
              <span className="text-sm text-slate-600 bg-white px-3 py-1 rounded border border-slate-200">
                {factor.value}
              </span>
            </div>
          ))}
        </div>
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-900">
            <strong>Final Priority Score:</strong> {topTask.priority_score}/100 - A weighted combination of deadline
            proximity (40%), context importance (30%), activity signals (20%), and delay risk (10%).
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
