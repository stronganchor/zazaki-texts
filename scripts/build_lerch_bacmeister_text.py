#!/usr/bin/env python3
"""Build a live-importable LL Tools text document for Lerch's Bacmeister samples."""

from __future__ import annotations

import json
import re
import shutil
import importlib.util
import sys
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
CONVERTER_SCRIPT = LERCH_ROOT / "build_lerch_feud_interlinear_bundle.py"
TOKEN_STRIP = " \t\r\n.,;:!?()[]{}\"“”‘’«»—–"


BACMEISTER_TOKEN_GLOSSES: dict[int, list[str]] = {
    1: ["God", "NEG", "die"],
    2: ["person", "life", "3SG.OBL", "short"],
    3: ["mother", "children", "children", "self/her", "very", "love"],
    4: ["breasts", "3SG.OBL", "very", "milk", "exist"],
    5: ["husband", "3SG.OBL", "love", "do"],
    6: ["that", "woman", "pregnant"],
    7: ["six", "day", "one", "son", "bore"],
    8: ["still", "NEG", "healthy"],
    9: ["daughter", "3SG.OBL", "beside", "sitting", "cry"],
    10: ["child", "breast", "NEG", "want"],
    11: ["girl", "still", "foot", "NEG", "walk"],
    12: ["one", "year", "two", "month", "was born"],
    13: ["these", "four", "all", "boys", "healthy"],
    14: ["one", "first", "run", "do", "that", "second", "jump", "dance", "do", "that", "third", "song", "say/sing", "that", "fourth", "laugh"],
    15: ["this", "person", "eye", "3SG.OBL", "3SG.OBL", "blind"],
    16: ["wife", "3SG.OBL", "3SG.OBL", "deaf"],
    17: ["voice", "our", "that", "we", "said", "NEG", "hear"],
    18: ["brother", "2SG.OBL", "sneeze", "come"],
    19: ["sister", "2SG.OBL", "sleep", "fell"],
    20: ["father", "2PL.OBL", "awake", "sitting"],
    21: ["little", "eat/drink"],
    22: ["nose", "is", "middle", "face-in"],
    23: ["two", "feet", "we", "exist", "each", "hand", "our-in", "five", "fingers", "exist"],
    24: ["hair", "head-on", "come/grow"],
    25: ["teeth", "tongue", "is", "mouth-in"],
    26: ["hand/arm", "right", "strong", "than", "hand", "left"],
    27: ["one", "hair", "long", "thin"],
    28: ["blood", "red"],
    29: ["bones", "like", "stone", "hard"],
    30: ["fish-in", "eyes", "exist", "ears", "not-exist"],
    31: ["this", "bird", "slowly", "fly"],
    32: ["descend", "ground-to"],
    33: ["wings", "bird-in", "hairs/feathers", "black", "exist"],
    34: ["tree-in", "leaves", "green", "branches", "thick", "exist"],
    35: ["this", "bird", "beak", "pointed", "exist", "tail", "short", "exist"],
    36: ["nest-in", "inside", "eggs", "white", "exist"],
    37: ["fire", "burn", "smoke", "flame", "coal", "we", "see"],
    38: ["this", "river", "water", "quickly", "go/flow"],
    39: ["moon", "stars-than", "big", "sun-than", "small"],
    40: ["yesterday", "evening", "rain", "rained"],
    41: ["today", "morning", "I", "rainbow", "arc", "saw"],
    42: ["night", "dark", "day", "bright"],
    43: ["we", "speech", "do/speak", "Zaza-in"],
    44: ["you.PL", "Zaza-in", "know"],
}


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


def load_lerch_converter():
    if not CONVERTER_SCRIPT.exists():
        raise RuntimeError(f"Missing Lerch converter script: {CONVERTER_SCRIPT}")
    spec = importlib.util.spec_from_file_location("lerch_feud_converter", CONVERTER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load Lerch converter from {CONVERTER_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


LERCH_CONVERTER = load_lerch_converter()


def token_core(value: str) -> str:
    return value.strip(TOKEN_STRIP)


def split_token_punctuation(value: str) -> tuple[str, str, str]:
    prefix_match = re.match(r'^[\s"“”‘’«»(\[\{]+', value)
    suffix_match = re.search(r'[\s"“”‘’«».,;:!?()\]\}]+$', value)
    prefix = prefix_match.group(0) if prefix_match else ""
    suffix = suffix_match.group(0) if suffix_match else ""
    core_start = len(prefix)
    core_end = len(value) - len(suffix) if suffix else len(value)
    core = value[core_start:core_end]
    return prefix, core, suffix


def build_token(raw: str, gloss: str = "") -> dict[str, object]:
    prefix, core, suffix = split_token_punctuation(raw)
    if core == "":
        core = token_core(raw)
        prefix = ""
        suffix = raw[len(core):] if core and raw.endswith(core) is False else ""
    ipa = LERCH_CONVERTER.lerch_to_ipa(core) if core else ""
    zazaki = LERCH_CONVERTER.lerch_to_zazaki(core) if core else ""
    token: dict[str, object] = {
        "form": core or raw,
        "ipa": ipa,
        "zazaki": zazaki,
        "display_gloss": gloss,
        "morphemes": [
            {
                "form": core or raw,
                "normalized": zazaki,
                "gloss": gloss,
                "confidence": "working",
                "evidence": "Automatic Bacmeister sentence-sample interlinear pass; review against the scan before treating as final.",
            }
        ],
    }
    if prefix:
        token["prefix_punct"] = prefix
    if suffix:
        token["suffix_punct"] = suffix
    return token


def build_tokens(row: dict[str, str]) -> list[dict[str, object]]:
    row_no = int(row["row_no"])
    raw_tokens = re.findall(r"\S+", row["zaza"])
    glosses = BACMEISTER_TOKEN_GLOSSES.get(row_no, [])
    if len(glosses) != len(raw_tokens):
        glosses = [""] * len(raw_tokens)
    return [build_token(raw, gloss) for raw, gloss in zip(raw_tokens, glosses)]


def copy_assets() -> None:
    target = assert_inside_repo(TEXT_DIR / "assets")
    target.mkdir(parents=True, exist_ok=True)
    for image in sorted(ASSET_SOURCE.glob("row??_*.jpg")):
        shutil.copy2(image, target / image.name)


def source_line(row: dict[str, str]) -> dict:
    row_no = int(row["row_no"])
    tokens = build_tokens(row)
    ipa_line = " ".join(str(token.get("ipa") or "") for token in tokens).strip()
    zazaki_line = "".join(
        (
            str(token.get("prefix_punct") or "")
            + str(token.get("zazaki") or token.get("form") or "")
            + str(token.get("suffix_punct") or "")
            + (" " if index < len(tokens) - 1 else "")
        )
        for index, token in enumerate(tokens)
    ).strip()
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
        {"label": "LERCH", "value": row["zaza"]},
        {"label": "IPA", "value": ipa_line},
        {"label": "ZAZAKI", "value": zazaki_line},
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
        "source_note": plain(row["notes"]),
        "display_rows": display_rows,
        "witnesses": witnesses,
        "tokens": tokens,
        "phrase_matches": [],
        "hidden_rows": ["LEMMA", "POS"],
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
