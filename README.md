# 🔵🟣 Kali Tool Explorer

> **Interaktiver Kali Linux Tool-Explorer** — 144 Tools in Blue (Offensive) und Purple (Defensive) Team. Single-file HTML, kein Build, kein Server, kein Tracking.

![Version](https://img.shields.io/badge/version-3.1-22d3ee?style=flat-square)
![Tools](https://img.shields.io/badge/tools-144-a855f7?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)
![Size](https://img.shields.io/badge/size-178KB-f59e0b?style=flat-square)

## ✨ Was ist das?

Der **Kali Tool Explorer** ist ein einzelnes HTML-File, das die komplette Welt der Kali-Linux-Tools interaktiv erlebbar macht — mit allen Features, die ein modernes Cybersecurity-Lern-Tool braucht:

- 🔵🟣 **Dual Mode** (Blue/Purple) — Wechsel zwischen Offensive und Defensive mit weichen Farbübergängen
- 📊 **Tool-Detail-Modal** — Jede Karte zeigt Beispiele, Related Tools, Links
- 🔧 **Command Builder** — Interaktive Flag-Toggles für 15 Top-Tools (nmap, sqlmap, hashcat, ...)
- 🤖 **LLM-Prompt-Builder** — Generiert fertige Prompts für ChatGPT/Claude (4 Templates)
- 🛤️ **Lernpfade** — 4 strukturierte Curricula mit Progress-Tracking
- 🚀 **Quick-Start Playbooks** — 12 vorgefertigte Workflows (6 Blue + 6 Purple)
- 🧭 **Guided Wizard** — Branching-Wizard für Tool-Empfehlungen
- ⭐ **Favorites + Comparator** — Bis zu 4 Tools side-by-side vergleichen
- 🎨 **3 Themes** — Dark / Cyber / Light
- ♿ **a11y + Print** — Komplett tastaturbedienbar, printbar als PDF

## 🚀 Quickstart

Einfach `forensik-explorer.html` im Browser öffnen. Fertig. Kein npm, kein Docker, kein Build.

```bash
# Optional: lokal servieren für File-URL-Blockaden
python3 -m http.server 8080
# Dann http://127.0.0.1:8080/forensik-explorer.html
```

## 🎧 Audiobook

**12,5 Minuten Beginner-Guide** im Yuno-Stil (locker, charmant, mit dir redend):

| Datei | Beschreibung | Dauer |
|---|---|---|
| `audiobook/kali-explorer-gesamthörbuch.mp3` | Komplettes Hörbuch | 12:30 |
| `audiobook/kali-explorer-01-hallo.mp3` | Hallo + Was ist der Explorer | 1:20 |
| `audiobook/kali-explorer-02-zwei-welten.mp3` | Blue/Purple Mode-Switch | 1:30 |
| `audiobook/kali-explorer-03-karten.mp3` | Tool-Cards + Detail-Modal | 1:35 |
| `audiobook/kali-explorer-04-playbooks.mp3` | Quick-Start Playbooks | 1:30 |
| `audiobook/kali-explorer-05-wizard.mp3` | Guided Wizard | 1:05 |
| `audiobook/kali-explorer-06-command-builder.mp3` | Command Builder | 1:20 |
| `audiobook/kali-explorer-07-prompt-builder.mp3` | LLM-Prompt-Builder | 1:15 |
| `audiobook/kali-explorer-08-lernpfade.mp3` | Learning Paths | 1:25 |
| `audiobook/kali-explorer-09-basics.mp3` | Suchen, Filtern, Vergleichen | 1:05 |
| `audiobook/kali-explorer-10-abschied.mp3` | Zusammenfassung | 1:10 |
| `audiobook/audiobook-explorer-yuno.md` | Komplettes Script (Markdown) | — |

## 📂 Inhalt

```
kali-tool-explorer/
├── forensik-explorer.html         # ⭐ Hauptapp — 178 KB, 144 Tools, alle Features
├── kali-tool-database.json        # Tool-DB: 121 Tools mit Beschreibungen + Commands
├── README.md                       # Diese Datei
├── docs/                           # Markdown-Übersichten
│   ├── kali-forensik-overview.md  # Forensik-Tools Übersicht
│   └── kali-blue-vs-purple.md      # Blue vs Purple Team Erklärung
├── audiobook/                      # 🎧 12,5 Min Audiobook + Script
│   ├── kali-explorer-gesamthörbuch.mp3
│   ├── kali-explorer-01-hallo.mp3  ... bis 10-abschied.mp3
│   └── audiobook-explorer-yuno.md
├── audits/                         # Code-Reviews & Bug-Hunt Reports
│   ├── grand-polish-review-ux.md   # UX-Review (19 KB)
│   ├── grand-polish-review-engineer.md  # Engineer-Review (21 KB)
│   ├── bug-hunt-report.md          # Bug-Hunt v1 (24 KB)
│   ├── bug-hunt-v2-report.md       # Bug-Hunt v2 (16 KB)
│   ├── ui-polish-report.md         # UI-Polish v1 (18 KB)
│   └── ui-polish-v2-report.md      # UI-Polish v2 (31 KB)
└── plans/                          # SDD-Pläne
    ├── forensik-explorer-sdd.md    # Phase 1 Plan
    ├── phase2-blue-purple-switch.md
    └── phase3-extensions.md
```

## 🛠️ Tech-Stack

- **HTML/CSS/JS** — Vanilla, keine Frameworks
- **Inline JSON** — `kali-tool-database.json` ist als `<script type="application/json">` in der HTML eingebettet
- **Google Fonts** — Inter + JetBrains Mono (CDN)
- **TTS** — MiniMax Speech 2.8 HD (für Audiobook)
- **Zero Build** — Speichern → Browser öffnen → fertig

## 🎯 Features im Detail

### Mode-Switch (🔵 Blau / 🟣 Lila)

Ein Klick wechselt zwischen Offensive (Red/Blue Team, 103 Tools) und Defensive (Blue/Purple Team, 41 Tools). Farben, Tools, Playbooks, Wizard — alles passt sich an. Sanftes Mini-Fade auf allen Elementen.

### Tool-Cards (144 Stück)

Jede Karte zeigt:
- **Badge** (Daily Driver / Klassiker / Goldstandard)
- Name + Kategorie (12 Blue-Kategorien / 6 Purple NIST-CSF-Kategorien)
- Beschreibung + Tags
- Base Command mit Copy-Button
- Klick → Detail-Modal mit 3-5 Beispielen, Related Tools, externen Links

### Tool-Detail-Modal

99 Tools haben kuratierte Beispiel-Commands. 15 Top-Tools haben den **interaktiven Command Builder** mit Flag-Toggles (klick → live-generierter Befehl mit deinem Ziel).

### Quick-Start Playbooks (12)

**🔵 Blue:** Recon Sprint, Web Pentest, Password Crack, WiFi Audit, AD Attack Chain, Post-Exploit
**🟣 Purple:** System Hardening, Active Overwatch, Incident Response, Threat Hunt, Vuln Assessment, Backup Recovery

Klick → Tools werden im Grid hervorgehoben + Auto-Scroll.

### Guided Wizard

Fragt: Was willst du angreifen / Was ist deine Mission? Verzweigt, kommt zum perfekten Playbook mit "▶ Playbook starten"-Button.

### LLM-Prompt-Builder

4 Templates (Pentest, SOC, IR, Learning) + Tool-Multi-Select + Ziel-Input → generiert fertigen Prompt mit Rolle, Task, Tool-Liste und Output-Format. Copy oder Download als Markdown.

### Lernpfade

4 strukturierte Curricula mit Wochen-Checkboxen und Progress-Bars (gespeichert in localStorage):
- Pentest von Null (4 Wochen)
- SOC Analyst Basics (3 Wochen)
- Web App Security (3 Wochen)
- Forensik Fundamentals (2 Wochen)

### Keyboard Navigation

- `Ctrl+K` → Suche fokussieren
- `1-6` → Playbook #1-6 triggern
- `0` → Alle Tools
- `F` → Nur Favoriten
- `C` → Comparator öffnen
- `?` → Cheat-Sheet
- `Esc` → Modals schließen

## 📊 Stats

- **144 Tools** (103 Blue + 41 Purple)
- **178 KB** single-file HTML
- **12 Playbooks** (6 + 6)
- **15 Command-Builder** Flag-Datenbanken
- **99 Beispiel-Commands**
- **4 Lernpfade** (13 Wochen total)
- **0 externe Dependencies** außer Google Fonts

## 🤝 Contributing

Pull Requests willkommen! Bitte:
1. `patch` Tool nutzen (kein `write_file` für Edits)
2. `read_file` mit offset/limit (kein `cat`)
3. State-Variablen IMMER oben deklarieren (TDZ-Lesson!)
4. Conventional Commits
5. Vor PR: einen Bug-Hunt + UI-Review laufen lassen

## 📜 License

MIT — Basti / @Toqsick

## 🙏 Credits

- Gebaut mit Yuno + Hermes Agent Schwarm
- TTS: MiniMax Speech 2.8 HD
- 4 parallele Subagenten für Reviews, 4 für Fixes, 14 serielle SDD-Tasks für die Hauptapp
- ~14 Stunden Arbeit (beginnend v1 single-file audio tour → v3.1 full-featured explorer)