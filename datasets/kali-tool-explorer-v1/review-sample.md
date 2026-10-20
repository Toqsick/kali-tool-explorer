# Kali Tool Explorer — Review-Stichprobe
> 26 von 131 Tools (19.8 %), stratifiziert über Modi und Kategorien. Bitte pro Tool die vier Checks und eine Entscheidung eintragen. Der Fragenkatalog mit Entscheidungsregeln steht im [Review Runbook](REVIEW.md). Die maschinenlesbare Quelle ist `kali-review-sample.jsonl`; die Tabelle `kali-review-sample.csv` enthält dieselben Felder.

## Wie ausfüllen

- **Beschreibung:** korrekt, verständlich, nicht irreführend?
- **Command:** syntaktisch und fachlich richtig? `unverified` ist der Ausgangszustand, kein Fehler.
- **Tags/Achsen:** passen die normalisierten Achsen und die Roh-Tags?
- **Safety:** sind `dual-use`/`defensiv` und das Risk-Level angemessen?
- **Entscheidung:** `accept`, `fix` oder `reject`; bei `fix`/`reject` bitte eine kurze Notiz.
- **Agent:** vorausgefüllter Konsistenz-Check; **Cmd verifiziert** zeigt, ob mindestens ein Command per `--help` geprüft wurde.

## Übersicht

| # | Tool | Modus | Kategorie | Risk | Safety | Agent | Cmd verifiziert | Entscheidung |
|---:|---|---|---|---|---|---|---|---|
| 1 | `apparmor` | purple | protect | low | defensive | pass | ja | offen |
| 2 | `arkime` | purple | detect | medium | defensive | pass | nein | offen |
| 3 | `arpspoof` | blue | sniffing-spoofing | medium | dual-use | pass | nein | offen |
| 4 | `autorecon` | purple | identify | low | defensive | pass | nein | offen |
| 5 | `chisel` | blue | post-exploitation | high | dual-use | pass | nein | offen |
| 6 | `defectdojo` | purple | govern | low | defensive | pass | nein | offen |
| 7 | `exploitdb` | blue | exploitation | high | dual-use | pass | nein | offen |
| 8 | `fail2ban` | purple | protect | low | defensive | pass | nein | offen |
| 9 | `falco` | purple | detect | medium | defensive | pass | nein | offen |
| 10 | `ffuf` | blue | web-app-analysis | medium | dual-use | pass | nein | offen |
| 11 | `foremost` | blue | forensik | medium | dual-use | pass | nein | offen |
| 12 | `gdb` | blue | reverse-engineering | medium | dual-use | pass | nein | offen |
| 13 | `gobuster` | blue | web-app-analysis | medium | dual-use | pass | nein | offen |
| 14 | `guymager` | blue | forensik | medium | dual-use | pass | nein | offen |
| 15 | `gvm` | blue/purple | vulnerability-analysis | medium | dual-use | pass | nein | offen |
| 16 | `impacket-scripts` | blue | post-exploitation | high | dual-use | pass | nein | offen |
| 17 | `john` | blue | password-attacks | high | dual-use | pass | nein | offen |
| 18 | `kismet` | blue | wireless-attacks | high | dual-use | pass | nein | offen |
| 19 | `ltrace` | blue | reverse-engineering | medium | dual-use | pass | nein | offen |
| 20 | `nmap` | blue/purple | info-gathering | medium | dual-use | pass | nein | offen |
| 21 | `reaver` | blue | wireless-attacks | high | dual-use | pass | nein | offen |
| 22 | `recordmydesktop` | blue | reporting | low | dual-use | pass | nein | offen |
| 23 | `rsync` | purple | recover | low | defensive | pass | nein | offen |
| 24 | `thehive` | purple | respond | medium | defensive | pass | nein | offen |
| 25 | `tnscmd10g` | blue | database-assessment | medium | dual-use | pass | nein | offen |
| 26 | `wireshark` | blue | info-gathering | medium | dual-use | pass | nein | offen |

## Die 26 Tools

### 1. AppArmor (`apparmor`)

**Modus:** purple · **Kategorie:** protect · **Risk:** low · **Safety:** defensive · **Agent:** pass · **Cmd verifiziert:** ja

**Beschreibung:** Mandatory-Access-Control — Prozess-Sandboxing.

**Primärer Command:** `aa-status`

**Roh-Tags:** MAC, Linux

**Achsen:** hardening

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 2. Arkime (Moloch) (`arkime`)

**Modus:** purple · **Kategorie:** detect · **Risk:** medium · **Safety:** defensive · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Full-Packet-Capture + Index + Search. Cluster-fähig.

**Primärer Command:** `arkime-config`

**Roh-Tags:** PCAP, Search

**Achsen:** forensics, network, recon, threat-detection

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 3. arpspoof (`arpspoof`)

