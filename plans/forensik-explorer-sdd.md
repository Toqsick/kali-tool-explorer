# Forensik Tool-Explorer — SDD Implementation Plan

> **For agentic workers:** Use `subagent-driven-development` skill. Tasks are SERIALIZED — never parallel (same target file).
> **Plan Status:** Draft
> **Created:** 2026-08-06
> **Architecture:** Single-file HTML (~80-150 KB) with inline CSS, JS, and JSON-DB. Self-contained, offline, local-first.

**Goal:** Baue einen interaktiven Forensik-Tool-Explorer: Tippe Tool-Name → krieg die Card. 25 Tools in JSON-DB, Search, Filter, Favorites, Comparator, Recipes, Decision-Tree, Themes, Keyboard-Nav.

**Tech Stack:** Vanilla HTML5 + CSS3 (custom properties, grid, flexbox) + Vanilla JS (no framework). localStorage für Favorites. fetch() für tools.json (async load on init).

**Single-file constraint:** Everything inline in one HTML file. JSON-DB embedded as `<script type="application/json" id="tool-db">` block (not external fetch — keeps it truly single-file).

---

## Hard Constraints (NICHT ERLAUBT — breach = abort)

| Constraint | Why |
|---|---|
| `write_file` on the HTML after Task 1 with full content > 4KB | Truncation pitfall (root cause of 2026-08-06 crash). Use `patch` for all subsequent edits. |
| `cat -n` or `cat` to load file content into subagent context | 50KB stdout cap truncates silently. Use `read_file` with offset/limit pagination instead. |
| Parallel subagents editing the same HTML file | `patch` shifts line numbers. Serialize all tasks. |
| `patch` with non-unique `old_string` | Will fail "Found N matches". Always include 2+ lines context. |
| Subagent claims "file written" without Queen verification | Queen MUST `ls -la` + `grep` the claimed anchor after every task. |

---

## Task Breakdown

### Task 1: Scaffold + JSON-DB + Base Layout
**Files:**
- Create: `docs/kali-research/forensik-explorer.html`

**Anchor-Table:**
| Op | Target | Anchor | Verify |
|---|---|---|---|
| Create new file | forensik-explorer.html | N/A (new file) | `ls -la forensik-explorer.html` + `grep -c '<!DOCTYPE' forensik-explorer.html` |

- [ ] **Step 1:** Create `forensik-explorer.html` with:
  - `<!DOCTYPE html>`, `<html lang="de">`, `<head>` with meta tags (charset, viewport, description, theme-color, favicon as data: URI)
  - Google Fonts link (Inter 400/600/700, JetBrains Mono 400/600, Sora 700 only)
  - `<style>` block with `:root` CSS custom properties (dark theme palette from brainstorm)
  - `:focus-visible` global rule
  - `<body>` with: skip-link, header (title + meta), filter-bar (search input + phase filter buttons), main container, footer
  - `<script type="application/json" id="tool-db">` with 25 tool entries (from kali-forensik-overview.md data)
  - Empty `<script>` block at end of body
  - `</body></html>`

- [ ] **Step 2:** JSON-DB schema per tool:
  ```json
  {
    "id": "guymager",
    "name": "guymager",
    "num": 1,
    "phase": 1,
    "phaseName": "Acquisition",
    "cmd": "guymager",
    "desc": "GUI-Klassiker für Disk-Imaging. Multi-threaded, parallel MD5/SHA1/SHA256.",
    "tags": ["GUI", "E01", "AFF", "Hash"],
    "pop": "daily",
    "audioJump": 0,
    "audioTime": "0:00"
  }
  ```
  All 25 tools from the forensik-overview + audiobook script.

- [ ] **Step 3:** Verify: `python3 -c "import json; json.load(open('forensik-explorer.html').read().split('<script type=\"application/json\" id=\"tool-db\">')[1].split('</script>')[0])"` — must print no error.

---

### Task 2: Card Rendering + Grid Layout
**Files:**
- Modify: `forensik-explorer.html` (CSS + JS sections)

**Anchor-Table:**
| Op | Target section | Anchor | Verify |
|---|---|---|---|
| Insert CSS | After `:focus-visible` rule | `:focus:not(:focus-visible){outline:none}` | `grep -c '.tool-card' forensik-explorer.html` |
| Insert JS | After `// === RENDER ===` comment | `<script>` at end of body | `grep -c 'renderTools' forensik-explorer.html` |

- [ ] **Step 1:** Add CSS for `.tool-card` (dark surface, phase-color top border, hover lift, tool-name with `>` prefix, tool-cmd with copy button, tool-desc, tags, pop-badge, audio-jump button).
- [ ] **Step 2:** Add CSS for `.tools-grid` (CSS grid, `repeat(auto-fill, minmax(340px, 1fr))`, gap 16px).
- [ ] **Step 3:** Add JS `renderTools(tools)` function that:
  - Clears `#tool-grid`
  - For each tool: creates `<article class="tool-card" data-phase="N" data-id="toolname">`
  - Renders: tool-head (name + num + pop-badge), tool-cmd (with copy button), tool-desc, tool-tags, tool-audio (jump button + time)
  - Appends to grid
- [ ] **Step 4:** Call `renderTools(DB.tools)` on DOMContentLoaded.

---

### Task 3: Search + Phase Filter
**Files:**
- Modify: `forensik-explorer.html` (JS section)

**Anchor-Table:**
| Op | Target | Anchor | Verify |
|---|---|---|---|
| Insert JS | After `renderTools` function | `renderTools(DB.tools)` call | `grep -c 'filterTools' forensik-explorer.html` |

