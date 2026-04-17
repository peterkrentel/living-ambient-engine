#!/usr/bin/env python3
"""Deterministic weekly advisory: rank next moves from correlate + audit (v0, no LLM).

**Brand** (default): ``data/suggestions.json`` + ``data/reports/audit-YYYY-WW.md`` →
``data/reports/run-next-YYYY-WW.md``.

**Personal** (``--lane personal``): ``data/suggestions_personal.json`` +
``data/reports/audit-YYYY-WW-personal.md`` → ``data/reports/run-next-YYYY-WW-personal.md``.

Run from repo root: ``python scripts/run_next_report.py`` or ``python scripts/run_next_report.py --lane personal``
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SUGGESTIONS_BRAND = _REPO_ROOT / "data" / "suggestions.json"
DEFAULT_SUGGESTIONS_PERSONAL = _REPO_ROOT / "data" / "suggestions_personal.json"
DEFAULT_REPORTS = _REPO_ROOT / "data" / "reports"
DEFAULT_PERSONAL_ANALYTICS = _REPO_ROOT / "data" / "analytics_personal.json"
DEFAULT_BRAND_ANALYTICS = _REPO_ROOT / "data" / "analytics.json"


def _display_path(path: Path) -> str:
    """Repo-relative path when under repo root; else absolute string."""
    try:
        return str(path.resolve().relative_to(_REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def iso_week_suffix(utc_now: datetime | None = None) -> str:
    """YYYY-Www for filenames (calendar ISO week), matching ``audit_channel.py``."""
    now = utc_now or datetime.now(timezone.utc)
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def _metric_label(metric: str | None) -> str:
    m = metric or ""
    if "percentage" in m or m == "average_view_percentage":
        return "retention %"
    if "watch" in m.lower() or m == "watch_time_minutes":
        return "watch min / video (window)"
    return m or "metric"


def _confidence_rank(conf: str | None) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get((conf or "").lower(), 3)


def _sort_actionable(rows: list[tuple[int, dict]]) -> list[tuple[int, dict]]:
    return sorted(
        rows,
        key=lambda t: (_confidence_rank(t[1].get("confidence")), -(t[1].get("group_views") or 0)),
    )


def _sort_exploratory(rows: list[tuple[int, dict]]) -> list[tuple[int, dict]]:
    return sorted(rows, key=lambda t: -(t[1].get("group_views") or 0))


def _audit_overview_excerpt(audit_text: str, max_lines: int = 18) -> str:
    """Return the ## Overview block (trimmed) or empty."""
    lines = audit_text.splitlines()
    out: list[str] = []
    in_overview = False
    for line in lines:
        if line.startswith("## Overview"):
            in_overview = True
            continue
        if in_overview:
            if line.startswith("## "):
                break
            out.append(line)
            if len(out) >= max_lines:
                break
    return "\n".join(out).strip()


