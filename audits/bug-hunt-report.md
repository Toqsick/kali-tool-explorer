# Bug-Hunt Report — Kali Explorer v2.0

- **File:** `docs/kali-research/forensik-explorer.html`
- **Total lines:** 2832
- **Tool DB shape:** JSON in `<script type="application/json" id="tool-db">` (L339–L2195)
- **Counts:** 144 tool records across 131 unique IDs · 12 categories · 2 modes (blue/purple) · 12 playbooks · 5 wizard steps
- **Reviewer:** focused bug-hunt (no fixes applied)

---

## Critical Bugs (will break functionality)

- **[BUG-001] Playbook references 5 tool IDs that do not exist in the tool DB**
  - **Locations:**
    - `recon-sprint` (blue) → `'theharvester'` (DB has `'theHarvester'` with capital H)
    - `ad-attack` (blue) → `'powersploit'`
    - `post-exploit` (blue) → `'powersploit'`, `'empire'` (DB has `'powershell-empire'`)
    - `system-hardening` (purple) → `'letsencrypt'` (DB has `'openssh'` nearby, no let’s-encrypt entry)
    - `threat-hunt` (purple) → `'malcolm'`
  - **Effect:** `highlightPlaybook()` uses `pb.tools.forEach(tid => document.querySelector(`.tool-card[data-id="${tid}"]`)?.classList.add('pb-match'))`. Missing tool IDs silently match nothing — highlight ring never appears on those cards, breaking the "start playbook → see highlighted tools" UX. Wizard output (`pb.tools.map(t => ...)`) renders the ID as text but no backing card exists for the click-through.
  - **Fix:** rename playbook IDs to canonical DB IDs (`theHarvester`, `powershell-empire`), or add stub tools to the DB, or change the playbook to reference existing tools.

- **[BUG-002] Audio buttons render but no `<audio>` element, no click handler, and no playback wiring**
  - **Location:** L2296–L2314 (renderTools), `data-jump` attribute, `.tool-audio-btn` selector exists at L76 but no `document.addEventListener('click', ...)` matches it.
  - **Effect:** Forensics category (24 tools) shows a "▶ Audio" button next to each card. Clicking it does literally nothing. `aria-label="Springt zu Audio bei X:XX"` promises behavior that never happens. Major UX lie.
  - **Fix:** either add a `<audio>` element + delegated handler that seeks to `tool.audioJump`, or delete the audio button + the `audioJump`/`audioTime` fields.

- **[BUG-003] Broken emoji glyph (U+FFFD replacement character) on "Threat Hunt" playbook card**
  - **Location:** L2531 — `icon:'\ufffd'` in the `threat-hunt` entry of purple playbooks.
  - **Effect:** Threat Hunt card renders a black-diamond-with-question-mark (or browser-default tofu) instead of an icon. Visible regression from a likely encoding mishandling (an intended `🕵️` / `🔍` / `🎯`).
  - **Fix:** replace with a valid emoji (e.g. `'🔍'` — already used elsewhere).

- **[BUG-004] Comparator shows "Vergleichen" button when only 1 tool is selected, then silently no-ops**
  - **Location:** L2468 (`if (compareSet.size < 2) return;`), bar rendered at L2456 only when `compareSet.size === 0`. With exactly 1 item the bar stays visible, the user clicks Vergleichen, nothing happens (no toast, no error, no shake).
  - **Effect:** Dead-click frustration. Same for keyboard `C` at L2807.
  - **Fix:** show inline message "Mindestens 2 Tools auswählen", or disable the button at `compareSet.size < 2`, or fall back to a single-tool detail view.

- **[BUG-005] Meta description and subtitle claim "25 Werkzeuge, 7 Phasen" — DB has 144 records**
  - **Location:** L7 (`<meta name="description">`) and L258 (`<p class="subtitle">`).
  - **Effect:** SEO + first-impression misrepresentation. Actual reality: 144 entries / 131 unique IDs, 12 blue + 6 purple = 18 categories, 12 playbooks.
  - **Fix:** dynamic text from `getAllTools().length` rendered into subtitle (`renderHeaderStats` already has the truth); update meta description to match.

