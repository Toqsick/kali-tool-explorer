# Kali Tool Explorer — Dataset v1

Kuratierter Seed-Korpus aus diesem Repository: **131 kanonische Tools**, **182 Beispiel-Commands**, **12 Playbooks**, **4 Lernpfade** und **131 deutsche Narrationen**. Die Daten wurden aus dem Inline-Block der App, den Audio-Skripten, zwei Research-Dokumenten und sechs Audit-Berichten extrahiert, dedupliziert und mit Provenienz, Safety-Klassifikation und normalisierten Themenachsen versehen.

> **Status:** Seed-Korpus, kein fertig verifizierter Benchmark. 34 Commands wurden per `--help` lokal installierter Binaries annotiert, 148 sind `unverified`, 0 ungültig. Die menschliche Abnahme der 26er-Stichprobe steht noch aus. Commands sind Beispiele, keine geprüften Handlungsanweisungen.

## Inhalt

| Datei | Inhalt | Zeilen |
|---|---|---:|
| `kali-tools.jsonl` | 131 kanonische Tools, 144 Varianten, Kategorien, Achsen, Safety, Provenienz | 131 |
| `kali-commands.jsonl` | 182 Beispiel-Commands + 15 Builder-Records | 197 |
| `kali-curriculum.jsonl` | 12 Playbooks, 4 Lernpfade, 2 Wizard-Flows | 18 |
| `kali-narration.jsonl` | 131 deutsche Narrationen mit Roh- und Normalform | 131 |
| `kali-docs.jsonl` | 21 Chunks aus Blue-vs-Purple und Forensik-Überblick | 21 |
| `kali-audits.jsonl` | sechs Audit-Berichte plus Live-Prüfung | 7 |
| `kali-review-sample.jsonl` | 26 Tools für die menschliche Abnahme | 26 |
| `kali-review-sample.csv` | dieselbe Stichprobe als Tabelle | 26 |
| `kali-tag-taxonomy.json` | 32 Achsen, 185 Tag-Mappings, 0 unmapped | — |
| `kali-source-manifest.json` | Quellen, SHA256-Hashes, Versionen, Zähler | — |
| `quality-report.md` | Messwerte, Verifikationsstand, Grenzen | — |
| `review-sample.md` | ausfüllbares Review-Dokument mit 26 Tool-Blöcken | — |
| `REVIEW.md` | Fragenkatalog, Entscheidungsregeln, Red Flags, Zeitplan | — |
| `SAFETY.md` | Nutzungsgrenzen und Dual-Use-Regeln | — |

## Schnellstart

```python
import json

def load(name):
    return [json.loads(line) for line in open(name, encoding="utf-8")]

tools = load("kali-tools.jsonl")
commands = load("kali-commands.jsonl")

scanning = [t for t in tools if "scanning" in t["topic_axes"]]
high_risk = [t for t in tools if t["risk_level"] == "high"]
verified = {c["tool_id"] for c in commands if c["verified"]}

print(len(tools), len(scanning), len(high_risk), len(verified))
```

## Schema

### Tool (`kali-tools.jsonl`)

- `id`, `name`, `name_variants`, `aliases`
- `modes`, `categories`, `primary_category`
- `description`, `description_variants`, `primary_command`, `commands`
- `tags_raw`, `topic_axes`, `attributes`, `unmapped_tags`
- `badges`, `risk_level`, `safety`
- `reference_url`, `reference_url_status`
- `provenance`, `variants`

`topic_axes` sind die normalisierten Themenachsen (`recon`, `scanning`, `web`, `network`, `credentials`, `forensics`, …). `attributes` tragen nicht-thematische Eigenschaften wie `interface:gui`, `platform:linux`, `artifact:e01`, `maturity:gold`. `tags_raw` bleibt für Rückverfolgbarkeit erhalten.

### Command (`kali-commands.jsonl`)

