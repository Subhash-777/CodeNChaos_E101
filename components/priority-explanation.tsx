"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function PriorityExplanation() {
  const factors = [
    { label: "Deadline Proximity", value: "High" },
    { label: "Context Importance", value: "Hackathon Review" },
    { label: "User Activity Signals", value: "Email + Document" },
    { label: "Delay Risk", value: "High impact if missed" },
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
            <strong>Final Priority Score:</strong> A weighted combination of deadline proximity (40%), context
            importance (30%), activity signals (20%), and delay risk (10%).
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
