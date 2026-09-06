#!/usr/bin/env python3
"""Normalize Lerch reader rows without splitting inside sentences.

The interlinear view remains line-based against the scans. This script only
updates the reader-facing `reading_units` and the derived prose markdown files.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

from reviewed_lerch_reader_guard import guard_existing_reader_layout


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXTS_ROOT = REPO_ROOT / "texts" / "lerch"
SENTENCE_BOUNDARY_RE = re.compile(r"(?:[.!?]+)(?:[\"'”’»]+)?(?=\s|$)")
SENTENCE_COMPLETE_RE = re.compile(r"(?:[.!?]+)(?:[\"'”’»)\]]+)?$")
WORD_RE = re.compile(r"\S+")
SKIP_SLUGS = {"gespraech-mit-hassan"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def split_paragraphs(markdown: str) -> list[str]:
    return [part.strip() for part in re.split(r"\r?\n\s*\r?\n", markdown.strip()) if part.strip()]


def split_sentences(text: str) -> list[str]:
    text = " ".join((text or "").split())
    if not text:
        return []

    parts: list[str] = []
    start = 0
    for match in SENTENCE_BOUNDARY_RE.finditer(text):
        end = match.end()
        parts.append(text[start:end].strip())
        start = end

    rest = text[start:].strip()
    if rest:
        parts.append(rest)
    return [part for part in parts if part]


def sentence_complete(text: str) -> bool:
    return bool(SENTENCE_COMPLETE_RE.search((text or "").strip()))


def append_text(base: str, addition: str) -> str:
    return " ".join([part for part in [base.strip(), addition.strip()] if part]).strip()


def combine_line_ids(first, second):
    ids: list[str] = []
    for value in [first, second]:
        if isinstance(value, list):
            for item in value:
                item = str(item)
                if item not in ids:
                    ids.append(item)
    return ids or None


def merge_source_sections(sections: list[dict]) -> list[dict]:
    if not sections:
        return []

    merged = deepcopy(sections[0])
    for section in sections[1:]:
        merged["source"] = append_text(merged.get("source", ""), section.get("source", ""))
        combined_line_ids = combine_line_ids(
            merged.get("source_line_ids"),
            section.get("source_line_ids"),
        )
        if combined_line_ids:
            merged["source_line_ids"] = combined_line_ids
        else:
            merged.pop("source_line_ids", None)
        if section.get("source_note"):
            merged["source_note"] = append_text(
                str(merged.get("source_note") or ""),
                str(section.get("source_note") or ""),
            )
    return [merged]


def source_sections_from_unit(unit: dict) -> list[dict]:
    source = str(unit.get("source") or "").strip()
    if source == "":
        return []

    sections: list[dict] = []
    for piece in split_sentences(source) or [source]:
        section = {
            "source": piece,
            "source_line_ids": deepcopy(unit.get("source_line_ids")),
        }
        if unit.get("source_note"):
            section["source_note"] = unit.get("source_note")
        sections.append(section)
    return sections


def raw_units_from_unit(unit: dict, old_index: int) -> list[dict]:
    sections = source_sections_from_unit(unit)
    if not sections:
        return []

    translations = {
        lang: str(value).strip()
        for lang, value in (unit.get("translations") or {}).items()
        if isinstance(value, str) and value.strip()
    }

    if len(sections) > 1:
        # Only split translations when they have the same sentence count as the
        # source. Otherwise keep the source section together so the reader view
        # does not create rows whose translations belong to a different span.
        mismatched_translation = any(
            len(split_sentences(value)) != len(sections)
            for value in translations.values()
        )
        if mismatched_translation:
            sections = merge_source_sections(sections)

    translation_chunks: dict[str, list[str]] = {}
    for lang, value in translations.items():
        translation_chunks[lang] = [value] if len(sections) == 1 else split_sentences(value)

    base_id = str(unit.get("id") or f"u{old_index:03d}")
    rows: list[dict] = []
    for section_index, section in enumerate(sections, start=1):
        unit_id = base_id if len(sections) == 1 else f"{base_id}_{section_index:02d}"
        row = {
            "id": unit_id,
            "source": section["source"],
            "translations": {
                lang: chunks[section_index - 1]
                for lang, chunks in translation_chunks.items()
                if section_index - 1 < len(chunks) and chunks[section_index - 1] != ""
            },
        }
        if section.get("source_line_ids"):
            row["source_line_ids"] = section["source_line_ids"]
        if section.get("source_note"):
            row["source_note"] = section["source_note"]
        rows.append(row)
    return rows


def merge_reader_units(units: list[dict]) -> list[dict]:
    merged: list[dict] = []
    pending: dict | None = None

    def flush_pending() -> None:
        nonlocal pending
        if pending is not None:
            merged.append(pending)
            pending = None

    for unit in units:
        current = deepcopy(unit)
        if pending is None:
            pending = current
        else:
            pending["source"] = append_text(str(pending.get("source") or ""), str(current.get("source") or ""))
            combined_line_ids = combine_line_ids(
                pending.get("source_line_ids"),
                current.get("source_line_ids"),
            )
            if combined_line_ids:
                pending["source_line_ids"] = combined_line_ids
            else:
                pending.pop("source_line_ids", None)
            if current.get("source_note"):
                pending["source_note"] = append_text(
                    str(pending.get("source_note") or ""),
                    str(current.get("source_note") or ""),
                )
            pending_translations = pending.setdefault("translations", {})
            for lang, text in (current.get("translations") or {}).items():
                if isinstance(text, str) and text.strip():
                    pending_translations[lang] = append_text(str(pending_translations.get(lang) or ""), text)

        if pending is not None and sentence_complete(str(pending.get("source") or "")):
            flush_pending()

    flush_pending()
    return merged


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
    if guard_existing_reader_layout(payload):
        return text_dir.name, len(units), len(units)

    title_unit = units[0] if is_title_unit(units[0]) else None
    body_units = units[1:] if title_unit is not None else units

    raw_body_units: list[dict] = []
    for old_index, old_unit in enumerate(body_units, start=1):
        raw_body_units.extend(raw_units_from_unit(old_unit, old_index))

    body_units = merge_reader_units(raw_body_units)
    new_units = ([title_unit] if title_unit is not None else []) + body_units

    payload["reading_units"] = new_units
    payload.setdefault("summary", {})["reading_units"] = len(new_units)
    write_json(payload_path, payload)

    z_title = document_title(text_dir / "text.zazaki.md", str(payload.get("title") or text_dir.name))
    rewrite_markdown(text_dir / "text.zazaki.md", z_title, [str(unit.get("source") or "") for unit in body_units])

    translations_by_lang: dict[str, list[str]] = {}
    for unit in body_units:
        for lang, text in (unit.get("translations") or {}).items():
            if isinstance(text, str) and text.strip():
                translations_by_lang.setdefault(lang, []).append(text)

    for lang, chunks in translations_by_lang.items():
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