- **[BUG-006] Tool IDs are not unique — 12 duplicates collapse favorites, highlights, comparator, and category labels**
  - **Affected IDs:** `nmap`, `masscan`, `maltego`, `wireshark`, `sqlmap`, `nikto`, `legion`, `lynis`, `dradis`, `gvm` (×3), `photorec`, `wazuh`.
  - **Effect — favorites:** `favorites.has(t.id)` Set treats duplicates as one entry; toggling any one mark/unmarks all duplicates of the same id simultaneously in the visual grid (because the className render at L2299 reads `favorites.has(tool.id)` for every card with that id, they all sync — this is actually happy, but cross-mode duplicates where user wants ONLY the purple instance favorited is impossible).
  - **Effect — category label:** L2291 `toolCatMap[t.id] = c` — last write wins. The first-rendered occurrence gets the wrong category badge label.
  - **Effect — playbook highlight:** `document.querySelector('.tool-card[data-id=...]')` returns the FIRST occurrence. Duplicate-id tools beyond the first never get `pb-match`.
  - **Effect — comparator:** `getAllTools().find(t => t.id === id)` always returns the first DB hit; user may have added the second occurrence to the comparator and never sees the correct rendering in the modal.
  - **Fix:** namespace IDs (`blue/identify:nmap` vs `purple/protect:nmap`) or keep a `(mode, category)` tuple as the Set key.

---

## Important Bugs (degraded UX)

- **[BUG-101] `currentMode` from localStorage is unvalidated**
  - **Location:** L2203 — `let currentMode = localStorage.getItem(MODE_KEY) || 'blue';`
  - **Effect:** If user (or another script) sets `localStorage['kali-mode']` to `'rainbow'`, then `DB.modes['rainbow']` is `undefined` → first call to `getCategories()` throws `Cannot read property 'categories' of undefined`. Whole app dies.
  - **Fix:** `if (!['blue','purple'].includes(currentMode)) currentMode = 'blue';`

- **[BUG-102] Bare `JSON.parse` on DB at startup**
  - **Location:** L2199 — `const DB = JSON.parse(document.getElementById('tool-db').textContent);`
  - **Effect:** If the JSON ever becomes invalid (HTML-unescape glitch, manual edit, BOM), the entire `<script>` block throws on line 2 and nothing renders. No fallback.
  - **Fix:** wrap in try/catch and render an error message; or render server-validated JSON.

- **[BUG-103] Bare `localStorage.setItem` in 4 of 5 sites**
  - **Location:** L2213 (mode), L2342 (favorites), L2748 (theme). Only `loadFavorites` (L2338) is wrapped in try/catch.
  - **Effect:** In private-browsing / Safari ITP / quota-exceeded, the first `setItem` throws and aborts the rest of init silently.
  - **Fix:** wrap every storage write in a `safeSet(key, value)` helper that swallows & warns.

- **[BUG-104] `kbd-hint` (z=90) is covered by `compare-bar` (z=100)**
  - **Location:** L165 + L91.
  - **Effect:** When the comparator bar slides up at the bottom, the floating "Shortcuts" hint in the bottom-right is occluded. Visual regression for power users who keep the comparator open.
  - **Fix:** bump `.kbd-hint` above the compare bar (z=110) or reposition it to `top:64px` / `left:16px`.

- **[BUG-105] `#wizard-open` button uses class `wizard-btn` but has no base CSS rule (only a purple-mode override at L211)**
  - **Location:** HTML L280 — `<button class="wizard-btn" id="wizard-open">🧭 Guided Wizard</button>`. The `[data-mode="purple"] .wizard-btn` rule at L211 styles it in purple mode (purple border, purple text), but no base rule provides padding/colors/background for the default state, so it relies entirely on browser-default button styling. Identical issue: the print rule at L233 *does* include `.wizard-btn{display:none}` which masks it from print output, confirming the original developer intent.
  - **Effect:** Inconsistent button appearance — looks unstyled in blue mode (no theme accent), only gets the purple ring in purple mode. The print rule hides it, which means a developer *did* think of this class.
  - **Fix:** add a base `.wizard-btn{padding:8px 16px;border:1px solid var(--border);border-radius:8px;background:var(--bg-elevated);color:var(--text-primary);cursor:pointer;font-size:.85rem;font-family:var(--font-body)}` (and a hover variant), so blue mode also gets a proper look.

