#!/usr/bin/env python3
"""Build a word-form index for the processed Lerch Zazaki texts.

This script is intentionally report-only. It reads the processed text
interlinear TSV files and the current local Lerch glossary TSV, then writes a
durable index that can be reviewed before any public glossary import.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXT_ROOT = REPO_ROOT / "texts" / "lerch"
REPORT_DIR = REPO_ROOT / "reports"


def load_compare_module() -> Any:
    path = REPO_ROOT / "scripts" / "compare_lerch_text_forms_to_glossary.py"
    spec = importlib.util.spec_from_file_location("lerch_compare", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["lerch_compare"] = module
    spec.loader.exec_module(module)
    return module


@dataclass
class WordBucket:
    key: str
    token_count: int = 0
    texts: Counter[str] = field(default_factory=Counter)
    variants_zazaki: Counter[str] = field(default_factory=Counter)
    variants_lerch: Counter[str] = field(default_factory=Counter)
    lemmas: Counter[str] = field(default_factory=Counter)
    glosses: Counter[str] = field(default_factory=Counter)
    examples: list[dict[str, str]] = field(default_factory=list)
    match_sources: set[str] = field(default_factory=set)
    matched_entries: dict[str, dict[str, str]] = field(default_factory=dict)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_source_lines() -> dict[tuple[str, str], dict[str, str]]:
    lines: dict[tuple[str, str], dict[str, str]] = {}
    for text_dir in sorted(TEXT_ROOT.iterdir()):
        if not text_dir.is_dir():
            continue
        payload_path = text_dir / "text-document.json"
        if not payload_path.exists():
            continue
        payload = read_json(payload_path)
        for line in payload.get("source_lines") or []:
            if not isinstance(line, dict):
                continue
            segment_id = str(line.get("id") or "")
            if not segment_id:
                continue
            lines[(text_dir.name, segment_id)] = {
                "zazaki": str(line.get("zazaki") or ""),
                "lerch": str(line.get("lerch") or line.get("text") or ""),
                "title": str(line.get("title") or ""),
            }
    return lines


def top_values(counter: Counter[str], limit: int = 8) -> str:
    return "; ".join(value for value, _count in counter.most_common(limit) if value)


def glossary_entry_label(row: dict[str, str]) -> str:
    return (
        row.get("entry_display")
        or row.get("entry")
        or row.get("raw_headword")
        or row.get("entry_id")
        or ""
    )


def add_matches(compare: Any, bucket: WordBucket, record: Any, glossary_index: dict[str, list[dict[str, str]]]) -> None:
    if compare.compact(record.lemma):
        values = {"lemma": {record.lemma}}
    else:
        values = {
            "surface_zazaki": {record.token_zazaki},
            "surface_lerch": {record.token_lerch},
        }
    candidate_keys = {
        source: {key for value in raw_values for key in compare.candidate_forms(value) if key}
        for source, raw_values in values.items()
    }
    for source, keys in candidate_keys.items():
        for candidate_key in keys:
            rows = compare.matching_rows_for_key(candidate_key, glossary_index)
            if not rows:
                continue
            bucket.match_sources.add(source)
            for row in rows[:8]:
                entry_id = row.get("entry_id") or glossary_entry_label(row)
                if not entry_id:
                    continue
                bucket.matched_entries.setdefault(
                    entry_id,
                    {
                        "entry": glossary_entry_label(row),
                        "entry_search": row.get("entry_search") or "",
                        "definition_de": row.get("definition_de") or "",
                        "definition_en": row.get("definition_en") or "",
                        "definition_tr": row.get("definition_tr") or "",
                        "review_status": row.get("entry_review_status") or "",
                    },
                )


def is_proper_name(compare: Any, bucket: WordBucket) -> bool:
    form_bucket = compare.FormBucket(key=bucket.key)
    form_bucket.glosses = bucket.glosses.copy()
    return bool(compare.is_proper_name_bucket(form_bucket))


def status_for(compare: Any, bucket: WordBucket) -> str:
    if is_proper_name(compare, bucket):
        return "proper_name_or_place"
    if bucket.match_sources:
        return "glossary_match"
    if bucket.token_count >= 3 or len(bucket.texts) >= 2:
        return "review_candidate"
    return "low_frequency_unmatched"


def build_index(compare: Any) -> tuple[list[WordBucket], dict[str, Any]]:
    titles = compare.load_text_titles()
    records = compare.load_token_records(titles)
    glossary_rows, glossary_index = compare.load_glossary_index(compare.DEFAULT_GLOSSARY)
    source_lines = load_source_lines()

    buckets: dict[str, WordBucket] = {}
    for record in records:
        key = compare.compact(record.lemma) or compare.compact(record.token_zazaki) or compare.compact(record.token_lerch)
        if not key:
            continue
        bucket = buckets.setdefault(key, WordBucket(key=key))
        bucket.token_count += 1
        bucket.texts[record.text_slug] += 1
        if record.token_zazaki:
            bucket.variants_zazaki[record.token_zazaki] += 1
        if record.token_lerch:
            bucket.variants_lerch[record.token_lerch] += 1
        if record.lemma:
            bucket.lemmas[record.lemma] += 1
        for gloss in record.glosses:
            if gloss:
                bucket.glosses[gloss] += 1
        if len(bucket.examples) < 5:
            line = source_lines.get((record.text_slug, record.segment_id), {})
            bucket.examples.append(
                {
                    "text_slug": record.text_slug,
                    "segment_id": record.segment_id,
                    "token_index": str(record.token_index),
                    "token_zazaki": record.token_zazaki,
                    "token_lerch": record.token_lerch,
                    "line_zazaki": line.get("zazaki", ""),
                    "line_lerch": line.get("lerch", ""),
                }
            )
        add_matches(compare, bucket, record, glossary_index)

    metadata = {
        "token_records": len(records),
        "glossary_rows": len(glossary_rows),
        "source_glossary": str(compare.DEFAULT_GLOSSARY),
    }
    return list(buckets.values()), metadata


def write_tsv(path: Path, compare: Any, buckets: list[WordBucket]) -> None:
    fields = [
        "lemma_key",
        "status",
        "token_count",
        "text_count",
        "text_counts",
        "lemma_hints",
        "zazaki_variants",
        "lerch_variants",
        "context_gloss_hints",
        "glossary_entries",
        "glossary_match_sources",
        "example_ref",
        "example_token_zazaki",
        "example_token_lerch",
        "example_line_zazaki",
        "example_line_lerch",
    ]
    sorted_buckets = sorted(buckets, key=lambda item: (status_for(compare, item), item.key))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        for bucket in sorted_buckets:
            example = bucket.examples[0] if bucket.examples else {}
            entries = [
                data["entry"]
                for data in bucket.matched_entries.values()
                if data.get("entry")
            ]
            writer.writerow(
                {
                    "lemma_key": bucket.key,
                    "status": status_for(compare, bucket),
                    "token_count": bucket.token_count,
                    "text_count": len(bucket.texts),
                    "text_counts": "; ".join(f"{text}:{count}" for text, count in bucket.texts.most_common()),
                    "lemma_hints": top_values(bucket.lemmas),
                    "zazaki_variants": top_values(bucket.variants_zazaki),
                    "lerch_variants": top_values(bucket.variants_lerch),
                    "context_gloss_hints": top_values(bucket.glosses),
                    "glossary_entries": "; ".join(dict.fromkeys(entries)),
                    "glossary_match_sources": "; ".join(sorted(bucket.match_sources)),
                    "example_ref": (
                        f"{example.get('text_slug')}:{example.get('segment_id')}:{example.get('token_index')}"
                        if example
                        else ""
                    ),
                    "example_token_zazaki": example.get("token_zazaki", ""),
                    "example_token_lerch": example.get("token_lerch", ""),
                    "example_line_zazaki": example.get("line_zazaki", ""),
                    "example_line_lerch": example.get("line_lerch", ""),
                }
            )


def write_report(path: Path, compare: Any, buckets: list[WordBucket], metadata: dict[str, Any]) -> None:
    statuses = Counter(status_for(compare, bucket) for bucket in buckets)
    review_candidates = [
        bucket for bucket in buckets if status_for(compare, bucket) == "review_candidate"
    ]
    review_candidates.sort(key=lambda item: (-item.token_count, -len(item.texts), item.key))

    matched = [bucket for bucket in buckets if bucket.match_sources]
    matched.sort(key=lambda item: (-item.token_count, item.key))

    lines: list[str] = []
    lines.append("# Lerch All-Text Word Index")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("- Groups every token in `texts/lerch/*/morphemes.tsv` by the current interlinear lemma key, falling back to the normalized surface form when no lemma is present.")
    lines.append("- Preserves the Zazaki and Lerch-orthography variants that occur in the processed texts.")
    lines.append("- Compares each bucket against the current local Lerch glossary with the same broad matching and known-alias policy used by the candidate review report.")
    lines.append("- This report is a review aid; it does not add or modify glossary entries.")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append(f"- Token records: {metadata['token_records']}")
    lines.append(f"- Glossary rows: {metadata['glossary_rows']}")
    lines.append(f"- Glossary: `{metadata['source_glossary']}`")
    lines.append("")
    lines.append("## Status Counts")
    lines.append("")
    lines.append("| Status | Lemma/form buckets |")
    lines.append("| --- | ---: |")
    for status, count in statuses.most_common():
        lines.append(f"| {status} | {count} |")
    lines.append("")
    lines.append("## Highest-Priority Review Candidates")
    lines.append("")
    lines.append("These forms occur often enough to review, are not currently classified as names/places, and did not match the working Lerch glossary.")
    lines.append("")
    lines.append("| Form key | Tokens | Texts | Zazaki variants | Lerch variants | Gloss hints | Example |")
    lines.append("| --- | ---: | ---: | --- | --- | --- | --- |")
    for bucket in review_candidates[:120]:
        example = bucket.examples[0] if bucket.examples else {}
        example_ref = (
            f"{example.get('text_slug')}:{example.get('segment_id')}:{example.get('token_index')}"
            if example
            else ""
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    bucket.key,
                    str(bucket.token_count),
                    str(len(bucket.texts)),
                    top_values(bucket.variants_zazaki, 4).replace("|", "\\|"),
                    top_values(bucket.variants_lerch, 4).replace("|", "\\|"),
                    top_values(bucket.glosses, 4).replace("|", "\\|"),
                    example_ref,
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Most Frequent Glossary-Matched Forms")
    lines.append("")
    lines.append("| Form key | Tokens | Texts | Glossary entries | Gloss hints |")
    lines.append("| --- | ---: | ---: | --- | --- |")
    for bucket in matched[:80]:
        entries = [
            data["entry"]
            for data in bucket.matched_entries.values()
            if data.get("entry")
        ]
        lines.append(
            "| "
            + " | ".join(
                [
                    bucket.key,
                    str(bucket.token_count),
                    str(len(bucket.texts)),
                    "; ".join(dict.fromkeys(entries[:5])).replace("|", "\\|"),
                    top_values(bucket.glosses, 3).replace("|", "\\|"),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("- Full TSV index: `reports/lerch-word-index.tsv`")
    lines.append("- Summary report: `reports/lerch-word-index.md`")
    lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    compare = load_compare_module()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    buckets, metadata = build_index(compare)
    write_tsv(REPORT_DIR / "lerch-word-index.tsv", compare, buckets)
    write_report(REPORT_DIR / "lerch-word-index.md", compare, buckets, metadata)
    print(f"Indexed {metadata['token_records']} token records into {len(buckets)} lemma/form buckets.")
    print(f"Wrote {REPORT_DIR / 'lerch-word-index.tsv'}")
    print(f"Wrote {REPORT_DIR / 'lerch-word-index.md'}")


if __name__ == "__main__":
    main()
