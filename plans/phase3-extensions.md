# Phase 3 — Kali Explorer Extensions

## Ziel
4 neue Features in `forensik-explorer.html` (~114KB → ~155KB target).

## Constraints
- `patch` ONLY (NEVER `write_file` for edits, NEVER `cat`)
- `read_file` with offset/limit ONLY
- State-Variablen IMMER oben deklarieren (TDZ-Lesson!)
- Mini-Fade auf alle neuen Transitions
- `prefers-reduced-motion` respektieren

## Tasks

### P3-1: Tool-Detail-Modal (foundational)
- Click auf Tool-Card → Full-Screen-Overlay
- Inhalt: Name, Beschreibung (lang), Command mit Syntax-Highlighting
- Beispiel-Commands (3-5 pro Tool)
- Tags, Kategorie, Difficulty
- Related Tools (gleiche Tags)
- Externe Links: man-page, Kali-Doc, GitHub
- Copy-Button für Commands
- ESC zum Schließen, Click-Outside

### P3-2: LLM-Prompt-Builder
- Button im Header: "🤖 Prompt Builder"
- Modal: Tool-Auswahl (Multi-Select aus aktuellen Favoriten/Compare oder manuell)
- Template-Auswahl: Pentest-Report, SOC-Analyse, Incident-Response, Learning-Guide
- Generiert fertigen LLM-Prompt mit:
  - Rolle ("Du bist ein erfahrener Penetration Tester...")
  - Kontext (ausgewählte Tools mit Desc + Commands)
  - Task-Beschreibung
  - Output-Format-Vorgaben
- Live-Preview mit Copy-Button
- Export als Markdown

### P3-3: Command-Builder
- Im Tool-Detail-Modal: "🔧 Command Builder" Tab
- Interaktive Flag-Toggles pro Tool (Top 20 Tools mit Flag-DB)
- Live-Command-Preview aktualisiert sich beim Toggeln
- Ziel-IP/Host Input-Feld
- Copy generierten Command
- "Save as Snippet" → localStorage

### P3-4: Lernpfade (Learning Paths)
- Neue Section unter Playbooks
- Strukturierte Curricula:
  - "Pentest von Null" (4 Wochen)
  - "SOC Analyst Basics" (3 Wochen)
  - "Web App Security" (3 Wochen)
  - "Forensik Fundamentals" (2 Wochen)
- Pro Woche: Tools, Ziele, Übungen
- Fortschritts-Tracking via localStorage (Checkboxen)
- Progress-Bar pro Pfad
