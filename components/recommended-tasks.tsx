"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Sparkles } from "lucide-react"

export default function RecommendedTasks() {
  const tasks = [
    {
      title: "Review and approve design mockups",
      explanation: "Design team is waiting for feedback to proceed with development.",
      isPriority: true,
    },
    {
      title: "Prepare budget forecast",
      explanation: "Q1 planning meeting is tomorrow morning.",
      isPriority: false,
    },
    {
      title: "Sync with product team",
      explanation: "Outstanding action items from weekly standup.",
      isPriority: false,
    },
  ]

  return (
    <Card className="border-slate-200 shadow-sm rounded-2xl">
      <CardHeader>
        <CardTitle className="text-slate-900">What Should I Work On Next?</CardTitle>
        <CardDescription>Top 3 recommended tasks</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {tasks.map((task, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-xl border transition-colors ${
                task.isPriority ? "bg-blue-50 border-blue-200 shadow-sm" : "bg-slate-50 border-slate-200"
              }`}
            >
              <div className="flex items-start gap-3">
                {task.isPriority && <Sparkles className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />}
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className={`font-medium ${task.isPriority ? "text-blue-900" : "text-slate-900"}`}>
                      {task.title}
                    </h4>
                    {task.isPriority && <Badge className="bg-blue-600 text-white text-xs">Priority #1</Badge>}
                  </div>
                  <p className={`text-sm ${task.isPriority ? "text-blue-800" : "text-slate-600"}`}>
                    {task.explanation}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
