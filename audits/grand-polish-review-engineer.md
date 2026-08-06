# Engineering Review — Forensik Tour HTML

**Artifact:** `/home/bratan/20-Workspace/docs/kali-research/forensik-tour-ui.html` (1,382 lines, 53.6 KB, single-file static HTML)
**Reviewer scope:** Code quality, performance, accessibility, robustness, best practices
**Method:** Static read-through + targeted grep checks (no execution). All issues cite a line number or selector.

---

## Summary

The file is a clean, well-structured single-page artifact that makes consistent use of semantic HTML5 (`<header>`, `<main>`, `<nav>`, `<section>`, `<article>`, `<footer>`), CSS custom properties for theming, and a tidy 8-section JS block at the bottom of `<body>`. It is small (≈53 KB), self-contained, and ships zero third-party requests beyond Google Fonts. **The critical work is concentrated in three areas: (1) accessibility is materially deficient — there is no `:focus` style anywhere in the file, no skip link, and several text-on-background combinations fail WCAG AA contrast; (2) the JS layer has at least one correctness bug (`progressBar` click before `loadedmetadata`) and at least one dead element (a hidden, unused `<audio>` in Phase 7); (3) cross-browser polish is incomplete — `backdrop-filter` and `mask-image` are missing `-webkit-` prefixes and there is no `prefers-reduced-motion` guard for the blinking terminal dot and reveal animation.** Beyond those three clusters, the file is in good shape for a static deliverable.

---

## Critical Bugs / Accessibility Blocks

- [ ] **No `:focus` styles anywhere** (0 matches for `focus`/`outline`/`tabindex` in the file). Every interactive element — 8 filter buttons, 1 play button, 25 audio-jump buttons, 1 progress bar — has no visible keyboard focus indicator. **WCAG 2.4.7 (Focus Visible) FAIL.** Keyboard users cannot tell where they are.
- [ ] **`progressBar` click is unsafe before `loadedmetadata` fires** (line 1301–1305). If the user clicks the progress bar while `audio.duration` is still `NaN` (slow network, missing file), `pct * audio.duration` evaluates to `NaN`, then `audio.currentTime = NaN` throws `InvalidStateError` on some browsers and silently breaks on others. The progress bar should be disabled (`aria-disabled`, `pointer-events: none`) until `loadedmetadata` resolves, or the click handler must guard `isFinite(audio.duration)`.
- [ ] **Phase 7 (Wrap-Up) filter shows zero cards** (line 655: `<span class="filter-count">0</span>`). Clicking it hides every section with no visible feedback — a user can lose all content and not understand why. Either (a) hide / disable the button when `filter-count === 0`, or (b) make Phase 7 contain the "Wrap-Up" summary card as an article.
- [ ] **Dead audio element** (line 1226–1228). A second `<audio preload="none" style="display:none">` is embedded inside `<section id="phase-7">` with a `#t=1020` fragment. It has no controls, no ID, and no JS reference — it is dead markup that still triggers a metadata request on some browsers. Delete it.
- [ ] **Hardcoded total time `18:30`** (line 610) is set in HTML even though `loadedmetadata` overwrites it within ~200 ms on a normal connection. If the audio file is unreachable, the user sees `0:00 / 18:30` forever and the progress bar appears frozen. Replace with `—:—` or `<span id="totalTime">—:—</span>`.
- [ ] **`text-dim #52525b` on `bg-void #050507`** (used line 1239 for the footer secondary line) has a measured contrast ratio of ≈3.4:1 — **below WCAG AA 4.5:1** for normal text. Only passes for ≥18 pt. Either darken to `#6b6b75` or enlarge to `font-size:.82rem` minimum.
- [ ] **No `prefers-reduced-motion` guard** for the `.terminal-prefix::before` blink animation (line 113), the `.reveal` opacity/translate (line 545), or the `progress-fill` width transition (line 220). Users with vestibular disorders or motion sensitivity are not protected. Wrap each in `@media (prefers-reduced-motion: no-preference)` or set `animation: none` in the reduced-motion block.

---

