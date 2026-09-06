# Reviewed Lerch reader inputs

Four texts have source-reviewed reading units in each text folder's
`reviewed-reader-translations.json`: Miller and Fox, Go'in, Three Brothers,
and Conversation with Hassan. These files are explicit build inputs. Their
review metadata distinguishes newly checked German from preserved English
and Turkish. Keeping a translation here does not independently certify it.

The manifests preserve reviewed reader IDs, source grouping, translations,
and explanatory editorial notes. The updater restores them only when the
ordered physical source-line IDs and Zazaki strings match exactly. A missing
required manifest or changed source fails before writing that document.
The generic normalizer leaves these reviewed layouts alone and rejects a
changed reader ID/source. This prevents sentence-count heuristics and old
translation drafts from overwriting the checked readings.

When the source or a reviewed translation changes, first verify the original
scan and reconcile the sentence alignment and witness differences. Update
the text document, matching translation Markdown, and manifest together;
record what was reviewed and the evidence in the manifest's `review` field.
Do not regenerate a manifest merely to suppress a source-mismatch error.
The historical source/OCR is not rewritten by this mechanism.

Run the portable regression tests from the repository root:

```powershell
python scripts/test_reviewed_lerch_reader_guard.py
```

The 2026-09-06 audit also rebuilt all four texts from the actual local review
bundles into a temporary directory: all 174 reading units and their three
translation lanes matched exactly, explanatory notes survived, and subsequent
normalization changed no output bytes. Asset copying was excluded from that
focused check. Evidence is in the Language/Z workspace under
`artifacts/research-curation-20260906/lerch/story_review/generator-validation.json`.
