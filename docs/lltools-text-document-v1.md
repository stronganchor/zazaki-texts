# LL Tools Text Document Payload

`text-document.json` files use `schema: "ll_tools_text_document.v1"` and are imported into LL Tools through the existing interlinear payload storage.

Core fields:

- `kind`: use `corpus_text`.
- `lesson_id`: stable text id used by LL Tools import/export.
- `title`: display title for the content lesson.
- `source_label`: label for the source-text column in reader view.
- `translations`: language metadata keyed by language code, for example `tr` and `en`.
- `reading_units`: public reader rows. Each row has `source` and `translations`.
- `source_lines`: staff linguist rows. Each row may have `display_rows`, `witnesses`, regular interlinear `tokens`, and `phrase_matches`.
- `witnesses`: document-level source notes.

`source_lines[].witnesses[].image_url` may be a relative path inside the text directory. The importer resolves relative paths, imports those images into WordPress media, and replaces them with attachment URLs in the site payload.

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
