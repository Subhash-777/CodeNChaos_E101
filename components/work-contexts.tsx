"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle2, Loader2 } from "lucide-react"
import { fetchContexts, type Context } from "@/lib/api"

export default function WorkContexts() {
  const [contexts, setContexts] = useState<Context[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadContexts() {
      try {
        setLoading(true)
        const data = await fetchContexts()
        setContexts(data)
        setError(null)
      } catch (err) {
        setError("Failed to load contexts")
        console.error("Error fetching contexts:", err)
      } finally {
        setLoading(false)
      }
    }
    loadContexts()
  }, [])

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
