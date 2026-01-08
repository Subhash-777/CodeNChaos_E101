"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Mail, FileText, MessageSquare, Loader2 } from "lucide-react"
import { fetchTasks, type Task } from "@/lib/api"
import { useSync } from "@/lib/sync-context"
import { useUser } from "@/lib/user-context"

const sourceIcons: Record<string, typeof Mail> = {
  Email: Mail,
  Document: FileText,
  Slack: MessageSquare,
  Message: MessageSquare,
}

export default function TaskDetection() {
  const { refreshKey } = useSync()
  const { userId } = useUser()
  const [showTasks, setShowTasks] = useState(false)
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
        setTasks(data)
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
      console.log("🔄 Auto-refreshing tasks for user:", userId.substring(0, 8) + "...")
      loadTasks()
    }, 30000)
    
    return () => clearInterval(autoRefreshInterval)
  }, [refreshKey, userId]) // Refetch when sync completes or user changes

  // Map tasks to extracted tasks format
  const extractedTasks = tasks.slice(0, 3).map((task, idx) => {
    // Determine source based on context field
    let source = "Slack" // default
    if (task.context === "Email") {
      source = "Email"
    } else if (task.context === "Calendar") {
      source = "Slack" // Calendar tasks show with message icon
    } else if (task.context && (task.context.includes("Hackathon") || task.context.includes("College"))) {
      source = task.context.includes("Hackathon") ? "Email" : "Document"
    }
    
    const IconComponent = sourceIcons[source] || Mail
    
    return {
      title: task.title,
      priority: idx + 1,
      source: source,
      icon: IconComponent,
      explanation: task.explanation,
    }
  })

  return (
    <Card className="border-slate-200 shadow-sm rounded-2xl">
      <CardHeader>
        <CardTitle className="text-slate-900">Automatic Task Detection</CardTitle>
        <CardDescription>Tasks extracted automatically from emails, documents, and calendar</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Button onClick={() => setShowTasks(!showTasks)} variant="outline" className="w-full md:w-auto">
          {showTasks ? "Hide" : "Show"} Extracted Tasks
        </Button>

        {loading && (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
          </div>
        )}

        {error && !loading && (
          <div className="text-center text-slate-500 text-sm py-4">{error}</div>
        )}

        {showTasks && !loading && !error && extractedTasks.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {extractedTasks.map((task, idx) => {
              const IconComponent = task.icon
              return (
                <div
                  key={idx}
                  className="p-4 bg-slate-50 rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <IconComponent className="w-4 h-4 text-slate-400" />
                    <Badge
                      variant="secondary"
                      className={`text-xs ${
                        task.priority === 1 ? "bg-amber-100 text-amber-800" : "bg-slate-200 text-slate-700"
                      }`}
                    >
                      Priority {task.priority}
                    </Badge>
                  </div>
                  <h4 className="font-medium text-slate-900 text-sm mb-2">{task.title}</h4>
                  <p className="text-xs text-slate-600 mb-3">{task.explanation}</p>
                  <span className="text-xs text-slate-500 bg-white px-2 py-1 rounded border border-slate-200 inline-block">
                    {task.source}
                  </span>
                </div>
              )
            })}
          </div>
        )}

        {showTasks && !loading && !error && extractedTasks.length === 0 && (
          <div className="text-center text-slate-500 text-sm py-4">
            No extracted tasks. Connect and sync your Google account to see automatic task detection.
          </div>
        )}
      </CardContent>
    </Card>
  )
}
