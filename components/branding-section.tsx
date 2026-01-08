"use client"

import { useEffect, useState } from "react"

export function BrandingSection() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary/10 via-accent/5 to-background relative overflow-hidden items-center justify-center p-8">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-96 h-96 bg-primary/20 rounded-full blur-3xl opacity-30 animate-pulse" />
        <div
          className="absolute bottom-0 right-0 w-72 h-72 bg-accent/20 rounded-full blur-3xl opacity-20 animate-pulse"
          style={{ animationDelay: "1s" }}
        />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-md text-center">
        {/* Logo / Icon */}
        <div className="mb-8 flex justify-center">
          <div className="w-16 h-16 bg-primary rounded-xl flex items-center justify-center shadow-lg">
            <div className="text-primary-foreground text-2xl font-bold">✨</div>
          </div>
        </div>

        <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4 text-balance">
          Productivity Meets Intelligence
        </h2>

        <p className="text-base sm:text-lg text-muted-foreground text-pretty">
          Let AI transform how you work. FocusFlow AI learns your patterns,
          optimizes your workflow, and helps you achieve more with less effort.
        </p>
      </div>
    </div>
  )
}
