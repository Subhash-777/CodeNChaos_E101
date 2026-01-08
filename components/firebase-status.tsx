"use client"

import { useEffect, useState } from "react"
import { isConfigured } from "@/lib/firebase"

export function FirebaseStatus() {
  const [configured, setConfigured] = useState(false)

  useEffect(() => {
    setConfigured(isConfigured())
  }, [])

  if (configured) return null

  return (
    <div className="fixed bottom-4 right-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4 shadow-lg max-w-sm z-50">
      <div className="flex items-start gap-3">
        <div className="text-yellow-600 text-xl">⚠️</div>
        <div className="flex-1">
          <h3 className="font-semibold text-yellow-900 mb-1">Firebase Not Configured</h3>
          <p className="text-sm text-yellow-800 mb-2">
            Authentication will not work until Firebase credentials are added to `.env.local`
          </p>
          <a
            href="/FIREBASE_SETUP.md"
            target="_blank"
            className="text-xs text-yellow-700 underline hover:text-yellow-900"
          >
            View setup instructions →
          </a>
        </div>
      </div>
    </div>
  )
}