- **[BUG-107] `.recipe-name` CSS rule targets a class that is never used**
  - **Location:** L210 — `[data-mode="purple"] .recipe-name{color:#c084fc}`. No element matches.
  - **Effect:** Dead CSS — leftover from a removed "recipes" feature (consistent with the clean removal of `renderRecipes`).
  - **Fix:** delete L210.

- **[BUG-108] `Object.hasOwn` … `dup` IDs broken in comparator modal "Tags" row**
  - **Location:** L2475 — `Tags: get: t => t.tags.join(', ')`. If a duplicate-id tool has `tags` missing in one record but present in another, the first hit always wins; also no guard for `t.tags === undefined`.
  - **Effect:** `TypeError: Cannot read property 'join' of undefined` if any tool lacks the `tags` array (legacy data safety).
  - **Fix:** `(t.tags || []).join(', ')`.

- **[BUG-109] `highlightPlaybook` silently no-ops if `pb.tools` references IDs missing from DOM**
  - **Location:** L2568 — `document.querySelector(`.tool-card[data-id="${tid}"]`)?.classList.add('pb-match');` — the `?.` makes the missing-match silent.
  - **Effect:** Combined with BUG-001, 5 playbook tools never highlight. No console warning, no visual cue. User assumes the playbook "didn't work".
  - **Fix:** collect missing IDs into a one-time `console.warn` per playbook activation.

- **[BUG-110] Mode-switch / theme / playbooks / wizard — no focus trap inside modals**
  - **Location:** all modals (`.compare-modal-overlay`, `.wizard-overlay`, `.cheat-overlay`).
  - **Effect:** Tabbing out of the modal puts focus on the page behind the dim overlay. Screen-reader / keyboard users can lose context. No `role="dialog"` / `aria-modal="true"` / `aria-labelledby`. No initial focus management (focus stays on the button that opened the modal).
  - **Fix:** add role/aria-modal attributes and a small focus-trap helper that loops Tab inside the open overlay.

- **[BUG-111] `playbook-card` lacks `role="button"` and `aria-pressed`**
  - **Location:** L2545–L2554 — `.playbook-card` is a `<div>` with click handler but no semantics.
  - **Effect:** Screen readers announce "group, playbook-name", not "button, toggle". Keyboard users can't activate it (no `tabindex`, no Enter/Space handler).
  - **Fix:** make it a `<button>` (preferred) or add `role="button" tabindex="0"` + keydown Enter/Space handler + `aria-pressed`.

- **[BUG-112] Wizard content/state stale when user switches mode mid-wizard**
  - **Location:** L2707–L2712 wizard-open resets state only at open; `renderWizardStep()` reads `wizardFlows[currentMode]` at render time but cached DOM is not re-rendered when mode changes while modal is visible.
  - **Effect:** If user opens wizard in blue → switches to purple (without closing modal) → stays on blue flow content. The blue "result" buttons trigger `highlightPlaybook(pbId)` which then queries `getPlaybooks()` and `pbId` may not exist in purple → silent fail (L2565 `if (!pb) return;`).
  - **Fix:** inside wizard-open or mode-switch, if `wizard-overlay.visible`, call `renderWizardStep()` again.

- **[BUG-113] Top-of-document init runs OUTSIDE `DOMContentLoaded` (script is at end of body, but order matters if moved)**
  - **Location:** L2236 calls `renderPlaybooks()` before L2826 `DOMContentLoaded` handler. L2232 mode-button listeners attached at script-parse time, not deferred.
  - **Effect:** Works today because script is at end of body and DOM is parsed. Brittle — moving the `<script>` to `<head>` would break everything.
  - **Fix:** wrap all init in `window.addEventListener('DOMContentLoaded', () => {...})` or `<script defer>`.

- **[BUG-114] `window.toggleFavorite = toggleFavorite;` precedes the function declaration**
  - **Location:** L2346 vs L2348. Works only because `function` declarations hoist. If `toggleFavorite` were ever refactored to `const toggleFavorite = function() {...}`, `window.toggleFavorite` would be `undefined` and the line `let favorites = loadFavorites()` would still succeed but external triggers would silently no-op.
  - **Effect:** Latent footgun.
  - **Fix:** move the assignment after the declaration, or use an IIFE.

