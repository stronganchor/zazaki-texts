# Lerch Bacmeister Sentence Samples Status

Generated: 2026-05-19

## Scope

Read-only inspection of the local Bacmeister/example-sentence Lerch review bundle and source draft. No text folders, review bundles, scripts, or live-site files were edited.

Primary inspected paths:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\build_lerch_bacmeister_samples_review_bundle.py
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_bacmeister_samples_review_bundle\
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\translation_project\lerch\appendix_bacmeister_sentence_samples\
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\translation_project\sources\bacmeister_sentence_samples_rendered_pages\
```

## Source Identification

This is not one of Lerch's narrative texts. It is a sentence-sample appendix titled:

```text
Uebersetzung der "Sprachproben" Bacmeisters in die kurdischen Mundarten Kurmandi und Zaza
```

The local README describes it as Lerch's section containing 44 Bacmeister sample sentences printed in parallel Kurmanji and Zaza, followed by German glosses. The draft file describes the working text as a transcription and translation draft from Lerch, Abt. I, printed pp. 1-4 of the text section, preserving Lerch's historical phonetic transcription rather than normalizing to modern Zazaki.

The review bundle metadata says the scan witnesses are:

- Russian Book II viewer pages 55-58 / printed pp. 41-44.
- German PDF rendered pages 45-48.
- German high-resolution diacritic-pass crops under `translation_project\sources\bacmeister_sentence_samples_rendered_pages\hires_diacritic_pass\`.

The bundle README says the Russian original crops are shown first and the German reprint crops are secondary witnesses. That matches the established Lerch witness hierarchy used elsewhere in this workspace: Russian original first, German reprint second, later/secondary controls only when needed.

## Counts

The source draft table has 44 numbered sample rows.

The current review bundle JSON has 8 review cards:

| Review card | Draft row(s) |
| --- | --- |
| `row04_tide` | 4 |
| `row10_lade_tide` | 10 |
| `row14_howenu` | 14 |
| `row23_pand` | 23 |
| `row24_tizik` | 24 |
| `row35_boete` | 35 |
| `row37_39_below_marks` | 37 and 39 |
| `row43_44_zaza_suffix` | 43 and 44 |

So the publishable unit would be a 44-row example-sentence appendix, with 8 currently highlighted review cards covering 10 of those rows.

## Review Autosave Status

`review_autosave.json` exists:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_bacmeister_samples_review_bundle\review_autosave.json
```

It appears genuinely edited, not just an empty tool placeholder:

- It contains saved Zaza text, notes, and statuses.
- Several notes differ from the generated review-card notes.
- All saved statuses are still `needs-review`.

Important caveat: the autosave is older than the current rebuilt bundle. The autosave payload has 7 items, while the current review JSON has 8 items. The current HTML restore logic compares save timestamps against `DATA.generated_at`; because the disk autosave predates the rebuilt source data, the browser should ignore it and display the rebuilt source text unless there is a newer browser-local save.

There is also a pre-recrop backup:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_bacmeister_samples_review_bundle\review_autosave.before_recrop_20260513_120039.json
```

This supports treating the autosave as prior human/tool review history, but not as final accepted state.

## Current Review UI

Bundle path:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_bacmeister_samples_review_bundle\
```

HTML review page:

```text
C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lerch_bacmeister_samples_review_bundle\lerch_bacmeister_samples_review.html
```

Disk-autosave server command, from the bundle folder:

```powershell
python serve_lerch_bacmeister_samples_review.py --port 8772
```

Then open:

```text
http://127.0.0.1:8772/lerch_bacmeister_samples_review.html
```

The included `open_lerch_bacmeister_samples_review.cmd` opens the same URL.

Regeneration command from the `Language\Z` folder:

```powershell
python Dictionaries/Lerch/build_lerch_bacmeister_samples_review_bundle.py
```

## What Is Ready For Autonomous Work

Safe autonomous next steps, if assigned later:

- Prepare a publication draft from the 44-row markdown table without changing source text.
- Preserve the historical Lerch transcription in the main display.
- Keep Kurmanji, Zaza, German, English, and Turkish columns, because the local draft already has all five.
- Add concise source/provenance notes explaining that this is Bacmeister sentence-sample data as printed by Lerch, not a narrative text.
- Add an editorial note that the Russian original is the primary witness and the German reprint is secondary.
- Keep the 8 review-card rows visibly flagged until manually accepted.
- Build a non-live preview artifact in `zazaki-texts` once the publication shape is approved.

## What Needs User Review

Do not publish as final without user review of the remaining glyph/form queue.

The unresolved review surface is small but material: the bundle exists specifically to confirm marks such as under-consonant marks, acute/macron distinctions, line-below versus ring/dot-below, gamma/t-with-crescent-below handling, and joined line-break forms. The current autosave does not mark any row as accepted, and the current 8-card bundle includes one card (`row37_39_below_marks`) missing from the older disk autosave.

The user/editor should specifically review and either accept or correct:

- Row 4: `Tide`/`estu` diacritic details.
- Row 10: `Lade tide` acute/macron and consonant marks.
- Row 14: `verie`, `damu`, `hirune`, `howen'u`, and line-break join.
- Row 23: below mark in `Di`, `esti`, and `pand`.
- Row 24: initial gamma versus normalized mark handling and below-marked vowel.
- Row 35: `En'oe`, `bo'ete`, and `qilma`.
- Rows 37 and 39: below-mark class in `qile`, `komur`, and `qida`.
- Rows 43 and 44: `zazade`/`zazada`, `zani`, and below-marked `Sima`.

## Publication Recommendation

Recommended shape: examples page / appendix, not a standalone Lerch text.

Reasoning:

- It is a coherent 44-row unit, but it is sentence-sample data rather than a story, dialogue, or prose text.
- It has strong value as a Lerch Zaza examples appendix and as source-backed example material for future glossary entries.
- Publishing it as a standalone corpus text would make it look equivalent to narrative texts like the existing Lerch story folders, which would be misleading.
- Folding it directly into the glossary now would bury the parallel-sentence structure and the Kurmanji/Zaza comparison.

Practical publication shape:

- Title it as a Lerch Bacmeister sentence-sample appendix.
- Present the 44 examples in a table-like page, with Zaza as the main target column and Kurmanji/German/English/Turkish available beside it.
- Keep a source note and witness note near the top.
- Link or later reuse individual rows as glossary examples after the glyph review is accepted.

Current publication status: hold for final publication, but ready for a reviewed preview/examples-page draft. The blocker is not volume or structure; it is the remaining 8-card glyph/form review queue.
