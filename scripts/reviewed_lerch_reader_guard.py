"""Preserve reviewed reader alignment while its underlying source stays unchanged.

The historical source/OCR remains untouched. Reviewed reader manifests are
explicit build inputs, not another sentence-alignment guess.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re

TEXTS_ROOT = Path(__file__).resolve().parents[1] / 'texts' / 'lerch'
SCHEMA = 'zazaki_texts.reviewed_reader_translations.v1'
PROTECTED_LESSONS = {
    'lerch-degirmenci-ve-tilki',
    'lerch-goin-puhu-kusunun-hikayesi',
    'lerch-uc-kardes-masali',
    'lerch-gespraech-mit-hassan',
}


def source_anchors(source_lines: list[dict]) -> list[dict]:
    anchors = [{'id': line.get('id'), 'zazaki': line.get('zazaki')} for line in source_lines]
    ids = [line['id'] for line in anchors]
    if any(not isinstance(item, str) or not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError('Reviewed reader source lines require unique nonempty ids')
    if any(not isinstance(line['zazaki'], str) for line in anchors):
        raise ValueError('Reviewed reader source lines require exact Zazaki strings')
    return anchors


def make_review_manifest(doc: dict, review: dict) -> dict:
    return {
        'schema': SCHEMA,
        'lesson_id': doc['lesson_id'],
        'review': deepcopy(review),
        'source_lines': source_anchors(doc['source_lines']),
        'reading_units': deepcopy(doc['reading_units']),
        'editorial_notes': {
            key: value for key, value in doc.get('metadata', {}).get('publication', {}).items()
            if key in {'editorial_note_de', 'editorial_note_en', 'editorial_note_tr'}
        },
    }


def _manifest_path(lesson_id: str, texts_root: Path) -> Path | None:
    if not lesson_id.startswith('lerch-'):
        return None
    slug = lesson_id.removeprefix('lerch-')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError(f'Invalid reviewed reader lesson id: {lesson_id!r}')
    return texts_root / slug / 'reviewed-reader-translations.json'


def _load_reviewed_manifest(lesson_id: str, source_lines: list[dict], texts_root: Path) -> dict | None:
    path = _manifest_path(lesson_id, texts_root)
    if path is None or not path.exists():
        if lesson_id in PROTECTED_LESSONS:
            raise ValueError(f'{lesson_id}: required reviewed-reader-translations.json is missing; refusing unreviewed rebuild')
        return None
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if manifest.get('schema') != SCHEMA or manifest.get('lesson_id') != lesson_id:
        raise ValueError(f'{lesson_id}: invalid reviewed reader manifest')
    if manifest.get('source_lines') != source_anchors(source_lines):
        raise ValueError(f'{lesson_id}: source line id/Zazaki changed; review and update the reader manifest before rebuilding')
    units = manifest.get('reading_units')
    if not isinstance(units, list) or not units:
        raise ValueError(f'{lesson_id}: empty or invalid reviewed reader units')
    if any(not isinstance(unit, dict) for unit in units):
        raise ValueError(f'{lesson_id}: invalid reviewed reader unit')
    ids = [unit.get('id') for unit in units]
    if any(not isinstance(item, str) or not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError(f'{lesson_id}: duplicate or missing reviewed unit id')
    source_ids = {line['id'] for line in manifest['source_lines']}
    for unit in units:
        if not isinstance(unit.get('source'), str) or not unit['source']:
            raise ValueError(f'{lesson_id}/{unit["id"]}: missing reviewed source')
        translations = unit.get('translations')
        if not isinstance(translations, dict) or any(not isinstance(v, str) for v in translations.values()):
            raise ValueError(f'{lesson_id}/{unit["id"]}: invalid reviewed translations')
        if any(item not in source_ids for item in unit.get('source_line_ids', [])):
            raise ValueError(f'{lesson_id}/{unit["id"]}: unknown source line reference')
    notes = manifest.get('editorial_notes', {})
    if not isinstance(notes, dict) or any(
        key not in {'editorial_note_de', 'editorial_note_en', 'editorial_note_tr'} or not isinstance(value, str)
        for key, value in notes.items()
    ):
        raise ValueError(f'{lesson_id}: invalid reviewed editorial notes')
    return manifest


def load_reviewed_reader_units(lesson_id: str, source_lines: list[dict], texts_root: Path = TEXTS_ROOT) -> list[dict] | None:
    manifest = _load_reviewed_manifest(lesson_id, source_lines, texts_root)
    return deepcopy(manifest['reading_units']) if manifest is not None else None


def apply_reviewed_reader_units(doc: dict, texts_root: Path = TEXTS_ROOT) -> bool:
    """Restore a reviewed layout after rebuilding from unchanged physical lines."""
    if doc.get('schema') != 'll_tools_text_document.v1' or 'source_lines' not in doc:
        return False
    manifest = _load_reviewed_manifest(doc.get('lesson_id', ''), doc['source_lines'], texts_root)
    if manifest is None:
        return False
    units = deepcopy(manifest['reading_units'])
    doc['reading_units'] = units
    doc.setdefault('summary', {})['reading_units'] = len(units)
    for unit in units:
        for lang in unit['translations']:
            doc.setdefault('translations', {}).setdefault(lang, {'label': {'de': 'German', 'en': 'English', 'tr': 'Turkish'}.get(lang, lang)})
    if manifest.get('editorial_notes'):
        doc.setdefault('metadata', {}).setdefault('publication', {}).update(deepcopy(manifest['editorial_notes']))
    return True


def guard_existing_reader_layout(doc: dict, texts_root: Path = TEXTS_ROOT) -> bool:
    """Stop generic normalization from changing a reviewed source/id alignment."""
    units = load_reviewed_reader_units(doc.get('lesson_id', ''), doc.get('source_lines', []), texts_root)
    if units is None:
        return False
    layout = lambda rows: [(row.get('id'), row.get('source')) for row in rows]
    if layout(doc.get('reading_units', [])) != layout(units):
        raise ValueError(f'{doc.get("lesson_id")}: reviewed unit id/source changed; refusing to normalize without review')
    return True
