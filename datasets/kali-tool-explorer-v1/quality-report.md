# Kali Tool Explorer — Dataset-Qualitätsbericht

> Automatisch erzeugt am 2026-10-20 aus dem Inline-Block, den Audio-Skripten, den beiden Research-Dokumenten und den sechs Audit-Berichten. Der Bericht beschreibt den kuratierten Seed-Korpus in diesem Ordner, nicht die App-Laufzeit.

## Bestand

| Asset | Anzahl |
|---|---:|
| Tools (kanonisch) | 131 |
| Beispiel-Commands | 182 |
| Command-Builder-Records | 15 |
| Playbooks | 12 |
| Lernpfade | 4 |
| Wizard-Flows | 2 |
| Narrationen | 131 |
| Doku-Chunks | 21 |
| Audit-Records | 7 |
| Review-Sample | 26 |

## Feldvollständigkeit und Duplikate

- Kanonische Tools: **131**, davon mit mindestens einer Beschreibung: **131**.
- Tools mit leerem `primary_command`: **0**.
- Gemergte Varianten: **144**; Tools mit mehr als einer Variante: **12**.
- Safety: **{'dual-use': 100, 'defensive': 31}**; Risk: **{'high': 28, 'medium': 80, 'low': 23}**.

## Tag-Normalisierung

- Roh-Tags: **185**; gemappt: **185**; unmapped: **0**.
- Ziel-Achsen: **32** definiert, **30** verwendet; unbenutzt: `cloud, enumeration`.

## Command-Verifikation

- Beispiel-Commands: **182**; syntaktisch plausibel: **182**; verifiziert: **34**; ungültig: **0**.
- Davon aus der Tool-DB: **122**; Auxiliary-Commands für Tools außerhalb der 131er-DB: **60**.
- Builder-Records: **15**; alle als `unverified` markiert, weil die Live-Ausgabe nachweislich fehlerhaft ist.
- Status: **{'unverified': 148, 'verified': 34}**; Gründe: **{'binary_not_installed': 129, 'generic_wrapper_not_tool_binary': 5, 'flag_not_found_in_help': 14, 'help_check_passed': 34}**.
- Wrapper-Aufrufe (java, docker, systemctl, …), die nicht als Tool-Verifikation zählen: **5**.
- Für `--help` verfügbare Binaries: `aa-enforce, aa-status, auditctl, ausearch, curl, dd, dig, exiftool, httpx, iptables, john, nc, nft, nslookup, openvpn, ping, rsync, scp, socat, ssh, ssh-copy-id, ssh-keygen, tcpdump, ufw, wg, wg-quick, wget`.
- Verifikationsmethode: `--help` nur für direkt aufgerufene, lokal installierte Binaries; sonst Syntaxprüfung. Wrapper und nicht installierte Tools bleiben `unverified`.

## Curriculum

- Playbook-Tool-Referenzen: **62**; fehlend: **0**.
- Lernpfad-Wochen: **12**; Tool-Referenzen: **39**.
- Wizard-Playbook-Referenzen fehlend: **0**.

## Narration

- Skripte: **131**; Audio vorhanden: **131/131**.
- Zeichen: **37843**; Wörter: **4656**.
- Normalisierung: `Doppelminus` → `--`, `Minus` → `-`, `bewaehrt` → `bewährt`, `fuer` → `für`; `normalized_text` ist eine Best-Effort-Form, `raw_text` bleibt erhalten.

## Review

- Stratified Sample: **26** Tools (19.8 %), mindestens ein Tool je Kategorie.
- Agenten-Review: **26 pass**, **0 warn**.
- Davon Commands per `--help` verifiziert: **1/26**.
- Menschliche Abnahme: **26 pending**.
- Ausfüllhilfe: [Review Sample](review-sample.md) · Fragenkatalog: [Review Runbook](REVIEW.md).

## Bekannte Grenzen

- Die Commands sind **nicht** gegen eine Live-Kali-Installation verifiziert. 34 Commands wurden per `--help` lokal installierter Binaries annotiert; 148 bleiben `unverified`, davon 129 ohne installiertes Binary, 14 mit nicht gefundenem Flag und 5 Wrapper-Aufrufe.
- Die Builder-Templates sind aus den Flag-Daten abgeleitet und korrigieren die vier Live-Befunde, sind aber ungetestet.
- Die Tag-Achsen sind eine kuratierte Heuristik; die Roh-Tags bleiben für Rückverfolgbarkeit erhalten.
- Die Narration-Normalisierung ist konservativ und nicht sprachlich vollständig geprüft.
- Die 20-%-Stichprobe ist vorbereitet, aber menschlich noch nicht abgenommen.
- Die separate `kali-tool-database.json` wurde nicht als Quelle verwendet; maßgeblich ist der Inline-Block mit 144 Datensätzen.

## Dateien

- `kali-tools.jsonl` — 131 kanonische Tools mit Varianten, Achsen, Safety und Provenienz.
- `kali-commands.jsonl` — 182 Beispiel-Commands plus 15 Builder-Records.
- `kali-curriculum.jsonl` — 12 Playbooks, 4 Lernpfade, 2 Wizard-Flows.
- `kali-narration.jsonl` — 131 Narrationen mit Roh- und Normalform.
- `kali-docs.jsonl` — Chunks der beiden Research-Dokumente.
- `kali-audits.jsonl` — sechs Audit-Berichte plus Live-Prüfung.
- `kali-tag-taxonomy.json` — Achsen, Mapping und Abdeckung.
- `kali-review-sample.jsonl` — 20-%-Stichprobe mit Review-Checkliste.
- `kali-review-sample.csv` — dieselbe Stichprobe als Tabelle für die menschliche Abnahme.
- `kali-source-manifest.json` — Quellen, Hashes und Zähler.

## Links

- [Dataset README](README.md)
- [Safety Policy](SAFETY.md)
- [Review Runbook](REVIEW.md)
- [Review Sample](review-sample.md)
