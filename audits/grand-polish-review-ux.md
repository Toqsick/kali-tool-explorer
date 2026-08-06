# UX Review — Forensik Tour HTML

**File reviewed:** `docs/kali-research/forensik-tour-ui.html` (1382 lines, 53 KB)
**Reviewer scope:** Design, UX, content quality, accessibility, mobile, missing features
**Review date:** 2026-08-06

---

## Summary

This is an ambitious single-file deliverable: a 25-tool, 7-phase interactive tour with sticky audio player, filter bar, mouse-tracking card effects, CRT scanlines, and a "Hörbuch-Integration" that syncs tool descriptions to audio timestamps. The dark "tape-color" palette, the `> tool-name` shell-prompt motif, and the `★ Daily Driver / Klassiker / Spezialist / Standard / Goldstandard` badges give it a strong, consistent identity. Core content quality is **high** — tool descriptions are technically accurate (sampled: guymager, dc3dd, ewfacquire, autopsy, volatility, bulk_extractor, yara, photorec, binwalk, scrounge-ntfs, chkrootkit, pdfid) and the audio `data-jump` values align with the `phaseRanges` in JS. However, the polish level is **inconsistent**: Phase 7 is essentially empty (a long paragraph + a dead-code `<audio>` element), several common UX primitives are missing (no search, no copy-to-clipboard, no back-to-top, no focus states), and the mouse-tracking radial gradient is a performance and visual-noise liability. For a "Grand Polish" pass, the priorities are: (1) fill Phase 7 with something visual, (2) add copy-to-clipboard for `tool-cmd`, (3) cut the mouse-tracking gradient or make it optional, (4) introduce a search box, (5) tighten mobile layouts below 480px.

---

## Critical Issues (must fix)

### C1. Phase 7 (Wrap-Up) is visually broken
- **Where:** Lines 1215–1229. The `<section class="phase" id="phase-7">` contains only a phase-header, a single 4-sentence `<p class="phase-summary">` (line 1225), and a dead-code `<audio preload="none" style="display:none">` element with `#t=1020`.
- **Problem:** All other phases (1–6) have a `.tools-grid` with 3–6 cards. Phase 7 has zero cards. The visual rhythm collapses — the user sees a 7th header, scrolls expecting content, finds nothing, then hits the footer. The hidden audio element is also dead code: no JS touches it.
- **Impact:** High. This is the first thing the user will notice on scroll-through.
- **Fix sketch:**
  - Remove the dead `<audio>` element.
  - Add a `<div class="tools-grid">` with 3–5 "wrap-up" cards: e.g. *Recommended starter kit* (3 tools), *Cheat sheet* (link), *Where to go next* (link to kali-forensik-overview.md), *Audio summary* (a single full-width card with a play button to jump to `data-jump="1020"`).
  - Or add a "next steps" CTA panel with the existing text, a download link for the script, and a "Back to top" anchor.

### C2. Mouse-tracking gradient (`--mx`, `--my`) is a performance and visual liability
- **Where:** CSS lines 373–380 (`.tool::after` radial-gradient), JS lines 1370–1378 (`mousemove` listener that writes `--mx`/`--my` on every event).
- **Problem:**
  - The listener fires **on every pixel of mouse movement** over 25 cards, recomputing percentages and writing two CSS custom properties per card. With `backdrop-filter: blur(20px)` on the sticky audio player and `mix-blend-mode: overlay` scanlines already on `body::before`, every `mousemove` triggers style recalc + paint + potentially a new layer.
  - The visual effect (a 4% white radial highlight following the cursor) is barely perceptible at the chosen opacity (`.04`) and reads as noise on a dark CRT theme — it doesn't telegraph useful information.
  - On touch devices the gradient sticks at the last `mousemove` position (no `mouseleave` reset).
- **Impact:** High (perf), Medium (visual).
- **Fix:** Either remove entirely (preferred) or replace with a `:focus-within`/`:hover` static highlight + a single, slower `requestAnimationFrame`-throttled handler. Reset `--mx`/`--my` on `mouseleave`.

