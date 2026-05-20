#!/usr/bin/env python3
"""Split Lerch reader text into smaller source/translation-aligned units.

The interlinear view stays line-based against the scans. This script only
normalizes the reader-facing `reading_units` used for the two-column text view.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXTS_ROOT = REPO_ROOT / "texts" / "lerch"
SOURCE_BOUNDARY_RE = re.compile(r"(?:[.!?]+|;)(?:[\"'”’»]+)?(?=\s|$)")
TRANSLATION_BOUNDARY_RE = re.compile(r"(?:[.!?]+)(?:[\"'”’»]+)?(?=\s|$)")
WORD_RE = re.compile(r"\S+")
TINY_WORD_LIMIT = 3
LONG_WORD_LIMIT = 45
SKIP_SLUGS = {"gespraech-mit-hassan"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def split_paragraphs(markdown: str) -> list[str]:
    return [part.strip() for part in re.split(r"\r?\n\s*\r?\n", markdown.strip()) if part.strip()]


def split_sentences(text: str, *, split_semicolons: bool = False) -> list[str]:
    text = " ".join((text or "").split())
    if not text:
        return []

    parts: list[str] = []
    start = 0
    boundary_re = SOURCE_BOUNDARY_RE if split_semicolons else TRANSLATION_BOUNDARY_RE
    for match in boundary_re.finditer(text):
        end = match.end()
        parts.append(text[start:end].strip())
        start = end

    rest = text[start:].strip()
    if rest:
        parts.append(rest)
    return [part for part in parts if part]


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text or ""))


def split_long_piece(text: str) -> list[str]:
    if word_count(text) <= LONG_WORD_LIMIT:
        return [text]

    parts = [part.strip() for part in re.split(r"(?<=,)\s+", text) if part.strip()]
    if len(parts) <= 1:
        return [text]

    chunks: list[str] = []
    current = ""
    for part in parts:
        candidate = append_text(current, part)
        if current and word_count(candidate) > LONG_WORD_LIMIT:
            chunks.append(current)
            current = part
        else:
            current = candidate
    if current:
        chunks.append(current)

    if len(chunks) == 1:
        return [text]

    return chunks


def append_text(base: str, addition: str) -> str:
    return " ".join([part for part in [base.strip(), addition.strip()] if part]).strip()


def partition_translation(sentences: list[str], source_sections: list[dict]) -> list[str]:
    if not source_sections:
        return []
    if not sentences:
        return ["" for _ in source_sections]
    if len(sentences) == len(source_sections):
        return sentences
    if len(source_sections) == 2 and len(sentences) == 3:
        return [sentences[0], " ".join(sentences[1:]).strip()]

    source_weights = [max(1, word_count(section["source"])) for section in source_sections]
    total_source = sum(source_weights)
    total_sentences = len(sentences)
    chunks: list[str] = []
    cursor = 0
    cumulative_source = 0

    for index, weight in enumerate(source_weights):
        cumulative_source += weight
        remaining_sections = len(source_weights) - index - 1
        if remaining_sections == 0:
            target_end = total_sentences
        else:
            target_end = round((cumulative_source / total_source) * total_sentences)
            target_end = max(cursor + 1, target_end)
            target_end = min(target_end, total_sentences - remaining_sections)

        chunks.append(" ".join(sentences[cursor:target_end]).strip())
        cursor = target_end

    return chunks


def source_sections_from_unit(unit: dict) -> list[dict]:
    sections: list[dict] = []
    source = str(unit.get("source") or "").strip()
    if source == "":
        return []

    sentence_pieces = split_sentences(source, split_semicolons=True) or [source]
    pieces = [piece for sentence in sentence_pieces for piece in split_long_piece(sentence)]
    for piece in pieces:
        section = {
            "source": piece,
            "source_line_ids": deepcopy(unit.get("source_line_ids")),
        }
        if unit.get("source_note"):
            section["source_note"] = unit.get("source_note")
        sections.append(section)

    merged: list[dict] = []
    pending: dict | None = None
    for section in sections:
        if word_count(section["source"]) <= TINY_WORD_LIMIT:
            if pending is None:
                pending = deepcopy(section)
                continue
            pending["source"] = append_text(pending["source"], section["source"])
            pending["source_line_ids"] = combine_line_ids(
                pending.get("source_line_ids"),
                section.get("source_line_ids"),
            )
            continue

        if pending is not None:
            section = deepcopy(section)
            section["source"] = append_text(pending["source"], section["source"])
            section["source_line_ids"] = combine_line_ids(
                pending.get("source_line_ids"),
                section.get("source_line_ids"),
            )
            pending = None

        merged.append(section)

    if pending is not None:
        if merged:
            merged[-1]["source"] = append_text(merged[-1]["source"], pending["source"])
            merged[-1]["source_line_ids"] = combine_line_ids(
                merged[-1].get("source_line_ids"),
                pending.get("source_line_ids"),
            )
        else:
            merged.append(pending)

    return merged


def combine_line_ids(first, second):
    ids: list[str] = []
    for value in [first, second]:
        if isinstance(value, list):
            ids.extend(str(item) for item in value if str(item) not in ids)
    return ids or None


def merge_source_sections(sections: list[dict]) -> list[dict]:
    if not sections:
        return []

    merged = deepcopy(sections[0])
    for section in sections[1:]:
        merged["source"] = append_text(merged.get("source", ""), section.get("source", ""))
        merged["source_line_ids"] = combine_line_ids(
            merged.get("source_line_ids"),
            section.get("source_line_ids"),
        )
        if not merged.get("source_note") and section.get("source_note"):
            merged["source_note"] = section.get("source_note")
    return [merged]


def keep_unit_unsplit_for_translation_alignment(unit: dict, sections: list[dict]) -> bool:
    if len(sections) <= 1:
        return False
    if word_count(" ".join(section["source"] for section in sections)) > LONG_WORD_LIMIT:
        return False

    translations = unit.get("translations") or {}
    for value in translations.values():
        if isinstance(value, str) and value.strip() and len(split_sentences(value)) <= 1:
            return True
    return False


def is_title_unit(unit: dict) -> bool:
    return str(unit.get("id") or "") == "title"


def document_title(path: Path, fallback: str) -> str:
    if not path.exists():
        return fallback
    paragraphs = split_paragraphs(path.read_text(encoding="utf-8"))
    return paragraphs[0] if paragraphs else fallback


def rewrite_markdown(path: Path, title: str, paragraphs: list[str]) -> None:
    body = "\n\n".join([title, *[paragraph for paragraph in paragraphs if paragraph.strip()]])
    path.write_text(body.strip() + "\n", encoding="utf-8")


def normalize_document(text_dir: Path) -> tuple[str, int, int]:
    payload_path = text_dir / "text-document.json"
    if not payload_path.exists():
        return text_dir.name, 0, 0

    payload = read_json(payload_path)
    units = payload.get("reading_units")
    if not isinstance(units, list) or not units:
        return text_dir.name, 0, 0

    title_unit = units[0] if is_title_unit(units[0]) else None
    body_units = units[1:] if title_unit is not None else units
    new_units: list[dict] = []
    if title_unit is not None:
        new_units.append(title_unit)

    all_source_sections: list[dict] = []
    all_translation_sections: dict[str, list[str]] = {}
    for old_index, old_unit in enumerate(body_units, start=1):
        source_sections = source_sections_from_unit(old_unit)
        if not source_sections:
            continue
        if keep_unit_unsplit_for_translation_alignment(old_unit, source_sections):
            source_sections = merge_source_sections(source_sections)

        translations = old_unit.get("translations") or {}
        translation_chunks = {
            lang: partition_translation(split_sentences(str(value)), source_sections)
            for lang, value in translations.items()
            if isinstance(value, str) and value.strip()
        }
        base_id = str(old_unit.get("id") or f"u{old_index:03d}")

        for section_index, section in enumerate(source_sections, start=1):
            unit_id = base_id if len(source_sections) == 1 else f"{base_id}_{section_index:02d}"
            unit = {
                "id": unit_id,
                "source": section["source"],
                "translations": {
                    lang: chunks[section_index - 1]
                    for lang, chunks in translation_chunks.items()
                    if section_index - 1 < len(chunks) and chunks[section_index - 1] != ""
                },
            }
            if section.get("source_line_ids"):
                unit["source_line_ids"] = section["source_line_ids"]
            if section.get("source_note"):
                unit["source_note"] = section["source_note"]
            new_units.append(unit)
            all_source_sections.append(section)
            for lang, text in unit["translations"].items():
                all_translation_sections.setdefault(lang, []).append(text)

    payload["reading_units"] = new_units
    payload.setdefault("summary", {})["reading_units"] = len(new_units)
    write_json(payload_path, payload)

    z_title = document_title(text_dir / "text.zazaki.md", str(payload.get("title") or text_dir.name))
    rewrite_markdown(text_dir / "text.zazaki.md", z_title, [section["source"] for section in all_source_sections])
    for lang, chunks in all_translation_sections.items():
        translation_path = text_dir / f"translation.{lang}.md"
        if translation_path.exists():
            title = document_title(translation_path, z_title)
            rewrite_markdown(translation_path, title, chunks)

    return text_dir.name, len(units), len(new_units)


def main() -> None:
    rows = []
    for text_dir in sorted(TEXTS_ROOT.iterdir()):
        if text_dir.is_dir() and text_dir.name not in SKIP_SLUGS:
            rows.append(normalize_document(text_dir))

    for slug, before, after in rows:
        if before or after:
            print(f"{slug}: {before} -> {after} reader units")


if __name__ == "__main__":
    main()
