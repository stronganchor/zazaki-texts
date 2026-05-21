#!/usr/bin/env python3
"""Package Lerch Zaza-related prose translations as a draft book_text payload."""

from __future__ import annotations

import json
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


def build_payload() -> dict:
    en_preface, en_sections = split_h2_sections(read_text(EN_FULL))
    tr_preface, tr_sections = split_h2_sections(read_text(TR_FULL))
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
                "label": spec.label_tr,
                "labels": {
                    "tr": spec.label_tr,
                    "en": spec.label_en,
                    "de": spec.label_de,
                },
                "source_note": spec.source_note,
                "texts": {
                    "tr": tr_sections[spec.tr_heading],
                    "en": en_sections[spec.en_heading],
                    "de": de_text,
                },
            }
        )

    return {
        "schema": "ll_tools_text_document.v1",
        "kind": "book_text",
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
        rendered = combine_markdown(language, sections)
        (OUT_DIR / f"book-text.{language}.md").write_text(rendered, encoding="utf-8")
        (TEXT_DIR / f"book-text.{language}.md").write_text(rendered, encoding="utf-8")
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
        "- `book-text.tr.md`, `book-text.en.md`, `book-text.de.md`: language-specific Markdown exports for review.",
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
        "- `drafts/lerch/book-zaza-sections/book-text.tr.md`",
        "- `drafts/lerch/book-zaza-sections/book-text.en.md`",
        "- `drafts/lerch/book-zaza-sections/book-text.de.md`",
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
            "- LL Tools now has local `book_text` renderer/import support; live import depends on the deployed plugin matching that support.",
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
