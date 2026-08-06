# Bug-Hunt Review — Kali Explorer v3.0

**File:** `docs/kali-research/forensik-explorer.html`
**Lines:** 4133 (single-file HTML application)
**Date:** 2026-08-06
**Scope:** New v3.0 features — Tool-Detail-Modal, LLM-Prompt-Builder, Command-Builder, Learning-Paths — plus cross-feature interactions and TDZ review.

---

## TL;DR

- **8 Critical bugs** (functional regressions visible to users).
- **5 Important bugs** (UX degradation, edge-case confusion).
- **6 Minor issues** (dead data, missing coverage).
- **TDZ check: PASS** — all `const`/`let` for v3.0 state are declared before the functions that consume them, and `switchMode` runs only via `DOMContentLoaded` after the script body completes.

---

## Methodology

Read the entire file in paged slices (offset/limit 350–600 lines). Cross-checked all top-level state declarations (`toolFlags`, `toolExamples`, `promptTemplates`, `learningPaths`, `playbooks`, `wizardFlows`, `promptTarget`, `selectedPromptTools`) against every function that consumes them. Enumerated all `document.addEventListener('click', ...)` handlers and traced their event-bubble interactions. Verified DB cross-references in `learningPaths[].weeks[].tools`, `playbooks[*].tools`, `toolExamples`, and `toolFlags` against the JSON in `<script id="tool-db">`.

---

## CRITICAL bugs (functional impact, hit in normal use)

### C1 — Command-Builder fallback produces wrong single-dash flags

**Location:** `updateCommandPreview()` — `forensik-explorer.html:3470`

```js
const prefix = (flagDef && flagDef.prefix) ? flagDef.prefix : `--${id} `;
```

The fallback `--${id}` is wrong for any flag whose ID represents a **single-dash** short option (e.g. `-O`, `-f`, `-a 0`, `-vV`). The current data has **~30 flags** without an explicit `prefix:` that fall back to a double-dash output, producing commands the shell will reject.

**Affected flags (sample):**

| Tool | Flag id | Wrong fallback | Real flag |
|------|---------|----------------|-----------|
| nmap | `O` | `--O` | `-O` |
| nmap | `A` | `--A` | `-A` |
| nmap | `sV` | `--sV` | `-sV` |
| nmap | `sC` | `--sC` | `-sC` |
| nmap | `p-` | `--p-` | `-p-` |
| nmap | `T4` | `--T4` | `-T4` |
| nmap | `sn` | `--sn` | `-sn` |
| hashcat | `O` | `--O` | `-O` |
| hashcat | `a 0` | `--a 0` | `-a 0` |
| john | `show` | `--show` ✓ (correct, kept for context) |
| hydra | `f` | `--f` | `-f` |
| hydra | `vV` | `--vV` | `-vV` |
| aircrack | `b` | `--b` | `-b` |
| aircrack | `e` | `--e` | `-e` |
| aircrack | `q` | `--q` | `-q` |
| msfconsole | `q` | `--q` | `-q` |
| ffuf | `ac` | `--ac` | `-ac` |
| masscan | `sV` | `--sV` | (actual flag is `--banner`, not `-sV`) |
| masscan | `echo` | `--echo` ✓ |
| wpscan | `aggressive` | `--aggressive` (real flag is `--detection-mode aggressive`) |
| nikto | `ssl` | `--ssl` ✓ |

A safe heuristic is to prefix with single dash when `id.length <= 2` and contains no `=` or `-` separator; otherwise double-dash. Even better: store both `dashCount` and `flag` in the flag def.

---

### C2 — `toolFlags.hashcat.increment` id does not match the real flag

**Location:** `forensik-explorer.html:3096`

```js
{id:'increment', label:'Brute Force', desc:'-a 3 — Brute-Force Mode', default:false},
```

The label/desc correctly say `-a 3`, but the `id` is `increment`. Output becomes `--increment`, which hashcat does not recognise. Either rename the id to `a 3` (matching sibling flag `a 0`) or store the full flag string.

---

### C3 — `toolExamples` lookup misses four aliased tools

**Location:** `showToolDetail()` — `forensik-explorer.html:3263-3265`

```js
const exKey = tool.id in toolExamples ? tool.id
  : (tool.id + '-ng' in toolExamples ? tool.id + '-ng' : null);
```

