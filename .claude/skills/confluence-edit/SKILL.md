---
name: confluence-edit
description: Navigate to, read, and edit Confluence Cloud pages via the REST API using the user's existing browser session. Use whenever the user asks to "open", "view", "read", "find", "edit", "update", "modify", "restructure", "rewrite", "fix", "rename", "insert sections into", "delete sections from", or "publish to" a specific Confluence page or wiki page. Works on any Confluence Cloud tenant (atlassian.net, atlassian.com, custom domains) where the user is already logged in in the connected Chrome browser. Browser session only — does NOT use the Atlassian MCP connector unless the user explicitly asks (see Tooling boundary below). Does not require an API token, admin rights, or a Confluence MCP server — uses session cookies already present in the browser.
user-invocable: true
---

<!-- Repo-owned copy, vendored from the Anthropic-bundled anthropic-skills:confluence-edit, with two local guardrails added: (1) "browser session only, no Atlassian MCP", and (2) "author Confluence prose in the owner's voice" (ties the skill to wiki/_resources/voice-guide.md). Owned and version-controlled here so the guardrails persist; will not auto-update with the upstream bundle. -->


# Read, navigate, and edit Confluence Cloud pages

This skill operates on any Confluence Cloud page through the **Confluence REST API**, calling it from inside the page context with `fetch()` and the user's session cookies. It works on every Confluence Cloud tenant the user is logged in to — no per-tenant configuration, no API tokens, no MCP server.

The skill covers four workflows: **navigate**, **read**, **edit**, and **verify**. Use only the ones you need for the request.

> [!important] Tooling boundary — browser session only, no Atlassian MCP
> This skill's mechanism **is** the browser session (`fetch()` with the user's cookies via the connected Chrome MCP). That is the default and the expectation.
>
> **Do NOT reach for the Atlassian MCP connector** (`plugin:engineering:atlassian`, `mcp.atlassian.com`, or any "Atlassian"/"Confluence" MCP server) to read or edit Confluence — not even as a "faster" or "cleaner" alternative, and not when the browser path is slow, rate-limited, or hitting an output cap. Work around browser-path friction within the browser approach instead (e.g. paginate large reads in chunks, sanitise responses, navigate per page).
>
> Only use the Atlassian MCP connector if the **user explicitly asks for it in this session** (e.g. "use the Atlassian connector / MCP"). Authorising that connector requires an OAuth consent the user may be unable or unwilling to grant; defaulting to it wastes a round-trip and can dead-end. If you think the MCP would genuinely help, *ask first* rather than starting its OAuth flow.

