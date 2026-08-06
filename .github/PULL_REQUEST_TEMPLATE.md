name: 📝 Pull Request
about: Reiche einen PR für den Kali Tool Explorer ein
title: ''
labels: ''
assignees: ''
---

## 📝 Was

Kurzbeschreibung der Änderung.

Closes #(issue)

## 🎯 Warum

Welches Problem löst das?

## 🧪 Test-Plan

- [ ] Manuell getestet: [was du getestet hast]
- [ ] Browser getestet: [Chrome / Firefox / Safari]
- [ ] Mobile getestet (falls relevant): [375px / 768px]
- [ ] Validation-Checks ausgeführt:
  - [ ] HTML parst OK
  - [ ] JSON valid
  - [ ] Keine Legacy-Referenzen (`DB.tools`, `renderRecipes`, `data-phase`)

## 📸 Screenshots

Falls UI-Änderung:

## 🔍 Audit-Notizen

Falls du selbst einen Mini-Bug-Hunt oder UI-Review gemacht hast, kurz zusammenfassen.

## ✅ Checklist

- [ ] `patch` Tool genutzt (kein `write_file` für Edits)
- [ ] State-Variablen IMMER oben deklariert (TDZ!)
- [ ] Conventional Commit-Message
- [ ] Selbst getestet in mindestens 2 Browsern
- [ ] Keine Konsole-Errors