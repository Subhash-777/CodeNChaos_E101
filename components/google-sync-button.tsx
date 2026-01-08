"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { RefreshCw, Link, CheckCircle2, AlertCircle } from "lucide-react"
import { useSync } from "@/lib/sync-context"
import { useUser } from "@/lib/user-context"
import { auth } from "@/lib/firebase"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

interface SyncStatus {
  connected: boolean
  last_sync: string | null
  has_calendar_data: boolean
  has_email_data: boolean
}

export default function GoogleSyncButton() {
  const { triggerRefresh } = useSync()
  const { userId } = useUser()
  const [status, setStatus] = useState<SyncStatus | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isSyncing, setIsSyncing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchStatus = async () => {
    if (!userId) return
    
    try {
      const headers: HeadersInit = {
        "X-User-Id": userId
      }
      const response = await fetch(`${API_URL}/api/google/status`, { headers })
      if (response.ok) {
        const data = await response.json()
        setStatus(data)
        setError(null)
      }
    } catch (err) {
      console.error("Error fetching Google status:", err)
    }
  }

  useEffect(() => {
    if (userId) {
      fetchStatus()
      // Refresh status every 30 seconds
      const interval = setInterval(fetchStatus, 30000)
      return () => clearInterval(interval)
    }
  }, [userId])

  const handleAuth = async () => {
    if (!userId) {
      setError("User not authenticated")
      return
    }
    
    console.log("🔐 Connecting Google for user:", userId)
    setIsLoading(true)
    setError(null)

    try {
      const headers: HeadersInit = {
        "X-User-Id": userId
      }
      console.log("📤 Sending auth request with user ID:", userId)
      const response = await fetch(`${API_URL}/api/google/auth`, { headers })
      const data = await response.json()
      console.log("📥 Auth response:", data)

      if (response.ok) {
        setStatus((prev) => ({ ...prev!, connected: true }))
        // After auth, trigger a sync
        setTimeout(() => {
          handleSync()
        }, 1500)
      } else {
        setError(data.detail || "Failed to connect Google account")
      }
    } catch (err: any) {
      setError("Failed to connect Google account. Please check if the backend is running.")
      console.error("Auth error:", err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSync = async () => {
    if (!userId) {
      setError("User not authenticated")
      return
    }
    
    console.log("🔄 Syncing Google data for user:", userId)
    setIsSyncing(true)
    setError(null)

    try {
      const headers: HeadersInit = {
        "X-User-Id": userId
      }
      console.log("📤 Sending sync request with user ID:", userId)
      const response = await fetch(`${API_URL}/api/google/sync`, {
        method: "POST",
        headers,
      })

      const data = await response.json()
      console.log("📥 Sync response:", data)

      if (response.ok) {
        console.log("✅ Sync completed for user:", userId)
        // Refresh status after sync
        await fetchStatus()
        // Trigger dashboard refresh multiple times to ensure data is loaded
        setTimeout(() => {
          console.log("🔄 Triggering dashboard refresh for user:", userId)
          triggerRefresh()
        }, 500)
        setTimeout(() => {
          console.log("🔄 Second refresh trigger for user:", userId)
          triggerRefresh()
        }, 1500)
      } else {
        setError(data.detail || "Sync failed")
      }
    } catch (err: any) {
      setError("Sync failed. Please check if the backend is running.")
      console.error("Sync error:", err)
    } finally {
      setIsSyncing(false)
    }
  }

  if (!status) {
    return (
      <Button variant="outline" size="sm" disabled>
        <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
        Loading...
      </Button>
    )
  }

  if (!status.connected) {
    return (
      <div className="flex items-center gap-2">
        <Button variant="outline" size="sm" onClick={handleAuth} disabled={isLoading}>
          {isLoading ? (
            <>
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              Connecting...
            </>
          ) : (
            <>
              <Link className="w-4 h-4 mr-2" />
              Connect Google
            </>
          )}
        </Button>
        {error && (
          <div className="flex items-center gap-1 text-xs text-red-600">
            <AlertCircle className="w-3 h-3" />
            <span>{error}</span>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="flex items-center gap-2">
      <Button
        variant="outline"
        size="sm"
        onClick={handleSync}
        disabled={isSyncing}
        className="relative"
      >
        {isSyncing ? (
          <>
            <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            Syncing...
          </>
        ) : (
          <>
            <RefreshCw className="w-4 h-4 mr-2" />
            Sync Now
          </>
        )}
      </Button>

      {status.last_sync && (
        <div className="flex items-center gap-1 text-xs text-slate-500">
          <CheckCircle2 className="w-3 h-3 text-green-600" />
          <span>
            Synced {new Date(status.last_sync).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </span>
        </div>
      )}

      {error && (
        <div className="flex items-center gap-1 text-xs text-red-600">
          <AlertCircle className="w-3 h-3" />
          <span>{error}</span>
        </div>
      )}
    </div>
  )
}
