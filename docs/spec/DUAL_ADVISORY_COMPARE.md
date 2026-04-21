# Dual advisory — how to read and compare (v0)

**Advisory only.** These markdown files are **not** `run_intent`, **not** `batch_generate`, and **not** causal proof. Use them beside **deterministic** [`run-next`](../../scripts/run_next_report.py) output and committed **JSON** ([`AGENT.md`](./AGENT.md) guardrails).

**Script:** [`scripts/agent_dual_advisory.py`](../../scripts/agent_dual_advisory.py) — **Gemini** (full bundle) and **runner GGUF** (lean bundle) run in **parallel** per lane and week.

---

## 1. Invariants (do this every time)

| Rule | Why |
|------|-----|
| **Same ISO week + same lane** | Brand files pair with `data/reports/run-next-YYYY-WW.md` and `suggestions.json` / `analytics.json`; personal with `run-next-YYYY-WW-personal.md` and `suggestions_personal.json` / `analytics_personal.json`. |
| **Trust numbers last** | Any count, %, or average in an LLM file should be **checkable** against `run-next`, weekly report, or JSON. If it disagrees, **JSON + run-next win**. |
| **Lane isolation (runner)** | Runner CONTEXT **omits** the human **cross-read** block from `run-next` (other lane). Gemini still receives the **full** `run-next` for optional cross-lane narrative. |

Outputs:

- `data/reports/agent-insight-YYYY-WW-{lane}-gemini.md`
- `data/reports/agent-insight-YYYY-WW-{lane}-runner.md`

---

## 2. What each file is

### Gemini (`*-gemini.md`)

- **Input:** **Full** bundle — weekly report, full `run-next` (including cross-read), blocked report, full-path `suggestions*.json` and `analytics*.json` excerpts (capped by `MAX_CONTEXT_GEMINI` in the script).
- **Strength:** Usually **clearer narrative**, more **structured** risks/experiments, better at naming **planner blocked** and thresholds when the API succeeds.
- **Failure modes:** **`GEMINI_API_KEY`** missing → short **stub**; **HTTP 429 / 503** → error body in the file; rate limits on free tier — see [`workflows.md`](./workflows.md) personal pacing notes.

### Runner (`*-runner.md`)

- **Input:** **Lean** bundle — scope banner, `run-next` **without** cross-lane section, short weekly + blocked reads, **compact** suggestions (incl. `coverage_summary`) and analytics (top by views + retention slice), hard char cap for small `n_ctx`.
- **Model:** Default **Qwen2.5-1.5B** GGUF on CPU (`temperature` > 0 → not byte-reproducible).
- **Strength:** **Cheap**, always runs if `llama-cpp-python` + weights present; good **quick checksum** on headline stats and “nothing actionable.”
- **Failure modes:** **Template drift** (`###` vs `##`), **repetition**, **generic** “next tries,” occasional **hallucinated** or sloppy rows — do not treat as authoritative.

---

## 3. Suggested read order (one sitting)

1. **`run-next-…md`** (same week, same lane) — deterministic summary, actionable vs exploratory, planner/blocked pointers.
2. **`run-intent-blocked*.md`** (if present) — exact gate language.
3. **Peek `suggestions*.json`** — headline stats + any row the prose cites.
4. **`*-gemini.md`** — full story and experiments (if not stub/error).
5. **`*-runner.md`** — second opinion; flag **disagreements** with Gemini or with JSON.

---

## 4. Comparison rubric (fill mentally per week)

Use the same **dimensions** for brand and personal so weeks are comparable.

| Dimension | What to check | If they disagree |
|-----------|----------------|------------------|
| **Headline totals** | Views, watch time, subs, window dates, `videos_analyzed` / with views | Prefer **weekly report** + **suggestions** JSON |
| **Planner / blocked** | “Blocked”, `n≥5`, `group_views≥200`, or intent present | Prefer **`run-next`** + **blocked** markdown |
| **Dominant mood / skew** | e.g. `art_creator` share of catalog | Prefer **JSON** + weekly table |
| **Top titles / patterns** | 5‑min “Ambient … Evolving …” etc. | Prefer **analytics** + weekly “top” lists |
| **Risks** | Thin *n*, 1-view high retention, confounders | Both LLMs should echo **`run-next`** packaging caveat; if not, note it |
| **Experiments** | Concrete vs generic bullets | Prefer **specific** ideas tied to CONTEXT; generic runner bullets are low signal |

**Heuristic:** **Agreement** (Gemini ≈ runner ≈ JSON/run-next on facts) → higher confidence in that thread. **Conflict** → re-open JSON and `run-next`; ignore LLM until resolved.

---

## 5. When to drop or change a path

- **Drop Gemini** (runner-only or skip dual step) if marginal value is low, keys/egress are painful, or **503/429** dominates — see [`COHESION_ROADMAP.md`](../COHESION_ROADMAP.md) Phase 6 *Dual advisory refinement*.
- **Invest in runner** (bundle, `temperature`/`seed`, optional larger GGUF) only when you still want **two** opinions without a second API — [`HANDOFF.md`](../HANDOFF.md) **#9**.
- **Add validators** before any automation **consumes** LLM prose — same Phase 6 iteration order.

---

## 6. Plan links

| Doc | Role |
|-----|------|
| [`START_HERE.md`](../START_HERE.md) § Plan checklist | **Dual advisory refinement** row — human compare (this playbook). |
| [`HANDOFF.md`](../HANDOFF.md) **#9** | Refinement backlog (lane CONTEXT, decoding, validators). |
| [`COHESION_ROADMAP.md`](../COHESION_ROADMAP.md) Phase 6 | Shipped prototype + iteration order + autonomy horizon. |
| [`workflows.md`](./workflows.md) | CI steps, secrets, stubs, logs (`[gemini-advisory]`, `[runner-advisory]`). |
