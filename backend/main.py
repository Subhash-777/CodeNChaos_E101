from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import httpx
from typing import List, Dict, Any
from datetime import datetime, timedelta
import os
import random

app = FastAPI(title="Productivity Dashboard API")

# CORS middleware to allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")


class AssistantQuery(BaseModel):
    query: str


# ============================================================================
# MOCK DATA FUNCTIONS - All data is in this file as requested
# ============================================================================

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


# ============================================================================
# SYNTHETIC DATA GENERATION FOR TRAINING
# ============================================================================

def generate_synthetic_contexts(count: int = 5) -> List[Dict[str, Any]]:
    """Generate synthetic work contexts for training examples"""
    context_templates = [
        {"name": "Project Alpha", "urgency": "high", "type": "software"},
        {"name": "Marketing Campaign", "urgency": "medium", "type": "marketing"},
        {"name": "Client Presentation", "urgency": "high", "type": "sales"},
        {"name": "Quarterly Review", "urgency": "medium", "type": "analysis"},
        {"name": "Team Training", "urgency": "low", "type": "hr"},
    ]
    
    synthetic = []
    for i in range(count):
        template = random.choice(context_templates)
        synthetic.append({
            "id": f"ctx_synth_{i+1}",
            "name": template["name"],
            "urgency": template["urgency"],
            "deadline": (datetime.now() + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d"),
            "tasks": [f"Task {j+1} for {template['name']}" for j in range(random.randint(2, 4))]
        })
    return synthetic


def generate_synthetic_tasks(count: int = 8) -> List[Dict[str, Any]]:
    """Generate synthetic tasks for training examples"""
    task_templates = [
        {"title": "Review documentation", "context": "Project Alpha"},
        {"title": "Prepare meeting agenda", "context": "Marketing Campaign"},
        {"title": "Update project timeline", "context": "Client Presentation"},
        {"title": "Analyze data metrics", "context": "Quarterly Review"},
        {"title": "Schedule training sessions", "context": "Team Training"},
    ]
    
    synthetic = []
    for i in range(count):
        template = random.choice(task_templates)
        synthetic.append({
            "id": f"task_synth_{i+1}",
            "title": template["title"],
            "context": template["context"],
            "deadline": (datetime.now() + timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d"),
            "priority_score": random.randint(50, 95),
            "status": random.choice(["not_started", "in_progress", "completed"]),
            "explanation": f"Generated task for {template['context']} with priority {random.randint(50, 95)}"
        })
    return synthetic


def generate_synthetic_insights(count: int = 4) -> List[Dict[str, Any]]:
    """Generate synthetic behavioral insights for training"""
    insight_types = [
        {"type": "context_switching", "severity": "high", "message": "High context switching detected"},
        {"type": "deadline_proximity", "severity": "medium", "message": "Multiple deadlines approaching"},
        {"type": "ignored_priority", "severity": "low", "message": "Some high-priority tasks need attention"},
        {"type": "focus_time", "severity": "medium", "message": "Focus time decreased this week"},
    ]
    
    synthetic = []
    for i in range(count):
        insight = random.choice(insight_types)
        synthetic.append({
            "type": insight["type"],
            "severity": insight["severity"],
            "count": random.randint(5, 20) if insight["type"] == "context_switching" else None,
            "message": insight["message"]
        })
    return synthetic


def get_synthetic_training_examples() -> str:
    """Generate synthetic training examples for few-shot learning"""
    examples = []
    
    # Example 1: Focus recommendation
    examples.append({
        "user_query": "What should I focus on today?",
        "assistant_response": "Focus on your Project Alpha tasks first - you have 2 urgent deadlines tomorrow with priority scores of 87 and 75. Your cognitive load is at 78/100 (High) due to 12 context switches today. I recommend blocking 9-11 AM for uninterrupted work on Project Alpha to complete both tasks in a single focus session."
    })
    
    # Example 2: Cognitive load explanation
    examples.append({
        "user_query": "Why is my cognitive load high?",
        "assistant_response": "Your cognitive load is at 78/100 (High) because you're managing 2 parallel contexts (Project Alpha and Marketing Campaign) with 2 urgent deadlines. The main contributor is 12 context switches today, which fragments your focus. Consider deferring Marketing Campaign tasks to next week to reduce your load to around 50."
    })
    
    # Example 3: Task prioritization
    examples.append({
        "user_query": "What's my biggest productivity issue?",
        "assistant_response": "Context switching - you switched between projects 12 times today, losing approximately 4 hours of focus time. Each switch costs 15-20 minutes of recovery time. Try batching similar tasks and blocking dedicated time for your Project Alpha work to reduce this."
    })
    
    # Format examples for prompt
    formatted = "\n\n=== TRAINING EXAMPLES ===\n"
    for i, ex in enumerate(examples, 1):
        formatted += f"\nExample {i}:\n"
        formatted += f"User: {ex['user_query']}\n"
        formatted += f"Assistant: {ex['assistant_response']}\n"
    
    return formatted


# ============================================================================
# OLLAMA API CLIENT
# ============================================================================

async def call_ollama(messages: List[Dict[str, str]], model: str = None) -> str:
    """Call Ollama API with chat messages"""
    model = model or OLLAMA_MODEL
    url = f"{OLLAMA_URL}/api/chat"
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 300,  # max_tokens equivalent
        }
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "No response generated")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "Productivity Dashboard API",
        "status": "running",
        "ollama_url": OLLAMA_URL,
        "model": OLLAMA_MODEL
    }


