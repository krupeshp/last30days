#!/usr/bin/env python3
"""Compute the research time window and emit per-source search queries.

Pure stdlib, no network. The skill calls this to (a) get exact date bounds for
the "last N days" window and (b) get a ready-made set of source-scoped search
queries to fan out with WebSearch.

Usage:
    python3 window.py "nvidia earnings reaction" [--days 30]
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone

# Source -> query template. {q} is the user's topic, {after} is an ISO date.
# Templates use site: scoping and date hints so WebSearch favors fresh, on-source results.
SOURCE_TEMPLATES = {
    "reddit": '{q} site:reddit.com',
    "hackernews": '{q} site:news.ycombinator.com',
    "github": '{q} site:github.com (released OR launch OR "v" OR changelog)',
    "x": '{q} (site:x.com OR site:twitter.com OR site:nitter.net)',
    "youtube": '{q} site:youtube.com',
    "arxiv": '{q} site:arxiv.org',
    "news": '{q} news after:{after}',
    "web": '{q} (announcement OR release OR update) after:{after}',
}


def build(topic: str, days: int, sources: list[str]) -> dict:
    now = datetime.now(timezone.utc)
    after = (now - timedelta(days=days)).date().isoformat()
    queries = []
    for s in sources:
        tmpl = SOURCE_TEMPLATES.get(s)
        if not tmpl:
            continue
        queries.append({"source": s, "query": tmpl.format(q=topic, after=after)})
    return {
        "topic": topic,
        "window_days": days,
        "after": after,
        "before": now.date().isoformat(),
        "generated_at": now.isoformat(),
        "queries": queries,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("topic", help="the subject to research")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument(
        "--sources",
        default=",".join(SOURCE_TEMPLATES),
        help="comma-separated subset of: " + ",".join(SOURCE_TEMPLATES),
    )
    args = ap.parse_args()
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    print(json.dumps(build(args.topic, args.days, sources), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
