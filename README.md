## Productivity Dashboard

An AI-powered productivity dashboard that combines your Google Calendar, Gmail, and real‑time behavioral signals to surface high‑impact work, explain your cognitive load, and recommend what to do next.

The project is split into a **Next.js 16 + Firebase** frontend and a **FastAPI + Ollama** backend, connected via JSON APIs.

---

## Features

- **Personalized dashboard**: Work contexts, prioritized tasks, cognitive load, and behavioral insights that refresh automatically.
- **Real‑time updates**: Frontend auto‑refreshes key widgets every 30 seconds, with a manual **Refresh** button.
- **Google integration**: Optional Google Calendar + Gmail sync, stored locally on disk and used to enrich the dashboard.
- **AI work assistant**: Backend connects to Ollama (`qwen2.5:3b-instruct`) to answer questions about your current work state.
- **Authentication**: Firebase Auth (email/password + Google) with user‑specific data isolation from backend to UI.

---

## Tech Stack

- **Frontend**: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Radix UI, shadcn‑style components.
- **Backend**: FastAPI, Python 3, httpx, Google API client libraries.
- **AI**: Ollama running locally (`qwen2.5:3b-instruct`).
- **Auth**: Firebase Authentication (web SDK).

See `ARCHITECTURE_DIAGRAM.md` for a deeper system overview.

---

## Project Structure

```text
app/                # Next.js app (frontend)
backend/            # FastAPI service (APIs, Google, Ollama)
components/         # Reusable UI components (Dashboard, AI chat, etc.)
hooks/              # React hooks (auth, toasts, mobile)
lib/                # Frontend helpers (API client, Firebase, context providers)
styles/             # Global styles
```

Additional docs:

- `QUICK_START.md` – how dynamic updates & multi‑user data work in the UI.
- `ARCHITECTURE_DIAGRAM.md` – end‑to‑end data flow.
- `backend/README.md` – backend and Ollama details.
- `FIREBASE_SETUP.md` – configuring Firebase auth.
- `backend/GOOGLE_SETUP.md` – Google Calendar & Gmail integration.

---

## Prerequisites

- **Node.js** 18+ (recommended) with **pnpm** or **npm**
- **Python** 3.10+ with `pip`
- **Ollama** installed and running locally (for AI features)
- Google + Firebase accounts if you want real data (optional; mock data works out of the box)

---

## Setup

### 1. Frontend (Next.js)

```bash
cd /home/subhash/Projects/productivity-dashboard
pnpm install        # or npm install
```

If you want authentication to work, configure Firebase as described in `FIREBASE_SETUP.md`:

1. Create a Firebase project and web app.
2. Copy `.env.example` to `.env.local`.
3. Fill in your `NEXT_PUBLIC_FIREBASE_*` values.

Start the dev server:

```bash
pnpm dev            # runs Next.js on http://localhost:3000
```

Visit:

- `http://localhost:3000` – auth & landing.
- `http://localhost:3000/dashboard` – main productivity dashboard.

### 2. Backend (FastAPI + Ollama)

```bash
cd /home/subhash/Projects/productivity-dashboard/backend
pip install -r requirements.txt
```

Install and start Ollama, then pull the model:

```bash
ollama pull qwen2.5:3b-instruct
ollama serve    # if not already running
```

Run the backend:

```bash
python main.py          # FastAPI on http://localhost:8000
```

Key endpoints:

- `GET /health` – health + Ollama status.
- `GET /api/dashboard` – aggregate dashboard data.
- `POST /assistant` – AI assistant using your current work state.

See `backend/README.md` for full backend and environment variable details.

### 3. Google Calendar & Gmail (Optional)

To use your real calendar and email data instead of mock data:

1. Follow `backend/GOOGLE_SETUP.md` to:
   - Create a Google Cloud project.
   - Enable Calendar & Gmail APIs.
   - Download `credentials.json` into `backend/`.
2. Start the backend.
3. From the frontend or a REST client:
   - Call `GET /api/google/auth` once to complete OAuth.
   - Call `POST /api/google/sync` or click the **Sync** button in the UI.

Synced data is stored under `backend/data/` and is user‑specific.

---

## Using the Dashboard

- **Login** via Firebase and navigate to `/dashboard`.
- The dashboard:
  - Auto‑refreshes contexts, tasks, insights, and cognitive load every **30 seconds**.
  - Lets you trigger an immediate refresh via the **Refresh** button.
  - Lets you sync Google data via the **Sync** button (if configured).
- Multiple logged‑in users see **different, isolated data**; see `QUICK_START.md` for test scenarios.

---

## Testing & Troubleshooting

- Run dynamic‑update checks:

```bash
cd /home/subhash/Projects/productivity-dashboard
bash test-dynamic-updates.sh
```

- If the dashboard is not updating:
  - Ensure the backend is running on `http://localhost:8000`.
  - Open browser DevTools → **Console** & **Network**; verify `/api/*` requests.
  - See `QUICK_START.md` and `DYNAMIC_UPDATES_FIX.md` for detailed debugging steps.

---


