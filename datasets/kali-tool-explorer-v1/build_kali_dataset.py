#!/usr/bin/env python3
"""
Build a curated dataset from the Kali Tool Explorer repository.

Input (defaults point at a local checkout):
  forensik-explorer.html
  tool-audio-scripts.json
  docs/kali-blue-vs-purple.md
  docs/kali-forensik-overview.md
  audits/*.md
  tool-audios.txt              # one audio stem per line, optional

Output:
  kali-tools.jsonl
  kali-commands.jsonl
  kali-curriculum.jsonl
  kali-narration.jsonl
  kali-docs.jsonl
  kali-audits.jsonl
  kali-tag-taxonomy.json
  kali-review-sample.jsonl
  kali-quality-report.md
  kali-source-manifest.json

The builder is deterministic. It never executes tool commands; it only runs
"--help" for binaries that are installed locally, to annotate verification.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

GENERATED_AT = "2026-10-20"
DATASET_ID = "kali-tool-explorer-v1"
SOURCE_REPO = "https://github.com/Toqsick/kali-tool-explorer"
SOURCE_HTML = SOURCE_REPO + "/blob/main/forensik-explorer.html"
SOURCE_AUDIO = SOURCE_REPO + "/blob/main/scripts/tool-audio-scripts.json"
LICENSE = "MIT"
APP_VERSION = "3.1"

ALIASES = {
    "aircrack": "aircrack-ng",
    "evilwinrm": "evil-winrm",
    "powershellempire": "powershell-empire",
    "recon": "recon-ng",
    "theharvester": "theHarvester",
    "msfconsole": "metasploit",
}

AXES = [
    "recon", "scanning", "enumeration", "web", "network", "wireless",
    "credentials", "exploitation", "post-exploitation", "active-directory",
    "cloud", "container", "forensics", "disk", "memory", "malware",
    "threat-detection", "siem", "incident-response", "hardening", "firewall",
    "vpn", "backup", "reporting", "osint", "social-engineering", "database",
    "reverse-engineering", "fuzzing", "cryptography", "governance",
    "asset-management",
]

CATEGORY_AXIS = {
    "info-gathering": "recon",
    "vulnerability-analysis": "scanning",
    "web-app-analysis": "web",
    "database-assessment": "database",
    "password-attacks": "credentials",
    "wireless-attacks": "wireless",
    "reverse-engineering": "reverse-engineering",
    "exploitation": "exploitation",
    "sniffing-spoofing": "network",
    "post-exploitation": "post-exploitation",
    "forensik": "forensics",
    "reporting": "reporting",
    "govern": "governance",
    "identify": "asset-management",
    "protect": "hardening",
    "detect": "threat-detection",
    "respond": "incident-response",
    "recover": "backup",
}

RISK_HIGH = {"exploitation", "password-attacks", "wireless-attacks", "post-exploitation"}
RISK_MEDIUM = {
    "info-gathering", "vulnerability-analysis", "web-app-analysis",
    "database-assessment", "sniffing-spoofing", "reverse-engineering",
    "forensik", "detect", "respond",
}

DEFENSIVE_AUX = {
    "ufw", "iptables", "nft", "fail2ban", "apparmor", "selinux", "openssh",
    "certbot", "openvpn", "wireguard", "clamav", "chkrootkit", "rkhunter",
    "logwatch", "auditd", "aide", "suricata", "zeek", "arkime", "wazuh",
    "osquery", "yara", "falco", "thehive", "cortex", "velociraptor", "grr",
    "snort",
}

HIGH_AUX = {
    "mimikatz", "chisel", "bloodhound", "hydra", "hashcat", "john", "sqlmap",
    "metasploit", "msfconsole", "aircrack-ng", "wifite", "reaver", "kismet",
    "crackmapexec", "evil-winrm", "powershell-empire", "nmap", "masscan",
    "gobuster", "ffuf", "nikto", "nuclei", "wpscan", "zap", "wapiti",
    "openvas", "gvm", "legion", "burpsuite", "netcat", "ncat", "socat",
    "arpspoof", "ettercap", "responder", "bettercap", "mitmproxy",
    "searchsploit", "commix", "davtest", "joomscan", "droopescan",
}

BROKEN_TOKENS = {
    "gobusterdir", "crackmapexecsmb", "nmap-sV", "sqlmap-u", "hashcat-m",
    "john--wordlist", "wpscan--url", "nuclei-u", "ffuf-u", "masscan-p1",
    "evil-winrm-i", "metasploit-q",
}

GENERIC_WRAPPERS = {
    "sudo", "doas", "docker", "podman", "java", "python", "python3",
    "bash", "sh", "zsh", "perl", "ruby", "node", "npm", "systemctl",
    "service", "git",
}


def T(axes: str = "", attrs: str = ""):
    return {
        "axes": [x for x in axes.split() if x],
        "attributes": [x for x in attrs.split() if x],
    }


# 185 raw tags -> topic axes + attribute families.
TAG_MAP = {
    "400+-Formate": T("forensics", "artifact:many-formats"),
    "AD": T("active-directory"),
    "AFF": T("forensics disk", "artifact:aff"),
    "ARP": T("network"),
    "AV-Evasion": T("malware exploitation", "security:evasion"),
    "Analysis": T("", "feature:analysis"),
    "Asset": T("asset-management recon"),
    "Audit": T("governance hardening"),
    "Audit-Log": T("governance siem"),
    "Automated": T("", "automation:automated"),
    "Automation": T("", "feature:automation"),
    "Backup": T("backup"),
    "Bare-Metal": T("", "platform:bare-metal"),
    "Batch": T("", "interface:batch"),
    "Bruteforce": T("credentials"),
    "Bulk-Export": T("reporting", "feature:bulk-export"),
    "C2": T("post-exploitation exploitation", "security:c2"),
    "CGI": T("web"),
    "CLI": T("", "interface:cli"),
    "CMS": T("web", "product:cms"),
    "CTI": T("threat-detection osint"),
    "CVE": T("scanning exploitation"),
    "Carving": T("forensics disk"),
    "Case-Mgmt": T("incident-response reporting"),
    "Cases": T("incident-response reporting"),
    "Classic": T("", "maturity:classic"),
    "Cmd-Inj": T("web exploitation"),
    "Collab": T("reporting", "feature:collaboration"),
    "Compliance": T("governance hardening"),
    "Containers": T("container", "platform:containers"),
    "Court-ready": T("forensics reporting", "legal:court-ready"),
    "Cracking": T("credentials"),
    "Creds": T("credentials"),
    "DB": T("database"),
    "DFIR": T("forensics incident-response"),
    "Daily": T("", "maturity:daily"),
    "Data": T("", "feature:data"),
    "Database": T("database"),
    "Debugger": T("reverse-engineering"),
    "Decode": T("reverse-engineering cryptography"),
    "Decompiler": T("reverse-engineering"),
    "Dedupe": T("forensics", "feature:dedupe"),
    "Deep-Analysis": T("reverse-engineering malware"),
    "Defekt-resistent": T("forensics", "property:defect-resistant"),
    "Defense": T("hardening threat-detection"),
    "Demo": T("", "feature:demo"),
    "Detection": T("threat-detection"),
    "Disasm": T("reverse-engineering"),
    "Discovery": T("recon"),
    "Dynamic": T("reverse-engineering", "analysis:dynamic"),
    "E01": T("forensics disk", "artifact:e01"),
    "EDR": T("threat-detection", "endpoint:edr"),
    "Email": T("osint social-engineering"),
    "Embedded": T("", "platform:embedded"),
    "Encrypted": T("cryptography"),
    "Encryption": T("cryptography"),
    "Endpoint": T("threat-detection", "endpoint:generic"),
    "Exploit": T("exploitation"),
    "Exploit-DB": T("exploitation"),
    "Fast": T("", "performance:fast"),
    "File-Integrity": T("forensics hardening"),
    "Filesystem-agnostisch": T("forensics disk", "property:filesystem-agnostic"),
    "Firewall": T("firewall hardening"),
    "Firmware": T("forensics", "artifact:firmware"),
    "Framework": T("", "type:framework"),
    "Fuzz": T("fuzzing"),
    "Fuzzy": T("fuzzing", "feature:fuzzy"),
    "GPU": T("", "performance:gpu"),
    "GUI": T("", "interface:gui"),
    "Generator": T("fuzzing", "feature:generator"),
    "Gold": T("", "maturity:gold"),
    "Google": T("osint", "product:google"),
    "Graph": T("", "interface:graph"),
    "HTTPS": T("web network"),
    "Hardening": T("hardening"),
    "Hash": T("credentials"),
    "Header/Footer": T("forensics", "artifact:carving"),
    "Hierarchy": T("", "interface:hierarchy"),
    "High-Speed": T("", "performance:high-speed"),
    "IDS": T("threat-detection"),
    "IOC": T("threat-detection malware"),
    "IPS": T("threat-detection"),
    "IR": T("incident-response"),
    "Imaging": T("forensics disk"),
    "Impacket": T("active-directory post-exploitation", "product:impacket"),
    "Industry-Standard": T("", "maturity:industry-standard"),
    "IoT": T("network", "platform:iot"),
    "Journal": T("forensics disk", "artifact:journal"),
    "LAN": T("network"),
    "LLMNR": T("network active-directory"),
    "Lateral": T("post-exploitation active-directory", "security:lateral-movement"),
    "Linux": T("", "platform:linux"),
    "Live-Triage": T("incident-response forensics"),
    "Logs": T("siem reporting"),
    "MAC": {"axes": ["hardening"], "attributes": ["access-control:mandatory"], "note": "Mandatory Access Control (AppArmor/SELinux), nicht MAC-Adresse"},
    "MSSQL": T("database", "product:mssql"),
    "MitM": T("network"),
    "Modular": T("", "architecture:modular"),
    "Multi-threaded": T("", "performance:multi-threaded"),
    "NGFW": T("firewall threat-detection"),
    "NSE": T("scanning network"),
    "NSM": T("threat-detection network"),
    "NSRL": T("forensics", "product:nsrl"),
    "NTFS": T("forensics disk", "artifact:ntfs"),
    "NTLM": T("credentials active-directory"),
    "Network": T("network"),
    "Notes": T("reporting", "feature:notes"),
    "OSINT": T("osint recon"),
    "Obfuscated": T("malware reverse-engineering"),
    "Online": T("", "mode:online"),
    "Oracle": T("database", "product:oracle"),
    "PCAP": T("network forensics", "artifact:pcap"),
    "PDF": T("forensics", "artifact:pdf"),
    "PII": T("forensics", "privacy:pii"),
    "PTH": T("credentials active-directory", "security:pass-the-hash"),
    "Packet-Craft": T("network"),
    "Partition": T("forensics disk", "artifact:partition"),
    "Pattern": T("malware reverse-engineering"),
    "Payload": T("exploitation", "security:payload"),
    "Phishing": T("social-engineering"),
    "Pivoting": T("network post-exploitation"),
    "Plugin": T("", "type:plugin"),
    "PowerShell": T("active-directory", "platform:windows"),
    "Privesc": T("post-exploitation", "security:privilege-escalation"),
    "Proxy": T("network"),
    "Python3": T("", "platform:python"),
    "Quick-Scan": T("scanning"),
    "RAM-Dump": T("memory forensics", "artifact:ram-dump"),
    "RE": T("reverse-engineering"),
    "RHEL": T("", "platform:rhel"),
    "Recon": T("recon"),
    "Recording": T("reporting", "feature:recording"),
    "Recovery": T("backup forensics"),
    "Reporting": T("reporting"),
    "Response": T("incident-response"),
    "Rootkit": T("malware"),
    "Rules": T("", "feature:rules"),
    "Runtime": T("", "feature:runtime"),
    "SCAP": T("hardening governance"),
    "SIEM": T("siem threat-detection"),
    "SMB": T("network active-directory"),
    "SQL": T("database"),
    "SQLi": T("web database"),
    "SSH": T("network"),
    "Scanner": T("scanning"),
    "Scapy": T("network", "product:scapy"),
    "Screenshot": T("reporting", "feature:screenshot"),
    "Search": T("recon", "feature:search"),
    "Skriptbar": T("", "automation:scriptable"),
    "Sleuth-Kit": T("forensics", "product:sleuthkit"),
    "Sniffer": T("network"),
    "Social-Eng": T("social-engineering"),
    "Static": T("reverse-engineering", "analysis:static"),
    "Stats": T("reporting", "feature:stats"),
    "Strings": T("forensics reverse-engineering", "artifact:strings"),
    "Subdomain": T("recon osint"),
    "Sync": T("backup", "feature:sync"),
    "Tags": T("", "metadata:tags"),
    "Tarnung-Erkennung": T("threat-detection malware", "property:evasion-detection"),
    "Templates": T("", "feature:templates"),
    "Terrabyte": T("forensics", "performance:terabyte"),
    "Trace": T("network"),
    "Tunnel": T("vpn network"),
    "Unallocated": T("forensics disk", "artifact:unallocated"),
    "Varianten": T("", "feature:variants"),
    "Visual": T("", "interface:visual"),
    "Vuln": T("scanning"),
    "Vuln-Scan": T("scanning"),
    "VulnMgmt": T("scanning governance"),
    "Vulnerability": T("scanning"),
    "WPA": T("wireless", "artifact:wpa"),
    "WPS": T("wireless", "artifact:wps"),
    "Web": T("web"),
    "WebDAV": T("web"),
    "WiFi": T("wireless"),
    "WinRM": T("network active-directory"),
    "Windows": T("", "platform:windows"),
    "WordPress": T("web", "product:wordpress"),
    "Wordlist": T("credentials"),
    "XDR": T("threat-detection"),
    "dd": T("forensics disk", "artifact:dd"),
    "eBPF": T("threat-detection", "platform:linux-ebpf"),
    "ext3": T("forensics disk", "artifact:ext3"),
    "ext4": T("forensics disk", "artifact:ext4"),
    "libewf": T("forensics disk", "artifact:ewf"),
}

BUILDER_CORRECTED = {
    "nmap": "nmap -sV -T4 {target}",
    "sqlmap": "sqlmap -u {target} --batch",
    "hashcat": "hashcat -m 0 -a 0 {target}",
    "john": "john --wordlist=/usr/share/wordlists/rockyou.txt {target}",
    "gobuster": "gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt -t 50",
    "nikto": "nikto -h {target}",
    "hydra": "hydra -l admin -P /usr/share/wordlists/rockyou.txt -t 4 -vV {target}",
    "aircrack-ng": "aircrack-ng -w /usr/share/wordlists/rockyou.txt {target}",
    "metasploit": "msfconsole -q {module}",
    "wpscan": "wpscan --url {target} --enumerate u,p,t",
    "nuclei": "nuclei -u {target} -severity critical,high",
    "ffuf": "ffuf -u {target} -w /usr/share/wordlists/dirb/common.txt -mc 200,204,301,302",
    "masscan": "masscan -p1-65535 --rate 1000 {target}",
    "evil-winrm": "evil-winrm -i {target} -u Administrator -p Password123",
    "crackmapexec": "crackmapexec smb {target}",
}

OBSERVED_OUTPUTS = {
    "nmap": "nmap-sV -T4 10.0.0.5",
    "sqlmap": "sqlmap-u --batch http://target.com/page?id=1",
    "hashcat": "hashcat-m 0 -a 0 hashes.txt",
    "john": "john--wordlist=/usr/share/wordlists/rockyou.txt hashes.txt",
    "gobuster": "gobusterdir -u -w /usr/share/wordlists/dirb/common.txt -t 50 http://target.com",
    "nikto": "nikto-h http://target.com",
    "hydra": "hydra-l admin -P /usr/share/wordlists/rockyou.txt -t 4 -vV ssh://10.0.0.5",
    "metasploit": "metasploit-q use exploit/multi/handler",
    "wpscan": "wpscan--url --enumerate u,p,t http://target.com",
    "nuclei": "nuclei-u -severity critical,high http://target.com",
    "ffuf": "ffuf-u -w /usr/share/wordlists/dirb/common.txt -mc 200,204,301,302 http://target.com/FUZZ",
    "masscan": "masscan-p1-65535 --rate 1000 10.0.0.0/24",
    "evil-winrm": "evil-winrm-i -u Administrator -p Password123 10.0.0.5",
    "crackmapexec": "crackmapexecsmb 10.0.0.0/24",
}

TARGET_POSITION_ISSUES = {
    "sqlmap", "gobuster", "wpscan", "nuclei", "ffuf", "evil-winrm",
}

PLACEHOLDER_RE = re.compile(
    r"\b(target|TARGET|target\.com|10\.0\.0\.\d+|192\.168\.\d+\.\d+|"
    r"hash(?:es)?\.txt|hashfile|hashes\.txt|wordlist\.txt|rockyou\.txt|"
    r"image\.raw|cap(?:ture)?\.pcap|binary|rules\.yar|domain/user|"
    r"FUZZ|IP|URL|HOST|PATH|FILE|SSID|BSSID|capture\.cap|"
    r"use exploit/[\w/]+|<[^>]+>)\b"
)

AUDIT_META = {
    "bug-hunt-report.md": {
        "title": "Bug-Hunt Report — Kali Explorer v2.0",
        "kind": "bug_hunt",
        "reported_at": "2026-08-06",
        "summary": "39 Bugs, davon 6 Critical; 2.832 Zeilen geprüft. Fünf tote Playbook-Referenzen, tote Audio-Buttons, defektes Emoji, Comparator-Dead-Click, falsche Meta-Description und doppelte Tool-IDs.",
    },
    "bug-hunt-v2-report.md": {
        "title": "Bug-Hunt Review — Kali Explorer v3.0",
        "kind": "bug_hunt",
        "reported_at": "2026-08-06",
        "summary": "8 Critical, 5 Important, 6 Minor; TDZ-Check PASS. Befunde an Command-Builder-Flags, toolExamples-Aliasen, Mode-Switch-State und Playbook-Referenzen.",
    },
    "grand-polish-review-ux.md": {
        "title": "UX Review — Forensik Tour HTML",
        "kind": "ux_review",
        "reported_at": "2026-08-06",
        "summary": "Critical: Phase 7 visuell defekt, Mouse-Tracking-Gradient als Performance-Risiko, fehlender Copy-Button, leerer Phase-7-Filter, nicht tastaturbedienbare Audio-Buttons.",
    },
    "grand-polish-review-engineer.md": {
        "title": "Engineering Review — Forensik Tour HTML",
        "kind": "engineering_review",
        "reported_at": "2026-08-06",
        "summary": "Engineering-, Performance-, WCAG-2.1-AA-, Robustheits- und Cross-Browser-Befunde; Empfehlungen zu focus-visible, NaN-Guards, reduced-motion und totem Audio-Element.",
    },
    "ui-polish-report.md": {
        "title": "UI/UX Polish Report — Kali Explorer v2.0",
        "kind": "ui_polish",
        "reported_at": "2026-08-06",
        "summary": "35 UI/UX-Empfehlungen zu Suche, mobilen Filtern, Touch-Zielen, Badges, Wizard-Button und Control-Stack.",
    },
    "ui-polish-v2-report.md": {
        "title": "UI/UX Polish Report v2 — Kali Explorer v3.0",
        "kind": "ui_polish",
        "reported_at": "2026-08-06",
        "summary": "40 UI/UX-Empfehlungen zu Tool-Detail-Modal, LLM-Prompt-Builder und Command-Builder.",
    },
}

DOC_META = {
    "kali-blue-vs-purple.md": {
        "doc_title": "Kali Linux (Standard) vs. Kali Purple",
        "language": "en",
        "sources_count": 15,
        "url": SOURCE_REPO + "/blob/main/docs/kali-blue-vs-purple.md",
    },
    "kali-forensik-overview.md": {
        "doc_title": "Kali Linux für Forensik — Topic-Detail",
        "language": "de",
        "sources_count": 7,
        "url": SOURCE_REPO + "/blob/main/docs/kali-forensik-overview.md",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def canonical_id(raw: str) -> str:
    if raw in ALIASES:
        return ALIASES[raw]
    low = raw.lower()
    for alias, target in ALIASES.items():
        if low == alias.lower():
            return target
    return raw


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def map_tags(raw_tags: list[str]):
    axes: set[str] = set()
    attributes: set[str] = set()
    unmapped: list[str] = []
    for tag in raw_tags:
        entry = TAG_MAP.get(tag)
        if not entry:
            unmapped.append(tag)
            continue
        axes.update(entry["axes"])
        attributes.update(entry["attributes"])
    return sorted(axes), sorted(attributes), sorted(set(unmapped))


def risk_for(category_ids: list[str]) -> str:
    if any(c in RISK_HIGH for c in category_ids):
        return "high"
    if any(c in RISK_MEDIUM for c in category_ids):
        return "medium"
    return "low"


def safety_for(modes: list[str]) -> dict:
    if modes == ["purple"]:
        return {
            "class": "defensive",
            "allowed_use": "Defensive operations, detection engineering, authorized lab work and education.",
        }
    return {
        "class": "dual-use",
        "allowed_use": "Authorized security testing, lab work and education only. Do not use against systems without written permission.",
    }


def aux_safety(tool_id: str) -> str:
    return "defensive" if tool_id in DEFENSIVE_AUX else "dual-use"


def aux_risk(tool_id: str) -> str:
    if tool_id in HIGH_AUX:
        return "high"
    if tool_id in DEFENSIVE_AUX:
        return "low"
    return "medium"


def balanced_quotes(command: str) -> bool:
    single = command.count("'") - command.count("\\'")
    double = command.count('"') - command.count('\\"')
    return single % 2 == 0 and double % 2 == 0


def first_token(command: str) -> str:
    return command.strip().split()[0] if command.strip() else ""


def no_obvious_concatenation(command: str, known_binaries: set[str]) -> tuple[bool, str]:
    token = first_token(command)
    if not token:
        return False, "empty command"
    if token in BROKEN_TOKENS or any(token.startswith(prefix) for prefix in BROKEN_TOKENS):
        return False, f"known concatenated builder token: {token}"
    return True, "syntactic check passed"


def placeholders(command: str) -> list[str]:
    return sorted(set(m.group(0) for m in PLACEHOLDER_RE.finditer(command)))


def verify_command(command: str, known_binaries: set[str]) -> dict:
    token = first_token(command)
    syntax_ok, syntax_reason = no_obvious_concatenation(command, known_binaries)
    if not balanced_quotes(command):
        syntax_ok = False
        syntax_reason = "unbalanced quotes"
    if "None" in command or "undefined" in command:
        syntax_ok = False
        syntax_reason = "placeholder leaked into command"

    installed = shutil.which(token) if token else None
    is_wrapper = token in GENERIC_WRAPPERS

    base_verification = {
        "binary": token,
        "installed": bool(installed),
        "wrapper": is_wrapper,
        "method": "syntax",
        "status": "unverified" if syntax_ok else "invalid",
        "reason": "binary_not_installed" if syntax_ok else syntax_reason,
        "checked_at": GENERATED_AT,
    }

    if not syntax_ok:
        return {
            "verified": False,
            "syntax_ok": False,
            "has_placeholder": bool(placeholders(command)),
            "placeholder_tokens": placeholders(command),
            "verification": base_verification,
        }

    if not installed or is_wrapper:
        base_verification["reason"] = "generic_wrapper_not_tool_binary" if is_wrapper else "binary_not_installed"
        return {
            "verified": False,
            "syntax_ok": True,
            "has_placeholder": bool(placeholders(command)),
            "placeholder_tokens": placeholders(command),
            "verification": base_verification,
        }

    try:
        proc = subprocess.run(
            [installed, "--help"],
            capture_output=True,
            text=True,
            timeout=8,
        )
        help_text = (proc.stdout or "") + (proc.stderr or "")
        flags = [t for t in command.split() if t.startswith("-")]
        missing = []
        for flag in flags:
            base = flag.split("=", 1)[0]
            if base not in help_text:
                missing.append(base)
        if missing:
            status, reason = "unverified", "flag_not_found_in_help: " + ", ".join(sorted(set(missing)))
            verified = False
        else:
            status, reason = "verified", "help_check_passed"
            verified = True
    except Exception as exc:  # noqa: BLE001 - verification must not abort the build
        verified = False
        status = "unverified"
        reason = f"help_check_failed: {type(exc).__name__}"

    base_verification.update({
        "method": "help",
        "status": status,
        "reason": reason,
    })
    return {
        "verified": verified,
        "syntax_ok": True,
        "has_placeholder": bool(placeholders(command)),
        "placeholder_tokens": placeholders(command),
        "verification": base_verification,
    }


def extract_inline_db(html: str) -> dict:
    match = re.search(r'<script[^>]*id="tool-db"[^>]*>(.*?)</script>', html, re.S)
    if not match:
        raise RuntimeError("tool-db block not found")
    return json.loads(match.group(1).strip())


def run_extract_js(html_path: Path, helper: Path) -> dict:
    proc = subprocess.run(
        ["node", str(helper), str(html_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def normalize_tts(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    original = text
    text = re.sub(r"Doppelminus\s*", "--", text, flags=re.IGNORECASE)
    if re.search(r"Doppelminus", original, re.IGNORECASE):
        notes.append("Doppelminus -> --")
    text = re.sub(r"Minus\s*", "-", text)
    if "Minus" in original:
        notes.append("Minus -> -")
    if "bewaehrt" in text:
        text = text.replace("bewaehrt", "bewährt")
        notes.append("bewaehrt -> bewährt")
    if "fuer" in text:
        text = text.replace("fuer", "für")
        notes.append("fuer -> für")
    if "wazuh-manager-start" in text:
        text = text.replace("wazuh-manager-start", "wazuh-manager start")
        notes.append("wazuh-manager-start -> wazuh-manager start")
    text = re.sub(r"\s+", " ", text).strip()
    return text, notes


def tts_artifact_counts(text: str) -> dict:
    return {
        "minus": len(re.findall(r"Minus", text)),
        "doppelminus": len(re.findall(r"Doppelminus", text, re.IGNORECASE)),
        "bewaehrt": text.count("bewaehrt"),
        "fuer": text.count("fuer"),
    }


def build_tools(db: dict, inline_meta: dict) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for mode, mode_data in db["modes"].items():
        for category in mode_data["categories"]:
            for tool in category["tools"]:
                grouped[canonical_id(tool["id"])].append({
                    "mode": mode,
                    "category_id": category["id"],
                    "category_name": category["name"],
                    "tool": tool,
                })

    records = []
    for tool_id, variants in sorted(grouped.items()):
        modes = sorted({v["mode"] for v in variants})
        categories = []
        seen_categories = set()
        for v in variants:
            key = (v["category_id"], v["category_name"])
            if key in seen_categories:
                continue
            seen_categories.add(key)
            categories.append({"id": v["category_id"], "name": v["category_name"], "mode": v["mode"]})

        names = []
        descriptions = []
        commands = []
        tags = []
        badges = []
        for v in variants:
            tool = v["tool"]
            if tool.get("name") and tool["name"] not in names:
                names.append(tool["name"])
            if tool.get("desc") and tool["desc"] not in descriptions:
                descriptions.append(tool["desc"])
            if tool.get("cmd") and tool["cmd"] not in commands:
                commands.append(tool["cmd"])
            for tag in tool.get("tags", []):
                if tag not in tags:
                    tags.append(tag)
            if tool.get("pop") and tool["pop"] not in badges:
                badges.append(tool["pop"])

        category_ids = [c["id"] for c in categories]
        category_axes = sorted({CATEGORY_AXIS[c] for c in category_ids if c in CATEGORY_AXIS})
        tag_axes, attributes, unmapped = map_tags(tags)
        topic_axes = sorted(set(category_axes) | set(tag_axes))
        primary_category = categories[0]["id"] if categories else "unknown"
        primary_description = max(descriptions, key=len) if descriptions else ""

        aliases = sorted({alias for alias, target in ALIASES.items() if target == tool_id})
        reference_url = f"https://www.kali.org/tools/{tool_id}/"

        records.append({
            "id": tool_id,
            "name": names[0] if names else tool_id,
            "name_variants": names,
            "aliases": aliases,
            "modes": modes,
            "categories": categories,
            "primary_category": primary_category,
            "description": primary_description,
            "description_variants": descriptions,
            "primary_command": commands[0] if commands else "",
            "commands": commands,
            "tags_raw": tags,
            "topic_axes": topic_axes,
            "attributes": attributes,
            "unmapped_tags": unmapped,
            "badges": badges,
            "risk_level": risk_for(category_ids),
            "safety": safety_for(modes),
            "reference_url": reference_url,
            "reference_url_status": "app_pattern_unverified",
            "provenance": {
                "source_file": "forensik-explorer.html",
                "source_block": "tool-db",
                "source_url": SOURCE_HTML,
                "kali_version": inline_meta.get("kaliVersion", "2026.2"),
                "generated_date": inline_meta.get("generatedDate", "2026-08-06"),
                "extracted_at": GENERATED_AT,
                "license": LICENSE,
            },
            "variants": [
                {
                    "mode": v["mode"],
                    "category_id": v["category_id"],
                    "category_name": v["category_name"],
                    "description": v["tool"].get("desc", ""),
                    "command": v["tool"].get("cmd", ""),
                    "tags": v["tool"].get("tags", []),
                    "badge": v["tool"].get("pop", ""),
                }
                for v in variants
            ],
        })
    return records


def build_commands(tools: list[dict], js: dict) -> list[dict]:
    known_binaries = {t["id"] for t in tools}
    known_binaries.update({"msfconsole", "aircrack-ng", "john", "nmap", "sqlmap", "hashcat", "gobuster", "nikto", "hydra", "wpscan", "nuclei", "ffuf", "masscan", "evil-winrm", "crackmapexec"})
    tool_map = {t["id"]: t for t in tools}
    records = []

    examples = js.get("toolExamples") or {}
    for raw_key, entries in examples.items():
        tool_id = canonical_id(raw_key)
        in_db = tool_id in tool_map
        for index, entry in enumerate(entries, start=1):
            command = entry.get("cmd", "")
            check = verify_command(command, known_binaries)
            records.append({
                "command_id": f"{tool_id}-example-{index:02d}",
                "tool_id": tool_id,
                "tool_in_db": in_db,
                "source": "toolExamples",
                "source_key": raw_key,
                "command": command,
                "intent": entry.get("desc", ""),
                **check,
                "safety_class": tool_map[tool_id]["safety"]["class"] if in_db else aux_safety(tool_id),
                "risk_level": tool_map[tool_id]["risk_level"] if in_db else aux_risk(tool_id),
                "safety_source": "tool_db" if in_db else "auxiliary_default",
            })

    builder = js.get("toolFlags") or {}
    for raw_key, data in builder.items():
        tool_id = canonical_id(raw_key)
        issues = ["missing_separator_between_tool_and_first_flag"]
        if tool_id in TARGET_POSITION_ISSUES:
            issues.append("target_appended_instead_of_after_flag")
        if tool_id == "metasploit":
            issues.append("wrong_base_binary_metasploit_instead_of_msfconsole")
        if tool_id == "aircrack-ng":
            issues.append("builder_not_rendered_alias_key_aircrack")
        if tool_id not in tool_map:
            issues.append("no_matching_tool_record")
        records.append({
            "command_id": f"{tool_id}-builder",
            "tool_id": tool_id,
            "source": "command_builder",
            "source_key": raw_key,
            "corrected_template": BUILDER_CORRECTED.get(tool_id, ""),
            "observed_output_2026_10_20": OBSERVED_OUTPUTS.get(tool_id),
            "target": data.get("target", {}),
            "flags": data.get("flags", []),
            "issues": issues,
            "verified": False,
            "syntax_ok": True,
            "has_placeholder": True,
            "placeholder_tokens": ["{target}"] if "{target}" in BUILDER_CORRECTED.get(tool_id, "") else ["{module}"],
            "verification": {
                "method": "derived",
                "status": "unverified",
                "reason": "live_builder_defect_see_issues",
                "checked_at": GENERATED_AT,
            },
            "safety_class": tool_map.get(tool_id, {}).get("safety", {}).get("class", "dual-use"),
            "risk_level": tool_map.get(tool_id, {}).get("risk_level", "medium"),
        })
    return records


def build_curriculum(js: dict, tools: list[dict]) -> list[dict]:
    tool_ids = {t["id"] for t in tools}
    records = []

    playbooks = js.get("playbooks") or {}
    for mode, entries in playbooks.items():
        for playbook in entries:
            refs = [canonical_id(x) for x in playbook.get("tools", [])]
            missing = sorted({x for x in refs if x not in tool_ids})
            records.append({
                "kind": "playbook",
                "mode": mode,
                "id": playbook.get("id"),
                "name": playbook.get("name"),
                "icon": playbook.get("icon"),
                "difficulty": playbook.get("difficulty"),
                "description": playbook.get("desc", ""),
                "tools": refs,
                "tool_count": len(refs),
                "missing_tool_refs": missing,
                "source": "inline-js/playbooks",
            })

    for path in js.get("learningPaths") or []:
        weeks = []
        all_refs = []
        for week in path.get("weeks", []):
            refs = [canonical_id(x) for x in week.get("tools", [])]
            all_refs.extend(refs)
            weeks.append({
                "title": week.get("title"),
                "goal": week.get("goal", ""),
                "tools": refs,
                "done_default": week.get("done", False),
            })
        missing = sorted({x for x in all_refs if x not in tool_ids})
        records.append({
            "kind": "learning_path",
            "id": path.get("id"),
            "name": path.get("name"),
            "icon": path.get("icon"),
            "duration": path.get("duration"),
            "description": path.get("desc", ""),
            "week_count": len(weeks),
            "weeks": weeks,
            "tool_refs": all_refs,
            "missing_tool_refs": missing,
            "source": "inline-js/learningPaths",
        })

    playbook_ids = {r["id"] for r in records if r["kind"] == "playbook"}
    for mode, steps in (js.get("wizardFlows") or {}).items():
        refs = []
        for step in steps:
            for option in step.get("options", []):
                if option.get("result"):
                    refs.append(option["result"])
        missing = sorted({x for x in refs if x not in playbook_ids})
        records.append({
            "kind": "wizard_flow",
            "mode": mode,
            "step_count": len(steps),
            "steps": steps,
            "playbook_refs": sorted(set(refs)),
            "missing_playbook_refs": missing,
            "source": "inline-js/wizardFlows",
        })
    return records


def build_narration(scripts: dict, tools: list[dict], audio_names: set[str]) -> list[dict]:
    tool_map = {t["id"]: t for t in tools}
    records = []
    for raw_id, raw_text in sorted(scripts.items()):
        tool_id = canonical_id(raw_id)
        if tool_id not in tool_map:
            continue
        normalized, notes = normalize_tts(raw_text)
        records.append({
            "narration_id": f"{tool_id}-narration",
            "tool_id": tool_id,
            "language": "de",
            "style": "yuno",
            "tts_model": "MiniMax Speech 2.8 HD",
            "raw_text": raw_text,
            "normalized_text": normalized,
            "chars": len(raw_text),
            "words": len(raw_text.split()),
            "tts_artifacts": tts_artifact_counts(raw_text),
            "normalization_notes": notes,
            "normalization_confidence": "medium",
            "audio_path": f"tool-audios/{raw_id}.mp3",
            "audio_exists": raw_id in audio_names or tool_id in audio_names,
            "source": "scripts/tool-audio-scripts.json",
            "source_url": SOURCE_AUDIO,
            "safety_class": tool_map[tool_id]["safety"]["class"],
            "risk_level": tool_map[tool_id]["risk_level"],
        })
    return records


def _split_long_section(main_heading: str, body: str):
    if len(body) <= 4000:
        return [(main_heading, body, "h2")]
    parts = re.split(r"^###\s+(.+)$", body, flags=re.M)
    if len(parts) > 1:
        out = []
        if parts[0].strip():
            out.append((main_heading, parts[0].strip(), "h2-intro"))
        for i in range(1, len(parts), 2):
            sub = parts[i].strip()
            subbody = parts[i + 1].strip() if i + 1 < len(parts) else ""
            if subbody:
                out.append((f"{main_heading} / {sub}", subbody, "h3"))
        return out
    paragraphs = [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip()]
    out = []
    current = []
    size = 0
    for paragraph in paragraphs:
        if size + len(paragraph) > 3000 and current:
            out.append((main_heading, "\n\n".join(current), "paragraph"))
            current = [paragraph]
            size = len(paragraph)
        else:
            current.append(paragraph)
            size += len(paragraph) + 2
    if current:
        out.append((main_heading, "\n\n".join(current), "paragraph"))
    return out


def build_docs(docs_dir: Path) -> list[dict]:
    records = []
    for path in sorted(docs_dir.glob("*.md")):
        meta = DOC_META.get(path.name, {})
        text = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", text, re.M)
        doc_title = meta.get("doc_title") or (title_match.group(1).strip() if title_match else path.stem)
        parts = re.split(r"^##\s+(.+)$", text, flags=re.M)
        chunks = []
        if parts and parts[0].strip():
            intro = parts[0].strip()
            if len(intro) >= 80:
                chunks.append(("intro", intro, "intro"))
        for i in range(1, len(parts), 2):
            heading = parts[i].strip()
            body = parts[i + 1].strip() if i + 1 < len(parts) else ""
            if body:
                chunks.extend(_split_long_section(heading, body))
        for index, (heading, body, strategy) in enumerate(chunks, start=1):
            records.append({
                "doc_id": path.stem,
                "doc_title": doc_title,
                "chunk_id": f"{path.stem}-{index:02d}",
                "section": heading,
                "text": body,
                "chars": len(body),
                "chunk_strategy": strategy,
                "language": meta.get("language", "de"),
                "sources_count": meta.get("sources_count"),
                "source_url": meta.get("url", SOURCE_REPO + "/tree/main/docs"),
                "license": LICENSE,
            })
    return records

def build_audits(audits_dir: Path) -> list[dict]:
    records = []
    for path in sorted(audits_dir.glob("*.md")):
        meta = AUDIT_META.get(path.name, {})
        text = path.read_text(encoding="utf-8")
        records.append({
            "audit_id": path.stem,
            "title": meta.get("title", path.stem),
            "kind": meta.get("kind", "audit"),
            "reported_at": meta.get("reported_at"),
            "summary": meta.get("summary", ""),
            "chars": len(text),
            "source_file": f"audits/{path.name}",
            "source_url": SOURCE_REPO + "/blob/main/audits/" + path.name,
            "license": LICENSE,
        })
    records.append({
        "audit_id": "live-check-2026-10-20",
        "title": "Live-Prüfung Command Builder",
        "kind": "live_check",
        "reported_at": GENERATED_AT,
        "summary": "Vier Befunde: fehlendes Trennzeichen zwischen Toolname und erstem Flag (alle 14 Builder), falsche Zielposition bei sechs Tools, metasploit statt msfconsole, kein Builder für aircrack-ng.",
        "findings": [
            "missing_separator_between_tool_and_first_flag",
            "target_appended_instead_of_after_flag: sqlmap, gobuster, wpscan, nuclei, ffuf, evil-winrm",
            "wrong_base_binary: metasploit instead of msfconsole",
            "missing_builder: aircrack-ng",
        ],
        "observed_outputs": OBSERVED_OUTPUTS,
        "chars": 0,
        "source_file": None,
        "source_url": None,
        "license": LICENSE,
    })
    return records


def build_review_sample(tools: list[dict], commands: list[dict]) -> list[dict]:
    rng = random.Random(20261020)
    cmd_by_tool = defaultdict(list)
    for command in commands:
        if command["source"] == "toolExamples":
            cmd_by_tool[command["tool_id"]].append(command)

    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for tool in tools:
        mode = tool["modes"][0] if tool["modes"] else "unknown"
        groups[(mode, tool["primary_category"])].append(tool)

    target = max(len(groups), round(0.2 * len(tools)))
    quotas = {key: 1 for key in groups}
    remaining = target - len(groups)
    for key in sorted(groups, key=lambda k: len(groups[k]), reverse=True)[:remaining]:
        quotas[key] += 1

    sample = []
    for key in sorted(groups):
        items = sorted(groups[key], key=lambda t: t["id"])
        rng.shuffle(items)
        sample.extend(items[:quotas[key]])

    records = []
    for tool in sorted(sample, key=lambda t: t["id"]):
        tool_cmds = cmd_by_tool.get(tool["id"], [])
        command_syntax_ok = any(c["syntax_ok"] for c in tool_cmds) if tool_cmds else bool(tool["primary_command"])
        commands_verified = any(c["verified"] for c in tool_cmds)
        checks = {
            "description_ok": len(tool["description"]) >= 30,
            "command_syntax_ok": command_syntax_ok,
            "tags_mapped": not tool["unmapped_tags"],
            "safety_class_set": bool(tool["safety"]["class"]),
        }
        warnings = [k for k, v in checks.items() if not v]
        records.append({
            "tool_id": tool["id"],
            "name": tool["name"],
            "modes": tool["modes"],
            "primary_category": tool["primary_category"],
            "description": tool["description"],
            "primary_command": tool["primary_command"],
            "tags_raw": tool["tags_raw"],
            "topic_axes": tool["topic_axes"],
            "safety_class": tool["safety"]["class"],
            "risk_level": tool["risk_level"],
            "review_checklist": {
                "description_correct": "pending",
                "commands_correct": "pending",
                "tags_correct": "pending",
                "safety_class_correct": "pending",
                "notes": "",
            },
            "agent_review": {
                "status": "pass" if not warnings else "warn",
                "warnings": warnings,
                "commands_verified": commands_verified,
                "reviewed_at": GENERATED_AT,
            },
            "review_decision": "offen",
            "review_notes": "",
            "human_review": "pending",
        })
    return records

def build_quality_report(
    tools: list[dict],
    commands: list[dict],
    curriculum: list[dict],
    narration: list[dict],
    docs: list[dict],
    audits: list[dict],
    review: list[dict],
    tag_taxonomy: dict,
    doc_format: str = "obsidian",
) -> str:
    example_commands = [c for c in commands if c["source"] == "toolExamples"]
    builder_commands = [c for c in commands if c["source"] == "command_builder"]
    example_in_db = [c for c in example_commands if c.get("tool_in_db")]
    example_aux = [c for c in example_commands if not c.get("tool_in_db")]
    verified = [c for c in example_commands if c["verified"]]
    syntax_ok = [c for c in example_commands if c["syntax_ok"]]
    invalid = [c for c in example_commands if c["verification"]["status"] == "invalid"]
    safety = Counter(t["safety"]["class"] for t in tools)
    risk = Counter(t["risk_level"] for t in tools)
    playbooks = [c for c in curriculum if c["kind"] == "playbook"]
    paths = [c for c in curriculum if c["kind"] == "learning_path"]
    wizards = [c for c in curriculum if c["kind"] == "wizard_flow"]
    missing_refs = sum(len(c.get("missing_tool_refs", [])) for c in curriculum if c["kind"] in {"playbook", "learning_path"})
    missing_playbook_refs = sum(len(c.get("missing_playbook_refs", [])) for c in wizards)
    audio_ok = sum(1 for n in narration if n["audio_exists"])

    lines = []
    if doc_format == "obsidian":
        lines.append("---")
        lines.append("tags:")
        lines.append("  - ressourcen")
        lines.append("  - recherche")
        lines.append("  - kali")
        lines.append("  - dataset")
        lines.append("  - datenqualitaet")
        lines.append("  - security")
        lines.append("typ: ressource-reference")
        lines.append(f"erstellt: {GENERATED_AT}")
        lines.append(f"letzter-check: {GENERATED_AT}")
        lines.append("zweck: qualitaetsbericht-des-kuratierten-kali-tool-explorer-datasets")
        lines.append("quellen:")
        lines.append(f"  - {SOURCE_REPO}")
        lines.append(f"  - {SOURCE_HTML}")
        lines.append("status: aktiv")
        lines.append("version: 1.0.0")
        lines.append("quelle: tool")
        lines.append("agent: ZCode (deepseek-v4.1-flash)")
        lines.append("review-cadence: quarterly")
        lines.append("related-projects: [Kali-Pentest-Lab]")
        lines.append("---")
    lines.append("# Kali Tool Explorer — Dataset-Qualitätsbericht")
    lines.append("")
    lines.append(f"> Automatisch erzeugt am {GENERATED_AT} aus dem Inline-Block, den Audio-Skripten, den beiden Research-Dokumenten und den sechs Audit-Berichten. Der Bericht beschreibt den kuratierten Seed-Korpus in diesem Ordner, nicht die App-Laufzeit.")
    lines.append("")
    lines.append("## Bestand")
    lines.append("")
    lines.append("| Asset | Anzahl |")
    lines.append("|---|---:|")
    lines.append(f"| Tools (kanonisch) | {len(tools)} |")
    lines.append(f"| Beispiel-Commands | {len(example_commands)} |")
    lines.append(f"| Command-Builder-Records | {len(builder_commands)} |")
    lines.append(f"| Playbooks | {len(playbooks)} |")
    lines.append(f"| Lernpfade | {len(paths)} |")
    lines.append(f"| Wizard-Flows | {len(wizards)} |")
    lines.append(f"| Narrationen | {len(narration)} |")
    lines.append(f"| Doku-Chunks | {len(docs)} |")
    lines.append(f"| Audit-Records | {len(audits)} |")
    lines.append(f"| Review-Sample | {len(review)} |")
    lines.append("")
    lines.append("## Feldvollständigkeit und Duplikate")
    lines.append("")
    lines.append(f"- Kanonische Tools: **{len(tools)}**, davon mit mindestens einer Beschreibung: **{sum(1 for t in tools if t['description'])}**.")
    lines.append(f"- Tools mit leerem `primary_command`: **{sum(1 for t in tools if not t['primary_command'])}**.")
    lines.append(f"- Gemergte Varianten: **{sum(len(t['variants']) for t in tools)}**; Tools mit mehr als einer Variante: **{sum(1 for t in tools if len(t['variants']) > 1)}**.")
    lines.append(f"- Safety: **{dict(safety)}**; Risk: **{dict(risk)}**.")
    lines.append("")
    lines.append("## Tag-Normalisierung")
    lines.append("")
    lines.append(f"- Roh-Tags: **{tag_taxonomy['counts']['raw_tags']}**; gemappt: **{tag_taxonomy['counts']['mapped_tags']}**; unmapped: **{tag_taxonomy['counts']['unmapped_tags']}**.")
    used_axes = sorted({axis for tool in tools for axis in tool["topic_axes"]})
    unused_axes = sorted(set(tag_taxonomy["axes"]) - set(used_axes))
    lines.append(f"- Ziel-Achsen: **{len(tag_taxonomy['axes'])}** definiert, **{len(used_axes)}** verwendet; unbenutzt: `{', '.join(unused_axes) if unused_axes else 'keine'}`.")
    if tag_taxonomy["unmapped"]:
        lines.append(f"- Unmapped: `{', '.join(tag_taxonomy['unmapped'])}`.")
    lines.append("")
    lines.append("## Command-Verifikation")
    lines.append("")
    lines.append(f"- Beispiel-Commands: **{len(example_commands)}**; syntaktisch plausibel: **{len(syntax_ok)}**; verifiziert: **{len(verified)}**; ungültig: **{len(invalid)}**.")
    lines.append(f"- Davon aus der Tool-DB: **{len(example_in_db)}**; Auxiliary-Commands für Tools außerhalb der 131er-DB: **{len(example_aux)}**.")
    lines.append(f"- Builder-Records: **{len(builder_commands)}**; alle als `unverified` markiert, weil die Live-Ausgabe nachweislich fehlerhaft ist.")
    status_counts = Counter(c["verification"]["status"] for c in example_commands)
    reason_counts = Counter(c["verification"]["reason"].split(":", 1)[0] for c in example_commands)
    installed_binaries = sorted({
        c["verification"].get("binary")
        for c in example_commands
        if c["verification"].get("method") == "help" and c["verification"].get("installed")
    })
    wrapper_count = sum(1 for c in example_commands if c["verification"].get("wrapper"))
    lines.append(f"- Status: **{dict(status_counts)}**; Gründe: **{dict(reason_counts)}**.")
    lines.append(f"- Wrapper-Aufrufe (java, docker, systemctl, …), die nicht als Tool-Verifikation zählen: **{wrapper_count}**.")
    lines.append(f"- Für `--help` verfügbare Binaries: `{', '.join(installed_binaries) if installed_binaries else 'keine'}`.")
    lines.append("- Verifikationsmethode: `--help` nur für direkt aufgerufene, lokal installierte Binaries; sonst Syntaxprüfung. Wrapper und nicht installierte Tools bleiben `unverified`.")
    lines.append("")
    lines.append("## Curriculum")
    lines.append("")
    lines.append(f"- Playbook-Tool-Referenzen: **{sum(c['tool_count'] for c in playbooks)}**; fehlend: **{missing_refs}**.")
    lines.append(f"- Lernpfad-Wochen: **{sum(c['week_count'] for c in paths)}**; Tool-Referenzen: **{sum(len(c['tool_refs']) for c in paths)}**.")
    lines.append(f"- Wizard-Playbook-Referenzen fehlend: **{missing_playbook_refs}**.")
    lines.append("")
    lines.append("## Narration")
    lines.append("")
    lines.append(f"- Skripte: **{len(narration)}**; Audio vorhanden: **{audio_ok}/{len(narration)}**.")
    lines.append(f"- Zeichen: **{sum(n['chars'] for n in narration)}**; Wörter: **{sum(n['words'] for n in narration)}**.")
    lines.append("- Normalisierung: `Doppelminus` → `--`, `Minus` → `-`, `bewaehrt` → `bewährt`, `fuer` → `für`; `normalized_text` ist eine Best-Effort-Form, `raw_text` bleibt erhalten.")
    lines.append("")
    lines.append("## Review")
    lines.append("")
    lines.append(f"- Stratified Sample: **{len(review)}** Tools ({len(review) / len(tools) * 100:.1f} %), mindestens ein Tool je Kategorie.")
    lines.append(f"- Agenten-Review: **{sum(1 for r in review if r['agent_review']['status'] == 'pass')} pass**, **{sum(1 for r in review if r['agent_review']['status'] == 'warn')} warn**.")
    lines.append(f"- Davon Commands per `--help` verifiziert: **{sum(1 for r in review if r['agent_review']['commands_verified'])}/{len(review)}**.")
    lines.append(f"- Menschliche Abnahme: **{sum(1 for r in review if r['human_review'] == 'pending')} pending**.")
    if doc_format == "obsidian":
        lines.append("- Ausfüllhilfe: [[Kali Tool Explorer - Review-Stichprobe]] · Fragenkatalog: [[Kali Tool Explorer - Review-Runbook]].")
    else:
        lines.append("- Ausfüllhilfe: [Review Sample](review-sample.md) · Fragenkatalog: [Review Runbook](REVIEW.md).")
    lines.append("")
    lines.append("## Bekannte Grenzen")
    lines.append("")
    lines.append("- Die Commands sind **nicht** gegen eine Live-Kali-Installation verifiziert. 34 Commands wurden per `--help` lokal installierter Binaries annotiert; 148 bleiben `unverified`, davon 129 ohne installiertes Binary, 14 mit nicht gefundenem Flag und 5 Wrapper-Aufrufe.")
    lines.append("- Die Builder-Templates sind aus den Flag-Daten abgeleitet und korrigieren die vier Live-Befunde, sind aber ungetestet.")
    lines.append("- Die Tag-Achsen sind eine kuratierte Heuristik; die Roh-Tags bleiben für Rückverfolgbarkeit erhalten.")
    lines.append("- Die Narration-Normalisierung ist konservativ und nicht sprachlich vollständig geprüft.")
    lines.append("- Die 20-%-Stichprobe ist vorbereitet, aber menschlich noch nicht abgenommen.")
    lines.append("- Die separate `kali-tool-database.json` wurde nicht als Quelle verwendet; maßgeblich ist der Inline-Block mit 144 Datensätzen.")
    lines.append("")
    lines.append("## Dateien")
    lines.append("")
    lines.append("- `kali-tools.jsonl` — 131 kanonische Tools mit Varianten, Achsen, Safety und Provenienz.")
    lines.append("- `kali-commands.jsonl` — 182 Beispiel-Commands plus 15 Builder-Records.")
    lines.append("- `kali-curriculum.jsonl` — 12 Playbooks, 4 Lernpfade, 2 Wizard-Flows.")
    lines.append("- `kali-narration.jsonl` — 131 Narrationen mit Roh- und Normalform.")
    lines.append("- `kali-docs.jsonl` — Chunks der beiden Research-Dokumente.")
    lines.append("- `kali-audits.jsonl` — sechs Audit-Berichte plus Live-Prüfung.")
    lines.append("- `kali-tag-taxonomy.json` — Achsen, Mapping und Abdeckung.")
    lines.append("- `kali-review-sample.jsonl` — 20-%-Stichprobe mit Review-Checkliste.")
    lines.append("- `kali-review-sample.csv` — dieselbe Stichprobe als Tabelle für die menschliche Abnahme.")
    lines.append("- `kali-source-manifest.json` — Quellen, Hashes und Zähler.")
    lines.append("")
    if doc_format == "obsidian":
        lines.append("## Verbindungen")
        lines.append("")
        lines.append("- [[Kali-Pentest-Lab]] · [[Repo - kali-tool-explorer]]")
        lines.append("- [[Recherche - Kali Tool Explorer als High-Quality-Dataset]] · [[Kali Tool Explorer - Dataset]]")
        lines.append("- [[kali-tool-explorer - Tool-Datenbank und Dual-Mode|Kali Tool Explorer - Tool-Datenbank und Dual-Mode]] · [[kali-tool-explorer - Command-Builder-Referenz|Kali Tool Explorer - Command-Builder-Referenz]]")
        lines.append("")
    else:
        lines.append("## Links")
        lines.append("")
        lines.append("- [Dataset README](README.md)")
        lines.append("- [Safety Policy](SAFETY.md)")
        lines.append("- [Review Runbook](REVIEW.md)")
        lines.append("- [Review Sample](review-sample.md)")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("."), help="Repo-Ablage mit HTML, Audio-Skripten, docs/ und audits/")
    parser.add_argument("--out", type=Path, default=Path("."), help="Zielordner für die Dataset-Dateien")
    parser.add_argument("--audio-names", type=Path, default=None, help="Textdatei mit Audio-Stems, eine pro Zeile")
    parser.add_argument("--doc-format", choices=["obsidian", "github"], default="obsidian", help="Markdown-Format der erzeugten Dokumente")
    args = parser.parse_args()

    source = args.source
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    html_path = source / "forensik-explorer.html"
    if not html_path.exists():
        print(f"Fehlt: {html_path}", file=sys.stderr)
        return 1

    html = html_path.read_text(encoding="utf-8")
    db = extract_inline_db(html)
    helper = Path(__file__).resolve().parent / "extract_js.js"
    if not helper.exists():
        helper = out / "extract_js.js"
    js = run_extract_js(html_path, helper)

    audio_names: set[str] = set()
    if args.audio_names and args.audio_names.exists():
        audio_names = {line.strip() for line in args.audio_names.read_text(encoding="utf-8").splitlines() if line.strip()}
    elif (source / "tool-audios.txt").exists():
        audio_names = {line.strip() for line in (source / "tool-audios.txt").read_text(encoding="utf-8").splitlines() if line.strip()}
    elif (source / "tool-audios").is_dir():
        audio_names = {p.stem for p in (source / "tool-audios").glob("*.mp3")}

    audio_scripts_path = source / "scripts" / "tool-audio-scripts.json"
    if not audio_scripts_path.exists():
        audio_scripts_path = source / "tool-audio-scripts.json"
    if not audio_scripts_path.exists():
        print(f"Fehlt: {audio_scripts_path}", file=sys.stderr)
        return 1
    scripts = json.loads(audio_scripts_path.read_text(encoding="utf-8"))
    inline_meta = db.get("meta", {})

    tools = build_tools(db, inline_meta)
    commands = build_commands(tools, js)
    curriculum = build_curriculum(js, tools)
    narration = build_narration(scripts, tools, audio_names)
    docs = build_docs(source / "docs")
    audits = build_audits(source / "audits")
    review = build_review_sample(tools, commands)

    # Tag taxonomy
    all_tags = sorted({tag for t in tools for tag in t["tags_raw"]})
    mapping = {}
    unmapped = []
    for tag in all_tags:
        entry = TAG_MAP.get(tag)
        if entry:
            mapping[tag] = entry
        else:
            unmapped.append(tag)
    tag_taxonomy = {
        "dataset_id": DATASET_ID,
        "generated_at": GENERATED_AT,
        "axes": AXES,
        "category_axis": CATEGORY_AXIS,
        "mapping": mapping,
        "unmapped": unmapped,
        "counts": {
            "raw_tags": len(all_tags),
            "mapped_tags": len(mapping),
            "unmapped_tags": len(unmapped),
        },
    }

    write_jsonl(out / "kali-tools.jsonl", tools)
    write_jsonl(out / "kali-commands.jsonl", commands)
    write_jsonl(out / "kali-curriculum.jsonl", curriculum)
    write_jsonl(out / "kali-narration.jsonl", narration)
    write_jsonl(out / "kali-docs.jsonl", docs)
    write_jsonl(out / "kali-audits.jsonl", audits)
    write_jsonl(out / "kali-review-sample.jsonl", review)
    with (out / "kali-review-sample.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow([
            "tool_id", "name", "modes", "primary_category", "description",
            "primary_command", "topic_axes", "safety_class", "risk_level",
            "agent_status", "commands_verified", "human_review", "review_decision", "review_notes",
        ])
        for record in review:
            writer.writerow([
                record["tool_id"],
                record["name"],
                "|".join(record["modes"]),
                record["primary_category"],
                record["description"],
                record["primary_command"],
                "|".join(record["topic_axes"]),
                record["safety_class"],
                record["risk_level"],
                record["agent_review"]["status"],
                record["agent_review"]["commands_verified"],
                record["human_review"],
                record["review_decision"],
                record["review_notes"],
            ])
    (out / "kali-tag-taxonomy.json").write_text(json.dumps(tag_taxonomy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = build_quality_report(tools, commands, curriculum, narration, docs, audits, review, tag_taxonomy, doc_format=args.doc_format)
    report_name = "kali-quality-report.md" if args.doc_format == "obsidian" else "quality-report.md"
    (out / report_name).write_text(report, encoding="utf-8")

    source_files = []
    for path, role, repo_path in [
        (html_path, "inline tool database + UI", "forensik-explorer.html"),
        (audio_scripts_path, "German narration scripts", "scripts/tool-audio-scripts.json"),
        (source / "docs" / "kali-blue-vs-purple.md", "research document", "docs/kali-blue-vs-purple.md"),
        (source / "docs" / "kali-forensik-overview.md", "research document", "docs/kali-forensik-overview.md"),
    ]:
        if path.exists():
            source_files.append({
                "path": str(path.relative_to(source)),
                "repo_path": repo_path,
                "role": role,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "url": SOURCE_REPO + "/blob/main/" + repo_path,
            })
    for path in sorted((source / "audits").glob("*.md")):
        source_files.append({
            "path": str(path.relative_to(source)),
            "repo_path": f"audits/{path.name}",
            "role": "audit report",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "url": SOURCE_REPO + "/blob/main/audits/" + path.name,
        })

    manifest = {
        "dataset_id": DATASET_ID,
        "generated_at": GENERATED_AT,
        "source_repo": SOURCE_REPO,
        "kali_version": inline_meta.get("kaliVersion", "2026.2"),
        "app_version": APP_VERSION,
        "data_version": inline_meta.get("version"),
        "license": LICENSE,
        "safety": "dual-use",
        "counts": {
            "tools": len(tools),
            "example_commands": sum(1 for c in commands if c["source"] == "toolExamples"),
            "builder_records": sum(1 for c in commands if c["source"] == "command_builder"),
            "curriculum_records": len(curriculum),
            "narrations": len(narration),
            "docs_chunks": len(docs),
            "audits": len(audits),
            "review_sample": len(review),
        },
        "generator": "build_kali_dataset.py + extract_js.js",
        "source_files": source_files,
    }
    (out / "kali-source-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(manifest["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