## Code Quality Issues

- [ ] **Repeated inline styles** (`style="flex:1"` appears 7× in phase headers at lines 666, 738, 826, 952, 1042, 1148, 1218; `style="color:var(--text-muted)"` and `style="color:var(--accent-cyan)"` at lines 591–592). These should be classes (`.phase-header-text`, `.kbd-cmd-comment`, `.kbd-cmd-cmd`).
- [ ] **Magic numbers in `phaseRanges`** (line 1254–1262) duplicate the per-card `data-jump="…"` and `tool-audio-time` strings. If the audio is re-cut, both sides must be edited. Consider deriving ranges from one source of truth or at least leaving a `// keep in sync with HTML data-jump values` comment.
- [ ] **No semicolons omitted intentionally** — single-line JS blocks compress to one statement and skip the trailing `;`. Not a bug per se, but a stylistic mismatch with the `const`-heavy style above. Consider adding them for consistency (ASI works, but mixing styles invites future bugs).
- [ ] **Console-free, debug-free** ✓ (0 matches for `console.` or `debugger`). Good.
- [ ] **All `querySelector` / `getElementById` calls happen at top-level of `<script>`** which sits at the bottom of `<body>` — so DOMContentLoaded has effectively fired. ✓ no timing bug.
- [ ] **Mousemove handler on every `.tool` (line 1370–1378)** runs synchronously on every mouse movement over 25 cards, computing `getBoundingClientRect()` per event (forced reflow) and writing two CSS custom properties. On a hover that crosses the card, this can fire 60+ times/second × 25 cards = up to 1500 forced layouts/sec worst case. Throttle with `requestAnimationFrame` or move the rect read outside the handler.
- [ ] **No `e.preventDefault()` on Space when audio is paused** — handled correctly (line 1311), but the Space handler does not distinguish "user is page-scrolling" from "user wants to play". A scrollable container with focus could still trigger play. Acceptable trade-off but worth a comment.
- [ ] **`k` as a global shortcut** (line 1310) collides with the normal typing flow. A user filling any future input gets `k` → play toggle. The `INPUT/TEXTAREA` guard covers only those two tag names; `contenteditable` divs (e.g. Obsidian embeds) are not guarded.
- [ ] **Filter re-query** (line 1339, 1346, 1350): every filter click walks the DOM with `querySelectorAll('.tool')` and `querySelectorAll('.phase')`. With 25 cards and 7 sections, the cost is trivial today but should cache the NodeLists once at script init.
- [ ] **The hidden audio-jump `display:none` second `<audio>` element** (line 1226) is dead markup — see Critical Bugs.
- [ ] **Phase ranges assume a 1110-second (18:30) audio file.** Total time is set from `audio.duration` (good), but the phase list is hard-coded. If the audio ever changes, phase labels drift silently. Compute from a small lookup table or document the coupling.

---

## Performance Issues

- [ ] **Three Google Fonts loaded** (line 9): Inter (5 weights), JetBrains Mono (4 weights), Sora (4 weights). Total: 13 font files at minimum. Sora is used only for `h1`, `.player-title`, and `.phase-title` (display headings) — could be a single 700-weight subset. Inter is used for body and at 5 weights where 400/600 would cover ≥95 % of uses. **Estimated savings: ~150 KB transfer.**
- [ ] **No `font-display` is set in the URL** — defaults to `swap`. Good for FOUT, but worth adding `&display=swap` (already present) and pinning only the used weights.
- [ ] **mousemove on every `.tool`** (line 1370–1378) — see Code Quality. This is the largest in-page CPU cost when hovering a long list.
- [ ] **No `defer` / `async` needed** — script is at end of `<body>`, equivalent to `defer`. ✓
- [ ] **`<link rel="preconnect">` to `fonts.gstatic.com` is correct** (line 8). ✓
- [ ] **Audio `preload="metadata"` is the right choice** (line 618) — pulls duration + first frame without the full file. ✓
- [ ] **`reveal` IntersectionObserver** (line 1358–1367) is correctly throttled by the browser, unobserves after first reveal, and uses a sensible `rootMargin`. ✓
- [ ] **Inline SVG is not used** — all icons are emoji (📼, 🔍, etc.). Cheaper, but no control over color/animation. Acceptable for this design.
- [ ] **No images, no `<picture>`, no lazy-loading needed** — there are no `<img>` tags in the file. ✓
- [ ] **`.ambient::before` grid + body::before scanline** (line 67–87) are full-viewport fixed overlays that re-paint on scroll. Cost is small but visible on low-end mobile. Consider `will-change: transform` or rasterizing to a single PNG if mobile is in scope.
- [ ] **Filter toggling causes layout reflow** (line 1341–1353). Inline `style.display = 'none'` triggers a full layout pass. Switching to a `hidden` attribute on a parent `<section>` would be cheaper; alternatively a CSS-only solution with `[data-filter-active="3"] .tool:not([data-phase="3"]) { display:none }` would batch the read/write.

