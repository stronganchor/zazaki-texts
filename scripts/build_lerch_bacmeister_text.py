#!/usr/bin/env python3
"""Build a live-importable LL Tools text document for Lerch's Bacmeister samples."""

from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = REPO_ROOT / "texts" / "lerch" / "bacmeister-ornek-cumleleri"
LERCH_ROOT = Path(r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch")
SOURCE_DRAFT = (
    LERCH_ROOT
    / "translation_project"
    / "lerch"
    / "appendix_bacmeister_sentence_samples"
    / "bacmeister_sentence_samples_transcription_translation_draft.md"
)
REVIEW_BUNDLE = LERCH_ROOT / "lerch_bacmeister_samples_review_bundle"
ASSET_SOURCE = REVIEW_BUNDLE / "assets"


def assert_inside_repo(path: Path) -> Path:
    resolved = path.resolve()
    root = REPO_ROOT.resolve()
    if resolved != root and root not in resolved.parents:
        raise RuntimeError(f"Refusing to write outside repo: {resolved}")
    return resolved


def strip_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1]
    return value


def split_markdown_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells: list[str] = []
    buf: list[str] = []
    escaped = False
    for char in line:
        if escaped:
            buf.append(char)
            escaped = False
            continue
        if char == "\\":
            buf.append(char)
            escaped = True
            continue
        if char == "|":
            cells.append("".join(buf).strip())
            buf = []
            continue
        buf.append(char)
    cells.append("".join(buf).strip())
    return cells


def parse_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for line in SOURCE_DRAFT.read_text(encoding="utf-8").splitlines():
        if line.startswith("| No. | Kurmanji in Lerch |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = split_markdown_row(line)
        if len(cells) < 7 or not cells[0].isdigit():
            continue
        rows.append(
            {
                "row_no": cells[0],
                "kurmanji": strip_code(cells[1]),
                "zaza": strip_code(cells[2]),
                "german": cells[3],
                "english": cells[4],
                "turkish": cells[5],
                "notes": cells[6],
            }
        )
    if len(rows) != 44:
        raise RuntimeError(f"Expected 44 Bacmeister rows, found {len(rows)}")
    return rows


def plain(value: str) -> str:
    return re.sub(r"`([^`]+)`", r"\1", value).strip()


def write_text(path: Path, value: str) -> None:
    path = assert_inside_repo(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2))


def copy_assets() -> None:
    target = assert_inside_repo(TEXT_DIR / "assets")
    target.mkdir(parents=True, exist_ok=True)
    for image in sorted(ASSET_SOURCE.glob("row??_*.jpg")):
        shutil.copy2(image, target / image.name)


def source_line(row: dict[str, str]) -> dict:
    row_no = int(row["row_no"])
    witnesses = []
    for label, suffix in (("Russian scan", "russian"), ("German reprint scan", "german")):
        asset = f"assets/row{row_no:02d}_{suffix}.jpg"
        if (ASSET_SOURCE / f"row{row_no:02d}_{suffix}.jpg").exists():
            witnesses.append(
                {
                    "label": label,
                    "image_url": asset,
                    "source": "Lerch Bacmeister sentence-sample line crop",
                }
            )
    display_rows = [
        {"label": "ZAZA IN LERCH", "value": row["zaza"]},
        {"label": "KURMANJI IN LERCH", "value": row["kurmanji"]},
        {"label": "GERMAN", "value": plain(row["german"])},
        {"label": "ENGLISH", "value": plain(row["english"])},
        {"label": "TURKISH", "value": plain(row["turkish"])},
    ]
    if row["notes"]:
        display_rows.append({"label": "NOTE", "value": plain(row["notes"])})
    return {
        "id": f"bacmeister_row_{row_no:02d}",
        "title": f"Örnek cümle {row_no}",
        "text": row["zaza"],
        "lerch": row["zaza"],
        "source_note": plain(row["notes"]),
        "display_rows": display_rows,
        "witnesses": witnesses,
        "tokens": [],
        "phrase_matches": [],
    }


