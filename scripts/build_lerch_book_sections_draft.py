#!/usr/bin/env python3
"""Package Lerch Zaza-related prose translations as a draft book_text payload."""

from __future__ import annotations

import json
import html
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "drafts" / "lerch" / "book-zaza-sections"
TEXT_DIR = REPO_ROOT / "texts" / "lerch" / "lerch-book-zazaki-sections"
REPORT = REPO_ROOT / "reports" / "lerch-book-sections-draft-status.md"

LOCAL_PROJECT = Path(r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\translation_project\lerch")
EN_FULL = LOCAL_PROJECT / "full_translation_en" / "lerch_relevant_pieces_en_full_translation_draft.md"
TR_FULL = LOCAL_PROJECT / "full_translation_tr" / "lerch_relevant_pieces_tr_full_translation_draft.md"


@dataclass(frozen=True)
class SectionSpec:
    section_id: str
    label_tr: str
    label_en: str
    label_de: str
    en_heading: str
    tr_heading: str
    de_file: Path
    source_note: str


SECTIONS = [
    SectionSpec(
        "dorn-report",
        "B. von Dorn'un Roslavl Raporu",
        "B. von Dorn's Roslavl Report",
        "B. von Dorns Bericht über Roslawl",
        "B. von Dorn's Report on Lerch's Journey to Roslavl",
        "B. von Dorn'un Lerch'in Roslavl Seyahati Hakkındaki Raporu",
        LOCAL_PROJECT / "post1_dorn_report" / "post1_de_readable_draft.md",
        "Dorn's introductory report on Lerch's Roslavl materials and the Zaza-related prose/poetry inventory.",
    ),
    SectionSpec(
        "method-hassan",
        "Lerch'in Yöntemi ve Hassan",
        "Lerch's Method and Hassan",
        "Lerchs Methode und Hassan",
        "Lerch's Method and His Zaza Source Hassan",
        "Lerch'in Yöntemi ve Zaza Kaynağı Hassan",
        LOCAL_PROJECT / "post2_method_hassan" / "post2_de_readable_draft.md",
        "Lerch's account of his Roslavl elicitation method and Hassan as his main Zaza source.",
    ),
    SectionSpec(
        "hassan-context",
        "Hassan Diyaloğu Bağlamı",
        "Hassan Dialogue Context",
        "Das Gespräch mit Hassan als Quellenkontext",
        "Conversation with Hassan: Selected Source Context",
        "Hassan ile Konuşma: Seçilmiş Kaynak Bağlamı",
        LOCAL_PROJECT / "post3_hassan_context" / "post3_de_readable_draft.md",
        "Selected source context from the Hassan interview: Sivan, Kasan, villages, seasonal movement, and feud memory.",
    ),
    SectionSpec(
        "alphabet-method",
        "Lerch Zaza'yı Nasıl Yazdı",
        "How Lerch Wrote Zaza",
        "Wie Lerch Zaza schrieb",
        "How Lerch Wrote Zaza",
        "Lerch Zaza'yı Nasıl Yazdı",
        LOCAL_PROJECT / "post4_alphabet_method" / "post4_de_readable_draft.md",
        "Lerch's sound-count and alphabet-method notes, including the later Lepsius-related postscript.",
    ),
    SectionSpec(
        "glossary-context",
        "Sözlük ve Seçilmiş Zaza Notları",
        "Glossary and Selected Zaza Notes",
        "Das Glossar und ausgewählte Zazä-Notizen",
        "The Glossary and Selected Zaza Notes",
        "Sözlük ve Seçilmiş Zaza Notları",
        LOCAL_PROJECT / "post5_glossary_context" / "post5_de_readable_draft.md",
        "The glossary volume's organization, Zaza-related notes, and selected addenda such as `ver` and `go'in`.",
    ),
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing source file: {path}")
    return path.read_text(encoding="utf-8").strip()


def extract_footnote_definitions(markdown: str) -> tuple[str, dict[str, str]]:
    lines = markdown.splitlines()
    body: list[str] = []
    definitions: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^\[\^([A-Za-z0-9_-]+)\]:\s*(.*)$", line)
        if not match:
            body.append(line)
            index += 1
            continue

        footnote_id = match.group(1)
        parts = [match.group(2).strip()]
        index += 1
        while index < len(lines) and (lines[index].startswith("    ") or lines[index].startswith("\t")):
            parts.append(lines[index].strip())
            index += 1
        definitions[footnote_id] = " ".join(part for part in parts if part)

    return "\n".join(body).strip(), definitions


def split_table_row(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def is_markdown_block_start(line: str, next_line: str = "") -> bool:
    stripped = line.strip()
    if stripped == "":
        return True
    if re.match(r"^#{1,6}\s+", stripped):
        return True
    if stripped.startswith(">"):
        return True
    if re.match(r"^\d+\.\s+", stripped) or re.match(r"^[-*+]\s+", stripped):
        return True
    if stripped.startswith("|") and next_line.strip().startswith("|") and is_table_separator(next_line):
        return True
    return False


def render_inline_markdown(text: str, footnotes: dict[str, str], seen_footnotes: dict[str, int], language: str = "en") -> str:
    placeholders: dict[str, str] = {}

    def placeholder(rendered: str) -> str:
        key = f"@@LLBOOK{len(placeholders)}@@"
        placeholders[key] = rendered
        return key

    def code_repl(match: re.Match[str]) -> str:
        return placeholder(f'<span class="ll-book-text__term">{html.escape(match.group(1))}</span>')

    def link_repl(match: re.Match[str]) -> str:
        label = render_inline_markdown(match.group(1), {}, {}, language)
        url = match.group(2).strip()
        if not re.match(r"^https?://", url, re.I):
            return html.escape(match.group(0))
        safe_url = html.escape(url, quote=True)
        return placeholder(f'<a href="{safe_url}" target="_blank" rel="noopener noreferrer">{label}</a>')

    def footnote_repl(match: re.Match[str]) -> str:
        footnote_id = match.group(1)
        if footnote_id not in footnotes:
            return match.group(0)
        if footnote_id not in seen_footnotes:
            seen_footnotes[footnote_id] = len(seen_footnotes) + 1
        number = seen_footnotes[footnote_id]
        safe_id = re.sub(r"[^A-Za-z0-9_-]", "", footnote_id)
        note_word = {"tr": "Dipnot", "de": "Anmerkung", "en": "Note"}.get(language, "Note")
        return placeholder(
            f'<sup class="ll-book-text__footnote-ref" id="ll-book-fnref-{safe_id}">'
            f'<a href="#ll-book-fn-{safe_id}" aria-label="{note_word} {number}">{number}</a>'
            f'</sup>'
        )

    text = re.sub(r"`([^`]+)`", code_repl, text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", link_repl, text)
    text = re.sub(r"\[\^([A-Za-z0-9_-]+)\]", footnote_repl, text)

    rendered = html.escape(text, quote=False)
    rendered = re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", rendered)
    for key, value in placeholders.items():
        rendered = rendered.replace(key, value)
    return rendered


def render_markdown_table(lines: list[str], footnotes: dict[str, str], seen_footnotes: dict[str, int], language: str) -> str:
    header = split_table_row(lines[0])
    body_rows = [split_table_row(line) for line in lines[2:]]
    header_html = "".join(
        f'<th scope="col">{render_inline_markdown(cell, footnotes, seen_footnotes, language)}</th>'
        for cell in header
    )
    rows_html = []
    for row in body_rows:
        cells = list(row)
        if len(cells) < len(header):
            cells.extend([""] * (len(header) - len(cells)))
        row_html = "".join(
            f"<td>{render_inline_markdown(cell, footnotes, seen_footnotes, language)}</td>"
            for cell in cells[: len(header)]
        )
        rows_html.append(f"<tr>{row_html}</tr>")
    return (
        '<div class="ll-book-text__table-wrap"><table class="ll-book-text__table">'
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(rows_html)}</tbody>"
        "</table></div>"
    )


def render_book_markdown(markdown: str, footnotes: dict[str, str] | None = None, language: str = "en") -> str:
    footnotes = footnotes or {}
    lines = markdown.strip().splitlines()
    output: list[str] = []
    seen_footnotes: dict[str, int] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        next_line = lines[index + 1] if index + 1 < len(lines) else ""

        if stripped == "":
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            level = max(3, min(6, len(heading.group(1))))
            output.append(f"<h{level}>{render_inline_markdown(heading.group(2), footnotes, seen_footnotes, language)}</h{level}>")
            index += 1
            continue

        if stripped.startswith("|") and next_line.strip().startswith("|") and is_table_separator(next_line):
            table_lines = [line, next_line]
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            output.append(render_markdown_table(table_lines, footnotes, seen_footnotes, language))
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(re.sub(r"^>\s?", "", lines[index].strip()))
                index += 1
            quote = " ".join(line.strip() for line in quote_lines if line.strip())
            output.append(f"<blockquote><p>{render_inline_markdown(quote, footnotes, seen_footnotes, language)}</p></blockquote>")
            continue

        if re.match(r"^\d+\.\s+", stripped) or re.match(r"^[-*+]\s+", stripped):
            ordered = bool(re.match(r"^\d+\.\s+", stripped))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            pattern = r"^\d+\.\s+" if ordered else r"^[-*+]\s+"
            while index < len(lines) and re.match(pattern, lines[index].strip()):
                item = re.sub(pattern, "", lines[index].strip())
                items.append(f"<li>{render_inline_markdown(item, footnotes, seen_footnotes, language)}</li>")
                index += 1
            output.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            upcoming = lines[index + 1] if index + 1 < len(lines) else ""
            if is_markdown_block_start(lines[index], upcoming):
                break
            paragraph_lines.append(lines[index].strip())
            index += 1
        paragraph = " ".join(line for line in paragraph_lines if line)
        output.append(f"<p>{render_inline_markdown(paragraph, footnotes, seen_footnotes, language)}</p>")

    if seen_footnotes:
        note_labels = {"tr": "Dipnotlar", "de": "Anmerkungen", "en": "Notes"}
        label = note_labels.get(language, "Notes")
        notes = []
        for footnote_id, number in sorted(seen_footnotes.items(), key=lambda item: item[1]):
            safe_id = re.sub(r"[^A-Za-z0-9_-]", "", footnote_id)
            note = render_inline_markdown(footnotes.get(footnote_id, ""), {}, {}, language)
            back_label = {"tr": "Metne dön", "de": "Zurück zum Text", "en": "Back to text"}.get(language, "Back to text")
            notes.append(
                f'<li id="ll-book-fn-{safe_id}">{note} '
                f'<a class="ll-book-text__footnote-back" href="#ll-book-fnref-{safe_id}" aria-label="{back_label}">↩</a>'
                "</li>"
            )
        output.append(f'<section class="ll-book-text__footnotes"><h3>{label}</h3><ol>{"".join(notes)}</ol></section>')

    return "\n".join(output)


def split_h2_sections(markdown: str) -> tuple[str, dict[str, str]]:
    lines = markdown.splitlines()
    preface: list[str] = []
    sections: dict[str, list[str]] = {}
    current_heading = ""
    for line in lines:
        if line.startswith("## "):
            current_heading = line[3:].strip()
            sections[current_heading] = []
            continue
        if current_heading:
            sections[current_heading].append(line)
        else:
            preface.append(line)
    return "\n".join(preface).strip(), {heading: "\n".join(body).strip() for heading, body in sections.items()}


def remove_h1(markdown: str) -> str:
    lines = markdown.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return markdown.strip()


def clean_german_public_text(markdown: str) -> str:
    markdown = remove_h1(markdown)
    paragraphs = [paragraph.strip() for paragraph in markdown.split("\n\n") if paragraph.strip()]
    paragraphs = [paragraph for paragraph in paragraphs if not paragraph.startswith("Draft status:")]
    cleaned = "\n\n".join(paragraphs)
    cleaned = cleaned.replace(" [Datum prüfen.]", "")
    return cleaned.strip()


def combine_markdown(language: str, sections: list[dict]) -> str:
    label_key = f"label_{language}"
    chunks: list[str] = []
    for section in sections:
        chunks.append(f"## {section['labels'][language]}")
        chunks.append("")
        chunks.append(section["texts"][language].strip())
        chunks.append("")
    return "\n".join(chunks).strip() + "\n"


def combine_html(language: str, sections: list[dict]) -> str:
    chunks: list[str] = []
    for section in sections:
        label = html.escape(str(section["labels"][language]))
        chunks.append(f"<h2>{label}</h2>")
        chunks.append(section["texts"][language].strip())
    return "\n\n".join(chunks).strip() + "\n"


def build_payload() -> dict:
    en_markdown, en_footnotes = extract_footnote_definitions(read_text(EN_FULL))
    tr_markdown, tr_footnotes = extract_footnote_definitions(read_text(TR_FULL))
    en_preface, en_sections = split_h2_sections(en_markdown)
    tr_preface, tr_sections = split_h2_sections(tr_markdown)
    book_sections: list[dict] = []
    for spec in SECTIONS:
        if spec.en_heading not in en_sections:
            raise SystemExit(f"Missing English section heading: {spec.en_heading}")
        if spec.tr_heading not in tr_sections:
            raise SystemExit(f"Missing Turkish section heading: {spec.tr_heading}")
        de_text = clean_german_public_text(read_text(spec.de_file))
        book_sections.append(
            {
                "id": spec.section_id,
                "text_format": "html",
                "label": spec.label_tr,
                "labels": {
                    "tr": spec.label_tr,
                    "en": spec.label_en,
                    "de": spec.label_de,
                },
                "source_note": spec.source_note,
                "texts": {
                    "tr": render_book_markdown(tr_sections[spec.tr_heading], tr_footnotes, "tr"),
                    "en": render_book_markdown(en_sections[spec.en_heading], en_footnotes, "en"),
                    "de": render_book_markdown(de_text, {}, "de"),
                },
            }
        )

    return {
        "schema": "ll_tools_text_document.v1",
        "kind": "book_text",
        "text_format": "html",
        "lesson_id": "lerch-book-zazaki-sections",
        "title": "Peter Lerch'in Zazaca Bölümleri",
        "metadata": {
            "collection": "lerch",
            "collection_label": "Peter Lerch Metinleri",
            "excerpt": "Lerch'in Zazaca metinleri, sözlüğü ve ilgili açıklamalarından seçilmiş bölümlerin çok dilli seçkisi.",
            "default_language": "tr",
            "working_status": "reviewed working edition; not final critical edition",
            "generated_at": date.today().isoformat(),
            "source_project": str(LOCAL_PROJECT),
            "publication": {
                "public_summary_tr": "Lerch'in Zazaca metinleri, kaynak kişileri, kullandığı yazı sistemi ve sözlüğü hakkında kendi kitabındaki ilgili bölümlerden hazırlanmış çok dilli seçki.",
                "content_warning_tr": "",
                "people_tr": "Peter Lerch; Hassan; B. von Dorn; Hussein.",
                "places_tr": "Roslavl; Palu; Sivan; Kasan/Kassau/Kaschan; Muş; Tujik/Tuzik; Dúmbeli.",
                "historical_context_tr": "Bu metin, Lerch'in Zazaca malzemeyi nasıl topladığını ve Zazaca metinleri neden bilimsel açıdan önemli gördüğünü açıklayan bölümleri bir araya getirir.",
                "editorial_note_tr": "Bu bölüm anlatı ya da interlinear metin değil, kaynak kitabın Zazaca ile ilgili açıklamalarından yapılmış çok dilli bir okuma metnidir.",
            },
            "intro": {
                "tr": tr_preface.replace("Güncel Türkçe tam çeviri taslağı", "Güncel Türkçe çeviri").replace("Bu bir özet değil, çeviri taslağıdır.", "Bu bir özet değil, çeviridir."),
                "en": en_preface.replace("Working English translation draft", "English translation").replace("This is a translation draft, not a summary.", "This is a translation, not a summary."),
                "de": "Mehrsprachige Auswahl Zazä-bezogener Abschnitte aus Lerchs kurdischen Bänden.",
            },
        },
        "translations": {
            "tr": {"label": "Türkçe"},
            "en": {"label": "English"},
            "de": {"label": "Deutsch"},
        },
        "summary": {
            "book_sections": len(book_sections),
        },
        "book_sections": book_sections,
        "witnesses": [
            {
                "label": "Russian original volumes",
                "citation": "Lerch, Peter Ivanovich. Izsledovaniia ob iranskikh kurdakh i ikh predkakh, severnykh khaldeiakh. St. Petersburg: Imperial Academy of Sciences, 1856-1858.",
                "note": "Russian witnesses are used where the local translation project has aligned them.",
            },
            {
                "label": "German editions",
                "citation": "Lerch, Peter. Forschungen über die Kurden und die iranischen Nordchaldäer. St. Petersburg: Kaiserliche Akademie der Wissenschaften, 1857-1858.",
                "note": "German readable drafts are used for the current German book-text layer.",
            },
        ],
    }


def write_outputs(payload: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    sections = payload["book_sections"]
    (OUT_DIR / "book-text-draft.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (TEXT_DIR / "text-document.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for language in ("tr", "en", "de"):
        rendered = combine_html(language, sections)
        for directory in (OUT_DIR, TEXT_DIR):
            old_markdown = directory / f"book-text.{language}.md"
            if old_markdown.exists():
                old_markdown.unlink()
            (directory / f"book-text.{language}.html").write_text(rendered, encoding="utf-8")
    (TEXT_DIR / "metadata.json").write_text(
        json.dumps(
            {
                "id": payload["lesson_id"],
                "title": payload["title"],
                "title_lerch": "Zaza-related passages from Lerch's Kurdish volumes",
                "author_collector": "Peter Lerch",
                "language": "Turkish, English, German",
                "status": "reviewed working edition",
                "lltools_payload": "text-document.json",
                "publication": payload["metadata"]["publication"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    readme = [
        "# Lerch Book Zaza Sections Draft",
        "",
        "Non-live draft package for a future LL Tools `book_text` post.",
        "",
        "Files:",
        "",
        "- `book-text-draft.json`: draft payload matching the proposed LL Tools book-text shape.",
        "- `book-text.tr.html`, `book-text.en.html`, `book-text.de.html`: language-specific HTML exports for review.",
        "",
        "Status:",
        "",
        "- Live-importable now that LL Tools supports `book_text` documents.",
        "- This remains a reviewed working edition rather than a final critical edition.",
        "- German is assembled from the five readable German section drafts, not from a single full German file.",
        "",
    ]
    (OUT_DIR / "README.md").write_text("\n".join(readme), encoding="utf-8")

    report_lines = [
        "# Lerch Book Sections Draft Status",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "Created a non-live draft package for the Zaza-related prose portions of Lerch's Kurdish volumes.",
        "",
        "## Output",
        "",
        "- `drafts/lerch/book-zaza-sections/book-text-draft.json`",
        "- `drafts/lerch/book-zaza-sections/book-text.tr.html`",
        "- `drafts/lerch/book-zaza-sections/book-text.en.html`",
        "- `drafts/lerch/book-zaza-sections/book-text.de.html`",
        "- `drafts/lerch/book-zaza-sections/README.md`",
        "- `texts/lerch/lerch-book-zazaki-sections/text-document.json`",
        "",
        "## Sections",
        "",
    ]
    for section in sections:
        report_lines.append(f"- `{section['id']}`: {section['labels']['en']} / {section['labels']['tr']} / {section['labels']['de']}")
    report_lines.extend(
        [
            "",
            "## Publication Notes",
            "",
            "- LL Tools now has local `book_text` renderer/import support, including explicit sanitized HTML bodies; live import depends on the deployed plugin matching that support.",
            "- German is stitched from section drafts; a final German full-text pass would still be useful.",
            "",
        ]
    )
    REPORT.write_text("\n".join(report_lines), encoding="utf-8")


def main() -> None:
    payload = build_payload()
    write_outputs(payload)
    print(f"Wrote {OUT_DIR / 'book-text-draft.json'}")
    print(f"Sections: {len(payload['book_sections'])}")


if __name__ == "__main__":
    main()
