"use client"

import { useState } from "react"
import { MessageCircle, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import GoogleSyncButton from "./google-sync-button"
import { useSync } from "@/lib/sync-context"

interface HeaderProps {
  onChatClick: () => void
  chatOpen: boolean
}

export default function Header({ onChatClick, chatOpen }: HeaderProps) {
  const { triggerRefresh } = useSync()
  const [isRefreshing, setIsRefreshing] = useState(false)

  const handleManualRefresh = async () => {
    setIsRefreshing(true)
    console.log("🔄 Manual refresh triggered by user")
    triggerRefresh()
    // Show refresh animation for 1 second
    setTimeout(() => {
      setIsRefreshing(false)
    }, 1000)
  }

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-8 py-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Personal Productivity Intelligence Dashboard</h1>
        </div>
        <div className="flex items-center gap-4">
          <Button
            variant="outline"
            size="sm"
            onClick={handleManualRefresh}
            disabled={isRefreshing}
            className="flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? "animate-spin" : ""}`} />
            {isRefreshing ? "Refreshing..." : "Refresh"}
          </Button>
          <GoogleSyncButton />
          <Button
            variant="outline"
            size="icon"
            onClick={onChatClick}
            className={`rounded-full transition-colors ${chatOpen ? "bg-blue-50 border-blue-200" : ""}`}
          >
            <MessageCircle className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </header>
  )
}