> [!important] Voice — author Confluence prose in the owner's voice
> Whenever this skill **writes or rewrites prose** that will be published under the owner's name (a new page body, a rewritten section, a paragraph, bullet glosses, callout text), the prose follows **the owner's voice guide**, the same as any voiced output destined for the wiki. This is not optional polish; it is part of the edit.
>
> **Before drafting**, load the voice by reading **`wiki/_resources/voice-guide.md`** (the canonical guide) and deferring to it.
>
> The load-bearing rules, applied inline even without re-reading the guide:
> - **No em dashes in prose. Hard rule.** Period, colon, or comma. (Structural em dashes in tables, headings, and diagram labels are house style and stay; the storage-format entity is `&mdash;`.)
> - **Active voice, subject first.** "Unity Catalog governs source access", not "source access is governed in Unity Catalog".
> - **Plain copula** (is / are / has), and **name things then repeat the name verbatim** (no synonym cycling).
> - **Cut generated-prose tells:** "-ing" padding, copula avoidance ("serves as / boasts"), negative parallelism, pseudo-depth, piled-up hyphen-speak.
> - **Numbers and names carry the argument**; use the owner's locale number formatting where figures appear.
> - **Status tags inline** for open points: render `Confirmed` / `Tentative` / `To be validated` as a Confluence **status** macro (a yellow `To be validated` lozenge), not a parenthetical "(to confirm)".
> - **Run the voice self-check before the PUT** (stance taken; claims carry a number/name/tag; no passive; no em dash in prose; nothing that would survive copy-paste into any consultancy deck; trimmed toward the owner's register).
>
> **Scope.** This applies to prose the owner is authoring. It does **not** govern purely mechanical edits (fix one table cell, rename a heading, move a section verbatim, correct a link) or verbatim edits to someone else's page. When unsure whether a body counts as the owner's content, default to applying the voice for any **new** prose. Don't retrofit the voice onto existing third-party page text unless asked.

---

## Prerequisites — gather before doing anything

Before running any tool call, confirm or collect:

1. **Page identifier.** One of:
   - A full URL the user pasted (e.g. `https://acme.atlassian.net/wiki/spaces/ENG/pages/123456789/Page+Title`)
   - A page ID and tenant base URL
   - A page title plus a space key (you'll need to resolve it via search)
2. **Tenant base URL.** Extract from the page URL. It's the part up to `/wiki/`, e.g. `https://acme.atlassian.net/wiki`. The skill assumes Confluence **Cloud**, not Data Center / Server.
3. **Browser session.** The user must be logged in to that exact tenant in the connected Chrome browser. Check by listing connected browsers, then opening the tenant root in a tab and confirming you're authenticated (no redirect to a login page).
4. **Permission scope.** For **edits**, get explicit user confirmation before the first PUT in a session. Editing wiki content falls under "Publishing, modifying or deleting public content" — never proceed silently. Reads do not require explicit confirmation but stay within the page the user pointed to.

If any of the above is missing, **ask the user before running any tool**. Don't guess the tenant URL or page ID.

### Extracting the page ID from a URL

Page URLs have predictable shapes:

```
https://<tenant>/wiki/spaces/<SPACE>/pages/<PAGE_ID>/<URL-encoded-title>
https://<tenant>/wiki/spaces/<SPACE>/pages/<PAGE_ID>
https://<tenant>/wiki/pages/viewpage.action?pageId=<PAGE_ID>
```

In all forms, the `PAGE_ID` is a numeric string. Strip query strings and trailing slashes; the ID is the segment after `/pages/`.

### Extracting the space key

The space key is the segment immediately after `/spaces/` in the URL. The REST API doesn't strictly need the space key on every call, but `PUT` requires it. If you only have a page ID, the space key comes back in the GET response under `space.key`.

---

## Workflow 1 — Navigate to a page

When the user asks to "open" a page, or you need the page open before editing:

```javascript
// Use the navigation tool from the Chrome MCP, passing the full URL the user gave you
// or constructed from {tenant}/wiki/spaces/{SPACE}/pages/{PAGE_ID}
```

After navigation, wait a few seconds (`computer.wait` action, 3–5 seconds) before further calls — the SPA needs time to hydrate. Then confirm via `get_page_text` or a simple `document.title` JS call.

If the user pasted a URL fragment like `https://...#section-anchor`, navigate to the URL **without** the fragment — Confluence's anchor links can interfere with subsequent page-state queries.

---

## Workflow 2 — Read a page

Reads are non-destructive. They are also the **first step of every edit**: never edit without re-fetching live state.

### Read the full storage representation

This returns the page in Confluence storage format (XHTML-ish with macro tags). It's also how you get the current version number for safe editing.

```javascript
// Run in the Confluence tab via the Chrome JavaScript tool
window._cur = null;
fetch('/wiki/rest/api/content/PAGE_ID?expand=version,body.storage,space', {
  credentials: 'include'
})
  .then(r => r.json())
  .then(d => {
    window._curBody = d.body.storage.value;
    window._curVer = d.version.number;
    window._curTitle = d.title;
    window._curSpaceKey = d.space && d.space.key;
    window._cur = 'ok';
  });
'fetching';
```

After firing the fetch, wait 3–5 seconds, then read the variables you stored on `window`.

### Read rendered text (cheap, for summaries)

If you only need the visible text — for example to answer "what does this page say?" — the rendered DOM is usually easier than parsing storage format:

```javascript
document.body.innerText
```

### Get just metadata (lightweight)

```javascript
fetch('/wiki/rest/api/content/PAGE_ID?expand=version,space,history,ancestors', {
  credentials: 'include'
}).then(r => r.json()).then(d => {
  window._meta = {
    title: d.title,
    space: d.space && d.space.key,
    version: d.version.number,
    lastUpdated: d.version.when,
    createdBy: d.history && d.history.createdBy && d.history.createdBy.displayName
  };
});
```

### Search the tenant for a page

If you only have a title or topic, search via CQL (Confluence Query Language). Useful when the user asks "find the page about X" rather than giving a URL.

```javascript
// Search by title in a specific space
const cql = encodeURIComponent('type=page AND space=SPACE_KEY AND title~"keyword"');
fetch(`/wiki/rest/api/content/search?cql=${cql}&limit=10`, { credentials: 'include' })
  .then(r => r.json()).then(d => { window._results = d.results.map(p => ({id: p.id, title: p.title})); });
```

Confluence also has a UI search route the browser can navigate to: `/wiki/search?text=...`. The UI is sometimes faster for discovery; the API is better when you need exact IDs.

---

## Workflow 3 — Edit a page

This is the surgical part. The pattern is always: **re-fetch → modify → PUT → verify**.

### Step 3.1 — Re-fetch the latest state

Even if you fetched the body 30 seconds ago, fetch again. The user may have edited the page in another tab. Stale `version.number` causes the PUT to fail with a 409 conflict.

Use the read query from Workflow 2.

### Step 3.2 — Understand the structure before editing

Find section boundaries by looking for headings:

```javascript
(function () {
  const b = window._curBody;
  const idx = {};
  // Pass in the headings you expect; record their byte positions
  ['Section A', 'Section B', 'Conclusion'].forEach(s => { idx[s] = b.indexOf(s); });
  return idx;
})()
```

To inspect the **markup shape** without triggering content filters in the browser tool, strip text and keep tags:

```javascript
const skel = sample.replace(/>[^<]+</g, m => {
  const inner = m.slice(1, -1);
  return inner.length <= 15 ? '>' + inner + '<' : '>«' + inner.length + 'chars»<';
});
```

For table rows specifically:

```javascript
const rows = [...section.matchAll(/<tr[^>]*>[\s\S]*?<\/tr>/g)];
```

Note `<tr[^>]*>` — Confluence storage format adds `ac:local-id="..."` attributes to most tags, so a naive `<tr>` won't match.

### Step 3.3 — Construct the new body

Two strategies, pick by edit size:

**Strategy A — Surgical string replacement.** For small, targeted changes (renaming a heading, replacing one table cell, inserting one section). Best when you can find a **unique substring** as anchor.

```javascript
let body = window._curBody;
body = body.replace('Old phrase', 'New phrase');
body = body.replace(
  '<h2 local-id="abc">Existing section</h2>',
  '<h2>New section</h2><p>Content</p><h2 local-id="abc">Existing section</h2>'
);
window._newBody = body;
```

Caveats: `String.replace(str, str)` replaces **only the first occurrence**. Use a regex with `g` flag if you need all, or be more specific.

**Strategy B — Splice by byte ranges.** For rebuilding whole sections.

```javascript
const b = window._curBody;
const sectionStart = b.indexOf('<h2>Old section</h2>');
const sectionEnd = b.indexOf('<h2>', sectionStart + 1);
const newBody = b.substring(0, sectionStart) + newSection + b.substring(sectionEnd);
```

When inserting/removing by offset, do edits **from highest position to lowest** so earlier positions stay stable. Or use string-based replacements throughout.

### Step 3.4 — PUT the new body

```javascript
window._putRes = 'pending';
const payload = {
  id: 'PAGE_ID',
  type: 'page',
  title: window._curTitle, // exact existing title
  space: { key: window._curSpaceKey },
  version: { number: window._curVer + 1 }
  // intentionally NO version.message
  ,
  body: { storage: { value: window._newBody, representation: 'storage' } }
};
fetch('/wiki/rest/api/content/PAGE_ID', {
  method: 'PUT',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
    'X-Atlassian-Token': 'no-check',
    'Accept': 'application/json'
  },
  body: JSON.stringify(payload)
}).then(r => r.text().then(t => {
  window._putRes = { status: r.status, ok: r.ok, snippet: t.slice(0, 200) };
})).catch(e => { window._putRes = 'error: ' + e.message; });
'started';
```

Wait 6–8 seconds, then read `window._putRes`. A successful PUT returns `{status: 200, ok: true, snippet: "{\"id\":...}"}`.

**Critical rules:**

- **Do not set `version.message`** unless the user explicitly asks for a version comment. When the user owns the page session, a version comment attributed to anyone else reads as misattributed.
- The `title` must match the current title exactly or the PUT fails.
- The `version.number` must equal current + 1. On 409 conflict, re-fetch and retry.
- Always pass `space.key` from the fresh GET; don't hard-code.

### Step 3.5 — Verify

The browser JS tool's response window is short. A PUT that returns 200 server-side may appear to "time out" from the tool's perspective. **Always verify** by re-fetching the version:

```javascript
window._verCheck = null;
fetch('/wiki/rest/api/content/PAGE_ID?expand=version', { credentials: 'include' })
  .then(r => r.json())
  .then(d => { window._verCheck = { ver: d.version.number, when: d.version.when }; });
'started';
```

Wait 3 seconds. If `ver` is greater than what you started with, the PUT committed.

For content verification:

```javascript
// After page reload, check rendered text for expected content
const t = document.body.innerText;
({ hasNewSection: t.includes('New section title'), oldRemoved: !t.includes('Removed phrase') });
```

---

## Storage format basics

Confluence storage format is XHTML + custom macro syntax. The standard subset you'll use most:

| What | Storage format |
|---|---|
| Heading | `<h1>` `<h2>` `<h3>` |
| Paragraph | `<p>...</p>` |
| Bold | `<strong>...</strong>` |
| Italic | `<em>...</em>` |
| Inline code | `<code>...</code>` |
| Bullet list | `<ul><li>...</li></ul>` |
| Numbered list | `<ol><li>...</li></ol>` |
| Table | `<table><tbody><tr><th>...</th></tr><tr><td>...</td></tr></tbody></table>` |
| External link | `<a href="https://...">label</a>` |
| Link to another Confluence page | `<ac:link><ri:page ri:content-title="Exact Title" /></ac:link>` |
| Em dash | `&mdash;` |
| En dash | `&ndash;` |
| Curly quotes | `&ldquo;` `&rdquo;` `&lsquo;` `&rsquo;` |
| Right arrow | `&rarr;` |
| Ampersand (literal) | `&amp;` |
| Less / greater than | `&lt;` `&gt;` |

Common macros:

| Macro | Tag |
|---|---|
| Table of Contents | `<ac:structured-macro ac:name="toc">` |
| Status badge / lozenge | `<ac:structured-macro ac:name="status">` |
| Info / Note / Warning panel | `<ac:structured-macro ac:name="info" / "note" / "warning">` |
| Code block | `<ac:structured-macro ac:name="code">` |
| Page Properties (key-value metadata block) | `<ac:structured-macro ac:name="details">` |
| Page Properties Report (rollup table) | `<ac:structured-macro ac:name="detailsreport">` |
| Expand / collapsible | `<ac:structured-macro ac:name="expand">` |
| Children display | `<ac:structured-macro ac:name="children">` |
| User mention | `<ac:link><ri:user ri:account-id="..."/></ac:link>` |

When you PUT simple `<tr><td><p>` markup, Confluence adds `ac:local-id="..."` attributes on save. You don't need to generate them.

---

## Preserving a metadata block ("don't change these fields")

Many ADR / SDR / decision-record templates start with a Page Properties macro (named `details` in storage format) holding the immutable fields — owner, contributors, due date, related decisions, etc. When the user says "don't change contributors / due date / previous decisions", preserve that macro intact.

Approach:

1. Find the first `<h2>` heading position — that's where the body content typically begins.
2. Treat everything before it as an immutable **prefix**: copy verbatim.
3. Build your new body as `prefix + newContent`.
4. Do **not** rebuild the metadata macro by hand — you risk losing the status macro, embedded TOC, ID attributes, and downstream cross-links.

```javascript
const h2Start = window._curBody.search(/<h2[^>]*>/);
const prefix = window._curBody.substring(0, h2Start);
window._newBody = prefix + newBodyContent;
```

---

## Common pitfalls (learned the hard way)

**The browser tool's output filter blocks cookie-like content.** When you return long body slices, the response may come back as `[BLOCKED: Cookie/query string data]`. Work around it by:

- Returning lengths, counts, and positions rather than raw text spans.
- Stripping tags to produce a structural skeleton.
- Inspecting per-character with `charCodeAt` for short, targeted spans.

**Storage format has surprise attributes.** A heading you wrote as `<h2>Title</h2>` may come back as `<h2 local-id="abc123">Title</h2>` after a save. Don't rely on exact-match for the wrapping tags — use partial anchors like `>Title</h2>` or use regex.

**Tags wrap things in unexpected places.** A textual em dash between two phrases may live outside a `</em>` or `</strong>` close. Probe the actual byte sequence before crafting a replacement:

```javascript
const slice = body.substring(targetPos, targetPos + 80);
let s = '';
for (const ch of slice) {
  const code = ch.charCodeAt(0);
  if (code < 32 || code > 126) s += '\\u' + code.toString(16).padStart(4, '0');
  else s += ch;
}
return s;
```

**`replace()` replaces only the first occurrence.** Use regex with `g` flag, or be more specific with surrounding context, or verify after every edit.

**Position offsets shift mid-edit.** When inserting/removing by offset, do edits from highest position to lowest, or use string-based replacements throughout.

**Fetches "time out" but succeed.** The browser JS tool may report no response within its window even when the server-side write returned 200. Always verify with a follow-up GET on `?expand=version` — don't trust the immediate response.

**The user may have edited between fetches.** Every edit cycle: re-fetch, modify, PUT. Never reuse `_curBody` from a previous turn.

**Confluence Cloud vs. Data Center / Server.** This skill is for Cloud. The REST API path on Cloud is `/wiki/rest/api/content/...`. On Data Center it's typically `/rest/api/content/...` (no `/wiki` prefix) and authentication is different. Detect Cloud by checking the URL pattern: `*.atlassian.net/wiki/...`.

---

## Anti-patterns

- **Editing via simulated keyboard/mouse in the rich-text editor.** Fragile: panels, embedded images, custom layouts. Always prefer the REST API.
- **Setting a version message that names a third party.** If the user owns the page session, the message looks misattributed. Default to no message.
- **Using cached `_curBody` across user turns.** State drifts. Re-fetch every time.
- **PUT without verifying.** Tool timeouts can mask successful or failed writes.
- **Hard-coding tenant, space key, or title.** Pull them from the fresh GET.

---

## Quick checklist before every PUT

- [ ] Re-fetched current `version.number` and `body.storage.value` in this turn.
- [ ] New body builds on the freshly fetched body, not a cached copy.
- [ ] `version.number` = current + 1.
- [ ] No `version.message` (unless user explicitly asked).
- [ ] `title` exactly matches current.
- [ ] `space.key` pulled from the fresh GET.
- [ ] Storage format is well-formed (open tags closed, entities encoded).
- [ ] If preserving metadata, the Page Properties prefix is untouched.
- [ ] Headers include `Content-Type: application/json` and `X-Atlassian-Token: no-check`.
- [ ] If the body contains prose the owner authored, it passed the voice self-check (no em dash in prose, active voice, status lozenges for open points) — see the Voice guardrail above.
- [ ] User has confirmed the edit in chat (for the first PUT in this session).

---

## Reporting back to the user

After a successful edit:

- Confirm the new version number.
- Summarise what changed (sections added/removed/renamed, key replacements).
- Provide the page link so the user can review.
- Do **not** narrate every API call. The user wants the result, not the play-by-play.

After a read or navigation:

- Answer the user's actual question. The act of fetching is plumbing, not the deliverable.

---

## End-to-end example (read → edit → verify)

```javascript
// Inputs collected from the user:
const PAGE_ID = '123456789';
const PAGE_URL = 'https://acme.atlassian.net/wiki/spaces/ENG/pages/123456789/Title';

// Step 1 — Navigate (if the page isn't already open)
// Use Chrome MCP navigate to PAGE_URL, then wait 4-5s

// Step 2 — GET
window._cur = null;
fetch('/wiki/rest/api/content/' + PAGE_ID + '?expand=version,body.storage,space', { credentials: 'include' })
  .then(r => r.json()).then(d => {
    window._curBody = d.body.storage.value;
    window._curVer = d.version.number;
    window._curTitle = d.title;
    window._curSpaceKey = d.space.key;
    window._cur = 'ok';
  });
'fetching';

// [wait 4 seconds]

// Step 3 — Verify GET
({ ver: window._curVer, len: window._curBody && window._curBody.length, title: window._curTitle });

// Step 4 — Modify
let body = window._curBody;
body = body.replace('Old phrase', 'New phrase');
window._newBody = body;

// Step 5 — PUT
window._putRes = 'pending';
const payload = {
  id: PAGE_ID, type: 'page', title: window._curTitle,
  space: { key: window._curSpaceKey },
  version: { number: window._curVer + 1 },
  body: { storage: { value: window._newBody, representation: 'storage' } }
};
fetch('/wiki/rest/api/content/' + PAGE_ID, {
  method: 'PUT', credentials: 'include',
  headers: { 'Content-Type': 'application/json', 'X-Atlassian-Token': 'no-check', 'Accept': 'application/json' },
  body: JSON.stringify(payload)
}).then(r => r.text().then(t => { window._putRes = { status: r.status, ok: r.ok }; }))
  .catch(e => { window._putRes = 'error: ' + e.message; });
'started';

// [wait 6-8 seconds]

// Step 6 — Verify version increment
window._verCheck = null;
fetch('/wiki/rest/api/content/' + PAGE_ID + '?expand=version', { credentials: 'include' })
  .then(r => r.json()).then(d => { window._verCheck = d.version.number; });
'started_verify';

// [wait 3 seconds, then read window._verCheck — should be old version + 1]
```
