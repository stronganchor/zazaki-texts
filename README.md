# Zazaki Texts

Source-of-truth repository for edited Zazaki texts, translations, interlinear data, and source-witness assets.

The first imported text is Peter Lerch's `Kawge Nyerib u Sivani` story. Each text directory is meant to be usable both as a Git-maintained archival/editing format and as an import source for LL Tools corpus-text content lessons.

## Layout

- `texts/<collection>/<slug>/metadata.json` - stable metadata for the text.
- `texts/<collection>/<slug>/text-document.json` - LL Tools text-document payload.
- `texts/<collection>/<slug>/text.zazaki.md` - readable Zazaki text.
- `texts/<collection>/<slug>/translation.en.md` - English free translation.
- `texts/<collection>/<slug>/translation.tr.md` - Turkish free translation.
- `texts/<collection>/<slug>/translation.de.md` - German free translation when an original German translation is available.
- `texts/<collection>/<slug>/morphemes.tsv` - morpheme-level working interlinear data.
- `texts/<collection>/<slug>/assets/` - source-witness images referenced by the payload.
- `scripts/import_lltools_corpus_text.php` - imports one `text-document.json` into a local LL Tools WordPress site.

## LL Tools Import

Example from the repo root:

```powershell
& "$env:APPDATA\Local\lightning-services\php-8.2.23+0\bin\win64\php.exe" `
  -c "$env:APPDATA\Local\run\oDN9bJpJi\conf\php\php.ini" `
  scripts\import_lltools_corpus_text.php `
  --wp-root="C:\Users\messy\Local Sites\starter-english-local\app\public" `
  --payload="texts\lerch\kauge-nyerib-u-sivani\text-document.json" `
  --wordset-slug="zazaki-historical-texts" `
  --wordset-name="Zazaki Historical Texts" `
  --post-slug="lerch-kauge-nyerib-u-sivani" `
  --status="publish"
```

The importer creates or updates the wordset, content lesson post, source-image attachments, and `_ll_tools_interlinear_payload` meta. Text-document payloads automatically mark the content lesson as `corpus_text` in LL Tools.
