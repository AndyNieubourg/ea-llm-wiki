# Provenance Ledger — <target-name>

Audited: <YYYY-MM-DD> · Corpus: <raw/ scope> + <KB scope> + <in-session: N documents, M assertions>
Spans: <N> · Grounded <g> · Partial <p> · Ungrounded <u> (<breakdown by class>) · Contradicted <c>
Grounded share of factual spans: <g+…>/<factual N> = <pct>%. Open proposals awaiting the owner: <k>. <"No covert invented claims." once k = 0>

## Span table

| id | excerpt | class | grounding | conf. | sources | s-trust | x-check | proposal | resolution |
|----|---------|-------|-----------|-------|---------|---------|---------|----------|------------|
| S01 | "<load-bearing 8-15 words>" | <class> | <status> | <conf> | <locators or —> | <trusted/mixed/weak/unverified> | <confirmed/silent/contradicts or —> | <none/rewrite/hedge/reclassify/cut/flag-conflict> | <none/accepted/edited/rejected> |

<!-- one row per span -->

## Challenge-and-iterate log

> **<id>** — current text: *"<span>"*. Classed `<class>` / `<grounding>`: <why weak>. Searched <where> with <terms>. <found / not found>. **Proposed:** <rewrite | hedge | reclassify | cut | flag> → *"<candidate wording>"*, <confidence or badge change>. <Awaiting the owner | resolved: accepted/edited/rejected>.

<!-- one block per span the loop touched -->

## Reverse traceability — corpus coverage

| source | used by spans | status |
|--------|---------------|--------|
| <locator or [[page]]> | S03, S05 | used |
| <locator> | — | **unused — gap or over-claim?** |
