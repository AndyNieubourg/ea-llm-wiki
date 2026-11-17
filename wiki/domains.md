---
title: EA-discipline domains — coverage taxonomy
type: reference
created: 2026-06-05
updated: 2026-11-17
tags: [taxonomy, domains]
---

Canonical list of `#domain:<name>` tags used across the wiki. The taxonomy is anchored in the **disciplines of the enterprise-architecture craft** — each domain is a coherent area of practice an EA works across. It is owner-tunable: the `/init-wiki` interview confirms, prunes, or extends this default set to match how the owner actually divides their work. Whatever set this file declares is the set the `lint` coverage scan reads.

The taxonomy serves two jobs:
1. Day-to-day tagging of pages so the `lint` domain-coverage scan can show, per domain, how much wiki material exists and where the gaps are.
2. Anchoring `wiki/questions/domain-<name>.md` pages — the open-question records per domain, used to drive rumination and surface starved areas.

A page can carry multiple `#domain:` tags when its content legitimately contributes to several (common case: AI governance spanning [[#data]] + [[#security]] + [[#governance]] + [[#exponential-tech-innovation]]).

---

## The default 12 domains

| # | Tag | Scope |
|---|---|---|
| 1 | `#domain:strategy` | Strategy frames, schools, evaluation; capturing, challenging, and making explicit an organisation's strategic plan; linking strategy to architecture; the strategy-execution gap. |
| 2 | `#domain:enterprise-architecture` | The EA discipline itself: definitions, schools of thought, EA frameworks (TOGAF / Zachman / EDGY / DYA / etc.), the architect role, EA operating models, modelling languages, architecting in practice, building a comprehensive EA portfolio. |
| 3 | `#domain:business-architecture` | Business capabilities, value streams, capability viewpoints & heatmaps, organisation design, operating models, motivation modelling, the bridge from strategy to solution. |
| 4 | `#domain:business-to-it` | Business → IT translation. Business process modelling (BPMN), requirements engineering, functional analysis, application landscape, integration patterns, ATAM. Where business intent becomes IT-implementable specification. |
| 5 | `#domain:software-architecture` | Software design patterns, integration craft, solution architecture work, loosely-coupled design, bounded contexts, domain-driven design. |
| 6 | `#domain:solution-delivery` | Solution and project delivery; estimation; delivery practices; team topologies; getting solutions actually shipped. |
| 7 | `#domain:data` | Data architecture, data management (DAMA/DMBOK spine), governance, quality, lineage, data products, data mesh / lakehouse / fabric, AI-readiness, information management, data strategy. |
| 8 | `#domain:tech-infra-cloud` | Compute, network, **cloud**, platform engineering, internal developer platforms, technology architecture. |
| 9 | `#domain:exponential-tech-innovation` | AI/ML, agentic systems, novel-tech assessment frameworks, and innovation management. Hype-cycle thinking, technology trade-offs, the EA's role in evaluating emerging tech. |
| 10 | `#domain:security` | Threat modelling, zero trust, privacy/security by design, DevSecOps, intelligent continuous security, AI security, secure supply chain. |
| 11 | `#domain:governance` | Enterprise governance of IT, COBIT / EGIT, governance bodies & structures, benefits realisation, risk + resource optimisation, business cases, ESG, legal/compliance impact on EA. |
| 12 | `#domain:organizational-change` | Organisational behaviour, change management, transformation leadership, culture, team topologies, the human/social dimension of EA. |

> [!note] Tune at init
> These twelve are a sensible default for a generalist enterprise architect. During `/init-wiki`, narrow or widen the set to the owner's practice — a data-and-AI specialist might collapse `software-architecture` and `solution-delivery`, while a security-focused architect might split `security` into application vs. infrastructure. Add a domain only when it represents a genuinely distinct area of the owner's work; an over-fine taxonomy makes the coverage scan noisy.

---

## Per-domain detail

For each domain: linked question page, analyses (if any), and key frameworks/concepts already in the wiki. Surfaces orphan domains. Built from current wiki state, refreshed by `lint`'s domain-coverage scan.

> _Empty on a fresh foundation. The first `lint` after content lands populates this section and rebuilds [[coverage]]._

### 1. `#domain:strategy`
- Question: _(none yet; expected at `questions/domain-strategy.md`)_
- Analyses: _(none yet)_
- Frameworks / Concepts / Sources: _(none yet)_

### 2. `#domain:enterprise-architecture`
- Question: _(none yet; expected at `questions/domain-enterprise-architecture.md`)_

### 3. `#domain:business-architecture`
- Question: _(none yet; expected at `questions/domain-business-architecture.md`)_

### 4. `#domain:business-to-it`
- Question: _(none yet; expected at `questions/domain-business-to-it.md`)_

### 5. `#domain:software-architecture`
- Question: _(none yet; expected at `questions/domain-software-architecture.md`)_

### 6. `#domain:solution-delivery`
- Question: _(none yet; expected at `questions/domain-solution-delivery.md`)_

### 7. `#domain:data`
- Question: _(none yet; expected at `questions/domain-data.md`)_

### 8. `#domain:tech-infra-cloud`
- Question: _(none yet; expected at `questions/domain-tech-infra-cloud.md`)_

### 9. `#domain:exponential-tech-innovation`
- Question: _(none yet; expected at `questions/domain-exponential-tech-innovation.md`)_

### 10. `#domain:security`
- Question: _(none yet; expected at `questions/domain-security.md`)_

### 11. `#domain:governance`
- Question: _(none yet; expected at `questions/domain-governance.md`)_

### 12. `#domain:organizational-change`
- Question: _(none yet; expected at `questions/domain-organizational-change.md`)_

---

## Related

- `CLAUDE.md` (repo root, outside the vault): operating manual; the authoritative spec
- [[coverage]]: materialised coverage matrix across these domains
- [[index]]: wiki catalog
