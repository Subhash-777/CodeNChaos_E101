"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { X, Send } from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"

interface AIChatPanelProps {
  isOpen: boolean
  onClose: () => void
}

export default function AIChatPanel({ isOpen, onClose }: AIChatPanelProps) {
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([
    {
      role: "user",
      content: "What should I focus on now?",
    },
    {
      role: "assistant",
      content:
        "Based on your current priorities, you should focus on reviewing and approving the design mockups. The design team is waiting for your feedback to proceed with development, and this task has a high deadline proximity score. It's part of your Hackathon Review context and was flagged through recent email activity.",
    },
  ])
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (!input.trim()) return

    const newMessages = [
      ...messages,
      { role: "user" as const, content: input },
      {
        role: "assistant" as const,
        content: "That's a great follow-up. Let me help you with that task.",
      },
    ]

    setMessages(newMessages)
    setInput("")
  }

  return (
    <div
      className={`fixed right-0 top-0 h-screen w-96 bg-white border-l border-slate-200 shadow-lg transform transition-transform duration-300 z-50 ${
        isOpen ? "translate-x-0" : "translate-x-full"
      }`}
    >
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-900">AI Assistant</h2>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="w-5 h-5" />
          </Button>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1 p-6">
          <div className="space-y-4">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-xs px-4 py-2 rounded-lg ${
                    msg.role === "user" ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-900"
                  }`}
                >
                  <p className="text-sm">{msg.content}</p>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>

        {/* Input */}
        <div className="p-4 border-t border-slate-200">
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Ask me anything..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSend()}
              className="flex-1 px-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <Button size="icon" onClick={handleSend} className="bg-blue-600 hover:bg-blue-700">
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
