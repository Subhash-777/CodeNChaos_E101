"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { LoginForm } from "./login-form"
import { SignupForm } from "./signup-form"
import { BrandingSection } from "./branding-section"
import { FirebaseStatus } from "./firebase-status"

export function AuthPage() {
  const [activeTab, setActiveTab] = useState("login")

  return (
    <div className="min-h-screen bg-background flex">
      {/* Branding Section - Desktop Only */}
      <BrandingSection />

      {/* Auth Section */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-6 lg:p-8">
        <div className="w-full max-w-md">
          {/* Header */}
          <div className="mb-8 text-center lg:text-left lg:mb-10">
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground mb-2">FocusFlow AI</h1>
            <p className="text-sm sm:text-base text-muted-foreground">
              Your personal productivity intelligence assistant
            </p>
          </div>

          {/* Auth Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 bg-muted border border-border">
              <TabsTrigger value="login">Login</TabsTrigger>
              <TabsTrigger value="signup">Sign Up</TabsTrigger>
            </TabsList>

            <TabsContent value="login" className="mt-6 space-y-6">
              <LoginForm />
            </TabsContent>

            <TabsContent value="signup" className="mt-6 space-y-6">
              <SignupForm />
            </TabsContent>
          </Tabs>

          {/* Footer */}
          <div className="mt-12 text-center text-xs text-muted-foreground">
            <p>© 2026 FocusFlow AI</p>
          </div>
        </div>
      </div>
      
      {/* Firebase Status Warning */}
      <FirebaseStatus />
    </div>
  )
}
