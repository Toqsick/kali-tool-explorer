# Kali Linux für Forensik — Topic-Detail (Komprimiert)

> **Stand:** 5. August 2026 · **Quellen:** 7 (live verifiziert via curl/requests) · **Scope:** Read-only live-Recherche ~3 min

---

## TL;DR

Kali Linux liefert im Forensik-Menü **~60+ spezialisierte Tools** in 8 Sub-Kategorien — von Disk-Imaging über File Carving, Sleuth Kit Suite bis PDF-Forensik. **Die zwei Kerntools, die du sofort lernen willst:** **Autopsy** (GUI, der de-facto-Standard für Disk-Untersuchungen) und **The Sleuth Kit** (CLI-Schicht darunter — mächtiger, skriptbar). Für Memory-Forensik zusätzlich **Volatility**.

---

## 1. Forensik-Menü-Struktur (kali.org/tools)

| Sub-Kategorie | Anzahl | Wichtigste Tools |
|---|---|---|
| **Digital Forensics** | 10 | `dc3dd`, `dcfldd`, `hexwalk`, `missidentify`, `readpst`, `reglookup`, `regripper`, `undbx`, `vinetto` |
| **Forensic Carving Tools** | 16 | `foremost`, `photorec`, `scalpel`, `testdisk`, `safecopy`, `scrounge-ntfs`, `extundelete`, `rifiuti/2` |
| **Forensic Imaging Tools** | 6 | `guymager`, `dd_rescue`, `ewfacquire`, `dc3dd`, `dcfldd`, `affcat` |
| **PDF Forensics Tools** | 2 | `pdfid`, `pdf-parser` |
| **Sleuth Kit Suite** | ~30 | `autopsy`, `fls`, `icat`, `mmls`, `tsk_recover`, `mactime`, `srch_strings` |
| **Incident Response / Malware** | 14 | `binwalk`, `bulk_extractor`, `hashdeep`, `ssdeep`, `yara`, `rkhunter`, `chkrootkit`, `unhide` |
| **Reporting Tools** | 13 | `cherrytree`, `dradis`, `maltego`, `obsidian`, `faraday`, `pipal`, `cutycapt` |
| **Laboratories** | 2 | `juice-shop-start`, `dvwa-start` |

(Quelle: kali.org/tools, Forensik-Sektion)

---

## 2. Die 6 Tools, die du wirklich brauchst

### Disk Imaging & Acquisition

**guymager** — wenn du von einer Disk ein forensisches Image erstellen willst
- Free, open-source, Linux-nativ
- Generiert dd (raw), EWF (E01) und AFF-Images
- Multi-threaded, pipelined, sehr schnell
- GUI mit angeschlossenen Devices
- Version 0.8.13 ist aktuell
- URL: guymager.sourceforge.net

**Workflow:** Quell-Disk anschließen → im Read-Only-Modus mounten → guymager starten → Image-Format wählen → Hash (MD5/SHA1/SHA256) parallel mitschreiben → Image verifizieren.

### Disk / File-System Analyse

**Autopsy** — der de-facto-Standard für Disk-Untersuchungen
- End-to-end open-source forensics platform
- "The premier end-to-end open source digital forensics platform" (autopsy.com)
- Built by Sleuth Kit Labs (Brian Carrier)
- GUI mit Plug-in-Architektur (Java/Python-Add-ons möglich)
- Schnell, gründlich, effizient
- URL: autopsy.com

**The Sleuth Kit (TSK)** — die CLI-Schicht unter Autopsy
- Sammlung von Command-Line-Tools für disk & filesystem analysis
- `fls` (list files), `icat` (extract by inode), `mmls` (partition layout), `mactime` (timeline), `srch_strings` (strings aus Images)
- Skriptbar, in eigene Pipelines integrierbar
- URL: sleuthkit.org

### File Carving

**Foremost / Scalpel / Photorec** — gelöschte Files aus unallokiertem Speicher rekonstruieren
- Foremost: Klassiker, header/footer-basiert
- Scalpel: schneller, optimiert für große Disks
- Photorec: ignoriert Filesystem komplett, sehr gründlich
- Testdisk: Partitions-Wiederherstellung

### Memory Forensik

**Volatility** — der Standard für RAM-Dump-Analyse
- "The world's most widely used memory forensics platform" (volatilityfoundation.org)
- Von Law Enforcement, Military, Academia und kommerziellen Investigatoren genutzt
- Plugins für Process-Liste, Netzwerk-Connections, Registry-Hives, Malware-Detection

### Malware-/Pattern-Matching

