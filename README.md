# 🔵🟣 Kali Tool Explorer

> **Deine interaktive Karte durch die Welt der Kali-Linux-Tools.** 144 Tools in Blue (Offensive) und Purple (Defensive). Single-File-HTML. Kein Build, kein Server, kein Tracking. Inklusive 12,5-Minuten-Audiobook im Beginner-Format.

[![Version](https://img.shields.io/badge/version-3.1-22d3ee?style=for-the-badge)](https://github.com/Toqsick/kali-tool-explorer/releases)
[![Tools](https://img.shields.io/badge/tools-144-a855f7?style=for-the-badge)](./forensik-explorer.html)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge)](./LICENSE)
[![Size](https://img.shields.io/badge/size-178KB-f59e0b?style=for-the-badge)](./forensik-explorer.html)
[![Audiobook](https://img.shields.io/badge/audiobook-12.5min_🎧-fbbf24?style=for-the-badge)](./audiobook/kali-explorer-gesamthörbuch.mp3)

[🚀 Quickstart](#-quickstart) · [✨ Features](#-features) · [🎧 Audiobook](#-audiobook) · [📖 Doku](#-dokumentation) · [🤝 Contributing](#-contributing) · [❓ FAQ](#-faq)

---

## 🎯 Was ist das?

Du öffnest Kali Linux zum ersten Mal. Siehst hunderte Tools im Menü. nmap. Burp Suite. Metasploit. Wireshark. Und du denkst dir: **Okay. Und jetzt?**

Der **Kali Tool Explorer** löst genau dieses Problem. Es ist ein einzelnes HTML-File, das du direkt im Browser öffnest — keine Installation, kein Login, keine Cloud, keine Tracking. Eine Datei. Doppelklick. Fertig.

Stell dir vor, es ist ein **interaktiver Atlas** für die Cybersecurity-Welt. Er zeigt dir nicht nur, welche Tools existieren, sondern auch:

- 🛣️ **Welche Tools** für welche Aufgabe
- 🧭 **In welcher Reihenfolge** du sie nutzt (Playbooks & Wizard)
- 🔧 **Welche Flags** du setzen musst (Command Builder)
- 🤖 **Wie du KI-Assistenten** richtig fragst (Prompt Builder)
- 🛤️ **Wie du lernst** (strukturierte Lernpfade mit Fortschritt)

Das Ganze in einer einzigen HTML-Datei, 178 KB klein, und visuell so smooth, dass alle Übergänge sanft faden. Dark Theme, dezent, mit blau/violett Modus-Wechsel für Offensive vs Defensive.

---

## 🚀 Quickstart

### Option 1: Direkt öffnen (schnellste Methode)

```bash
# 1. Repository klonen
git clone https://github.com/Toqsick/kali-tool-explorer.git
cd kali-tool-explorer

# 2. Im Browser öffnen
xdg-open forensik-explorer.html    # Linux
open forensik-explorer.html        # macOS
start forensik-explorer.html       # Windows
```

**Fertig.** Der Explorer ist sofort einsatzbereit.

### Option 2: Lokaler Server (für File-URL-Blockaden)

Manche Browser blockieren `file://`-URLs. Falls du Probleme mit Audio-Buttons oder externen Features hast:

```bash
python3 -m http.server 8080
# Dann: http://127.0.0.1:8080/forensik-explorer.html
```

### Option 3: Online-Demo

Besuche das Repo auf GitHub Pages (siehe Releases) oder hoste es selbst mit:

```bash
# GitHub Pages aktivieren in den Repo-Settings → Pages → main branch
# Dann: https://toqsick.github.io/kali-tool-explorer/forensik-explorer.html
```

---

## ✨ Features

### 🔵🟣 Dual-Mode (Blue & Purple Team)

Oben rechts: zwei Knöpfe, Blau und Lila. Ein Klick wechselt die **gesamte Anwendung**:

| Modus | Fokus | Tools | Playbooks |
|---|---|---|---|
| 🔵 **Blue** | Offensive / Red Team | 103 Tools (nmap, Burp, Metasploit, ...) | 6 Playbooks |
| 🟣 **Purple** | Defensive / SOC | 41 Tools (Suricata, Wazuh, TheHive, ...) | 6 Playbooks |

**Sanfte Farbübergänge**, alle Elemente faden mit dem `cardFadeIn`-Animation. Kein hartes Switch, sondern ein weiches Gleiten zwischen den Welten.

### 📊 Tool-Detail-Modal

Klick auf eine Tool-Card → großes Modal mit:

- **Badge** (Daily Driver / Klassiker / Goldstandard)
- Name + Kategorie (12 Blue-Kategorien / 6 Purple NIST-CSF-Kategorien)
- Ausführliche Beschreibung
- 3–5 **Beispiel-Commands** mit Erklärungen (für 99 Tools kuratiert)
- **Related Tools** (gleiche Tags)
- **Externe Links**: Kali Docs, Man-Pages

### 🔧 Command Builder (15 Top-Tools)

Für **15 wichtigste Tools** (nmap, sqlmap, hashcat, john, gobuster, nikto, hydra, aircrack-ng, metasploit, wpscan, nuclei, ffuf, masscan, evil-winrm, crackmapexec):

- **Interaktive Flag-Toggles** mit Beschreibungen
- **Live-Preview** — der Befehl wird in Echtzeit zusammengebaut
- **Copy-Button** → direkt ins Terminal
- Beispiel: nmap: Häkchen bei "Service Detection", "Default Scripts", "Fast Timing" setzen → `nmap -sV -sC -T4 scanme.nmap.org`

### 🤖 LLM-Prompt-Builder

4 Templates für KI-Assistenten (ChatGPT, Claude, Gemini):

| Template | Use-Case |
|---|---|
| ⚔️ **Pentest Plan** | Strukturierter Angriffsplan |
| 👁️ **SOC Analyse** | Defensive Monitoring-Strategien |
| 🚨 **Incident Response** | NIST IR-Framework Triage |
| 📚 **Lern-Guide** | Tool-Tutorial für Anfänger |

**Tool-Auswahl** (Multi-Select oder "★ Favoriten laden"), **Ziel/Szenario**-Input → fertiger Prompt mit Rolle, Task, Tools und Output-Format. **Copy oder Download als Markdown**.

### 🛤️ Lernpfade (4 Curricula)

| Pfad | Wochen | Fokus |
|---|---|---|
| ⚔️ **Pentest von Null** | 4 | Komplett-Anfänger → erster Pentest |
| 👁️ **SOC Analyst Basics** | 3 | Monitoring, Detection, Response |
| 🌐 **Web App Security** | 3 | OWASP Top 10 praktisch |
| 🔬 **Forensik Fundamentals** | 2 | Disk, Memory, File-Recovery |

Pro Woche: Ziel-Beschreibung + Tool-Liste + Checkbox. **Progress-Bar** pro Pfad, gespeichert in localStorage. Klick eine Woche ab → Balken füllt sich → motiviert weiterzulernen.

### 🚀 Quick-Start Playbooks (12)

Klick auf ein Playbook → alle zugehörigen Tools leuchten im Grid auf + Auto-Scroll:

**🔵 Blue:** Recon Sprint · Web Pentest · Password Crack · WiFi Audit · AD Attack Chain · Post-Exploit
**🟣 Purple:** System Hardening · Active Overwatch · Incident Response · Threat Hunt · Vuln Assessment · Backup Recovery

### 🧭 Guided Wizard

Weißt du nicht, welches Playbook? Wizard fragt:
- **Blue:** "Was willst du angreifen?" → Web / Netzwerk / Passwörter / WiFi / AD
- **Purple:** "Was ist deine Mission?" → Härten / Monitoring / Respond / Hunt

Verzweigt, kommt zum perfekten Playbook mit "▶ Playbook starten".

### ⭐ Favorites + ⚖️ Comparator

- **Favoriten** mit Stern-Symbol, persistiert in localStorage
- **Comparator** wählt bis zu 4 Tools aus, zeigt sie side-by-side mit allen Properties

### ⌨️ Keyboard Navigation

| Taste | Aktion |
|---|---|
| `Ctrl+K` | Suche fokussieren |
| `1`–`6` | Playbook #1–6 triggern |
| `0` | Alle Tools |
| `F` | Nur Favoriten |
| `C` | Comparator öffnen |
| `?` | Cheat-Sheet anzeigen |
| `Esc` | Modals schließen |

### 🎨 Themes

3 Themes: **Dark** (default, dezent) · **Cyber** (Neon-Akzente) · **Light** (helle Alternative).

### ♿ Accessibility & Print

- ARIA-Labels überall
- Tastaturbedienung komplett
- Print-Stylesheet → als PDF speicherbar
- `@media(hover:none),(pointer:coarse)` → Touch-Geräte-Buttons immer sichtbar
- `prefers-reduced-motion` → Animationen aus

---

## 🎧 Audiobook

**12,5 Minuten Beginner-Guide** im Yuno-Stil (locker, charmant, mit dir redend). Generiert mit MiniMax Speech 2.8 HD.

### Komplett

| Datei | Beschreibung | Dauer |
|---|---|---|
| [`kali-explorer-gesamthörbuch.mp3`](./audiobook/kali-explorer-gesamthörbuch.mp3) | Komplettes Hörbuch in einem File | **12:30** |

### Einzelne Kapitel

| # | Kapitel | Thema | Dauer |
|---|---|---|---|
| 1 | [Hallo, Basti](./audiobook/kali-explorer-01-hallo.mp3) | Einleitung + Was ist der Explorer | 1:20 |
| 2 | [Zwei Welten, ein Schalter](./audiobook/kali-explorer-02-zwei-welten.mp3) | Blue/Purple Mode-Switch | 1:30 |
| 3 | [Die Karten](./audiobook/kali-explorer-03-karten.mp3) | Tool-Cards + Detail-Modal | 1:35 |
| 4 | [Playbooks — die Abkürzung](./audiobook/kali-explorer-04-playbooks.mp3) | Quick-Start Playbooks | 1:30 |
| 5 | [Der Wizard](./audiobook/kali-explorer-05-wizard.mp3) | Guided Wizard | 1:05 |
| 6 | [Command Builder](./audiobook/kali-explorer-06-command-builder.mp3) | Interaktiver Flag-Generator | 1:20 |
| 7 | [LLM-Prompt-Builder](./audiobook/kali-explorer-07-prompt-builder.mp3) | KI-Prompts generieren | 1:15 |
| 8 | [Lernpfade](./audiobook/kali-explorer-08-lernpfade.mp3) | Strukturiertes Lernen | 1:25 |
| 9 | [Suchen, Filtern, Vergleichen](./audiobook/kali-explorer-09-basics.mp3) | Bedienung-Basics | 1:05 |
| 10 | [Tschüss für jetzt](./audiobook/kali-explorer-10-abschied.mp3) | Zusammenfassung + Motivation | 1:10 |

**Plus**: [`audiobook-explorer-yuno.md`](./audiobook/audiobook-explorer-yuno.md) — komplettes Script als Markdown zum Mitlesen oder Übersetzen.

---

## 📖 Dokumentation

### 📁 Repo-Struktur

```
kali-tool-explorer/
├── ⭐ forensik-explorer.html         178 KB — Haupt-App, 144 Tools, alle Features
├── ⭐ kali-tool-database.json        40 KB  — Tool-DB (121 Tools mit Beschreibungen)
├── 📖 README.md                              Diese Datei
├── ⚖️ LICENSE                               MIT
│
├── 📁 audiobook/                    23 MB  — Audiobook + Script
├── 📁 audits/                              6 Review-Reports (siehe unten)
├── 📁 plans/                               3 SDD-Plans (Phase 1-3)
└── 📁 docs/                                Markdown-Übersichten
    ├── kali-forensik-overview.md
    └── kali-blue-vs-purple.md
```

### 📁 Audits (transparente Development-History)

Wir glauben an **transparente Entwicklung**. Alle Reviews sind im Repo:

| Report | Größe | Was es enthält |
|---|---|---|
| [`grand-polish-review-ux.md`](./audits/grand-polish-review-ux.md) | 19 KB | UX-Review vor Launch v1 |
| [`grand-polish-review-engineer.md`](./audits/grand-polish-review-engineer.md) | 21 KB | Engineer-Review vor Launch v1 |
| [`bug-hunt-report.md`](./audits/bug-hunt-report.md) | 24 KB | Bug-Hunt v1 — 39 Bugs (6 Critical) |
| [`bug-hunt-v2-report.md`](./audits/bug-hunt-v2-report.md) | 16 KB | Bug-Hunt v2 — 8 Critical + TDZ-Check |
| [`ui-polish-report.md`](./audits/ui-polish-report.md) | 18 KB | UI-Polish v1 — 35 Empfehlungen |
| [`ui-polish-v2-report.md`](./audits/ui-polish-v2-report.md) | 31 KB | UI-Polish v2 — 40 Empfehlungen |

### 📁 SDD-Plans

| Plan | Was es beschreibt |
|---|---|
| [`forensik-explorer-sdd.md`](./plans/forensik-explorer-sdd.md) | Phase 1: 8 SDD-Tasks (Scaffold, Cards, Search, Favorites, Comparator, Recipes, Keyboard, Polish) |
| [`phase2-blue-purple-switch.md`](./plans/phase2-blue-purple-switch.md) | Phase 2: Dual-Mode + Full Wizard |
| [`phase3-extensions.md`](./plans/phase3-extensions.md) | Phase 3: Detail-Modal + Prompt-Builder + Command-Builder + Learning-Paths |

### 📁 Docs

- [`kali-forensik-overview.md`](./docs/kali-forensik-overview.md) — Übersicht der Forensik-Tools
- [`kali-blue-vs-purple.md`](./docs/kali-blue-vs-purple.md) — Blue vs Purple Team erklärt

---

## 📦 Datasets

Kuratierte, reproduzierbare Datensätze liegen unter [`datasets/`](./datasets/). Der erste Datensatz [`kali-tool-explorer-v1`](./datasets/kali-tool-explorer-v1/) enthält 131 Tools, 182 Beispiel-Commands, 12 Playbooks, 4 Lernpfade und 131 Narrationen — mit Provenienz, Safety-Klassifikation, Qualitätsbericht und einer 26-Tool-Review-Stichprobe.

- [Datasets-Übersicht](./datasets/README.md)
- [Dataset v1](./datasets/kali-tool-explorer-v1/README.md)
- [Qualitätsbericht](./datasets/kali-tool-explorer-v1/quality-report.md)
- [Safety Policy](./datasets/kali-tool-explorer-v1/SAFETY.md)

## 📊 Stats

| Metrik | Wert |
|---|---|
| **Version** | 3.1 |
| **Total Tools** | 144 |
| **Blue Team Tools** | 103 |
| **Purple Team Tools** | 41 |
| **HTML Size** | 178 KB |
| **Code Lines** | 4.158 |
| **Playbooks** | 12 (6 Blue + 6 Purple) |
| **Wizard Flows** | 2 (Blue + Purple) mit Branching |
| **Lernpfade** | 4 (13 Wochen total) |
| **Command-Builder Tools** | 15 Top-Tools mit Flag-DB |
| **Beispiel-Commands** | 99 kuratiert |
| **Dependencies** | 0 (außer Google Fonts) |
| **Critical Bugs** | 0 |
| **Audiobook Length** | 12,5 Min HD |
| **License** | MIT |

---

## 🛠️ Tech-Stack

- **HTML/CSS/JS** — Vanilla, keine Frameworks
- **Inline JSON** — `kali-tool-database.json` ist als `<script type="application/json">` in der HTML eingebettet
- **Google Fonts** — Inter + JetBrains Mono (CDN, optional)
- **TTS** — MiniMax Speech 2.8 HD (für Audiobook)
- **Zero Build** — Speichern → Browser öffnen → fertig

### Architektur

```
HTML
├── <head>
│   ├── Inline CSS (alle Styles, ~30 KB)
│   └── Google Fonts <link>
└── <body>
    ├── <header>        — Mode-Switch + Themes
    ├── <.filter-bar>   — Suche + 14 Kategorie-Chips
    ├── <.playbooks>    — 12 Playbook-Cards
    ├── <.paths>        — 4 Lernpfad-Cards
    ├── <.tool-grid>    — 144 Tool-Cards
    └── Overlays
        ├── #detail-overlay    — Tool-Detail-Modal (z:300)
        ├── #prompt-overlay    — LLM-Prompt-Builder (z:350)
        ├── #wizard-overlay    — Guided Wizard (z:200)
        ├── #cheat-overlay     — Keyboard-Cheat-Sheet (z:200)
        └── #compare-overlay   — Comparator (z:250)

<script>
    ├── DB = JSON.parse(<tool-db>)
    ├── State: favorites, compareSet, currentMode, etc.
    ├── renderTools(), renderPlaybooks(), renderLearningPaths()
    ├── showToolDetail(), renderPromptModal(), renderWizardStep()
    ├── Mode-Switch, Filter, Search, Theme
    └── localStorage-Persistenz
</script>
```

---

## 🎬 Walkthrough: 60 Sekunden

```text
[ 0:00]  Öffne forensik-explorer.html
        ↓
[ 0:02]  Siehst 103 blaue Tools, alle sofort sichtbar
        ↓
[ 0:05]  Klick auf "🔵 Blue" / "🟣 Purple" oben rechts
        ↓ Farben faden sanft über, Tools wechseln
        ↓
[ 0:10]  Tippe "nmap" in die Suche
        ↓ Ergebnisse filtern sofort, Counter zeigt "1 von 103"
        ↓
[ 0:15]  Klick auf die nmap-Karte
        ↓ Detail-Modal öffnet: Beispiele, Related Tools, Links
        ↓
[ 0:25]  Klick "🔧 Command Builder" (unten im Modal)
        ↓ Toggle ein paar Flags an, z.B. -sV, -sC, -T4
        ↓ Befehl wird live generiert: nmap -sV -sC -T4 scanme.nmap.org
        ↓
[ 0:40]  Klick "🚀 Quick-Start Playbooks" → "Recon Sprint"
        ↓ 5 Tools leuchten im Grid auf, Auto-Scroll zum ersten
        ↓
[ 0:50]  Klick "🤖 Prompt Builder" oben
        ↓ Wähle Template + Tools, generiere fertigen Prompt
        ↓ Copy & Paste in ChatGPT für strukturierten Plan
        ↓
[ 0:60]  Fertig. Du hast 144 Tools, Playbooks, Command Builder
        und KI-Integration in 60 Sekunden gesehen.
```

---

## ❓ FAQ

### Warum eine einzelne HTML-Datei?

**Single-File = maximale Portabilität.** Du kannst sie auf USB-Stick kopieren, auf Air-Gap-Rechner übertragen, in Obsidian einbetten, per E-Mail verschicken, oder auf jedem Webspace hosten (oder gar nicht — funktioniert auch offline).

### Brauche ich Internet?

**Nein** — nur für Google Fonts (Schriftart) und GitHub-Links. Beides optional. Die App funktioniert komplett offline.

### Sind meine Daten sicher?

**Komplett lokal.** Keine Cloud, kein Telemetrie, kein Analytics. localStorage (für Favoriten + Progress) bleibt in deinem Browser. Nichts wird hochgeladen.

### Kann ich es kommerziell nutzen?

**Ja** — MIT-Lizenz. Nutze es, modifiziere es, verteile es, verkaufe es. Nur Copyright-Hinweis behalten.

### Funktioniert es auf dem Handy?

**Teilweise.** Layout ist responsive (375px+), aber für ernsthaftes Arbeiten empfehle ich Desktop. Touch-Geräte sind supported (Buttons sind immer sichtbar).

### Wie aktualisiere ich auf eine neue Version?

```bash
cd kali-tool-explorer
git pull origin main
```

Fertig. Deine localStorage-Daten bleiben erhalten.

### Ich finde einen Bug. Was tun?

1. Checke die [Issues](https://github.com/Toqsick/kali-tool-explorer/issues) — vielleicht schon gemeldet
2. Falls neu: Issue erstellen mit Screenshot + Schritte zum Reproduzieren
3. Oder direkt PR mit Fix (siehe Contributing unten)

### Kann ich eigene Tools hinzufügen?

**Ja!** Öffne `forensik-explorer.html` und editiere das `<script type="application/json" id="tool-db">`-Block. Oder besser: mach einen PR mit deinen Ergänzungen.

---

## 🤝 Contributing

Pull Requests sind willkommen! Hier der Workflow:

### Development-Setup

```bash
git clone https://github.com/Toqsick/kali-tool-explorer.git
cd kali-tool-explorer
# Kein npm install — direkt loslegen!
```

### Wichtige Regeln

1. **`patch` Tool** für Edits — kein `write_file` für gezielte Änderungen
2. **`read_file` mit offset/limit** — kein `cat` (Output-Cap-Schutz)
3. **State-Variablen IMMER oben** — TDZ-Lesson! (Const/Let vor Funktionen die sie referenzieren)
4. **Conventional Commits** — `feat:`, `fix:`, `docs:`, `refactor:`, `perf:`, `chore:`
5. **Vor PR: Bug-Hunt + UI-Review** — mindestens selber testen

### Contribution-Ideen

- 🎯 Mehr Tools zur DB hinzufügen
- 🔧 Command Builder für mehr Tools (derzeit 15)
- 📚 Mehr Beispiel-Commands (derzeit 99)
- 🛤️ Mehr Lernpfade (z.B. "Cloud Security", "Malware Analysis")
- 🤖 Mehr LLM-Prompt-Templates
- 🌍 Übersetzungen (EN, FR, ES, ...)
- 🎨 Weitere Themes
- ♿ Verbesserte A11y

### PR-Template

```markdown
## Was
[Kurzbeschreibung]

## Warum
[Problem das gelöst wird]

## Test-Plan
- [ ] Manuelle Tests: [was du getestet hast]
- [ ] Browser-Kompatibilität: [Chrome/Firefox/Safari]
- [ ] Mobile-Test: [falls relevant]

## Screenshots
[falls UI-Änderung]

## Audit-Notizen
[falls du selbst einen Mini-Bug-Hunt gemacht hast]
```

---

## 📜 License

**MIT License** — siehe [LICENSE](./LICENSE)

Copyright (c) 2026 Basti (@Toqsick)

---

## 🙏 Credits

- **Gebaut mit**: Yuno + Hermes Agent Schwarm
- **TTS**: MiniMax Speech 2.8 HD
- **Subagenten**: 4× Reviews + 4× Fixes + 14 serielle SDD-Tasks
- **Timeline**: ~14 Stunden Arbeit, beginnend mit v1 single-file audio tour → v3.1 full-featured explorer

### Tech-Danksagungen

- [Inter Font](https://rsms.me/inter/) — UI-Schriftart
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/) — Code-Schriftart
- Kali Linux Team — für die phänomenale Tool-Sammlung
- Alle Open-Source-Tool-Autoren (nmap, Burp, Metasploit, etc.) — ihr rockt

---

## 🌟 Star History

Wenn dir der Explorer hilft, gib uns einen ⭐ auf GitHub!

[![Star on GitHub](https://img.shields.io/github/stars/Toqsick/kali-tool-explorer?style=social)](https://github.com/Toqsick/kali-tool-explorer)

---

<div align="center">

**Built with ❤️ by Basti (@Toqsick) + Yuno**

*"Die Karte ist nicht das Ziel. Sie ist der Startpunkt. Die Reise machst du."*

</div>