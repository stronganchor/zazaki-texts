#!/usr/bin/env python3
"""Build a review table for converting Lerch glossary headwords to Zazaki.

This is intentionally a report, not a glossary importer.  The source glossary
still contains OCR-level rows, so the generated modern orthography should be
reviewed before publication.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LERCH_DIR = Path(r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch")
GLOSSARY_TSV = LERCH_DIR / "lltools_import" / "lltools_dictionary_lerch_glossary_full.tsv"
CONVERTER_MODULE_DIR = LERCH_DIR
OUT_TSV = REPO_ROOT / "reports" / "lerch-glossary-modern-conversion.tsv"
OUT_MD = REPO_ROOT / "reports" / "lerch-glossary-modern-conversion.md"


if str(CONVERTER_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(CONVERTER_MODULE_DIR))

from build_lerch_feud_interlinear_bundle import lerch_to_zazaki  # noqa: E402


LOW_CONFIDENCE_ENTRY_RE = re.compile(r"[?;§ÂÃÐÑ�]|\b(?:Ortsname|Personenname)\b")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def confidence_for(row: dict[str, str], modern: str) -> tuple[str, str]:
    entry = row.get("entry", "")
    status = row.get("entry_review_status", "")
    notes: list[str] = []

    if not modern:
        return "none", "empty conversion"

    if status == "qa_reviewed":
        confidence = "high"
    elif status == "headword_parented":
        confidence = "medium"
    else:
        confidence = "low"
        notes.append("source row is still OCR-level")

    if LOW_CONFIDENCE_ENTRY_RE.search(entry):
        confidence = "low"
        notes.append("entry contains OCR/noise markers")

    if any(char.isdigit() for char in entry):
        confidence = "low"
        notes.append("entry contains digits")

    if len(entry.split()) > 2:
        confidence = "low"
        notes.append("multiword or collapsed row")

    return confidence, "; ".join(notes)


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_tsv(GLOSSARY_TSV):
        entry = row.get("entry", "").strip()
        modern = lerch_to_zazaki(entry).strip() if entry else ""
        confidence, notes = confidence_for(row, modern)
        rows.append(
            {
                "row_id": row.get("source_row_idx", ""),
                "entry_id": row.get("entry_id", ""),
                "source_page": row.get("source_page", ""),
                "entry_lerch": entry,
                "entry_modern_zazaki_guess": modern,
                "parent_headword": row.get("parent", ""),
                "definition_de": row.get("definition_de", ""),
                "definition_en": row.get("definition_en", ""),
                "definition_tr": row.get("definition_tr", ""),
                "entry_review_status": row.get("entry_review_status", ""),
                "conversion_confidence": confidence,
                "conversion_notes": notes,
            }
        )
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "row_id",
        "entry_id",
        "source_page",
        "entry_lerch",
        "entry_modern_zazaki_guess",
        "parent_headword",
        "definition_de",
        "definition_en",
        "definition_tr",
        "entry_review_status",
        "conversion_confidence",
        "conversion_notes",
    ]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    status_counts = Counter(row["entry_review_status"] or "(blank)" for row in rows)
    confidence_counts = Counter(row["conversion_confidence"] for row in rows)
    translated_en = sum(1 for row in rows if row["definition_en"])
    translated_tr = sum(1 for row in rows if row["definition_tr"])
    translated_de = sum(1 for row in rows if row["definition_de"])
    parented = sum(1 for row in rows if row["parent_headword"])

    lines = [
        "# Lerch Glossary Modern Orthography Conversion",
        "",
        "This report applies the current Lerch-to-Zazaki converter to the working local Lerch glossary headwords.",
        "It is a review aid, not a publish-ready dictionary export, because most glossary rows remain OCR-level.",
        "",
        "## Inputs",
        "",
        f"- Source glossary: `{GLOSSARY_TSV}`",
        "- Converter: `Dictionaries/Lerch/build_lerch_feud_interlinear_bundle.py::lerch_to_zazaki`",
        f"- TSV output: `{OUT_TSV.relative_to(REPO_ROOT)}`",
        "",
        "## Counts",
        "",
        f"- Total rows: {len(rows)}",
        f"- Rows parented to a modern dictionary headword: {parented}",
        f"- Rows with German gloss: {translated_de}",
        f"- Rows with English gloss: {translated_en}",
        f"- Rows with Turkish gloss: {translated_tr}",
        "",
        "## Entry Review Status",
        "",
    ]
    for key, count in sorted(status_counts.items()):
        lines.append(f"- {key}: {count}")
    lines.extend(["", "## Conversion Confidence", ""])
    for key, count in sorted(confidence_counts.items()):
        lines.append(f"- {key}: {count}")
    lines.extend(
        [
            "",
            "## Publication Readiness",
            "",
            "- The conversion logic exists and now has a full review table.",
            "- The conversion output should not be published as final until OCR-level rows are reviewed against the scans.",
            "- Rows marked `qa_reviewed` are the safest starting subset for a public pilot glossary.",
            "- Rows marked `headword_parented` are useful internally but still need headword/diacritic verification.",
            "- Rows marked `ocr_extracted` should be treated as unreviewed.",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_outputs(rows)
    print(f"Wrote {OUT_TSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
