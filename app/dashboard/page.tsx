"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { onAuthStateChanged } from "firebase/auth"
import { auth } from "@/lib/firebase"
import Header from "@/components/header"
import WorkContexts from "@/components/work-contexts"
import TaskDetection from "@/components/task-detection"
import RecommendedTasks from "@/components/recommended-tasks"
import PriorityExplanation from "@/components/priority-explanation"
import WorkHabitInsights from "@/components/work-habit-insights"
import AIChatPanel from "@/components/ai-chat-panel"

export default function Dashboard() {
  const router = useRouter()
  const [chatOpen, setChatOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (!user) {
        router.push("/")
      } else {
        setLoading(false)
      }
    })

    return () => unsubscribe()
  }, [router])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50 transition-all duration-300">
      <Header onChatClick={() => setChatOpen(!chatOpen)} chatOpen={chatOpen} />

      {/* Main dashboard content */}
      <main className={`transition-all duration-300 ${chatOpen ? "mr-96" : "mr-0"}`}>
        <div className="max-w-6xl mx-auto p-8 space-y-6">
          {/* Work Contexts */}
          <WorkContexts />

          {/* Automatic Task Detection */}
          <TaskDetection />

          {/* Recommended Tasks Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* What Should I Work On Next? */}
            <RecommendedTasks />

            {/* Why This Task Is Priority #1 */}
            <PriorityExplanation />
          </div>

          {/* Work Habit Insights */}
          <WorkHabitInsights />
        </div>
      </main>

      {/* AI Chat Panel */}
      <AIChatPanel isOpen={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  )
}