def build_payload(rows: list[dict[str, str]]) -> dict:
    reading_units = []
    for row in rows:
        row_no = int(row["row_no"])
        reading_units.append(
            {
                "id": f"u{row_no:02d}",
                "source": row["zaza"],
                "translations": {
                    "tr": plain(row["turkish"]),
                    "en": plain(row["english"]),
                    "de": plain(row["german"]),
                },
                "source_line_ids": [f"bacmeister_row_{row_no:02d}"],
            }
        )

    return {
        "schema": "ll_tools_text_document.v1",
        "kind": "corpus_text",
        "lesson_id": "lerch-bacmeister-ornek-cumleleri",
        "title": "Bacmeister Örnek Cümleleri",
        "source_label": "Zaza (Lerch yazımı)",
        "translations": {
            "tr": {"label": "Turkish"},
            "en": {"label": "English"},
            "de": {"label": "German"},
        },
        "metadata": {
            "collection": "lerch",
            "collection_label": "Peter Lerch Metinleri",
            "excerpt": "Lerch'in Bacmeister'in dil örneklerinden hareketle Kurmanci ve Zaza için yazdığı 44 kısa örnek cümle. Zaza sütunu Lerch'in tarihî ses yazımıyla korunmuştur.",
            "source_author": "Peter Lerch",
            "source_work": "Forschungen über die Kurden und die iranischen Nordchaldäer / Russian original Zazaki transcriptions",
            "story_title_lerch": 'Uebersetzung der "Sprachproben" Bacmeisters in die kurdischen Mundarten Kurmandi und Zaza',
            "story_title_modern_zazaki": "Bacmeister Örnek Cümleleri",
            "working_status": "reviewed working edition; not final critical edition",
            "created_from": str(SOURCE_DRAFT),
            "exported_at": date.today().isoformat(),
            "reader_unit": "sample_sentence",
            "publication": {
                "public_summary_tr": "Lerch'in Bacmeister'in dil örneklerinden hareketle Kurmanci ve Zaza için yazdığı 44 kısa örnek cümle. Zaza sütunu Lerch'in tarihî ses yazımıyla korunmuştur.",
                "content_warning_tr": "",
                "people_tr": "",
                "places_tr": "",
                "historical_context_tr": "Bu bölüm anlatı metni değil, kısa örnek cümlelerden oluşan bir dil malzemesidir. Lerch, Bacmeister'in örneklerini önce Türkçeye çevirip sonra Kürt konuşurlara Kurmanci ve Zaza karşılıklarını söylettiğini açıklar.",
                "editorial_note_tr": "Zaza cümleleri modern yazıma çevrilmeden, Lerch'in tarihî fonetik yazımıyla verilir. Not satırları, tanık farklarını veya kaynakta görünen muhtemel yazım/transkripsiyon hatalarını belirtir.",
            },
        },
        "summary": {
            "lines": len(rows),
            "source_lines": len(rows),
            "reading_units": len(reading_units),
            "tokens": 0,
        },
        "witnesses": [
            {
                "label": "Russian original edition",
                "citation": "Lerch, Peter Ivanovich. Izsledovaniia ob iranskikh kurdakh i ikh predkakh, severnykh khaldeiakh. Vol. 2. St. Petersburg: Imperial Academy of Sciences, 1856. Bacmeister sentence samples, printed pp. 41-44.",
                "pages": "Russian Book II viewer pages 55-58; printed pp. 41-44.",
                "note": "Primary scan witness for the Zaza column in Lerch's historical orthography.",
                "urls": [
                    {
                        "label": "RGO catalog record",
                        "url": "https://elib.rgo.ru/handle/123456789/218398",
                    }
                ],
            },
            {
                "label": "German edition / reprint scan",
                "citation": "Lerch, Peter. Forschungen über die Kurden und die iranischen Nordchaldäer. Abth. 1. St. Petersburg: Kaiserliche Akademie der Wissenschaften, 1857. Bacmeister sentence samples, pp. 1-4 of the text section.",
                "pages": "German reprint pages 45-48 in the local rendered scan set.",
                "note": "Used as a second scan witness and for Lerch's German glosses.",
                "urls": [
                    {
                        "label": "Internet Archive item",
                        "url": "https://archive.org/details/bub_gb_WlGVYoEkr7sC",
                    }
                ],
            },
        ],
        "reading_units": reading_units,
        "source_lines": [source_line(row) for row in rows],
    }


def main() -> None:
    rows = parse_rows()
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    copy_assets()
    payload = build_payload(rows)
    write_json(TEXT_DIR / "text-document.json", payload)
    write_json(
        TEXT_DIR / "metadata.json",
        {
            "id": "lerch-bacmeister-ornek-cumleleri",
            "title": "Bacmeister Örnek Cümleleri",
            "title_lerch": 'Uebersetzung der "Sprachproben" Bacmeisters in die kurdischen Mundarten Kurmandi und Zaza',
            "author_collector": "Peter Lerch",
            "language": "Zazaki",
            "dialect_region_note": "Short elicited Zaza sentence samples from Lerch's Roslavl materials.",
            "status": "reviewed working edition",
            "line_count": len(rows),
            "token_count": 0,
            "lltools_payload": "text-document.json",
            "reviewed_transcription_synced_at": date.today().isoformat(),
            "publication": payload["metadata"]["publication"],
        },
    )
    write_text(TEXT_DIR / "text.zazaki.md", "Bacmeister Örnek Cümleleri\n\n" + "\n\n".join(row["zaza"] for row in rows))
    write_text(TEXT_DIR / "translation.tr.md", "Bacmeister Örnek Cümleleri\n\n" + "\n\n".join(plain(row["turkish"]) for row in rows))
    write_text(TEXT_DIR / "translation.en.md", "Bacmeister Sentence Samples\n\n" + "\n\n".join(plain(row["english"]) for row in rows))
    write_text(TEXT_DIR / "translation.de.md", "Bacmeister Sprachproben\n\n" + "\n\n".join(plain(row["german"]) for row in rows))
    print(f"Wrote {TEXT_DIR.relative_to(REPO_ROOT)} with {len(rows)} rows.")


if __name__ == "__main__":
    main()
