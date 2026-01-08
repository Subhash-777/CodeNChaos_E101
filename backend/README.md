# Productivity Dashboard Backend

FastAPI backend that connects to Ollama for AI-powered work assistant with Google Calendar & Gmail integration.

## Features

- **Ollama Integration**: Uses `qwen2.5:3b-instruct` model on `localhost:11434`
- **Google Calendar & Gmail**: Real-time integration with Google APIs
- **Synthetic Data Training**: Few-shot learning examples for better responses
- **Privacy-Safe**: Sanitized data before sending to LLM
- **Mock Data Fallback**: Works with mock.json if Google sync hasn't run

## Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Install and Start Ollama:**
   - Install Ollama: https://ollama.ai
   - Start Ollama service: `ollama serve` (usually runs automatically)
   - Pull the model: `ollama pull qwen2.5:3b-instruct`
   - Verify: `ollama list` (should show qwen2.5:3b-instruct)

3. **Google Integration Setup** (Optional):
   - Follow instructions in `GOOGLE_SETUP.md`
   - Download `credentials.json` from Google Cloud Console
   - Place it in the `backend/` directory

4. **Start the FastAPI server:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Verify the connection:**
   - Backend API: http://localhost:8000
   - Health check: http://localhost:8000/health
   - API docs: http://localhost:8000/docs

## Testing

Test the Ollama connection:
```bash
cd backend
python test_connection.py
```

## API Endpoints

### Core Endpoints
- `POST /assistant` - Send a query to the AI assistant
- `GET /api/dashboard` - Get all dashboard data
- `GET /api/contexts` - Get work contexts
- `GET /api/tasks` - Get prioritized tasks
- `GET /api/cognitive-load` - Get cognitive load metrics
- `GET /api/insights` - Get behavioral insights
- `GET /api/recommendations` - Get recommendations

### Google Integration Endpoints
- `GET /api/google/auth` - Trigger Google OAuth authentication
- `POST /api/google/sync` - Manually sync Google Calendar & Gmail data
- `GET /api/google/status` - Check Google connection status

## Configuration

- **Ollama URL**: `http://localhost:11434` (default, set via `OLLAMA_URL` env var)
- **Model name**: `qwen2.5:3b-instruct` (default, set via `OLLAMA_MODEL` env var)
- **Synthetic Data**: Disabled by default (set `USE_SYNTHETIC_DATA=true` to enable)
- **Frontend URL**: `http://localhost:3000` (CORS allowed)

### Environment Variables

```bash
# Ollama configuration
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=qwen2.5:3b-instruct

# Enable synthetic data for training (optional)
export USE_SYNTHETIC_DATA=true
```

## Data Sources

The backend loads data from multiple sources (in priority order):

1. **Google Calendar & Gmail** (if synced)
   - Stored in: `backend/data/calendar.json` and `backend/data/emails.json`
   - Fetched via: `POST /api/google/sync`

2. **Mock Data** (fallback)
   - Stored in: `backend/mock.json`
   - Used when Google sync hasn't run

All data is automatically processed by existing intelligence layers:
- Context Detection
- Task Extraction
- Priority Scoring
- Cognitive Load Estimation
- Behavioral Analysis

## Files Structure

```
backend/
├── main.py                 # FastAPI application
├── mock.json              # Mock data (emails, calendar, tasks)
├── credentials.json       # Google OAuth credentials (download from Google Cloud)
├── token.json            # Saved OAuth token (auto-generated)
├── data/                 # Synced Google data
│   ├── calendar.json     # Calendar events
│   └── emails.json       # Email metadata
├── services/
│   ├── google_sync.py    # Google API integration
│   ├── data_loader.py    # Unified data loading
│   └── privacy.py        # Privacy sanitization
└── requirements.txt      # Python dependencies
```

## Next Steps

See `GOOGLE_SETUP.md` for detailed Google integration instructions.
