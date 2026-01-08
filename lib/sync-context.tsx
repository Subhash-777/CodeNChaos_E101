"use client"

import { createContext, useContext, useState, ReactNode } from "react"

interface SyncContextType {
  lastSyncTime: number | null
  triggerRefresh: () => void
  refreshKey: number
}

const SyncContext = createContext<SyncContextType | undefined>(undefined)

export function SyncProvider({ children }: { children: ReactNode }) {
  const [lastSyncTime, setLastSyncTime] = useState<number | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  const triggerRefresh = () => {
    console.log("🔄 SyncContext: Triggering refresh, current key:", refreshKey)
    setLastSyncTime(Date.now())
    setRefreshKey((prev) => {
      const newKey = prev + 1
      console.log("🔄 SyncContext: New refresh key:", newKey)
      return newKey
    })
  }

  return (
    <SyncContext.Provider value={{ lastSyncTime, triggerRefresh, refreshKey }}>
      {children}
    </SyncContext.Provider>
  )
}

export function useSync() {
  const context = useContext(SyncContext)
  if (context === undefined) {
    throw new Error("useSync must be used within a SyncProvider")
  }
  return context
}
