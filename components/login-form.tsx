"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Eye, EyeOff } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { signInWithEmailAndPassword, signInWithPopup } from "firebase/auth"
import { auth, googleProvider, isConfigured } from "@/lib/firebase"

export function LoginForm() {
  const router = useRouter()
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }))
    setError("")
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    
    if (!isConfigured()) {
      setError("Firebase is not configured. Please check your environment variables.")
      return
    }

    setIsLoading(true)
    setError("")

    try {
      const userCredential = await signInWithEmailAndPassword(auth, formData.email, formData.password)
      console.log("Login successful:", userCredential.user.email)
      // Redirect to dashboard on success
      router.push("/dashboard")
    } catch (err: any) {
      console.error("Login error:", err)
      let errorMessage = "Failed to login. Please check your credentials."
      
      // Provide user-friendly error messages
      if (err.code === "auth/user-not-found") {
        errorMessage = "No account found with this email address."
      } else if (err.code === "auth/wrong-password") {
        errorMessage = "Incorrect password. Please try again."
      } else if (err.code === "auth/invalid-email") {
        errorMessage = "Invalid email address."
      } else if (err.code === "auth/user-disabled") {
        errorMessage = "This account has been disabled."
      } else if (err.code === "auth/too-many-requests") {
        errorMessage = "Too many failed attempts. Please try again later."
      } else if (err.message) {
        errorMessage = err.message
      }
      
      setError(errorMessage)
      setIsLoading(false)
    }
  }

  const handleGoogleLogin = async () => {
    if (!isConfigured()) {
      setError("Firebase is not configured. Please check your environment variables.")
      return
    }

    setIsLoading(true)
    setError("")

    try {
      const result = await signInWithPopup(auth, googleProvider)
      console.log("Google login successful:", result.user.email)
      // Redirect to dashboard on success
      router.push("/dashboard")
    } catch (err: any) {
      console.error("Google login error:", err)
      let errorMessage = "Failed to login with Google."
      
      // Provide user-friendly error messages
      if (err.code === "auth/popup-closed-by-user") {
        errorMessage = "Sign-in popup was closed. Please try again."
      } else if (err.code === "auth/popup-blocked") {
        errorMessage = "Popup was blocked by your browser. Please allow popups and try again."
      } else if (err.code === "auth/cancelled-popup-request") {
        errorMessage = "Only one popup request is allowed at a time."
      } else if (err.message) {
        errorMessage = err.message
      }
      
      setError(errorMessage)
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Email Field */}
      <div className="space-y-2">
        <Label htmlFor="email" className="text-sm font-medium">
          Email
        </Label>
        <Input
          id="email"
          name="email"
          type="email"
          placeholder="you@example.com"
          value={formData.email}
          onChange={handleChange}
          required
          className="h-10 bg-input text-foreground placeholder:text-muted-foreground border-border focus:ring-2 focus:ring-primary"
        />
      </div>

      {/* Password Field */}
      <div className="space-y-2">
        <Label htmlFor="password" className="text-sm font-medium">
          Password
        </Label>
        <div className="relative">
          <Input
            id="password"
            name="password"
            type={showPassword ? "text" : "password"}
            placeholder="••••••••"
            value={formData.password}
            onChange={handleChange}
            required
            className="h-10 bg-input text-foreground placeholder:text-muted-foreground border-border focus:ring-2 focus:ring-primary pr-10"
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
      </div>

      {/* Remember Me & Forgot Password */}
      <div className="flex items-center justify-between pt-1">
        <label className="flex items-center gap-2 cursor-pointer">
          <Checkbox name="rememberMe" checked={formData.rememberMe} onChange={handleChange} className="h-4 w-4" />
          <span className="text-sm text-muted-foreground">Remember me</span>
        </label>
        <a href="#" className="text-sm text-primary hover:text-accent transition-colors font-medium">
          Forgot password?
        </a>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-3 bg-destructive/10 border border-destructive/30 rounded-lg text-sm text-destructive">
          {error}
        </div>
      )}

      {/* Login Button */}
      <Button
        type="submit"
        disabled={isLoading}
        className="w-full h-10 bg-primary text-primary-foreground hover:bg-primary/90 font-medium transition-all duration-200"
      >
        {isLoading ? "Logging in..." : "Login"}
      </Button>

      {/* Divider */}
      <div className="relative py-2">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-border" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-3 text-muted-foreground">or</span>
        </div>
      </div>

      {/* Google Button */}
      <Button
        type="button"
        variant="outline"
        onClick={handleGoogleLogin}
        disabled={isLoading}
        className="w-full h-10 border-border hover:bg-muted transition-colors bg-transparent"
      >
        <svg className="w-4 h-4 mr-2" viewBox="0 0 24 24">
          <path
            fill="currentColor"
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
          />
          <path
            fill="currentColor"
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          />
          <path
            fill="currentColor"
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
          />
          <path
            fill="currentColor"
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
          />
        </svg>
        Continue with Google
      </Button>
    </form>
  )
}
