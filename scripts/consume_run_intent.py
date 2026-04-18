#!/usr/bin/env python3
"""Validate ``data/run_intent.json`` (production-run-intent v1) for CI consumers.

Exits **1** on invalid JSON or contract violations (no downstream generate/upload).

When ``--emit-github-output`` is set, expects ``GITHUB_OUTPUT`` and appends
``moods``, ``duration``, ``dual``, ``channel``, ``upload`` for later workflow steps.

``--allow-planner-blocked`` (CI **validate-only**): if the intent file is missing but the
paired ``--blocked-report`` file exists (default ``data/reports/run-intent-blocked.md``;
personal lane: ``…-blocked-personal.md``), exit **0** and document BLOCKED in the Step
Summary — not a failure (planner said “no intent”). Without this flag, missing intent is **1**.

Spec: ``docs/spec/contracts/production-run-intent.md``.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

_REPO = Path(__file__).resolve().parents[1]
DEFAULT_INTENT = _REPO / "data" / "run_intent.json"
DEFAULT_BLOCKED = _REPO / "data" / "reports" / "run-intent-blocked.md"
MOODS_YAML = _REPO / "config" / "moods.yaml"

ALLOWED_DURATIONS = frozenset(
    {"5s", "10s", "30s", "1min", "5min", "10min", "30m", "1h", "2h", "3h", "4h", "1.5h"}
)


def load_factory_moods(path: Path | None = None) -> dict[str, object]:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    p = path or MOODS_YAML
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate_and_normalize(
    data: object,
    *,
    moods_yaml: Path | None = None,
) -> dict:
    """Return normalized intent dict (``moods`` possibly truncated). Raises ValueError."""
    if not isinstance(data, dict):
        raise ValueError("Intent root must be a JSON object")

    if data.get("schema_version") != 1:
        raise ValueError(f"schema_version must be 1, got {data.get('schema_version')!r}")

    channel = data.get("channel")
    if channel not in ("brand", "personal"):
        raise ValueError(f"channel must be 'brand' or 'personal', got {channel!r}")

    moods = data.get("moods")
    if not isinstance(moods, list) or not moods:
        raise ValueError("moods must be a non-empty array of strings")
    for m in moods:
        if not isinstance(m, str) or not m.strip():
            raise ValueError(f"Invalid mood entry: {m!r}")

    duration = data.get("duration")
    if not isinstance(duration, str) or duration.strip() not in ALLOWED_DURATIONS:
        raise ValueError(
            f"duration must be one of {sorted(ALLOWED_DURATIONS)}, got {duration!r}"
        )
    duration = duration.strip()

    dual = data.get("dual")
    if not isinstance(dual, bool):
        raise ValueError("dual must be a JSON boolean")

    upload = data.get("upload")
    if not isinstance(upload, bool):
        raise ValueError("upload must be a JSON boolean")

    max_videos = data.get("max_videos")
    if max_videos is not None:
        if not isinstance(max_videos, int) or max_videos < 1:
            raise ValueError("max_videos must be null or a positive integer")

    factory = load_factory_moods(moods_yaml)
    valid_keys = set(factory.keys())
    unknown = [m for m in moods if m not in valid_keys]
    if unknown:
        raise ValueError(f"Unknown mood(s) not in factory config: {unknown}")

    out_moods = [str(m) for m in moods]
    if max_videos is not None:
        out_moods = out_moods[:max_videos]
    if not out_moods:
        raise ValueError("After max_videos cap, moods list is empty")

    return {
        "schema_version": 1,
        "channel": channel,
        "moods": out_moods,
        "duration": duration,
        "dual": dual,
        "upload": upload,
        "max_videos": max_videos,
    }


def _github_output_set(name: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        raise RuntimeError("GITHUB_OUTPUT is not set")
    with open(path, "a", encoding="utf-8") as fh:
        if "\n" in value:
            delim = f"DELIM_{name}"
            fh.write(f"{name}<<{delim}\n{value}\n{delim}\n")
        else:
            fh.write(f"{name}={value}\n")


def emit_github_outputs(normalized: dict) -> None:
    _github_output_set("moods", ",".join(normalized["moods"]))
    _github_output_set("duration", normalized["duration"])
    _github_output_set("dual", "true" if normalized["dual"] else "false")
    _github_output_set("channel", normalized["channel"])
    _github_output_set("upload", "true" if normalized["upload"] else "false")


def append_step_summary(text: str) -> None:
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if not p:
        return
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(text)
        if not text.endswith("\n"):
            fh.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intent", type=Path, default=DEFAULT_INTENT, help="Path to run_intent.json")
    parser.add_argument(
        "--blocked-report",
        type=Path,
        default=DEFAULT_BLOCKED,
        help="Planner BLOCKED report path (paired with --intent for validate-only UX).",
    )
    parser.add_argument(
        "--moods-yaml",
        type=Path,
        default=None,
        help="Override moods.yaml path (tests)",
    )
    parser.add_argument(
        "--emit-github-output",
        action="store_true",
        help="Append moods,duration,dual,channel,upload to GITHUB_OUTPUT",
    )
    parser.add_argument(
        "--allow-planner-blocked",
        action="store_true",
        help="If intent is missing but run-intent-blocked.md exists, exit 0 (validate-only UX).",
    )
    args = parser.parse_args()

    intent_path: Path = args.intent if args.intent.is_absolute() else (_REPO / args.intent)
    blocked_path: Path = (
        args.blocked_report if args.blocked_report.is_absolute() else (_REPO / args.blocked_report)
    )
    if not intent_path.is_file():
        msg = f"Missing intent file: {intent_path}"
        if blocked_path.is_file():
            try:
                blocked_ref = blocked_path.relative_to(_REPO)
            except ValueError:
                blocked_ref = blocked_path
            msg += f"\n\nPlanner wrote {blocked_ref} instead."
            if args.allow_planner_blocked:
                print(msg)
                append_step_summary(
                    "## Run intent consumer\n\n"
                    "**Result:** Planner **BLOCKED** — no validated intent JSON at the path you passed. "
                    f"See `{blocked_ref}`.\n\n"
                    "*This is expected when the analytics gate finds no actionable moods.*\n"
                )
                return 0
        print(msg, file=sys.stderr)
        return 1

    try:
        with open(intent_path, encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {intent_path}: {e}", file=sys.stderr)
        return 1

    try:
        normalized = validate_and_normalize(raw, moods_yaml=args.moods_yaml)
    except (ValueError, RuntimeError) as e:
        print(f"Run intent validation failed: {e}", file=sys.stderr)
        return 1

    summary = (
        "## Run intent (validated)\n\n"
        f"- **Channel:** `{normalized['channel']}`\n"
        f"- **Moods:** {', '.join(normalized['moods'])}\n"
        f"- **Duration:** `{normalized['duration']}`\n"
        f"- **Dual:** `{normalized['dual']}`\n"
        f"- **Upload (in file):** `{normalized['upload']}`\n"
    )
    append_step_summary(summary)
    print(json.dumps(normalized, indent=2))

    if args.emit_github_output:
        try:
            emit_github_outputs(normalized)
        except RuntimeError as e:
            print(e, file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