@app.get("/health")
async def health():
    # Test Ollama connection
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()
            return {
                "status": "healthy",
                "ollama_connected": True,
                "model": OLLAMA_MODEL
            }
    except Exception as e:
        return {
            "status": "degraded",
            "ollama_connected": False,
            "error": str(e)
        }


@app.post("/assistant")
async def ask_assistant(request: AssistantQuery):
    try:
        # Fetch current system state from your database/storage
        contexts = get_active_contexts()
        tasks = get_prioritized_tasks()
        cognitive_load = get_cognitive_load()
        insights = get_latest_insights()
        recommendations = get_recommendations()
        
        # Get synthetic training examples
        training_examples = get_synthetic_training_examples()
        
        # Generate additional synthetic data for context (optional, can be toggled)
        use_synthetic_data = os.getenv("USE_SYNTHETIC_DATA", "false").lower() == "true"
        if use_synthetic_data:
            synthetic_contexts = generate_synthetic_contexts(3)
            synthetic_tasks = generate_synthetic_tasks(5)
            synthetic_insights = generate_synthetic_insights(2)
            # Merge with real data (or use only synthetic for training)
            all_contexts = contexts + synthetic_contexts
            all_tasks = tasks + synthetic_tasks
            all_insights = insights + synthetic_insights
        else:
            all_contexts = contexts
            all_tasks = tasks
            all_insights = insights
        
        # Format data for the prompt with training examples
        system_prompt = f"""You are an intelligent work assistant analyzing a user's digital work environment.

{training_examples}

=== CURRENT SYSTEM DATA ===

ACTIVE CONTEXTS:
{json.dumps(all_contexts, indent=2)}

TASKS BY PRIORITY:
{json.dumps(all_tasks, indent=2)}

COGNITIVE LOAD ANALYSIS:
Current Score: {cognitive_load['score']}/100
Status: {cognitive_load['status']}
Contributing Factors:
- Active Contexts: {cognitive_load['active_contexts']}
- Urgent Tasks: {cognitive_load['urgent_tasks']}
- Recent Context Switches: {cognitive_load['switches']}

BEHAVIORAL INSIGHTS:
{json.dumps(all_insights, indent=2)}

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
7. Follow the style and format of the training examples above

RESPONSE STYLE:
- Direct and helpful
- Reference specific work items by name
- Explain the "why" behind insights
- Suggest concrete next actions
- Match the tone and structure of the training examples"""

        # Call Ollama model
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.query}
        ]
        
        response_text = await call_ollama(messages, OLLAMA_MODEL)
        
        return {
            "response": response_text,
            "context_used": {
                "contexts": len(all_contexts),
                "tasks": len(all_tasks),
                "load_score": cognitive_load['score'],
                "synthetic_data_enabled": use_synthetic_data
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard")
async def get_dashboard_data():
    """Get all dashboard data in one endpoint"""
    try:
        contexts = get_active_contexts()
        tasks = get_prioritized_tasks()
        cognitive_load = get_cognitive_load()
        insights = get_latest_insights()
        recommendations = get_recommendations()
        
        return {
            "contexts": contexts,
            "tasks": tasks,
            "cognitive_load": cognitive_load,
            "insights": insights,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/contexts")
async def get_contexts():
    """Get active work contexts"""
    try:
        return {"contexts": get_active_contexts()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks")
async def get_tasks():
    """Get prioritized tasks"""
    try:
        return {"tasks": get_prioritized_tasks()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cognitive-load")
async def get_cognitive_load_data():
    """Get cognitive load metrics"""
    try:
        return {"cognitive_load": get_cognitive_load()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/insights")
async def get_insights():
    """Get behavioral insights"""
    try:
        return {"insights": get_latest_insights()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations")
async def get_recommendations_data():
    """Get recommendations"""
    try:
        return {"recommendations": get_recommendations()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
