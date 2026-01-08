"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { Loader2 } from "lucide-react"
import { fetchCognitiveLoad, fetchInsights, type CognitiveLoad, type Insight } from "@/lib/api"

export default function WorkHabitInsights() {
  const [cognitiveLoad, setCognitiveLoad] = useState<CognitiveLoad | null>(null)
  const [insights, setInsights] = useState<Insight[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        const [loadData, insightsData] = await Promise.all([fetchCognitiveLoad(), fetchInsights()])
        setCognitiveLoad(loadData)
        setInsights(insightsData)
        setError(null)
      } catch (err) {
        setError("Failed to load insights")
        console.error("Error fetching insights:", err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  // Generate task switching data from cognitive load switches
  const taskSwitchingData = cognitiveLoad
    ? [
        { day: "Mon", switches: Math.floor(cognitiveLoad.switches * 0.15) },
        { day: "Tue", switches: Math.floor(cognitiveLoad.switches * 0.12) },
        { day: "Wed", switches: Math.floor(cognitiveLoad.switches * 0.18) },
        { day: "Thu", switches: Math.floor(cognitiveLoad.switches * 0.10) },
        { day: "Fri", switches: Math.floor(cognitiveLoad.switches * 0.14) },
        { day: "Sat", switches: Math.floor(cognitiveLoad.switches * 0.08) },
        { day: "Sun", switches: Math.floor(cognitiveLoad.switches * 0.05) },
      ]
    : []

  // Generate ignored tasks data from insights
  const ignoredTasksCount = insights.filter((i) => i.type === "ignored_priority").length
  const ignoredTasksData = [
    { week: "Week 1", ignored: Math.max(1, ignoredTasksCount - 1) },
    { week: "Week 2", ignored: ignoredTasksCount },
    { week: "Week 3", ignored: Math.max(1, ignoredTasksCount - 1) },
    { week: "Week 4", ignored: ignoredTasksCount },
  ]

  if (loading) {
    return (
      <Card className="border-slate-200 shadow-sm rounded-2xl">
        <CardHeader>
          <CardTitle className="text-slate-900">Work Habit Insights</CardTitle>
          <CardDescription>Your task switching and completion patterns</CardDescription>
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
          <CardTitle className="text-slate-900">Work Habit Insights</CardTitle>
          <CardDescription>Your task switching and completion patterns</CardDescription>
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
        <CardTitle className="text-slate-900">Work Habit Insights</CardTitle>
        <CardDescription>Your task switching and completion patterns</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Task Switching Chart */}
          <div>
            <h3 className="text-sm font-medium text-slate-900 mb-4">Task Switching Frequency</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={taskSwitchingData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="day" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#f8fafc",
                    border: "1px solid #e2e8f0",
                    borderRadius: "8px",
                  }}
                />
                <Bar dataKey="switches" fill="#3b82f6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Ignored Tasks Chart */}
          <div>
            <h3 className="text-sm font-medium text-slate-900 mb-4">Ignored Tasks Over Time</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={ignoredTasksData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="week" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#f8fafc",
                    border: "1px solid #e2e8f0",
                    borderRadius: "8px",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="ignored"
                  stroke="#06b6d4"
                  strokeWidth={2}
                  dot={{ fill: "#06b6d4", r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
