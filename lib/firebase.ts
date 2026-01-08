// Firebase configuration with placeholders
// Replace these with your actual Firebase API keys

import { initializeApp, getApps, FirebaseApp } from "firebase/app"
import { getAuth, GoogleAuthProvider, Auth } from "firebase/auth"

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "YOUR_API_KEY_HERE",
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "YOUR_AUTH_DOMAIN_HERE",
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || "YOUR_PROJECT_ID_HERE",
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || "YOUR_STORAGE_BUCKET_HERE",
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "YOUR_MESSAGING_SENDER_ID_HERE",
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || "YOUR_APP_ID_HERE",
}

// Validate Firebase configuration
const isFirebaseConfigured = () => {
  return (
    firebaseConfig.apiKey &&
    firebaseConfig.apiKey !== "YOUR_API_KEY_HERE" &&
    firebaseConfig.authDomain &&
    firebaseConfig.authDomain !== "YOUR_AUTH_DOMAIN_HERE" &&
    firebaseConfig.projectId &&
    firebaseConfig.projectId !== "YOUR_PROJECT_ID_HERE"
  )
}

// Initialize Firebase only if not already initialized
let app: FirebaseApp
if (getApps().length === 0) {
  if (!isFirebaseConfigured()) {
    console.error(
      "⚠️ Firebase is not properly configured. Please add your Firebase credentials to .env.local"
    )
    console.error("See FIREBASE_SETUP.md for instructions")
  }
  app = initializeApp(firebaseConfig)
} else {
  app = getApps()[0]
}

// Initialize Firebase Authentication and get a reference to the service
export const auth: Auth = getAuth(app)

// Google Auth Provider with additional scopes
export const googleProvider = new GoogleAuthProvider()
googleProvider.setCustomParameters({
  prompt: "select_account",
})

// Export Firebase app and validation function
export { app }
export const isConfigured = isFirebaseConfigured

// Log configuration status (only in development)
if (process.env.NODE_ENV === "development") {
  if (isFirebaseConfigured()) {
    console.log("✅ Firebase is configured")
  } else {
    console.warn("⚠️ Firebase configuration incomplete - authentication will not work")
  }
}

export default app
