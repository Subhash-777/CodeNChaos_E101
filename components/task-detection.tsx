"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Mail, FileText, MessageSquare } from "lucide-react"

export default function TaskDetection() {
  const [showTasks, setShowTasks] = useState(false)

  const extractedTasks = [
    {
      title: "Review and approve design mockups",
      priority: 1,
      source: "Email",
      icon: Mail,
      explanation: "Received from design team this morning",
    },
    {
      title: "Prepare budget forecast",
      priority: 2,
      source: "Document",
      icon: FileText,
      explanation: "Mentioned in Q1 planning document",
    },
    {
      title: "Sync with product team",
      priority: 2,
      source: "Slack",
      icon: MessageSquare,
      explanation: "Action items from yesterday's discussion",
    },
  ]

  return (
    <Card className="border-slate-200 shadow-sm rounded-2xl">
      <CardHeader>
        <CardTitle className="text-slate-900">Automatic Task Detection</CardTitle>
        <CardDescription>Tasks extracted automatically from emails, documents, and messages</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Button onClick={() => setShowTasks(!showTasks)} variant="outline" className="w-full md:w-auto">
          {showTasks ? "Hide" : "Show"} Extracted Tasks
        </Button>

        {showTasks && (
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
      </CardContent>
    </Card>
  )
}
