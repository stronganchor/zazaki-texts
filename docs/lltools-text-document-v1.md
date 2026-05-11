# LL Tools Text Document Payload

`text-document.json` files use `schema: "ll_tools_text_document.v1"` and are imported into LL Tools through the existing interlinear payload storage.

Core fields:

- `kind`: use `corpus_text`.
- `lesson_id`: stable text id used by LL Tools import/export.
- `title`: display title for the content lesson.
- `source_label`: label for the source-text column in reader view.
- `translations`: language metadata keyed by language code, for example `tr`, `en`, and `de`.
- `reading_units`: public reader rows. Each row has `source` and `translations`.
- `source_lines`: public Interlinear rows for corpus-text posts. Each row may have `display_rows`, `witnesses`, regular interlinear `tokens`, and `phrase_matches`.
- `witnesses`: document-level source notes used by the public Sources tab.

Recommended `metadata` fields:

- `collection`: stable collection slug used by LL Tools grids, for example `lerch`.
- `collection_label`: human-readable collection name.
- `source_author`: collector/editor/source author name.
- `excerpt`: short summary used on corpus-text grid cards.

`source_lines[].witnesses[].image_url` may be a relative path inside the text directory. The importer resolves relative paths, imports those images into WordPress media, and replaces them with attachment URLs in the site payload.

Corpus texts are standalone in LL Tools by default. Use `[ll_corpus_text_grid collection="lerch"]` or `[ll_text_document_grid collection="lerch"]` on a WordPress page to render a public grid of imported texts from a collection.

Before live import, optimize source-line scan images and build a minimal import bundle:

```bash
node scripts/optimize_text_assets.js
node scripts/build_live_import_bundle.js
```

The optimizer rewrites image references in `text-document.json` to `.webp` and enforces a 300 KB ceiling for each referenced image. The bundle script copies only payload files and referenced WebP assets into `dist/lltools-lerch-texts-webp-import`, excluding older JPG/PNG working crops and QA images.

Use `hidden_rows` on a `source_lines[]` row to suppress specific interlinear rows. LL Tools also hides empty POS rows and lemma rows that only duplicate the visible word/morph form.

`tokens` follow the existing LL Tools interlinear token shape:

- `form`
- `lemma`
- `display_gloss`
- `pos`
- `morphemes[]`

`morphemes[]` can carry:

- `form`
- `normalized`
- `lemma`
- `gloss`
- `pos`
- `features`
- `confidence`
- `evidence`
- `notes`
