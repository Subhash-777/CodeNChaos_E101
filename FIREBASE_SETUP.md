# Firebase Setup Guide

## Getting Your Firebase API Keys

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Go to Project Settings (gear icon) → General tab
4. Scroll down to "Your apps" section
5. Click on the Web app icon (`</>`) to add a web app
6. Register your app and copy the Firebase configuration

## Setting Up Environment Variables

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. Open `.env.local` and replace the placeholder values with your Firebase credentials:
   ```env
   NEXT_PUBLIC_FIREBASE_API_KEY=your-actual-api-key
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
   NEXT_PUBLIC_FIREBASE_APP_ID=your-app-id
   ```

## Enabling Google Authentication

1. In Firebase Console, go to **Authentication** → **Sign-in method**
2. Click on **Google** provider
3. Enable it and set your project support email
4. Save the changes

## Installing Dependencies

After adding Firebase to `package.json`, install it:
```bash
npm install
# or
pnpm install
```

## Testing

1. Start the development server:
   ```bash
   pnpm dev
   ```

2. Navigate to `http://localhost:3000`
3. You should see the login/signup page
4. Try logging in with email/password or Google

## Troubleshooting

### Authentication Not Working

1. **Check Browser Console**: Open browser DevTools (F12) and check the Console tab for any Firebase errors

2. **Verify Environment Variables**: Make sure your `.env.local` file has all the required variables:
   ```bash
   # Check if variables are loaded
   echo $NEXT_PUBLIC_FIREBASE_API_KEY
   ```

3. **Restart Dev Server**: After adding/changing environment variables, restart your Next.js dev server:
   ```bash
   # Stop the server (Ctrl+C) and restart
   pnpm dev
   ```

4. **Check Firebase Console**:
   - Go to Firebase Console → Authentication → Sign-in method
   - Ensure Email/Password is enabled
   - Ensure Google provider is enabled
   - Check authorized domains (localhost should be included by default)

5. **Common Errors**:
   - "Firebase is not configured" → Check your `.env.local` file
   - "Popup blocked" → Allow popups in your browser
   - "auth/unauthorized-domain" → Add your domain to Firebase authorized domains
   - "auth/api-key-not-valid" → Check your API key in Firebase Console

6. **Enable Email/Password Authentication**:
   - Firebase Console → Authentication → Sign-in method
   - Click on "Email/Password"
   - Enable "Email/Password" toggle
   - Save

7. **Enable Google Authentication**:
   - Firebase Console → Authentication → Sign-in method
   - Click on "Google"
   - Enable the toggle
   - Set project support email
   - Save

## Notes

- The Firebase configuration is in `lib/firebase.ts`
- Login/Signup forms are in `components/login-form.tsx` and `components/signup-form.tsx`
- After successful authentication, users are redirected to `/dashboard`
- Check browser console for detailed error messages if authentication fails