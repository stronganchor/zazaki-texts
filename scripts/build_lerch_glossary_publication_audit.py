#!/usr/bin/env python3
"""Build a publication-readiness audit for the local Lerch glossary table."""

from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "reports"
DEFAULT_GLOSSARY = Path(
    r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lltools_import\lltools_dictionary_lerch_glossary_full.tsv"
)
OUT_TSV = REPORT_DIR / "lerch-glossary-publication-audit.tsv"
OUT_MD = REPORT_DIR / "lerch-glossary-publication-audit.md"

SUSPICIOUS_HEADWORD_RE = re.compile(r"[0-9$§=@#{}\[\]\\<>]")
LABEL_HINTS = (
    "personenname",
    "personennamen",
    "eigenname",
    "ortsname",
    "monatsname",
    "frauenname",
    "mannsname",
    "name eines",
    "name einer",
    "name des",
    "name der",
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def compact(value: str, limit: int = 140) -> str:
    value = " ".join((value or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def issue_labels(row: dict[str, str]) -> list[str]:
    labels: list[str] = []
    review_status = row.get("entry_review_status") or ""
    en_status = row.get("definition_en_review_status") or ""
    german = " ".join(
        [
            row.get("definition_de") or "",
            row.get("raw_headword") or "",
            row.get("entry_display") or "",
        ]
    ).lower()
    headword_blob = " ".join(
        [
            row.get("entry") or "",
            row.get("entry_display") or "",
            row.get("entry_search") or "",
            row.get("raw_headword") or "",
        ]
    )

    if review_status != "qa_reviewed":
        labels.append("not_qa_reviewed")
    if review_status == "ocr_extracted":
        labels.append("raw_ocr_extraction")
    if not (row.get("definition_en") or "").strip():
        labels.append("missing_english")
    if not (row.get("definition_tr") or "").strip():
        labels.append("missing_turkish")
    if en_status == "" and (row.get("definition_en") or "").strip():
        labels.append("english_unreviewed")
    if any(hint in german for hint in LABEL_HINTS):
        labels.append("likely_name_or_label")
    if SUSPICIOUS_HEADWORD_RE.search(headword_blob):
        labels.append("suspicious_headword_shape")
    if (row.get("parent") or row.get("parent_search")) and (
        "not_qa_reviewed" in labels or "missing_english" in labels or "missing_turkish" in labels
    ):
        labels.append("parented_but_needs_review")
    return labels


def priority(labels: list[str]) -> int:
    if "suspicious_headword_shape" in labels:
        return 1
    if "likely_name_or_label" in labels:
        return 2
    if "raw_ocr_extraction" in labels and ("missing_english" in labels or "missing_turkish" in labels):
        return 3
    if "parented_but_needs_review" in labels:
        return 4
    if "missing_english" in labels or "missing_turkish" in labels:
        return 5
    if "not_qa_reviewed" in labels:
        return 6
    return 9


def audit_row(row: dict[str, str]) -> dict[str, str]:
    labels = issue_labels(row)
    return {
        "priority": str(priority(labels)),
        "issues": "; ".join(labels),
        "entry_id": row.get("entry_id") or "",
        "entry_display": row.get("entry_display") or row.get("entry") or "",
        "entry_search": row.get("entry_search") or "",
        "parent": row.get("parent") or "",
        "parent_search": row.get("parent_search") or "",
        "entry_type": row.get("entry_type") or "",
        "entry_review_status": row.get("entry_review_status") or "",
        "definition_en_review_status": row.get("definition_en_review_status") or "",
        "definition_tr_source": row.get("definition_tr_source") or "",
        "definition_de": compact(row.get("definition_de") or "", 240),
        "definition_en": compact(row.get("definition_en") or "", 160),
        "definition_tr": compact(row.get("definition_tr") or "", 160),
        "raw_headword": compact(row.get("raw_headword") or "", 160),
        "source_page": row.get("source_page") or "",
        "source_row_idx": row.get("source_row_idx") or "",
        "suggested_next_step": suggested_next_step(labels),
    }


def suggested_next_step(labels: list[str]) -> str:
    if "suspicious_headword_shape" in labels:
        return "Check source scan/OCR before publishing."
    if "likely_name_or_label" in labels:
        return "Decide whether this belongs in the public glossary or in a names/places/context index."
    if "raw_ocr_extraction" in labels:
        return "Verify headword and German gloss against the source, then add reviewed English/Turkish glosses."
    if "parented_but_needs_review" in labels:
        return "Confirm parent/variant relation and inherit or add reviewed public definitions."
    if "missing_english" in labels or "missing_turkish" in labels:
        return "Add reviewed English and Turkish glosses before public import."
    if "not_qa_reviewed" in labels:
        return "Promote only after a human QA pass."
    return "Looks ready from this audit, pending broader editorial checks."


def write_tsv(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "priority",
        "issues",
        "entry_id",
        "entry_display",
        "entry_search",
        "parent",
        "parent_search",
        "entry_type",
        "entry_review_status",
        "definition_en_review_status",
        "definition_tr_source",
        "definition_de",
        "definition_en",
        "definition_tr",
        "raw_headword",
        "source_page",
        "source_row_idx",
        "suggested_next_step",
    ]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, str]], limit: int = 30) -> str:
    lines = [
        "| Priority | Issues | Entry | German gloss | EN | TR | Next step |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows[:limit]:
        lines.append(
            "| {priority} | {issues} | {entry} | {de} | {en} | {tr} | {next_step} |".format(
                priority=row["priority"],
                issues=compact(row["issues"], 80).replace("|", "\\|"),
                entry=compact(row["entry_display"], 60).replace("|", "\\|"),
                de=compact(row["definition_de"], 95).replace("|", "\\|"),
                en=compact(row["definition_en"], 70).replace("|", "\\|"),
                tr=compact(row["definition_tr"], 70).replace("|", "\\|"),
                next_step=compact(row["suggested_next_step"], 90).replace("|", "\\|"),
            )
        )
    return "\n".join(lines)


def write_markdown(source: Path, source_rows: list[dict[str, str]], audit_rows: list[dict[str, str]]) -> None:
    issue_counter: Counter[str] = Counter()
    for row in audit_rows:
        for issue in row["issues"].split("; "):
            if issue:
                issue_counter[issue] += 1

    status_counter = Counter(row.get("entry_review_status") or "" for row in source_rows)
    entry_type_counter = Counter(row.get("entry_type") or "" for row in source_rows)

    content = [
        "# Lerch Glossary Publication Audit",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        f"- Source: `{source}`",
        f"- Rows audited: {len(source_rows)}",
        "- This report is a review aid only. It does not change the working glossary.",
        "- Priority 1 means check before any public import; higher numbers are lower urgency.",
        "",
        "## Review Status Snapshot",
        "",
    ]
    for key, count in status_counter.most_common():
        content.append(f"- {key or '(blank)'}: {count}")
    content.extend(["", "## Entry Types", ""])
    for key, count in entry_type_counter.most_common():
        content.append(f"- {key or '(blank)'}: {count}")
    content.extend(["", "## Issue Counts", ""])
    for key, count in issue_counter.most_common():
        content.append(f"- {key}: {count}")
    content.extend(
        [
            "",
            "## Highest-Priority Rows",
            "",
            markdown_table(audit_rows, 40),
            "",
            "## Files",
            "",
            f"- TSV audit queue: `{OUT_TSV.relative_to(REPO_ROOT)}`",
            f"- Summary: `{OUT_MD.relative_to(REPO_ROOT)}`",
        ]
    )
    OUT_MD.write_text("\n".join(content) + "\n", encoding="utf-8")


def main() -> None:
    source_rows = read_tsv(DEFAULT_GLOSSARY)
    audit_rows = [audit_row(row) for row in source_rows]
    audit_rows.sort(
        key=lambda row: (
            int(row["priority"]),
            row["entry_review_status"] != "ocr_extracted",
            row["entry_display"].casefold(),
            row["entry_id"],
        )
    )
    write_tsv(audit_rows)
    write_markdown(DEFAULT_GLOSSARY, source_rows, audit_rows)
    print(f"Wrote {OUT_TSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
