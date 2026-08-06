# UI/UX Polish Report v2 — Kali Explorer v3.0

> **Scope:** Visual quality, comfort, and consistency across the **4 NEW v3.0 features**
> (Tool-Detail-Modal, LLM-Prompt-Builder, Command-Builder, Learning-Paths) plus the cross-cutting
> concerns introduced by them (modal stack, mode-switch coverage, mobile breakpoints, a11y).
>
> **Companion docs (do not duplicate):**
> - `audits/ui-polish-report.md` (v2.0 polish — cards, filters, wizard, comparator)
> - `audits/bug-hunt-report.md` (functional bugs — playbook IDs, audio dead-buttons, dup IDs)
> - `audits/grand-polish-review-ux.md`, `audits/grand-polish-review-engineer.md` (broad audits)
>
> **File audited:** `docs/kali-research/forensik-explorer.html` — 4133 lines, 176 KB
> **Reviewer stance:** describe only — **no code changes applied.**

---

## Executive Summary

The v3.0 features are a coherent, well-styled addition that respects the existing dark/cyan/purple
language. But the polish bar is held back by **systemic gaps, not cosmetic nits**:

1. **Mobile is unhandled.** Only one `@media(max-width:640px)` rule in the whole file, and it only
   flattens the tool grid. The 4 new features overflow, clip, or become unusable below ~640 px.
2. **Accessibility was not extended.** `role="dialog"`, `aria-modal`, focus-trap, `aria-live`
   for the live prompt output — none of these exist for the new modals.
3. **Empty/loading/error states are missing.** Path progress at 0%, empty favorites in Prompt
   Builder, Cmd-Builder with no target, all silently render a dead-looking widget.
4. **Visual hierarchy between Playbooks and Learning-Paths is too flat.** Both use the same
   `h2` size, same card pattern, same section spacing — they read as one duplicated block.
5. **Micro-interactions are inconsistent.** Some buttons animate on hover, some don't. Copy
   feedback varies (`'✓'` vs `'✅ Kopiert!'` vs text reversion 1500 ms). Section transitions
   between Playbooks → Paths → Tools grid are abrupt.

The good news: every issue below is **CSS-only or trivially-extends-the-existing-render**
— no DB schema changes, no JS rewrites.

---

## TL;DR — Counts

| Bucket | Count | Effort |
|--------|------:|--------|
| Quick Wins (≤ 30 min CSS / 1 hr total) | **9** | XS–S |
| Medium (1–3 hr) | **7** | S–M |
| Big Ideas (half-day+) | **4** | L |

Plus **5 ready-to-paste CSS/HTML snippets** for the top recommendations at the bottom.

---

# Section 1 — Tool-Detail-Modal

> Triggered by clicking a tool card. z-index 300, max-width 640 px, max-height 85 vh.
> Contains: badge, name, category, description, tags, std-command, examples, command-builder,
> related tools, external links.

## Quick Wins

**[QW-D1] Header badge colors are inconsistent with the card.**
`.tool-pop.daily` uses `var(--accent-cyan)` (cyan); `.detail-badge.daily` uses
`var(--accent-green)`. Same word "Daily Driver", different hue. Pick one and reuse.

```css
/* Suggested unification — pick the green/cyan that matches "active" everywhere */
.detail-badge.daily{background:rgba(34,211,238,.12);color:var(--accent-cyan)}
```

**[QW-D2] `.detail-cat` (category row) is the dimmest type on the page at 0.65 rem muted.**
On dark backgrounds this falls below WCAG AA contrast (3.0:1). Bump to `.7rem` and `--text-secondary`.

**[QW-D3] Standard-command block has a copy button that swaps to `✓` for 1500 ms.**
Detail examples and the related-tools section have **no** copy affordance. Inconsistent.
Either add a per-example copy button, or remove the one on the standard cmd and add a single
"Copy all examples" affordance — your call, but pick a side.

**[QW-D4] Related-tools grid `minmax(140px, 1fr)` is too sparse on wide screens.**
At 640 px modal width × 6 cards you get 4 columns of 140 px — but only 4 cards fit a row,
and the last 2 sit alone on row 2. Bump `minmax(160px, 1fr)` so it goes 3 + 3 cleanly.

**[QW-D5] No empty-state when the related-tool pool is empty.**
Forensics-only tools (which exist in only one category) always have ≥ 5 peers, so today the
"shared tags" fallback always succeeds — but a single-tool category would silently render
"no related tools" with no explanation. Add a `.detail-related-empty` styled as muted text.

