#!/usr/bin/env python3
"""Compare processed Lerch text forms against the current local Lerch glossary.

This is intentionally a conservative review helper. It does not mutate the
text documents or the glossary; it produces a report and a TSV candidate list
for forms that are common in the processed texts but do not yet have an obvious
match in the glossary working table.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXT_ROOT = REPO_ROOT / "texts" / "lerch"
REPORT_DIR = REPO_ROOT / "reports"
REVIEW_DIR = REPO_ROOT / "reviews" / "lerch-glossary-candidates"

DEFAULT_GLOSSARY = Path(
    r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lltools_import\lltools_dictionary_lerch_glossary_full.tsv"
)

PUNCT_RE = re.compile(r"[^\w\s]+", re.UNICODE)
WHITESPACE_RE = re.compile(r"\s+")
GLOSSARY_SPLIT_RE = re.compile(r"[|,;/]+")

# Normalized text forms that are clearly inflected/case-marked variants of a
# headword already represented in Lerch's glossary.  This keeps the review UI
# focused on real lexical gaps instead of asking whether forms like `şi` or
# `amêy` should become new headwords.
KNOWN_FORM_ALIASES: dict[str, tuple[str, ...]] = {
    # Pronouns / pronominal cases.
    "me": ("mjri", "ez"),
    "mi": ("mjri", "ez"),
    "miri": ("mjri", "ez"),
    "ma": ("rna",),
    "te": ("tu",),
    "tue": ("tu",),
    "tueri": ("tu",),
    "tuerira": ("tu",),
    "tweri": ("tu",),
    "twerira": ("tu",),
    "suma": ("sima",),
    "sımari": ("sima",),
    "simari": ("sima",),
    "xoe": ("ez",),
    "xoeri": ("ez",),
    "ena": ("ana", "awe"),
    "enoe": ("ana", "awe"),
    "enye": ("ana", "awe"),
    # Common verbs and transparent inflected forms.
    "si": ("siyayene", "siyene", "sussna", "sc", "sl"),
    "sye": ("siyayene", "siyene", "sussna"),
    "swe": ("siyayene", "siyene", "sussna"),
    "sueni": ("siyayene", "siyene", "sussna"),
    "sweni": ("siyayene", "siyene", "sussna"),
    "syeri": ("siyayene", "siyene", "sussna"),
    "ame": ("amayene",),
    "amey": ("amayene",),
    "ameya": ("amayene",),
    "amei": ("amayene",),
    "ameiya": ("amayene",),
    "werist": ("weriat", "warzdna"),
    "weristi": ("weriat", "warzdna"),
    "ersawute": ("eraauute",),
    "ersauute": ("eraauute",),
    "day": ("dayene", "dana", "da"),
    "dai": ("dayene", "dana", "da"),
    "bide": ("dayene", "dana", "da"),
    "bid": ("dayene", "dana", "da"),
    "byari": ("ardene",),
    "warze": ("warzdna",),
    "kawta": ("siyayene", "siyene", "sussna"),
    "swena": ("siyayene", "siyene", "sussna"),
    "yenu": ("amayene",),
    "kist": ("kisena",),
    "kisti": ("kisena",),
    "kistu": ("kisena",),
    "kenu": ("kena", "kerdene"),
    # Common nouns/titles already present under OCR-shaped glossary keys.
    "agay": ("aya", "aga", "axa"),
    "agayi": ("aya", "aga", "axa"),
    "beray": ("berd",),
    "berai": ("berd",),
    "kawge": ("kauya",),
    "kauge": ("kauya",),
    "lwe": ("lu",),
    "lue": ("lu",),
    "arewangci": ("arewantf",),
    "arewanti": ("arewantf",),
    "dewi": ("dau",),
    "dyewi": ("dau",),
    "keye": ("kei",),
    "keiye": ("kei",),
    "keynay": ("kcina",),
    "keynek": ("kcina",),
    "keyneke": ("kcina",),
    "keina": ("kcina",),
    "keinai": ("kcina",),
    "sere": ("ser",),
    "serey": ("ser",),
    # Lerch's OCR table embeds habür under the häl row.
    "habere": ("hal",),
    "haber": ("hal",),
    "mela": ("mola",),
    "hemine": ("heme",),
    "heta": ("hetaku",),
    "esti": ("estii",),
    "estu": ("estii",),
    "cinyu": ("tihu",),
    "cinu": ("tihu",),
    "ceher": ("tehtir",),
    "teher": ("tehtir",),
    "hirye": ("diei",),
    "gay": ("ga",),
    "espar": ("sstere",),
    "etya": ("gtia",),
    "meyste": ("melate",),
    "puroe": ("pero",),
    "wica": ("widd",),
    "awnya": ("aununa", "di"),
    "awnyay": ("aununa", "di"),
    "desmac": ("desmal",),
}

PROPER_NAME_KEYS = {
    "xalef",
    "halef",
    "ali",
    "ahmed",
    "ahmedi",
    "daqma",
    "qasim",
    "qasimi",
    "hasanek",
    "hasaneki",
    "hasan",
    "saban",
    "hyeni",
    "sivani",
    "nerib",
    "nyerib",
    "misri",
    "cemcaqu",
    "temtaqu",
    "cemcequ",
    "temtequ",
    "sele",
}

PROPER_NAME_HINTS = (
    "personal name",
    "person name",
    "place name",
    "group name",
    "tribe name",
    "kişi adı",
    "yer adı",
)

CHAR_MAP = str.maketrans(
    {
        "ı": "i",
        "İ": "i",
        "ê": "e",
        "Ê": "e",
        "û": "u",
        "Û": "u",
        "ü": "u",
        "Ü": "u",
        "ö": "o",
        "Ö": "o",
        "ş": "s",
        "Ş": "s",
        "ç": "c",
        "Ç": "c",
        "ğ": "g",
        "Ğ": "g",
        "γ": "g",
        "Γ": "g",
        "χ": "x",
        "Χ": "x",
        "ḳ": "k",
        "Ḳ": "k",
        "ḍ": "d",
        "Ḍ": "d",
        "ṭ": "t",
        "Ṭ": "t",
        "ẓ": "z",
        "Ẓ": "z",
        "ṣ": "s",
        "Ṣ": "s",
        "ʿ": "",
        "ʾ": "",
        "ʼ": "",
        "’": "",
        "'": "",
        "`": "",
    }
)


@dataclass
class TokenRecord:
    text_slug: str
    text_title: str
    segment_id: str
    token_index: int
    token_lerch: str
    token_zazaki: str
    lemma: str
    glosses: list[str] = field(default_factory=list)
    morphemes: list[str] = field(default_factory=list)


@dataclass
class FormBucket:
    key: str
    token_count: int = 0
    texts: Counter[str] = field(default_factory=Counter)
    variants: Counter[str] = field(default_factory=Counter)
    lemmas: Counter[str] = field(default_factory=Counter)
    glosses: Counter[str] = field(default_factory=Counter)
    examples: list[TokenRecord] = field(default_factory=list)
    match_sources: set[str] = field(default_factory=set)
    matched_entries: set[str] = field(default_factory=set)


def normalize(value: str) -> str:
    value = value or ""
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.translate(CHAR_MAP).lower()
    value = PUNCT_RE.sub(" ", value)
    value = WHITESPACE_RE.sub(" ", value).strip()
    return value


def compact(value: str) -> str:
    return normalize(value).replace(" ", "")


def add_case_stripped_forms(forms: set[str], key: str) -> None:
    if len(key) <= 3:
        return
    candidates = {key}
    for suffix in ("ri", "ra"):
        if len(key) > 4 and key.endswith(suffix):
            candidates.add(key[: -len(suffix)])
    expanded = set(candidates)
    for candidate in candidates:
        if len(candidate) > 3 and candidate.endswith(("i", "y")):
            expanded.add(candidate[:-1])
    forms.update(item for item in expanded if item)


def key_forms(value: str, *, split_words: bool = False) -> set[str]:
    forms: set[str] = set()
    values = [value]
    values.extend(GLOSSARY_SPLIT_RE.split(value or ""))
    for raw in values:
        for key in (normalize(raw), compact(raw)):
            if key:
                forms.add(key)
        if split_words:
            for part in normalize(raw).split():
                if part:
                    forms.add(part)
    return forms


def candidate_forms(value: str) -> set[str]:
    forms: set[str] = set()
    for key in (normalize(value), compact(value)):
        if key:
            forms.add(key)
            add_case_stripped_forms(forms, key)
    return forms


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_text_titles() -> dict[str, str]:
    titles: dict[str, str] = {}
    for text_dir in sorted(TEXT_ROOT.iterdir()):
        if not text_dir.is_dir():
            continue
        metadata_path = text_dir / "metadata.json"
        if metadata_path.exists():
            metadata = read_json(metadata_path)
            titles[text_dir.name] = metadata.get("title") or text_dir.name
        else:
            titles[text_dir.name] = text_dir.name
    return titles


def load_token_records(titles: dict[str, str]) -> list[TokenRecord]:
    records_by_token: dict[tuple[str, str, int], TokenRecord] = {}
    for text_dir in sorted(TEXT_ROOT.iterdir()):
        morpheme_path = text_dir / "morphemes.tsv"
        if not morpheme_path.exists():
            continue
        rows = read_tsv(morpheme_path)
        for row in rows:
            try:
                token_index = int(row.get("token_index") or 0)
            except ValueError:
                token_index = 0
            key = (text_dir.name, row.get("segment_id") or "", token_index)
            record = records_by_token.get(key)
            if record is None:
                record = TokenRecord(
                    text_slug=text_dir.name,
                    text_title=titles.get(text_dir.name, text_dir.name),
                    segment_id=row.get("segment_id") or "",
                    token_index=token_index,
                    token_lerch=row.get("token_lerch") or "",
                    token_zazaki=row.get("token_zazaki") or "",
                    lemma=row.get("lemma") or "",
                )
                records_by_token[key] = record
            morpheme = row.get("morpheme_surface_lerch") or row.get("morpheme_normalized") or ""
            gloss = row.get("gloss") or ""
            if morpheme:
                record.morphemes.append(morpheme)
            if gloss:
                record.glosses.append(gloss)
    return list(records_by_token.values())


def glossary_keys(row: dict[str, str]) -> set[str]:
    keys: set[str] = set()
    for field_name in (
        "entry",
        "entry_display",
        "entry_search",
        "parent",
        "parent_search",
        "raw_headword",
    ):
        value = row.get(field_name) or ""
        keys.update(key_forms(value, split_words=field_name in {"parent", "parent_search", "title_keys"}))
    for value in (row.get("title_keys") or "").split("|"):
        keys.update(key_forms(value, split_words=True))
    return keys


def load_glossary_index(path: Path) -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]]]]:
    rows = read_tsv(path)
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        for key in glossary_keys(row):
            index[key].append(row)
    return rows, index


def candidate_keys(record: TokenRecord) -> dict[str, set[str]]:
    values = {
        "surface_zazaki": {record.token_zazaki},
        "surface_lerch": {record.token_lerch},
        "lemma": {record.lemma},
        "morpheme": set(record.morphemes),
    }
    return {
        source: {key for value in raw_values for key in candidate_forms(value) if key}
        for source, raw_values in values.items()
    }


def matching_rows_for_key(candidate_key: str, glossary_index: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows = list(glossary_index.get(candidate_key) or [])
    seen = {row.get("entry_id") for row in rows}
    for alias_key in KNOWN_FORM_ALIASES.get(candidate_key, ()):
        for row in glossary_index.get(alias_key, []) or []:
            row_id = row.get("entry_id")
            if row_id not in seen:
                rows.append(row)
                seen.add(row_id)
    return rows


def add_match(bucket: FormBucket, source: str, rows: list[dict[str, str]]) -> None:
    bucket.match_sources.add(source)
    for row in rows[:5]:
        label = row.get("entry_display") or row.get("entry") or row.get("raw_headword") or row.get("entry_id") or ""
        if label:
            bucket.matched_entries.add(label)


def build_buckets(records: list[TokenRecord], glossary_index: dict[str, list[dict[str, str]]]) -> dict[str, FormBucket]:
    buckets: dict[str, FormBucket] = {}
    for record in records:
        key = compact(record.token_zazaki) or compact(record.token_lerch) or compact(record.lemma)
        if not key:
            continue
        bucket = buckets.setdefault(key, FormBucket(key=key))
        bucket.token_count += 1
        bucket.texts[record.text_slug] += 1
        if record.token_zazaki:
            bucket.variants[record.token_zazaki] += 1
        if record.token_lerch and record.token_lerch != record.token_zazaki:
            bucket.variants[record.token_lerch] += 1
        if record.lemma:
            bucket.lemmas[record.lemma] += 1
        for gloss in record.glosses:
            bucket.glosses[gloss] += 1
        if len(bucket.examples) < 3:
            bucket.examples.append(record)
        for source, keys in candidate_keys(record).items():
            for candidate_key in keys:
                matches = matching_rows_for_key(candidate_key, glossary_index)
                if matches:
                    add_match(bucket, source, matches)
    return buckets


def is_proper_name_bucket(bucket: FormBucket) -> bool:
    if bucket.key in PROPER_NAME_KEYS:
        return True
    gloss_text = " ".join(bucket.glosses).lower()
    if any(hint in gloss_text for hint in PROPER_NAME_HINTS):
        return True
    if "sivan tribe" in gloss_text or "hyeni" in gloss_text:
        return True
    return False


def top_values(counter: Counter[str], limit: int = 5) -> str:
    return "; ".join(value for value, _count in counter.most_common(limit))


def example_text(record: TokenRecord) -> str:
    gloss = "; ".join(dict.fromkeys(record.glosses))
    return f"{record.text_slug}:{record.segment_id}:{record.token_index} {record.token_zazaki or record.token_lerch}" + (
        f" = {gloss}" if gloss else ""
    )


def write_candidate_tsv(path: Path, buckets: dict[str, FormBucket]) -> list[FormBucket]:
    candidates = [
        bucket
        for bucket in buckets.values()
        if not bucket.match_sources
        and not is_proper_name_bucket(bucket)
        and (bucket.token_count >= 3 or len(bucket.texts) >= 2)
    ]
    candidates.sort(key=lambda item: (-item.token_count, -len(item.texts), item.key))
    fields = [
        "normalized_form",
        "token_count",
        "text_count",
        "texts",
        "variants",
        "lemmas",
        "best_gloss_hint",
        "examples",
        "review_action",
        "review_note",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        for bucket in candidates:
            writer.writerow(
                {
                    "normalized_form": bucket.key,
                    "token_count": bucket.token_count,
                    "text_count": len(bucket.texts),
                    "texts": "; ".join(f"{text}:{count}" for text, count in bucket.texts.most_common()),
                    "variants": top_values(bucket.variants),
                    "lemmas": top_values(bucket.lemmas),
                    "best_gloss_hint": top_values(bucket.glosses, 3),
                    "examples": " | ".join(example_text(record) for record in bucket.examples),
                    "review_action": "needs_review",
                    "review_note": "not_reviewed",
                }
            )
    return candidates


def candidate_payload(bucket: FormBucket) -> dict[str, object]:
    return {
        "normalized_form": bucket.key,
        "token_count": bucket.token_count,
        "text_count": len(bucket.texts),
        "texts": [{"text": text, "count": count} for text, count in bucket.texts.most_common()],
        "variants": [{"value": value, "count": count} for value, count in bucket.variants.most_common(8)],
        "lemmas": [{"value": value, "count": count} for value, count in bucket.lemmas.most_common(8)],
        "gloss_hints": [{"value": value, "count": count} for value, count in bucket.glosses.most_common(8)],
        "examples": [
            {
                "text_slug": record.text_slug,
                "segment_id": record.segment_id,
                "token_index": record.token_index,
                "token_zazaki": record.token_zazaki,
                "token_lerch": record.token_lerch,
                "lemma": record.lemma,
                "glosses": list(dict.fromkeys(record.glosses)),
            }
            for record in bucket.examples
        ],
    }


def write_review_data_js(path: Path, candidates: list[FormBucket]) -> None:
    payload = {
        "generated": date.today().isoformat(),
        "source_report": "reports/lerch-glossary-text-form-comparison.md",
        "source_tsv": "reports/lerch-glossary-text-form-comparison.tsv",
        "candidate_count": len(candidates),
        "candidates": [candidate_payload(bucket) for bucket in candidates],
    }
    path.write_text(
        "window.LERCH_GLOSSARY_CANDIDATES = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )


def write_report(
    path: Path,
    glossary_path: Path,
    glossary_rows: list[dict[str, str]],
    records: list[TokenRecord],
    buckets: dict[str, FormBucket],
    candidates: list[FormBucket],
) -> None:
    matched = [bucket for bucket in buckets.values() if bucket.match_sources]
    unmatched = [bucket for bucket in buckets.values() if not bucket.match_sources]
    review_status = Counter(row.get("entry_review_status") or "(blank)" for row in glossary_rows)
    rows_with_tr = sum(1 for row in glossary_rows if row.get("definition_tr"))
    rows_with_en = sum(1 for row in glossary_rows if row.get("definition_en"))
    rows_with_de = sum(1 for row in glossary_rows if row.get("definition_de"))

    source_counts = Counter()
    for bucket in matched:
        for source in bucket.match_sources:
            source_counts[source] += 1

    lines: list[str] = []
    lines.append("# Lerch Text Forms vs Local Glossary Comparison")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("- Compares `texts/lerch/*/morphemes.tsv` against the current local 600-row Lerch glossary TSV.")
    lines.append("- This is a review aid only. It uses broad accent-insensitive matching plus a known-alias map for common inflected forms, pronouns, and spelling variants. It can find obvious candidates but cannot replace manual lemma review.")
    lines.append("- Proper names and known place names are filtered out before the review list is generated.")
    lines.append("- No source text, translation, or glossary files were modified.")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append(f"- Glossary: `{glossary_path}`")
    lines.append("- Text source: `texts/lerch/*/morphemes.tsv`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("| --- | ---: |")
    lines.append(f"| Glossary rows | {len(glossary_rows)} |")
    lines.append(f"| Glossary rows with German gloss | {rows_with_de} |")
    lines.append(f"| Glossary rows with English gloss | {rows_with_en} |")
    lines.append(f"| Glossary rows with Turkish gloss | {rows_with_tr} |")
    lines.append(f"| Token records scanned | {len(records)} |")
    lines.append(f"| Unique normalized text forms | {len(buckets)} |")
    lines.append(f"| Forms with at least one glossary match | {len(matched)} |")
    lines.append(f"| Forms without an obvious glossary match | {len(unmatched)} |")
    lines.append(f"| High-priority unmatched review candidates | {len(candidates)} |")
    lines.append("")
    lines.append("## Glossary Review State")
    lines.append("")
    lines.append("| Review status | Rows |")
    lines.append("| --- | ---: |")
    for status, count in review_status.most_common():
        lines.append(f"| {status} | {count} |")
    lines.append("")
    lines.append("## Match Sources")
    lines.append("")
    lines.append("| Source | Unique forms matched |")
    lines.append("| --- | ---: |")
    for source, count in source_counts.most_common():
        lines.append(f"| {source} | {count} |")
    lines.append("")
    lines.append("## Top Unmatched Review Candidates")
    lines.append("")
    lines.append("These are good candidates for glossary review/addition because they are frequent or occur in multiple texts and do not have an obvious match under the broad matching and known-alias policy.")
    lines.append("")
    lines.append("| Form | Tokens | Texts | Variants | Gloss hint | Example |")
    lines.append("| --- | ---: | ---: | --- | --- | --- |")
    for bucket in candidates[:80]:
        example = example_text(bucket.examples[0]) if bucket.examples else ""
        lines.append(
            "| "
            + " | ".join(
                [
                    bucket.key,
                    str(bucket.token_count),
                    str(len(bucket.texts)),
                    top_values(bucket.variants, 4).replace("|", "\\|"),
                    top_values(bucket.glosses, 2).replace("|", "\\|"),
                    example.replace("|", "\\|"),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Next Review Actions")
    lines.append("")
    lines.append("1. Use `reports/lerch-glossary-text-form-comparison.tsv` as the editable checklist.")
    lines.append("2. Mark each candidate as `add_entry`, `merge_with_existing`, `inflected_form_only`, `proper_name`, or `ignore` in the `review_action` column.")
    lines.append("3. Promote reviewed candidates into a publication glossary table only after checking Lerch's scanned glossary page for the headword/diacritics.")
    lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    glossary_path = DEFAULT_GLOSSARY
    if not glossary_path.exists():
        raise SystemExit(f"Glossary TSV not found: {glossary_path}")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    titles = load_text_titles()
    records = load_token_records(titles)
    glossary_rows, glossary_index = load_glossary_index(glossary_path)
    buckets = build_buckets(records, glossary_index)
    candidates = write_candidate_tsv(REPORT_DIR / "lerch-glossary-text-form-comparison.tsv", buckets)
    write_review_data_js(REVIEW_DIR / "candidates-data.js", candidates)
    write_report(
        REPORT_DIR / "lerch-glossary-text-form-comparison.md",
        glossary_path,
        glossary_rows,
        records,
        buckets,
        candidates,
    )
    print(f"Scanned {len(records)} token records and {len(glossary_rows)} glossary rows.")
    print(f"Wrote {REPORT_DIR / 'lerch-glossary-text-form-comparison.md'}")
    print(f"Wrote {REPORT_DIR / 'lerch-glossary-text-form-comparison.tsv'}")
    print(f"Wrote {REVIEW_DIR / 'candidates-data.js'}")


if __name__ == "__main__":
    main()