def _latest_personal_report(reports_dir: Path) -> Path | None:
    cands = sorted(reports_dir.glob("*-personal.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return cands[0] if cands else None


def _latest_brand_weekly_report(reports_dir: Path) -> Path | None:
    """Latest ``YYYY-WW.md`` (brand weekly performance report), excluding audits/run-next."""
    cands = sorted(
        (
            p
            for p in reports_dir.glob("*.md")
            if re.match(r"^\d{4}-W\d{2}\.md$", p.name)
        ),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return cands[0] if cands else None


def _analytics_snapshot_line(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return f"Present at `{path.relative_to(_REPO_ROOT)}` but could not be read as JSON."
    videos = data.get("videos") or []
    fetched = data.get("fetched_at", "")
    n = len(videos)
    rel = path.relative_to(_REPO_ROOT)
    return f"`{rel}` — **{n}** videos in snapshot; `fetched_at`: {fetched or '—'}"


def build_markdown(
    week: str,
    suggestions_data: dict,
    audit_path: Path | None,
    audit_text: str | None,
    *,
    lane: str,
    suggestions_citation_path: str,
    cross_analytics_summary: str | None,
    cross_latest_report_rel: str | None,
) -> str:
    gen = suggestions_data.get("generated_at") or datetime.now(timezone.utc).isoformat()
    oar = suggestions_data.get("overall_avg_retention")
    oaw = suggestions_data.get("overall_avg_watch_minutes_per_video")
    va = suggestions_data.get("videos_analyzed")
    vw = suggestions_data.get("videos_with_views")
    raw_sug: list[dict] = suggestions_data.get("suggestions") or []

    is_personal = lane == "personal"
    title = f"# Run next — personal advisory ({week})" if is_personal else f"# Run next — advisory ({week})"
    primary = "Personal" if is_personal else "Brand"
    other = "brand" if is_personal else "personal"
    other_title = "Brand lane (cross-read only)" if is_personal else "Personal lane (context only)"
    audit_heading = "Audit — overview excerpt (personal)" if is_personal else "Audit — overview excerpt (brand)"
    audit_evidence_name = f"`data/reports/audit-{week}-personal.md`" if is_personal else f"`data/reports/audit-{week}.md`"
    audit_md_name = f"audit-{week}-personal.md" if is_personal else f"audit-{week}.md"
    ch = "personal" if is_personal else "brand"
    intro_source = f"`{suggestions_citation_path}` and the **{ch}** channel audit (`{audit_md_name}`). "

    lines: list[str] = [
        title,
        "",
        f"Generated (report): {datetime.now(timezone.utc).isoformat()}",
        f"**Correlate bundle `generated_at`:** {gen}",
        "",
        "## How to read this",
        "",
        f"This file is **machine-assembled** from {intro_source}"
        " It is **not** causal advice — see *Packaging & confounders* below.",
        "",
        "### Packaging & confounders",
        "",
        "**CTR, impressions, and retention** often move because of **title, thumbnail, traffic source, "
        "and seasonality** — not because a mood or art-period label “caused” an outcome. "
        "Do **not** treat bucket-level correlation as proof that generation **parameters** drove a result "
        "when **packaging** differed across videos. Correlation addresses **patterns in the data**, not "
        "hidden causes. (Spec: [`docs/spec/AGENT.md`](../../docs/spec/AGENT.md) § *Confounders & packaging*.)",
        "",
        f"## {primary} snapshot (this run)",
        "",
        f"- **Overall avg retention:** {oar}%",
    ]
    if oaw is not None:
        lines.append(f"- **Overall avg watch min / video (window):** {oaw:.3f}")
    lines += [
        f"- **Videos analyzed:** {vw} with views / {va} total",
        "",
        "## Evidence (paths)",
        "",
        f"- **Suggestions:** `{suggestions_citation_path}`",
        f"- **Channel audit:** {audit_evidence_name}",
    ]
    if audit_path and not audit_path.is_file():
        lines.append(f"- **Note:** expected audit file missing on disk (`{_display_path(audit_path)}`).")
    lines.append("")

    indexed = list(enumerate(raw_sug))
    actionable = _sort_actionable([(i, s) for i, s in indexed if s.get("actionable")])
    exploratory = [(i, s) for i, s in indexed if not s.get("actionable")]
    exp_up = _sort_exploratory([(i, s) for i, s in exploratory if s.get("action") == "increase"])
    exp_dn = _sort_exploratory([(i, s) for i, s in exploratory if s.get("action") == "reduce"])

    lines += ["## Actionable (correlate gates passed)", ""]
    if not actionable:
        lines.append("_None this week — all rows are exploratory or below actionable thresholds._")
    else:
        for i, s in actionable[:24]:
            icon = "↑" if s.get("action") == "increase" else "↓"
            ml = _metric_label(s.get("metric"))
            lines.append(
                f"{icon} **`{s.get('type')}` / `{s.get('name')}`** ({ml}) — {s.get('reason', '')} "
                f"— `{s.get('confidence', '')}` — evidence index **`{suggestions_citation_path}` → `suggestions[{i}]`**"
            )
    lines += ["", "## Exploratory — lean in (low n / views)", ""]
    for i, s in exp_up[:12]:
        ml = _metric_label(s.get("metric"))
        lines.append(
            f"↑ `{s.get('type')}` / `{s.get('name')}` ({ml}) — {s.get('reason', '')} "
            f"— `suggestions[{i}]`"
        )
    if not exp_up:
        lines.append('_No exploratory "increase" rows._')
    lines += ["", "## Exploratory — tread carefully (underperformers)", ""]
    for i, s in exp_dn[:12]:
        ml = _metric_label(s.get("metric"))
        lines.append(
            f"↓ `{s.get('type')}` / `{s.get('name')}` ({ml}) — {s.get('reason', '')} "
            f"— `suggestions[{i}]`"
        )
    if not exp_dn:
        lines.append('_No exploratory "reduce" rows._')

    lines += ["", f"## {audit_heading}", ""]
    if audit_text:
        excerpt = _audit_overview_excerpt(audit_text)
        if excerpt:
            lines.append(excerpt)
        else:
            lines.append("_Could not find an `## Overview` section in the audit file._")
    else:
        lines.append("_Audit body not loaded._")

    lines += ["", f"## {other_title}", ""]
    if cross_analytics_summary:
        lines.append(f"- {cross_analytics_summary}")
    else:
        if is_personal:
            lines.append(
                "- No committed `data/analytics.json` found — brand workflow publishes separately."
            )
        else:
            lines.append(
                "- No committed `data/analytics_personal.json` found — personal workflow publishes separately."
            )
    if cross_latest_report_rel:
        lines.append(f"- **Latest {other} markdown report:** `{cross_latest_report_rel}`")
    if is_personal:
        lines.append(
            "- **Not merged** into personal correlate — `data/suggestions.json` remains the **brand** bundle; "
            "compare lanes deliberately ([`docs/PERSONAL_ANALYTICS.md`](../../docs/PERSONAL_ANALYTICS.md))."
        )
    else:
        lines.append(
            "- **Not merged** into brand `suggestions.json` / correlate — use for cross-read only "
            "([`docs/PERSONAL_ANALYTICS.md`](../../docs/PERSONAL_ANALYTICS.md))."
        )

    lines += ["", "## Production hooks (manual)", ""]
    if is_personal:
        ri = _REPO_ROOT / "data" / "run_intent_personal.json"
        blk = _REPO_ROOT / "data" / "reports" / "run-intent-blocked-personal.md"
        intent_label = "`data/run_intent_personal.json`"
        blocked_label = "`data/reports/run-intent-blocked-personal.md`"
        consumer_note = (
            "Set workflow inputs **`intent_path`** = `data/run_intent_personal.json` and "
            "**`blocked_report_path`** = `data/reports/run-intent-blocked-personal.md` when dispatching the consumer."
        )
    else:
        ri = _REPO_ROOT / "data" / "run_intent.json"
        blk = _REPO_ROOT / "data" / "reports" / "run-intent-blocked.md"
        intent_label = "`data/run_intent.json`"
        blocked_label = "`data/reports/run-intent-blocked.md`"
        consumer_note = (
            "Dispatch [`run-intent-consumer.yml`](../../.github/workflows/run-intent-consumer.yml) with default intent paths "
            "(or set **`intent_path`** / **`blocked_report_path`** for the personal lane file pair)."
        )
    if ri.is_file():
        lines.append(
            f"- **{intent_label} present** — validate and run via "
            f"[`run-intent-consumer.yml`](../../.github/workflows/run-intent-consumer.yml) (still **manual** / gated). "
            f"{consumer_note}"
        )
    elif blk.is_file():
        lines.append(f"- **Planner blocked** — see {blocked_label} for this week's gate reason.")
    else:
        lines.append(
            f"- No committed intent JSON or blocked report detected at write time (expected: {intent_label} or {blocked_label})."
        )
    lines.append(
        "- **Batch strategy reminder:** before scaling one lever, skim mood vs algorithm batch intent in "
        "[`piano-batch.yml`](../../.github/workflows/piano-batch.yml) (personal cross-read there)."
    )

    lines += [
        "",
        "---",
        "",
        "*Produced by `scripts/run_next_report.py` (deterministic v0; no LLM, no `batch_generate`).*",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write run-next markdown from suggestions + audit.")
    parser.add_argument("--week", help="ISO week label e.g. 2026-W16 (default: UTC now)")
    parser.add_argument(
        "--lane",
        choices=("brand", "personal"),
        default="brand",
        help="brand → suggestions.json + audit-{week}.md; personal → suggestions_personal + audit-{week}-personal.md",
    )
    parser.add_argument(
        "--suggestions",
        type=Path,
        default=None,
        help="Override path to suggestions JSON (default depends on --lane)",
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=DEFAULT_REPORTS,
        help="Directory for audit input and run-next output",
    )
    parser.add_argument(
        "--personal-analytics",
        type=Path,
        default=DEFAULT_PERSONAL_ANALYTICS,
        help="Path to personal analytics JSON (for brand cross-read; default data/analytics_personal.json)",
    )
    parser.add_argument(
        "--brand-analytics",
        type=Path,
        default=DEFAULT_BRAND_ANALYTICS,
        help="Path to brand analytics JSON (for personal cross-read; default data/analytics.json)",
    )
    args = parser.parse_args(argv)

    lane = args.lane
    default_sug = DEFAULT_SUGGESTIONS_PERSONAL if lane == "personal" else DEFAULT_SUGGESTIONS_BRAND
    sug_path: Path = args.suggestions or default_sug
    reports_dir: Path = args.reports_dir
    if not sug_path.is_file():
        print(f"❌ Missing suggestions file: {sug_path}", file=sys.stderr)
        return 1

    week = (args.week or "").strip() or iso_week_suffix()
    if not re.match(r"^\d{4}-W\d{2}$", week):
        print(f"❌ Invalid --week {week!r} (expected YYYY-Www)", file=sys.stderr)
        return 1

    with sug_path.open(encoding="utf-8") as f:
        suggestions_data = json.load(f)

    if lane == "personal":
        audit_path = reports_dir / f"audit-{week}-personal.md"
        out_path = reports_dir / f"run-next-{week}-personal.md"
        cross_summary = _analytics_snapshot_line(args.brand_analytics)
        latest_br = _latest_brand_weekly_report(reports_dir)
        cross_report = str(latest_br.relative_to(_REPO_ROOT)) if latest_br else None
    else:
        audit_path = reports_dir / f"audit-{week}.md"
        out_path = reports_dir / f"run-next-{week}.md"
        cross_summary = _analytics_snapshot_line(args.personal_analytics)
        latest_pr = _latest_personal_report(reports_dir)
        cross_report = str(latest_pr.relative_to(_REPO_ROOT)) if latest_pr else None

    try:
        suggestions_citation = str(sug_path.resolve().relative_to(_REPO_ROOT))
    except ValueError:
        suggestions_citation = str(sug_path.resolve())

    audit_text: str | None = None
    if audit_path.is_file():
        audit_text = audit_path.read_text(encoding="utf-8")

    body = build_markdown(
        week,
        suggestions_data,
        audit_path,
        audit_text,
        lane=lane,
        suggestions_citation_path=suggestions_citation,
        cross_analytics_summary=cross_summary,
        cross_latest_report_rel=cross_report,
    )

    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    print(f"✅ Wrote {_display_path(out_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
