#!/usr/bin/env python3
"""Build a first high-value glossary review batch from the Lerch word index."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORD_INDEX = REPO_ROOT / "reports" / "lerch-word-index.tsv"
REPORT_DIR = REPO_ROOT / "reports"
REVIEW_DIR = REPO_ROOT / "reviews" / "lerch-glossary-review-batch-01"
BATCH_TSV = REPORT_DIR / "lerch-glossary-review-batch-01.tsv"
BATCH_MD = REPORT_DIR / "lerch-glossary-review-batch-01.md"


GRAMMAR_ONLY_KEYS = {
    "bi": "conjunctive/future prefix and several short inflected verb forms; review as grammar/morpheme, not as a simple new lexical headword.",
    "ne": "negative particle/prefix; connect to a negative morpheme entry rather than adding every inflected form.",
    "de": "locative/dative element and short pronoun-like forms; review under grammar/function entries.",
    "na": "short negative/demonstrative/verb-form ambiguity; review under existing function words if possible.",
    "we": "prefix/particle in compounds and verbs; review as morpheme/function element.",
    "ge": "short preverb/verb fragment in multiple contexts; review as grammar/morpheme.",
    "ka": "conditional/subordinator/auxiliary-like short form; review as function item.",
    "la": "short connector/phrase element; review before adding as lexical headword.",
}

LIKELY_ADD_KEYS = {
    "eskeri": "army, soldiers",
    "esker": "army, soldier",
    "deniai": "woman, wife",
    "deni": "woman",
    "pasai": "pasha, pasha title",
    "pasa": "pasha",
    "kagit": "paper, letter",
    "gelanke": "occasion, time/event",
    "namei": "name",
    "emsoe": "tonight",
    "het": "side, direction",
    "hete": "side, direction, with/to",
    "hadre": "ready",
    "rod": "day",
    "soba": "morning",
    "waxte": "time",
    "vist": "twenty",
    "tinu": "there is not / does not exist",
    "gai": "ox",
    "keinek": "girl",
    "daw": "village",
    "meiste": "tomorrow",
    "etia": "here",
    "bani": "house(s)",
    "launa": "kissed",
    "kidi": "small",
    "izmi": "permission",
    "vadi": "say, tell",
    "rez": "vineyard, vine",
    "simsyeri": "sword",
    "laser": "flood",
}

RELATED_KEY_ALIASES = {
    "daw": ("dau",),
    "gai": ("ga",),
    "gelanke": ("gelahke",),
    "hadre": ("hadru",),
    "kidi": ("kcina",),
    "keinek": ("kcina",),
    "simsyeri": ("simsyer",),
    "tina": ("tihu",),
    "tinu": ("tihu",),
    "vadi": ("va",),
}


@dataclass
class BatchRow:
    lemma_key: str
    suggested_action: str
    suggested_headword: str
    suggested_gloss_en: str
    suggested_gloss_tr: str
    rationale: str
    token_count: int
    text_count: int
    text_counts: str
    lemma_hints: str
    zazaki_variants: str
    lerch_variants: str
    context_gloss_hints: str
    related_glossary_hits: str
    example_ref: str
    example_token_zazaki: str
    example_token_lerch: str
    example_line_zazaki: str
    example_line_lerch: str
    review_status: str = "needs_human_review"
    reviewer_note: str = ""


def load_compare_module() -> Any:
    path = REPO_ROOT / "scripts" / "compare_lerch_text_forms_to_glossary.py"
    spec = importlib.util.spec_from_file_location("lerch_compare", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["lerch_compare"] = module
    spec.loader.exec_module(module)
    return module


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def compact_text(value: str, limit: int = 220) -> str:
    value = " ".join((value or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def title_case_headword(row: dict[str, str]) -> str:
    hints = [item.strip() for item in (row.get("lemma_hints") or "").split(";") if item.strip()]
    if hints:
        return hints[0]
    variants = [item.strip() for item in (row.get("zazaki_variants") or "").split(";") if item.strip()]
    if variants:
        return variants[0].lower()
    return row["lemma_key"]


def top_context_gloss(row: dict[str, str]) -> str:
    glosses = [item.strip() for item in (row.get("context_gloss_hints") or "").split(";") if item.strip()]
    return "; ".join(glosses[:3])


def related_hits(compare: Any, key: str, glossary_rows: list[dict[str, str]], limit: int = 4) -> str:
    key_norm = compare.compact(key)
    if not key_norm:
        return ""
    target_keys = {key_norm}
    target_keys.update(compare.compact(alias) for alias in RELATED_KEY_ALIASES.get(key_norm, ()) if alias)
    hits: list[str] = []
    seen: set[str] = set()
    for row in glossary_rows:
        search_values = [
            row.get("entry_search") or "",
            row.get("parent_search") or "",
            row.get("title_keys") or "",
            row.get("entry_display") or "",
            row.get("raw_headword") or "",
        ]
        search_keys = {compare.compact(value) for value in search_values if value}
        if not search_keys:
            continue
        matched = False
        for item in search_keys:
            if not item:
                continue
            if item in target_keys:
                matched = True
                break
            if len(key_norm) >= 4 and len(item) >= 4 and (item.startswith(key_norm[:4]) or key_norm.startswith(item[:4])):
                matched = True
                break
        if not matched:
            continue
        entry_id = row.get("entry_id") or row.get("entry_search") or row.get("entry_display") or ""
        if entry_id in seen:
            continue
        label = row.get("entry_display") or row.get("entry_search") or row.get("raw_headword") or entry_id
        entry_key = compare.compact(row.get("entry_search") or label)
        if len(entry_key) <= 2 and entry_key not in target_keys:
            continue
        seen.add(entry_id)
        gloss_bits = [
            row.get("definition_en") or "",
            row.get("definition_tr") or "",
            row.get("definition_de") or "",
        ]
        gloss = compact_text(next((bit for bit in gloss_bits if bit), ""), 80)
        hits.append(f"{label} [{entry_id}]" + (f": {gloss}" if gloss else ""))
        if len(hits) >= limit:
            break
    return " | ".join(hits)


def classify(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    key = row["lemma_key"]
    if key in GRAMMAR_ONLY_KEYS:
        return (
            "merge_or_function_entry",
            key,
            top_context_gloss(row),
            "",
            GRAMMAR_ONLY_KEYS[key],
        )
    if key in LIKELY_ADD_KEYS:
        return (
            "likely_add_or_merge",
            title_case_headword(row),
            LIKELY_ADD_KEYS[key],
            "",
            "Frequent text-attested form with a stable context gloss and no current exact glossary match.",
        )
    if "personal name" in (row.get("context_gloss_hints") or "").lower() or "place name" in (row.get("context_gloss_hints") or "").lower():
        return (
            "do_not_add_name_or_place",
            key,
            "",
            "",
            "Gloss hints indicate a name/place; keep out of the glossary unless there is a separate name index.",
        )
    if int(row.get("text_count") or 0) >= 3 and int(row.get("token_count") or 0) >= 3:
        return (
            "review_high_value",
            title_case_headword(row),
            top_context_gloss(row),
            "",
            "Occurs in multiple texts and should be checked against the scanned glossary/headword policy.",
        )
    return (
        "review_lower_priority",
        title_case_headword(row),
        top_context_gloss(row),
        "",
        "Included because it occurs frequently or has a useful context gloss, but needs manual headword judgment.",
    )


def build_batch(limit: int = 90) -> tuple[list[BatchRow], Counter[str]]:
    compare = load_compare_module()
    glossary_rows = read_tsv(compare.DEFAULT_GLOSSARY)
    word_rows = read_tsv(WORD_INDEX)
    candidates = [
        row
        for row in word_rows
        if row.get("status") == "review_candidate"
        and row.get("lemma_key")
        and int(row.get("token_count") or 0) >= 3
    ]
    candidates.sort(key=lambda row: (-int(row.get("token_count") or 0), -int(row.get("text_count") or 0), row["lemma_key"]))
    likely_rows = [row for row in candidates if row["lemma_key"] in LIKELY_ADD_KEYS]
    grammar_rows = [row for row in candidates if row["lemma_key"] in GRAMMAR_ONLY_KEYS]
    other_rows = [row for row in candidates if row["lemma_key"] not in LIKELY_ADD_KEYS and row["lemma_key"] not in GRAMMAR_ONLY_KEYS]
    selected: list[dict[str, str]] = []
    seen_keys: set[str] = set()
    for group, group_limit in ((likely_rows, 35), (grammar_rows, 12), (other_rows, limit)):
        for row in group:
            if row["lemma_key"] in seen_keys:
                continue
            selected.append(row)
            seen_keys.add(row["lemma_key"])
            if group is not other_rows and len([item for item in selected if item in group]) >= group_limit:
                break
            if len(selected) >= limit:
                break
        if len(selected) >= limit:
            break

    batch: list[BatchRow] = []
    action_counts: Counter[str] = Counter()
    for row in selected[:limit]:
        action, headword, gloss_en, gloss_tr, rationale = classify(row)
        action_counts[action] += 1
        batch.append(
            BatchRow(
                lemma_key=row["lemma_key"],
                suggested_action=action,
                suggested_headword=headword,
                suggested_gloss_en=gloss_en,
                suggested_gloss_tr=gloss_tr,
                rationale=rationale,
                token_count=int(row.get("token_count") or 0),
                text_count=int(row.get("text_count") or 0),
                text_counts=row.get("text_counts") or "",
                lemma_hints=row.get("lemma_hints") or "",
                zazaki_variants=row.get("zazaki_variants") or "",
                lerch_variants=row.get("lerch_variants") or "",
                context_gloss_hints=row.get("context_gloss_hints") or "",
                related_glossary_hits=related_hits(compare, row["lemma_key"], glossary_rows),
                example_ref=row.get("example_ref") or "",
                example_token_zazaki=row.get("example_token_zazaki") or "",
                example_token_lerch=row.get("example_token_lerch") or "",
                example_line_zazaki=compact_text(row.get("example_line_zazaki") or ""),
                example_line_lerch=compact_text(row.get("example_line_lerch") or ""),
            )
        )
    return batch, action_counts


def write_batch_tsv(path: Path, rows: list[BatchRow]) -> None:
    fields = list(BatchRow.__dataclass_fields__.keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def md_row(cells: list[str]) -> str:
    return "| " + " | ".join((cell or "").replace("|", "\\|") for cell in cells) + " |"


def write_report(path: Path, rows: list[BatchRow], action_counts: Counter[str]) -> None:
    lines: list[str] = []
    lines.append("# Lerch Glossary Review Batch 01")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("- Review batch built from `reports/lerch-word-index.tsv`.")
    lines.append("- It does not modify the working glossary.")
    lines.append("- The batch is intentionally conservative: frequent unmatched forms are proposed for review, not automatically imported.")
    lines.append("- `merge_or_function_entry` rows should usually become grammar/morpheme links rather than standalone dictionary headwords.")
    lines.append("")
    lines.append("## Batch Counts")
    lines.append("")
    lines.append(f"- Rows in batch: {len(rows)}")
    for action, count in action_counts.most_common():
        lines.append(f"- {action}: {count}")
    lines.append("")
    lines.append("## Highest Priority Rows")
    lines.append("")
    lines.append(md_row(["Key", "Action", "Suggested headword", "Tokens", "Texts", "Gloss hint", "Related glossary hit", "Example"]))
    lines.append(md_row(["---", "---", "---", "---:", "---:", "---", "---", "---"]))
    for row in rows[:50]:
        lines.append(
            md_row(
                [
                    row.lemma_key,
                    row.suggested_action,
                    row.suggested_headword,
                    str(row.token_count),
                    str(row.text_count),
                    row.suggested_gloss_en or row.context_gloss_hints,
                    compact_text(row.related_glossary_hits, 120),
                    row.example_ref,
                ]
            )
        )
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("- Editable TSV: `reports/lerch-glossary-review-batch-01.tsv`")
    lines.append("- Summary: `reports/lerch-glossary-review-batch-01.md`")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_review_data(path: Path, rows: list[BatchRow], action_counts: Counter[str]) -> None:
    payload = {
        "generated": date.today().isoformat(),
        "source_tsv": "reports/lerch-glossary-review-batch-01.tsv",
        "source_word_index": "reports/lerch-word-index.tsv",
        "counts": dict(action_counts),
        "rows": [
            {field: getattr(row, field) for field in BatchRow.__dataclass_fields__}
            for row in rows
        ],
    }
    path.write_text(
        "window.LERCH_GLOSSARY_REVIEW_BATCH_01 = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    if not WORD_INDEX.exists():
        raise SystemExit(f"Word index not found: {WORD_INDEX}. Run scripts/build_lerch_word_index.py first.")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    rows, action_counts = build_batch()
    write_batch_tsv(BATCH_TSV, rows)
    write_report(BATCH_MD, rows, action_counts)
    write_review_data(REVIEW_DIR / "batch-data.js", rows, action_counts)
    print(f"Wrote {len(rows)} glossary review rows.")
    print(f"Wrote {BATCH_TSV}")
    print(f"Wrote {BATCH_MD}")
    print(f"Wrote {REVIEW_DIR / 'batch-data.js'}")


if __name__ == "__main__":
    main()
