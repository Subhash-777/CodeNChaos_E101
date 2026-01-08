from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import httpx
import hashlib
from typing import List, Dict, Any
from datetime import datetime, timedelta
import os
import random
from pathlib import Path

# Import Google sync services
from services.google_sync import authenticate_google, sync_all_google_data, get_sync_status, disconnect_google
from services.data_loader import load_work_items
from services.privacy import sanitize_for_llm


def get_user_id(request: Request, x_user_id: Optional[str] = Header(None)) -> str:
    """Extract user ID from header, fallback to 'default' for testing"""
    return x_user_id or "default"

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

# Mock data path for fallback
MOCK_DATA_PATH = Path(__file__).parent / "mock.json"

def load_mock_data() -> Dict[str, Any]:
    """Load base mock data from JSON file"""
    try:
        if MOCK_DATA_PATH.exists():
            with open(MOCK_DATA_PATH, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading mock data: {e}")
    
    return {
        "emails": [],
        "calendar": [],
        "tasks": [],
        "documents": [],
        "contexts": [],
        "cognitive_load": {},
        "insights": [],
        "recommendations": []
    }


def get_user_specific_mock_data(user_id: str) -> Dict[str, Any]:
    """Return one of two distinct mock data sets based on user_id"""
    # Import the function from data_loader
    from services.data_loader import get_user_specific_mock_data as get_mock_data
    return get_mock_data(user_id)
    
    # Generate user-specific variations
    user_variations = {
        "names": ["Alex", "Jordan", "Sam", "Taylor", "Casey", "Morgan", "Riley", "Quinn"],
        "projects": ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Echo"],
        "teams": ["Engineering", "Design", "Marketing", "Sales", "Product"],
        "topics": ["API Integration", "UI Redesign", "Market Analysis", "Client Presentation", "Code Review"]
    }
    
    # Select variations based on user hash
    name_idx = user_hash % len(user_variations["names"])
    project_idx = (user_hash // 10) % len(user_variations["projects"])
    team_idx = (user_hash // 100) % len(user_variations["teams"])
    topic_idx = (user_hash // 1000) % len(user_variations["topics"])
    
    user_name = user_variations["names"][name_idx]
    user_project = user_variations["projects"][project_idx]
    user_team = user_variations["teams"][team_idx]
    user_topic = user_variations["topics"][topic_idx]
    
    # Modify emails with user-specific content
    modified_emails = []
    for i, email in enumerate(base_mock.get("emails", [])[:5]):
        email_copy = email.copy()
        email_copy["id"] = f"email_{user_id[:8]}_{i}"
        email_copy["subject"] = email_copy["subject"].replace("Design Mockups", f"{user_topic} Review")
        email_copy["subject"] = email_copy["subject"].replace("Q1 Budget", f"{user_project} Budget")
        email_copy["from"] = email_copy["from"].replace("design-team", f"{user_team.lower()}")
        modified_emails.append(email_copy)
    
    # Modify calendar events with user-specific content
    modified_calendar = []
    for i, event in enumerate(base_mock.get("calendar", [])[:4]):
        event_copy = event.copy()
        event_copy["id"] = f"meeting_{user_id[:8]}_{i}"
        event_copy["title"] = event_copy["title"].replace("Q1 Planning", f"{user_project} Planning")
        event_copy["title"] = event_copy["title"].replace("Design Review", f"{user_topic} Review")
        event_copy["description"] = f"Meeting for {user_name} regarding {user_project}"
        # Shift dates based on user hash to make them different
        days_offset = (user_hash % 7) - 3  # -3 to +3 days
        if event_copy.get("start"):
            try:
                start_dt = datetime.fromisoformat(event_copy["start"].replace("Z", "+00:00"))
                start_dt = start_dt + timedelta(days=days_offset)
                event_copy["start"] = start_dt.isoformat()
                if event_copy.get("end"):
                    end_dt = datetime.fromisoformat(event_copy["end"].replace("Z", "+00:00"))
                    end_dt = end_dt + timedelta(days=days_offset)
                    event_copy["end"] = end_dt.isoformat()
            except:
                pass
        modified_calendar.append(event_copy)
    
    # Modify tasks with user-specific content
    modified_tasks = []
    for i, task in enumerate(base_mock.get("tasks", [])[:5]):
        task_copy = task.copy()
        task_copy["id"] = f"task_{user_id[:8]}_{i}"
        task_copy["title"] = task_copy["title"].replace("design mockups", f"{user_topic} review")
        task_copy["title"] = task_copy["title"].replace("budget forecast", f"{user_project} analysis")
        task_copy["context"] = task_copy["context"].replace("Hackathon Review", user_project)
        # Adjust priority scores based on user hash
        priority_mod = (user_hash % 20) - 10  # -10 to +10
        task_copy["priority_score"] = max(50, min(95, task_copy.get("priority_score", 70) + priority_mod))
        modified_tasks.append(task_copy)
    
    # Modify contexts with user-specific content
    modified_contexts = []
    for i, ctx in enumerate(base_mock.get("contexts", [])[:2]):
        ctx_copy = ctx.copy()
        ctx_copy["id"] = f"ctx_{user_id[:8]}_{i}"
        ctx_copy["name"] = ctx_copy["name"].replace("Hackathon Review", user_project)
        ctx_copy["name"] = ctx_copy["name"].replace("College", f"{user_team} Work")
        modified_contexts.append(ctx_copy)
    
    # Modify cognitive load with user-specific values
    cognitive_load = base_mock.get("cognitive_load", {}).copy()
    load_mod = (user_hash % 30)  # 0 to 30
    cognitive_load["score"] = max(50, min(100, cognitive_load.get("score", 78) + load_mod - 15))
    cognitive_load["status"] = "High" if cognitive_load["score"] >= 75 else "Medium" if cognitive_load["score"] >= 50 else "Low"
    cognitive_load["active_contexts"] = 1 + (user_hash % 3)  # 1-3 contexts
    cognitive_load["urgent_tasks"] = 1 + (user_hash % 3)  # 1-3 urgent tasks
    cognitive_load["switches"] = 5 + (user_hash % 10)  # 5-15 switches
    
    # Modify insights with user-specific content
    modified_insights = []
    for i, insight in enumerate(base_mock.get("insights", [])[:2]):
        insight_copy = insight.copy()
        insight_copy["id"] = f"insight_{user_id[:8]}_{i}"
        insight_copy["count"] = 5 + (user_hash % 10) if insight_copy.get("count") else None
        insight_copy["message"] = insight_copy["message"].replace("12 times", f"{insight_copy.get('count', 10)} times")
        modified_insights.append(insight_copy)
    
    # Modify recommendations with user-specific content
    modified_recommendations = []
    for i, rec in enumerate(base_mock.get("recommendations", [])[:2]):
        rec_copy = rec.copy()
        rec_copy["id"] = f"rec_{user_id[:8]}_{i}"
        rec_copy["action"] = rec_copy["action"].replace("Hackathon Review", user_project)
        rec_copy["action"] = rec_copy["action"].replace("College tasks", f"{user_team} tasks")
        modified_recommendations.append(rec_copy)
    
    return {
        "emails": modified_emails,
        "calendar": modified_calendar,
        "tasks": modified_tasks,
        "documents": base_mock.get("documents", []),
        "contexts": modified_contexts,
        "cognitive_load": cognitive_load,
        "insights": modified_insights,
        "recommendations": modified_recommendations
    }


class AssistantQuery(BaseModel):
    query: str


# ============================================================================
# MOCK DATA FUNCTIONS - Load from mock.json file
# ============================================================================

def get_active_contexts(user_id: str) -> List[Dict[str, Any]]:
    """Fetch contexts from Google data, with mock data fallback if empty"""
    print(f"🔍 get_active_contexts called with user_id: {user_id[:8]}...")
    
    # Check if user has real Google data
    from services.data_loader import load_google_calendar_data, load_google_email_data
    calendar_data = load_google_calendar_data(user_id)
    email_data = load_google_email_data(user_id)
    has_real_data = len(calendar_data) > 0 or len(email_data) > 0
    
    print(f"   Has real Google data: {has_real_data} (calendar: {len(calendar_data)}, email: {len(email_data)})")
    
    # If no real Google data, use user-specific mock contexts directly
    if not has_real_data:
        print(f"   Using user-specific mock contexts for user {user_id[:8]}...")
        mock_data = get_user_specific_mock_data(user_id)
        contexts = mock_data.get("contexts", [])
        formatted = []
        for ctx in contexts[:2]:  # Limit to 2 contexts
            related_tasks = [t.get("title", "") for t in mock_data.get("tasks", []) 
                           if t.get("context") == ctx.get("name")][:3]
            formatted.append({
                "id": ctx.get("id", ""),
                "name": ctx.get("name", ""),
                "related_items": ctx.get("related_items", {}).get("emails", [])[:3] if isinstance(ctx.get("related_items"), dict) else [],
                "urgency": ctx.get("urgency", "medium"),
                "deadline": ctx.get("deadline", ""),
                "tasks": related_tasks if related_tasks else ctx.get("tasks", [])[:3]
            })
        
        # Ensure we always have at least one context
        if not formatted:
            import hashlib
            user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
            user_variations = {
                "projects": ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Echo"],
                "teams": ["Engineering", "Design", "Marketing", "Sales", "Product"],
                "topics": ["API Integration", "UI Redesign", "Market Analysis", "Client Presentation", "Code Review"]
            }
            project_idx = (user_hash // 10) % len(user_variations["projects"])
            team_idx = (user_hash // 100) % len(user_variations["teams"])
            topic_idx = (user_hash // 1000) % len(user_variations["topics"])
            
            user_project = user_variations["projects"][project_idx]
            user_team = user_variations["teams"][team_idx]
            user_topic = user_variations["topics"][topic_idx]
            
            formatted.append({
                "id": f"ctx_{user_id[:8]}_default",
                "name": user_project,
                "related_items": [],
                "urgency": "medium",
                "deadline": "",
                "tasks": [f"Work on {user_topic}", f"Review {user_team} tasks"]
            })
        
        print(f"   Returning {len(formatted)} user-specific mock contexts")
        if formatted:
            print(f"   First context: {formatted[0].get('name', 'N/A')}")
        return formatted
    
    # If we have real Google data, process it with user-specific naming
    work_items = load_work_items(user_id, use_mock_if_empty=False)
    print(f"   Processing {len(work_items)} real work items")
    
    import hashlib
    user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    user_variations = {
        "projects": ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Echo"],
        "teams": ["Engineering", "Design", "Marketing", "Sales", "Product"],
        "topics": ["API Integration", "UI Redesign", "Market Analysis", "Client Presentation", "Code Review"]
    }
    project_idx = (user_hash // 10) % len(user_variations["projects"])
    team_idx = (user_hash // 100) % len(user_variations["teams"])
    topic_idx = (user_hash // 1000) % len(user_variations["topics"])
    
    user_project = user_variations["projects"][project_idx]
    user_team = user_variations["teams"][team_idx]
    user_topic = user_variations["topics"][topic_idx]
    
    # Extract context names from calendar events and emails with user-specific naming
    google_contexts = {}
    for item in work_items:
        title = item.get("title", "").lower()
        # User-specific context grouping
        if any(word in title for word in ["meeting", "sync", "standup", "review"]):
            context_name = f"{user_team} Meetings"
        elif any(word in title for word in ["assignment", "paper", "project", "homework"]):
            context_name = user_project
        elif any(word in title for word in ["email", "message", "notification"]):
            context_name = f"{user_team} Communication"
        else:
            # Default context with user-specific name
            context_name = f"{user_topic} Work"
            
        if context_name not in google_contexts:
            google_contexts[context_name] = {
                "tasks": [],
                "items": []
            }
        google_contexts[context_name]["tasks"].append(item.get("title", ""))
        google_contexts[context_name]["items"].append(item.get("id", ""))
    
    # Format contexts to match expected structure
    formatted = []
    for idx, (context_name, context_data) in enumerate(google_contexts.items()):
        formatted.append({
            "id": f"ctx_{user_id[:8]}_{idx}",
            "name": context_name,
            "related_items": context_data["items"][:5],
            "urgency": "high" if idx == 0 else "medium",
            "deadline": "",
            "tasks": list(set(context_data["tasks"]))[:3]
        })
    
    print(f"   Returning {len(formatted)} contexts from real data")
    return formatted


def get_prioritized_tasks(user_id: str) -> List[Dict[str, Any]]:
    """Fetch tasks from Google data, with mock data fallback if empty"""
    # Load work items (with mock fallback if Google data is empty)
    work_items = load_work_items(user_id, use_mock_if_empty=True)
    
    # Convert work items to task format
    formatted = []
    
    # Process calendar events as tasks
    for item in work_items:
        if item.get("source") == "calendar" and item.get("kind") == "meeting":
            deadline = item.get("deadline", "")
            if deadline:
                try:
                    deadline_dt = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                    deadline = deadline_dt.strftime("%Y-%m-%d")
                except:
                    deadline = deadline[:10] if len(deadline) >= 10 else deadline
            
            # Calculate priority based on deadline proximity
            priority_score = 50
            if deadline:
                try:
                    deadline_dt = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                    days_until = (deadline_dt.date() - datetime.now().date()).days
                    if days_until <= 1:
                        priority_score = 85
                    elif days_until <= 3:
                        priority_score = 70
                    elif days_until <= 7:
                        priority_score = 60
                except:
                    pass
            
            formatted.append({
                "id": item.get("id", ""),
                "title": f"Attend: {item.get('title', 'Meeting')}",
                "context": "Calendar",
                "deadline": deadline,
                "priority_score": priority_score,
                "status": "scheduled",
                "explanation": f"Calendar meeting: {item.get('title', '')}"
            })
    
    # Process emails as tasks (especially unread emails)
    for item in work_items:
        if item.get("source") == "email" and item.get("kind") == "email":
            title = item.get("title", "")
            status = item.get("status", "read")
            
            # Extract task keywords from email subject
            task_keywords = ["action", "review", "approve", "complete", "submit", "deadline", "urgent", "important"]
            is_task_email = any(keyword in title.lower() for keyword in task_keywords)
            
            if is_task_email or status == "unread":
                # Calculate priority: unread emails get higher priority
                priority_score = 70 if status == "unread" else 50
                
                # Check if email mentions deadlines
                content = item.get("content", "").lower()
                if "deadline" in content or "due" in content:
                    priority_score = 80
                if "urgent" in content or "asap" in content:
                    priority_score = 90
                
                formatted.append({
                    "id": item.get("id", ""),
                    "title": title,
                    "context": "Email",
                    "deadline": item.get("timestamp", "")[:10] if item.get("timestamp") else "",
                    "priority_score": priority_score,
                    "status": "not_started",
                    "explanation": f"Email task: {title} - {'Unread email requires action' if status == 'unread' else 'Email action item'}"
                })
    
    # Ensure we always have at least one task with user-specific data
    if not formatted:
        formatted.append({
            "id": f"task_{user_id[:8]}_default",
            "title": f"Complete {user_topic} review",
            "context": user_project,
            "deadline": None,
            "priority_score": 70 + (user_hash % 20),
            "status": "not_started",
            "explanation": f"High priority task for {user_project}"
        })
    
    # If no tasks from work items, use user-specific mock tasks
    if not formatted:
        import hashlib
        user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        user_variations = {
            "projects": ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Echo"],
            "teams": ["Engineering", "Design", "Marketing", "Sales", "Product"],
            "topics": ["API Integration", "UI Redesign", "Market Analysis", "Client Presentation", "Code Review"]
        }
        project_idx = (user_hash // 10) % len(user_variations["projects"])
        team_idx = (user_hash // 100) % len(user_variations["teams"])
        topic_idx = (user_hash // 1000) % len(user_variations["topics"])
        
        user_project = user_variations["projects"][project_idx]
        user_team = user_variations["teams"][team_idx]
        user_topic = user_variations["topics"][topic_idx]
        
        mock_data = get_user_specific_mock_data(user_id)
        mock_tasks = mock_data.get("tasks", [])
        for task in mock_tasks[:5]:  # Limit to top 5
            deadline = task.get("deadline")
            if deadline:
                try:
                    deadline_dt = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                    deadline = deadline_dt.strftime("%Y-%m-%d")
                except:
                    deadline = deadline[:10] if len(deadline) >= 10 else deadline
            
            formatted.append({
                "id": task.get("id", ""),
                "title": task.get("title", ""),
                "context": task.get("context", ""),
                "deadline": deadline,
                "priority_score": task.get("priority_score", 50),
                "status": task.get("status", "not_started"),
                "explanation": task.get("explanation", "")
            })
    
    # Ensure we always have at least one task with user-specific data
    if not formatted:
        import hashlib
        user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        user_variations = {
            "projects": ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Echo"],
            "teams": ["Engineering", "Design", "Marketing", "Sales", "Product"],
            "topics": ["API Integration", "UI Redesign", "Market Analysis", "Client Presentation", "Code Review"]
        }
        project_idx = (user_hash // 10) % len(user_variations["projects"])
        team_idx = (user_hash // 100) % len(user_variations["teams"])
        topic_idx = (user_hash // 1000) % len(user_variations["topics"])
        
        user_project = user_variations["projects"][project_idx]
        user_team = user_variations["teams"][team_idx]
        user_topic = user_variations["topics"][topic_idx]
        
        formatted.append({
            "id": f"task_{user_id[:8]}_default",
            "title": f"Complete {user_topic} review",
            "context": user_project,
            "deadline": None,
            "priority_score": 70 + (user_hash % 20),
            "status": "not_started",
            "explanation": f"High priority task for {user_project}"
        })
    
    # Sort by priority score
    formatted.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
    
    return formatted


def get_cognitive_load(user_id: str) -> Dict[str, Any]:
    """Calculate cognitive load from Google data, with mock data fallback if empty"""
    # Load work items (with mock fallback if Google data is empty)
    work_items = load_work_items(user_id, use_mock_if_empty=True)
    
    # Calculate from actual data
    active_contexts_count = len(get_active_contexts(user_id))
    tasks = get_prioritized_tasks(user_id)
    urgent_tasks = [t for t in tasks if t.get("priority_score", 0) >= 75]
    
    # Count calendar events (meetings) which contribute to cognitive load
    calendar_items = [item for item in work_items if item.get("source") == "calendar"]
    email_items = [item for item in work_items if item.get("source") == "email"]
    
    # Estimate context switches based on item count
    switches = min(len(work_items) * 2, 20)  # Rough estimate
    
    # Calculate score (0-100)
    score = min(100, (active_contexts_count * 15) + (len(urgent_tasks) * 10) + (len(calendar_items) * 3) + switches)
    
    # If score is 0 and we have mock data, use user-specific mock cognitive load
    if score == 0 and work_items:
        mock_data = get_user_specific_mock_data(user_id)
        mock_load = mock_data.get("cognitive_load", {})
        if mock_load:
            return {
                "score": mock_load.get("score", 50),
                "status": mock_load.get("status", "Medium"),
                "active_contexts": mock_load.get("active_contexts", 2),
                "urgent_tasks": mock_load.get("urgent_tasks", 2),
                "switches": mock_load.get("switches", 5),
                "breakdown": mock_load.get("breakdown", f"{mock_load.get('active_contexts', 2)} parallel contexts + {mock_load.get('urgent_tasks', 2)} urgent deadlines + {mock_load.get('switches', 5)} switches today")
            }
    
    status = "Low" if score < 50 else "Medium" if score < 75 else "High"
    
    return {
        "score": score,
        "status": status,
        "active_contexts": active_contexts_count,
        "urgent_tasks": len(urgent_tasks),
        "switches": switches,
        "breakdown": f"{active_contexts_count} parallel contexts + {len(urgent_tasks)} urgent tasks + {len(calendar_items)} meetings + {switches} estimated switches"
    }


def get_latest_insights(user_id: str) -> List[Dict[str, Any]]:
    """Generate insights from Google data, with mock data fallback if empty"""
    work_items = load_work_items(user_id, use_mock_if_empty=True)
    
    # Generate simple insights from actual data
    insights = []
    tasks = get_prioritized_tasks(user_id)
    contexts = get_active_contexts(user_id)
    
    # Insight: Context switching
    if len(contexts) > 1:
        insights.append({
            "type": "context_switching",
            "severity": "high" if len(contexts) > 3 else "medium",
            "count": len(contexts),
            "message": f"You're managing {len(contexts)} different contexts, which may impact focus."
        })
    
    # Insight: Urgent tasks
    urgent_tasks = [t for t in tasks if t.get("priority_score", 0) >= 75]
    if urgent_tasks:
        insights.append({
            "type": "deadline_proximity",
            "severity": "high" if len(urgent_tasks) > 2 else "medium",
            "tasks": [t.get("title") for t in urgent_tasks[:3]],
            "message": f"{len(urgent_tasks)} urgent task(s) require immediate attention."
        })
    
    # If no insights, use user-specific mock insights
    if not insights:
        mock_data = get_user_specific_mock_data(user_id)
        mock_insights = mock_data.get("insights", [])
        for insight in mock_insights[:2]:  # Limit to 2 insights
            insights.append({
                "type": insight.get("type", ""),
                "severity": insight.get("severity", "medium"),
                "count": insight.get("count"),
                "task": insight.get("task"),
                "tasks": insight.get("tasks"),
                "message": insight.get("message", "")
            })
    
    return insights


def get_recommendations(user_id: str) -> List[Dict[str, Any]]:
    """Generate recommendations from Google data, with mock data fallback if empty"""
    work_items = load_work_items(user_id, use_mock_if_empty=True)
    
    recommendations = []
    tasks = get_prioritized_tasks(user_id)
    cognitive_load = get_cognitive_load(user_id)
    
    # Recommendation: Focus on urgent tasks
    urgent_tasks = [t for t in tasks if t.get("priority_score", 0) >= 75]
    if urgent_tasks:
        top_task = urgent_tasks[0]
        recommendations.append({
            "action": f"Prioritize '{top_task.get('title')}' today",
            "reason": f"Highest priority task (score: {top_task.get('priority_score')})",
            "expected_impact": "Complete most urgent work first to reduce cognitive load"
        })
    
    # Recommendation: Batch similar work
    if cognitive_load.get("score", 0) > 70:
        recommendations.append({
            "action": "Batch similar tasks together",
            "reason": f"High cognitive load ({cognitive_load.get('score')}/100) due to multiple contexts",
            "expected_impact": "Reduce context switching and improve focus"
        })
    
    # If no recommendations, use user-specific mock recommendations
    if not recommendations:
        mock_data = get_user_specific_mock_data(user_id)
        mock_recommendations = mock_data.get("recommendations", [])
        for rec in mock_recommendations[:2]:  # Limit to 2 recommendations
            recommendations.append({
                "action": rec.get("action", ""),
                "reason": rec.get("reason", ""),
                "expected_impact": rec.get("expected_impact", "")
            })
    
    return recommendations


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
async def ask_assistant(request: AssistantQuery, http_request: Request, x_user_id: Optional[str] = Header(None)):
    try:
        # Require user ID - don't fallback to default
        if not x_user_id:
            raise HTTPException(status_code=400, detail="User ID is required. Please ensure you're logged in.")
        
        user_id = x_user_id
        # Fetch current system state from Google data ONLY (no mock data)
        contexts = get_active_contexts(user_id)
        tasks = get_prioritized_tasks(user_id)
        cognitive_load = get_cognitive_load(user_id)
        insights = get_latest_insights(user_id)
        recommendations = get_recommendations(user_id)
        
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
        
        # Sanitize work items for LLM (privacy-safe)
        work_items = load_work_items(user_id)
        sanitized_items = sanitize_for_llm(work_items)
        
        # Separate emails and calendar events for better context
        emails = [item for item in sanitized_items if item.get("source") == "email"]
        calendar_events = [item for item in sanitized_items if item.get("source") == "calendar"]
        
        # Format data for the prompt with training examples
        system_prompt = f"""You are an intelligent work assistant analyzing a user's digital work environment.

{training_examples}

=== CURRENT SYSTEM DATA ===

ACTIVE CONTEXTS:
{json.dumps(all_contexts, indent=2)}

TASKS BY PRIORITY:
{json.dumps(all_tasks, indent=2)}

RECENT EMAILS ({len(emails)} emails):
{json.dumps(emails[:15], indent=2) if emails else "No recent emails available"}

UPCOMING CALENDAR EVENTS ({len(calendar_events)} events):
{json.dumps(calendar_events[:15], indent=2) if calendar_events else "No upcoming calendar events"}

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
2. Always cite specific context names, task titles, email subjects, calendar event titles, and metric values
3. When asked about emails, reference specific email subjects and senders from the RECENT EMAILS section above
4. When asked about meetings/calendar, reference specific event titles and times from the UPCOMING CALENDAR EVENTS section above
5. Explain WHY something matters by referencing the data
6. Be concise and actionable (2-3 sentences max unless asked for details)
7. If asked about something not in the data, say "I don't have that information in your current work data"
8. Use natural language, avoid jargon like "context_id" - say "your Hackathon Review project" instead
9. Follow the style and format of the training examples above

RESPONSE STYLE:
- Direct and helpful
- Reference specific work items by name (emails by subject, meetings by title)
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
async def get_dashboard_data(x_user_id: Optional[str] = Header(None)):
    """Get all dashboard data in one endpoint"""
    try:
        if not x_user_id:
            print(f"⚠️ WARNING: No user ID provided in /api/dashboard headers")
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        print(f"✅ Loading dashboard data for user: {user_id[:8]}...")
        contexts = get_active_contexts(user_id)
        tasks = get_prioritized_tasks(user_id)
        cognitive_load = get_cognitive_load(user_id)
        insights = get_latest_insights(user_id)
        recommendations = get_recommendations(user_id)
        
        print(f"✅ Dashboard data loaded for user {user_id[:8]}... - {len(contexts)} contexts, {len(tasks)} tasks")
        
        return {
            "contexts": contexts,
            "tasks": tasks,
            "cognitive_load": cognitive_load,
            "insights": insights,
            "recommendations": recommendations
        }
    except Exception as e:
        print(f"❌ Error loading dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/contexts")
async def get_contexts(x_user_id: Optional[str] = Header(None)):
    """Get active work contexts"""
    try:
        if not x_user_id:
            print(f"⚠️ WARNING: No user ID provided in headers. Available headers: {x_user_id}")
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        print(f"✅ Loading contexts for user: {user_id[:8]}...")
        contexts = get_active_contexts(user_id)
        print(f"✅ Found {len(contexts)} contexts for user {user_id[:8]}...")
        # Log first context name to verify user-specific data
        if contexts:
            print(f"   First context: {contexts[0].get('name', 'N/A')}")
        return {"contexts": contexts}
    except Exception as e:
        print(f"❌ Error loading contexts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks")
async def get_tasks(x_user_id: Optional[str] = Header(None)):
    """Get prioritized tasks"""
    try:
        if not x_user_id:
            print(f"⚠️ WARNING: No user ID provided in headers")
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        print(f"✅ Loading tasks for user: {user_id[:8]}...")
        tasks = get_prioritized_tasks(user_id)
        print(f"✅ Found {len(tasks)} tasks for user {user_id[:8]}...")
        # Log first task to verify user-specific data
        if tasks:
            print(f"   Top task: {tasks[0].get('title', 'N/A')} (score: {tasks[0].get('priority_score', 0)})")
        return {"tasks": tasks}
    except Exception as e:
        print(f"❌ Error loading tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cognitive-load")
async def get_cognitive_load_data(x_user_id: Optional[str] = Header(None)):
    """Get cognitive load metrics"""
    try:
        if not x_user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        return {"cognitive_load": get_cognitive_load(user_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/insights")
async def get_insights(x_user_id: Optional[str] = Header(None)):
    """Get behavioral insights"""
    try:
        if not x_user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        return {"insights": get_latest_insights(user_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations")
async def get_recommendations_data(x_user_id: Optional[str] = Header(None)):
    """Get recommendations"""
    try:
        if not x_user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        return {"recommendations": get_recommendations(user_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# GOOGLE INTEGRATION ENDPOINTS
# ============================================================================

@app.get("/api/google/auth")
async def google_auth(x_user_id: Optional[str] = Header(None)):
    """Trigger first-time Google login"""
    try:
        if not x_user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        creds = authenticate_google(user_id)
        if creds:
            return {
                "status": "authenticated",
                "message": "Google account connected successfully. Token saved."
            }
        else:
            return {
                "status": "error",
                "message": "Failed to authenticate with Google"
            }
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"credentials.json not found. Please download it from Google Cloud Console and place it in the backend directory. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")


@app.post("/api/google/sync")
async def google_sync(x_user_id: Optional[str] = Header(None)):
    """Manually trigger Google data refresh"""
    try:
        if not x_user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        print(f"🔄 Sync triggered for user: {user_id[:8]}...")
        result = sync_all_google_data(user_id)
        print(f"✅ Sync completed for user: {user_id[:8]}... - Calendar: {result.get('synced', {}).get('calendar', 0)}, Emails: {result.get('synced', {}).get('emails', 0)}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync error: {str(e)}")


@app.get("/api/google/status")
async def google_status(x_user_id: Optional[str] = Header(None)):
    """Check if Google is connected and get sync status"""
    try:
        if not x_user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        return get_sync_status(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/google/disconnect")
async def google_disconnect(x_user_id: Optional[str] = Header(None)):
    """Disconnect Google account and remove saved token"""
    try:
        if not x_user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        user_id = x_user_id
        result = disconnect_google(user_id)
        if result.get("status") == "success":
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("message", "Disconnect failed"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disconnect error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
