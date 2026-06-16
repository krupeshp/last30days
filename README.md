# Last 30 Days

A Claude Code skill that researches **what people actually said about any topic in
the last 30 days** — across Reddit, Hacker News, GitHub, X, YouTube, arXiv, and
news — then ranks by recency + engagement and writes a cited briefing.

Everything runs inside Claude using built-in `WebSearch` / `WebFetch`. **No API
keys required.**

## Install

Add this repo as a plugin marketplace, then install the plugin:

```
/plugin marketplace add kar2gan/last30days
/plugin install last30days@last30days
```

(Replace `kar2gan/last30days` with the actual repo if you fork it.)

## Use

```
/last30days nvidia earnings reaction
/last30days AI agent frameworks --days 7
/last30days rust async runtimes, only reddit and hackernews
```

The skill:

1. Computes the exact date window and builds per-source search queries.
2. Fans out `WebSearch` across all sources in parallel.
3. `WebFetch`es the strongest hits for real content.
4. Dedupes, ranks by recency + engagement, clusters into themes.
5. Writes a cited markdown briefing.

## Structure

```
.claude-plugin/
  plugin.json          # plugin manifest
  marketplace.json     # marketplace manifest (makes it installable)
skills/last30days/
  SKILL.md             # the skill definition + workflow
  scripts/window.py    # computes date window + per-source queries (stdlib only)
```

## Roadmap

- [ ] Dedicated scrapers per source (richer engagement metrics than web search)
- [ ] Optional API-key providers for higher-fidelity data
- [ ] Watchlists / scheduled recurring briefings
- [ ] HTML briefing export

## License

MIT