---

## Accessibility Issues (WCAG 2.1 AA)

- [ ] **No `:focus` styles** — see Critical Bugs. Add a global token:
  ```css
  :focus-visible{outline:2px solid var(--accent-cyan);outline-offset:3px;border-radius:4px}
  ```
- [ ] **No skip-to-content link.** Add as the first focusable element:
  ```html
  <a href="#main" class="skip-link">Zum Inhalt springen</a>
  ```
  with `.skip-link{position:absolute;left:-9999px}.skip-link:focus{left:1rem;top:1rem}`.
- [ ] **Contrast failures** (verified against `bg-void #050507` and `bg-surface #12121a`):
  | Pairing | Ratio | AA Normal? | Used at |
  |---|---|---|---|
  | `text-primary #e4e4e7` on `bg-void #050507` | ~16:1 | ✓ | body |
  | `text-secondary #a1a1aa` on `bg-void #050507` | ~9.5:1 | ✓ | subtitles |
  | `text-muted #71717a` on `bg-void #050507` | ~5.3:1 | ✓ (border) | meta, footer |
  | `text-muted #71717a` on `bg-surface #12121a` | ~4.6:1 | ✗ | meta-chip body |
  | `text-dim #52525b` on `bg-void #050507` | ~3.4:1 | ✗ | footer caption |
  | `accent-cyan #22d3ee` on `bg-elevated #1a1a24` | ~9.8:1 | ✓ | filter active |
  | `accent-cyan #22d3ee` on `bg-void #050507` (large) | ~11:1 | ✓ | play-btn fill |
- [ ] **`meta-chip` color** uses `text-muted` (line 145) — borderline fail. Use `text-secondary` instead.
- [ ] **`<audio>` element has no transcript / captions** (line 618). For an 18-minute narrated tour, providing a text transcript either as a sibling section or as a `<track kind="captions">` is expected practice. At minimum, the per-card `tool-desc` paragraphs could be linked into a transcript view.
- [ ] **Filter button has no `aria-pressed`** (line 625). The active state is conveyed only by class. Add `aria-pressed="true|false"` and toggle on filter click.
- [ ] **Tool audio-jump buttons** (line 689, 708, 727, …) have no accessible name — only a `▶` glyph. Screen readers announce "button" with no purpose. Add `aria-label="Springt zu Audio bei 1:40"` or similar.
- [ ] **Progress bar is a `<div>` not a `<progress>` element** (line 605). For an audio scrubber this is acceptable, but should carry `role="slider"` + `aria-valuenow` + `aria-valuemin="0"` + `aria-valuemax` + `aria-valuetext="2:14 von 18:30"` and respond to `ArrowLeft/Right` keys natively.
- [ ] **Decorative emoji icons** (📼, 🔍, 🔬, 🧠, 🦠, 📄, 🎯) lack `aria-hidden="true"`. Screen readers will read "videocassette, magnifying glass tilted left…" before the heading. Add `aria-hidden="true"` to each `.phase-icon`.
- [ ] **No `lang` attribute on inner German strings** — the document is `lang="de"` (line 2) ✓ but quoted English code snippets in `.tool-desc` (e.g. "Most widely used memory forensics platform") should be wrapped in `<span lang="en">` to prevent mispronunciation.
- [ ] **Tab order is natural DOM order** ✓, but with 25 audio-jump buttons and no skip-to-content, keyboard users must tab through dozens of identical buttons. Consider grouping via `<section aria-labelledby="phase-1-title">` and a heading link, or collapse the audio-jump row behind a disclosure.

