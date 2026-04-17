#!/usr/bin/env python3
"""Gated planner v0: suggestions.json → run intent JSON or BLOCKED report.

Reads ``data/suggestions.json`` (brand correlate output). Emits either:
  - ``data/run_intent.json`` — matches ``docs/spec/contracts/production-run-intent.md`` v1, or
  - ``data/reports/run-intent-blocked.md`` — human-readable reasons (no intent file).

**Gates (conservative):** only ``action=increase`` rows with ``type=mood`` and ``actionable=true``
(n≥5, group_views≥200 per correlate). No auto-upload by default: ``upload`` stays ``false`` unless
``--upload`` is passed; CI upload still requires ``run-intent-consumer`` + ``confirm_upload`` when intent requests upload.

**Overrides (explicit human / CI smoke):** ``--force-moods a,b`` skips suggestion mining and
writes intent if moods validate against ``config/moods.yaml``.

Spec: ``docs/spec/contracts/production-run-intent.md`` · Roadmap: ``docs/COHESION_ROADMAP.md`` Phase 6.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

_REPO = Path(__file__).resolve().parents[1]
SUGGESTIONS_PATH = _REPO / "data" / "suggestions.json"
INTENT_PATH = _REPO / "data" / "run_intent.json"
BLOCKED_PATH = _REPO / "data" / "reports" / "run-intent-blocked.md"
MOODS_YAML = _REPO / "config" / "moods.yaml"

# Mirror scripts/correlate.py / AGENT.md actionability gates
MIN_SAMPLE_SIZE = 5
MIN_GROUP_VIEWS = 200

ALLOWED_DURATIONS = frozenset(
    {"30s", "1min", "5min", "10min", "30m", "1h", "2h", "3h", "4h", "1.5h"}
)


def load_factory_moods() -> list[str]:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with open(MOODS_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return sorted(data.keys())


def validate_duration(label: str) -> str:
    s = label.strip()
    if s not in ALLOWED_DURATIONS:
        raise SystemExit(f"Unknown duration {s!r}; allowed: {sorted(ALLOWED_DURATIONS)}")
    return s


def moods_from_suggestions(data: dict) -> tuple[list[str], list[str]]:
    """Return (mood_names, block_reasons). Reasons accumulate if empty."""
    reasons: list[str] = []
    rows = data.get("suggestions") or []
    picked: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if row.get("type") != "mood":
            continue
        if row.get("action") != "increase":
            continue
        if not row.get("actionable"):
            reasons.append(
                f"Mood {row.get('name')!r}: not actionable "
                f"(n={row.get('sample_size')}, views={row.get('group_views')}, "
                f"need n≥{MIN_SAMPLE_SIZE} and views≥{MIN_GROUP_VIEWS})."
            )
            continue
        name = row.get("name")
        if not name or name in seen:
            continue
        seen.add(name)
        picked.append(str(name))
    return picked, reasons


def write_blocked(text: str) -> None:
    INTENT_PATH.unlink(missing_ok=True)
    BLOCKED_PATH.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(
        [
            "# Run intent — BLOCKED",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            text,
            "",
            "---",
            "*Produced by `scripts/plan_run_intent.py`.*",
            "",
        ]
    )
    BLOCKED_PATH.write_text(body, encoding="utf-8")
    print(f"⛔ BLOCKED — wrote {BLOCKED_PATH.relative_to(_REPO)}")
    print(text)


def write_intent(
    *,
    moods: list[str],
    channel: str,
    duration: str,
    dual: bool,
    upload: bool,
    max_videos: int | None,
) -> None:
    BLOCKED_PATH.unlink(missing_ok=True)
    intent = {
        "schema_version": 1,
        "channel": channel,
        "moods": moods,
        "duration": duration,
        "dual": dual,
        "upload": upload,
        "max_videos": max_videos,
    }
    INTENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    INTENT_PATH.write_text(json.dumps(intent, indent=2) + "\n", encoding="utf-8")
    print(f"✅ Wrote {INTENT_PATH.relative_to(_REPO)}")
    print(json.dumps(intent, indent=2))


def main() -> int:
    os.chdir(_REPO)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--suggestions",
        type=Path,
        default=SUGGESTIONS_PATH,
        help="Path to suggestions.json",
    )
    parser.add_argument(
        "--channel",
        choices=("brand", "personal"),
        default=os.environ.get("RUN_INTENT_CHANNEL", "brand"),
    )
    parser.add_argument("--duration", default=os.environ.get("RUN_INTENT_DURATION", "10min"))
    parser.add_argument(
        "--dual",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--upload",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="If true, intent requests upload (default false until CI consumer validates this).",
    )
    parser.add_argument(
        "--max-moods",
        type=int,
        default=int(os.environ.get("RUN_INTENT_MAX_MOODS", "4")),
        help="Cap moods taken from actionable suggestions.",
    )
    parser.add_argument(
        "--force-moods",
        type=str,
        default="",
        help="Comma-separated moods: skip suggestions and emit intent (must exist in moods.yaml).",
    )
    args = parser.parse_args()

    try:
        duration = validate_duration(args.duration)
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 1

    valid_moods = set(load_factory_moods())

    if args.force_moods.strip():
        moods = [m.strip() for m in args.force_moods.split(",") if m.strip()]
        bad = [m for m in moods if m not in valid_moods]
        if bad:
            write_blocked(
                f"**--force-moods** contains unknown moods: {bad!r}.\n\n"
                f"Valid keys are from `config/moods.yaml`."
            )
            return 0
        if not moods:
            write_blocked("**--force-moods** was empty after parsing.")
            return 0
        write_intent(
            moods=moods[: args.max_moods],
            channel=args.channel,
            duration=duration,
            dual=args.dual,
            upload=args.upload,
            max_videos=None,
        )
        return 0

    if not args.suggestions.exists():
        write_blocked(f"**Missing file:** `{args.suggestions}` — run `scripts/correlate.py` / Analytics Agent first.")
        return 0

    with open(args.suggestions, encoding="utf-8") as f:
        data = json.load(f)

    moods, reasons = moods_from_suggestions(data)
    moods = [m for m in moods if m in valid_moods]
    moods = moods[: args.max_moods]

    if not moods:
        lines = [
            "**No actionable mood increases** in `suggestions.json` passed the planner gate.",
            "",
            f"- Require `type=mood`, `action=increase`, `actionable=true` (n≥{MIN_SAMPLE_SIZE}, group_views≥{MIN_GROUP_VIEWS}).",
            "",
        ]
        if reasons:
            lines.append("**Exploratory / non-actionable mood rows (sample):**")
            lines.extend(f"- {r}" for r in reasons[:12])
            if len(reasons) > 12:
                lines.append(f"- … ({len(reasons) - 12} more)")
        else:
            lines.append("There were no qualifying mood suggestion rows at all.")
        lines.append("")
        lines.append(
            "**Smoke / dev:** re-run with `--force-moods trance,sleep` (or any valid keys) "
            "to emit `data/run_intent.json` without using suggestions."
        )
        write_blocked("\n".join(lines))
        return 0

    write_intent(
        moods=moods,
        channel=args.channel,
        duration=duration,
        dual=args.dual,
        upload=args.upload,
        max_videos=None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