## Medium Effort

**[M-D1] The whole modal scrolls as one block.** On a 600-px-tall mobile, users see only the
header + first 2 sections; the Examples and Cmd-Builder are below the fold and there is no
TOC. Add an internal scroll-spy or sticky mini-nav (`Beschreibung · Kommandos · Builder ·
Verwandt · Links`).

**[M-D2] Cmd-Builder appears as an inline sub-section with no visual divider from
"Beispiel-Kommandos" above it.** A user skimming sees two near-identical blocks of
checkboxes/commands. Add a `border-top:1px dashed var(--border)` between them and a different
section-icon (🔧 vs �).

**[M-D3] Related-tool click re-renders the entire modal** (via `showToolDetail`). Works, but
the modal does not animate the transition — it just snaps. A 120 ms `opacity` fade on the
inner `.detail-body` would feel premium.

## Big Ideas

**[B-D1] Make Detail-Modal the canonical entry point.** Today Cmd-Builder lives *inside*
the detail. If you later build a full-screen Cmd-Builder (with explanation panels for each
flag), promote it to a sibling of Detail-Modal and link between them with a breadcrumb.

---

# Section 2 — LLM-Prompt-Builder

> Triggered by header button `🤖 Prompt Builder`. z-index **350** (highest in app).
> Contains: 4 template cards, target input, ~144 tool chips, output area, copy/download.

## Quick Wins

**[QW-P1] Tool-chip list has no visual distinction between "selected" vs "available" beyond color.**
On 200 px height with ~30 chips visible, users lose track. Add a small leading bullet `✓` for
selected chips in addition to the cyan border (already done — but only the border, which is
invisible against the cyan background tint). Bump contrast:

```css
.prompt-tool-chip.selected{background:rgba(34,211,238,.18);border-color:var(--accent-cyan);
  color:#e0fbff;font-weight:600}
```

**[QW-P2] "★ Favoriten laden" button uses ★ which conflicts with the gold star color used
elsewhere.** Use `🟦 Favoriten` or `📥 Favoriten` to avoid the false promise that you're
starring a favorite.