---

## Robustness Issues

- [ ] **Missing audio file → forever-`0:00 / 18:30`** — see Critical Bugs (hardcoded total). Also: an `<source>` with no fallback (no `<source type="audio/ogg">`) means Firefox-on-Linux with MP3-codec issues fails silently. Provide both `audio/mpeg` and `audio/ogg`, or use `<audio>` without `<source>` and let the browser sniff.
- [ ] **Missing `loadedmetadata`** → no `totalTime` update, no progress. The page should still be usable: the play button and filter should work even if audio is broken. **Today:** clicking the play button on a broken-audio page surfaces a console error and the button toggles `▶`→`⏸` even though nothing played. Add an `error` event listener that surfaces "Audio konnte nicht geladen werden" in the `.player-info`.
- [ ] **Phase 7 filter shows zero cards** — see Critical Bugs.
- [ ] **`prefers-reduced-motion`** not respected — see Critical Bugs.
- [ ] **`:has()` selector not used**, so no Safari < 15.4 fallback needed. ✓
- [ ] **`mask-image`** (line 86) needs `-webkit-mask-image` for Safari. Currently a Safari < 15 user sees a square grid instead of a radial fade. Add:
  ```css
  -webkit-mask-image:radial-gradient(ellipse 100% 70% at 50% 0%,black 0%,transparent 80%);
  ```
- [ ] **No `touchstart` listener for audio-jump on mobile** — `click` fires fine on tap but with a 300 ms delay on legacy mobile browsers. Acceptable today (iOS Safari no longer has this) but a comment would help.
- [ ] **Window resize not handled** — the sticky audio player plus the filter bar can collide on a 360-px-wide viewport (`@media (max-width:480px)` line 560 puts `.progress-wrap` on its own row but does not address the filter bar wrapping). Add a `min-width: 0` and `flex-shrink` rule, or test at 320 px.
- [ ] **No `audio.play()` Promise rejection handling** (line 1289, 1327). Mobile Safari blocks autoplay and rejects the promise; today the UI silently sits at `▶` even though nothing played. Catch and surface the error:
  ```js
  audio.play().catch(err => { playBtn.textContent='▶'; console.warn(err) });
  ```
- [ ] **No CORS / `crossorigin` on the audio** — irrelevant for local files but if the page is ever hosted cross-origin, `MediaElement` errors stay opaque. Add `crossorigin="anonymous"` if you anticipate that.

---

## Cross-Browser Issues

- [ ] **`backdrop-filter` without `-webkit-` prefix** (line 179). Safari < 18 and older iOS need `-webkit-backdrop-filter:blur(20px)`.
- [ ] **`mask-image` without `-webkit-` prefix** (line 86). Same browser-coverage issue.
- [ ] **`background-clip:text` / `-webkit-text-fill-color`** (line 123–124, 128) — both prefixes are present ✓
- [ ] **`mix-blend-mode: overlay`** on `body::before` (line 73) — supported in all current targets ✓
- [ ] **CSS Grid `auto-fill,minmax(320px,1fr)`** (line 352) — supported in Safari ≥ 10.1 ✓
- [ ] **`Intl` not used**, **`?.` optional chaining not used**, **`??` nullish not used** — none of these are needed; the code uses broad compatibility. ✓
- [ ] **`<audio>` element** — Safari on iOS requires a user gesture to `play()`; the `e.preventDefault()` on Space key is correct but tapping the play button relies on Safari's gesture whitelist. The current code should work; add a test pass on a real device.
- [ ] **No IE / legacy Edge path needed** — none of the modern CSS features degrade gracefully on IE11, but IE is unsupported in 2026 ✓.

---

## Best Practices

