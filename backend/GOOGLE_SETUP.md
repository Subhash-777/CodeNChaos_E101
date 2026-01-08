# Google Calendar & Gmail Integration Setup Guide

## Phase 1: Google Cloud Console Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on project dropdown → "New Project"
3. Project name: `Work Intelligence System`
4. Click "Create"

### Step 2: Enable APIs

1. In the project, go to **APIs & Services** → **Library**
2. Search for and enable:
   - **Google Calendar API**
   - **Gmail API**

### Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. If prompted, configure OAuth consent screen:
   - User Type: **External** (or Internal if you have Google Workspace)
   - App name: `Work Intelligence System`
   - User support email: Your email
   - Developer contact: Your email
   - Add scopes:
     - `https://www.googleapis.com/auth/calendar.readonly`
     - `https://www.googleapis.com/auth/gmail.readonly`
   - Save and continue through remaining steps
4. Application type: **Desktop app**
5. Name: `Work Intelligence Desktop Client`
6. Click **Create**
7. **Download** the credentials JSON file
8. Rename it to `credentials.json`
9. Move it to the `backend/` directory

### Step 4: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`

## Phase 2: First-Time Authentication

### Step 1: Connect Google Account

1. Start your backend server:
   ```bash
   cd backend
   python main.py
   ```

2. In your browser or frontend, click **"Connect Google"** button
   - Or call: `GET http://localhost:8000/api/google/auth`

3. Your browser will open for Google OAuth login
4. Sign in and grant permissions (Calendar read-only, Gmail read-only)
5. Token will be saved to `backend/token.json`

### Step 2: Sync Data

1. Click **"Sync Now"** button in the frontend
   - Or call: `POST http://localhost:8000/api/google/sync`

2. Data will be fetched and saved to:
   - `backend/data/calendar.json`
   - `backend/data/emails.json`

## API Endpoints

### `GET /api/google/auth`
- Triggers OAuth flow for first-time authentication
- Opens browser for Google login
- Saves token for future use

### `POST /api/google/sync`
- Manually triggers data refresh
- Fetches latest calendar events and emails
- Returns sync statistics

### `GET /api/google/status`
- Checks if Google is connected
- Returns last sync time and data availability

## Data Flow

```
User clicks "Sync Now"
  ↓
POST /api/google/sync
  ↓
fetch_calendar_events() + fetch_gmail_emails()
  ↓
Save to data/calendar.json + data/emails.json
  ↓
load_work_items() reads Google data
  ↓
Existing endpoints (/contexts, /tasks, etc.) return enriched data
  ↓
Frontend displays real Google Calendar + Gmail data
```

## Privacy & Security

- Only **read-only** access (Calendar & Gmail)
- Email content limited to **200 characters** (preview only)
- Full content never sent to LLM
- Token stored locally in `token.json` (add to `.gitignore`)

## Troubleshooting

### "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Place in `backend/` directory
- Ensure file is named exactly `credentials.json`

### "Authentication failed"
- Check that APIs are enabled in Google Cloud Console
- Verify OAuth consent screen is configured
- Ensure scopes are added to consent screen

### "No data synced"
- Check token.json exists and is valid
- Verify you have calendar events/emails in your Google account
- Check backend logs for API errors

### Token expired
- Delete `token.json` and re-authenticate
- Or tokens will auto-refresh if refresh token is valid

## File Structure

```
backend/
├── credentials.json      # OAuth credentials (download from Google Cloud)
├── token.json            # Saved OAuth token (auto-generated)
├── data/
│   ├── calendar.json     # Synced calendar events
│   └── emails.json       # Synced email metadata
└── services/
    ├── google_sync.py    # Google API integration
    ├── data_loader.py    # Unified data loading
    └── privacy.py        # Privacy sanitization
```

## Next Steps

After setup:
1. The dashboard will automatically use Google data when available
2. Fallback to mock.json if Google sync hasn't run
3. All existing features work with real Google data
4. LLM assistant can answer questions about your real calendar and emails
