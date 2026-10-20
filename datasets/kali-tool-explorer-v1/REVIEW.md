# Kali Tool Explorer — Review-Runbook

> Schritt-für-Schritt-Anleitung für die menschliche Abnahme der 26er-Stichprobe. Ziel ist keine perfekte Neu-Recherche, sondern eine belastbare Entscheidung pro Tool: **accept**, **fix** oder **reject** — mit einer kurzen Begründung. Ausfüllvorlage: [Kali Tool Explorer - Review-Stichprobe](review-sample.md).

## Vorbereitung

1. [Kali Tool Explorer - Review-Stichprobe](review-sample.md) öffnen.
2. Bei Bedarf [Kali Tool Explorer - Dataset](README.md) für das Schema und [Kali Tool Explorer - Safety-Policy](SAFETY.md) für die Nutzungsgrenzen daneben legen.
3. [Dataset-Qualitätsbericht](quality-report.md) nur für den Kontext öffnen: 34 Commands sind per `--help` annotiert, 148 unverified, 0 ungültig.
4. Entscheiden: **Schnellmodus** (alle 26 Tools, 6 Kernfragen) oder **Vollmodus** (6 Kernfragen plus 8 Tiefenfragen für High-Risk- und Fix-Kandidaten).

## Zeitplan

| Session | Umfang | Zeit |
|---|---|---:|
| 1 | 9 Tools, Kernfragen | 30–40 Min |
| 2 | 9 Tools, Kernfragen | 30–40 Min |
| 3 | 8 Tools, Kernfragen + Tiefenpass für High-Risk/Fix | 40–60 Min |

High-Risk-Tools in der Stichprobe: `chisel`, `exploitdb`, `impacket-scripts`, `john`, `kismet`, `reaver`. Für diese lohnt der Tiefenpass zuerst.

## Der Fragenkatalog

### Kernfragen — für jedes Tool

| # | Frage | Woran erkennst du „ja“? |
|---:|---|---|
| 1 | **Beschreibung:** Beschreibt sie das Tool korrekt, konkret und ohne Irreführung? | Zweck, Einsatzgebiet und Grenze sind erkennbar; keine falsche Behauptung. |
| 2 | **Primärer Command:** Ist der Befehl vollständig, mit dem richtigen Binary und ohne kaputte Verkettung? | Binary existiert; zwischen Toolname und Flag steht ein Leerzeichen; keine Fantasie-Flags. |
| 3 | **Ziel/Platzhalter:** Ist das Ziel klar als Platzhalter erkennbar und kein echter Host? | `target`, `10.0.0.0/24`, `hash.txt`, `capture.pcap` oder ähnlich; kein reales Ziel. |
| 4 | **Kategorie/Achsen:** Passt die Kategorie, und decken die Achsen den Hauptzweck ab? | Die erste Achse entspricht dem, wofür man das Tool wirklich einsetzt. |
| 5 | **Safety/Risk:** Ist die Einstufung angemessen? | Dual-Use/defensiv und high/medium/low passen zu Wirkung und Kontext. |
| 6 | **Entscheidung:** accept, fix oder reject? | Regel unten; bei `fix`/`reject` eine konkrete Notiz. |

### Tiefenfragen — für High-Risk und Fix-Kandidaten

| # | Frage | Woran erkennst du „ja“? |
|---:|---|---|
| 7 | **Binary-Mapping:** Ist der Toolname eindeutig dem richtigen Binary zugeordnet? | Beispiel: `apparmor` → `aa-status`, `metasploit` → `msfconsole`, `impacket-scripts` → `impacket-*`. |
| 8 | **Flags/Subcommands:** Existieren die Flags/Subcommands in Kali 2026.2, und sind sie richtig kombiniert? | `--help`, Man-Page oder offizielle Doku bestätigt sie. |
| 9 | **Voraussetzungen:** Fehlt eine Prerequisite? | Root, Capture-Datei, Wordlist, Ziel-URL, API-Key, laufender Dienst. |
| 10 | **Sicherheitsgrenze:** Fehlt eine Warnung? | Destruktive Aktion, aktiver Angriff, Credential-Nutzung, Datenlöschung. |
| 11 | **Tags/Attribute:** Sind Roh-Tags und Attribute korrekt? | Plattform, Interface, Artefakt und Ambiguitäten wie `MAC` (Mandatory Access Control vs. MAC-Adresse) sind richtig. |
| 12 | **Dubletten/Aliase:** Ist die ID kanonisch und der Alias korrekt? | Kein doppelter Datensatz, kein Alias, der auf ein anderes Tool zeigt. |
| 13 | **Verifikation:** Ist `verified: false` korrekt, oder ist der Befehl belegbar? | `--help`/Doku bestätigt; sonst bleibt `unverified`. |
| 14 | **Fachliche Tiefe:** Fehlt eine wichtige Information? | Ein Reviewer würde den Eintrag ohne diese Info nicht verstehen. |