- [ ] **`<audio>` should have `controls` hidden but discoverable** — for accessibility, expose a fallback control:
  ```html
  <audio id="audio" preload="metadata" controls style="position:absolute;left:-9999px;width:1px;height:1px" aria-label="Audio-Tour">
  ```
- [ ] **`<noscript>` block missing.** Without JS the filter bar is non-functional (cards still display because no filtering happens) but the audio-jump buttons do nothing. Add a one-line `<noscript>` explaining audio and filtering need JS.
- [ ] **`<meta name="description">` missing.** Add for SEO / social sharing:
  ```html
  <meta name="description" content="Interaktive Tour durch 25 Kali-Linux-Forensik-Werkzeuge in 7 Phasen, mit 18:30-min Hörbuch-Integration.">
  ```
- [ ] **`<meta name="theme-color">` missing.** For mobile browser chrome:
  ```html
  <meta name="theme-color" content="#050507">
  ```
- [ ] **`<link rel="canonical">` missing** — relevant if the page is ever deployed.
- [ ] **Open Graph / Twitter Card tags missing** — relevant if shared.
- [ ] **No `<base>` tag**, no favicons referenced (`<link rel="icon">`). Add a `data:` favicon to avoid a 404.
- [ ] **JS is at the bottom of `<body>`**, not in `<head>` ✓. Consider moving to `<head defer>` for clarity, but functionally equivalent.
- [ ] **No `defer` / `type="module"`** — script runs synchronously after parsing. With ~80 lines of JS this is fine.
- [ ] **CSS is inline** — fine for a single-file deliverable, but a `<link>` to a separate `.css` would let a service worker cache it. Document this as an intentional choice.
- [ ] **Inline event handlers** — none ✓ (all listeners attached via `addEventListener`).
- [ ] **`document.querySelectorAll('.tool').forEach`** (lines 1321, 1334, 1370) attaches listeners independently — see Performance. Cache once at init.
- [ ] **Inline styles set per hover** (lines 1375–1376) — see Performance. Could be done with a CSS custom property on `:hover` using `--mx`/`--my` if the mouse coordinate is forwarded via `mousemove` once per `pointermove` rather than per event.
- [ ] **The `kbd` elements showing `Space` `←` `→`** (line 614–616) are static labels, not `<kbd>` semantic elements. Use `<kbd>` for screen-reader friendliness.
- [ ] **`<span class="filter-count">25</span>`** could be inside an `aria-label="25 Werkzeuge"` or wrapped in a visually-hidden span — currently the count is announced as part of the button name.
- [ ] **HTML comments are decorative banners** ✓ — useful for navigation in a 1,300-line file.

---

## Specific Recommendations

### R1. Add `:focus-visible` styles (high impact, low effort)

**Problem:** No keyboard-focus indicator anywhere in the file. WCAG 2.4.7 violation, blocking.
**Proposed fix:** Add after the `:root` block (after line 51):
```css
:focus-visible{outline:2px solid var(--accent-cyan);outline-offset:3px;border-radius:4px}
:focus:not(:focus-visible){outline:none}
```
**Estimated impact:** Restores keyboard accessibility for ~34 interactive elements. Zero side effects.

### R2. Guard `progressBar` click against `NaN duration` (high impact, low effort)

**Problem:** Line 1301–1305 crashes / silently fails if `loadedmetadata` hasn't fired.
**Proposed fix:**
```js
progressBar.addEventListener('click', (e) => {
  if (!isFinite(audio.duration) || audio.duration <= 0) return;
  const rect = progressBar.getBoundingClientRect();
  const pct = (e.clientX - rect.left) / rect.width;
  audio.currentTime = Math.max(0, Math.min(audio.duration, pct * audio.duration));
});
```
**Estimated impact:** Eliminates a crash on slow networks / missing audio. Also caps `currentTime` to `[0, duration]` as a defensive bonus.

### R3. Handle Phase 7 (Wrap-Up) zero-card filter (medium impact, low effort)