### C3. Tool-cmd code blocks lack copy-to-clipboard
- **Where:** 25 `.tool-cmd` blocks (one per card). The block shows e.g. `dc3dd if=/dev/sda of=image.dd hash=sha256` but has no way to copy without manual selection.
- **Problem:** This is a tool-tour. Users will want to run these commands. Manual selection in a tiny monospace block on mobile is friction.
- **Impact:** High (functional).
- **Fix sketch:** Add a small `Copy` button at top-right of each `.tool-cmd` block. Use `navigator.clipboard.writeText(...)` on click, swap label to `Copied!` for 1.5s. CSS:
  ```css
  .tool-cmd{position:relative;padding-right:64px}
  .tool-cmd-copy{position:absolute;top:6px;right:6px;...}
  ```

### C4. Filter "Phase 7 (Wrap-Up)" produces an empty page when active
- **Where:** Filter bar lines 653–656, JS lines 1346–1353.
- **Problem:** Filter button shows `Wrap-Up 0`. Clicking it hides every `.phase` (because no tool has `data-phase="7"`), leaving an empty main area with only the audio player above. The user has to click "Alle" to recover.
- **Impact:** Medium-high (UX trap).
- **Fix:** Either disable the Phase 7 filter button (`pointer-events:none; opacity:.4`) until Phase 7 actually has cards, OR make Phase 7 cards carry `data-phase="7"` so they show up. The first option is cleaner since Phase 7 should arguably not be a "filterable" category at all.

### C5. No keyboard accessibility for the audio-jump buttons
- **Where:** 25 `.tool-audio-btn` elements (line 493 onwards).
- **Problem:** Buttons are 24×24 px, use only a unicode `▶` glyph (no text label), and lack `aria-label`. Screen readers announce them as "button" with no context. They are reachable via Tab but the focus state is the browser default — no visible focus ring on the dark theme. Also: there's no Esc-to-pause, no M-to-mute, no number-key (1–7) phase jump.
- **Impact:** Medium (a11y).
- **Fix:**
  - Add `aria-label="Jump to audio 1:40 for dc3dd"` to every audio button (generate from `tool-name` + `tool-audio-time`).
  - Add `:focus-visible` styles with a 2px cyan outline.
  - Add Esc to pause, M to mute, digits 1–7 to jump audio to phase start (mirror the `phaseRanges` array).

---

## Important Issues (should fix)

