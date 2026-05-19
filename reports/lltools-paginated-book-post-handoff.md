# LL Tools Handoff: Paginated Multilingual Source-Book Text Posts

## Goal

Add a lightweight LL Tools content type for publishing long source-book excerpts, such as the Zaza-related portions of Peter Lerch's book, as normal items in a corpus-text collection grid.

This should be separate from the current interlinear corpus-text view. It is for a text-only book/article style post with multilingual text buttons and page/section navigation.

## User Experience

- The post appears in `[ll_corpus_text_grid collection="lerch"]` alongside the existing Lerch text posts.
- Opening it shows a simple reading interface, not an interlinear interface.
- The title and intro/summary appear at the top.
- A language switcher offers `Türkçe`, `English`, and `Deutsch` using the same button style as the translation buttons on corpus-text posts.
- The selected language should default from the current LL Tools/site language. If the site language is Turkish, choose `tr`; if English, choose `en`; if German, choose `de`; otherwise fall back to the document default.
- The user's manual language choice should persist in the URL or local state the same way corpus-text translation selection does.
- The body is paginated or sectioned with clear previous/next controls, page numbers/section labels, and deep-linkable anchors.
- A print button should print the title, intro, currently selected language, and sources.
- The Sources section should support scholarly citations and links, as the corpus-text sources tab already does.

## Proposed Payload Shape

Extend `ll_tools_text_document.v1` or add a compatible `kind`, for example:

```json
{
  "schema": "ll_tools_text_document.v1",
  "kind": "book_text",
  "lesson_id": "lerch-book-zazaki-sections",
  "title": "Peter Lerch'in Zazaca Bölümleri",
  "metadata": {
    "collection": "lerch",
    "collection_label": "Peter Lerch Metinleri",
    "excerpt": "Lerch'in Zazaca metinleri, sözlüğü ve ilgili açıklamalarından seçilmiş bölümlerin çok dilli yayını.",
    "default_language": "tr"
  },
  "translations": {
    "tr": { "label": "Türkçe" },
    "en": { "label": "English" },
    "de": { "label": "Deutsch" }
  },
  "book_sections": [
    {
      "id": "intro",
      "label": "Giriş",
      "source_page": "Book I, pp. ...",
      "texts": {
        "tr": "Türkçe metin...",
        "en": "English text...",
        "de": "Deutscher Text..."
      }
    }
  ],
  "witnesses": [
    {
      "label": "Russian original",
      "citation": "...",
      "url": "..."
    }
  ]
}
```

## Rendering Rules

- `kind=book_text` should not show the `Metin / Satır arası / Kaynaklar` tab set unless sources are rendered as a tab or collapsible section.
- It should not require `reading_units`, `source_lines`, interlinear tokens, witnesses per line, POS rows, morphology rows, or source scan line images.
- It should use `book_sections[]` as the primary body.
- Each section should render only the selected language's text.
- The selected language should be resolved by:
  1. explicit `ll_book_language` or equivalent query parameter,
  2. persisted user choice,
  3. LL Tools current locale/site language,
  4. payload `metadata.default_language`,
  5. first available language.
- Keep the post public like existing corpus-text posts; do not apply staff-only interlinear policy.

## Import Requirements

- The existing `/wp-json/ll-tools/v1/corpus-texts/import` route can accept this payload if `ll_tools_interlinear_payload_is_text_document()` treats `book_text` as a text-document kind.
- The importer should set the post kind/meta so the collection grid includes this item.
- The grid card should use `metadata.excerpt` and the title as it does for corpus texts.

## Tests

- PHPUnit: importing a `book_text` payload creates/updates an `ll_content_lesson`, marks it as a collection item, stores the payload, and renders without interlinear rows.
- PHPUnit: language resolution prefers URL parameter, then current locale, then default.
- Playwright: collection grid opens the book text, language buttons switch text without breaking pagination, and print mode includes sources.
- Regression: existing `corpus_text` posts with `reading_units` and `source_lines` still render unchanged.