- **[BUG-115] Theme toggle buttons have no visible focus style on `cyan accent` for non-`:focus-visible` users**
  - **Location:** L23–L24 — `:focus-visible{outline...}` exists but L251–L253 theme buttons are empty `<button>`s without text. With `aria-label`, NVDA/JAWS announce correctly, but low-vision users relying on visual focus ring still see one because of `outline:2px solid var(--accent-cyan)`. So this is **OK** — leave it. *Noted but not a bug.*

- **[BUG-116] Keyboard `1`–`9` digit bound to category filter, conflicts with no other shortcut, but no `Shift+1` etc. for 10+ categories (12 blue categories exist)**
  - **Location:** L2783–L2795.
  - **Effect:** Blue mode has 12 categories, only `1`–`9` accessible via keyboard. Purple has 6 — all OK. Power users on blue mode can't reach categories 10/11/12 via key.
  - **Fix:** document as known limit OR map `!@#$%^&*()` to blue 10–12 / extend to letter keys.

- **[BUG-117] `.filter-search:focus{border-color:var(--accent-cyan)}` not overridden by purple-mode CSS, but `[data-mode="purple"] .filter-search:focus{border-color:#a855f7}` (L206) — good. *Noted, no bug.***

- **[BUG-118] Search query that returns 0 results + favorites filter active = silent zero state, no message specific to "no favorites"**
  - **Location:** L2282–L2287 — generic `no-results` div with text "Kein Tool gefunden. Versuche einen anderen Suchbegriff." shown for any empty result.
  - **Effect:** User with favorites filter on who types "xyz" gets the same message as a user with all results off. Could say "Keine Favoriten gefunden" when `favOnly && resultCount === 0`.
  - **Fix:** parameterize the message.

---

## Minor Issues

- **[BUG-201] `compare-tool` `name` field inserted via `innerHTML` — XSS surface**
  - **Location:** L2302 `tool.name`, L2306 `tool.desc`, L2307 tag-text, L2463 `${tool.name}`, L2480 `<th>${t.name}</th>` and L2484 `row.get(t)` (description/text). Same for `cat.name`, `pb.name`, `pb.desc`, `pb.tools`, etc.
  - **Effect:** Today the data is hard-coded and safe. If anyone ever imports the tool DB from user input / external feed, HTML injection becomes possible (`<img onerror=...>`).
  - **Fix:** create a small `esc(s)` helper and use everywhere innerHTML builds user-facing strings. Or use `textContent` / `createElement` for every interpolation.

- **[BUG-202] No-CORS `<link>` to fonts.googleapis.com leaks request to Google on first paint**
  - **Location:** L10–L12.
  - **Effect:** Privacy / offline-mode behavior. Minor.

- **[BUG-203] `<noscript>` block visible until JS runs, but is stripped by `<style>` rules. Slight FOUC for first paint.**
  - **Location:** L245.
  - **Effect:** Cosmetic.

- **[BUG-204] `compare-bar` overflows viewport width on screens < 320px because `flex-wrap:wrap` + 24px padding**
  - **Location:** L91.
  - **Effect:** Items wrap but the bar may still need horizontal scroll on tiny screens. Cosmetic.

- **[BUG-205] `.theme-toggle{position:absolute;top:48px;right:24px}` ignores header height change in mobile**
  - **Location:** L186.
  - **Effect:** On mobile (header-inner goes column), the theme buttons may overlap the title block.
  - **Fix:** also relocate under `@media(max-width:640px)`.

- **[BUG-206] Wizard option buttons don't activate on Enter / Space when focused**
  - **Location:** L2654–L2667 — only adds `click` listener, not keydown.
  - **Effect:** Buttons are native `<button>`s so Enter/Space activates click → actually this DOES work natively in all browsers. *Not a bug, leaving as note.*

- **[BUG-207] No try/catch around `navigator.clipboard.writeText` (L2323)**
  - **Location:** Copy handler.
  - **Effect:** In non-secure-context or clipboard-denied iframes, promise rejects silently — user sees "Copy" button briefly toggle, then revert with no signal.
  - **Fix:** `.catch(err => e.target.textContent = '✗')` with a short revert.