**Modus:** blue · **Kategorie:** sniffing-spoofing · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** ARP-Cache-Poisoning — Klassiker für LAN-MitM.

**Primärer Command:** `arpspoof -i eth0 -t 192.168.1.10 192.168.1.1`

**Roh-Tags:** ARP, MitM

**Achsen:** network

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 4. autorecon (`autorecon`)

**Modus:** purple · **Kategorie:** identify · **Risk:** low · **Safety:** defensive · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Multi-threaded-Recon — erkennt automatisch Services + Tests.

**Primärer Command:** `autorecon 10.10.10.5`

**Roh-Tags:** Recon, Automated

**Achsen:** asset-management, recon

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 5. chisel (`chisel`)

**Modus:** blue · **Kategorie:** post-exploitation · **Risk:** high · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** TCP/UDP-Tunnel über HTTP. Schnelles Pivoting.

**Primärer Command:** `chisel server -p 8000 --reverse`

**Roh-Tags:** Pivoting, Tunnel

**Achsen:** network, post-exploitation, vpn

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 6. DefectDojo (`defectdojo`)

**Modus:** purple · **Kategorie:** govern · **Risk:** low · **Safety:** defensive · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Vulnerability-Management-Platform — korreliert Scans über Teams.

**Primärer Command:** `defectdojo-start`

**Roh-Tags:** VulnMgmt, Reporting

**Achsen:** governance, reporting, scanning

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 7. Exploit-DB (`exploitdb`)

**Modus:** blue · **Kategorie:** exploitation · **Risk:** high · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Datenbank verifizierter Exploits und Proof-of-Concepts.

**Primärer Command:** `searchsploit -t vsftpd`

**Roh-Tags:** Exploit-DB, Database

**Achsen:** database, exploitation

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 8. fail2ban (`fail2ban`)

**Modus:** purple · **Kategorie:** protect · **Risk:** low · **Safety:** defensive · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Blockiert IPs nach fehlgeschlagenen Login-Versuchen.

**Primärer Command:** `fail2ban-client status sshd`

**Roh-Tags:** Bruteforce, Defense

**Achsen:** credentials, hardening, threat-detection

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 9. Falco (`falco`)

**Modus:** purple · **Kategorie:** detect · **Risk:** medium · **Safety:** defensive · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Runtime-Security-Detection mit eBPF. Container/K8s-nativ.

**Primärer Command:** `falco -k https://your-api-key`

**Roh-Tags:** Runtime, eBPF, Containers

**Achsen:** container, threat-detection

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 10. ffuf (`ffuf`)

**Modus:** blue · **Kategorie:** web-app-analysis · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Ultraschneller Web-Fuzzer. Multithreaded, viele Protokolle.

**Primärer Command:** `ffuf -u https://target.com/FUZZ -w wordlist.txt`

**Roh-Tags:** Fuzz, Web, Fast

**Achsen:** fuzzing, web

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 11. foremost (`foremost`)

**Modus:** blue · **Kategorie:** forensik · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Original von US Air Force OSI. Header/Footer-basiert. Audit-Log mit Offsets und Größen.

**Primärer Command:** `foremost -i image.raw -o carved/ -T`

**Roh-Tags:** Header/Footer, Audit-Log

**Achsen:** forensics, governance, siem

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 12. gdb (`gdb`)

**Modus:** blue · **Kategorie:** reverse-engineering · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** GNU-Debugger — Standard für Runtime-Analyse.

**Primärer Command:** `gdb ./binary -ex 'break main' -ex run`

**Roh-Tags:** Debugger, Analysis

**Achsen:** reverse-engineering

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 13. gobuster (`gobuster`)

**Modus:** blue · **Kategorie:** web-app-analysis · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Schneller Directory/Subdomain-Buster (Go-Implementierung).

**Primärer Command:** `gobuster dir -u https://target.com -w wordlist.txt`

**Roh-Tags:** Web, Fuzz, Fast

**Achsen:** fuzzing, web

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 14. guymager (`guymager`)

**Modus:** blue · **Kategorie:** forensik · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** GUI-Klassiker für Disk-Imaging. Multi-threaded, parallel MD5/SHA1/SHA256. Generiert dd, E01 und AFF.

**Primärer Command:** `guymager`

**Roh-Tags:** GUI, E01, AFF, Hash

**Achsen:** credentials, disk, forensics

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 15. gvm (Greenbone) (`gvm`)

**Modus:** blue/purple · **Kategorie:** vulnerability-analysis · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Open-Source Vulnerability Management — ehemals OpenVAS. Industrie-Standard-Scanner.

**Primärer Command:** `gvm-start && gvm-cli -h`

**Roh-Tags:** Vuln-Scan, Compliance, Gold, Vuln

