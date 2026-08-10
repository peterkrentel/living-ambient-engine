#!/usr/bin/env python3
"""Gemini Lite recommendation engine for content strategy.

Reads all analytics metrics (and optionally YouTube trend data) and asks
Gemini to recommend the best next content to produce for virality.

Usage (CLI)::

    python -m agent.gemini_advisor
    python -m agent.gemini_advisor --trends-file data/youtube_trends.json
    python -m agent.gemini_advisor --out data/gemini_recommendation.json

Environment variables:

- ``GEMINI_API_KEY``: Google AI / Gemini API key (required).
- ``ANALYTICS_JSON_PATH``: path to analytics JSON (default ``data/analytics.json``).

Spec: docs/spec/AGENT.md
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import google.generativeai as genai  # type: ignore

    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

DATA_DIR = Path("data")
DEFAULT_ANALYTICS_JSON = str(DATA_DIR / "analytics.json")
DEFAULT_OUT = str(DATA_DIR / "gemini_recommendation.json")
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


def _gemini_model() -> str:
    return (os.environ.get("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _analytics_json_path() -> Path:
    return Path(os.environ.get("ANALYTICS_JSON_PATH", DEFAULT_ANALYTICS_JSON))


def _load_analytics() -> Dict[str, Any]:
    path = _analytics_json_path()
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {"videos": []}


def _load_trends(trends_file: Optional[str]) -> List[Dict[str, Any]]:
    if not trends_file:
        return []
    p = Path(trends_file)
    if not p.exists():
        return []
    with open(p) as f:
        data = json.load(f)
    return data.get("trends", data) if isinstance(data, dict) else data


def _top_performers(videos: List[Dict[str, Any]], n: int = 10) -> List[Dict[str, Any]]:
    """Return top-n videos by views (for the prompt summary)."""
    with_views = [v for v in videos if v.get("metrics", {}).get("views")]
    return sorted(with_views, key=lambda v: v["metrics"]["views"], reverse=True)[:n]


def _build_prompt(
    analytics: Dict[str, Any],
    trends: List[Dict[str, Any]],
) -> str:
    """Build the Gemini prompt from analytics and optional trend data."""
    videos = analytics.get("videos", [])
    date_range = analytics.get("date_range") or {}

    # Aggregate totals
    total_views = sum(v.get("metrics", {}).get("views", 0) for v in videos)
    total_wt = sum(v.get("metrics", {}).get("watch_time_minutes", 0) for v in videos)
    avg_ret_vals = [
        v["metrics"]["average_view_percentage"]
        for v in videos
        if v.get("metrics", {}).get("average_view_percentage")
    ]
    avg_ret = sum(avg_ret_vals) / len(avg_ret_vals) if avg_ret_vals else 0.0

    top = _top_performers(videos)
    top_lines = "\n".join(
        f"  - \"{v.get('title', v['video_id'])}\": "
        f"{v['metrics'].get('views', 0):,} views, "
        f"{v['metrics'].get('average_view_percentage', 0):.1f}% retention, "
        f"{v['metrics'].get('watch_time_minutes', 0):,.0f} min watch time"
        for v in top
    )

    # Mood breakdown
    mood_stats: Dict[str, Dict[str, Any]] = {}
    for v in videos:
        mood = v.get("mood") or "unknown"
        s = mood_stats.setdefault(mood, {"count": 0, "views": 0, "ret_sum": 0, "ret_n": 0})
        s["count"] += 1
        s["views"] += v.get("metrics", {}).get("views", 0)
        r = v.get("metrics", {}).get("average_view_percentage")
        if r:
            s["ret_sum"] += r
            s["ret_n"] += 1

    mood_lines = "\n".join(
        f"  - {mood}: {s['count']} videos, {s['views']:,} views, "
        f"avg retention {s['ret_sum']/s['ret_n']:.1f}%"
        if s["ret_n"] > 0
        else f"  - {mood}: {s['count']} videos, {s['views']:,} views"
        for mood, s in sorted(mood_stats.items(), key=lambda x: x[1]["views"], reverse=True)
    )

    # Trend section
    if trends:
        trend_lines = "\n".join(
            f"  - \"{t.get('title', 'Unknown')}\""
            f"{(' — ' + t['description'][:120]) if t.get('description') else ''}"
            for t in trends[:20]
        )
        trend_section = f"\n\n## Current YouTube Trending Topics\n{trend_lines}"
    else:
        trend_section = ""

    dr_str = ""
    if date_range.get("start") and date_range.get("end"):
        dr_str = f" (analytics window: {date_range['start']} → {date_range['end']})"

    prompt = f"""You are a viral YouTube content strategist for a channel producing ambient / lo-fi / focus music videos.

## Channel Performance Summary{dr_str}

