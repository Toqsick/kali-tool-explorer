# Changelog

Alle nennenswerten Änderungen am Kali Tool Explorer werden hier dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [3.1] — 2026-08-06

### 🎉 Initial Public Release

**Erste öffentliche Version** — nach 14 Stunden Bauzeit (v1 single-file audio tour → v3.1 full-featured explorer).

### ✨ Features

#### Phase 1: Grundgerüst
- ✅ 24 Forensik-Tools mit Audiobook-Integration
- ✅ Card-Rendering mit Badges, Tags, Categories
- ✅ Live-Suche mit Debouncing + Results-Counter
- ✅ Favorites (localStorage)
- ✅ Comparator (max 4 Tools side-by-side)
- ✅ Recipes/Playbooks + Decision-Tree-Wizard
- ✅ Keyboard Navigation (Ctrl+K, 1-6, F, C, ?, Esc)
- ✅ 3 Themes (Dark, Cyber, Light)
- ✅ Print/PDF-Stylesheet, A11y, Touch-safe

#### Phase 2: Blue/Purple Dual-Mode
- ✅ 144 Tools total (103 Blue Offensive + 41 Purple Defensive)
- ✅ Mode-Switch mit sanften Farbübergängen
- ✅ Globale Mini-Fade-Transitions auf alle UI-Elemente
- ✅ 12 Playbooks (6 Blue + 6 Purple) mit Difficulty-Badges
- ✅ Full Dual-Mode Wizard mit Branching und Back-Button
- ✅ Karteikarten für `recon-sprint`, `web-pentest`, `system-hardening`, `active-overwatch`, etc.

#### Phase 3: 4 neue Major-Features
- ✅ **Tool-Detail-Modal** — 99 kuratierte Beispiel-Commands, Related Tools, externe Links
- ✅ **LLM-Prompt-Builder** — 4 Templates (Pentest/SOC/IR/Learning), Tool-Multi-Select, Copy + Markdown-Download
- ✅ **Command Builder** — 15 Top-Tools mit interaktiven Flag-Toggles und Live-Preview
- ✅ **Learning Paths** — 4 strukturierte Curricula (Pentest von Null, SOC Analyst Basics, Web App Security, Forensik Fundamentals) mit Progress-Tracking in localStorage

### 🐛 Bugfixes (2 Runden)

#### v3.0 → v3.1 (Bug-Hunt v2)
- ✅ 8 Critical Bugs gefixt:
  - Command-Builder: 37 Flags ohne Prefix → explizite Prefix-Felder hinzugefügt
  - `hashcat.increment` Flag falsch (`-a 3` statt `--increment`)
  - `toolExamples`: 4 Tool-IDs mismatched (`aircrack-ng`, `evil-winrm`, `powershell-empire`, `recon-ng`)
  - `selectedPromptTools` persistierte bei Mode-Switch
  - Lernpfad: `powersploit` nicht in DB → `powershell-empire`
  - Playbook: `certbot` nicht in DB → existierendes Tool
  - `toolFlags`: `msfconsole` vs DB-ID `metasploit` (Key-Rename)
  - Mode-Switch schloss nicht alle Overlays
  - Path-Card Click bubbelte zu Tool-Details
- ✅ TDZ (Temporal Dead Zone) verifiziert: alle State-Variablen vor Funktionen
- ✅ Inline UI-Polish: Progress-Bar 6px + Glow, Path-Card Left-Border, Tool-Chips klickbar, Done-State

### 🎧 Audiobook
- ✅ 12,5 Min Beginner-Guide im Yuno-Stil (MiniMax Speech 2.8 HD)
- ✅ 10 Kapitel einzeln + komplett
- ✅ Script als Markdown

### 📚 Dokumentation
- ✅ 6 Audit-Reports im `/audits/` Ordner (UX, Engineer, Bug-Hunt v1+v2, UI-Polish v1+v2)
- ✅ 3 SDD-Pläne im `/plans/` Ordner
- ✅ 2 Übersichts-Markdown im `/docs/` Ordner

---

## Legende

| Symbol | Bedeutung |
|---|---|
| ✨ | Neues Feature |
| 🐛 | Bugfix |
| ⚡ | Performance |
| 📚 | Dokumentation |
| 🔒 | Security-Fix |
| ⚠️ | Breaking Change |

[Unreleased]: https://github.com/Toqsick/kali-tool-explorer/compare/v3.1...HEAD
[3.1]: https://github.com/Toqsick/kali-tool-explorer/releases/tag/v3.1