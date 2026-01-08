"""
Privacy and sanitization layer for LLM processing
Removes sensitive content before sending to Ollama
"""

from typing import List, Dict, Any


def sanitize_for_llm(work_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sanitize work items before sending to LLM.
    Removes sensitive content and keeps only essential metadata.
    
    Args:
        work_items: List of work items to sanitize
    
    Returns:
        Sanitized work items safe for LLM processing
    """
    sanitized = []
    
    for item in work_items:
        # Create sanitized version
        sanitized_item = {
            "id": item.get("id", ""),
            "source": item.get("source", ""),
            "kind": item.get("kind", ""),
            "title": item.get("title", ""),
            "timestamp": item.get("timestamp", ""),
            "status": item.get("status", ""),
        }
        
        # Limit content preview (privacy-safe)
        content = item.get("content", "")
        if content:
            sanitized_item["content"] = content[:200] + "..." if len(content) > 200 else content
        else:
            sanitized_item["content"] = ""
        
        # Include participant count, not full list
        participants = item.get("participants", [])
        sanitized_item["participant_count"] = len(participants)
        if participants:
            # Only show first participant for context
            sanitized_item["main_participant"] = participants[0].split("@")[0] if "@" in participants[0] else participants[0]
        
        # Include deadline if available
        if item.get("deadline"):
            sanitized_item["deadline"] = item.get("deadline")
        
        # Include safe metadata only
        meta = item.get("meta", {})
        safe_meta = {}
        if meta.get("location"):
            safe_meta["has_location"] = True
        if meta.get("meeting_link"):
            safe_meta["has_meeting_link"] = True
        if meta.get("labels"):
            safe_meta["labels"] = [l for l in meta.get("labels", []) if l in ["INBOX", "IMPORTANT", "UNREAD"]]
        
        if safe_meta:
            sanitized_item["meta"] = safe_meta
        
        sanitized.append(sanitized_item)
    
    return sanitized


def check_permissions() -> bool:
    """
    Check if OAuth tokens are still valid.
    Returns True if permissions are valid, False otherwise.
    """
    # This would check token validity
    # For now, return True if token.json exists
    from pathlib import Path
    token_file = Path(__file__).parent.parent / "token.json"
    return token_file.exists()