- [ ] **Step 1:** Add `filterTools(phaseFilter, searchText)` function:
  - Filters by phase (if not "all")
  - Filters by search text (matches name + desc + tags, case-insensitive)
  - Both conditions must match (AND)
  - Calls `renderTools(filtered)`
- [ ] **Step 2:** Wire search input `addEventListener('input', ...)` — debounced 150ms
- [ ] **Step 3:** Wire filter buttons `addEventListener('click', ...)` — sets active state, aria-pressed, calls filterTools
- [ ] **Step 4:** Add "no results" message when filter returns 0 tools.

---

### Task 4: Favorites + localStorage
**Files:**
- Modify: `forensik-explorer.html` (CSS + JS)

**Anchor-Table:**
| Op | Target | Anchor | Verify |
|---|---|---|---|
| Insert CSS | After `.tool-card` styles | `.tool-audio-btn:hover` rule | `grep -c '.fav-btn' forensik-explorer.html` |
| Insert JS | After filterTools | `filterTools` function end | `grep -c 'toggleFavorite' forensik-explorer.html` |

- [ ] **Step 1:** Add `.fav-btn` to each card (star icon, toggles `.active` class)
- [ ] **Step 2:** Add `loadFavorites()` → reads `localStorage.getItem('forensik-favs')` → returns Set of tool IDs
- [ ] **Step 3:** Add `toggleFavorite(toolId)` → updates Set, saves to localStorage, re-renders star state
- [ ] **Step 4:** Add "★ Favorites" filter button in filter-bar (toggles fav-only view)

---

### Task 5: Comparator
**Files:**
- Modify: `forensik-explorer.html` (CSS + JS)

- [ ] **Step 1:** Add `.compare-btn` to each card ("Compare" toggle)
- [ ] **Step 2:** Add `.compare-bar` (fixed bottom, shows selected tools, "Compare" button)
- [ ] **Step 3:** Add `toggleCompare(toolId)` — max 4 tools, updates compare-bar
- [ ] **Step 4:** Add `showCompareModal()` — side-by-side table of selected tools (cmd, tags, pop, phase)
- [ ] **Step 5:** Add `closeCompareModal()` — clears selection

---

### Task 6: Recipes + Decision-Tree
**Files:**
- Modify: `forensik-explorer.html` (JSON-DB + JS)

- [ ] **Step 1:** Add `recipes` array to JSON-DB:
  ```json
  "recipes": [
    {"id": "disk-triage", "name": "Standard Disk-Triage", "tools": ["dc3dd", "mmls", "fls", "foremost"], "desc": "..."},
    {"id": "mem-analyze", "name": "Memory-Analyse", "tools": ["avml", "volatility", "bulk_extractor"], "desc": "..."}
  ]
  ```
- [ ] **Step 2:** Add Recipes section above tool-grid (recipe cards, click highlights involved tools)
- [ ] **Step 3:** Add Decision-Tree wizard: modal with 3 questions (Use Case → Input Type → Skill Level) → recommends tool

---

### Task 7: Keyboard Navigation + Themes
**Files:**
- Modify: `forensik-explorer.html` (JS + CSS)

- [ ] **Step 1:** Add keyboard handler:
  - `Cmd/Ctrl+K` → focus search
  - `1`-`7` → phase filter
  - `0` → show all
  - `f` → toggle favorites filter
  - `c` → open comparator
  - `?` → show keyboard cheat-sheet modal
  - `Esc` → close any modal
- [ ] **Step 2:** Add theme toggle (3 themes: Tape/Dark, Cyber, Light) — persists in localStorage
- [ ] **Step 3:** Add `prefers-reduced-motion` media query (disable animations)
- [ ] **Step 4:** Add reading-progress bar (2px fixed top, scroll-based)

---

### Task 8: Polish + Accessibility Final Pass
**Files:**
- Modify: `forensik-explorer.html` (CSS + JS)

- [ ] **Step 1:** Add `-webkit-` prefixes for backdrop-filter, mask-image
- [ ] **Step 2:** Add aria-labels to all interactive elements (audio-jump, copy, fav, compare buttons)
- [ ] **Step 3:** Add `role="slider"` + aria attributes to audio scrubber (if audio player included)
- [ ] **Step 4:** Verify WCAG AA contrast on all text/background pairs
- [ ] **Step 5:** Add `<noscript>` message
- [ ] **Step 6:** Final HTML validation: `python3 -c "from html.parser import HTMLParser; HTMLParser().feed(open('forensik-explorer.html').read()); print('OK')"`

---

## Verification Checklist (Queen runs after ALL tasks)

- [ ] `ls -la forensik-explorer.html` — file exists, > 60KB
- [ ] `grep -c 'tool-card' forensik-explorer.html` — ≥ 25 references
- [ ] `grep -c 'data-phase' forensik-explorer.html` — ≥ 25 references
- [ ] JSON-DB valid: extract + `json.load()` — no errors
- [ ] `python3 -c "from html.parser import HTMLParser; HTMLParser().feed(open('...').read()); print('OK')"`
- [ ] Open in preview: search "yara" → 1 card visible
- [ ] Open in preview: filter Phase 3 → 6 cards visible
- [ ] Open in preview: star a tool → reload → still starred
- [ ] Open in preview: Cmd+K → search focused
- [ ] File has `<body>`, `</body>`, `</head>`, `</style>`, `</script>` — ALL present

---

## Execution Rules

1. **SERIAL execution** — Task 1 → wait → verify → Task 2 → wait → verify → ...
2. **NEVER parallel** — all tasks modify the same file
3. **Queen verifies after each task** — `ls -la` + `grep` on claimed anchors
4. **Subagents use `patch` only** (never `write_file` for edits after Task 1)
5. **Subagents use `read_file` with offset/limit** (never `cat` or `cat -n`)