The lookup tries `id` then `id + '-ng'`. Four DB tools have examples keyed by a **different alias** that the logic never tests:

| DB id | Examples key | Result |
|-------|--------------|--------|
| `aircrack-ng` | `aircrack` | no examples shown |
| `evil-winrm` | `evilwinrm` | no examples shown |
| `powershell-empire` | `powershellempire` | no examples shown |
| `recon-ng` | `recon` | no examples shown |

The "Beispiel-Kommandos" section is absent for all four despite detailed examples existing in the data. Fix: add a `examplesKey` field per tool in the DB, or extend the lookup to try `id.replace('-ng','')`, `id.replace('-','')`.

---

### C4 — `selectedPromptTools` persists across mode switches

**Location:** `switchMode()` — `forensik-explorer.html:3482-3504` (does not clear `selectedPromptTools`)

Sequence that triggers the bug:

1. User opens LLM Prompt Builder in **blue** mode.
2. Selects 5 blue tools → counter shows "5 ausgewählt".
3. User closes the prompt overlay and switches mode to **purple**.
4. User opens the prompt overlay again.
5. The chip selector only renders purple tools (41 visible), but the counter still reads **5** because `selectedPromptTools` retains the blue-mode IDs.
6. None of those chips are highlighted (the IDs aren't in the purple chip list), so the user sees "5 selected" with zero chips visually selected.

The selection never gets invalidated against the new mode's `getAllTools()` set. Fix: in `switchMode`, either reset `selectedPromptTools` or filter it to IDs present in `getAllTools().map(t => t.id)`.

---

### C5 — `★ Favoriten laden` includes cross-mode favorites, silently dropped from prompt output

**Location:** `renderPromptModal()` — `forensik-explorer.html:2646-2649`

```js
document.getElementById('prompt-select-favs').addEventListener('click', () => {
  selectedPromptTools = new Set(favorites);
  renderPromptModal();
});
```

`favorites` is a single persistent Set across both modes (correctly — it's user data). When invoked from the prompt overlay in purple mode, it loads blue-mode favorite IDs that may not exist in `getAllTools()`. `buildPrompt()` silently drops them via `filter(Boolean)`, so the generated prompt is incomplete compared to what the user thought they selected.

Same root cause as C4 — fix together.

---

### C6 — Learning Path "Pentest von Null" references a non-existent tool

**Location:** `forensik-explorer.html:2402`

```js
{title:'Woche 4: Post-Exploitation', goal:'...', tools:['mimikatz','powersploit','evil-winrm'], done:false},
```

`powersploit` is not in the tool DB. The week renders with an empty chip. Most likely it was meant to be `powershell-empire` (which exists in the `ad-attack` playbook). Either rename or drop.

---

### C7 — Playbook "System Hardening" references a non-existent tool

**Location:** `forensik-explorer.html:3229`

```js
{id:'system-hardening', ..., tools:['ufw','fail2ban','apparmor','openssh','certbot'], ...}
```

`certbot` is not in the DB (only `openssl`, `openssh`, `wireguard`, `openvpn` exist). The playbook renders with an empty tool chip. Either add `certbot` to a purple category, or replace with `openssl` / drop the entry.

---

### C8 — `toolFlags` keyed `msfconsole` but DB id is `metasploit`

**Location:** `forensik-explorer.html:3151`

```js
msfconsole: { ... }
```

`findToolGlobal('metasploit')` returns the tool, but `tool.id in toolFlags` is `false` for `metasploit`, and `'metasploit-ng'` is not in `toolFlags` either. The Command-Builder section never opens for `metasploit`. Either rename the key to `metasploit` or extend the lookup (same fix pattern as C3).

---

## IMPORTANT bugs (UX degradation, won't crash)

### I1 — ESC inside a modal input only blurs, doesn't close the modal

**Location:** `forensik-explorer.html:4059-4062`

```js
if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
  if (e.key === 'Escape') e.target.blur();
  return;
}
```

When the user is typing in `cmd-target` or `prompt-target`, pressing Escape blurs the input but the modal stays open. They have to press Escape a second time to actually close it. The single-line `querySelectorAll(...).forEach(...)` at 4073 only fires after the early-return. Fix: change `if (e.key === 'Escape') e.target.blur(); return;` to `if (e.key === 'Escape' && e.target.blur() !== undefined) { /* let outer handler also close overlays */ }`, or restructure so Escape inside an input first closes the parent overlay.

---

### I2 — path-card auto-collapses after toggling a week or resetting

**Location:** `togglePathWeek()`, `resetPath()` — `forensik-explorer.html:2481-2495`

Both functions call `renderLearningPaths()`, which replaces `paths-grid.innerHTML`. The `.active` class that was on the currently-expanded card is wiped because new DOM nodes are created without the class. The user's "current view" state is lost on every checkbox toggle and reset click.

Fix: persist the open path id in a module-scoped variable (`openPathId`) and re-apply `.active` in the render loop when a path matches.

---

### I3 — Cheat-overlay can be opened via `?` while hidden behind detail-modal

**Location:** `forensik-explorer.html:4078-4081`

```js
if (e.key === '?') {
  document.getElementById('cheat-overlay').classList.toggle('visible');
  return;
}
```

`cheat-overlay` is `z-index: 200`; `detail-overlay` is `z-index: 300`. While detail is open, pressing `?` toggles `cheat-overlay.visible` — the user sees no change because it's behind detail. Pressing Esc closes detail first, revealing the cheat sheet — confusingly, the user may not have known they opened it. Fix: skip the toggle if any higher-z overlay is open.

---

### I4 — Mode-switch leaves detail/prompt/wizard open (theoretical only)

`switchMode()` does not call `closeToolDetail()`, `prompt-close`, or `wizard-close`. In practice the mode-switch buttons are at `z-index: 2` (header) while all overlays are `z-index: 200+`, so the user cannot reach the mode buttons while a modal is open. The only path to trigger this is keyboard shortcut, and the existing keyboard shortcuts (`?`, `F`, `C`) don't switch mode. **Not reachable in practice** but worth a defensive `switchMode` cleanup to reset any open overlay state.

---

### I5 — No mode-aware reset on `compareSet`

`switchMode()` clears `compareSet` (line 3495) but the `compareSet` IDs may include tools from the prior mode that no longer exist in the new mode's `getAllTools()`. `updateCompareBar()` calls `getAllTools().find(t => t.id === id)` per item and falls back to `id` if not found (line 3752). So the user sees a chip with the raw ID (e.g. `nmap-vulners`) instead of a tool name when switching modes with items in the compare set. The cleaner fix is to clear `compareSet` on mode switch (already happens — `compareSet.clear()` at 3495 — but the local variables aren't reset). **Verified safe** because `compareSet.clear()` runs, so this is a **non-issue**. Removed from the important list.

---

## MINOR issues (cosmetic / low-impact)

### M1 — 34 orphan keys in `toolExamples`

Keys present in `toolExamples` that are **not reachable** from any DB tool id (neither `id` nor `id+'-ng'` matches): `aide, auditd, certbot, clamav, curl, dcfldd, dig, dirsearch, dnsenum, dnsx, evilwinrm, exiftool, httpx, logwatch, ncat, netcat, nft, nslookup, openvassd, openvpn, ping, powershellempire, scp, socat, ssh, steghide, subfinder, tcpdump, traceroute, tshark, wapiti, wget, whois, wireguard`. These are dead data — they render nothing.

### M2 — 68 DB tools have no examples at all

Including `aircrack-ng, arpspoof, autorecon, bettercap, blkls, bulk_extractor, bully, cherrytree, commix, ...` (full list in the audit run). The detail-modal's "Beispiel-Kommandos" section is silently omitted. Acceptable (graceful degradation), but UX-inconsistent.

### M3 — 117/144 DB tools have no Command Builder

Only 15 tools have `toolFlags` entries (`nmap, sqlmap, hashcat, john, gobuster, nikto, hydra, aircrack, msfconsole, wpscan, nuclei, ffuf, masscan, evil-winrm, crackmapexec`). The detail-modal's "Command Builder" section is silently absent for the remaining 117 tools. Same graceful degradation as M2.

### M4 — HTML escaping missing in modal HTML

`showToolDetail()` interpolates `tool.name`, `tool.desc`, `tool.cmd` directly into innerHTML without escaping (lines 3360, 3366, 3374). DB-curated data is clean today (no `<`, `>`, `&`, `"` in any tool name/desc/cmd), so there is no live XSS. But the related-tools loop, the prompts section, the wizard result, and the compare-table all share the pattern. A single malformed DB entry would inject HTML. Fix: build a small `esc()` helper and apply it to all dynamic insertions.

### M5 — hashcat flag id contains a space (`'a 0'`)

Works today because the lookup is by string equality, but it's an unusual identifier. If anyone later does `id.split('-')` they'll be surprised.

### M6 — Tool-card click handler at line 3814 has redundant guard

`if (e.target.closest('.fav-btn, .compare-btn, .tool-cmd-copy, .tool-audio-btn')) return;` already excludes inner buttons. The `e.stopPropagation()` calls inside the delegated handlers at 3724, 3801, 3601 are redundant. Harmless but signals confusion about the event flow.

---

## NOT-BUGS (verified, do not change)

- **TDZ: PASS.** All `const`/`let` for v3.0 state (`toolFlags` L3061, `toolExamples` L2675, `promptTemplates` L2524, `learningPaths` L2394, `playbooks` L3219) are declared before the functions that consume them. `function` declarations are hoisted. The only top-level function call before `DOMContentLoaded` is `renderPlaybooks()` at L3511, which depends on `playbooks` (L3219 — declared earlier) and `activePlaybook` (L2387 — earlier). `switchMode()` itself runs only inside `DOMContentLoaded` (L4127-4130), so the entire module is initialised by the time it fires.
- **`findToolGlobal` searches both modes** — it iterates `Object.keys(DB.modes)` (L3241). ✓
- **Multiple `document.addEventListener('click', ...)` handlers coexist correctly** — each checks its own target/closest pattern and they do not double-fire on the same click. The `.tool-card` delegated handler (L3814) correctly excludes `.fav-btn`, `.compare-btn`, `.tool-cmd-copy`, `.tool-audio-btn` via the closest-check, so child button clicks never bubble up to open the detail modal.
- **No `prompt-overlay` ↔ `detail-overlay` ESC conflict** — only one global keydown handler at L4057-4111 closes all overlays via a single `querySelectorAll(...).forEach(m => m.classList.remove('visible'))` (L4073).
- **`buildPrompt` handles empty selection** — `[...selectedPromptTools]` is empty, map returns `[]`, filter(Boolean) returns `''`, template still renders with "## Verfügbare Tools\n" section empty. No crash.
- **Detail-modal `findToolGlobal` for non-existent toolId** — returns `null`, `showToolDetail` returns early (L3252). No crash.
- **Tools with no tags** — `(tool.tags && tool.tags.length)` is false → `tagsHtml` is `''` → section omitted. In related-fallback (L3320-3342), `toolTagSet` is empty, `shared` is 0 for every candidate → `top` is empty → section omitted. No crash.
- **`renderPromptModal` re-entry safety** — each call replaces `innerHTML`, so old child listeners are detached. The only listener attached to a long-lived element is on `prompt-overlay` itself (L4017), attached once.
- **`findToolGlobal` does not return ambiguous categories** — every tool has a unique id across both modes (verified). Related-tools list always renders the correct category.
- **`showCompareModal` filter for missing tools** — `getAllTools().find(t => t.id === id)` may return undefined, but the `.filter(Boolean)` at L3764 drops them. No crash.
- **Wizard re-init on mode switch** — wizard-overlay can't be opened while a mode switch happens (z-index blocks header access). When reopened, `wizard-open` resets `wizStep`/`wizHistory` and re-renders the correct mode's flow.

---

## Recommended fix priority

1. **C1 + C2** (single line each in `updateCommandPreview` + data fix in `toolFlags`) — users see broken commands instantly.
2. **C3 + C8** (lookup logic) — fixes silent absence of features for four popular tools.
3. **C4 + C5** (`switchMode` clears/filters `selectedPromptTools`) — silent data inconsistency.
4. **C6 + C7** (data fixes) — one-liner renames in `learningPaths` and `playbooks`.
5. **I1 + I2** — small UX polish, high-frequency paths.
6. **M1, M4** — clean up dead data and add `esc()` helper before more features land.

---

## Files written

- `/home/bratan/20-Workspace/audits/bug-hunt-v2-report.md` (this report)