## Entscheidungsregeln

| Entscheidung | Wann | Was eintragen |
|---|---|---|
| **accept** | Alle Kernfragen „ja“; keine sachliche Abweichung. Kleinere Stilfragen sind eine Notiz, kein Blocker. | `accept` plus optionale Notiz. |
| **fix** | Mindestens eine sachliche Abweichung: falsches Binary, falscher Flag, falsche Achse, falsche Safety, fehlende Voraussetzung. Das Tool bleibt aber im Korpus. | `fix` plus konkreter Korrekturvorschlag. |
| **reject** | Der Eintrag ist fundamental falsch, irreführend oder unsicher; Kernidentität oder Befehl nicht rettbar. | `reject` plus Begründung und ggf. Quelle. |
| **unsicher** | Keine Entscheidung möglich, weil Beleg fehlt. | `fix` mit der offenen Frage; nicht `accept`. |

**Faustregel:** `accept` heißt nicht „perfekt“, sondern „belastbar genug für einen Seed-Korpus“. `unverified` bei Commands ist kein Ablehnungsgrund; `verified: true` ohne Beleg ist einer.

## Red Flags

- Toolname und Binary fallen auseinander (`apparmor`/`aa-status`, `metasploit`/`msfconsole`, `impacket-scripts`/`impacket-*`).
- Command beginnt mit `java`, `docker`, `systemctl`, `sudo` oder `python3` — das ist ein Wrapper, keine Tool-Verifikation.
- Ziel ist ein realer Host, eine reale Domain oder eine echte IP statt eines Platzhalters.
- `verified: true` ohne `--help`/Doku-Beleg.
- `defensive` bei einem klar offensiven Tool oder `low` bei Credential-/Exploitation-Tools.
- Ambigue Akronyme: `MAC`, `AD`, `IR`, `RE`, `DB`, `PTH`.
- Kategorie und Achse widersprechen sich (z. B. Forensik-Tool nur unter `reporting`).
- Doppelte ID, Alias-Konflikt oder zwei Einträge für dasselbe Binary.
- Fehlende Prerequisite (Wordlist, Capture, API-Key, Root).
- Destruktiver Befehl ohne Warnung (löschen, überschreiben, formatieren).

## Evidenzstandard

- **Binary/Flags:** `--help`, `man <tool>` oder offizielle Doku.
- **Zweck:** Kali-Tools-Seite oder Projekt-Homepage.
- **Tags/Achsen/Safety:** Kategorie plus Tool-Zweck; die Begründung in die Notiz schreiben.
- **Keine Evidenz:** `unverified` bleibt stehen; nicht als `verified` markieren.
- **Quelle notieren:** URL oder `--help`-Aufruf in die Notiz, damit die Entscheidung nachvollziehbar bleibt.

## Copy-Paste-Block pro Tool

```text
### <tool_id>
- Beschreibung korrekt? [ ] ja [ ] nein
- Command korrekt? [ ] ja [ ] nein [ ] unverified
- Ziel/Platzhalter klar? [ ] ja [ ] nein
- Kategorie/Achsen passend? [ ] ja [ ] nein
- Safety/Risk passend? [ ] ja [ ] nein
- Red Flag: <keine | ...>
- Entscheidung: accept / fix / reject
- Notiz: <was genau ändern?>
```

## Abschluss

| Datum | Reviewer | accept | fix | reject | Notizen |
|---|---|---|---:|---:|---:|---|
|  |  |  |  |  |  |

Nach der letzten Session: Summen prüfen (26 = accept + fix + reject), offene Fragen sammeln, dann Bescheid geben.

## Hand-off

Sag ZCode: **„Stichprobe reviewed“** und gib die Entscheidungen durch (oder fülle `kali-review-sample.csv` aus). Dann übernehme ich `review_decision` und `review_notes` in `kali-review-sample.jsonl`/`.csv` und ziehe den [Dataset-Qualitätsbericht](quality-report.md) nach.
