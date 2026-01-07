"use client"

import { MessageCircle } from "lucide-react"
import { Button } from "@/components/ui/button"

interface HeaderProps {
  onChatClick: () => void
  chatOpen: boolean
}

export default function Header({ onChatClick, chatOpen }: HeaderProps) {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-8 py-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Personal Productivity Intelligence Dashboard</h1>
        </div>
        <Button
          variant="outline"
          size="icon"
          onClick={onChatClick}
          className={`rounded-full transition-colors ${chatOpen ? "bg-blue-50 border-blue-200" : ""}`}
        >
          <MessageCircle className="w-5 h-5" />
        </Button>
      </div>
    </header>
  )
}
