# Lerch Glossary Publication Readiness

Generated: 2026-05-21

## Current State

- Working extraction: `C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_zazaki_glossary_extraction.tsv`
- Working LL Tools-style import: `C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lltools_import\lltools_dictionary_lerch_glossary_full.tsv`
- Current row count: 600 glossary rows.
- Current German gloss coverage: 598 rows.
- Current English gloss coverage: 95 rows.
- Current Turkish gloss coverage: 131 rows.
- Current modern-Zazaki conversion review table: `reports/lerch-glossary-modern-conversion.tsv`

## Review Status

- `qa_reviewed`: 16 rows.
- `headword_parented`: 116 rows.
- `ocr_extracted`: 468 rows.

## Readiness Assessment

- The glossary is useful as an internal research aid now.
- It is not yet ready to publish as a final public glossary.
- The main blocker is not row count; it is source verification. Most entries still come from OCR-level extraction and have not been checked against the German/Russian scans.
- The German gloss OCR is broad enough for internal matching, but not clean enough to treat all 598 German gloss rows as publication-grade.
- The English and Turkish glosses are partial. They mostly come from reviewed overrides or matches against modern dictionaries, not from a complete translation pass over every German gloss.
- A Lerch-to-modern-Zazaki conversion now exists as a full review table, but most converted forms inherit the OCR uncertainty of their source entries.

## Recommended Publication Path

1. Publish no full glossary yet.
2. Start with a pilot subset made from the `qa_reviewed` rows plus any newly reviewed high-value entries from the texts.
3. Add scan-backed review fields before public release:
   - reviewed Lerch headword
   - modern Zazaki form
   - German gloss
   - English gloss
   - Turkish gloss
   - source page
   - review status
   - notes on uncertainty
4. Use `headword_parented` rows as the next review queue, because they already have a plausible modern dictionary match.
5. Treat `ocr_extracted` rows as unreviewed until the headword and gloss are checked against the scan.

## Open Work

- Build or refine a glossary review UI with scan crop, OCR row, editable Lerch headword, modern-Zazaki conversion, German gloss, English gloss, Turkish gloss, and review status.
- Review all 600 headwords against the scan, prioritizing entries that occur in the processed Lerch texts.
- Complete English and Turkish translation of the German glosses.
- Decide whether public glossary entries should include all inflected forms as separate historical entries, or group them under normalized lemmas with Lerch's printed forms as variants.
- Add example citations from the processed texts where available.
