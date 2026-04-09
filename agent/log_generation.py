#!/usr/bin/env python3
"""Log video generation parameters.

Records generation parameters to data/generations.json for correlation with
YouTube Analytics (join on video_id). See docs/spec/AGENT.md.

Spec: docs/spec/AGENT.md
Contract: docs/spec/contracts/agent-youtube.md
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_DIR = Path("data")
GENERATIONS_FILE = DATA_DIR / "generations.json"
SCHEMA_VERSION = 1


def load_generations() -> Dict[str, Any]:
    """Load existing generations data or create empty structure."""
    if GENERATIONS_FILE.exists():
        with open(GENERATIONS_FILE, "r") as f:
            data = json.load(f)
            if "videos" not in data:
                data["videos"] = []
            return data
    return {"schema_version": SCHEMA_VERSION, "videos": []}


def _ensure_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    if "schema_version" not in data:
        data["schema_version"] = SCHEMA_VERSION
    if "videos" not in data:
        data["videos"] = []
    return data


def save_generations(data: Dict[str, Any]) -> None:
    """Save generations data to file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _ensure_schema(data)
    data["schema_version"] = data.get("schema_version", SCHEMA_VERSION)
    with open(GENERATIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def video_id_index() -> Dict[str, Dict[str, Any]]:
    """Map YouTube video_id -> ledger row (latest wins if duplicates)."""
    data = load_generations()
    out: Dict[str, Dict[str, Any]] = {}
    for row in data.get("videos", []):
        vid = row.get("video_id")
        if vid:
            out[vid] = row
    return out


def record_generation_upload(
    *,
    video_id: str,
    workflow: str,
    generation_id: Optional[str] = None,
    mood: Optional[str] = None,
    duration_seconds: int = 300,
    seed: Optional[int] = None,
    variant: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    generated_at: Optional[str] = None,
) -> str:
    """Upsert a ledger row after a successful upload.

    Prefer matching by generation_id when present (stable across retries).
    Otherwise match by video_id for legacy rows. Appends a new row if none match.

    Returns:
        generation_id for this record.
    """
    data = _ensure_schema(load_generations())
    rows: List[Dict[str, Any]] = data["videos"]
    now = datetime.now(timezone.utc).isoformat()

    params_out: Dict[str, Any] = dict(params or {})
    if seed is not None:
        params_out["seed"] = seed
    if variant:
        params_out["variant"] = variant

    commit_sha = os.environ.get("GITHUB_SHA")

    idx_by_gen = None
    if generation_id:
        for i, r in enumerate(rows):
            if r.get("generation_id") == generation_id:
                idx_by_gen = i
                break

    idx_by_vid = None
    for i, r in enumerate(rows):
        if r.get("video_id") == video_id:
            idx_by_vid = i
            break

    new_id = generation_id or str(uuid.uuid4())

    entry: Dict[str, Any] = {
        "generation_id": new_id,
        "video_id": video_id,
        "workflow": workflow,
        "mood": mood,
        "duration_seconds": duration_seconds,
        "params": params_out,
        "metadata": metadata or {},
        "generated_at": generated_at or now,
        "uploaded_at": now,
        "updated_at": now,
    }
    if commit_sha:
        entry["commit_sha"] = commit_sha

    if idx_by_gen is not None:
        prev = rows[idx_by_gen]
        entry["generation_id"] = prev.get("generation_id", new_id)
        entry["generated_at"] = prev.get("generated_at", entry["generated_at"])
        rows[idx_by_gen].update(entry)
        save_generations(data)
        return entry["generation_id"]

    if idx_by_vid is not None:
        prev = rows[idx_by_vid]
        if generation_id:
            entry["generation_id"] = generation_id
        else:
            entry["generation_id"] = prev.get("generation_id", new_id)
        entry["generated_at"] = prev.get("generated_at", entry["generated_at"])
        rows[idx_by_vid].update(entry)
        save_generations(data)
        return entry["generation_id"]

    rows.append(entry)
    save_generations(data)
    return entry["generation_id"]


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
    """CLI/legacy: log by video_id (assigns generation_id if new)."""
    record_generation_upload(
        video_id=video_id,
        workflow=workflow,
        generation_id=None,
        mood=mood,
        duration_seconds=duration_seconds,
        params=params,
        metadata=metadata,
        generated_at=generated_at or uploaded_at,
    )
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
