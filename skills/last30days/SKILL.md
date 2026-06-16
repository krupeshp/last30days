---
name: last30days
version: "0.1.0"
description: "Research what people actually said about any topic in the last 30 days. Fans out web searches across Reddit, Hacker News, GitHub, X, YouTube, arXiv, and news, ranks by recency and engagement, and writes a cited briefing. Use for 'last 30 days', 'what's new with X', 'recent reaction to X', monthly recaps."
argument-hint: "last30days nvidia earnings reaction | last30days AI agent frameworks | last30days react server components"
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, AskUserQuestion
homepage: https://github.com/krupeshp/last30days
repository: https://github.com/krupeshp/last30days
author: krupeshp
license: MIT
user-invocable: true
---

# Last 30 Days

Produce a fresh, multi-source briefing on **what happened with a topic in the
last N days** (default 30). Everything runs inside Claude using `WebSearch` and
`WebFetch` — no API keys required.

## Inputs

- **Topic** — the subject to research (from the user's argument). If missing, ask once.
- **Window** — default 30 days. Honor "last 7 days", "this week", "past quarter", etc.
- **Sources** — default all. Honor "only reddit and HN", "skip twitter", etc.

## Steps

### 1. Build the window + queries

Run the helper to get exact date bounds and per-source search queries:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}/skills/last30days/scripts/window.py" "<TOPIC>" --days 30
```

(Override `--days` and `--sources reddit,hackernews,github,...` to match the request.)
It prints JSON with `after`/`before` dates and a `queries` list (one per source).

### 2. Fan out the searches

For **each** query in the JSON, call `WebSearch`. Run them in parallel (multiple
tool calls in one turn). Sources covered: Reddit, Hacker News, GitHub, X/Twitter,
YouTube, arXiv, general news, and broad web.

Discard anything clearly older than the `after` date — recency is the whole point.
Prefer results that expose a date and an engagement signal (upvotes, comments,
stars, views, points).

### 3. Fetch the strongest hits

Pick the ~10–15 most promising URLs across sources and `WebFetch` each to pull the
real content (title, date, key claims, numbers, sentiment). Skip paywalls and
dead links rather than guessing their contents.

### 4. Dedupe, rank, cluster

- **Dedupe** the same story reported in multiple places — keep the best source.
- **Rank** by a blend of recency and engagement (newer + higher engagement = higher).
- **Cluster** into 3–6 themes when natural (e.g. "Launches", "Reactions",
  "Controversy", "Benchmarks").

### 5. Write the briefing

Output markdown:

- **Header** — topic + window (e.g. *"Last 30 days: AI agent frameworks — May 17 → Jun 16, 2026"*) and a one-line takeaway.
- **What mattered** — 8–15 bullets, each a markdown link to the source, tagged
  with the source (`[Reddit]`, `[HN]`, `[GitHub]`…), a one-line summary, and the
  key signal (e.g. *312 upvotes*, *1.2k stars this month*). Group under theme
  headings when clusters exist.
- **By source** — a short roundup per source so nothing important is buried.
- **Signals & sentiment** — 2–3 sentences on the overall mood / direction.

### Rules

- **Only report what the searches and fetches actually returned.** Never invent
  posts, numbers, dates, or sentiment. If a source came back empty, say so.
- Every claim links to a real URL. Trim long summaries to one readable line.
- Engagement-based ranking is for ordering, not an exact metric — don't present
  it as authoritative.

## Examples

- `last30days nvidia earnings reaction`
- `last30days AI video tools --days 7`
- `last30days rust async runtimes, only reddit and hackernews`
