#!/usr/bin/env python3
"""Build a corrected working layer for Lerch's Zazaki glossary.

The raw extraction remains untouched.  This script proposes scan/text-informed
fields that can be reviewed before any public glossary import.
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LERCH_DIR = Path(r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch")
GLOSSARY_TSV = LERCH_DIR / "lltools_import" / "lltools_dictionary_lerch_glossary_full.tsv"
QA_TSV = LERCH_DIR / "lerch_zazaki_glossary_qa.tsv"
TEXTS_DIR = REPO_ROOT / "texts" / "lerch"
OUT_TSV = REPO_ROOT / "reports" / "lerch-glossary-corrected-layer.tsv"
OUT_MD = REPO_ROOT / "reports" / "lerch-glossary-corrected-layer.md"

if str(LERCH_DIR) not in sys.path:
    sys.path.insert(0, str(LERCH_DIR))

from build_lerch_feud_interlinear_bundle import lerch_to_zazaki  # noqa: E402


FUNCTION_WORDS = {
    "de",
    "ra",
    "re",
    "ke",
    "ki",
    "bi",
    "ne",
    "ma",
    "ez",
    "tu",
    "ti",
    "a",
    "u",
    "û",
}

OCR_CLEANUPS = {
    "Ã¶lTne": "öffne",
    "Ã¶lTnet": "öffnet",
    "giebt": "gibt",
    "falleu": "fallen",
    "Einmischen": "Einmischen",
    "tiirk": "türk.",
    "tÃ¼rk": "türk.",
    "Ygl.": "Vgl.",
    "SÃ¤ugclhier": "Säugetier",
    "Terpentiubaum": "Terpentinbaum",
    "sÃ¤u- met": "säumet",
    "ver- gleichen": "vergleichen",
    "zusam- men": "zusammen",
    "einmischeo": "einmischen",
}

GERMAN_GLOSS_MAP: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"\bPersonenname\b|\bEigenname\b", re.I), "personal name", "kişi adı"),
    (re.compile(r"\bOrtsname\b", re.I), "place name", "yer adı"),
    (re.compile(r"\bMonatsname\b", re.I), "month name", "ay adı"),
    (re.compile(r"\bWasser\b.*\bQuelle\b.*\bBach\b", re.I), "water; spring; stream", "su; kaynak; dere"),
    (re.compile(r"\bWasser\b", re.I), "water", "su"),
    (re.compile(r"\bQuelle\b", re.I), "spring; source", "kaynak; pınar"),
    (re.compile(r"\bBach\b", re.I), "stream", "dere"),
    (re.compile(r"\bsogleich\b|\bsofort\b", re.I), "immediately", "hemen"),
    (re.compile(r"\bSchakal\b", re.I), "jackal", "çakal"),
    (re.compile(r"\bVerstand\b", re.I), "understanding; reason", "akıl; anlayış"),
    (re.compile(r"\bAgha\b|\bAga\b", re.I), "agha; notable", "ağa"),
    (re.compile(r"\bStamm\b|\bTribus\b", re.I), "tribe", "aşiret"),
    (re.compile(r"\bMonat\b.*\bMond\b|\bMond\b.*\bMonat\b", re.I), "month; moon", "ay"),
    (re.compile(r"\bMehl\b", re.I), "flour", "un"),
    (re.compile(r"\bMühle\b", re.I), "mill", "değirmen"),
    (re.compile(r"\bGold\b", re.I), "gold", "altın"),
    (re.compile(r"\bgolden\b", re.I), "golden", "altın renkli; altından"),
    (re.compile(r"\bKummer\b|\bSorge\b", re.I), "sorrow; worry", "üzüntü; kaygı"),
    (re.compile(r"\bBrot\b", re.I), "bread", "ekmek"),
    (re.compile(r"\bLohn\b", re.I), "reward; pay", "ödül; ücret"),
    (re.compile(r"\bEsel\b", re.I), "donkey", "eşek"),
    (re.compile(r"\bdick\b", re.I), "thick", "kalın"),
    (re.compile(r"\bblind\b", re.I), "blind", "kör"),
    (re.compile(r"\bRabe\b", re.I), "raven; crow", "karga"),
    (re.compile(r"\bSichel\b", re.I), "sickle", "orak"),
    (re.compile(r"\bWeide\b", re.I), "willow; pasture", "söğüt; mera"),
    (re.compile(r"\bKopf\b", re.I), "head", "baş; kafa"),
    (re.compile(r"\bGesicht\b", re.I), "face", "yüz"),
    (re.compile(r"\bSchwert\b", re.I), "sword", "kılıç"),
    (re.compile(r"\bDorf\b", re.I), "village", "köy"),
    (re.compile(r"\bTag\b", re.I), "day", "gün"),
    (re.compile(r"\bNacht\b", re.I), "night", "gece"),
    (re.compile(r"\bMorgen\b", re.I), "morning", "sabah"),
    (re.compile(r"\bheute\b", re.I), "today", "bugün"),
    (re.compile(r"\bmorgen\b", re.I), "tomorrow", "yarın"),
    (re.compile(r"\bgestern\b", re.I), "yesterday", "dün"),
    (re.compile(r"\bMann\b", re.I), "man", "adam; erkek"),
    (re.compile(r"\bWeib\b|\bFrau\b", re.I), "woman; wife", "kadın; eş"),
    (re.compile(r"\bTochter\b|\bMädchen\b", re.I), "daughter; girl", "kız; kız çocuğu"),
    (re.compile(r"\bSohn\b", re.I), "son", "oğul"),
    (re.compile(r"\bVater\b", re.I), "father", "baba"),
    (re.compile(r"\bMutter\b", re.I), "mother", "anne"),
    (re.compile(r"\bBruder\b", re.I), "brother", "kardeş"),
    (re.compile(r"\bSchwester\b", re.I), "sister", "kız kardeş"),
    (re.compile(r"\bHaus\b", re.I), "house", "ev"),
    (re.compile(r"\bPferd\b", re.I), "horse", "at"),
    (re.compile(r"\bOchse\b|\bStier\b", re.I), "ox; bull", "öküz; boğa"),
    (re.compile(r"\bHund\b", re.I), "dog", "köpek"),
    (re.compile(r"\bHase\b", re.I), "hare", "tavşan"),
    (re.compile(r"\bWolf\b", re.I), "wolf", "kurt"),
    (re.compile(r"\bFuchs\b", re.I), "fox", "tilki"),
    (re.compile(r"\bVogel\b", re.I), "bird", "kuş"),
    (re.compile(r"\bBlut\b", re.I), "blood", "kan"),
    (re.compile(r"\bFeuer\b", re.I), "fire", "ateş"),
    (re.compile(r"\bErde\b", re.I), "earth; ground", "toprak; yer"),
    (re.compile(r"\bStein\b", re.I), "stone", "taş"),
    (re.compile(r"\bHand\b", re.I), "hand", "el"),
    (re.compile(r"\bFuß\b|\bFuss\b", re.I), "foot", "ayak"),
    (re.compile(r"\bAuge\b", re.I), "eye", "göz"),
    (re.compile(r"\bOhr\b", re.I), "ear", "kulak"),
    (re.compile(r"\bNase\b", re.I), "nose", "burun"),
    (re.compile(r"\bZahn\b", re.I), "tooth", "diş"),
    (re.compile(r"\bHerz\b", re.I), "heart", "kalp; yürek"),
    (re.compile(r"\bessen\b|\biss\b|\bisst\b", re.I), "eat", "yemek"),
    (re.compile(r"\btrinken\b|\btrinkt\b", re.I), "drink", "içmek"),
    (re.compile(r"\bkommen\b|\bkommt\b|\bkomme\b", re.I), "come", "gelmek"),
    (re.compile(r"\bgehen\b|\bging\b", re.I), "go", "gitmek"),
    (re.compile(r"\bsehen\b|\bsehe\b|\bsah\b", re.I), "see", "görmek"),
    (re.compile(r"\bsagen\b|\bsagt\b", re.I), "say; tell", "söylemek; demek"),
    (re.compile(r"\bgeben\b|\bgibt\b|\bgab\b", re.I), "give", "vermek"),
    (re.compile(r"\bnehmen\b|\bnahm\b", re.I), "take", "almak"),
    (re.compile(r"\bbringen\b|\bbrachte\b", re.I), "bring", "getirmek"),
    (re.compile(r"\böffne\b|\böffnete\b", re.I), "open", "açmak"),
    (re.compile(r"\bschlagen\b|\bSchlag\b", re.I), "strike; blow", "vurmak; darbe"),
    (re.compile(r"\bfallen\b|\bfiel\b", re.I), "fall", "düşmek"),
    (re.compile(r"\bstehen\b|\bstand\b", re.I), "stand", "durmak"),
    (re.compile(r"\bsitzen\b|\bsaß\b|\bsass\b", re.I), "sit", "oturmak"),
    (re.compile(r"\bbleiben\b|\bblieb\b", re.I), "remain; stay", "kalmak"),
    (re.compile(r"\bberühre\b|\brühret\b", re.I), "touch", "dokunmak"),
    (re.compile(r"\bgro[ßs]\b", re.I), "big; large", "büyük"),
    (re.compile(r"\bklein\b", re.I), "small", "küçük"),
    (re.compile(r"\bgut\b", re.I), "good", "iyi"),
    (re.compile(r"\bschlecht\b", re.I), "bad", "kötü"),
    (re.compile(r"\balt\b|\bältester\b", re.I), "old; oldest", "yaşlı; en büyük"),
    (re.compile(r"\bneu\b", re.I), "new", "yeni"),
    (re.compile(r"\brot\b", re.I), "red", "kırmızı"),
    (re.compile(r"\bweiß\b|\bweiss\b", re.I), "white", "beyaz"),
    (re.compile(r"\bschwarz\b", re.I), "black", "siyah"),
    (re.compile(r"\beins\b|\bein\b", re.I), "one", "bir"),
    (re.compile(r"\bzwei\b", re.I), "two", "iki"),
    (re.compile(r"\bdrei\b", re.I), "three", "üç"),
    (re.compile(r"\bvier\b", re.I), "four", "dört"),
    (re.compile(r"\bfünf\b|\bfuenf\b", re.I), "five", "beş"),
    (re.compile(r"\bzehn\b", re.I), "ten", "on"),
    (re.compile(r"\bhundert\b", re.I), "hundred", "yüz"),
]


@dataclass
class TextVariant:
    surface: str
    count: int
    examples: str


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def strip_marks(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value or "")
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def compact_key(value: str) -> str:
    value = strip_marks(value)
    value = value.replace("γ", "g").replace("Γ", "g").replace("χ", "x").replace("Χ", "x")
    value = value.replace("š", "s").replace("Š", "s").replace("ž", "z").replace("Ž", "z")
    value = value.replace("ı", "i").replace("İ", "i").replace("ʼ", "").replace("’", "").replace("'", "")
    value = re.sub(r"[^0-9A-Za-z]+", "", value)
    return value.casefold()


def diacritic_score(value: str) -> int:
    score = 0
    for ch in value or "":
        if unicodedata.category(ch) == "Mn":
            score += 2
        elif ord(ch) > 127:
            score += 1
    return score


def clean_headword(value: str) -> str:
    value = (value or "").strip()
    value = re.sub(r"\s+", " ", value)
    value = value.strip(" ,.;:()[]")
    if "," in value:
        value = value.split(",", 1)[0].strip()
    return value


def clean_german_gloss(value: str) -> str:
    text = " ".join((value or "").replace("\u00ad", "").split())
    for old, new in OCR_CLEANUPS.items():
        text = text.replace(old, new)
    text = text.replace(" .", ".").replace(" ,", ",")
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"([,.;:])(?=\S)", r"\1 ", text)
    return text.strip()


def short_gloss_for_translation(value: str) -> str:
    text = value or ""
    text = re.sub(r"\bVgl\..*$", "", text).strip()
    text = re.sub(r"\bcf\..*$", "", text).strip()
    text = re.sub(r"\b[0-9]{1,3}\.[0-9A-Za-z.\- ]+.*$", "", text).strip()
    return text.strip(" ;,.")


def translate_german_gloss(value: str) -> tuple[str, str, str]:
    text = short_gloss_for_translation(value)
    if not text:
        return "", "", ""
    hits_en: list[str] = []
    hits_tr: list[str] = []

    def add_parts(target: list[str], value: str) -> None:
        for part in re.split(r"\s*;\s*", value):
            part = part.strip()
            if part and part not in target:
                target.append(part)

    for pattern, en, tr in GERMAN_GLOSS_MAP:
        if pattern.search(text):
            add_parts(hits_en, en)
            add_parts(hits_tr, tr)
    if not hits_en:
        return "", "", ""
    return "; ".join(hits_en[:4]), "; ".join(hits_tr[:4]), "rule_guess_from_german"


def load_qa() -> dict[str, dict[str, str]]:
    return {row.get("row_id", ""): row for row in read_tsv(QA_TSV) if row.get("row_id")}


def load_text_variant_index() -> dict[str, TextVariant]:
    buckets: dict[str, Counter[str]] = defaultdict(Counter)
    examples: dict[tuple[str, str], set[str]] = defaultdict(set)
    for path in TEXTS_DIR.glob("*/morphemes.tsv"):
        slug = path.parent.name
        for row in read_tsv(path):
            values = [
                row.get("token_lerch") or "",
                row.get("morpheme_surface_lerch") or "",
            ]
            segment = row.get("segment_id") or ""
            for value in values:
                surface = clean_headword(value)
                key = compact_key(surface)
                if not key or key in FUNCTION_WORDS or len(key) <= 1:
                    continue
                buckets[key][surface] += 1
                if len(examples[(key, surface)]) < 3:
                    examples[(key, surface)].add(f"{slug}:{segment}")

    index: dict[str, TextVariant] = {}
    for key, counter in buckets.items():
        ranked = sorted(counter.items(), key=lambda item: (item[1], diacritic_score(item[0]), len(item[0])), reverse=True)
        if not ranked:
            continue
        surface, count = ranked[0]
        index[key] = TextVariant(surface=surface, count=count, examples="; ".join(sorted(examples[(key, surface)])))
    return index


def propose_group(entry: str, row: dict[str, str], corrected: str) -> tuple[str, str]:
    parent = row.get("parent", "").strip()
    if parent:
        return parent, "existing_parent"

    raw = entry or ""
    if "=" in raw:
        rhs = raw.split("=", 1)[1].strip()
        rhs = clean_headword(rhs)
        if rhs:
            return rhs, "equals_reference"

    german = row.get("definition_de", "") or ""
    match = re.search(r"(?:^|[.;]\s*)s\.\s*([A-Za-zÄÖÜäöüßÇçÊêÎîÛûĀāĒēĪīŌōŠšŽžḱǵṅγχʼ’'\-]+)", german)
    if match:
        return match.group(1).strip(), "see_reference"

    if re.search(r"[’']a$", corrected):
        return re.sub(r"[’']a$", "-", corrected), "verb_present_stem_guess"
    if re.search(r"[’']u$", corrected):
        return re.sub(r"[’']u$", "-", corrected), "verb_present_stem_guess"
    return corrected, "self"


def build_rows() -> list[dict[str, str]]:
    qa = load_qa()
    text_index = load_text_variant_index()
    rows: list[dict[str, str]] = []

    for row in read_tsv(GLOSSARY_TSV):
        row_id = row.get("source_row_idx", "")
        raw_entry = row.get("entry_display") or row.get("entry") or ""
        raw_entry = clean_headword(raw_entry)
        qa_row = qa.get(row_id)
        text_variant = text_index.get(compact_key(raw_entry))

        corrected = raw_entry
        source = "raw_extraction"
        notes: list[str] = []
        if qa_row and qa_row.get("best_guess_lerch"):
            corrected = clean_headword(qa_row["best_guess_lerch"])
            source = "qa_reviewed"
        elif text_variant and text_variant.surface and diacritic_score(text_variant.surface) > diacritic_score(raw_entry):
            corrected = text_variant.surface
            source = "text_form_match"
            notes.append(f"text examples: {text_variant.examples}")

        german_raw = row.get("definition_de", "")
        german_clean = clean_german_gloss(qa_row.get("gloss_de", "") if qa_row and qa_row.get("gloss_de") else german_raw)
        en_rule, tr_rule, rule_source = translate_german_gloss(german_clean)

        definition_en = ""
        definition_en_source = ""
        definition_tr = ""
        definition_tr_source = ""
        if qa_row:
            definition_en = qa_row.get("gloss_en", "").strip()
            definition_tr = qa_row.get("gloss_tr", "").strip()
            if definition_en:
                definition_en_source = "qa_reviewed"
            if definition_tr:
                definition_tr_source = "qa_reviewed"
        if not definition_en and row.get("definition_en"):
            definition_en = row["definition_en"].strip()
            definition_en_source = row.get("definition_en_source") or "existing_import"
        if not definition_tr and row.get("definition_tr"):
            definition_tr = row["definition_tr"].strip()
            definition_tr_source = row.get("definition_tr_source") or "existing_import"
        if not definition_en and en_rule:
            definition_en = en_rule
            definition_en_source = rule_source
        if not definition_tr and tr_rule:
            definition_tr = tr_rule
            definition_tr_source = rule_source

        group_headword, group_source = propose_group(raw_entry, row, corrected)
        modern = lerch_to_zazaki(corrected)

        confidence = "low"
        if source == "qa_reviewed":
            confidence = "high"
        elif source == "text_form_match" or row.get("entry_review_status") == "headword_parented":
            confidence = "medium"

        rows.append(
            {
                "row_id": row_id,
                "entry_id": row.get("entry_id", ""),
                "source_page": row.get("source_page", ""),
                "raw_lerch_headword": raw_entry,
                "corrected_lerch_headword": corrected,
                "corrected_headword_source": source,
                "modern_zazaki_guess": modern,
                "proposed_group_headword": group_headword,
                "group_source": group_source,
                "german_gloss_raw": german_raw,
                "german_gloss_clean": german_clean,
                "english_gloss": definition_en,
                "english_gloss_source": definition_en_source,
                "turkish_gloss": definition_tr,
                "turkish_gloss_source": definition_tr_source,
                "existing_parent": row.get("parent", ""),
                "entry_review_status": row.get("entry_review_status", ""),
                "correction_confidence": confidence,
                "notes": "; ".join(notes),
            }
        )

    return rows


def write_summary(rows: list[dict[str, str]]) -> None:
    status = Counter(row["entry_review_status"] or "(blank)" for row in rows)
    source = Counter(row["corrected_headword_source"] for row in rows)
    confidence = Counter(row["correction_confidence"] for row in rows)
    group = Counter(row["group_source"] for row in rows)
    en_count = sum(1 for row in rows if row["english_gloss"])
    tr_count = sum(1 for row in rows if row["turkish_gloss"])
    german_clean_changed = sum(1 for row in rows if row["german_gloss_clean"] != row["german_gloss_raw"])
    text_matched = [row for row in rows if row["corrected_headword_source"] == "text_form_match"]

    lines = [
        "# Lerch Glossary Corrected Layer",
        "",
        "This is a generated review layer. It preserves the raw glossary extraction and proposes corrected fields for human review.",
        "",
        "## Counts",
        "",
        f"- Rows: {len(rows)}",
        f"- German glosses cleaned/changed: {german_clean_changed}",
        f"- Rows with English gloss after this pass: {en_count}",
        f"- Rows with Turkish gloss after this pass: {tr_count}",
        "",
        "## Headword Sources",
        "",
    ]
    for key, count in source.most_common():
        lines.append(f"- {key}: {count}")
    lines.extend(["", "## Correction Confidence", ""])
    for key, count in confidence.most_common():
        lines.append(f"- {key}: {count}")
    lines.extend(["", "## Existing Review Status", ""])
    for key, count in status.most_common():
        lines.append(f"- {key}: {count}")
    lines.extend(["", "## Grouping Sources", ""])
    for key, count in group.most_common():
        lines.append(f"- {key}: {count}")
    lines.extend(["", "## Text-Matched Headword Improvements", ""])
    lines.append("| Row | Page | Raw | Proposed | Modern Zazaki | Notes |")
    lines.append("| ---: | ---: | --- | --- | --- | --- |")
    for row in text_matched[:80]:
        lines.append(
            "| {row_id} | {page} | {raw} | {corrected} | {modern} | {notes} |".format(
                row_id=row["row_id"],
                page=row["source_page"],
                raw=row["raw_lerch_headword"].replace("|", "\\|"),
                corrected=row["corrected_lerch_headword"].replace("|", "\\|"),
                modern=row["modern_zazaki_guess"].replace("|", "\\|"),
                notes=row["notes"].replace("|", "\\|"),
            )
        )
    lines.extend(
        [
            "",
            "## Next Steps",
            "",
            "- Use the review UI to check each proposed corrected headword against the German scan page.",
            "- Treat `text_form_match` as a useful suggestion, not as final evidence, because glossary lemmas and text inflections may differ.",
            "- Promote reviewed rows into the import glossary only after the corrected headword and German gloss are scan-checked.",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    fields = [
        "row_id",
        "entry_id",
        "source_page",
        "raw_lerch_headword",
        "corrected_lerch_headword",
        "corrected_headword_source",
        "modern_zazaki_guess",
        "proposed_group_headword",
        "group_source",
        "german_gloss_raw",
        "german_gloss_clean",
        "english_gloss",
        "english_gloss_source",
        "turkish_gloss",
        "turkish_gloss_source",
        "existing_parent",
        "entry_review_status",
        "correction_confidence",
        "notes",
    ]
    write_tsv(OUT_TSV, rows, fields)
    write_summary(rows)
    print(f"Wrote {OUT_TSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
