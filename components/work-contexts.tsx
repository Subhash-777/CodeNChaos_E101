"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle2 } from "lucide-react"

export default function WorkContexts() {
  const contexts = [
    {
      name: "Hackathon Review",
      tasks: ["Finalize proposal deck", "Schedule team sync", "Prepare demo materials"],
    },
    {
      name: "College",
      tasks: ["Complete research paper", "Prepare presentation", "Review syllabus updates"],
    },
  ]

  return (
    <Card className="border-slate-200 shadow-sm rounded-2xl">
      <CardHeader>
        <CardTitle className="text-slate-900">Work Contexts</CardTitle>
        <CardDescription>Unified view of emails, documents, calendar, and tasks</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {contexts.map((context, idx) => (
            <div
              key={idx}
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
