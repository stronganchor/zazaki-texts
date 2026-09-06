"""Portable regression checks; no source bundles, services, or live writes needed."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import normalize_lerch_reader_units as normalizer
import reviewed_lerch_reader_guard as guard
import update_reviewed_lerch_texts as updater


class ReviewedReaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.lesson = 'lerch-degirmenci-ve-tilki'
        self.folder = self.root / 'degirmenci-ve-tilki'
        self.folder.mkdir()
        self.doc = {
            'schema': 'll_tools_text_document.v1', 'lesson_id': self.lesson,
            'source_lines': [{'id': 's1', 'zazaki': 'Exact source.'}],
            'reading_units': [{'id': 'u1', 'source': 'Exact source.', 'source_line_ids': ['s1'],
                               'translations': {'de': 'Geprüfte Lesefassung.', 'en': 'Preserved.'}}],
            'metadata': {'publication': {'editorial_note_de': 'Uncertain reading remains marked.'}},
        }
        self.path = self.folder / 'reviewed-reader-translations.json'
        self.manifest = guard.make_review_manifest(self.doc, {'date': '2026-09-06'})
        self.save_manifest()

    def save_manifest(self):
        self.path.write_text(json.dumps(self.manifest), encoding='utf-8')

    def test_restore_reviewed_segmentation_translations_and_notes(self):
        regenerated = deepcopy(self.doc)
        regenerated['reading_units'] = [{'id': 'merged', 'source': 'bad guess'}]
        regenerated.pop('metadata')
        self.assertTrue(guard.apply_reviewed_reader_units(regenerated, self.root))
        self.assertEqual(regenerated['reading_units'], self.doc['reading_units'])
        self.assertEqual(regenerated['metadata'], self.doc['metadata'])
        self.assertEqual(regenerated['summary']['reading_units'], 1)
        self.assertIn('de', regenerated['translations'])

    def test_source_change_refused_before_any_mutation(self):
        changed = deepcopy(self.doc)
        changed['source_lines'][0]['zazaki'] += ' Changed.'
        before = deepcopy(changed)
        with self.assertRaisesRegex(ValueError, 'source line id/Zazaki changed'):
            guard.apply_reviewed_reader_units(changed, self.root)
        self.assertEqual(changed, before)

    def test_missing_required_manifest_refused(self):
        self.path.unlink()
        with self.assertRaisesRegex(ValueError, 'required reviewed-reader'):
            guard.apply_reviewed_reader_units(self.doc, self.root)

    def test_duplicate_reviewed_unit_ids_refused(self):
        self.manifest['reading_units'].append(deepcopy(self.manifest['reading_units'][0]))
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'duplicate or missing'):
            guard.apply_reviewed_reader_units(self.doc, self.root)

    def test_invalid_source_reference_refused(self):
        self.manifest['reading_units'][0]['source_line_ids'] = ['unknown']
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'unknown source line'):
            guard.apply_reviewed_reader_units(self.doc, self.root)

    def test_invalid_editorial_note_refused_before_mutation(self):
        self.manifest['editorial_notes']['unrelated'] = 'Do not copy arbitrary metadata.'
        self.save_manifest()
        before = deepcopy(self.doc)
        with self.assertRaisesRegex(ValueError, 'invalid reviewed editorial notes'):
            guard.apply_reviewed_reader_units(self.doc, self.root)
        self.assertEqual(self.doc, before)

    def test_unreviewed_lesson_unchanged(self):
        self.doc['lesson_id'] = 'lerch-unprotected-story'
        before = deepcopy(self.doc)
        self.assertFalse(guard.apply_reviewed_reader_units(self.doc, self.root))
        self.assertEqual(self.doc, before)

    def test_changed_reader_id_or_source_refused(self):
        for field in ('id', 'source'):
            changed = deepcopy(self.doc)
            changed['reading_units'][0][field] += ' changed'
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'reviewed unit id/source changed'):
                guard.guard_existing_reader_layout(changed, self.root)

    def test_normalizer_leaves_reviewed_files_byte_identical(self):
        payload_path = self.folder / 'text-document.json'
        payload_path.write_text(json.dumps(self.doc), encoding='utf-8')
        markdown_path = self.folder / 'translation.de.md'
        markdown_path.write_text('Keep exact reviewed paragraph layout.\n', encoding='utf-8')
        before = {p: p.read_bytes() for p in (payload_path, markdown_path)}
        with patch.object(normalizer, 'guard_existing_reader_layout',
                          side_effect=lambda doc: guard.guard_existing_reader_layout(doc, self.root)):
            self.assertEqual(normalizer.normalize_document(self.folder), (self.folder.name, 1, 1))
        self.assertEqual({p: p.read_bytes() for p in before}, before)

    def test_writer_refuses_changed_source_before_creating_output(self):
        self.doc['source_lines'][0]['zazaki'] = 'Changed source.'
        target = self.root / 'output' / 'text-document.json'
        with patch.object(updater, 'REPO_ROOT', self.root), patch.object(
            updater, 'apply_reviewed_reader_units',
            side_effect=lambda doc: guard.apply_reviewed_reader_units(doc, self.root)
        ), self.assertRaises(ValueError):
            updater.write_json(target, self.doc)
        self.assertFalse(target.exists())
        self.assertFalse(target.parent.exists())


if __name__ == '__main__':
    unittest.main()
