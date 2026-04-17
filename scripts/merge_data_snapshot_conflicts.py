#!/usr/bin/env python3
"""Resolve merge conflicts in catalog / ledger / library markdown (append-only union).

Intended for GitHub Actions when two upload lanes both advance ``content_catalog.json``,
``data/generations.json``, and ``CONTENT_LIBRARY.md``. Run only while a merge is in progress
(``.git/MERGE_HEAD`` exists) and those paths are unmerged.

Reads git stages ``:2:`` (ours / current branch) and ``:3:`` (theirs / merged-in main), unions
records by ``youtube_id`` / ``video_id``, regenerates ``CONTENT_LIBRARY.md`` from the merged
catalog, then writes the working tree. Caller must ``git add`` and ``git commit``.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def _run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=_REPO, text=True)


def _git_show(stage: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{stage}:{path}"], cwd=_REPO)


def _parse_json(blob: bytes) -> dict:
    return json.loads(blob.decode("utf-8"))


def _merge_generations(ours: dict, theirs: dict) -> dict:
    by_vid: dict[str, dict] = {}
    for row in theirs.get("videos") or []:
        vid = row.get("video_id")
        if vid:
            by_vid[vid] = dict(row)
    for row in ours.get("videos") or []:
        vid = row.get("video_id")
        if not vid:
            continue
        if vid not in by_vid:
            by_vid[vid] = dict(row)
        else:
            # Same video_id: prefer row with more keys, then newer uploaded_at
            a, b = by_vid[vid], row
            if len(b) > len(a) or (
                len(b) == len(a)
                and (b.get("uploaded_at") or "") > (a.get("uploaded_at") or "")
            ):
                by_vid[vid] = dict(b)
    sv = max(int(ours.get("schema_version") or 1), int(theirs.get("schema_version") or 1))
    videos = list(by_vid.values())
    return {"schema_version": sv, "videos": videos}


def _merge_catalog(ours: dict, theirs: dict) -> dict:
    base_meta = dict(theirs)
    by_yt: dict[str, dict] = {}
    for row in theirs.get("videos") or []:
        yid = row.get("youtube_id")
        if yid:
            by_yt[yid] = dict(row)
    for row in ours.get("videos") or []:
        yid = row.get("youtube_id")
        if not yid:
            continue
        if yid not in by_yt:
            by_yt[yid] = dict(row)
        else:
            a, b = by_yt[yid], row
            if len(b) > len(a) or (
                len(b) == len(a)
                and (b.get("uploaded_at") or "") > (a.get("uploaded_at") or "")
            ):
                by_yt[yid] = dict(b)
    videos = list(by_yt.values())
    base_meta["videos"] = videos
    base_meta["total_videos"] = len(videos)
    base_meta["last_updated"] = datetime.now(timezone.utc).isoformat()
    return base_meta


def _regenerate_content_library(catalog_path: Path) -> None:
    sys.path.insert(0, str(_REPO))
    from library.catalog import ContentLibrary  # noqa: PLC0415

    lib = ContentLibrary(catalog_path=str(catalog_path))
    lib.export_markdown()


def main() -> int:
    merge_head = _REPO / ".git" / "MERGE_HEAD"
    if not merge_head.exists():
        print("❌ No merge in progress (.git/MERGE_HEAD missing).", file=sys.stderr)
        return 1

    unmerged = set(
        _run_git(["diff", "--name-only", "--diff-filter=U"]).strip().splitlines()
    )
    allowed = {"data/generations.json", "content_catalog.json", "CONTENT_LIBRARY.md"}
    foreign = sorted(unmerged - allowed)
    if foreign:
        print(
            "❌ Unmerged files this script does not handle: " + ", ".join(foreign),
            file=sys.stderr,
        )
        return 1

    json_targets = ("data/generations.json", "content_catalog.json")
    resolved_json: list[str] = []
    for rel in json_targets:
        if rel not in unmerged:
            continue
        try:
            raw_ours = _git_show("2", rel)
            raw_theirs = _git_show("3", rel)
        except subprocess.CalledProcessError as e:
            print(f"❌ Could not read merge stages for {rel}: {e}", file=sys.stderr)
            return 1
        out = _REPO / rel
        if rel == "data/generations.json":
            merged = _merge_generations(_parse_json(raw_ours), _parse_json(raw_theirs))
            out.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
            print(f"✅ Resolved {rel} ({len(merged['videos'])} videos)")
        else:
            merged = _merge_catalog(_parse_json(raw_ours), _parse_json(raw_theirs))
            out.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
            print(f"✅ Resolved {rel} ({len(merged['videos'])} videos)")
        resolved_json.append(rel)

    if not resolved_json and "CONTENT_LIBRARY.md" not in unmerged:
        print(
            "❌ Expected unmerged data/generations.json and/or content_catalog.json.",
            file=sys.stderr,
        )
        print(f"   Unmerged: {sorted(unmerged) or '(none)'}", file=sys.stderr)
        return 1

    cat_path = _REPO / "content_catalog.json"
    if not cat_path.exists():
        print("❌ content_catalog.json missing after merge resolution.", file=sys.stderr)
        return 1
    try:
        json.loads(cat_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ content_catalog.json is not valid JSON: {e}", file=sys.stderr)
        return 1

    regen_lib = ("content_catalog.json" in unmerged) or ("CONTENT_LIBRARY.md" in unmerged)
    if regen_lib:
        _regenerate_content_library(cat_path)
        print("✅ Regenerated CONTENT_LIBRARY.md from merged catalog")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
