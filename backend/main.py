from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta

app = FastAPI(title="Productivity Dashboard API")

# CORS middleware to allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to LM Studio local server
# Use environment variable or default to localhost
import os
import httpx

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://10.187.15.14:1234/v1")

# Create httpx client without proxies to avoid initialization errors
# Note: httpx.Client doesn't take base_url, OpenAI client handles that
http_client = httpx.Client(
    proxies=None,  # Explicitly disable proxies
    timeout=60.0
)

client = OpenAI(
    base_url=LM_STUDIO_URL,
    api_key="not-needed",
    http_client=http_client
)


class AssistantQuery(BaseModel):
    query: str


# Mock data functions - replace with actual database calls later
def get_active_contexts() -> List[Dict[str, Any]]:
    """Fetch from your SQLite/JSON storage"""
    return [
        {
            "id": "ctx_hackathon",
            "name": "Hackathon Review",
            "related_items": ["email_01", "doc_02", "meeting_01"],
            "urgency": "high",
            "deadline": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "tasks": ["Finalize proposal deck", "Schedule team sync", "Prepare demo materials"]
        },
        {
            "id": "ctx_college",
            "name": "College",
            "related_items": ["doc_05", "email_03"],
            "urgency": "medium",
            "deadline": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "tasks": ["Complete research paper", "Prepare presentation", "Review syllabus updates"]
        }
    ]


def get_prioritized_tasks() -> List[Dict[str, Any]]:
    """Fetch from your task extraction layer"""
    return [
        {
            "id": "task_01",
            "title": "Review and approve design mockups",
            "context": "Hackathon Review",
            "deadline": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "priority_score": 87,
            "status": "in_progress",
            "explanation": "Design team is waiting for feedback to proceed with development. Deadline tomorrow + high importance"
        },
        {
            "id": "task_02",
            "title": "Prepare budget forecast",
            "context": "Hackathon Review",
            "deadline": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "priority_score": 75,
            "status": "not_started",
            "explanation": "Q1 planning meeting is tomorrow morning"
        },
        {
            "id": "task_03",
            "title": "Complete research paper",
            "context": "College",
            "deadline": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "priority_score": 65,
            "status": "not_started",
            "explanation": "Due in 7 days + medium importance"
        },
        {
            "id": "task_04",
            "title": "Sync with product team",
            "context": "Hackathon Review",
            "deadline": None,
            "priority_score": 55,
            "status": "not_started",
            "explanation": "Outstanding action items from weekly standup"
        }
    ]


def get_cognitive_load() -> Dict[str, Any]:
    """Fetch from your cognitive load estimator"""
    return {
        "score": 78,
        "status": "High",
        "active_contexts": 2,
        "urgent_tasks": 2,
        "switches": 12,
        "breakdown": "2 parallel contexts + 2 urgent deadlines + 12 switches today"
    }


def get_latest_insights() -> List[Dict[str, Any]]:
    """Fetch from behavioral analysis layer"""
    return [
        {
            "type": "context_switching",
            "severity": "high",
            "count": 12,
            "message": "You switched between contexts 12 times today, losing ~4 hours of focus time"
        },
        {
            "type": "ignored_priority",
            "severity": "medium",
            "task": "Review and approve design mockups",
            "message": "Design mockups review (high priority) has no activity for 2 days"
        },
        {
            "type": "deadline_proximity",
            "severity": "high",
            "tasks": ["Review and approve design mockups", "Prepare budget forecast"],
            "message": "2 tasks with deadlines tomorrow need immediate attention"
        }
    ]


def get_recommendations() -> List[Dict[str, Any]]:
    """Fetch from recommendation engine"""
    return [
        {
            "action": "Block 9-11 AM tomorrow for Hackathon Review only",
            "reason": "Deadline tomorrow + high switching detected",
            "expected_impact": "Complete design review and budget forecast in single focus session"
        },
        {
            "action": "Defer College tasks to next week",
            "reason": "Reduce cognitive load from 78 to ~50",
            "expected_impact": "Lower stress and finish urgent work first"
        },
        {
            "action": "Batch all Hackathon Review tasks together",
            "reason": "Minimize context switching between related work",
            "expected_impact": "Complete 3 tasks in 2 hours instead of 4 hours"
        }
    ]


@app.get("/")
async def root():
    return {"message": "Productivity Dashboard API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/assistant")
async def ask_assistant(request: AssistantQuery):
    try:
        # Fetch current system state from your database/storage
        contexts = get_active_contexts()
        tasks = get_prioritized_tasks()
        cognitive_load = get_cognitive_load()
        insights = get_latest_insights()
        recommendations = get_recommendations()
        
        # Format data for the prompt
        system_prompt = f"""You are an intelligent work assistant analyzing a user's digital work environment.

=== SYSTEM DATA ===

ACTIVE CONTEXTS:
{json.dumps(contexts, indent=2)}

TASKS BY PRIORITY:
{json.dumps(tasks, indent=2)}

COGNITIVE LOAD ANALYSIS:
Current Score: {cognitive_load['score']}/100
Status: {cognitive_load['status']}
Contributing Factors:
- Active Contexts: {cognitive_load['active_contexts']}
- Urgent Tasks: {cognitive_load['urgent_tasks']}
- Recent Context Switches: {cognitive_load['switches']}

BEHAVIORAL INSIGHTS:
{json.dumps(insights, indent=2)}

RECOMMENDATIONS:
{json.dumps(recommendations, indent=2)}

=== YOUR ROLE ===
You help users understand their work patterns and make better decisions.

RULES:
1. Answer ONLY using the system data above - never invent information
2. Always cite specific context names, task titles, and metric values
3. Explain WHY something matters by referencing the data
4. Be concise and actionable (2-3 sentences max unless asked for details)
5. If asked about something not in the data, say "I don't have that information in your current work data"
6. Use natural language, avoid jargon like "context_id" - say "your Hackathon Review project" instead

RESPONSE STYLE:
- Direct and helpful
- Reference specific work items by name
- Explain the "why" behind insights
- Suggest concrete next actions"""

        # Call LM Studio model
        # Use environment variable or default model name
        model_name = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct-1m")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.query}
            ],
            temperature=0.7,  # Balanced creativity
            max_tokens=300,   # Keep responses concise
        )
        
        return {
            "response": response.choices[0].message.content,
            "context_used": {
                "contexts": len(contexts),
                "tasks": len(tasks),
                "load_score": cognitive_load['score']
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