### I1. Phase 7's `<audio preload="none" style="display:none">` is dead code
- **Where:** Lines 1226–1228.
- **Fix:** Delete. No JS handler references it; it serves no purpose. (Already covered by C1, listed separately because it's the most obvious "code smell" on a Grand Polish review.)

### I2. Tool `tool-pop` badge is below the title instead of inline
- **Where:** Line 421 onwards. `.tool-pop` appears as a block under `.tool-head`, not next to `.tool-name`.
- **Problem:** Users scanning the grid for "is this a Daily Driver?" have to read below the title. Putting it inline (next to `#01`) makes the badge a scannable signal.
- **Fix:** Move the badge into `.tool-head` flex row, after `.tool-num`. Wrap `.tool-pop` in a flex container that doesn't push the layout.

### I3. `.meta-chip` "Yuno-Stil" and "7 Quellen live" are noise
- **Where:** Header meta-row lines 582–588.
- **Problem:** "Yuno-Stil" is a self-promotion that doesn't help a forensic analyst; "7 Quellen live" is a behind-the-scenes fact about the generation pipeline, not content. For a "Grand Polish" pass these read as generator artifacts.
- **Fix:** Replace with forensic-relevant metadata: *Kali Version 2026.2 · Live System · 25 Tools · ~18 min Audio*.

### I4. `.phase-divider` is invisible on mobile
- **Where:** Lines 323–326 + the responsive layout.
- **Problem:** At 768px the header-inner goes single-column, but the `.phase-header` (icon + title + divider) still tries to lay out with a `flex:1` divider that has a gradient `transparent` end. On narrow widths the divider collapses to ~0px and the section break becomes the only separator — which is fine — but the phase headers still feel weak compared to the page header. They lack a phase-color accent.
- **Fix:** Add a 4px top accent to each phase-header (mirror the card `::before` treatment using `--phase-color`). This unifies the visual language across header → section → card.

### I5. Phase color tokens — `--tape-4` (violet) and `--tape-7` (pink) are too similar
- **Where:** Lines 26, 29: `#a78bfa` vs `#f472b6`.
- **Problem:** At small sizes and for users with red-green color vision deficiency (deuteranopia/protanopia), violet and pink converge. They're also close in luminance.
- **Fix:** Shift `--tape-7` to something distinctly different — e.g. a teal `#14b8a6` or a true orange `#fb923c`. Run a CVD simulator (e.g. Sim Daltonism) to verify the seven colors are all distinguishable.

### I6. No visible focus state for cards, filter buttons, or filter-active border
- **Where:** Default browser focus rings, which are nearly invisible on dark themes.
- **Fix:** Add a global `:focus-visible` rule:
  ```css
  :focus-visible{outline:2px solid var(--accent-cyan);outline-offset:2px;border-radius:4px}
  ```

### I7. Filter bar counts are hardcoded and don't update
- **Where:** Lines 627, 631, 635, etc. — `Alle 25`, `Acquisition 3`, `Disk-Analyse 4`, etc.
- **Problem:** If a card is removed/added, the count drifts. There's no `aria-live` announcement when filtering. Also, after filtering, the page jumps because filter buttons wrap differently.
- **Fix:** Generate counts from `document.querySelectorAll('.tool').length` and `[data-phase="N"]` counts. Add `aria-pressed="true|false"` to filter buttons (not just `.active`).

### I8. CRT scanlines may be inaccessible for users with vestibular/sensory sensitivity
- **Where:** Lines 67–74. `body::before` with 4px stripes at 0.2 opacity, `mix-blend-mode: overlay`.
- **Problem:** `mix-blend-mode: overlay` + persistent stripes + ambient grid + 25 cards with hover gradients = a lot of competing visual texture. People with vestibular disorders or photosensitivity can find this disorienting.
- **Fix:** Wrap the scanline/ambient layers in a `@media (prefers-reduced-motion: reduce)` block (also drop the `.reveal` animation and the `blink` keyframe). Add a small UI toggle: `▢ Reduce CRT effects`.

### I9. Tool descriptions have inconsistent voice and density
- **Where:** All 25 `.tool-desc` paragraphs.
- **Problem:**
  - Some are one sentence (blkls, extundelete). Some are two sentences with technical detail (autopsy, volatility, bulk_extractor).
  - Typos/grammar: *"Helft"* in scrounge-ntfs (line 937) should be *"Hilft"*. *"allesamt"* in Phase 7 (line 1225) is awkward German. *"wechsle zu scalpel"* (line 861) is colloquial.
  - Some descriptions mention authors (Simson Garfinkel for bulk_extractor, Brian Carrier for autopsy, Victor Alvarez is missing from yara), some don't. Inconsistency.
- **Fix:** Pass for German proofreading. Standardize on: 1–2 sentences, German voice, mention author + version when known, always include the most distinctive feature.

### I10. `pdf-parser.py -o suspicious.pdf` is technically incorrect
- **Where:** Line 1182.
- **Problem:** `pdf-parser.py -o N file.pdf` dumps object N to stdout. Without `-o`, the tool prints a summary of all objects. Showing just `pdf-parser.py -o suspicious.pdf` would error.
- **Fix:** Change to `pdf-parser.py suspicious.pdf | head -100` or `pdf-parser.py -o 1 suspicious.pdf`.

### I11. Autopsy is now Python-based, not Java
- **Where:** Line 753.
- **Problem:** "Java-GUI mit Plug-in-Architektur" — Autopsy 4.x moved from Java to a Java/Python hybrid (Sleuthkit Python bindings), and current versions are predominantly Python. The "Java" description is outdated.
- **Fix:** "GUI mit Plug-in-Architektur auf Python/Sleuth-Kit-Basis. Deckt 80–90% aller Disk-Cases ab."

---

## Nice-to-have

- **N1. Search box.** With 25 tools across 7 phases, a `🔍 Suche…` filter on tag/description/name would beat the phase-only filter. Combine with the existing filter chips.
- **N2. Sort options.** Alphabetical, by audio timestamp, by pop-badge type, by complexity.
- **N3. "Back to top" button.** Sticky, appears after 600px scroll. Use `window.scrollTo({top:0, behavior:'smooth'})`.
- **N4. Reading progress indicator.** A thin 2px cyan bar at the very top of the page (above the audio player) showing scroll position. Easy: `position:fixed;top:0;height:2px;background:var(--accent-cyan);` with width set by scroll listener.
- **N5. Tooltip on `.tool-tag`** — hover shows what e.g. "NSRL" stands for (National Software Reference Library) or "EWF" (Expert Witness Format). Use `title="…"` or a tiny CSS tooltip.
- **N6. Compare two tools side-by-side.** Click a card to "pin" it, then click a second. Show their `.tool-cmd`, tags, pop-badge next to each other in a footer strip.
- **N7. Keyboard shortcut legend.** The audio player shows `Space ← →` chips, but `K` (play), `M` (mute), `1–7` (phase jump), `Esc` (pause) aren't documented anywhere.
- **N8. Print improvements.** Current `@media print` is OK but: cards become 1-column on print, so 25 cards become a 25-page document. Consider a 2-column print grid, and ensure `.tool-cmd` text wraps inside the box instead of `overflow-x:auto` (which produces horizontal scrolling in PDF print).
- **N9. "Audio transcript" expandable view per card.** Long-form text matching the audio segment — useful for accessibility (deaf/HoH users) and for searching.
- **N10. Loading state for the audio.** While `loadedmetadata` hasn't fired, the total time shows `18:30` (hardcoded in HTML) which is fine, but consider showing `--:--` until known.
- **N11. Favicon + Open Graph tags.** `og:title`, `og:description`, `og:image` for Slack/Twitter previews.
- **N12. Skip-to-content link.** First focusable element, hidden until focused: `Zum Inhalt springen`.

---

## What's Overdone

- **O1. Three web fonts** (Inter, JetBrains Mono, Sora) loaded from Google Fonts. Sora is used only for the H1 and `.phase-title`/`.player-title`. Consider system stack for body and keep JetBrains Mono + one display font. Cuts ~150 KB.
- **O2. `.tool::after` mouse-tracking gradient.** See C2.
- **O3. Multiple glow effects stacking.** `.play-btn` has `box-shadow:0 0 20px rgba(34,211,238,.3)` (line 195). `.filter-btn.active` has `0 0 16px rgba(34,211,238,.15)`. `.progress-fill::after` has a glow on hover. `.terminal-prefix::before` has `0 0 12px var(--accent-green)`. `.footer .badge::before` has another. Cumulative glow reads as a 1990s Winamp skin.
- **O4. CRT scanlines + ambient grid + reveal animation + mouse-tracking.** Four layered "this is a hacker UI" effects. Pick two.
- **O5. The `> ` prefix on every `.tool-name`** (lines 416–420). Adds shell-prompt flavor but on a 25-card grid it's repetitive visual noise. Could appear only on hover or in a code context.
- **O6. Reveal animation** at threshold 0.1 with 500ms duration. Works fine on first load, but every time the user scrolls up then back down the cards re-animate? No — `unobserve` after first reveal, so this is fine. Keep.
- **O7. The header `apt-get install kali-linux-forensics` line.** It's a nice touch but the `$ ` prefix is rendered via `::before` only on `.header-cmd`, while the `span` inside uses inline styles. Inconsistent with the rest of the codebase which uses CSS classes.

---

## What's Missing

- **M1. Tool detail modal / expand-on-click.** No way to read more about a tool. Cards are intentionally short, but there's no `Read more` or click target.
- **M2. Source links per tool.** Where does the user go to learn more? E.g. volatility → `https://www.volatilityfoundation.org/`, yara → `https://virustotal.github.io/yara/`. A subtle `↗` icon in `.tool-name` would do.
- **M3. Author / version meta per tool.** The descriptions sometimes mention them, sometimes don't. A consistent `.tool-meta` row (author, latest version, license) would make this a reference document.
- **M4. "Install" hint.** For each tool: `apt-get install <name>`. Right now only the global install command is in the header.
- **M5. Glossary popover.** "EWF", "NSRL", "EXIF", "AFF" are in tags/commands without definition. A small `<details>`-based glossary at the bottom (or hover tooltips) would help newcomers.
- **M6. Phase 7 visual elements.** See C1 — this is the most visible "missing" thing on the page.
- **M7. Audio transcript / chapter markers list.** A sidebar or above-the-fold summary listing all 25 timestamps would let users navigate without scrolling.
- **M8. Dark/Light theme toggle.** The CRT theme is gorgeous but a print/reading-friendly mode (warm white background, dark text) would broaden usability. The `@media print` already inverts — a clickable version would extend that.
- **M9. Share / permalink per tool.** `#tool-volatility` style anchor links.
- **M10. Schema.org / JSON-LD structured data.** For SEO if the page is ever indexed.
- **M11. Reduced-motion handling.** `@media (prefers-reduced-motion: reduce)` is missing entirely. The reveal animation, blink keyframe, and CRT layers should all be conditional.
- **M12. Touch device handling for `.tool::after`.** On touch the gradient stays at the last tap position because there's no mouseleave. Reset on `touchend`.

---

## Specific Recommendations

### R1. Add copy-to-clipboard to every `.tool-cmd`
- **Problem:** 25 monospace command blocks without a copy affordance force manual selection — friction for a tool reference.
- **Fix:**
  ```html
  <div class="tool-cmd">
    <button class="tool-cmd-copy" aria-label="Copy command">Copy</button>
    dc3dd if=/dev/sda of=image.dd hash=sha256
  </div>
  ```
  ```js
  document.querySelectorAll('.tool-cmd-copy').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const cmd = btn.nextSibling.textContent.trim();
      await navigator.clipboard.writeText(cmd);
      const orig = btn.textContent;
      btn.textContent = '✓';
      setTimeout(() => btn.textContent = orig, 1500);
    });
  });
  ```
- **Impact:** High.

### R2. Replace Phase 7 with a wrap-up card grid
- **Problem:** Phase 7 is text-only; the dead `<audio>` element signals unfinished work.
- **Fix:** Three cards inside a `.tools-grid`:
  1. **Starter-Set** — guymager + autopsy + photorec + yara (text-only summary card with `data-pop="starter"`)
  2. **Skript-Templates** — link to `kali-forensik-overview.md`, with a `data-jump="1020"` button to listen to the wrap-up audio
  3. **Quellen & Weiter** — links to docs / GitHub / SANS reading list
- **Impact:** High (closes the visual rhythm).

### R3. Remove or scope down the mouse-tracking gradient
- **Problem:** See C2.
- **Fix:** Delete the JS at lines 1370–1378 and the `.tool::after` rule at 373–380. Replace with a static `:hover::after {opacity:1; background: radial-gradient(circle at 50% 0%, rgba(255,255,255,.06), transparent 60%)}` — a fixed gradient that doesn't move. Or scope the effect behind `prefers-reduced-motion: no-preference` AND a coarse-pointer media query so it only runs on mouse devices.
- **Impact:** High (perf), Medium (visual).

### R4. Add a search input next to the filter bar
- **Problem:** With 25 tools, filter-by-phase is too coarse.
- **Fix:**
  ```html
  <div class="filter-bar">
    <input type="search" class="filter-search" placeholder="🔍 Suche in 25 Tools…" aria-label="Search tools">
    <!-- existing buttons -->
  </div>
  ```
  ```js
  const search = document.querySelector('.filter-search');
  search.addEventListener('input', () => {
    const q = search.value.toLowerCase().trim();
    document.querySelectorAll('.tool').forEach(t => {
      const hay = (t.querySelector('.tool-name').textContent + ' ' +
                    t.querySelector('.tool-desc').textContent + ' ' +
                    Array.from(t.querySelectorAll('.tool-tag')).map(x=>x.textContent).join(' ')).toLowerCase();
      t.style.display = (!q || hay.includes(q)) ? '' : 'none';
    });
  });
  ```
- **Impact:** Medium.

### R5. Make audio-jump buttons 44px tall with text label
- **Problem:** 24×24 px button with only a `▶` glyph is too small for touch and has no a11y label.
- **Fix:** Restructure:
  ```html
  <button class="tool-audio-btn" data-jump="100" aria-label="Audio ab 1:40 für dc3dd abspielen">
    <span class="tool-audio-icon">▶</span>
    <span class="tool-audio-time">1:40</span>
  </button>
  ```
  Style as a horizontal pill, ~32px tall, with the time visible inline so the affordance is unmistakable.
- **Impact:** Medium (a11y + UX).

### R6. Add `@media (prefers-reduced-motion: reduce)` overrides
- **Problem:** Reveal animation, blink keyframe, mouse-tracking, hover lift all run unconditionally.
- **Fix:**
  ```css
  @media (prefers-reduced-motion: reduce) {
    .reveal{opacity:1;transform:none;transition:none}
    .terminal-prefix::before{animation:none}
    .tool:hover{transform:none}
    body::before{display:none}
  }
  ```
- **Impact:** Medium (a11y).

### R7. Distinguish `--tape-7` from `--tape-4` for CVD users
- **Problem:** Violet and pink are hard to tell apart for ~8% of male readers.
- **Fix:** Change `--tape-7` to `#14b8a6` (teal) — fits the "wrap-up / completion" semantic better than pink and is hue-distinct from all other tokens.
- **Impact:** Medium (a11y + design).

### R8. Add an "Install" line under `.tool-cmd`
- **Problem:** Each tool has a `cmd` but no install hint.
- **Fix:** Below each `.tool-cmd`, add a tiny mono label: `<div class="tool-install">apt-get install <name></div>` (using the tool's slug). Keeps the visual hierarchy: install → command → description → tags.
- **Impact:** Medium.

### R9. Add chapter-marker list above the audio player
- **Problem:** To jump to a specific phase's audio, you have to scrub or click an individual tool button.
- **Fix:** A horizontal scroll list of 7 chips (one per phase) below the audio player: `1 Acquisition · 2 Disk · 3 Carving · 4 Memory · 5 Malware · 6 Reporting · 7 Wrap`. Each chip has `data-jump` set to the phase's start.
- **Impact:** Medium.

### R10. Back-to-top button + reading progress bar
- **Problem:** No wayfinding after scrolling past the first phase.
- **Fix:** Two CSS-only additions:
  - 2px fixed-top progress bar (width = scroll %, accent-cyan).
  - Bottom-right FAB that appears after `window.scrollY > 600`, scrolls to top on click.
- **Impact:** Medium.

### R11. Inline-correct the German prose
- **Specific fixes:**
  - Line 937: "Helft" → "Hilft"
  - Line 861: "Wenn foremost zu langsam ist, wechsle zu scalpel." → "Wenn foremost zu langsam ist, wechsle zu scalpel." → "Wer foremost zu langsam findet, wechselt zu scalpel." (drop colloquial imperative)
  - Line 1225: "weil allesamt Open Source" → "weil alle Open Source sind"
  - Add Oxford comma consistency.
- **Impact:** Low (prose polish).

### R12. Add `:focus-visible` outline globally
- **Problem:** Dark theme hides default focus rings.
- **Fix:** One rule:
  ```css
  :focus-visible{outline:2px solid var(--accent-cyan);outline-offset:3px;border-radius:4px}
  ```
- **Impact:** Medium (a11y).

---

## Mobile / Responsive Audit (375 / 768 / 1024)

### 375px (iPhone SE)
- ✅ `.header-inner` collapses to 1 column (`max-width:768px` rule).
- ✅ `.tools-grid` is 1 column.
- ⚠️ The audio player `.progress-wrap` is `order:99; flex-basis:100%` — it does wrap correctly to a new row, but the player-info column sits next to the play button while shortcuts and progress stack underneath. Visually crowded. Consider a 3-row layout: row 1 = play + title, row 2 = progress, row 3 = shortcuts + time.
- ⚠️ `.meta-chip` row wraps to 5 lines (5 chips × ~150px each at 375px width). Could be 2 rows max.
- ⚠️ `.phase-header` flex (icon | title | divider) — divider collapses to 0, fine. But the `flex:1` wrapper inside the `<div style="flex:1">` is duplicated; only one flex container needed.

### 768px (iPad portrait)
- ✅ Cards switch to 1 column at ≤768px.
- ⚠️ The header `.header-cmd` block is shown at min-width 280px on a 768px viewport — fits. On 768px exactly it works; on 769px the header-inner goes back to 2-column and the cmd block sits next to title — could feel cramped.

### 1024px (iPad landscape / small laptop)
- ✅ Cards in 3-column grid (`repeat(auto-fill,minmax(320px,1fr))` at 1280px max-width → 4 cols at 1024px viewport considering padding).
- ✅ All audio player elements in a single row.

### General mobile issues
- **Touch targets** for `.tool-audio-btn` are 24×24 px — under the 44×44 px iOS guideline. See R5.
- **`<input>` would be needed for the search box** (R4) — currently no form elements, so the keyboard shortcut handler's `if (e.target.tagName === 'INPUT') return;` is dead defense.
- **Print preview at A4** stacks cards 1-per-row → 25 pages. See N8.

---

## Content Quality Spot-Checks

| # | Tool | Verdict | Notes |
|---|------|---------|-------|
| 01 | guymager | ✅ Accurate | Multi-hash + E01/AFF correct; v0.8.13 reasonable. |
| 02 | dc3dd | ✅ Accurate | DoD Cyber Crime Center origin. |
| 03 | ewfacquire | ✅ Accurate | Court-admissibility framing correct. |
| 04 | autopsy | ⚠️ Outdated | "Java-GUI" is no longer true (Python-based since 4.x). See I11. |
| 05 | sleuthkit | ✅ Accurate | "Engine unter Autopsy" correct. |
| 10 | photorec | ✅ Accurate | Testdisk pairing correct. |
| 13 | scrounge-ntfs | ✅ Accurate (typo) | "Helft" → "Hilft". |
| 14 | volatility | ✅ Accurate | v3, Python, plugins all correct. |
| 15 | bulk_extractor | ✅ Accurate | Simson Garfinkel authorship correct. |
| 16 | binwalk | ✅ Accurate | SquashFS/CramFS examples correct. |
| 18 | yara | ✅ Mostly | "von VirusTotal" — created by Victor Alvarez at VirusTotal. OK. |
| 21 | chkrootkit | ✅ Accurate | "älter, schnelle Live-Triage" correct. |
| 23 | pdfid | ✅ Accurate | Didier Stevens authorship correct. |
| 24 | pdf-parser | ❌ Command bug | `-o` without object number errors. See I10. |
| 25 | obsidian | ⚠️ Out of scope | Obsidian isn't a Kali forensics tool — it's the user's note-taking app. The inclusion feels like a self-reference to the author's workflow. Consider replacing with `cherrytree` or `casefile` (true Kali tools) or moving to a "Where I keep my notes" footer callout. |

**Pop-badge taxonomy** (4 visible types + 1 special):
- `★ Daily Driver` (green) — used 5×: guymager, autopsy, sleuthkit, bulk_extractor, photorec, yara, obsidian (actually 7×). Most common.
- `★ Goldstandard` (green) — volatility only. Visually identical to Daily Driver except for the word. **Redundant** — consolidate or differentiate by color.
- `Klassiker` (yellow) — dc3dd, foremost.
- `Spezialist` (amber) — ewfacquire, scalpel, extundelete, safecopy, scrounge-ntfs, missidentify, ssdeep, pdf-parser. Most common after Daily Driver.
- `Standard` (cyan) — blkls, tsk_recover, binwalk, hashdeep, chkrootkit, rkhunter, pdfid.

The taxonomy is *understandable* but the visual distinction between "Daily Driver" and "Goldstandard" is zero. Recommendation: drop one of them, OR make Goldstandard a different color (e.g. gold/amber for volatility as the canonical example).

---

## Priority Matrix

| ID | Issue | Impact | Effort | Priority |
|----|-------|--------|--------|----------|
| C1 | Phase 7 visually broken | High | Medium | **P0** |
| C2 | Mouse-tracking gradient perf | High | Low | **P0** |
| C3 | No copy-to-clipboard | High | Low | **P0** |
| C4 | Phase 7 filter shows empty | Med-High | Low | **P0** |
| C5 | Audio-jump a11y | Medium | Low | **P0** |
| I4 | Phase headers lack phase-color | Medium | Low | P1 |
| I5 | tape-4 vs tape-7 too similar | Medium | Low | P1 |
| I11 | Autopsy "Java" outdated | Medium | Trivial | P1 |
| I10 | pdf-parser command wrong | Medium | Trivial | P1 |
| R4 | Search input | Medium | Low | P1 |
| R6 | prefers-reduced-motion | Medium | Low | P1 |
| R12 | :focus-visible | Medium | Trivial | P1 |
| I9 | German proofreading | Low | Low | P2 |
| N8 | Print 2-column | Low | Low | P3 |
| N1 | Sort options | Low | Medium | P3 |