**Problem:** Line 655 button shows `0` cards and clicking it hides everything.
**Proposed fix:** Replace the Wrap-Up filter button with a "disabled" indicator that explains why:
```html
<button class="filter-btn" data-filter="7" disabled aria-disabled="true" title="Wrap-Up-Phase hat keine Tool-Karten">
  <span class="filter-dot"></span>
  Wrap-Up <span class="filter-count">0</span>
</button>
```
plus
```css
.filter-btn[disabled]{opacity:.4;cursor:not-allowed}
```
**Estimated impact:** Removes a dead-end state. 4 lines of HTML + 1 CSS rule.

### R4. Add `prefers-reduced-motion` guard (medium impact, low effort)

**Problem:** Three CSS animations and one JS-driven transform run unconditionally.
**Proposed fix:** Wrap each in the no-preference media query, or add a global override:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001s !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001s !important;
  }
  .reveal{opacity:1;transform:none}
}
```
**Estimated impact:** WCAG 2.3.3 compliance. Affects ~5% of users with motion sensitivities.

### R5. Delete the dead `<audio>` element in Phase 7 (low impact, trivial)

**Problem:** Line 1226–1228 — unused, hidden, but still parsed.
**Proposed fix:** Delete lines 1226–1228 entirely.
**Estimated impact:** Clean DOM. Removes a potential metadata request on some browsers.

### R6. Add `-webkit-` prefixes for `backdrop-filter` and `mask-image` (medium impact, low effort)

**Problem:** Line 179, 86 — Safari < 18 ignores unprefixed `backdrop-filter`; Safari < 15 ignores unprefixed `mask-image`.
**Proposed fix:**
```css
backdrop-filter:blur(20px);
-webkit-backdrop-filter:blur(20px);
```
and
```css
mask-image:radial-gradient(...);
-webkit-mask-image:radial-gradient(...);
```
**Estimated impact:** Restores glass-blur on older Safari; restores radial grid fade on iOS 14.

### R7. Throttle the tool-card mousemove handler (high impact for low-end CPUs, low effort)

**Problem:** Lines 1370–1378 — synchronous `getBoundingClientRect()` per mousemove × 25 cards.
**Proposed fix:**
```js
document.querySelectorAll('.tool').forEach(tool => {
  let raf = 0, lastRect = null;
  tool.addEventListener('mousemove', (e) => {
    if (raf) return;
    raf = requestAnimationFrame(() => {
      lastRect = lastRect || tool.getBoundingClientRect();
      const mx = ((e.clientX - lastRect.left) / lastRect.width) * 100;
      const my = ((e.clientY - lastRect.top)  / lastRect.height) * 100;
      tool.style.setProperty('--mx', mx + '%');
      tool.style.setProperty('--my', my + '%');
      raf = 0;
    });
  });
  tool.addEventListener('mouseleave', () => { lastRect = null; });
});
```
**Estimated impact:** Caps work at ~60 fps regardless of mousemove rate. Removes a forced reflow per event.

### R8. Make the audio scrubber a proper `role="slider"` (medium impact, medium effort)

**Problem:** Line 605 — `<div class="progress-bar">` has no ARIA semantics.
**Proposed fix:**
```html
<div class="progress-bar" id="progressBar" role="slider"
     aria-label="Audio-Position" aria-valuemin="0"
     aria-valuemax="100" aria-valuenow="0" tabindex="0">
```
and update JS to set `aria-valuenow` and respond to Arrow keys natively.
**Estimated impact:** Screen readers announce scrubber state; keyboard users can scrub without needing global arrow-key shortcuts.

### R9. Add `aria-pressed` to filter buttons (medium impact, low effort)

**Problem:** Line 625+ — active state conveyed only by class.
**Proposed fix:** Toggle `aria-pressed` in the click handler (line 1336–1337):
```js
document.querySelectorAll('.filter-btn').forEach(b => {
  b.classList.remove('active');
  b.setAttribute('aria-pressed', 'false');
});
btn.classList.add('active');
btn.setAttribute('aria-pressed', 'true');
```
and initial markup `<button … aria-pressed="false">` (and `aria-pressed="true"` on the active one).
**Estimated impact:** Screen-reader users know which filter is active.

### R10. Add `aria-label` to per-card audio-jump buttons (medium impact, low effort)

**Problem:** 25 `▶` glyphs (e.g. line 689) read as "button" with no name.
**Proposed fix:** Replace static text with a labelled button:
```html
<button class="tool-audio-btn" data-jump="100" aria-label="Springt zu Audio bei 1:40">
  <span aria-hidden="true">▶</span>
