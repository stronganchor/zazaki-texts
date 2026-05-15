from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXTS_ROOT = REPO_ROOT / "texts" / "lerch"
LERCH_ROOT = Path(r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch")
EXPORT_DATE = date.today().isoformat()
TRANSLATION_TITLES = {
    "ali-agha-ladi-kelhani": {
        "en": "Ali Agha, Son of Kelhan",
        "tr": "Kelhan'ın Oğlu Ali Ağa",
        "de": "Ali Agha, der Sohn Kelhän's",
    },
    "kauge-nyerib-u-hyeni": {
        "en": "The Feud Between Nerib and Hyeni",
        "tr": "Nyêrib ile Hyêni'nin Kavgası",
        "de": "Fehde zwischen Nerib und Hyeni",
    },
    "kauge-nyerib-u-sivani": {
        "en": "The hostilities between Nerib and Sivan",
        "tr": "Nyêrib ve Sivan'ın kavgası",
        "de": "Die Feindseligkeiten zwischen Nerib und Sivan",
    },
    "gespraech-mit-hassan": {
        "en": "Conversation with Hassan",
        "tr": "Hassan ile Söyleşi",
    },
}

READING_UNIT_SOURCE_LINE_IDS = {
    "kauge-nyerib-u-sivani": {
        "u01": ["s01_l02", "s01_l03", "s01_l04"],
        "u02": ["s01_l05"],
        "u03": ["s01_l06"],
        "u04": ["s01_l07", "s01_l08"],
        "u05": ["s01_l09"],
        "u06": ["s01_l10"],
        "u07": ["s01_l11", "s01_l12", "s01_l13"],
        "u08": ["s02_l01", "s02_l02", "s02_l03"],
        "u09": ["s02_l04", "s02_l05", "s02_l06", "s02_l07"],
        "u10": ["s02_l08", "s02_l09"],
        "u11": ["s02_l10"],
        "u12": ["s02_l11", "s02_l12"],
        "u13": ["s02_l13", "s02_l14"],
        "u14": ["s02_l15"],
        "u15": ["s03_l01", "s03_l02"],
        "u16": ["s03_l03"],
        "u17": ["s03_l04"],
        "u18": ["s03_l05", "s03_l06", "s03_l07"],
        "u19": ["s03_l08", "s03_l09"],
        "u20": ["s03_l10"],
        "u21": ["s03_l11", "s03_l12", "s03_l13", "s04_l01"],
        "u22": ["s04_l02", "s04_l03"],
        "u23": ["s04_l04"],
        "u24": ["s04_l05"],
        "u25": ["s04_l06", "s04_l07"],
        "u26": ["s04_l08", "s04_l09"],
        "u27": ["s04_l10"],
        "u28": ["s04_l11", "s04_l12"],
        "u29": ["s04_l13"],
        "u30": ["s04_l14", "s04_l15", "s05_l01", "s05_l02"],
        "u31": ["s05_l03", "s05_l04", "s05_l05"],
        "u32": ["s05_l06", "s05_l07"],
        "u33": ["s05_l08", "s05_l09"],
        "u34": ["s05_l10"],
        "u35": ["s05_l11", "s05_l12"],
        "u36": ["s05_l13", "s05_l14", "s05_l15"],
        "u37": ["s06_l01"],
        "u38": ["s06_l02"],
        "u39": ["s06_l03"],
        "u40": ["s06_l04"],
    },
}

SIVAN_SOURCE_SEGMENT_GROUPS = [
    [0],
    [1, 2],
    [3, 4],
    [5, 6],
    [7, 8],
    [9],
    [10],
    [11],
    [12],
    [13],
    [14],
    [15],
    [16],
    [17],
    [18],
    [19],
    [20],
    [21],
    [22],
    [23],
    [24],
    [25],
    [26],
    [27],
    [28],
    [29],
    [30],
    [31],
    [32],
    [33],
    [34],
    [35],
    [36],
    [37],
    [38],
    [39],
    [40],
]

SIVAN_TRANSLATION_GROUPS_FROM_40 = [
    [0],
    [1],
    [2],
    [3],
    [4, 5],
    [6],
    [7],
    [8],
    [9],
    [10],
    [11],
    [12],
    [13],
    [14],
    [15, 16],
    [17],
    [18],
    [19],
    [20],
    [21],
    [22],
    [23],
    [24],
    [25],
    [26],
    [27],
    [28],
    [29],
    [30],
    [31],
    [32],
    [33],
    [34],
    [35],
    [36],
    [37, 38],
    [39],
]

TRAILING_PUNCTUATION = ".,;:?!-"


def assert_inside_repo(path: Path) -> Path:
    resolved = path.resolve()
    root = REPO_ROOT.resolve()
    if resolved != root and root not in resolved.parents:
        raise RuntimeError(f"Refusing to write outside repo: {resolved}")
    return resolved


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path = assert_inside_repo(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def write_text(path: Path, value: str) -> None:
    path = assert_inside_repo(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip() + "\n")


def clean_join(parts: list[str]) -> str:
    return re.sub(r"\s+", " ", " ".join(part.strip() for part in parts if part and part.strip())).strip()


def join_source_parts(parts: list[str]) -> str:
    text = clean_join(parts)
    text = re.sub(r"-\s+", "", text)
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    return clean_join([text])


def trailing_punctuation(value: str) -> str:
    end = len(value)
    start = end
    while start > 0 and value[start - 1] in TRAILING_PUNCTUATION:
        start -= 1
    return value[start:end]


def token_text(token: dict, key: str) -> str:
    text = str(token.get(key, "") or "")
    if key != "zazaki" or not text:
        return text
    punctuation = trailing_punctuation(str(token.get("lerch", "") or ""))
    if punctuation and not text.endswith(punctuation):
        text += punctuation
    return text


def line_text(line: dict, key: str) -> str:
    return clean_join([token_text(token, key) for token in line.get("tokens", [])])


def corpus_token(token: dict) -> dict:
    morphemes = token.get("morphemes") if isinstance(token.get("morphemes"), list) else []
    first_morph = morphemes[0] if morphemes else {}
    return {
        "form": token.get("lerch") or token.get("core") or "",
        "ipa": token.get("ipa") or "",
        "zazaki": token_text(token, "zazaki"),
        "lemma": first_morph.get("lemma") or token.get("core") or token.get("lerch") or "",
        "display_gloss": token.get("gloss") or "",
        "gloss_tr": token.get("gloss_tr") or "",
        "gloss_de": token.get("gloss_de") or "",
        "pos": first_morph.get("pos") or "",
        "morphemes": [
            {
                "form": morph.get("surface_lerch") or morph.get("form") or "",
                "normalized": morph.get("normalized") or "",
                "lemma": morph.get("lemma") or "",
                "gloss": morph.get("gloss") or "",
                "pos": morph.get("pos") or "",
                "features": morph.get("features") or "",
                "confidence": morph.get("confidence") or "",
                "evidence": morph.get("evidence") or "",
                "notes": morph.get("notes") or "",
            }
            for morph in morphemes
        ],
    }


def source_line(line: dict, source_label: str) -> dict:
    lerch = line_text(line, "lerch")
    ipa = line_text(line, "ipa")
    zazaki = line_text(line, "zazaki")
    display_rows = [
        {"label": "LERCH", "value": lerch},
        {"label": "IPA", "value": ipa},
        {"label": "ZAZAKI", "value": zazaki},
    ]
    if line.get("free_translation_en"):
        display_rows.append({"label": "ENGLISH", "value": line["free_translation_en"]})
    if line.get("free_translation_tr"):
        display_rows.append({"label": "TURKISH", "value": line["free_translation_tr"]})

    witnesses = []
    if line.get("russian_asset"):
        witnesses.append(
            {
                "label": "Russian scan",
                "image_url": line["russian_asset"],
                "source": f"Lerch line crop; Russian printed page {line.get('russian_print_page') or ''}, scan page {line.get('russian_page') or ''}".strip(),
            }
        )
    if line.get("german_asset"):
        witnesses.append(
            {
                "label": "German reprint scan",
                "image_url": line["german_asset"],
                "source": f"{source_label} German line crop",
            }
        )

    return {
        "id": line["segment_id"],
        "title": line.get("title") or line["segment_id"],
        "text": lerch,
        "lerch": lerch,
        "ipa": ipa,
        "zazaki": zazaki,
        "source_note": line.get("source_note") or "",
        "russian_print_page": line.get("russian_print_page"),
        "russian_scan_page": line.get("russian_page"),
        "display_rows": display_rows,
        "witnesses": witnesses,
        "tokens": [corpus_token(token) for token in line.get("tokens", [])],
        "phrase_matches": line.get("phrases") or [],
        "hidden_rows": {"bingol_transcription": line.get("bingol_transcription") or ""},
    }


def sentence_segments_from_source_lines(source_lines: list[dict]) -> list[str]:
    text = join_source_parts([str(line.get("zazaki", "")) for line in source_lines])
    return [segment.strip() for segment in re.split(r"(?<=[.?])\s+", text) if segment.strip()]


def grouped_translation(units: list[dict], indexes: list[int], lang: str) -> str:
    return clean_join([str(units[index].get("translations", {}).get(lang, "")) for index in indexes if index < len(units)])


def repair_existing_sivan_translations(units: list[dict]) -> list[dict]:
    if len(units) != len(SIVAN_SOURCE_SEGMENT_GROUPS):
        return units
    split_markers = {
        "tr": "Hayder Ağa ata bindi",
        "en": "Haider Agha mounted",
        "de": "Haider Agha sass auf",
    }
    repaired = json.loads(json.dumps(units, ensure_ascii=False))
    for lang, marker in split_markers.items():
        first = str(repaired[34].get("translations", {}).get(lang, ""))
        second = str(repaired[35].get("translations", {}).get(lang, ""))
        if marker not in second:
            continue
        prefix, suffix = second.split(marker, 1)
        if not prefix.strip():
            continue
        repaired[34].setdefault("translations", {})[lang] = clean_join([first, prefix])
        repaired[35].setdefault("translations", {})[lang] = clean_join([marker + suffix])
    return repaired


def rebuild_sivan_reader_units(doc: dict, source_lines: list[dict]) -> list[dict]:
    old_units = repair_existing_sivan_translations(list(doc.get("reading_units", [])))
    source_segments = sentence_segments_from_source_lines(source_lines[1:])
    if len(source_segments) <= max(max(group) for group in SIVAN_SOURCE_SEGMENT_GROUPS):
        return old_units

    if len(old_units) == len(SIVAN_TRANSLATION_GROUPS_FROM_40) + 3:
        translation_groups = SIVAN_TRANSLATION_GROUPS_FROM_40
    elif len(old_units) == len(SIVAN_SOURCE_SEGMENT_GROUPS):
        translation_groups = [[index] for index in range(len(SIVAN_SOURCE_SEGMENT_GROUPS))]
    else:
        translation_groups = [[index] for index in range(min(len(old_units), len(SIVAN_SOURCE_SEGMENT_GROUPS)))]

    units = []
    for index, source_group in enumerate(SIVAN_SOURCE_SEGMENT_GROUPS):
        translation_group = translation_groups[index] if index < len(translation_groups) else []
        translations = {
            lang: grouped_translation(old_units, translation_group, lang)
            for lang in doc.get("translations", {})
        }
        units.append(
            {
                "id": f"u{index + 1:02d}",
                "source": join_source_parts([source_segments[segment_index] for segment_index in source_group]),
                "translations": {lang: value for lang, value in translations.items() if value},
            }
        )
    return units


def copy_bundle_assets(bundle_dir: Path, target_dir: Path) -> None:
    source_assets = bundle_dir / "assets"
    if not source_assets.exists():
        return
    target_assets = assert_inside_repo(target_dir / "assets")
    target_assets.mkdir(parents=True, exist_ok=True)
    for source in source_assets.iterdir():
        if source.is_file():
            shutil.copy2(source, target_assets / source.name)


def copy_morphemes(bundle_dir: Path, target_dir: Path, morpheme_file: str) -> None:
    source = bundle_dir / morpheme_file
    target = assert_inside_repo(target_dir / "morphemes.tsv")
    lines = source.read_text(encoding="utf-8").splitlines()
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(line.rstrip() for line in lines) + "\n")


def update_existing_text(slug: str, bundle: str, interlinear_file: str, morpheme_file: str, source_label: str) -> dict:
    target_dir = TEXTS_ROOT / slug
    bundle_dir = LERCH_ROOT / bundle
    doc_path = target_dir / "text-document.json"
    doc = read_json(doc_path)
    data = read_json(bundle_dir / interlinear_file)
    lines = data.get("lines", [])
    fresh_source_lines = [source_line(line, source_label) for line in lines]
    source_by_id = {line["id"]: line for line in fresh_source_lines}

    if slug == "kauge-nyerib-u-sivani":
        doc["reading_units"] = rebuild_sivan_reader_units(doc, fresh_source_lines)
    else:
        for unit in doc.get("reading_units", []):
            ids = unit.get("source_line_ids") or READING_UNIT_SOURCE_LINE_IDS.get(slug, {}).get(unit.get("id"), [])
            if ids:
                unit["source_line_ids"] = ids
            unit["source"] = join_source_parts([source_by_id[line_id]["zazaki"] for line_id in ids if line_id in source_by_id])

    doc["source_lines"] = fresh_source_lines
    doc["summary"] = {
        **doc.get("summary", {}),
        "lines": len(lines),
        "source_lines": len(fresh_source_lines),
        "reading_units": len(doc.get("reading_units", [])),
        "tokens": sum(len(line.get("tokens", [])) for line in lines),
    }
    doc.setdefault("metadata", {})["reviewed_transcription_synced_at"] = EXPORT_DATE
    write_json(doc_path, doc)

    metadata_path = target_dir / "metadata.json"
    if metadata_path.exists():
        metadata = read_json(metadata_path)
        metadata["line_count"] = len(lines)
        metadata["token_count"] = doc["summary"]["tokens"]
        metadata["reviewed_transcription_synced_at"] = EXPORT_DATE
        write_json(metadata_path, metadata)

    write_public_text_files(target_dir, doc)
    copy_bundle_assets(bundle_dir, target_dir)
    copy_morphemes(bundle_dir, target_dir, morpheme_file)
    return {"slug": slug, "lines": len(lines), "tokens": doc["summary"]["tokens"]}


def write_public_text_files(target_dir: Path, doc: dict) -> None:
    units = doc.get("reading_units", [])
    write_text(target_dir / "text.zazaki.md", f"{doc['title']}\n\n" + "\n\n".join(unit.get("source", "") for unit in units))
    translation_titles = TRANSLATION_TITLES.get(target_dir.name, {})
    for lang in doc.get("translations", {}):
        paragraphs = [unit.get("translations", {}).get(lang, "") for unit in units]
        paragraphs = [paragraph for paragraph in paragraphs if paragraph]
        if paragraphs:
            write_text(target_dir / f"translation.{lang}.md", f"{translation_titles.get(lang, doc['title'])}\n\n" + "\n\n".join(paragraphs))


def hassan_witnesses() -> list[dict]:
    common_bingol_urls = [
        {
            "label": "Bingöl repository PDF",
            "url": "https://bnposta.bingol.edu.tr/bitstream/handle/20.500.12898/600/10053832.pdf?isAllowed=y&sequence=1",
        },
        {
            "label": "YÖK thesis record",
            "url": "https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id=XSxuloAAz12quT5oHaDwnA&no=lqmlps2zRpavNQmdt0OGGQ",
        },
    ]
    return [
        {
            "label": "Russian original edition",
            "citation": "Lerch, Peter Ivanovich. Izsledovaniia ob iranskikh kurdakh i ikh predkakh, severnykh khaldeiakh. Vol. 1. St. Petersburg: Imperial Academy of Sciences, 1856. Dialogue with Hassan, printed pp. 96-99.",
            "pages": "Russian RGO viewer images 110-113; printed pp. 96-99.",
            "note": "Primary scan witness for Lerch's Zazaki transcription and Russian free translation.",
            "urls": [
                {
                    "label": "RGO viewer, text start",
                    "url": "https://elib.rgo.ru/safe-view/123456789/218398/1/MTAwMDAyMTBfTGVya2gsIFBldHIgSXZhbm92aWNoICgxODI3LTE4ODQpLiBJc3NsZWRvdmFuaXlhIG8ucGRm#110",
                }
            ],
        },
        {
            "label": "German edition / reprint scan",
            "citation": "Lerch, Peter. Forschungen über die Kurden und die iranischen Nordchaldäer. Abth. 1. St. Petersburg: Kaiserliche Akademie der Wissenschaften, 1857. Text 'Gespräch mit Hassan,' pp. 103-105.",
            "pages": "Internet Archive scan pages around n146-n148; printed pp. 103-105.",
            "note": "Used as a second scan witness for the Zazaki transcription and for German comparison.",
            "urls": [
                {
                    "label": "Internet Archive, text start",
                    "url": "https://archive.org/details/bub_gb_WlGVYoEkr7sC/page/n146/mode/1up",
                },
                {
                    "label": "Internet Archive item",
                    "url": "https://archive.org/details/bub_gb_WlGVYoEkr7sC",
                },
            ],
        },
        {
            "label": "Bingöl University thesis transcription",
            "citation": "Aslanoğulları, Mehmet. Lerch'in Zazaki Derlemelerinin Çevrimyazımı ve Türlerine Göre Sözcüklerin Tahlili. Master's thesis, Bingöl Üniversitesi, 2014.",
            "pages": "PDF pp. 44-46; heading 'Diyalog.'",
            "note": "Secondary transcription witness used during alignment and review. The transcription text is cited here but is not reproduced in the Interlinear view.",
            "urls": common_bingol_urls,
        },
    ]


def translation_for_group(lines: list[dict], lang: str) -> str:
    text = clean_join([line.get(f"free_translation_{lang}") or "" for line in lines])
    fixes = {
        "He- mek": "Hemek",
        "Sa- ma": "Sama",
        "po- megranate": "pomegranate",
        "nar- ağaçları": "nar ağaçları",
        "I saw many feuds. By my father, the feud between Nerib and Hyeni I saw;": "I saw many feuds. By my father, I saw the feud between Nerib and Hyeni;",
        "Çok kavga gördüm. Babamın hakkı için, Nyêrib ile Hyêni'nin kavgasını ben gördüm;": "Çok kavga gördüm. Babamın hakkı için, Nyêrib ile Hyêni'nin kavgasını gördüm;",
    }
    for old, new in fixes.items():
        text = text.replace(old, new)
    return text


def create_hassan_text() -> dict:
    slug = "gespraech-mit-hassan"
    target_dir = TEXTS_ROOT / slug
    bundle_dir = LERCH_ROOT / "lerch_hassan_review_bundle"
    data = read_json(bundle_dir / "lerch_hassan_interlinear_data.json")
    lines = data.get("lines", [])
    source_lines = [source_line(line, "Müller 1865") for line in lines]
    source_by_id = {line["id"]: line for line in source_lines}
    raw_by_id = {line["segment_id"]: line for line in lines}

    groups = [
        ("u01", ["h01_l01", "h01_l02"]),
        ("u02", ["h01_l03", "h01_l04"]),
        ("u03", ["h01_l05", "h01_l06"]),
        ("u04", ["h01_l07", "h01_l08", "h01_l09", "h01_l10", "h01_l11", "h01_l12"]),
        ("u05", ["h01_l13", "h02_l01"]),
        ("u06", ["h02_l02", "h02_l03"]),
        ("u07", ["h02_l04", "h02_l05"]),
        ("u08", ["h02_l06", "h02_l07"]),
        ("u09", ["h02_l08", "h02_l09"]),
        ("u10", ["h02_l10", "h02_l11", "h02_l12"]),
        ("u11", ["h02_l13", "h02_l14", "h02_l15"]),
        ("u12", ["h02_l16", "h03_l01"]),
        ("u13", ["h03_l02", "h03_l03"]),
        ("u14", ["h03_l04", "h03_l05"]),
        ("u15", ["h03_l06", "h03_l07"]),
        ("u16", ["h03_l08", "h03_l09", "h03_l10"]),
        ("u17", ["h03_l11", "h03_l12", "h03_l13", "h03_l14"]),
        ("u18", ["h03_l15", "h04_l01"]),
    ]
    reading_units = []
    for unit_id, ids in groups:
        group_source = [source_by_id[line_id] for line_id in ids]
        group_raw = [raw_by_id[line_id] for line_id in ids]
        reading_units.append(
            {
                "id": unit_id,
                "source": clean_join([line["zazaki"] for line in group_source]),
                "translations": {
                    "en": translation_for_group(group_raw, "en"),
                    "tr": translation_for_group(group_raw, "tr"),
                },
                "source_line_ids": ids,
            }
        )

    doc = {
        "schema": "ll_tools_text_document.v1",
        "kind": "corpus_text",
        "lesson_id": "lerch-gespraech-mit-hassan",
        "title": "Hassan ile Söyleşi",
        "source_label": "Zazaki",
        "translations": {
            "tr": {"label": "Turkish"},
            "en": {"label": "English"},
        },
        "metadata": {
            "collection": "lerch",
            "collection_label": "Peter Lerch Zazaki Texts",
            "excerpt": "Hassan ile yapılan kısa bir söyleşide Sivan aşiretinin köyleri, Kasan köyü, bahçeler, yayla yaşamı ve Hassan'ın gördüğü kan davaları anlatılır.",
            "source_author": "Peter Lerch",
            "source_work": "Forschungen über die Kurden und die iranischen Nordchaldäer / Russian original Zazaki transcriptions",
            "story_title_lerch": "Gespräch mit Hassan",
            "story_title_modern_zazaki": "Hassan ile Söyleşi",
            "working_status": "reviewed working edition; not final critical edition",
            "created_from": "Lerch Hassan review bundle in Language/Z/Dictionaries/Lerch",
            "exported_at": EXPORT_DATE,
            "reviewed_transcription_synced_at": EXPORT_DATE,
            "reader_unit": "dialogue_exchange",
        },
        "summary": {
            "lines": len(lines),
            "source_lines": len(source_lines),
            "reading_units": len(reading_units),
            "tokens": sum(len(line.get("tokens", [])) for line in lines),
        },
        "witnesses": hassan_witnesses(),
        "reading_units": reading_units,
        "source_lines": source_lines,
    }
    write_json(target_dir / "text-document.json", doc)
    write_json(
        target_dir / "metadata.json",
        {
            "id": "lerch-gespraech-mit-hassan",
            "title": "Hassan ile Söyleşi",
            "title_lerch": "Gespräch mit Hassan",
            "author_collector": "Peter Lerch",
            "language": "Zazaki",
            "dialect_region_note": "Sivan/Kasan-area material as discussed in local project notes.",
            "status": "reviewed working edition",
            "line_count": len(lines),
            "token_count": doc["summary"]["tokens"],
            "lltools_payload": "text-document.json",
            "reviewed_transcription_synced_at": EXPORT_DATE,
        },
    )
    write_public_text_files(target_dir, doc)
    copy_bundle_assets(bundle_dir, target_dir)
    copy_morphemes(bundle_dir, target_dir, "lerch_morpheme_segmentation.tsv")
    return {"slug": slug, "lines": len(lines), "tokens": doc["summary"]["tokens"]}


def main() -> None:
    results = [
        update_existing_text(
            "ali-agha-ladi-kelhani",
            "lerch_ali_agha_review_bundle",
            "lerch_ali_agha_interlinear_data.json",
            "lerch_ali_agha_morpheme_segmentation.tsv",
            "Müller 1865",
        ),
        update_existing_text(
            "kauge-nyerib-u-hyeni",
            "lerch_nerib_hyeni_review_bundle",
            "lerch_nerib_hyeni_interlinear_data.json",
            "lerch_nerib_hyeni_morpheme_segmentation.tsv",
            "Müller 1865",
        ),
        update_existing_text(
            "kauge-nyerib-u-sivani",
            "lerch_feud_review_bundle",
            "lerch_feud_interlinear_data.json",
            "lerch_morpheme_segmentation.tsv",
            "Müller 1865",
        ),
        create_hassan_text(),
    ]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
