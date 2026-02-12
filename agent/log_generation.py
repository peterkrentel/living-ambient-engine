#!/usr/bin/env python3
"""Log video generation parameters.

Records all generation parameters to data/generations.json for later
correlation with YouTube Analytics data.

Spec: docs/spec/AGENT.md
Contract: docs/spec/contracts/agent-youtube.md
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


DATA_DIR = Path("data")
GENERATIONS_FILE = DATA_DIR / "generations.json"


def load_generations() -> Dict[str, Any]:
    """Load existing generations data or create empty structure."""
    if GENERATIONS_FILE.exists():
        with open(GENERATIONS_FILE, "r") as f:
            return json.load(f)
    return {"videos": []}


def save_generations(data: Dict[str, Any]) -> None:
    """Save generations data to file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(GENERATIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_generation(
    video_id: str,
    workflow: str,
    mood: Optional[str] = None,
    duration_seconds: int = 300,
    params: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    generated_at: Optional[str] = None,
    uploaded_at: Optional[str] = None,
) -> None:
    """Log a video generation to the generations file.
    
    Args:
        video_id: YouTube video ID (11 characters)
        workflow: Name of the workflow that generated this video
        mood: Mood preset used (if applicable)
        duration_seconds: Video duration in seconds
        params: Generation parameters (tempo, visual_speed, etc.)
        metadata: YouTube metadata (title, tags, description)
        generated_at: ISO 8601 timestamp of generation
        uploaded_at: ISO 8601 timestamp of upload
    """
    now = datetime.now(timezone.utc).isoformat()
    
    data = load_generations()
    
    # Check for duplicate (idempotent)
    for video in data["videos"]:
        if video.get("video_id") == video_id:
            # Update existing entry
            video.update({
                "workflow": workflow,
                "mood": mood,
                "duration_seconds": duration_seconds,
                "params": params or {},
                "metadata": metadata or {},
                "generated_at": generated_at or video.get("generated_at", now),
                "uploaded_at": uploaded_at or now,
                "updated_at": now,
            })
            save_generations(data)
            print(f"✅ Updated generation log for video {video_id}")
            return
    
    # Add new entry
    entry = {
        "video_id": video_id,
        "generated_at": generated_at or now,
        "uploaded_at": uploaded_at or now,
        "workflow": workflow,
        "mood": mood,
        "duration_seconds": duration_seconds,
        "params": params or {},
        "metadata": metadata or {},
    }
    
    data["videos"].append(entry)
    save_generations(data)
    print(f"✅ Logged generation for video {video_id}")


def main():
    """CLI entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Log video generation parameters")
    parser.add_argument("--video-id", required=True, help="YouTube video ID")
    parser.add_argument("--workflow", required=True, help="Workflow name")
    parser.add_argument("--mood", help="Mood preset")
    parser.add_argument("--duration", type=int, default=300, help="Duration in seconds")
    parser.add_argument("--title", help="Video title")
    parser.add_argument("--params-json", help="JSON string of generation params")
    
    args = parser.parse_args()
    
    params = {}
    if args.params_json:
        params = json.loads(args.params_json)
    
    metadata = {}
    if args.title:
        metadata["title"] = args.title
    
    log_generation(
        video_id=args.video_id,
        workflow=args.workflow,
        mood=args.mood,
        duration_seconds=args.duration,
        params=params,
        metadata=metadata,
    )


if __name__ == "__main__":
    main()