**YARA** — Pattern-Matching-Swiss-Knife für Malware-Familien
- "The pattern matching swiss knife for malware researchers" (virustotal.github.io/yara)
- Definiere Malware-Familien anhand Text-/Binary-Patterns
- Wird von Virustotal, FireEye, CrowdStrike, GitHub-Secret-Scanning genutzt
- YARA-Regeln sind das Industry-Format für Indicator-Sharing

### PDF-Forensik

**pdfid** + **pdf-parser** — scannt PDFs auf verdächtige Objekte (JavaScript, eingebettete Files, Auto-Actions)

---

## 3. Live verifizierte Verfügbarkeit (Kali 2026.2)

| Tool | In Kali Repo | Status |
|---|---|---|
| guymager | ✅ | Version 0.8.13 (laut Upstream) |
| autopsy | ✅ | Aktuelle Sleuth Kit Labs Distribution |
| sleuthkit | ✅ | Vollständige CLI-Suite |
| volatility | ✅ (v2/v3) | Python 3.11-kompatibel seit 2023.1 |
| yara | ✅ | v4.x |
| bulk_extractor | ✅ | Aktives Projekt |
| binwalk | ✅ | v2.x / binwalk3 |
| pdfid / pdf-parser | ✅ | Didier Stevens Suite |

---

## 4. Klassischer Forensik-Workflow (Cooked)

```
1. SICHERN
   - Zielsystem NICHT mounten (Live-System)
   - RAM-Dump:  sudo avml /mnt/usb/memdump.raw
                 oder: sudo liME acquisition
   - Disk-Image: guymager → E01 mit SHA256-Hash

2. UNTERSUCHEN (am sauberen Forensic-Workstation)
   - Image einlesen:  ewfmount image.E01 /mnt/ewf
   - Partition-Layout: mmls /mnt/ewf/image.raw
   - Filesystem:      fsstat /mnt/ewf/image.raw
   - Files listen:    fls -r /mnt/ewf/image.raw
   - Timeline:        mactime -b body.csv -d > timeline.csv
   - Strings:         srch_strings -a image.raw > strings.txt
   - Carving:         foremost -i image.raw -o carved/
   - YARA-Scan:       yara -r rules.yar /mnt/ewf/

3. ANALYSIEREN
   - Autopsy GUI → Cases, Tags, Reports
   - Volatility → plugins für Process/Malware-Detection
   - Obsidian → Notes, Verlinkungen, Timeline-View

4. REPORTEN
   - cherrytree → hierarchische Notes
   - dradis → Team-Kollaboration
   - obsidian → Markdown-Investigation-Reports
```

---

## 5. Was Kali hier besser macht als CAINE/DEFT

- **Toolset-Breite:** Alle Sub-Kategorien in einer Live-Distro (Imaging + Carving + Sleuth Kit + Memory + PDFs)
- **Maintenance:** Kali wird aktiv gepflegt, monatliche Releases, Rolling Release
- **Duales Profil:** Forensik + offensive Tools in einem Image — praktisch für Investigatoren, die auch Malware analysieren
- **Tool-Vielfalt:** Sleuth Kit Suite (~30 Binaries) ist konkurrenzlos tief

---

## 6. Wenn du nur EIN Tool lernen willst

**Autopsy.** Es ist die GUI, die alle Sleuth-Kit-Tools unter einer Oberfläche konsolidiert, Cases/Tags/Reports built-in hat, und mit der du 90% aller Disk-Forensik-Cases erledigen kannst. Die CLI (`fls`, `icat`, `mmls`, `mactime`) lernst du dann on-demand, wenn du Automatisierung brauchst.

Für Memory-Forensik: **Volatility 3** (Python-basiert, moderner als v2).

---

## 7. Quellen (7 verifiziert)

1. Kali Tools — Offizielle Tool-Übersicht · kali.org · https://www.kali.org/tools/
2. TheLinuxCode — Kali Linux: Definitive Guide to Forensic Tools · thelinuxcode.com · https://thelinuxcode.com/kali_linux_forensics_tools/
3. Autopsy — Digital Forensics · autopsy.com · https://www.autopsy.com/
4. The Sleuth Kit · sleuthkit.org · https://www.sleuthkit.org/
5. Volatility Foundation · volatilityfoundation.org · https://www.volatilityfoundation.org/
6. YARA · virustotal.github.io/yara · https://virustotal.github.io/yara/
7. Guymager · guymager.sourceforge.net · https://guymager.sourceforge.net/

---

*Recherche-Dauer: ~3 min · 7 Quellen live verifiziert · Read-only*
