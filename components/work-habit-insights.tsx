"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

export default function WorkHabitInsights() {
  const taskSwitchingData = [
    { day: "Mon", switches: 8 },
    { day: "Tue", switches: 6 },
    { day: "Wed", switches: 9 },
    { day: "Thu", switches: 5 },
    { day: "Fri", switches: 7 },
    { day: "Sat", switches: 3 },
    { day: "Sun", switches: 2 },
  ]

  const ignoredTasksData = [
    { week: "Week 1", ignored: 2 },
    { week: "Week 2", ignored: 3 },
    { week: "Week 3", ignored: 1 },
    { week: "Week 4", ignored: 2 },
  ]

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