- `command_id`, `tool_id`, `tool_in_db`, `source`, `command`, `intent`
- `verified`, `syntax_ok`, `has_placeholder`, `placeholder_tokens`
- `verification` mit `method`, `status`, `reason`, `binary`, `installed`, `wrapper`
- `safety_class`, `risk_level`

`source` ist `toolExamples` für die 182 Beispiel-Commands und `command_builder` für die 15 Flag-Records. Builder-Records enthalten `corrected_template`, `observed_output_2026_10_20`, `target`, `flags` und `issues`.

### Curriculum (`kali-curriculum.jsonl`)

`kind` ist `playbook`, `learning_path` oder `wizard_flow`. Playbooks und Lernpfade enthalten kanonische Tool-IDs; Wizard-Flows enthalten Playbook-Referenzen. Alle 101 Tool-Referenzen und alle Playbook-Referenzen sind geprüft.

### Narration (`kali-narration.jsonl`)

`tool_id`, `raw_text`, `normalized_text`, `chars`, `words`, `tts_artifacts`, `normalization_notes`, `audio_path`, `audio_exists`, `language`, `style`, `tts_model`.

## Qualität

- 131 kanonische Tools aus 144 Datensätzen; 12 mehrfach verwendete IDs sind zusammengeführt, die Varianten bleiben erhalten.
- 185 Roh-Tags auf 32 Achsen gemappt, 0 unmapped; 30 Achsen werden tatsächlich verwendet.
- 182 Beispiel-Commands: 182 syntaktisch plausibel, 34 per `--help` annotiert, 148 unverified, 0 ungültig.
- 101 Curriculum-Referenzen, 0 fehlend.
- 131 Narrationen, 131 Audios vorhanden.
- 26 Tools (19,8 %) stratified für die menschliche Abnahme vorbereitet.

Details: [quality-report.md](quality-report.md).

## Safety

Der Korpus ist **dual-use**: 100 Tools sind als dual-use, 31 als defensiv klassifiziert; 28 haben Risk-Level `high`, 80 `medium`, 23 `low`. Die Beispiele sind keine Handlungsanweisung. Verbindliche Regeln: [SAFETY.md](SAFETY.md).

## Review

Die 26er-Stichprobe liegt als ausfüllbares Dokument bereit: [review-sample.md](review-sample.md). Der Fragenkatalog mit Entscheidungsregeln, Red Flags und Zeitplan steht in [REVIEW.md](REVIEW.md). Entscheidungen können in `kali-review-sample.csv` oder `kali-review-sample.jsonl` eingetragen werden.

## Reproduzieren

Voraussetzungen: Python 3.10+, Node.js 18+. Im Ordner `datasets/kali-tool-explorer-v1/`:

```bash
python3 build_kali_dataset.py --source ../.. --out . --doc-format github
python3 build_review_sheet.py --doc-format github
```

Das Skript liest `forensik-explorer.html`, `scripts/tool-audio-scripts.json`, `docs/`, `audits/` und `tool-audios/` aus dem Repo-Root. `extract_js.js` wird für die Datenobjekte in der HTML benötigt. Der Build ist deterministisch; das Review-Sample nutzt den Seed `20261020`.

## Provenienz und Lizenz

- Quelle: dieses Repository, Inline-Block `tool-db`, Audio-Skripte, `docs/`, `audits/`.
- Kali-Version: 2026.2; App-Version: 3.1; Datenbank-Version: 2.0.
- Lizenz: MIT (siehe [LICENSE](../../LICENSE)). Toolnamen und CLI-Beispiele sind faktische Angaben; Audio und TTS unterliegen zusätzlich den Bedingungen des TTS-Anbieters.
- Keine personenbezogenen Daten. Quellen-Hashes stehen in `kali-source-manifest.json`.

## Links

- [Datasets-Übersicht](../README.md)
- [Haupt-Repository](../../README.md)
- [Dokumentation](../../docs/) · [Audits](../../audits/) · [Audio-Skripte](../../scripts/)
