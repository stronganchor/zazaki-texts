# Lerch Glossary Publication Handoff

Generated: 2026-05-19

## Current Working Glossary

The richest current working glossary is outside this repository:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lltools_import\lltools_dictionary_lerch_glossary_full.tsv
```

This file has 600 rows with LL Tools-oriented fields: entry ids, display/search forms, parent links, entry type, Turkish/English/German definitions, source metadata, page/row references, raw Lerch headword, dialect labels, review status, and permission status.

It is not publishable as a full public glossary yet. Current review-state snapshot from the local working files:

- 468 rows are still marked `ocr_extracted`.
- 16 rows are marked `qa_reviewed`.
- 124 rows have parent links.
- 476 rows remain unparented.
- German source glosses are present for almost all rows, while English and Turkish glosses are only partly filled.

The safer immediate seed file is:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lltools_import\lltools_dictionary_lerch_glossary_reviewed_subset.tsv
```

That reviewed subset currently has 16 manually QA-reviewed rows with Turkish, English, and German definitions.

## Source And QA Files

Primary glossary extraction files:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch glossary german.pdf
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\Lerch Glossary - Full German Text.txt
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_zazaki_glossary_extraction.tsv
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_zazaki_glossary_extraction.txt
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_zazaki_glossary_summary.md
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_zazaki_glossary_review.md
```

QA and reviewed-subset files:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_zazaki_glossary_qa.tsv
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_zazaki_glossary_reviewed_subset_dezd_style.tsv
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_zazaki_glossary_russian_qa.md
```

Context and matching evidence:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_glossary_full_headword_match_report.tsv
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_glossary_full_headword_match_summary.md
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_glossary_text_contexts.tsv
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_glossary_text_contexts_unmatched.tsv
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_glossary_text_context_summary.md
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_glossary_remaining_witness_review.tsv
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_glossary_remaining_witness_review.md
```

Repository-side text index:

```text
C:\Users\messy\OneDrive\Documents\GitHub\zazaki-texts\reports\lerch-word-index.md
C:\Users\messy\OneDrive\Documents\GitHub\zazaki-texts\reports\lerch-word-index.tsv
C:\Users\messy\OneDrive\Documents\GitHub\zazaki-texts\reports\lerch-glossary-review-batch-01.md
C:\Users\messy\OneDrive\Documents\GitHub\zazaki-texts\reports\lerch-glossary-review-batch-01.tsv
C:\Users\messy\OneDrive\Documents\GitHub\zazaki-texts\reviews\lerch-glossary-review-batch-01\index.html
```

The repository index groups every token in the processed Lerch texts by the
current interlinear lemma/form key, preserves the attested Lerch and Zazaki
variants, attaches example locations, and marks whether each form matches the
current local glossary. It is safer for glossary-review triage than the older
surface-form gap report because it compares lemma keys first and avoids treating
short suffix fragments as whole-word glossary matches.

`lerch-glossary-review-batch-01` is the first high-value review batch generated
from that index. It contains 90 text-attested rows: likely add/merge candidates,
grammar/function items that should not become simple headwords, and lower-priority
review rows. The HTML review UI autosaves browser-local decisions and can export
review JSON.

## Publication Issues

The files appear to be valid UTF-8. The remaining problems are mostly OCR, review-state, and editorial-policy issues:

- Some extracted rows still contain collapsed or spilled adjacent entries.
- Old Lerch diacritics and apostrophes need one consistent public normalization policy.
- Short/common forms are ambiguous and should not be blindly merged.
- Many forms are attested in the texts but still need lemma-level grouping.
- Source/license metadata fields need to be filled before a full public import.
- The full 600-row import should not be published until rows are promoted from `ocr_extracted` in review batches.

## Recommended Next Step

Use `lltools_dictionary_lerch_glossary_full.tsv` as the working master, but publish from a reviewed candidate table. The practical next batch is:

1. Freeze the display/search/normalized-form column policy.
2. Fill source/license metadata consistently.
3. Use the text-context files to promote high-confidence entries from `ocr_extracted` to reviewed.
4. Compare the high-frequency word-form report in this repository against the full glossary to add missing text-attested forms with German, English, and Turkish glosses.
5. Publish either the 16-row reviewed seed or a larger reviewed batch, not the raw full extraction.
