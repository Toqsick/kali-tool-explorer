# 🤝 Contributing zum Kali Tool Explorer

Vielen Dank für dein Interesse, zum Kali Tool Explorer beizutragen! Jeder PR — egal ob Bug-Fix, neue Tools, Übersetzungen oder Doku — ist willkommen.

## 📋 Inhaltsverzeichnis

- [Verhaltenskodex](#verhaltenskodex)
- [Wie kann ich beitragen?](#wie-kann-ich-beitragen)
- [Development-Workflow](#development-workflow)
- [Coding-Standards](#coding-standards)
- [Bug melden](#bug-melden)
- [Feature-Wunsch](#feature-wunsch)
- [Pull-Request-Prozess](#pull-request-prozess)

---

## 📜 Verhaltenskodex

Wir wollen eine offene, freundliche Community. Bitte:

- ✅ Sei respektvoll und konstruktiv
- ✅ Hilf Neulingen
- ✅ Akzeptiere konstruktive Kritik
- ❌ Keine Beleidigungen, Diskriminierung oder Belästigung
- ❌ Keine "Gatekeeping" — Sicherheit ist für alle da

---

## 💡 Wie kann ich beitragen?

### 🐛 Bug fixen

Siehe [Issues](https://github.com/Toqsick/kali-tool-explorer/issues?q=is%3Aissue+is%3Aopen+label%3Abug) mit `bug`-Label.

### ✨ Feature hinzufügen

- Neue Tools zur DB
- Command Builder für mehr Tools (derzeit 15)
- Mehr Beispiel-Commands
- Neue Lernpfade (z.B. "Cloud Security", "Malware Analysis")
- Neue LLM-Prompt-Templates
- Übersetzungen (EN, FR, ES, ...)
- Neue Themes
- A11y-Verbesserungen

### 📚 Doku verbessern

- Tippfehler in README/Docs
- Fehlende Code-Kommentare
- Neue Markdown-Übersichten
- Mehr Beispiele in `docs/`

### 🎨 Polish

- Mobile-Optimierung
- Performance-Tweaks
- Bessere Animationen
- Bessere Empty-States

---

## ⚙️ Development-Workflow

### Setup

```bash
# 1. Fork auf GitHub, dann:
git clone https://github.com/DEIN-USER/kali-tool-explorer.git
cd kali-tool-explorer

# 2. Erstelle einen Branch
git checkout -b feat/dein-feature

# 3. KEIN npm install — direkt loslegen!
# Die App ist single-file HTML. Bearbeite forensik-explorer.html.
```

### Testen

```bash
# Lokal servieren
python3 -m http.server 8080

# Browser öffnen
# http://127.0.0.1:8080/forensik-explorer.html

# Manuell testen:
# - Mode-Switch (Blue ↔ Purple)
# - Suche + Filter
# - Favorites (Reload überlebt)
# - Comparator
# - Wizard (komplett durchklicken)
# - Lernpfad (Häkchen → Progress-Bar)
# - Detail-Modal mit Beispielen
# - Command Builder (Befehl wird generiert)
# - LLM-Prompt Builder (Copy funktioniert)
# - Keyboard-Shortcuts (Ctrl+K, F, C, ?)
# - Print/PDF
# - Mobile (375px, 768px)
```

### Validation

```bash
# HTML-Check
python3 -c "from html.parser import HTMLParser; HTMLParser().feed(open('forensik-explorer.html').read()); print('HTML OK')"

# JSON-Validität
python3 -c "import json; json.load(open('kali-tool-database.json')); print('JSON OK')"

# Legacy-Cleanup (sollte alles 0 sein)
grep -c 'DB.tools' forensik-explorer.html  # 0
grep -c 'renderRecipes' forensik-explorer.html  # 0
grep -c 'data-phase' forensik-explorer.html  # 0
```

---

## 📐 Coding-Standards

### ❗ KRITISCH: TDZ-Pattern

**State-Variablen (`const`/`let`) MÜSSEN VOR Funktionen deklariert werden, die sie referenzieren.**

```js
// ✅ RICHTIG: State oben, Funktionen unten
let favorites = loadFavorites();
const compareSet = new Set();
let activePlaybook = null;

function renderPlaybooks() {
  // kann favorites, compareSet, activePlaybook nutzen
}

// ❌ FALSCH: State nach Funktionen
function renderPlaybooks() {
  // CRASH! favorites existiert noch nicht
}
let favorites = loadFavorites();
```

**Lesson learned**: Frühere Versionen hatten TDZ-Crashes weil Subagents `const`/`let` mitten im Code platziert haben. Verifiziere die Reihenfolge vor jedem Edit.

### Tool nutzen

- **`patch`** für Edits (nicht `write_file` für gezielte Änderungen)
- **`read_file` mit offset/limit** (nicht `cat` — Output-Cap-Schutz)
- **`search_files`** für globale Suche (nicht `grep`)
- **Mehrere Subagenten** für große Tasks (parallel, scoped)

### Style

- **Deutsch** für User-facing Content (Beschreibungen, Templates, Labels)
- **Englisch** für Code-Kommentare und Variable-Names
- **Kommentare sparsam aber sinnvoll** — nicht jeder Line, nur wo Erklärung nötig
- **CSS-Vars nutzen** — `--bg-surface`, `--accent-cyan`, etc. (siehe :root in CSS)

### Commit-Messages

[Conventional Commits](https://www.conventionalcommits.org/):

```text
feat: add Cloud Security learning path
fix: resolve TDZ crash in renderLearningPaths
docs: expand README with FAQ section
refactor: extract command-builder logic into helper
perf: lazy-load playbook icons
chore: update .gitignore
test: add e2e test for wizard flow
```

---

## 🐛 Bug melden

### Vor dem Melden

1. Check ob der Bug in [neuester Version](https://github.com/Toqsick/kali-tool-explorer) noch da ist
2. Suche in [existing Issues](https://github.com/Toqsick/kali-tool-explorer/issues?q=is%3Aissue)
3. Test in anderem Browser (Chrome, Firefox, Safari)

### Issue-Template

```markdown
## Bug-Beschreibung
[Was passiert?]

## Erwartetes Verhalten
[Was sollte passieren?]

## Reproduktion
1. Öffne ...
2. Klick auf ...
3. Beobachte ...

## Screenshots
[falls relevant]

## Environment
- Browser: [Chrome 126]
- OS: [Linux Mint 21]
- App-Version: [3.1]
- localStorage-State: [clean/with favorites/etc.]

## Console-Errors
[Browser DevTools → Console → Errors hier pasten]
```

---

## 💫 Feature-Wunsch

### Issue-Template

```markdown
## Problem
[Welches Problem löst das Feature?]

## Vorgeschlagene Lösung
[Wie soll es funktionieren?]

## Alternativen
[Andere Möglichkeiten?]

## Mockups / Beispiele
[falls visuell — Skizzen, ASCII-Art, Links]

## Aufwand-Schätzung
[Dein Bauchgefühl: 1h / 1d / 1w]
```

---

## 🚀 Pull-Request-Prozess

### 1. Branch erstellen

```bash
git checkout -b feat/mein-feature
# oder
git checkout -b fix/bug-beschreibung
```

### 2. Änderungen machen

- Verwende `patch` Tool für Edits
- Halte Commits fokussiert (1 Commit pro logischer Änderung)
- Teste manuell im Browser
- Führe Validation-Checks aus

### 3. Committen

```bash
git add forensik-explorer.html
git commit -m "feat: add Cloud Security learning path

- 3-week curriculum covering AWS/Azure security
- Tools: kube-bench, scout-suite, prowler, kube-hunter
- Progress tracking via existing localStorage pattern"
```

### 4. Pushen & PR öffnen

```bash
git push origin feat/mein-feature
gh pr create --title "feat: Cloud Security learning path" \
             --body "## Was
Fügt Cloud Security Lernpfad hinzu...

## Test-Plan
- [x] Manuell getestet in Chrome
- [x] Progress-Bar funktioniert
- [x] localStorage persists über Reload"
```

### 5. Review

- Maintainer reviewt innerhalb von ~7 Tagen
- Bei Änderungswünschen: bitte adressieren oder diskutieren
- Nach Approval: squash-merge in `main`

---

## 🏷️ Labels

Issues und PRs werden gelabelt mit:

- `bug` — Bestätigter Bug
- `enhancement` — Neues Feature
- `docs` — Nur Dokumentation
- `good first issue` — Anfänger-freundlich
- `help wanted` — Maintainer braucht Hilfe
- `priority: high/medium/low` — Wichtigkeit
- `wontfix` — Wird nicht gefixt

---

## 🙏 Nochmal danke!

Ohne Contributors wäre dieses Projekt nur eine weitere Idee. Danke, dass du dir die Zeit nimmst, es besser zu machen.

Happy hacking! 🎉