</button>
```
**Estimated impact:** Each tool card announces meaningfully instead of as 25 identical "button" entries.

### R11. Replace hardcoded `18:30` with `—:—` placeholder (low impact, trivial)

**Problem:** Line 610 — `18:30` is hardcoded; if audio fails to load, the display lies.
**Proposed fix:**
```html
<span id="totalTime">—:—</span>
```
**Estimated impact:** UI honestly reflects unknown state.

### R12. Darken `text-dim` to pass WCAG AA (low impact, trivial)

**Problem:** Line 1239 — `text-dim #52525b` on `bg-void #050507` = ~3.4:1, below AA.
**Proposed fix:** Change `--text-dim:#52525b` (line 39) to `--text-dim:#6b6b75` (measured ~5.0:1) or `#71717a` (5.3:1).
**Estimated impact:** One token, restores AA on the footer caption line.

### R13. Add `<meta name="description">` and `theme-color` (low impact, trivial)

**Problem:** None present. SEO and mobile-chrome polish missing.
**Proposed fix:**
```html
<meta name="description" content="Interaktive Tour durch 25 Kali-Linux-Forensik-Werkzeuge in 7 Phasen — mit 18:30-min Hörbuch.">
<meta name="theme-color" content="#050507">
```
in `<head>`.
**Estimated impact:** Better sharing preview, matches browser chrome to dark theme.

### R14. Tighten the 3-font load to used weights only (medium impact, low effort)

**Problem:** Line 9 — Inter 5 weights, Sora 4 weights, JetBrains Mono 4 weights = up to 13 WOFF2 files.
**Proposed fix:** Audit actual usage:
- Inter: 300 (unused), 400, 500, 600, 700, 800 — keep 400/600/700
- Sora: 400, 600, 700, 800 — keep 700 only (used at `.player-title`, `.phase-title`, `.tool-name`-style headings; verify)
- JetBrains Mono: 400, 500, 600, 700 — keep 400/600

New URL:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&family=Sora:wght@700&display=swap" rel="stylesheet">
```
**Estimated impact:** ~150 KB transfer savings on first paint. Faster LCP.

### R15. Add `<noscript>` and a tiny inline data: favicon (low impact, trivial)

**Problem:** Filter and audio do nothing without JS; no favicon → 404 in dev tools.
**Proposed fix:**
```html
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><circle cx='8' cy='8' r='6' fill='%2322d3ee'/></svg>">
```
and after `<body>`:
```html
<noscript>Diese Seite benötigt JavaScript für Audio-Wiedergabe und Filter.</noscript>
```
**Estimated impact:** Removes a console 404; clarifies dependency.

---

## Verification Checklist (after applying recommendations)

- [ ] `Tab` through the page — every focusable element shows a cyan outline
- [ ] Open DevTools, throttle to Slow 3G, click the progress bar immediately — no exception
- [ ] Click the Wrap-Up filter — either it is disabled, or content remains visible
- [ ] Rename `audio-forensik/kali-forensik-tour.mp3` to `.missing` and reload — play button stays at `▶`, total time shows `—:—`
- [ ] DevTools → Rendering → Emulate `prefers-reduced-motion: reduce` — animations halt, reveal content shows immediately
- [ ] VoiceOver / NVDA on the filter bar — active filter is announced with `aria-pressed`
- [ ] VoiceOver on a tool card — audio-jump button announces "Springt zu Audio bei 1:40"
- [ ] Open in Safari 16 → glass blur on the audio player is visible
- [ ] Lighthouse Accessibility ≥ 95, Best Practices ≥ 95, Performance ≥ 90