# Phase 2: Blue/Purple Switch + Full Wizard — Implementation Plan

> **Status:** Draft · **Created:** 2026-08-06
> **Depends on:** Phase 1 (Tasks 1-8) complete + kali-tool-database.json ready

## Goal

Verwandle den Forensik-Explorer in einen vollwertigen **Kali Tool-Explorer** mit Blue/Purple Mode-Switch:
- **Blue Mode** (Standard): Kali Linux offensive Tools (12 Kategorien, ~60-80 Tools)
- **Purple Mode**: Kali Purple defensive Tools (6 NIST-CSF Kategorien, ~30-40 Tools)
- **Mode-Switch** oben rechts — wechselt komplette UI-Theme + Tool-Set
- **Purple-Filter**: wenn aktiv, badet alles in Violett (Background, Accents, Borders)
- **Full Wizard**: durch ALLE Tools beider Modi, nicht nur Forensik
- **Klarer Mode-Indikator**: Badge/Banner zeigt "🔵 Blue Team" oder "🟣 Purple Team"

---

## Architecture Decision

**Single-file stays single-file.** Die neue Tool-DB wird inline als zweites `<script type="application/json">` Block embedded (oder das bestehende DB-Objekt erweitert).

Schema:
```json
{
  "meta": {"kaliVersion": "2026.2", "generatedDate": "2026-08-06"},
  "modes": {
    "blue": {
      "label": "Blue Team (Offensive)",
      "icon": "🔵",
      "color": "#3b82f6",
      "categories": [ ...12 categories... ]
    },
    "purple": {
      "label": "Purple Team (Defensive)",
      "icon": "🟣",
      "color": "#a855f7",
      "categories": [ ...6 NIST-CSF categories... ]
    }
  }
}
```

---

## Tasks

### Task P2-1: Tool-Database Compilation
- Subagent recherchiert und kompiliert JSON mit 80-150 Tools
- 12 Blue-Kategorien (Top 5-8 Tools each)
- 6 Purple-Kategorien (Top 3-8 Tools each)
- Output: `kali-tool-database.json`
- **Status: 🔄 In Progress (deleg_d85ed260)**

### Task P2-2: Merge Tool-DB into HTML
- Embed `kali-tool-database.json` als inline `<script type="application/json" id="kali-db">` in HTML
- Restructure existing `DB` object to use `modes.blue` / `modes.purple` structure
- Die 24 Forensik-Tools werden eine der Blue-Kategorien ("Forensics")
- **Prerequisite:** P2-1 complete + Phase 1 (Task 8) complete

### Task P2-3: Blue/Purple Mode-Switch UI + Logic
- Mode-Toggle oben (neben Theme-Toggle): 🔵 / 🟣
- Wechselt `currentMode` state ('blue' or 'purple')
- Re-rendert: Filter-Chips (Kategorien statt Phasen), Tool-Grid
- CSS: `[data-mode="purple"]` override — alles wird violett
  - `--accent-cyan` → `--accent-purple`
  - Background bekommt violetten tint
  - Borders, hover-effects, progress-bar
- Mode-Badge im Header: "🔵 Blue Team — Offensive" oder "🟣 Purple Team — Defensive"
- Persistiert in localStorage (`forensik-mode`)

### Task P2-4: Quick-Start Playbooks + Full Dual-Mode Wizard
- **Quick-Start Playbook Section** — klickbare Cards oberhalb der Tool-Grid:
  - Blue Playbooks: Recon Sprint, Web Pentest, Password Crack, WiFi Audit, AD Attack Chain, Post-Exploit
  - Purple Playbooks: System Hardening, Active Overwatch (SOC), Incident Response, Threat Hunt, Vuln Assessment
- Klick auf Playbook → **highlighted alle involvierten Tools** im Grid (wie Recipes)
- Jede Playbook-Card zeigt: Icon, Name, Tool-Count, Schwierigkeitsgrad
- **Full Wizard Rebuild** — ersetzt den alten 3-Step-Wizard:
  - Step 0: "Blue oder Purple?" (basiert auf currentMode, auto-preselect)
  - Blue-Pfad: "Was willst du angreifen?" → Web/Network/Password/WiFi/AD → dann "Erfahrung?" → Playbook-Empfehlung
  - Purple-Pfad: "Was ist deine Mission?" → Harden/Monitor/Respond/Hunt → dann "Scale?" → Playbook-Empfehlung
  - Ergebnis: Zeigt Playbook + involvierte Tools + "Starte Playbook" Button (highlighted Tools)
- **Prerequisite:** P2-3 complete

### Task P2-5: Final Visual Polish for Dual-Mode
- Mode-Transition-Refinement
- Playbook-Highlight-Animation (wenn Wizard-Ergebnis gezeigt wird)
- Quick-Start-Section Header-Design
- Final HTML/JSON validation

---

## Execution Order

```
Phase 1 Task 8 (Polish) ────────┐
                                 ├──► P2-2 (Merge DB) ──► P2-3 (Switch) ──► P2-4 (Wizard) ──► P2-5 (Polish)
P2-1 (DB Research) ─────────────┘
```

P2-2 und P2-3 brauchen beide Voraussetzungen. P2-4 und P2-5 bauen auf P2-3 auf.

---

## Hard Constraints (same as Phase 1)

| Constraint | Why |
|---|---|
| `write_file` ONLY for new files, NEVER on existing HTML | Truncation pitfall |
| `cat`/`cat -n` NEVER for reading | 50KB stdout cap |
| Parallel subagents on same HTML file | Patch race conditions |
| `patch` with non-unique `old_string` | Fails with N matches |
| Queen verifies after every task | `ls -la` + `grep` + JSON parse |

---

## Verification (final, after all P2 tasks)

- [ ] Mode-Switch funktioniert: Blue → Purple → Blue
- [ ] Purple-Mode hat violetten Background/Theme
- [ ] Filter-Chips wechseln je nach Mode (Kategorien)
- [ ] Wizard hat beide Pfade (Blue + Purple)
- [ ] localStorage persistiert Mode
- [ ] Alle bestehenden Features (Search, Favorites, Compare, Themes) funktionieren in beiden Modi
- [ ] HTML valid, JSON valid, > 80KB