- Total videos tracked: {len(videos)}
- Total views: {total_views:,}
- Total watch time: {total_wt:,.0f} minutes
- Average view retention: {avg_ret:.1f}%

## Top Performing Videos
{top_lines or "  (no data yet)"}

## Performance by Mood / Category
{mood_lines or "  (no data yet)"}
{trend_section}

## Your Task

Based on all the metrics above{' and the trending topics' if trends else ''}, recommend the **next 3 content ideas** this channel should produce to maximise views, watch time, and subscriber growth (virality).

For each recommendation, provide:
1. **Title** — a compelling YouTube title (include keyword hooks)
2. **Mood / category** — which mood preset fits best (e.g. deep_focus, rain_sleep, lofi_study, etc.)
3. **Visual style** — which visual pattern to use and why (choose from: fibonacci_spiral, sacred_geometry, fractal_zoom, julia, starfield, rain_window, fireplace, aurora_borealis, nebula, lissajous, plasma, vortex, particle_flow, geometric_morph)
4. **Duration** — recommended length (5, 10, 30, 60, or 180 minutes) and why
5. **Rationale** — concise reasoning based on the data above

Also provide a brief **Overall Strategy** paragraph (3-5 sentences) on what the data reveals and how to grow the channel.

Respond in structured JSON using this schema:
{{
  "strategy": "<Overall strategy paragraph>",
  "recommendations": [
    {{
      "title": "<YouTube title>",
      "mood": "<mood preset>",
      "visual_style": "<pattern>",
      "duration_minutes": <number>,
      "rationale": "<data-driven reasoning>"
    }}
  ]
}}
"""
    return prompt


# ---------------------------------------------------------------------------
# Main advisor class
# ---------------------------------------------------------------------------


class GeminiAdvisor:
    """Ask Gemini Lite for content strategy recommendations."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        if not HAS_GENAI:
            raise ImportError(
                "google-generativeai not installed. "
                "Install with: pip install google-generativeai"
            )
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY environment variable or pass api_key."
            )
        genai.configure(api_key=self.api_key)
        self._model_name = model or _gemini_model()
        self.model = genai.GenerativeModel(self._model_name)

    def get_recommendation(
        self,
        analytics: Dict[str, Any],
        trends: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Ask Gemini for a content recommendation.

        Args:
            analytics: Analytics data (same schema as ``data/analytics.json``).
            trends: Optional list of YouTube trending video dicts.

        Returns:
            Dict with ``strategy``, ``recommendations``, ``model``, ``generated_at``.
        """
        prompt = _build_prompt(analytics, trends or [])
        response = self.model.generate_content(prompt)
        raw_text = response.text.strip()

        # Strip markdown code fences if present
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            # Remove first line (```json or ```) and last line (```)
            lines = [line for line in lines if not line.strip().startswith("```")]
            raw_text = "\n".join(lines).strip()

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            # Gemini sometimes adds prose before/after JSON — try to extract the JSON block
            import re

            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                parsed = json.loads(match.group())
            else:
                # Return raw text as fallback so callers can still log it
                parsed = {"raw_response": raw_text}

        parsed["model"] = self._model_name
        parsed["generated_at"] = datetime.now(timezone.utc).isoformat()
        return parsed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Get Gemini content recommendations from analytics metrics"
    )
    parser.add_argument(
        "--trends-file",
        help="Path to YouTube trends JSON (produced by youtube/trend_advisor.py)",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help=f"Output JSON path (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--model",
        default=_gemini_model(),
        help=f"Gemini model to use (default: {_gemini_model()})",
    )
    args = parser.parse_args()

    print("🤖 Loading analytics...")
    analytics = _load_analytics()
    n_videos = len(analytics.get("videos", []))
    if n_videos == 0:
        print("⚠️  No analytics data found. Run fetch_analytics first.")
        sys.exit(0)
    print(f"   {n_videos} videos loaded.")

    trends: List[Dict[str, Any]] = []
    if args.trends_file:
        trends = _load_trends(args.trends_file)
        print(f"   {len(trends)} trending topics loaded from {args.trends_file}.")

    print("🧠 Asking Gemini for recommendations...")
    try:
        advisor = GeminiAdvisor(model=args.model)
        result = advisor.get_recommendation(analytics, trends)
    except ImportError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Recommendation saved to {out_path}")
    print()

    # Pretty-print to terminal
    strategy = result.get("strategy", "")
    if strategy:
        print("📊 Strategy:")
        print(f"   {strategy}")
        print()

    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"🎬 Recommendation {i}: {rec.get('title', '?')}")
        print(f"   Mood:     {rec.get('mood', '?')}")
        print(f"   Visual:   {rec.get('visual_style', '?')}")
        print(f"   Duration: {rec.get('duration_minutes', '?')} min")
        print(f"   Why:      {rec.get('rationale', '?')}")
        print()


if __name__ == "__main__":
    main()
