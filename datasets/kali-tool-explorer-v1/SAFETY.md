# Kali Tool Explorer — Safety-Policy

> Verbindliche Nutzungsgrenzen für den Datensatz in diesem Ordner. Der Korpus beschreibt offensive und defensive Security-Werkzeuge; die Beispiele sind Dokumentation, keine Aufforderung. Übergeordnet gelten die Regeln dieses Repos und die Freigaben von Basti.

## Zweck

Der Datensatz macht Kali-Tools für Suche, Empfehlung, Lernpfade, RAG und kuratierte Q&A zugänglich. Er soll das Verständnis und die Verteidigung verbessern, nicht unbefugte Eingriffe ermöglichen.

## Erlaubt

- Security-Tests auf eigenen Systemen oder mit ausdrücklicher, dokumentierter Genehmigung.
- Labore, CTFs, Trainings und Lehre.
- Defensive Arbeit: Detection, Härtung, Forensik, Incident Response.
- Forschung an Tool-Taxonomien, Command-Syntax und LLM-Evaluationen.
- Interne Qualitätsprüfung und Kuratierung des Datensatzes.

## Nicht erlaubt

- Zugriff auf Systeme, Konten oder Netze ohne Genehmigung.
- Einsatz der Commands gegen fremde Infrastruktur, Massenziele oder kritische Infrastruktur.
- Malware-Erstellung, Persistenz, Exfiltration oder Evasion für schädliche Zwecke.
- Umgehung von Schutzmaßnahmen oder Löschung von Spuren ohne legitimen Auftrag.
- Weiterverkauf oder Veröffentlichung als angeblich geprüfte Angriffsanleitung.

## Klassifikation

- **Dual-Use:** 100 von 131 Tools; offensive und defensive Verwendung möglich.
- **Defensiv:** 31 von 131 Tools; überwiegend Purple-/NIST-CSF-Kategorien.
- **Risk-Level:** 28 hoch, 80 mittel, 23 niedrig.
- **Commands:** 182 Beispiele; 34 per `--help` lokal installierter Binaries annotiert, 148 unverified, 0 ungültig.
- **Builder:** 15 Records; alle als unverified markiert, weil die Live-Ausgabe vier dokumentierte Fehler hat.

Die Klassifikation ist eine Orientierung, keine Freigabe. Ein `low`-Risk-Tool kann in einem falschen Kontext trotzdem schädlich sein.

## Umgang mit Commands

1. Ziel und Berechtigung vor jedem Lauf prüfen.
2. Platzhalter (`target`, `10.0.0.0/24`, `hash.txt`, …) durch laborspezifische Werte ersetzen.
3. Commands zuerst in einer isolierten VM oder einem Container testen.
4. `verified: false` bedeutet nicht „falsch“, sondern „nicht gegen eine Live-Installation geprüft“.
5. Builder-Templates sind abgeleitet und ungetestet; die `observed_output_2026_10_20`-Felder dokumentieren die fehlerhafte App-Ausgabe.

## Lizenz und Herkunft

- Code und Dokumentation: MIT.
- Toolnamen und CLI-Beispiele: faktische Angaben.
- Audio und TTS: zusätzlich die Bedingungen des TTS-Anbieters prüfen.
- Keine personenbezogenen Daten; Quellen-Hashes in `kali-source-manifest.json`.

## Meldung von Fehlern

Fehlerhafte Commands, falsche Safety-Klassifikationen oder unklare Lizenzen gehören in die Review-Tabelle `kali-review-sample.csv` und in die Projektnotiz Kali-Pentest-Lab. Die menschliche Abnahme ist noch offen; bis dahin bleibt der Korpus ein Seed.