- **[BUG-208] `scroll-padding-top:100px` on `html` interacts with `.filter-bar` (`position:sticky;top:0`) — anchor jumps feel slightly too low for everything except the header**
  - **Location:** L27.
  - **Effect:** Cosmetic, but `prefers-reduced-motion` already kills smooth-scroll.
  - **Skip.**

- **[BUG-209] `cardFadeIn` animation (L218–L219) runs every time `renderTools` rebuilds the grid — including on filter/search toggle**
  - **Location:** L218.
  - **Effect:** Every keystroke in search causes all matching cards to re-fade. Distracting & costly.
  - **Fix:** apply the animation only on first render, or skip animation for re-renders.

- **[BUG-210] `loadTheme()` reads localStorage without try/catch**
  - **Location:** L2742.
  - **Effect:** Same as BUG-103 family — minor.

- **[BUG-211] `compareModal` shows "Audio" row with empty cells when first tool has `audioTime` and second doesn't (L2477 `Audio: get: t => t.audioTime` returns `undefined`)**
  - **Location:** L2477.
  - **Effect:** Row renders "—" / blank inconsistently across columns. Cosmetic.

- **[BUG-212] `switchMode()` resets `currentSearch=''` and `favOnly=false` but does not call `debouncedSearch(value)` to clear the debounce timer**
  - **Location:** L2220–L2223.
  - **Effect:** If a debounced search was in flight, it may overwrite the render 150ms later, showing stale matches.
  - **Fix:** capture timer id and `clearTimeout(t)` in `switchMode`.

- **[BUG-213] `Object-id` row in compare-table has duplicate label "Kategorie"**
  - **Location:** L2472 (label "Kategorie") vs L2476 (label "Kategorie" again — clearly intended "Popularität").
  - **Effect:** Compare-table renders two rows with identical header — looks like a bug.
  - **Fix:** rename second label to e.g. `Popularität` or `Pop`.

- **[BUG-214] `compareSet.has(tool.id)` in the render template (L2308) — when duplicate-id tools exist, every duplicate renders `active` simultaneously**
  - **Location:** L2308.
  - **Effect:** User sees 2+ "Vergleichen" buttons marked active when they meant only one. Cosmetic but confusing.

- **[BUG-215] `Mode-Switch: globaler Mini-Fade` (CSS L26) overrides `transform` transitions globally**
  - **Location:** L26 — `*,*::before,*::after{transition:background-color .2s ease,border-color .2s ease,color .15s ease,box-shadow .2s ease,opacity .2s ease,fill .2s ease}` — note: `transform` is *not* in the list, but the .tool-card has `transition:transform .2s,box-shadow .2s,border-color .2s` at L54. Two different transition lists → first declaration wins for unspecified transitions. Cosmetic.

- **[BUG-216] `cheat-overlay` toggle via `?` does not announce state to screen readers**
  - **Location:** L2777–L2779.
  - **Effect:** Modal opens without aria-expanded/aria-hidden update on the hint button. Minor a11y gap.

---

## Data Integrity Issues

### Missing tool IDs in playbooks (cross-reference result)

| Playbook       | Mode  | Tool ID         | Status                                              |
|----------------|-------|-----------------|-----------------------------------------------------|
| recon-sprint   | blue  | `theharvester`  | ❌ DB has `theHarvester` (capital H) — casing mismatch |
| ad-attack      | blue  | `powersploit`   | ❌ Not in DB (closest: `evil-winrm`, `impacket-scripts`) |
| post-exploit   | blue  | `powersploit`   | ❌ Not in DB                                         |
| post-exploit   | blue  | `empire`        | ❌ DB has `powershell-empire`                       |
| system-hardening | purple | `letsencrypt` | ❌ Not in DB (purple/protect has no equivalent tool) |
| threat-hunt    | purple | `malcolm`      | ❌ Not in DB (Malcolm is a UI, not a Kali package)   |

### Duplicate tool IDs across categories

