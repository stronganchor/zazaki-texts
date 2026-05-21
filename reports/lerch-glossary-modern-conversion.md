# Lerch Glossary Modern Orthography Conversion

This report applies the current Lerch-to-Zazaki converter to the working local Lerch glossary headwords.
It is a review aid, not a publish-ready dictionary export, because most glossary rows remain OCR-level.

## Inputs

- Source glossary: `C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lltools_import\lltools_dictionary_lerch_glossary_full.tsv`
- Converter: `Dictionaries/Lerch/build_lerch_feud_interlinear_bundle.py::lerch_to_zazaki`
- TSV output: `reports\lerch-glossary-modern-conversion.tsv`

## Counts

- Total rows: 600
- Rows parented to a modern dictionary headword: 124
- Rows with German gloss: 598
- Rows with English gloss: 95
- Rows with Turkish gloss: 131

## Entry Review Status

- headword_parented: 116
- ocr_extracted: 468
- qa_reviewed: 16

## Conversion Confidence

- high: 16
- low: 468
- medium: 116

## Publication Readiness

- The conversion logic exists and now has a full review table.
- The conversion output should not be published as final until OCR-level rows are reviewed against the scans.
- Rows marked `qa_reviewed` are the safest starting subset for a public pilot glossary.
- Rows marked `headword_parented` are useful internally but still need headword/diacritic verification.
- Rows marked `ocr_extracted` should be treated as unreviewed.
