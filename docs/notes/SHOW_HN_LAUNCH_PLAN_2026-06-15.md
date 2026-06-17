# Show HN Launch Plan

## Page

Entry point:

```text
site/index.html
```

Core sentence:

> AlphaGo did not create the largest structural shift in recorded Go. It accelerated how fast Go learns.

## Candidate Titles

Preferred:

```text
Show HN: How AI changed Go, measured across 400 years of recorded games
```

Shorter:

```text
Show HN: I measured how AlphaGo changed Go across recorded game history
```

## First Comment Draft

```text
Hi HN, I built this interactive analysis to understand how AlphaGo changed professional Go.

The surprising result is that the AI-era shift is not the largest structural shift in the recorded CWI history. What changes more clearly is the speed at which patterns are discovered, reused, and stabilized.

The page shows:
- a small SHP move-structure lens: chroma x rhythm
- Lee Sedol 2016 and Ke Jie 2017 as two different AI-alignment traces
- AI-era drift inside the historical envelope
- opening-pattern adoption accelerating after AI
- regional event streams converging, separating, then converging again

This is not a claim that AlphaGo did not matter. It mattered by changing the circulation speed of Go knowledge, not simply by moving Go to an unprecedented style point.

Code, manuscript draft, and reproduction notes are linked from the page.
```

## Pre-Launch Checklist

- Page opens without build tooling.
- Mobile viewport has no horizontal overflow.
- First screen shows the claim, scale, and core numbers.
- "What this is not" section is visible before external links.
- Repo README links to `site/index.html`.
- Raw CWI data and KataGo weights are not required for the page.

## Likely HN Questions

- Is CWI representative of all professional Go?
- Are regional labels national claims?
- Why use KataGo traces if the main claim is historical drift?
- How are opening patterns defined?
- Does "inside historical envelope" mean AI had no effect?
- Can I reproduce this without downloading the full dataset?

## Short Answers

- CWI is treated as a sedimented archive, not a complete census.
- Regional labels mean event streams in the database.
- KataGo is an alignment reference; the main drift and adoption claims use recorded games.
- Patterns are recurrent opening prefixes with fixed-horizon adoption checks.
- AI has a strong effect on circulation speed; it is not the largest measured drift.
- The static page uses precomputed aggregates; full reproduction requires the source tables.