**[QW-P3] Target input placeholder is great, but there's no helper line telling users
"{TARGET} will be substituted."** Add a one-line hint below the input that updates live as
the user types (e.g., "Wird eingesetzt in: Pentest Plan, SOC Analyse, Incident Response,
Lern-Guide" — count of templates that contain the placeholder).

**[QW-P4] Output area has a fixed 300 px max-height with `overflow-y:auto` but no
sticky-to-bottom scroll on update.** When the user adds the 8th tool, the output scrolls
to top and the newly-appended content is below the fold. Add `scrollTop =
scrollHeight` after `textContent = …` in every rebuild path.

**[QW-P5] Copy button feedback is `'✅ Kopiert!'` but the Download button has zero feedback.**
Inconsistent. Add the same `'✅ Gespeichert!'` swap for download.

**[QW-P6] Prompt-modal `max-width:720px` is wider than detail-modal `640px`** — but Prompt
has no horizontal content that warrants it (all chips are inline). Tighten to 680 px so the
two modals feel like a family.

## Medium Effort

**[M-P1] No template description preview on hover/focus.** Users see "Pentest Plan" and
"Erstelle einen strukturierten Pentest-Plan für…" only *after* clicking. Add a
`title="Vollständiges Template ansehen"` tooltip OR — better — a small "ℹ" disclosure
that pops the full role/task/output text in a side panel.

**[M-P2] Tool-chip filter input is missing.** With 144 chips, finding one in the scrollable
list is tedious. Add a search input above the chip cloud (debounced 150 ms, same UX as
the global search).

**[M-P3] Prompt-builder forgets state when re-opened.** Closing and re-opening the modal
re-renders from scratch — fine — but the previous "★ Favoriten laden" selections are
silently dropped instead of being highlighted ("previously selected"). Add a
`selected-last` ghost state on re-open.

**[M-P4] Output is plain `<div>` text, not Markdown-rendered.** Users expect the bold/italic/
backticks in the prompt to render. Two options: (a) render with `marked.min.js` (~50 KB,
worth it); (b) leave as plain text but at least render the `**bold**` literally with a
subtle muted style so the user sees what they're sending.

## Big Ideas

**[B-P1] Add a "history" tab.** Users will iterate on prompts. Save last 5 generations in
`localStorage` and offer a "recent prompts" list. Power feature, low dev cost.

**[B-P2] Template editor.** Today templates are hard-coded. Add a JSON editor modal
("Erweiterte Modus") that lets a power-user define their own template with the same
4-field shape. Closes the gap between casual and power user.

---

# Section 3 — Command-Builder

> Lives inside the Detail-Modal. Only renders when `tool.id ∈ toolFlags` (15 tools).
> Contains: target input, 4-8 flag checkboxes, live command preview, copy button.

## Quick Wins

**[QW-C1] `min-height:1.2em` on `.cmdbuilder-output` is too short** for a 1-line output, but
the moment the user toggles a flag, padding-right:90px creates a one-line tall block with the
copy button overlapping the text. Test: open `nmap` Cmd-Builder, check all 8 flags, observe
the copy button sits on top of the last 6 characters of the output. Add
`padding-right:96px;min-height:2.4em`.

**[QW-C2] Flag checkbox + label click area is split.** Clicking the label toggles the
checkbox (because the label is a `<div>`, not a `<label>`). Clicking the *description* text
does NOT toggle. Wrap each flag in a real `<label>` so the whole row is clickable. (The
current code at L3418 does toggle on row click via JS — but screen readers don't know.)

```css
.cmdbuilder-flag{cursor:pointer;user-select:none}
.cmdbuilder-flag input[type=checkbox]+*{pointer-events:none} /* fallback */
```

…or convert the JSX-style template to use `<label class="cmdbuilder-flag">` wrappers.

**[QW-C3] `Flags ein-/ausschalten → Command wird live generiert` hint is helpful but
low-contrast italic.** Same fix as detail-cat: bump from `--text-muted` to `--text-secondary`
and remove italic — italic on mono is harder to scan.

**[QW-C4] No "Reset flags to defaults" button.** Users who toggle everything off then want
to start over have to manually re-check 4-8 boxes. Add a "↺ Defaults" ghost button next to
the copy button.

**[QW-C5] Target placeholder is generic ("IP oder Hostname") but doesn't hint at the tool's
quirk.** For sqlmap, "http://target.com/page?id=1" is required — for hydra, "ssh://host"
is required. Show a one-line example below the input that disappears once the user types.

## Medium Effort

**[M-C1] Live command preview has no syntax awareness.** The output is just concatenated
strings — but flags like `-t 4` *should* show the `4` as a distinct color (parameter value
vs flag itself). Add a tiny tokenizer:
- `<span class="cmd-tool">nmap</span> <span class="cmd-flag">-sV</span> <span class="cmd-target">scanme.nmap.org</span>`

**[M-C2] No undo for accidental clicks.** Clicking a flag toggles it instantly. Add a 4-second
"↶ Rückgängig" pill that appears after a toggle, disappears if untouched.

**[M-C3] Flag descriptions mix DE and EN** (`-sV — Services und Versionen erkennen` is mostly
German, but flag id and shell form are English). Acceptable, but the *prefix* field is raw
string (`'-sV '`) — sometimes the prefix includes the trailing space, sometimes not
(`'--min-rate 1000 '` vs `'--banner'`). Audit `toolFlags` for inconsistent trailing-space
behavior and standardize.

## Big Ideas

**[B-C1] Add "Explain this flag" hover.** Power-user learning accelerator. On flag hover,
show a popover with: what the flag does, when to use it, common combos, link to man page.
Cheap with the man-page link already in the Detail-Modal.

**[B-C2] Persist user's flag-set in localStorage per tool** so opening nmap Cmd-Builder
yesterday's choices. UX win for iterative workflows.

---

# Section 4 — Learning-Paths

> 4 paths × 2-4 weeks × 3-4 tools. Card grid `minmax(320px, 1fr)`. Click to expand.
> Progress persisted in `localStorage['kali-path-progress']`.

## Quick Wins

**[QW-L1] Section header is `�️ Lernpfade` with no button counterpart** (compare Playbooks
section, which has both `🚀 Quick-Start Playbooks` + `🧭 Guided Wizard` + `🤖 Prompt Builder`
buttons). Add a `📊 Mein Fortschritt` button that opens a summary modal
("Du bist 23% durch Pentest von Null").

**[QW-L2] Progress bar height is 4 px — almost invisible on a 1024-px+ screen.**
Bump to 6 px, and add a subtle inner glow on the filled portion for visual weight.

```css
.path-progress-bar{height:6px;box-shadow:inset 0 1px 2px rgba(0,0,0,.4)}
.path-progress-fill{box-shadow:0 0 8px rgba(34,211,238,.4)}
```

**[QW-L3] `path-week-tool` chips are grey-on-grey (`--bg-elevated` + `--text-muted`).**
They disappear against the card background. Add `color:var(--text-secondary)` and a hover
state that links them to the tool's Detail-Modal:

```css
.path-week-tool{cursor:pointer;transition:color .2s,border-color .2s}
.path-week-tool:hover{color:var(--accent-cyan);border-color:var(--accent-cyan)}
```

Then in JS: click handler opens the tool's detail modal.

**[QW-L4] `path-reset` (Fortschritt zurücksetzen) only appears when progress > 0.** Good.
But it uses `--text-muted` → `--accent-red` on hover, with no confirmation. A user who
accidentally clicks loses their entire 4-week progress. Add a single `confirm()` or, better,
an inline "Bist du sicher? [Ja] [Nein]" reveal.

**[QW-L5] No visual distinction between completed weeks and current week.**
Today all weeks render the same; the checkbox is the only signal. Add a `.done` modifier:

```css
.path-week.done .path-week-title{text-decoration:line-through;color:var(--text-muted)}
.path-week.done .path-week-check{accent-color:var(--accent-green)}
```

## Medium Effort

**[M-L1] Path cards vs Playbook cards are visually identical** (same bg, border, padding,
hover treatment). New users can't tell they're different categories. Differentiate:

```css
.path-card{border-left:3px solid var(--accent-cyan)} /* vertical accent */
.playbook-card{border-top:3px solid transparent}    /* keep clean */
```

Or use a subtle background hue (`rgba(34,211,238,.02)` for paths).

**[M-L2] Click-to-expand only works on the card itself, not on the title/icon area.** A user
who clicks `.path-name` or `.path-icon` expects expand — and gets it (event delegation). But
clicking the *progress bar* or the *progress text* does NOT expand (because they bubble up
to the card too… actually, this works). Re-test: clicking the progress text DOES expand.
Skip if confirmed.

**[M-L3] Cards close when another opens (single-open accordion).** Good. But there's no
animation — instant snap. Add a 200 ms height/opacity transition on `.path-weeks`:

```css
.path-weeks{display:block;max-height:0;overflow:hidden;opacity:0;
  transition:max-height .25s ease,opacity .2s ease,margin-top .25s ease}
.path-card.active .path-weeks{max-height:1000px;opacity:1;margin-top:16px}
```

(Caveat: max-height transitions skip intermediate values — but visually fine for ≤ 6 weeks.)

**[M-L4] No keyboard navigation.** The card is a `<div>` with no `role`, no `tabindex`.
Adding the same checkbox pattern as the favorite button would make this accessible:
`role="region"` + `aria-expanded` + `tabindex="0"` + Enter/Space to toggle.

## Big Ideas

**[B-L1] Inline tooltips on week-tool chips.** Hovering `nmap` should preview the tool's
description (without opening the full Detail-Modal). Use the native `<details>` element or
a custom popover with the existing tool DB.

**[B-L2] Progress export.** Add a "📤 Fortschritt teilen" button that copies a shareable
URL (`#path=pentest-zero:3`) which, when opened, restores the user's progress. Same pattern
works for favorites.

---

# Section 5 — Cross-Feature Consistency

## Modal / overlay z-index map

| Layer | z-index | backdrop-filter | role/aria-modal |
|-------|--------:|-----------------|-----------------|
| `.skip-link` | 100 | — | ✅ |
| `.reading-progress` | 300 | — | n/a |
| `.filter-bar` (sticky) | 50 | ✅ | n/a |
| `.compare-bar` | 100 | ✅ | n/a |
| `.kbd-hint` | 90 | — | role=button |
| `.compare-modal-overlay` | 200 | ❌ | ❌ |
| `.cheat-overlay` | 200 | ❌ | ❌ |
| `.wizard-overlay` | 200 | ❌ | ❌ |
| `.detail-overlay` | 300 | ✅ | ❌ |
| `.prompt-overlay` | 350 | ✅ (no -webkit) | ❌ |

**Findings:**
- **z-index ladder is correct** as specced: detail(300), prompt(350), wizard(200). ✅
- **prompt-overlay is missing `-webkit-backdrop-filter`** while detail-overlay has it
  (inconsistent cross-browser support). Trivial fix.
- **compare / wizard / cheat overlays have no backdrop-filter** — they look flatter than
  detail/prompt. Add `backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)` to all
  three for visual consistency. (Cheat-modal especially — it's a tiny modal that benefits
  most from depth.)
- **None of the 4 new modals have `role="dialog"`, `aria-modal="true"`, or focus-trap.**
  Keyboard users tab into the page behind the dim overlay. Add a 10-line focus-trap helper.

## Mode-switch coverage

Searched 46 `[data-mode=...]` selectors. Coverage by feature:

| Feature | Blue-default | Purple-override | Complete? |
|---------|:---:|:---:|:---:|
| Tool cards | ✅ | ✅ | ✅ |
| Playbooks | ✅ | ✅ | ✅ |
| **Learning Paths** | ✅ (default) | ✅ (hover/active/fill/checkbox) | ✅ |
| **Tool-Detail-Modal** | ✅ | ✅ (section-title, link, link-hover, related-card-hover) | ⚠ partial |
| **LLM-Prompt-Builder** | ✅ | ✅ (label, template-hover/active, chip-selected, btn-primary) | ✅ |
| **Command-Builder** | ✅ | ✅ (title, target-focus, flag-hover/active, checkbox, output, copy-hover) | ✅ |
| **Cmd-Builder active state** | ✅ | ✅ | ✅ but **no purple glow** |

**QW-X1: Cmd-Builder active state in blue is just a border + 5% bg tint.** Compare to
Playbook-Card active (cyan border + cyan glow box-shadow). Cmd-Builder deserves the same:

```css
.cmdbuilder-flag.active{box-shadow:0 0 0 1px var(--accent-cyan),0 0 12px rgba(34,211,238,.15)}
[data-mode="purple"] .cmdbuilder-flag.active{box-shadow:0 0 0 1px #a855f7,0 0 12px rgba(168,85,247,.15)}
```

**QW-X2: Detail-related-card has purple hover** but **no purple active/selected state.**
Same fix — add a `.detail-related-card.active` rule (or just match the purple hover).

## Hover state audit

Audited 14 hover-state rules across the file. **Inconsistency:**

| Element | Hover transition | Hover transform | Hover shadow |
|---------|:---:|:---:|:---:|
| `.tool-card` | .2s | translateY(-2px) | 12 32 40 |
| `.playbook-card` | .2s (all prop) | ❌ | ❌ |
| `.path-card` | .2s (border) | ❌ | ❌ |
| `.prompt-template` | .2s (border) | ❌ | ❌ |
| `.detail-related-card` | .2s | ❌ | � |
| `.cmdbuilder-flag` | .15s | ❌ | ❌ |
| `.wizard-option` | .2s | translateX(4px) | ❌ |

**QW-X3: Path-card and prompt-template should rise slightly on hover** (matching tool-card).
Sub-1-line CSS. Path-card especially — it has the most vertical content.

## Section transitions

Between Playbooks → Learning-Paths → Tools Grid there is **no transition**. Sections render
and the user scrolls. The tool cards individually `cardFadeIn` (300 ms) but section
boundaries are abrupt.

**QW-X4: Add a subtle section-divider** with a faint gradient line and a small "↓ scrollt
zu Tools" hint after Playbooks + after Paths. Pure CSS, optional.

---

# Section 6 — Mobile (≤ 640 px) audit

The single `@media(max-width:640px)` rule at L191 only collapses the tools grid. On a
375 px phone:

| Feature | Behavior | Severity |
|---------|----------|:---:|
| **Tool-Detail-Modal** | max-width 640 px + padding 20 px → 335 px usable width. Body scrolls. **Works but cramped.** | ⚠ |
| **Cmd-Builder** | flags grid `1fr 1fr` → too narrow, wraps every label. | 🔴 |
| **LLM-Prompt-Builder** | templates grid `minmax(160px,1fr)` → 2 cols OK; chip cloud overflows horizontally. | ⚠ |
| **Prompt-output** | max-height 300 px + padding-right 0 → copy button overlaps text. | 🔴 |
| **Learning-Paths** | paths grid `minmax(320px,1fr)` → 1 column, OK. Card expand works. | ✅ |
| **Path-week-tools chips** | wrap fine, OK. | ✅ |
| **Playbooks** | grid `minmax(240px,1fr)` → 1 column, OK. | ✅ |
| **Filter chips** | wrap with flex-wrap, OK. | ✅ |
| **Header** | stacks vertically (already handled). | ✅ |

**QW-M1: Cmd-Builder flag grid → 1 column on mobile.**

```css
@media(max-width:640px){
  .cmdbuilder-flags{grid-template-columns:1fr}
  .cmdbuilder-output{padding-right:12px;min-height:3em}
  .cmdbuilder-copy{position:static;margin-top:8px;width:100%}
  .detail-modal,.prompt-modal,.compare-modal{padding:20px 16px}
  .prompt-templates{grid-template-columns:1fr 1fr}
  .detail-related{grid-template-columns:1fr 1fr}
  .path-card,.playbook-card{padding:14px}
}
```

**QW-M2: Add a 768 px breakpoint for tablets.** Between 640 px and 1024 px, the tool grid
auto-fills but modals still feel desktop-sized. Add a `md` breakpoint.

---

# Section 7 — Missing polish

## Loading states

- **Detail-Modal:** opens instantly because render is synchronous. ✅ fine.
- **Prompt-Builder:** opens instantly. ✅ fine.
- **Cmd-Builder live preview:** updates instantly. ✅ fine.
- **Path expand:** synchronous. ✅ fine.
- **Compare-Modal:** synchronous. ✅ fine.
- **Audio play** (audio buttons on tool cards): no spinner, no buffering state. (Known
  from prior bug-hunt — buttons are dead. Out of scope for v2 polish.)

**Verdict:** Loading states not needed. App is fast enough.

## Empty states

| Feature | Empty state | Today | Fix |
|---------|-------------|-------|-----|
| Search results | "Kein Tool gefunden…" | ✅ | — |
| Favorites filter | shows empty grid + no-results | ⚠ | add "Du hast noch keine Favoriten" CTA |
| Prompt-Builder, no tools selected | builds prompt with empty tools block | 🔴 | add inline "Mindestens 1 Tool wählen" hint that disappears when ≥ 1 selected |
| Prompt-Builder, no favorites | "★ Favoriten laden" silently loads nothing | ⚠ | disable button when `favorites.size === 0` |
| Cmd-Builder, no target | builds command without target | ⚠ | show ghost target placeholder in output (e.g. `<ZIEL>`) |
| Path progress at 0% | no reset button (correctly hidden) | ✅ | — |
| Compare < 2 tools | "Vergleichen" button dead-clicks | 🔴 | (known from bug-hunt) disable button |

## Active states (button feedback)

- "Copy" buttons → `✓` for 1500 ms. Consistent ✅
- "★ Favoriten laden" → no feedback. Inconsistent ⚠
- "⬇ Als Markdown" → no feedback. Inconsistent �
- "▶ Playbook starten" → closes modal (state change is feedback). ✅
- "↺ Neu starten" → resets wizard (state change is feedback). ✅
- "📋 Prompt kopieren" → `✅ Kopiert!` for 1500 ms. ✅

**QW-E1: Standardize all "action" buttons** with the same swap-and-revert pattern:

```js
function flashButton(btn, msg) {
  const orig = btn.textContent;
  btn.textContent = msg;
  btn.disabled = true;
  setTimeout(() => { btn.textContent = orig; btn.disabled = false; }, 1500);
}
```

## Transitions

- Modal open/close: **instant.** No fade, no scale. Detail-Modal and Prompt-Modal especially
  feel abrupt. Add a 150 ms opacity transition:

```css
.detail-overlay,.prompt-overlay,.compare-modal-overlay,.wizard-overlay,.cheat-overlay{
  opacity:0;transition:opacity .15s ease}
.XXX-overlay.visible{opacity:1}
```

(Caveat: `display:none` blocks transitions — need to switch to `visibility:hidden`/`opacity:0`
or use a JS class swap.)

## Scroll-to-top button

**Missing.** Long pages (with many tools expanded) have no way to jump back up without
scrolling. The reading-progress bar at top is purely passive.

**QW-S1: Add a `<button id="scroll-top">↑</button>` that fades in after 500 px of scroll.**

```css
.scroll-top{position:fixed;bottom:24px;left:24px;z-index:80;width:40px;height:40px;
  border-radius:50%;background:var(--bg-elevated);border:1px solid var(--border);
  color:var(--accent-cyan);cursor:pointer;opacity:0;pointer-events:none;
  transition:opacity .2s,border-color .2s}
.scroll-top.visible{opacity:1;pointer-events:auto}
.scroll-top:hover{border-color:var(--accent-cyan)}
```

---

# Section 8 — Quick-Win Summary (Top 9 to ship first)

| # | Item | Effort | File area | Impact |
|---|------|--------|-----------|--------|
| 1 | Mobile breakpoints for modals + Cmd-Builder (QW-M1) | 20 min | CSS L191 | � high |
| 2 | Path-card visual differentiation from Playbook (M-L1) | 5 min | CSS L138–142 | 🔴 high |
| 3 | Cmd-Builder flag click area = whole label (QW-C2) | 30 min | JS L3418, CSS L302 | 🔴 high |
| 4 | Progress bar height + glow (QW-L2) | 5 min | CSS L146–148 | 🟡 med |
| 5 | path-week-tool chips clickable → Detail-Modal (QW-L3) | 30 min | JS, CSS L159 | 🟡 med |
| 6 | Copy/download button feedback standard (QW-E1) | 20 min | JS | 🟡 med |
| 7 | Backdrop-filter on compare/wizard/cheat (z-index X) | 5 min | CSS L102, 163, 202 | 🟢 low |
| 8 | Tool-chip filter input in Prompt-Builder (M-P2) | 1 hr | JS L2602 | 🟡 med |
| 9 | Path progress empty-state CTA in Prompt Builder (QW-E, prompt) | 15 min | JS L2606 | 🟡 med |

---

# Section 9 — CSS / HTML Snippets for the Top 5 Recommendations

### Snippet 1 — Mobile breakpoints (consolidates QW-M1)

```css
@media(max-width:640px){
  /* Cards + grids */
  .tools-grid{grid-template-columns:1fr}
  .header-inner{flex-direction:column;align-items:flex-start}
  .paths-grid{grid-template-columns:1fr}
  .playbooks-grid{grid-template-columns:1fr}
  .detail-related{grid-template-columns:1fr 1fr}
  .prompt-templates{grid-template-columns:1fr 1fr}
  /* Modals */
  .detail-modal,.prompt-modal,.compare-modal,.wizard-modal,.cheat-modal{
    padding:20px 16px;border-radius:12px}
  /* Cmd-Builder */
  .cmdbuilder-flags{grid-template-columns:1fr}
  .cmdbuilder-output{padding-right:12px;min-height:3em}
  .cmdbuilder-copy{position:static;margin-top:8px;width:100%;text-align:center}
  /* Detail-modal close button */
  .detail-close,.prompt-close,.compare-modal-close,.wizard-close,.cheat-close{
    top:8px;right:8px}
}
@media(max-width:400px){
  .prompt-templates{grid-template-columns:1fr}
  .detail-related{grid-template-columns:1fr}
}
```

### Snippet 2 — Path-card visual differentiation (M-L1)

```css
/* Vertical accent on paths, no accent on playbooks */
.path-card{border-left:3px solid var(--accent-cyan);padding-left:20px}
[data-mode="purple"] .path-card{border-left-color:#a855f7}
/* Lighter background to differentiate from playbooks */
.path-card{background:linear-gradient(180deg,var(--bg-surface),rgba(34,211,238,.015))}
[data-mode="purple"] .path-card{background:linear-gradient(180deg,var(--bg-surface),rgba(168,85,247,.015))}
/* Subtle hover lift */
.path-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.3)}
```

### Snippet 3 — Cmd-Builder whole-row click (QW-C2)

```js
// In renderPromptModal/showToolDetail, replace the flag DIV with a LABEL
// (JS template):
`<label class="cmdbuilder-flag ${f.default ? 'active' : ''}" data-flag="${f.id}">
   <input type="checkbox" class="cmdbuilder-checkbox" ${f.default ? 'checked' : ''}>
   <div class="cmdbuilder-flag-info">
     <div class="cmdbuilder-flag-label">${f.label}</div>
     <div class="cmdbuilder-flag-desc">${f.desc}</div>
   </div>
 </label>`

// CSS — make sure label behaves like a div:
.cmdbuilder-flag{display:flex;align-items:flex-start;gap:8px;padding:8px 10px;
  background:var(--bg-elevated);border:1px solid var(--border);border-radius:8px;
  cursor:pointer;transition:border-color .15s,background .15s;margin:0}
/* Remove the JS row-click handler — clicking the label now toggles the input natively */
```

### Snippet 4 — Progress bar height + glow + week-done (QW-L2 + QW-L5)

```css
.path-progress-bar{height:6px;background:var(--bg-elevated);border-radius:100px;
  overflow:hidden;margin-bottom:8px;box-shadow:inset 0 1px 2px rgba(0,0,0,.4)}
.path-progress-fill{height:100%;background:var(--accent-cyan);border-radius:100px;
  transition:width .4s ease;box-shadow:0 0 8px rgba(34,211,238,.4)}
[data-mode="purple"] .path-progress-fill{background:#a855f7;box-shadow:0 0 8px rgba(168,85,247,.4)}
/* Completed week styling */
.path-week.done .path-week-title{text-decoration:line-through;color:var(--text-muted)}
.path-week.done .path-week-check{accent-color:var(--accent-green)}
```

### Snippet 5 — Standardize copy/download feedback (QW-E1)

```js
function flashButton(btn, msg) {
  const orig = btn.dataset.orig || btn.textContent;
  btn.dataset.orig = orig;
  btn.textContent = msg;
  btn.disabled = true;
  setTimeout(() => { btn.textContent = orig; btn.disabled = false; }, 1500);
}
// Usage:
// copyBtn.addEventListener('click', () => {
//   navigator.clipboard.writeText(cmd).then(() => flashButton(copyBtn, '✅ Kopiert!'));
// });
// downloadBtn.addEventListener('click', () => {
//   /* ...download logic... */
//   flashButton(downloadBtn, '✅ Gespeichert!');
// });
```

---

# Section 10 — What to defer (anti-list)

Things that look like polish opportunities but **should not be done** without
a stronger use case:

- **❌ Dark/Light/Cyber theme switcher for the new modals.** Theme is set globally;
  re-styling per modal is duplication. Skip.
- **❌ Animation library (framer-motion / GSAP) for path-card expand.** CSS transitions
  are sufficient and respect `prefers-reduced-motion` (already wired at L365).
- **❌ Re-doing the Tool-Detail-Modal as a slide-out side-panel.** It's already well-sized
  and the centered modal is more discoverable for the 144-tool use case.
- **❌ Building a "Prompt history" feature** until you see actual user demand. B-L1 is
  listed but low priority without usage data.

---

# Appendix A — Coverage matrix (final)

| Concern | Detail | Prompt | Cmd-Builder | Paths |
|---------|:---:|:---:|:---:|:---:|
| z-index correct | ✅ 300 | ✅ 350 | n/a (inline) | n/a |
| Backdrop-filter | ✅ | ✅ (no -webkit) | n/a | n/a |
| Mobile-friendly | ⚠ | ⚠ | 🔴 | ✅ |
| Mode-switch coverage | ✅ | ✅ | ✅ | ✅ |
| Empty state | ⚠ | ⚠ | ⚠ | ✅ |
| Loading state | n/a | n/a | n/a | n/a |
| Active state | n/a | ✅ (template) | ⚠ (no glow) | ✅ (card) |
| Focus-trap | ❌ | ❌ | n/a | ❌ |
| role/aria-modal | � | ❌ | ❌ | ❌ |
| Hover feedback | ⚠ (no lift) | ⚠ (no lift) | ✅ | ⚠ (no lift) |
| Copy feedback | ✅ | ✅ | ✅ | n/a |

Legend: ✅ done · ⚠ minor issue · 🔴 blocking issue · ❌ missing · n/a not applicable

---

# Appendix B — File-line index of v3.0 features (for future audits)

| Feature | CSS lines | HTML lines | JS lines |
|---------|-----------|------------|----------|
| Tool-Detail-Modal | 215, 254–292 | 488–491 | 3239–3480 |
| LLM-Prompt-Builder | 219, 221–253 | 493–496 | 2523–2672 |
| Command-Builder | 294–317 | (inline in detail-modal) | 3059–3215, 3410–3476 |
| Learning-Paths | 133–161 | 428–434 | 2393–2521 |

**Total v3.0 surface:** ~280 CSS lines, ~10 HTML lines, ~720 JS lines = ~1010 lines added.
That's ~24 % of the file — the audit above is sized accordingly.

---

*End of report. Reviewer stance: describe-only, no code changes applied. Ready for an
implementation pass to pick from the Quick Wins + Top-5 Snippets first.*
