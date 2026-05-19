#!/usr/bin/env python3
"""Build a non-live publication draft for Lerch's Bacmeister sentence samples.

The Bacmeister samples are not a narrative text. This script keeps them as a
reviewable appendix draft, preserving the source table content and carrying
forward the small glyph-review queue as publication flags.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "drafts" / "lerch" / "bacmeister-sentence-samples"
REPORT_DIR = REPO_ROOT / "reports"

SOURCE_DRAFT = Path(
    r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\translation_project\lerch\appendix_bacmeister_sentence_samples\bacmeister_sentence_samples_transcription_translation_draft.md"
)
REVIEW_DATA = Path(
    r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_bacmeister_samples_review_bundle\lerch_bacmeister_samples_review_data.json"
)


@dataclass
class SampleRow:
    no: str
    kurmanji_lerch: str
    zaza_lerch: str
    german: str
    english: str
    turkish: str
    notes: str


def strip_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1]
    return value


def split_markdown_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def parse_source_rows(path: Path) -> list[SampleRow]:
    rows: list[SampleRow] = []
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| No. | Kurmanji in Lerch |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = split_markdown_row(line)
        if len(cells) < 7:
            continue
        rows.append(
            SampleRow(
                no=cells[0],
                kurmanji_lerch=strip_code(cells[1]),
                zaza_lerch=strip_code(cells[2]),
                german=cells[3],
                english=cells[4],
                turkish=cells[5],
                notes=cells[6],
            )
        )
    return rows


def load_review_flags(path: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    flags: dict[str, dict[str, Any]] = {}
    for item in data.get("items") or []:
        row_no = str(item.get("row_no") or "")
        if not row_no:
            continue
        flags[row_no] = item
    return flags


def write_tsv(path: Path, rows: list[SampleRow], flags: dict[str, dict[str, Any]]) -> None:
    fields = [
        "row_no",
        "review_status",
        "review_focus",
        "review_question",
        "zaza_lerch",
        "kurmanji_lerch",
        "german",
        "english",
        "turkish",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        for row in rows:
            flag = flags.get(row.no) or {}
            writer.writerow(
                {
                    "row_no": row.no,
                    "review_status": "needs_glyph_review" if flag else "not_flagged",
                    "review_focus": flag.get("focus") or "",
                    "review_question": flag.get("question") or "",
                    "zaza_lerch": row.zaza_lerch,
                    "kurmanji_lerch": row.kurmanji_lerch,
                    "german": row.german,
                    "english": row.english,
                    "turkish": row.turkish,
                    "notes": row.notes,
                }
            )


def markdown_table_row(cells: list[str]) -> str:
    return "| " + " | ".join(cell.replace("|", "\\|") for cell in cells) + " |"


def write_markdown(path: Path, rows: list[SampleRow], flags: dict[str, dict[str, Any]]) -> None:
    lines: list[str] = []
    lines.append("# Lerch Bacmeister Sentence Samples")
    lines.append("")
    lines.append(f"Draft generated: {date.today().isoformat()}")
    lines.append("")
    lines.append("This is a non-live publication draft for Lerch's Zaza renderings of Bacmeister's sentence samples. It is an appendix-style table, not a narrative text. The Zaza column preserves Lerch's historical phonetic transcription rather than normalizing it to modern Zazaki orthography.")
    lines.append("")
    lines.append("Source heading: Uebersetzung der \"Sprachproben\" Bacmeisters in die kurdischen Mundarten Kurmandi und Zaza.")
    lines.append("")
    lines.append("Primary source note: Russian Book II viewer pages 55-58 / printed pp. 41-44 are treated as the primary witness; the German reprint pages 45-48 and high-resolution local crops are secondary controls for glyph review.")
    lines.append("")
    lines.append(f"Review status: {len(flags)} of {len(rows)} rows are flagged for remaining glyph/form review. These rows should not be treated as final until manually accepted.")
    lines.append("")
    lines.append(markdown_table_row(["No.", "Review", "Zaza in Lerch", "Kurmanji in Lerch", "English", "Turkish", "German", "Notes"]))
    lines.append(markdown_table_row(["---:", "---", "---", "---", "---", "---", "---", "---"]))
    for row in rows:
        flag = flags.get(row.no) or {}
        review = "needs glyph review" if flag else ""
        if flag.get("focus"):
            review = f"{review}: {flag['focus']}" if review else str(flag["focus"])
        lines.append(
            markdown_table_row(
                [
                    row.no,
                    review,
                    f"`{row.zaza_lerch}`",
                    f"`{row.kurmanji_lerch}`",
                    row.english,
                    row.turkish,
                    row.german,
                    row.notes,
                ]
            )
        )
    lines.append("")
    lines.append("## Flagged Review Rows")
    lines.append("")
    if not flags:
        lines.append("No rows are currently flagged.")
    else:
        for row_no in sorted(flags, key=lambda item: int(item) if item.isdigit() else item):
            flag = flags[row_no]
            lines.append(f"- Row {row_no}: {flag.get('question') or flag.get('focus') or 'needs review'}")
    lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_readme(path: Path, rows: list[SampleRow], flags: dict[str, dict[str, Any]]) -> None:
    lines = [
        "# Bacmeister Sentence Samples Draft",
        "",
        "This folder is a non-live publication draft generated from the local Lerch Bacmeister sentence-sample working files.",
        "",
        "Files:",
        "",
        "- `publication-draft.md`: human-readable appendix draft.",
        "- `samples.tsv`: machine-readable table with the same rows and review flags.",
        "",
        f"Rows: {len(rows)}",
        f"Rows flagged for glyph/form review: {len(flags)}",
        "",
        "Do not import this as a normal Lerch narrative text. It should become an appendix/examples page after the flagged glyph rows are accepted.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_report(path: Path, rows: list[SampleRow], flags: dict[str, dict[str, Any]]) -> None:
    lines = [
        "# Lerch Bacmeister Publication Draft",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "A non-live source-controlled draft has been created from the local 44-row Bacmeister sentence-sample table.",
        "",
        "## Output",
        "",
        "- `drafts/lerch/bacmeister-sentence-samples/publication-draft.md`",
        "- `drafts/lerch/bacmeister-sentence-samples/samples.tsv`",
        "- `drafts/lerch/bacmeister-sentence-samples/README.md`",
        "",
        "## Counts",
        "",
        f"- Rows: {len(rows)}",
        f"- Rows flagged for glyph/form review: {len(flags)}",
        "",
        "## Remaining Review Rows",
        "",
    ]
    for row_no in sorted(flags, key=lambda item: int(item) if item.isdigit() else item):
        flag = flags[row_no]
        lines.append(f"- Row {row_no}: {flag.get('focus') or ''} -- {flag.get('question') or ''}".rstrip())
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not SOURCE_DRAFT.exists():
        raise SystemExit(f"Source draft not found: {SOURCE_DRAFT}")
    if not REVIEW_DATA.exists():
        raise SystemExit(f"Review data not found: {REVIEW_DATA}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = parse_source_rows(SOURCE_DRAFT)
    flags = load_review_flags(REVIEW_DATA)
    write_tsv(OUT_DIR / "samples.tsv", rows, flags)
    write_markdown(OUT_DIR / "publication-draft.md", rows, flags)
    write_readme(OUT_DIR / "README.md", rows, flags)
    write_report(REPORT_DIR / "lerch-bacmeister-publication-draft.md", rows, flags)
    print(f"Wrote Bacmeister draft with {len(rows)} rows and {len(flags)} flagged review rows.")


if __name__ == "__main__":
    main()
