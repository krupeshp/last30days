---
name: last30days-tech
version: "0.1.0"
description: "Tech & AI intelligence for the last 30 days. A tech-tuned layer over the last30days engine: pulls model/product releases, papers, repos, frameworks, benchmarks, and community reaction from curated AI/dev communities (r/MachineLearning, r/LocalLLaMA, Hacker News, GitHub, Bluesky, the web), then writes a synthesized tech briefing. Use for 'what's new in AI', 'latest in <tech/framework/model>', 'monthly AI recap', 'recent releases in <area>'."
argument-hint: "last30days-tech AI agent frameworks | last30days-tech local LLMs | last30days-tech vector databases | last30days-tech what shipped in RAG"
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, AskUserQuestion
homepage: https://github.com/krupeshp/last30days
repository: https://github.com/krupeshp/last30days
author: krupeshp
license: MIT
user-invocable: true
---

# Last 30 Days — Tech

Produce a synthesized **tech/AI intelligence briefing** for the last N days (default 30)
on any technology topic. This is a focused layer on top of the proven `last30days`
**engine** (a sibling skill in this plugin) with tech-tuned source defaults and a
tech-shaped output. You do not reimplement retrieval — you run the engine, then
synthesize.

## Inputs

- **Topic** — the tech/AI subject (from the argument). If missing, ask once.
- **Window** — default 30 days; honor "last 7 days", "this quarter", etc.
- **Sources** — defaults come from `config/tech_sources.json`; honor overrides like
  "only HN and GitHub" or "include Reddit only".

## Step 1 — Resolve the engine and interpreter

The retrieval engine lives in the **sibling** `last30days` skill, not in this folder.

```bash
# SKILL_DIR = absolute path of the directory containing THIS SKILL.md you just Read.
SKILL_DIR="<absolute path of the directory containing the SKILL.md you Read>"
ENGINE="$SKILL_DIR/../last30days/scripts/last30days.py"
TECH_CONFIG="$SKILL_DIR/config/tech_sources.json"

if [ ! -f "$ENGINE" ]; then
  echo "ERROR: engine not found at $ENGINE (expected sibling last30days skill)." >&2
  exit 1
fi

# Python 3.12+ is required by the engine.
for py in python3.14 python3.13 python3.12 python3; do
  if command -v "$py" >/dev/null 2>&1 && "$py" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3,12) else 1)'; then
    LAST30DAYS_PYTHON="$py"; break
  fi
done
[ -z "$LAST30DAYS_PYTHON" ] && { echo "ERROR: needs Python 3.12+." >&2; exit 1; }
```

## Step 2 — Load the curated tech defaults

Read `config/tech_sources.json`. Use:

- `default_search` → the `--search` source list (e.g. `reddit,hackernews,github,bluesky,web`).
- `subreddits` → the `--subreddits` value (curated AI/dev communities). Trim to the
  ones most relevant to the topic when the topic is narrow (e.g. for "local LLMs",
  lead with `LocalLLaMA,MachineLearning`).
- `focus_themes` → the section structure for your final briefing.

Users can edit this file to tune the skill — always read it fresh, don't hardcode.

## Step 3 — Run the engine (tech-tuned)

```bash
"$LAST30DAYS_PYTHON" "$ENGINE" "{TOPIC}" \
  --emit=compact \
  --days 30 \
  --search reddit,hackernews,github,bluesky,web \
  --subreddits {CURATED_SUBS_FROM_CONFIG}
```

- Swap `--days` to match the requested window.
- For a **named entity** (a specific product, model, person, or project — e.g. "Claude Code",
  "vLLM", "LangGraph"), follow the engine's plan requirement: generate a `--plan` JSON
  per the main `last30days` SKILL.md Step 0.75 and pass `--plan "$QUERY_PLAN_FILE"`.
  For broad area topics ("RAG", "AI agents") the bare command above is fine.
- Pass the engine's output through your reading — the block between
  `<!-- EVIDENCE FOR SYNTHESIS -->` markers is raw evidence **for you**, not for the user.

## Step 4 — Enrich gaps with WebSearch/WebFetch

The engine covers Reddit/HN/GitHub/Bluesky/web. For tech, also fill two gaps it doesn't
natively scrape:

- **Papers** — run a `WebSearch` for `{TOPIC} site:arxiv.org` (and `site:huggingface.co/papers`)
  within the window; `WebFetch` the 2–3 strongest to pull the TL;DR and key results.
- **Model/dataset drops** — `WebSearch` `{TOPIC} site:huggingface.co` for new model/dataset releases.

Only add what the searches actually return. Don't invent papers, models, or numbers.

## Step 5 — Write the tech briefing

Synthesize the engine evidence + enrichment into **prose**, organized by the
`focus_themes` from config (drop themes with no material):

- **Header** — topic + window (e.g. *"Last 30 days in AI agent frameworks — May 17 → Jun 16, 2026"*) and a one-line "what mattered most".
- **Model & product releases** — what shipped, with version/date and a source link.
- **Research & papers** — notable papers/results, each linked, one-line takeaway.
- **Frameworks, libraries & tooling** — new/updated repos, with the month's star/PR signal where available.
- **Benchmarks & evals** — any new numbers or comparisons.
- **Community reaction & debate** — what r/LocalLLaMA, HN, Bluesky actually said; sentiment.
- **Signals** — 2–3 sentences on direction/momentum.

### Rules

- **Only report what the engine + searches returned.** Never fabricate releases, papers,
  versions, stars, or sentiment. If a theme came back empty, omit it (don't pad).
- Every claim links to a real URL. Synthesize into readable prose — do **not** dump the
  engine's raw `### N. (score …)` evidence clusters into the output.
- Engagement/recency ranking is for ordering, not an authoritative metric.
- Preserve the engine's footer/badge behavior if present in its stdout.

## Examples

- `last30days-tech AI agent frameworks`
- `last30days-tech local LLM inference --days 14`
- `last30days-tech what shipped in vector databases`
- `last30days-tech Claude Code` (named entity → generate a `--plan` first)