| Tool ID      | Occurrences                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------|
| `nmap`       | blue/info-gathering, purple/identify                                                                         |
| `masscan`    | blue/info-gathering, purple/identify                                                                         |
| `maltego`    | blue/info-gathering, blue/reporting-tools                                                                    |
| `wireshark`  | blue/info-gathering, blue/sniffing-spoofing                                                                  |
| `sqlmap`     | blue/web-app-analysis, blue/database-assessment                                                              |
| `nikto`      | blue/vulnerability-analysis, purple/identify                                                                  |
| `legion`     | blue/vulnerability-analysis, purple/identify                                                                  |
| `lynis`      | blue/vulnerability-analysis, purple/govern                                                                    |
| `dradis`     | blue/reporting-tools, purple/govern                                                                           |
| `gvm`        | blue/vulnerability-analysis, purple/govern, purple/identify                                                    |
| `photorec`   | blue/forensik, purple/recover                                                                                 |
| `wazuh`      | purple/detect, purple/respond                                                                                 |

12 duplicates × varying counts → 13 redundant tool entries; favorites/comparator/highlight logic is built on `id` equality and will silently misbehave for all 12.

### Stale references check (Task bullet 2)

| Pattern            | Matches |
|--------------------|---------|
| `DB.tools`         | 0       |
| `DB.phases`        | 0       |
| `data-phase`       | 0       |
| `currentPhase`     | 0       |
| `renderRecipes`    | 0       |
| `recipes`          | 0       |
| `recipe` (CSS str) | 1 (`.recipe-name` at L210 — dead CSS rule, see BUG-107) |

✅ Legacy migration complete — no stranded call sites from the v1 "phases/recipes" data model.

---

## Recommendations

1. **Fix BUG-001 through BUG-006 before any release** — they break primary UX (playbook click-through, audio button illusion, comparator empty-state, content-count meta) or hide data integrity issues (duplicate IDs).

2. **Namespace tool IDs** as `<mode>/<category-id>:<base-id>` (or simply suffix `-blue` / `-purple` where the same toolname serves in both modes with different meaning). This eliminates BUG-006 family entirely.

3. **Adopt a single `safeStorage` helper** around all localStorage access — covers BUG-103 + BUG-210.

4. **Wrap parsing of `<script type="application/json">` in try/catch** and render an error banner — covers BUG-102.

5. **Add ARIA semantics to playbook-card** and **focus-trap to modals** — covers BUG-110 + BUG-111.

6. **Decide on audio feature** — either wire the playback (BUG-002) or remove the buttons and the `audioJump`/`audioTime` fields entirely.

7. **One additional breakpoint** for 641–1024px tablets — extend `.compare-modal` padding rules below 640px.

8. **Deterministic fav-style for duplicates** — either deduplicate IDs upstream or use a different set-key strategy so favoriting a tool in `blue/post-exploitation` is independent from `purple/protect`.

9. **Fix CSS typos** — rename `.wizard-btn` (BUG-105/106) and remove `.recipe-name` rule (BUG-107) so cleanup audit passes.

10. **Re-run this audit after fixes** with the same script (`/tmp/bughunt.py`) to confirm no missing IDs remain and no new duplicates are introduced.

---

## Appendix — Methodology

1. Read full HTML (2832 lines) in 6 chunks via `read_file`.
2. Extracted tool DB JSON via regex; loaded into Python.
3. Cross-referenced `pb.tools[]` arrays (12 playbooks) against `getAllTools()` derived IDs.
4. Searched JS/CSS for stranded patterns: `DB.tools`, `DB.phases`, `data-phase`, `currentPhase`, `renderRecipes`, `recipes`.
5. grepped `aria-`, `role=`, `z-index:`, `localStorage`, `addEventListener`, `<audio>`, `data-jump` for missing wiring.
6. Hex-inspected all `icon:'...'` values in playbook definitions; identified U+FFFD replacement char at L2531.
7. Confirmed z-index stacking by reading all `z-index:` declarations and tracing overlap between `.compare-bar` (z=100) and `.kbd-hint` (z=90).
8. Verified no `<audio>` element, no `new Audio()`, and no click handler for `.tool-audio-btn` exists.

**Helper script:** `/tmp/bughunt.py` (run with `python3 /tmp/bughunt.py` to re-verify data integrity section after edits).
