"""
Data loading service that combines Google data with mock data
Provides fallback to mock data if Google sync hasn't run
"""

import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent.parent
MOCK_DATA_PATH = BASE_DIR / "mock.json"
DATA_DIR = BASE_DIR / "data"


def get_user_data_dir(user_id: str) -> Path:
    """Get data directory for a specific user"""
    user_dir = DATA_DIR / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

def get_user_calendar_file(user_id: str) -> Path:
    """Get calendar data file for a specific user"""
    return get_user_data_dir(user_id) / "calendar.json"

def get_user_email_file(user_id: str) -> Path:
    """Get email data file for a specific user"""
    return get_user_data_dir(user_id) / "emails.json"


def load_google_calendar_data(user_id: str) -> List[Dict[str, Any]]:
    """Load calendar data from Google sync for a specific user"""
    try:
        CALENDAR_DATA_FILE = get_user_calendar_file(user_id)
        if CALENDAR_DATA_FILE.exists():
            with open(CALENDAR_DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading calendar data: {e}")
    return []


def load_google_email_data(user_id: str) -> List[Dict[str, Any]]:
    """Load email data from Google sync for a specific user"""
    try:
        EMAIL_DATA_FILE = get_user_email_file(user_id)
        if EMAIL_DATA_FILE.exists():
            with open(EMAIL_DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading email data: {e}")
    return []


def load_mock_data() -> Dict[str, Any]:
    """Load mock data from JSON file"""
    try:
        if MOCK_DATA_PATH.exists():
            with open(MOCK_DATA_PATH, 'r') as f:
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


# Global counter to track syncs and toggle datasets
_sync_counter = {}

def toggle_user_dataset(user_id: str) -> None:
    """Toggle the dataset for a user (called on sync)"""
    if user_id not in _sync_counter:
        # Use hash to set initial dataset
        user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        _sync_counter[user_id] = user_hash % 2
    else:
        # Toggle on sync
        _sync_counter[user_id] = (_sync_counter[user_id] + 1) % 2
    print(f"🔄 Toggled dataset for user {user_id[:8]}... to dataset {_sync_counter[user_id] + 1}")

def get_user_specific_mock_data(user_id: str) -> Dict[str, Any]:
    """Return one of two distinct mock data sets based on user's current dataset"""
    base_mock = load_mock_data()
    if not base_mock.get("emails") and not base_mock.get("calendar"):
        return base_mock
    
    # Get current dataset for user (initialize if needed)
    if user_id not in _sync_counter:
        user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        _sync_counter[user_id] = user_hash % 2
    
    dataset_num = _sync_counter[user_id]
    
    print(f"   Using mock dataset {dataset_num + 1} for user {user_id[:8]}... (counter: {_sync_counter[user_id]})")
    
    if dataset_num == 0:
        # Dataset 1: Tech/Engineering Focus
        return {
            "emails": [
                {
                    "id": f"email_{user_id[:8]}_1",
                    "subject": "Code Review Request - Payment API",
                    "from": "tech-lead@company.com",
                    "date": "2026-01-08T10:00:00Z",
                    "body": "Please review the payment API implementation before deployment.",
                    "read": False,
                    "labels": ["IMPORTANT", "WORK"]
                },
                {
                    "id": f"email_{user_id[:8]}_2",
                    "subject": "Sprint Planning Meeting Tomorrow",
                    "from": "scrum-master@company.com",
                    "date": "2026-01-08T09:30:00Z",
                    "body": "Sprint planning session scheduled for tomorrow at 2 PM.",
                    "read": True,
                    "labels": ["WORK"]
                },
                {
                    "id": f"email_{user_id[:8]}_3",
                    "subject": "Database Migration Status Update",
                    "from": "devops@company.com",
                    "date": "2026-01-08T08:15:00Z",
                    "body": "Database migration completed successfully. All systems operational.",
                    "read": False,
                    "labels": ["IMPORTANT"]
                }
            ],
            "calendar": [
                {
                    "id": f"meeting_{user_id[:8]}_1",
                    "title": "Engineering Standup",
                    "start": "2026-01-09T09:00:00Z",
                    "end": "2026-01-09T09:30:00Z",
                    "description": "Daily engineering team standup meeting",
                    "location": "Conference Room A",
                    "attendees": ["team@company.com"]
                },
                {
                    "id": f"meeting_{user_id[:8]}_2",
                    "title": "API Architecture Review",
                    "start": "2026-01-10T14:00:00Z",
                    "end": "2026-01-10T15:30:00Z",
                    "description": "Review new API architecture design",
                    "location": "Zoom",
                    "attendees": ["architect@company.com", "tech-lead@company.com"]
                }
            ],
            "tasks": [
                {
                    "id": f"task_{user_id[:8]}_1",
                    "title": "Complete Payment API Integration",
                    "context": "Engineering Sprint",
                    "deadline": "2026-01-10",
                    "priority_score": 88,
                    "status": "in_progress",
                    "explanation": "High priority - blocking deployment"
                },
                {
                    "id": f"task_{user_id[:8]}_2",
                    "title": "Review Database Migration Plan",
                    "context": "Engineering Sprint",
                    "deadline": "2026-01-09",
                    "priority_score": 75,
                    "status": "not_started",
                    "explanation": "Due before next migration"
                },
                {
                    "id": f"task_{user_id[:8]}_3",
                    "title": "Update API Documentation",
                    "context": "Engineering Sprint",
                    "deadline": "2026-01-12",
                    "priority_score": 65,
                    "status": "not_started",
                    "explanation": "Documentation update needed"
                }
            ],
            "contexts": [
                {
                    "id": f"ctx_{user_id[:8]}_1",
                    "name": "Engineering Sprint",
                    "urgency": "high",
                    "deadline": "2026-01-12",
                    "related_items": {"emails": [f"email_{user_id[:8]}_1", f"email_{user_id[:8]}_2"]},
                    "tasks": ["Complete Payment API Integration", "Review Database Migration Plan"]
                },
                {
                    "id": f"ctx_{user_id[:8]}_2",
                    "name": "Code Reviews",
                    "urgency": "medium",
                    "deadline": "",
                    "related_items": {"emails": [f"email_{user_id[:8]}_1"]},
                    "tasks": ["Code Review Request - Payment API"]
                }
            ],
            "cognitive_load": {
                "score": 82,
                "status": "High",
                "active_contexts": 2,
                "urgent_tasks": 2,
                "switches": 8,
                "breakdown": "2 parallel contexts + 2 urgent deadlines + 8 switches today"
            },
            "insights": [
                {
                    "type": "context_switching",
                    "severity": "high",
                    "count": 8,
                    "message": "You switched between contexts 8 times today, losing ~2.5 hours of focus time"
                },
                {
                    "type": "deadline_proximity",
                    "severity": "medium",
                    "tasks": ["Complete Payment API Integration"],
                    "message": "1 urgent task(s) require immediate attention."
                }
            ],
            "recommendations": [
                {
                    "action": "Block 9-11 AM tomorrow for Payment API Integration only",
                    "reason": "Deadline tomorrow + high switching detected",
                    "expected_impact": "Complete integration in single focus session"
                },
                {
                    "action": "Batch code reviews together",
                    "reason": "Reduce cognitive load from 82 to ~60",
                    "expected_impact": "Lower stress and finish urgent work first"
                }
            ]
        }
    else:
        # Dataset 2: Design/Marketing Focus
        return {
            "emails": [
                {
                    "id": f"email_{user_id[:8]}_1",
                    "subject": "Brand Identity Design Review",
                    "from": "design-director@company.com",
                    "date": "2026-01-08T11:00:00Z",
                    "body": "Please review the new brand identity designs for the Q1 campaign.",
                    "read": False,
                    "labels": ["IMPORTANT", "WORK"]
                },
                {
                    "id": f"email_{user_id[:8]}_2",
                    "subject": "Marketing Campaign Launch Meeting",
                    "from": "marketing-manager@company.com",
                    "date": "2026-01-08T10:15:00Z",
                    "body": "Campaign launch meeting scheduled for next week.",
                    "read": True,
                    "labels": ["WORK"]
                },
                {
                    "id": f"email_{user_id[:8]}_3",
                    "subject": "Social Media Content Approval",
                    "from": "social-media@company.com",
                    "date": "2026-01-08T09:00:00Z",
                    "body": "Pending approval for this week's social media content.",
                    "read": False,
                    "labels": ["IMPORTANT"]
                }
            ],
            "calendar": [
                {
                    "id": f"meeting_{user_id[:8]}_1",
                    "title": "Design Team Sync",
                    "start": "2026-01-09T10:00:00Z",
                    "end": "2026-01-09T10:45:00Z",
                    "description": "Weekly design team synchronization meeting",
                    "location": "Design Studio",
                    "attendees": ["design-team@company.com"]
                },
                {
                    "id": f"meeting_{user_id[:8]}_2",
                    "title": "Q1 Campaign Strategy Review",
                    "start": "2026-01-11T13:00:00Z",
                    "end": "2026-01-11T14:30:00Z",
                    "description": "Review Q1 marketing campaign strategy",
                    "location": "Conference Room B",
                    "attendees": ["marketing@company.com", "design-director@company.com"]
                }
            ],
            "tasks": [
                {
                    "id": f"task_{user_id[:8]}_1",
                    "title": "Finalize Brand Identity Designs",
                    "context": "Q1 Campaign",
                    "deadline": "2026-01-11",
                    "priority_score": 92,
                    "status": "in_progress",
                    "explanation": "Critical - needed for campaign launch"
                },
                {
                    "id": f"task_{user_id[:8]}_2",
                    "title": "Approve Social Media Content",
                    "context": "Q1 Campaign",
                    "deadline": "2026-01-09",
                    "priority_score": 78,
                    "status": "not_started",
                    "explanation": "Content approval needed before publishing"
                },
                {
                    "id": f"task_{user_id[:8]}_3",
                    "title": "Create Campaign Presentation",
                    "context": "Q1 Campaign",
                    "deadline": "2026-01-13",
                    "priority_score": 70,
                    "status": "not_started",
                    "explanation": "Presentation for stakeholders"
                }
            ],
            "contexts": [
                {
                    "id": f"ctx_{user_id[:8]}_1",
                    "name": "Q1 Campaign",
                    "urgency": "high",
                    "deadline": "2026-01-15",
                    "related_items": {"emails": [f"email_{user_id[:8]}_1", f"email_{user_id[:8]}_2"]},
                    "tasks": ["Finalize Brand Identity Designs", "Approve Social Media Content"]
                },
                {
                    "id": f"ctx_{user_id[:8]}_2",
                    "name": "Design Reviews",
                    "urgency": "medium",
                    "deadline": "",
                    "related_items": {"emails": [f"email_{user_id[:8]}_1"]},
                    "tasks": ["Brand Identity Design Review"]
                }
            ],
            "cognitive_load": {
                "score": 85,
                "status": "High",
                "active_contexts": 2,
                "urgent_tasks": 2,
                "switches": 10,
                "breakdown": "2 parallel contexts + 2 urgent deadlines + 10 switches today"
            },
            "insights": [
                {
                    "type": "context_switching",
                    "severity": "high",
                    "count": 10,
                    "message": "You switched between contexts 10 times today, losing ~3 hours of focus time"
                },
                {
                    "type": "deadline_proximity",
                    "severity": "high",
                    "tasks": ["Finalize Brand Identity Designs"],
                    "message": "1 urgent task(s) require immediate attention."
                }
            ],
            "recommendations": [
                {
                    "action": "Block 10 AM-12 PM tomorrow for Brand Identity work only",
                    "reason": "Deadline in 3 days + high switching detected",
                    "expected_impact": "Complete designs in single focus session"
                },
                {
                    "action": "Defer content approval to afternoon",
                    "reason": "Reduce cognitive load from 85 to ~65",
                    "expected_impact": "Lower stress and finish urgent design work first"
                }
            ]
        }


def load_work_items(user_id: str, use_mock_if_empty: bool = True) -> List[Dict[str, Any]]:
    """
    Load work items from Google data, with mock data fallback if Google data is empty.
    
    Args:
        user_id: User ID to load data for
        use_mock_if_empty: If True, use mock data when Google data is empty
    
    Returns:
        List of work items from Google Calendar and Gmail, or mock data if empty
    """
    all_items = []
    
    # Load Google Calendar data (real data)
    calendar_items = load_google_calendar_data(user_id)
    all_items.extend(calendar_items)
    
    # Load Google Email data (real data)
    email_items = load_google_email_data(user_id)
    all_items.extend(email_items)
    
    # If we have Google data, return it
    if all_items:
        return all_items
    
    # If no Google data and mock fallback is enabled, use user-specific mock data
    if use_mock_if_empty:
        mock_data = get_user_specific_mock_data(user_id)
        
        # Convert mock calendar to work items
        for event in mock_data.get("calendar", []):
            all_items.append({
                "id": event.get("id", ""),
                "source": "calendar",
                "kind": "meeting",
                "title": event.get("title", ""),
                "content": event.get("description", ""),
                "timestamp": event.get("start", ""),
                "participants": event.get("attendees", []),
                "deadline": event.get("end", ""),
                "status": "scheduled",
                "meta": {"location": event.get("location", "")}
            })
        
        # Convert mock emails to work items
        for email in mock_data.get("emails", []):
            all_items.append({
                "id": email.get("id", ""),
                "source": "email",
                "kind": "email",
                "title": email.get("subject", ""),
                "content": email.get("body", "")[:200] if email.get("body") else "",
                "timestamp": email.get("date", ""),
                "participants": [email.get("from", "")],
                "status": "read" if email.get("read") else "unread",
                "meta": {"labels": email.get("labels", [])}
            })
    
    return all_items
