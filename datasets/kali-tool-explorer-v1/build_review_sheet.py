#!/usr/bin/env python3
"""
Generate a human review sheet from kali-review-sample.jsonl.

Run once before the review. If the generated Markdown has been annotated,
do not re-run this script unless you want to overwrite the annotations.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
SAMPLE = BASE / "kali-review-sample.jsonl"


def load_sample() -> list[dict]:
    return [json.loads(line) for line in SAMPLE.read_text(encoding="utf-8").splitlines() if line.strip()]


def yes_no(value: bool) -> str:
    return "ja" if value else "nein"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc-format", choices=["obsidian", "github"], default="obsidian")
    args = parser.parse_args()

    sample = load_sample()
    lines: list[str] = []
    if args.doc_format == "obsidian":
        lines.append("---")
        lines.append("tags:")
        for tag in ["ressourcen", "kali", "dataset", "review", "security"]:
            lines.append(f"  - {tag}")
        lines.append("typ: ressource-reference")
        lines.append("erstellt: 2026-10-20")
        lines.append("letzter-check: 2026-10-20")
        lines.append("zweck: menschliche-abnahme-der-26er-dataset-stichprobe")
        lines.append("quellen:")
        lines.append("  - ./kali-review-sample.jsonl")
        lines.append("status: aktiv")
        lines.append("version: 1.0.0")
        lines.append("quelle: tool")
        lines.append("agent: ZCode (deepseek-v4.1-flash)")
        lines.append("review-cadence: never")
        lines.append("related-projects: [Kali-Pentest-Lab]")
        lines.append("---")
    lines.append("# Kali Tool Explorer — Review-Stichprobe")
    runbook_sentence = (
        "Der Fragenkatalog mit Entscheidungsregeln steht im [[Kali Tool Explorer - Review-Runbook]]. "
        if args.doc_format == "obsidian"
        else "Der Fragenkatalog mit Entscheidungsregeln steht im [Review Runbook](REVIEW.md). "
    )
    lines.append(
        f"> {len(sample)} von 131 Tools ({len(sample) / 131 * 100:.1f} %), stratifiziert über Modi und Kategorien. "
        "Bitte pro Tool die vier Checks und eine Entscheidung eintragen. "
        + runbook_sentence
        + "Die maschinenlesbare Quelle ist `kali-review-sample.jsonl`; die Tabelle `kali-review-sample.csv` enthält dieselben Felder."
    )
    lines.append("")
    lines.append("## Wie ausfüllen")
    lines.append("")
    lines.append("- **Beschreibung:** korrekt, verständlich, nicht irreführend?")
    lines.append("- **Command:** syntaktisch und fachlich richtig? `unverified` ist der Ausgangszustand, kein Fehler.")
    lines.append("- **Tags/Achsen:** passen die normalisierten Achsen und die Roh-Tags?")
    lines.append("- **Safety:** sind `dual-use`/`defensiv` und das Risk-Level angemessen?")
    lines.append("- **Entscheidung:** `accept`, `fix` oder `reject`; bei `fix`/`reject` bitte eine kurze Notiz.")
    lines.append("- **Agent:** vorausgefüllter Konsistenz-Check; **Cmd verifiziert** zeigt, ob mindestens ein Command per `--help` geprüft wurde.")
    lines.append("")
    lines.append("## Übersicht")
    lines.append("")
    lines.append("| # | Tool | Modus | Kategorie | Risk | Safety | Agent | Cmd verifiziert | Entscheidung |")
    lines.append("|---:|---|---|---|---|---|---|---|---|")
    for index, tool in enumerate(sample, start=1):
        lines.append(
            f"| {index} | `{tool['tool_id']}` | {'/'.join(tool['modes'])} | {tool['primary_category']} | "
            f"{tool['risk_level']} | {tool['safety_class']} | {tool['agent_review']['status']} | "
            f"{yes_no(tool['agent_review']['commands_verified'])} | offen |"
        )
    lines.append("")
    lines.append("## Die 26 Tools")
    lines.append("")
    for index, tool in enumerate(sample, start=1):
        lines.append(f"### {index}. {tool['name']} (`{tool['tool_id']}`)")
        lines.append("")
        lines.append(
            f"**Modus:** {'/'.join(tool['modes'])} · **Kategorie:** {tool['primary_category']} · "
            f"**Risk:** {tool['risk_level']} · **Safety:** {tool['safety_class']} · "
            f"**Agent:** {tool['agent_review']['status']} · **Cmd verifiziert:** {yes_no(tool['agent_review']['commands_verified'])}"
        )
        lines.append("")
        lines.append(f"**Beschreibung:** {tool['description']}")
        lines.append("")
        command = tool['primary_command'] or "—"
        lines.append(f"**Primärer Command:** `{command}`")
        lines.append("")
        lines.append(f"**Roh-Tags:** {', '.join(tool['tags_raw']) if tool['tags_raw'] else '—'}")
        lines.append("")
        lines.append(f"**Achsen:** {', '.join(tool['topic_axes']) if tool['topic_axes'] else '—'}")
        lines.append("")
        lines.append("- [ ] Beschreibung korrekt")
        lines.append("- [ ] Command korrekt (syntax_ok; ggf. `unverified` akzeptieren)")
        lines.append("- [ ] Tags/Achsen passend")
        lines.append("- [ ] Safety-Klassifikation passend")
        lines.append("- **Entscheidung:** `offen` → `accept` / `fix` / `reject`")
        lines.append("- **Notizen:**")
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.append("## Nach der Abnahme")
    lines.append("")
    quality_link = (
        "[[kali-quality-report|Dataset-Qualitätsbericht]]"
        if args.doc_format == "obsidian"
        else "[Dataset-Qualitätsbericht](quality-report.md)"
    )
    lines.append(
        "Sag Bescheid, wenn die Stichprobe durch ist. Dann übernehme ich die Entscheidungen in "
        f"`kali-review-sample.jsonl` und `kali-review-sample.csv` und ziehe den {quality_link} nach."
    )
    lines.append("")
    if args.doc_format == "obsidian":
        lines.append("## Verbindungen")
        lines.append("")
        lines.append("- [[Kali Tool Explorer - Dataset]] · [[Kali Tool Explorer - Safety-Policy]]")
        lines.append("- [[kali-quality-report|Dataset-Qualitätsbericht]] · [[Kali-Pentest-Lab]]")
        lines.append("- [[Recherche - Kali Tool Explorer als High-Quality-Dataset]]")
        lines.append("")
        out_path = BASE / "Kali Tool Explorer - Review-Stichprobe.md"
    else:
        lines.append("## Links")
        lines.append("")
        lines.append("- [Dataset README](README.md)")
        lines.append("- [Safety Policy](SAFETY.md)")
        lines.append("- [Quality Report](quality-report.md)")
        lines.append("")
        out_path = BASE / "review-sample.md"

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"geschrieben: {out_path} ({len(sample)} Tools)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
