"""
Google Calendar and Gmail Integration Service
Handles OAuth2 authentication and data fetching from Google APIs
"""

import os
import json
import pickle
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

# Paths
BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
DATA_DIR = BASE_DIR / "data"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

def get_user_token_file(user_id: str) -> Path:
    """Get token file path for a specific user"""
    return BASE_DIR / f"token_{user_id}.json"

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


def authenticate_google(user_id: str) -> Optional[Credentials]:
    """
    Handle OAuth2 authentication for Google APIs.
    Returns authenticated credentials or None if authentication fails.
    """
    creds = None
    TOKEN_FILE = get_user_token_file(user_id)
    
    # Load existing token if available
    if TOKEN_FILE.exists():
        try:
            with open(TOKEN_FILE, 'r') as token:
                creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")
    
    # If no valid credentials, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None
        
        if not creds:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"credentials.json not found at {CREDENTIALS_FILE}. "
                    "Please download it from Google Cloud Console and place it in the backend directory."
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        try:
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"Error saving token: {e}")
    
    return creds


def fetch_calendar_events(user_id: str, days_back: int = 7, days_forward: int = 14) -> List[Dict[str, Any]]:
    """
    Fetch calendar events and convert to WorkItem format.
    
    Args:
        days_back: Number of days to look back
        days_forward: Number of days to look forward
    
    Returns:
        List of calendar events in WorkItem format
    """
    try:
        creds = authenticate_google(user_id)
        if not creds:
            return []
        
        service = build('calendar', 'v3', credentials=creds)
        
        # Calculate time range
        time_min = (datetime.now(timezone.utc) - timedelta(days=days_back)).isoformat()
        time_max = (datetime.now(timezone.utc) + timedelta(days=days_forward)).isoformat()
        
        # Fetch events
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            maxResults=100,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Convert to WorkItem format
        work_items = []
        for event in events:
            start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
            end = event.get('end', {}).get('dateTime', event.get('end', {}).get('date'))
            
            # Extract attendees
            attendees = []
            for attendee in event.get('attendees', []):
                email = attendee.get('email', '')
                if email:
                    attendees.append(email)
            
            work_item = {
                "id": f"calendar_{event.get('id', '')}",
                "source": "calendar",
                "kind": "meeting",
                "title": event.get('summary', 'No Title'),
                "content": event.get('description', '')[:500] if event.get('description') else '',  # Limit content
                "timestamp": start or datetime.now(timezone.utc).isoformat(),
                "participants": attendees,
                "deadline": end or start,
                "status": "scheduled",
                "meta": {
                    "location": event.get('location', ''),
                    "meeting_link": event.get('hangoutLink', ''),
                    "organizer": event.get('organizer', {}).get('email', ''),
                    "calendar_id": event.get('id', ''),
                    "html_link": event.get('htmlLink', '')
                }
            }
            work_items.append(work_item)
        
        # Save to user-specific file
        CALENDAR_DATA_FILE = get_user_calendar_file(user_id)
        with open(CALENDAR_DATA_FILE, 'w') as f:
            json.dump(work_items, f, indent=2, default=str)
        
        return work_items
        
    except FileNotFoundError as e:
        print(f"Credentials file not found: {e}")
        return []
    except HttpError as e:
        print(f"Google API error: {e}")
        return []
    except Exception as e:
        print(f"Error fetching calendar events: {e}")
        return []


def fetch_gmail_emails(user_id: str, max_results: int = 50, days_back: int = 7) -> List[Dict[str, Any]]:
    """
    Fetch recent email metadata (privacy-safe, no full content).
    
    Args:
        max_results: Maximum number of emails to fetch
        days_back: Number of days to look back
    
    Returns:
        List of emails in WorkItem format
    """
    try:
        creds = authenticate_google(user_id)
        if not creds:
            return []
        
        service = build('gmail', 'v1', credentials=creds)
        
        # Calculate query for recent emails
        days_ago = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime('%Y/%m/%d')
        query = f'newer_than:{days_ago}'
        
        # Fetch message list
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results,
            q=query
        ).execute()
        
        messages = results.get('messages', [])
        
        # Fetch metadata for each message
        work_items = []
        for msg in messages:
            try:
                message = service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['Subject', 'From', 'To', 'Date']
                ).execute()
                
                headers = {h['name']: h['value'] for h in message.get('payload', {}).get('headers', [])}
                
                # Extract participants
                participants = []
                if headers.get('From'):
                    participants.append(headers['From'])
                if headers.get('To'):
                    participants.extend([p.strip() for p in headers['To'].split(',')])
                
                # Get labels
                labels = message.get('labelIds', [])
                
                work_item = {
                    "id": f"email_{message.get('id', '')}",
                    "source": "email",
                    "kind": "email",
                    "title": headers.get('Subject', 'No Subject'),
                    "content": message.get('snippet', '')[:200] if message.get('snippet') else '',  # Preview only
                    "timestamp": headers.get('Date', datetime.now(timezone.utc).isoformat()),
                    "participants": participants[:10],  # Limit participants
                    "status": "unread" if "UNREAD" in labels else "read",
                    "meta": {
                        "thread_id": message.get('threadId', ''),
                        "labels": labels,
                        "message_id": message.get('id', '')
                    }
                }
                work_items.append(work_item)
                
            except Exception as e:
                print(f"Error processing email {msg.get('id')}: {e}")
                continue
        
        # Save to user-specific file
        EMAIL_DATA_FILE = get_user_email_file(user_id)
        with open(EMAIL_DATA_FILE, 'w') as f:
            json.dump(work_items, f, indent=2, default=str)
        
        return work_items
        
    except FileNotFoundError as e:
        print(f"Credentials file not found: {e}")
        return []
    except HttpError as e:
        print(f"Google API error: {e}")
        return []
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []


def sync_all_google_data(user_id: str) -> Dict[str, Any]:
    """
    Orchestrate all Google data fetches in one call.
    
    Args:
        user_id: User ID to sync data for
    
    Returns:
        Summary statistics of sync operation
    """
    try:
        # Toggle mock dataset when sync is called (if no real Google data)
        from services.data_loader import toggle_user_dataset
        toggle_user_dataset(user_id)
        
        calendar_count = 0
        email_count = 0
        errors = []
        
        # Sync calendar
        try:
            calendar_items = fetch_calendar_events(user_id)
            calendar_count = len(calendar_items)
        except Exception as e:
            errors.append(f"Calendar sync failed: {str(e)}")
        
        # Sync emails
        try:
            email_items = fetch_gmail_emails(user_id)
            email_count = len(email_items)
        except Exception as e:
            errors.append(f"Email sync failed: {str(e)}")
        
        return {
            "status": "success" if not errors else "partial",
            "synced": {
                "calendar": calendar_count,
                "emails": email_count
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "errors": errors
        }
        
    except Exception as e:
        return {
            "status": "error",
            "synced": {
                "calendar": 0,
                "emails": 0
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "errors": [str(e)]
        }


def disconnect_google(user_id: str) -> Dict[str, Any]:
    """
    Disconnect Google account by removing token and optionally clearing synced data.
    
    Args:
        user_id: User ID to disconnect
    
    Returns:
        Status of disconnection operation
    """
    try:
        TOKEN_FILE = get_user_token_file(user_id)
        CALENDAR_DATA_FILE = get_user_calendar_file(user_id)
        EMAIL_DATA_FILE = get_user_email_file(user_id)
        
        # Delete token file
        token_deleted = False
        if TOKEN_FILE.exists():
            try:
                TOKEN_FILE.unlink()
                token_deleted = True
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to delete token file: {str(e)}"
                }
        
        # Optionally delete synced data files (uncomment if you want to clear data on disconnect)
        calendar_deleted = False
        email_deleted = False
        
        if CALENDAR_DATA_FILE.exists():
            try:
                CALENDAR_DATA_FILE.unlink()
                calendar_deleted = True
            except Exception as e:
                print(f"Warning: Failed to delete calendar data: {e}")
        
        if EMAIL_DATA_FILE.exists():
            try:
                EMAIL_DATA_FILE.unlink()
                email_deleted = True
            except Exception as e:
                print(f"Warning: Failed to delete email data: {e}")
        
        return {
            "status": "success",
            "message": "Google account disconnected successfully",
            "token_deleted": token_deleted,
            "data_cleared": calendar_deleted and email_deleted
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Disconnect error: {str(e)}"
        }


def get_sync_status(user_id: str) -> Dict[str, Any]:
    """
    Check if Google is connected and get sync status.
    
    Args:
        user_id: User ID to check status for
    
    Returns:
        Status information including connection state and last sync time
    """
    TOKEN_FILE = get_user_token_file(user_id)
    CALENDAR_DATA_FILE = get_user_calendar_file(user_id)
    EMAIL_DATA_FILE = get_user_email_file(user_id)
    
    connected = TOKEN_FILE.exists()
    
    last_sync = None
    if CALENDAR_DATA_FILE.exists():
        try:
            stat = CALENDAR_DATA_FILE.stat()
            last_sync = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
        except:
            pass
    
    return {
        "connected": connected,
        "last_sync": last_sync,
        "has_calendar_data": CALENDAR_DATA_FILE.exists(),
        "has_email_data": EMAIL_DATA_FILE.exists()
    }
