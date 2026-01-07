# Productivity Dashboard Backend

FastAPI backend that connects to LM Studio for AI-powered work assistant.

## Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start LM Studio:**
   - Open LM Studio
   - Load a model (e.g., `qwen2.5-7b-instruct-1m`)
   - Go to Developer tab → Click "Start Server"
   - Note the server address (e.g., `http://10.187.15.14:1234` or `http://127.0.0.1:1234`)
   - Set environment variable if using a different address:
     ```bash
     export LM_STUDIO_URL=http://your-ip:1234/v1
     export LM_STUDIO_MODEL=qwen2.5-7b-instruct-1m
     ```

3. **Start the FastAPI server:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Verify the connection:**
   - Backend API: http://localhost:8000
   - Health check: http://localhost:8000/health
   - API docs: http://localhost:8000/docs

## Testing

Test the LM Studio connection:
```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="qwen2.5-7b-instruct",
    messages=[
        {"role": "user", "content": "Hello, are you working?"}
    ]
)

print(response.choices[0].message.content)
```

## API Endpoints

- `POST /assistant` - Send a query to the AI assistant
  - Request body: `{"query": "What should I focus on today?"}`
  - Returns: `{"response": "...", "context_used": {...}}`

- `GET /health` - Health check endpoint

## Configuration

- LM Studio URL: `http://10.187.15.14:1234/v1` (default, set via `LM_STUDIO_URL` env var)
- Model name: `qwen2.5-7b-instruct-1m` (default, set via `LM_STUDIO_MODEL` env var)
- Frontend URL: `http://localhost:3000` (CORS allowed)

### Environment Variables

You can configure the backend using environment variables:

```bash
export LM_STUDIO_URL=http://10.187.15.14:1234/v1
export LM_STUDIO_MODEL=qwen2.5-7b-instruct-1m
```

Or create a `.env` file in the backend directory (requires `python-dotenv` package).

## Next Steps

Replace the mock data functions (`get_active_contexts`, `get_prioritized_tasks`, etc.) with actual database queries when you have your data storage set up.
