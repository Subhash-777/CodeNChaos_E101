# Productivity Dashboard Backend

FastAPI backend that connects to Ollama for AI-powered work assistant with synthetic data training.

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

3. **Configure environment variables (optional):**
   ```bash
   export OLLAMA_URL=http://localhost:11434
   export OLLAMA_MODEL=qwen2.5:3b-instruct
   export USE_SYNTHETIC_DATA=false  # Set to true to include synthetic training data
   ```

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

Or test manually:
```bash
curl http://localhost:11434/api/tags
curl -X POST http://localhost:11434/api/chat -d '{
  "model": "qwen2.5:3b-instruct",
  "messages": [{"role": "user", "content": "Hello!"}],
  "stream": false
}'
```

## API Endpoints

- `POST /assistant` - Send a query to the AI assistant
  - Request body: `{"query": "What should I focus on today?"}`
  - Returns: `{"response": "...", "context_used": {...}}`

- `GET /health` - Health check endpoint (also tests Ollama connection)

- `GET /` - API info and status

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

## Synthetic Data Training

The backend includes synthetic data generation for few-shot learning:

- **Training Examples**: Built-in examples showing proper response format
- **Synthetic Contexts**: Generated work contexts for training
- **Synthetic Tasks**: Generated tasks with various priorities and deadlines
- **Synthetic Insights**: Generated behavioral insights

Enable synthetic data by setting `USE_SYNTHETIC_DATA=true`. This merges synthetic data with real mock data to provide more training context to the model.

## Mock Data

All mock data functions are in `main.py`:
- `get_active_contexts()` - Returns work contexts
- `get_prioritized_tasks()` - Returns prioritized tasks
- `get_cognitive_load()` - Returns cognitive load metrics
- `get_latest_insights()` - Returns behavioral insights
- `get_recommendations()` - Returns action recommendations

## Next Steps

Replace the mock data functions with actual database queries when you have your data storage set up.
