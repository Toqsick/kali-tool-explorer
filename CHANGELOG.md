# Changelog

Alle nennenswerten Änderungen am Kali Tool Explorer werden hier dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [3.2.1] — 2026-11-21

### 🐛 Bugfixes — Command-Builder (die 4 bekannten Fehler aus der Live-Prüfung 2026-10-20)

1. **Toolname ↔ erstes Flag nicht getrennt** — `parts.join('')` klebte Toolnamen
   und erstes Flag zusammen (`nmap-sV -T4 …`). Fix: `join(' ')` + Whitespace-
   Normalisierung. Betrifft alle 15 Builder-Tools.
2. **Ziel landete am Ende statt hinter dem Flag** — neue `{target}`-Platzhalter-
   Syntax in Flag-Präfixen: sqlmap `-u {target}`, gobuster `-u {target}`,
   wpscan `--url {target}`, nuclei `-u {target}`, ffuf `-u {target}`,
   evil-winrm `-i {target}`; zusätzlich fachlich identisch korrigiert:
   nikto `-h {target}`, crackmapexec `smb {target}`.
3. **metasploit → msfconsole** — neues `cmdBase`-Feld: Der Builder zeigt den
   echten CLI-Namen (`msfconsole -q …`) statt des DB-Namens.
4. **aircrack-ng bekam keinen Builder** — Lookup-Kette um `id.replace(/-ng$/, '')`
   erweitert; `aircrack-ng` findet jetzt den `aircrack`-Flag-Satz.

### 🧪 Verifikation

Headless-Browser, 13 Fälle mit gesetztem Ziel — alle bestanden:
`nmap -sV -T4 10.0.0.5` · `hashcat -m 0 -a 0 hashes.txt` ·
`john --wordlist=… hashes.txt` · `sqlmap -u http://target.com/page?id=1 --batch` ·
`gobuster dir -u http://target.com -w … -t 50` · `nikto -h http://target.com` ·
`wpscan --url http://target.com --enumerate u,p,t` · `nuclei -u http://target.com -severity critical,high` ·
`ffuf -u http://target.com/FUZZ -w … -mc 200,204,301,302` · `evil-winrm -i 10.0.0.5 -u Administrator -p Password123` ·
`crackmapexec smb 10.0.0.0/24` · `msfconsole -q use exploit/multi/handler` ·
`aircrack-ng -w … capture.cap`. node --check OK.

---

## [3.2] — 2026-11-21

### 🎯 Implementation-Pass für das ui-polish-v2-Report

Systemic-Gaps-Paket: Mobile, A11y, Empty-States, Feedback-Konsistenz —
basierend auf den 20 offenen Empfehlungen aus `audits/ui-polish-v2-report.md`.

### ✨ Features

#### Mobile komplett (QW-M1/QW-M2)
- ✅ Cmd-Builder: 1 Spalte auf ≤640px, Copy-Button unter dem Output statt darüber
- ✅ Modals: engere Polster, kleinere Close-Buttons, keine Text-Overlap mehr
- ✅ Neuer 400px-Breakpoint (kleinste Phones) + 641–900px Tablet-Breakpoint
- ✅ Media-Block ans Stylesheet-Ende verschoben (Cascade-Fix: Base-Regeln der v3.0-Features überschrieben vorher die Mobile-Overrides)

#### Accessibility (A11y)
- ✅ `role="dialog"` + `aria-modal="true"` + `aria-label` auf allen 5 Overlays
- ✅ Fokus-Falle (Tab-Trap): Fokus bleibt im obersten offenen Overlay
- ✅ Fokus-Management: Öffnen fokussiert Close-Button, Schließen gibt Fokus zurück (MutationObserver)
- ✅ Cmd-Builder-Flags als echte `<label>`-Wrapper — Screen-Reader + native Toggle (QW-C2)

#### Empty-States
- ✅ Prompt-Builder: "Noch kein Tool gewählt"-Hint + Tools-Block-Hinweis statt leerem Prompt
- ✅ "Favoriten laden" disabled bei 0 Favoriten (statt stummem Dead-Click), Umbau ★→📥 (QW-P2)
- ✅ Cmd-Builder: `<ZIEL>`-Platzhalter im Output bis ein Ziel eingetragen ist

#### UX-Standardisierung
- ✅ `flashButton()`-Helper: einheitliches Copy/Download/Reset-Feedback (QW-E1, QW-P5)
- ✅ "↺ Defaults"-Reset-Button im Cmd-Builder (QW-C4)
- ✅ Chip-Filter im Prompt-Builder: 103-Tool-Wolke live durchsuchbar (M-P2)
- ✅ Prompt-Output scrollt bei Updates nach unten (QW-P4)
- ✅ Scroll-to-top-Button nach 500px (QW-S1)
- ✅ Zweistufige Bestätigung für Lernpfad-Reset statt Ein-Klick-Datenverlust (QW-L4)

#### Visual Polish
- ✅ Modal-Fade + Rise-In-Animation beim Öffnen (respektiert `prefers-reduced-motion`)
- ✅ Backdrop-Blur konsistent auf allen 5 Overlays (inkl. `-webkit-`)
- ✅ Detail-Badge "Daily Driver" cyan (wie Tool-Card, war grün) (QW-D1)
- ✅ Kontrast: `.detail-cat` + Cmd-Builder-Hint auf `--text-secondary` (QW-D2/QW-C3)
- ✅ Hover-Lift für Path-Cards + Prompt-Templates (QW-X3)
- ✅ Cmd-Builder-Active-State mit Glow wie Playbook-Cards (QW-X1)
- ✅ Chip-Selected-Kontrast stärker (.18 Tint + font-weight) (QW-P1)
- ✅ Prompt-Modal 720→680px — modal-Familie wie Detail-Modal (QW-P6)
- ✅ Cmd-Output: `padding-right:96px; min-height:2.4em` — kein Copy-Overlap mehr (QW-C1)

### 🐛 Bugfixes
- ✅ Cascade-Bug: Mobile-Media-Queries für v3.0-Features wirkungslos (Base-Regeln standen NACH den Overrides) — Browser-verify verified: Flag-Grid 2→1 Spalte, Copy absolute→static
- ✅ Dead Code entfernt: ungenutzter `checkboxes`-Selector im Cmd-Builder-Wiring

### 🧪 Verifikation (Headless-Browser, alle grün)
- node --check: Syntax OK (4.432 Zeilen, 190 KB)
- Fokus-Falle: Tab vom letzten Button → Close-Button (Wrap) ✓
- Fokus-Rückgabe beim Schließen ✓, Detail-Öffnen fokussiert Close ✓
- Label-Klick toggelt Flag nativ, Preview live ✓, Reset stellt Defaults wieder her ✓
- `<ZIEL>`-Ghost ✓, Chip-Filter "nmap" → 2 Treffer ✓, Hint toggle ✓
- Mobile 390px: 1 Spalte, kein Overflow, alle Modal-Regeln greifen ✓
- Scroll-Top-Logik: sichtbar ab 500px, versteckt bei 0 ✓

---

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