**Achsen:** asset-management, governance, hardening, scanning

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 16. impacket-scripts (`impacket-scripts`)

**Modus:** blue · **Kategorie:** post-exploitation · **Risk:** high · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Python-Tools für Windows-Protokolle: psexec, wmiexec, secretsdump.

**Primärer Command:** `impacket-psexec domain/user:pass@10.10.10.5`

**Roh-Tags:** Windows, AD, PTH

**Achsen:** active-directory, credentials, post-exploitation

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 17. John the Ripper (`john`)

**Modus:** blue · **Kategorie:** password-attacks · **Risk:** high · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Klassischer Passwort-Cracker. Viele Hash-Formate.

**Primärer Command:** `john --wordlist=rockyou.txt hashes.txt`

**Roh-Tags:** Cracking, Hash, Classic

**Achsen:** credentials

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 18. kismet (`kismet`)

**Modus:** blue · **Kategorie:** wireless-attacks · **Risk:** high · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Wireless-Network-Detector + Sniffer + IDS.

**Primärer Command:** `kismet`

**Roh-Tags:** WiFi, Sniffer, Detection

**Achsen:** network, threat-detection, wireless

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 19. ltrace (`ltrace`)

**Modus:** blue · **Kategorie:** reverse-engineering · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Trace-Bibliotheks-Aufrufe zur Laufzeit.

**Primärer Command:** `ltrace ./binary`

**Roh-Tags:** Trace, Dynamic

**Achsen:** network, reverse-engineering

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 20. nmap (`nmap`)

**Modus:** blue/purple · **Kategorie:** info-gathering · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Der Netzwerk-Scanner Nr. 1. Port-Scan, Service-Erkennung, OS-Fingerprinting.

**Primärer Command:** `nmap -sV -sC -A target.com`

**Roh-Tags:** Network, Scanner, Recon, Asset, Daily

**Achsen:** asset-management, network, recon, scanning

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 21. reaver (`reaver`)

**Modus:** blue · **Kategorie:** wireless-attacks · **Risk:** high · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** WPS-PIN-Brute-Force-Angriff gegen Router.

**Primärer Command:** `reaver -i wlan0 -b AA:BB:CC:DD:EE:FF -vv`

**Roh-Tags:** WPS, Bruteforce

**Achsen:** credentials, wireless

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 22. recordmydesktop (`recordmydesktop`)

**Modus:** blue · **Kategorie:** reporting · **Risk:** low · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Desktop-Recorder für Demonstrationen.

**Primärer Command:** `recordmydesktop`

**Roh-Tags:** Recording, Demo

**Achsen:** reporting

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 23. rsync (`rsync`)

**Modus:** purple · **Kategorie:** recover · **Risk:** low · **Safety:** defensive · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Inkrementelles Backup mit Delta-Transfer.

**Primärer Command:** `rsync -avz /data/ backup:/backup/`

**Roh-Tags:** Backup, Sync

**Achsen:** backup

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 24. TheHive (`thehive`)

**Modus:** purple · **Kategorie:** respond · **Risk:** medium · **Safety:** defensive · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Incident-Response-Platform. Cases + Tasks + Observables.

**Primärer Command:** `thehive-start`

**Roh-Tags:** IR, Case-Mgmt, Gold

**Achsen:** incident-response, reporting

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 25. tnscmd10g (`tnscmd10g`)

**Modus:** blue · **Kategorie:** database-assessment · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Oracle-TNS-Listener-Befehle senden.

**Primärer Command:** `tnscmd10g status -h 10.10.10.5`

**Roh-Tags:** Oracle, Recon

**Achsen:** database, recon

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

### 26. wireshark (`wireshark`)

**Modus:** blue · **Kategorie:** info-gathering · **Risk:** medium · **Safety:** dual-use · **Agent:** pass · **Cmd verifiziert:** nein

**Beschreibung:** Der Standard-Netzwerk-Protokoll-Analyzer. Live-Capture + Deep-Dive in Pakete.

**Primärer Command:** `wireshark -i eth0 -k`

**Roh-Tags:** Network, Sniffer, GUI, Gold

**Achsen:** network, recon

- [ ] Beschreibung korrekt
- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)
- [ ] Tags/Achsen passend
- [ ] Safety-Klassifikation passend
- **Entscheidung:** `offen` → `accept` / `fix` / `reject`
- **Notizen:**

---

## Nach der Abnahme

Sag Bescheid, wenn die Stichprobe durch ist. Dann übernehme ich die Entscheidungen in `kali-review-sample.jsonl` und `kali-review-sample.csv` und ziehe den [Dataset-Qualitätsbericht](quality-report.md) nach.

## Links

- [Dataset README](README.md)
- [Safety Policy](SAFETY.md)
- [Quality Report](quality-report.md)
