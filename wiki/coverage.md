---
title: Domain coverage — materialised scan across the EA-discipline domains
type: reference
created: 2026-06-05
updated: 2026-06-05
tags: [coverage, lint-output, materialised]
---

Materialised output of `lint`'s domain-coverage scan. Rebuilt each lint pass; do not edit by hand. See [[domains]] for the canonical taxonomy and per-domain scope.

`coverage.base` is the live companion to this page: it gives filterable, per-page exploration across the domains (one view per domain, plus cross-domain-bridge and stale-page views), whereas this `.md` holds the synthesised cross-domain metrics. The `.base` is owned and re-serialised by Obsidian's Bases plugin — edit its views in Obsidian, not by hand.

> [!note] Empty on a fresh foundation
> No content has been ingested yet, so there is nothing to scan. The first `lint` after pages land will populate the matrix below. The thresholds are defaults from [[CLAUDE]] and should be re-tuned once the corpus is large enough to show a real distribution.

**Scan run:** _(not yet run)_

---

## Thresholds (canonical, per [[CLAUDE]])

Contributing pages = unique pages across `concepts/`, `sources/`, `frameworks/`, `analyses/`, `cases/`, `artifacts/` carrying the `#domain:<name>` tag.

| Bucket | Range | Meaning |
|---|---|---|
| **thin** | < 25 | Concept cluster still forming. Flag as a focus area for next ingest or query. |
| **balanced** | 25–49 | Coverage adequate for the domain's core questions to be answerable. |
| **dense** | 50–69 | Cluster ripe for synthesis — consider whether an `analyses/` page is overdue. |
| **over-saturated** | 70+ | Risk of duplicate / orphan / drifted concept pages; lint integrity pass should target these first. |

Re-tune the thresholds once the corpus shows a stable distribution (look at the quartile shape of pages-per-domain).

---

## Coverage matrix

| # | Domain | Pages | Δ | Bucket | 2D Status | Analyses |
|---|---|---|---|---|---|---|
| 1 | `strategy` | 0 | — | **thin** | starved | _(none yet)_ |
| 2 | `enterprise-architecture` | 0 | — | **thin** | starved | _(none yet)_ |
| 3 | `business-architecture` | 0 | — | **thin** | starved | _(none yet)_ |
| 4 | `business-to-it` | 0 | — | **thin** | starved | _(none yet)_ |
| 5 | `software-architecture` | 0 | — | **thin** | starved | _(none yet)_ |
| 6 | `solution-delivery` | 0 | — | **thin** | starved | _(none yet)_ |
| 7 | `data` | 0 | — | **thin** | starved | _(none yet)_ |
| 8 | `tech-infra-cloud` | 0 | — | **thin** | starved | _(none yet)_ |
| 9 | `exponential-tech-innovation` | 0 | — | **thin** | starved | _(none yet)_ |
| 10 | `security` | 0 | — | **thin** | starved | _(none yet)_ |
| 11 | `governance` | 0 | — | **thin** | starved | _(none yet)_ |
| 12 | `organizational-change` | 0 | — | **thin** | starved | _(none yet)_ |

---

## Related

- [[domains]]: canonical taxonomy and per-domain scope
- [[CLAUDE]]: operating manual; the authoritative spec
