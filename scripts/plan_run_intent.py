#!/usr/bin/env python3
"""Gated planner v0: suggestions.json → run intent JSON or BLOCKED report.

Reads suggestions JSON (default ``data/suggestions.json`` for brand). Emits either:
  - Intent JSON (default ``data/run_intent.json``) — matches ``docs/spec/contracts/production-run-intent.md`` v1, or
  - Blocked report (default ``data/reports/run-intent-blocked.md``) — human-readable reasons (no intent file).

**Personal lane:** pass ``--suggestions data/suggestions_personal.json``, ``--channel personal``,
``--intent-output data/run_intent_personal.json``, ``--blocked-output data/reports/run-intent-blocked-personal.md``.

**Gates (conservative):** only ``action=increase`` rows with ``type=mood`` and ``actionable=true``
(n≥5, group_views≥200 per correlate). No auto-upload by default: ``upload`` stays ``false`` unless
``--upload`` is passed; CI upload still requires ``run-intent-consumer`` + ``confirm_upload`` when intent requests upload.

**Overrides (explicit human / CI smoke):** ``--force-moods a,b`` skips suggestion mining and
writes intent if moods validate against ``config/moods.yaml``.

**Anti-repeat (optional):** When ``--anti-repeat-weeks N`` is positive (or env
``RUN_INTENT_ANTI_REPEAT_WEEKS``), drop any mood whose **(mood, duration_seconds)** matches a row
in ``data/generations.json`` for the **same** ``channel`` with ``uploaded_at`` in the last **N×7**
days. Rows **without** ``channel`` or ``uploaded_at`` are ignored (safe for legacy ledger).
Default **N=0** (off). **Brand** and **personal** lanes each use their own channel filter.

Spec: ``docs/spec/contracts/production-run-intent.md`` · Roadmap: ``docs/COHESION_ROADMAP.md`` Phase 6.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

_REPO = Path(__file__).resolve().parents[1]
SUGGESTIONS_PATH = _REPO / "data" / "suggestions.json"
MOODS_YAML = _REPO / "config" / "moods.yaml"

# Mirror scripts/correlate.py / AGENT.md actionability gates
MIN_SAMPLE_SIZE = 5
MIN_GROUP_VIEWS = 200

ALLOWED_DURATIONS = frozenset(
    {"5s", "10s", "30s", "1min", "5min", "10min", "30m", "1h", "2h", "3h", "4h", "1.5h"}
)


def iso_week_suffix(utc_now: datetime | None = None) -> str:
    """YYYY-Www (UTC ISO week) for filenames and intent provenance."""
    now = utc_now or datetime.now(timezone.utc)
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def _validate_week_label(week: str) -> str:
    s = (week or "").strip()
    if not s:
        raise SystemExit("week must be non-empty")
    if not re.match(r"^\d{4}-W\d{2}$", s):
        raise SystemExit(f"week must match YYYY-Www, got {s!r}")
    return s


def load_factory_moods() -> list[str]:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with open(MOODS_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return sorted(data.keys())


def validate_duration(label: str) -> str:
    s = label.strip()
    if s not in ALLOWED_DURATIONS:
        raise SystemExit(f"Unknown duration {s!r}; allowed: {sorted(ALLOWED_DURATIONS)}")
    return s


def duration_label_to_seconds(label: str) -> int:
    """Parse intent duration label to seconds (aligned with ``batch_generate.parse_duration``)."""
    duration_str = label.strip().lower()
    match = re.match(
        r"^(\d+(?:\.\d+)?)\s*(h|hr|hour|hours|m|min|mins|minutes|s|sec|secs|seconds)?$",
        duration_str,
    )
    if not match:
        raise ValueError(f"Invalid duration format: {label!r}")
    value = float(match.group(1))
    unit = match.group(2) or "s"
    if unit in ("h", "hr", "hour", "hours"):
        return int(value * 3600)
    if unit in ("m", "min", "mins", "minutes"):
        return int(value * 60)
    if unit in ("s", "sec", "secs", "seconds"):
        return int(value)
    return int(value)


def parse_iso_datetime(value: object) -> datetime | None:
    """Parse ledger ISO timestamps to timezone-aware UTC."""
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def recent_blocked_mood_duration_keys(
    generations_path: Path,
    *,
    channel: str,
    weeks: int,
    now_utc: datetime | None = None,
) -> set[tuple[str, int]]:
    """(mood, duration_seconds) keys uploaded on ``channel`` within the last ``weeks``×7 days."""
    if weeks <= 0:
        return set()
    path = _resolve_repo_path(generations_path)
    if not path.is_file():
        return set()
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return set()
    videos = data.get("videos") if isinstance(data, dict) else None
    if not isinstance(videos, list):
        return set()
    now = now_utc or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=7 * weeks)
    out: set[tuple[str, int]] = set()
    for row in videos:
        if not isinstance(row, dict):
            continue
        row_ch = row.get("channel")
        if not isinstance(row_ch, str) or row_ch.strip().lower() != channel:
            continue
        mood = row.get("mood")
        if not isinstance(mood, str) or not mood.strip():
            continue
        dur_raw = row.get("duration_seconds")
        if isinstance(dur_raw, bool):
            continue
        if isinstance(dur_raw, float) and dur_raw.is_integer():
            dur = int(dur_raw)
        elif isinstance(dur_raw, int):
            dur = dur_raw
        else:
            continue
        ts = parse_iso_datetime(row.get("uploaded_at"))
        if ts is None:
            continue
        if ts < cutoff:
            continue
        out.add((mood.strip(), dur))
    return out


def filter_moods_anti_repeat(
    moods: list[str],
    *,
    duration_seconds: int,
    blocked: set[tuple[str, int]],
) -> tuple[list[str], list[str]]:
    """Drop moods that collide with ``blocked``; return (kept, skip_reason_lines)."""
    kept: list[str] = []
    skipped: list[str] = []
    for m in moods:
        if (m, duration_seconds) in blocked:
            skipped.append(
                f"- {m!r} @ {duration_seconds}s — same mood×duration uploaded on this channel inside the anti-repeat window."
            )
        else:
            kept.append(m)
    return kept, skipped


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


def _resolve_repo_path(p: Path) -> Path:
    return p if p.is_absolute() else (_REPO / p)


def write_blocked(text: str, *, intent_path: Path, blocked_path: Path) -> None:
    intent_path = _resolve_repo_path(intent_path)
    blocked_path = _resolve_repo_path(blocked_path)
    intent_path.unlink(missing_ok=True)
    blocked_path.parent.mkdir(parents=True, exist_ok=True)
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
    blocked_path.write_text(body, encoding="utf-8")
    print(f"⛔ BLOCKED — wrote {blocked_path.relative_to(_REPO)}")
    print(text)


def write_intent(
    *,
    moods: list[str],
    channel: str,
    week: str,
    suggestions_generated_at: str | None,
    duration: str,
    dual: bool,
    upload: bool,
    max_videos: int | None,
    intent_path: Path,
    blocked_path: Path,
) -> None:
    intent_path = _resolve_repo_path(intent_path)
    blocked_path = _resolve_repo_path(blocked_path)
    blocked_path.unlink(missing_ok=True)
    intent = {
        "schema_version": 2,
        "channel": channel,
        "week": week,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "suggestions_generated_at": suggestions_generated_at,
        "moods": moods,
        "duration": duration,
        "dual": dual,
        "upload": upload,
        "max_videos": max_videos,
    }
    intent_path.parent.mkdir(parents=True, exist_ok=True)
    intent_path.write_text(json.dumps(intent, indent=2) + "\n", encoding="utf-8")
    print(f"✅ Wrote {intent_path.relative_to(_REPO)}")
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
    parser.add_argument(
        "--intent-output",
        type=Path,
        default=Path("data/run_intent.json"),
        help="Path for run intent JSON (repo-relative or absolute).",
    )
    parser.add_argument(
        "--blocked-output",
        type=Path,
        default=Path("data/reports/run-intent-blocked.md"),
        help="Path for BLOCKED markdown when no intent is emitted.",
    )
    parser.add_argument(
        "--week",
        default=os.environ.get("RUN_INTENT_WEEK", ""),
        help="ISO week label e.g. 2026-W18 (default: current UTC ISO week)",
    )
    parser.add_argument(
        "--generations-json",
        type=Path,
        default=Path(os.environ.get("RUN_INTENT_GENERATIONS_JSON", "data/generations.json")),
        help="Ledger path for anti-repeat (default: data/generations.json).",
    )
    parser.add_argument(
        "--anti-repeat-weeks",
        type=int,
        default=int(os.environ.get("RUN_INTENT_ANTI_REPEAT_WEEKS", "0")),
        metavar="N",
        help="Drop mood×duration if present on this channel in generations.json within N×7 days (0=off).",
    )
    args = parser.parse_args()

    intent_out = _resolve_repo_path(args.intent_output)
    blocked_out = _resolve_repo_path(args.blocked_output)
    sug_path = _resolve_repo_path(args.suggestions)
    try:
        sug_rel = sug_path.relative_to(_REPO)
    except ValueError:
        sug_rel = sug_path
    try:
        intent_rel = intent_out.relative_to(_REPO)
    except ValueError:
        intent_rel = intent_out

    try:
        duration = validate_duration(args.duration)
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 1
    try:
        week = _validate_week_label(args.week.strip() or iso_week_suffix())
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 1

    anti_weeks = max(0, args.anti_repeat_weeks)
    gen_path = _resolve_repo_path(args.generations_json)

    try:
        dur_sec = duration_label_to_seconds(duration)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1

    def anti_filter(moods_in: list[str]) -> tuple[list[str], list[str]]:
        if anti_weeks <= 0:
            return moods_in, []
        if not gen_path.is_file():
            print(
                "⚠️ Anti-repeat enabled but generations.json missing — using an empty ledger.",
                file=sys.stderr,
            )
        blocked = recent_blocked_mood_duration_keys(
            gen_path, channel=args.channel, weeks=anti_weeks
        )
        return filter_moods_anti_repeat(moods_in, duration_seconds=dur_sec, blocked=blocked)

    valid_moods = set(load_factory_moods())

    if args.force_moods.strip():
        moods = [m.strip() for m in args.force_moods.split(",") if m.strip()]
        bad = [m for m in moods if m not in valid_moods]
        if bad:
            write_blocked(
                f"**--force-moods** contains unknown moods: {bad!r}.\n\n"
                f"Valid keys are from `config/moods.yaml`.",
                intent_path=intent_out,
                blocked_path=blocked_out,
            )
            return 0
        if not moods:
            write_blocked(
                "**--force-moods** was empty after parsing.",
                intent_path=intent_out,
                blocked_path=blocked_out,
            )
            return 0
        moods, anti_skips = anti_filter(moods)
        moods = moods[: args.max_moods]
        if not moods:
            write_blocked(
                "**Anti-repeat (generations ledger)** removed every `--force-moods` candidate for this "
                f"channel×duration (`{duration}`).\n\n"
                f"Window: last **{anti_weeks}** week(s), channel=`{args.channel}`.\n\n"
                "**Skipped:**\n"
                + "\n".join(anti_skips)
                + "\n\n**Mitigations:** lower `--anti-repeat-weeks`, change `--duration`, or pick moods "
                "not recently uploaded on this channel.\n",
                intent_path=intent_out,
                blocked_path=blocked_out,
            )
            return 0
        write_intent(
            moods=moods,
            channel=args.channel,
            week=week,
            suggestions_generated_at=None,
            duration=duration,
            dual=args.dual,
            upload=args.upload,
            max_videos=None,
            intent_path=intent_out,
            blocked_path=blocked_out,
        )
        return 0

    if not sug_path.exists():
        write_blocked(
            f"**Missing file:** `{sug_rel}` — run `scripts/correlate.py` / Analytics Agent first.",
            intent_path=intent_out,
            blocked_path=blocked_out,
        )
        return 0

    with open(sug_path, encoding="utf-8") as f:
        data = json.load(f)

    moods, reasons = moods_from_suggestions(data)
    moods = [m for m in moods if m in valid_moods]
    moods, anti_skips = anti_filter(moods)
    moods = moods[: args.max_moods]

    if not moods:
        if anti_skips and anti_weeks > 0:
            lines = [
                "**Anti-repeat (generations ledger)** removed every actionable candidate for this "
                f"channel×duration (`{duration}`).\n",
                f"Window: last **{anti_weeks}** week(s), channel=`{args.channel}`.\n",
                "",
                "**Skipped:**",
                *anti_skips,
                "",
                "**Mitigations:** lower `--anti-repeat-weeks`, change `--duration`, wait for new uploads "
                "to age out of the window, or use `--force-moods` for an explicit mood not in the window.",
                "",
            ]
            if reasons:
                lines.append("**Context — non-actionable mood rows from correlate (sample):**")
                lines.extend(f"- {r}" for r in reasons[:8])
                lines.append("")
            write_blocked("\n".join(lines), intent_path=intent_out, blocked_path=blocked_out)
            return 0
        lines = [
            f"**No actionable mood increases** in `{sug_rel}` passed the planner gate.",
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
            f"to emit `{intent_rel}` without using suggestions."
        )
        write_blocked("\n".join(lines), intent_path=intent_out, blocked_path=blocked_out)
        return 0

    write_intent(
        moods=moods,
        channel=args.channel,
        week=week,
        suggestions_generated_at=(data.get("generated_at") if isinstance(data, dict) else None),
        duration=duration,
        dual=args.dual,
        upload=args.upload,
        max_videos=None,
        intent_path=intent_out,
        blocked_path=blocked_out,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
