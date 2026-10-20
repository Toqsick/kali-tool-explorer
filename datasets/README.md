# Datasets

Versionierte, reproduzierbare Datensätze aus dem Kali Tool Explorer und künftigen Quellen. Jeder Datensatz ist so aufgebaut, dass er **erstellt**, **evaluiert** und **menschlich abgenommen** werden kann.

## Aktuelle Datensätze

| Datensatz | Umfang | Status |
|---|---|---|
| [`kali-tool-explorer-v1`](./kali-tool-explorer-v1/) | 131 Tools, 182 Commands, 131 Narrationen, 21 Doku-Chunks | Seed-Korpus; 34 Commands per `--help` annotiert, 148 unverified, Review offen |

## Konvention

- Ein Ordner pro Datensatz: `<quelle>-v<major>` (z. B. `kali-tool-explorer-v1`).
- Jeder Ordner enthält:
  - `README.md` — Dataset-Card, Schema, Quickstart, Grenzen.
  - `SAFETY.md` — Nutzungsgrenzen und Dual-Use-Regeln.
  - `REVIEW.md` — Fragenkatalog und Entscheidungsregeln für die menschliche Abnahme.
  - `review-sample.md` — ausfüllbare Stichprobe.
  - `quality-report.md` — Messwerte, Verifikationsstand, bekannte Grenzen.
  - Daten als JSONL/CSV/JSON.
  - Build-Skripte und `extract_js.js` für die Reproduktion.
- Keine Secrets, Tokens, personenbezogenen Daten oder proprietären Inhalte committen.
- Commands sind Beispiele, keine geprüften Handlungsanweisungen. `verified` muss ehrlich gesetzt sein; `unverified` bleibt `unverified`.

## Neuen Datensatz erstellen

1. Ordner nach der Konvention anlegen oder einen bestehenden als Vorlage kopieren.
2. Build-Skript auf die Quelle zeigen lassen (`--source`) und in den Zielordner schreiben (`--out`).
3. `build_kali_dataset.py` und `build_review_sheet.py` ausführen; bei GitHub-Dokumenten `--doc-format github` verwenden.
4. `quality-report.md` lesen: Vollständigkeit, Duplikate, Command-Verifikation, Tag-Abdeckung, Grenzen.
5. `review-sample.md` für die menschliche Abnahme vorbereiten.
6. Daten und Dokumente committen, Branch pushen, PR öffnen.

## Evaluieren

- **Qualität:** `quality-report.md` — Feldvollständigkeit, Duplikate, Verifikationsstatus, Tag-Achsen, Curriculum-Referenzen.
- **Menschliche Abnahme:** `REVIEW.md` und `review-sample.md` — pro Tool vier Checks und eine Entscheidung (`accept` / `fix` / `reject`).
- **Grenzen dokumentieren:** Nicht verifizierte Commands, abgeleitete Builder-Templates, heuristische Tag-Zuordnungen und offene Reviews gehören in den Report.
- **Safety:** `SAFETY.md` gilt für alle Datensätze; dual-use Inhalte nur für autorisierte Tests, Lehre und Verteidigung.

## Links

- [Haupt-Repository](../README.md)
- [Kali-Tool-Explorer-Datensatz v1](./kali-tool-explorer-v1/)
