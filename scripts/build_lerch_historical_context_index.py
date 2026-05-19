#!/usr/bin/env python3
"""Build a conservative people/place/context index for the Lerch texts."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXTS_ROOT = REPO_ROOT / "texts" / "lerch"
REPORT_DIR = REPO_ROOT / "reports"
REPORT_MD = REPORT_DIR / "lerch-historical-context-index.md"
REPORT_TSV = REPORT_DIR / "lerch-historical-context-index.tsv"

HISTORICAL_TEXTS = [
    "gespraech-mit-hassan",
    "kauge-nyerib-u-hyeni",
    "kauge-nyerib-u-sivani",
    "ali-agha-ladi-kelhani",
]

FOLKTALES = [
    "goin-puhu-kusunun-hikayesi",
    "degirmenci-ve-tilki",
    "uc-kardes-masali",
]


@dataclass(frozen=True)
class Entity:
    text_slug: str
    entity_type: str
    name: str
    role_or_note: str
    source_basis: str
    confidence: str
    follow_up: str = ""


CURATED_ENTITIES: list[Entity] = [
    Entity(
        "gespraech-mit-hassan",
        "person",
        "Hassan",
        "Primary Zaza-speaking consultant for the processed Lerch Zazaki texts; says his tribe is Sivan and his village is Kasan/Kassau/Kaschan.",
        "Hassan interview text; Lerch collection intro notes",
        "text_attested",
        "Confirm the modern location of Kasan/Kassau/Kaschan and whether living descendants connect to this village name.",
    ),
    Entity(
        "gespraech-mit-hassan",
        "group",
        "Sivan",
        "Hassan's tribe; the interview says it had thirty-four villages.",
        "Hassan interview text",
        "text_attested",
    ),
    Entity(
        "gespraech-mit-hassan",
        "person",
        "Ali Beg of Aldun",
        "Named as the elder of Aldun.",
        "Hassan interview text",
        "text_attested",
        "Check against Ottoman/local records for Aldun and surrounding Palu/Genç material.",
    ),
    Entity(
        "gespraech-mit-hassan",
        "person",
        "Mistefa Ali",
        "Named as the elder of Gewel.",
        "Hassan interview text",
        "text_attested",
    ),
    Entity(
        "gespraech-mit-hassan",
        "person",
        "Avdula Beg",
        "Mentioned in Hassan's list of feuds he saw: the feud between Sivan and Avdula Beg.",
        "Hassan interview text",
        "text_attested",
        "Compare with the Avdulah Agha of Kelan in the Sivan-Nyêrib story.",
    ),
    Entity(
        "gespraech-mit-hassan",
        "person",
        "Ahmed Beg",
        "Mentioned in Hassan's list of feuds: the feud between Ahmed Beg and Sivan.",
        "Hassan interview text",
        "text_attested",
    ),
    Entity(
        "gespraech-mit-hassan",
        "place",
        "Kasan / Kassau / Kaschan",
        "Hassan's village; described as having sixty houses in the interview.",
        "Hassan interview text; Lerch collection intro notes",
        "text_attested",
        "High-priority place identification; keep all spellings together until externally resolved.",
    ),
    Entity(
        "gespraech-mit-hassan",
        "place",
        "Sivan village list",
        "The interview gives a list of Sivan villages: Fatrakom, Hopsor, Tenik, Rezuan, Zimag, Horsig, Hemek, Bilike, Melekan, Mark, Aldun, Gewel, Kasan, Hoena, Sama, Emera, Shekera, Heylan, Mala-Ibrahiman, Avdelan, Mistan, Sayere, Abasa, Wisheyn, Haspeg, Seratyori, Akeragi, Letan, Gahar, Gowman, Kavare, Talek.",
        "Hassan interview text",
        "text_attested",
        "Split into individually researched modern place rows after external checking.",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "person",
        "Xalef Ağa",
        "Nerib leader in the Nerib-Hyêni feud; receives the report of the first killing, organizes the Nerib side, fights Daqma Beg, and later makes peace.",
        "Nerib-Hyêni text and translation",
        "text_attested",
        "Also appears in the Sivan-Nyêrib story; compare chronology across the two narratives.",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "person",
        "Daqma Beg",
        "Hyêni leader opposing Xalef Ağa; gathers his army near Temir Beg's house and later makes peace through the Ziriki aghas.",
        "Nerib-Hyêni text and translation",
        "text_attested",
        "Check whether Daqma Beg can be identified in external Hani/Hyêni records.",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "person",
        "Temir Beg / Timur Bey of Hani",
        "The story mentions Temir Beg's house as a gathering point. Local research notes identify a likely match with Timur/Temir Bey of Hani, active by 1819 and defeated/exiled in 1835.",
        "Nerib-Hyêni text; local external-source research note",
        "working_hypothesis",
        "Verify the identification in the cited Ottoman/dissertation/Brant sources before making a firm historical claim.",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "person",
        "Mela Haseynê Mûğara",
        "The first Hyêni man killed is described as his servant; the killer says Mela Haseynê Mûğara had killed one of his grandfather's servants earlier.",
        "Nerib-Hyêni text and translation",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "person",
        "Wesman Ağa",
        "Agha of Little Nerib; Xalef sends him word to warn Mehmet Agha.",
        "Nerib-Hyêni text and translation",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "person",
        "Mêhmêt Ağa of Deştê Henzi",
        "Receives warning through Wesman Ağa and reports readiness for the expected Hyêni attack.",
        "Nerib-Hyêni text and translation",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "person",
        "Xalil Efendi",
        "Killed during the attack on Hyêni; his head is taken to Xalef Ağa.",
        "Nerib-Hyêni text and translation",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "group",
        "Ziriki aghas",
        "Asked by Daqma Beg to mediate; they bring Daqma Beg to Xalef Ağa's house and the feud ends with compensation/exchange.",
        "Nerib-Hyêni text and translation",
        "text_attested",
        "Potentially useful for researching regional beylik networks.",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "place",
        "Hyêni / Hêni / Hani / Khini",
        "Main opposing territory/town in the Nerib-Hyêni feud; connected in working notes with Hani and Temir/Timur Bey.",
        "Nerib-Hyêni text; publication metadata",
        "text_attested",
        "Use Hani as a working modern Turkish identification only with caveat.",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "place",
        "Nyêrib",
        "Nerib-side home territory and Xalef Ağa's base.",
        "Nerib-Hyêni text",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "place",
        "Deştê Henzi",
        "Place tied to Mehmet Ağa and also appears in the Sivan-Nyêrib story.",
        "Nerib-Hyêni text; Sivan-Nyêrib text",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "person",
        "Xalef Ağa",
        "Nerib leader in the Sivan-Nyêrib feud; threatens Avdulah Ağa after one of his men is killed, is later badly defeated, and seeks mediation through Hayder Ağa.",
        "Sivan-Nyêrib text and translation",
        "text_attested",
        "Because this story appears to allude to the earlier Hyêni conflict, compare with the Xalef Ağa of the Nerib-Hyêni story.",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "person",
        "Avdulah Ağa of Kelan",
        "Sivan-side leader; confronts Xalef Ağa, burns and plunders Nerib villages, and later grants reconciliation after Hayder Ağa intercedes.",
        "Sivan-Nyêrib text and translation",
        "text_attested",
        "Compare with Hassan's mention of a feud between Sivan and Avdula Beg.",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "person",
        "Mela Ahmed Qafon",
        "His house is robbed at the beginning of the story.",
        "Sivan-Nyêrib text and translation",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "person",
        "Huseyin, son of Mela Ahmed",
        "Catches and kills the Nerib thief and sends word to Xalef Ağa.",
        "Sivan-Nyêrib text and translation",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "person",
        "Hayder Ağa of Qotwesan",
        "Mediates after Xalef Ağa's defeat; takes Xalef Ağa to Avdulah Ağa's house and secures reconciliation.",
        "Sivan-Nyêrib text and translation",
        "text_attested",
        "Potentially important external research target because he acts as protector/mediator.",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "place",
        "Horsig",
        "Sivan-associated place where the opening theft takes place.",
        "Sivan-Nyêrib text and Hassan interview village list",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "place",
        "Kelan",
        "Avdulah Ağa's place.",
        "Sivan-Nyêrib text",
        "text_attested",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "place",
        "Sele stream",
        "Battle rendezvous point named by Avdulah Ağa.",
        "Sivan-Nyêrib text and translation",
        "text_attested",
        "Needs modern identification.",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "place",
        "Dait",
        "Direction/place named as Xalef Ağa's side of the planned battle route.",
        "Sivan-Nyêrib text and translation",
        "text_attested",
        "Needs modern identification.",
    ),
    Entity(
        "kauge-nyerib-u-sivani",
        "date_context",
        "Working chronology: after Nerib-Hyêni, before/during 1853 collection horizon",
        "The message to Xalef warns him not to come to Hyêni because he fought there, so this story seems later than the Nerib-Hyêni story. Since Lerch recorded the texts during the Crimean War period, the broad working range is roughly 1820-1853.",
        "Sivan-Nyêrib story-internal allusion; collection date",
        "working_hypothesis",
        "Do not publish as a fixed date without external confirmation.",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Ali Ağa, son of Kelhan",
        "Mir/chief of the Karbegan district; his village is Narbêş. The story says he killed thirty-four people and was later killed with his four sons.",
        "Ali Ağa text and translation",
        "text_attested",
        "Search external Karbegan/Sivan feud references and possible Ottoman records.",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Kelhan",
        "Named as Ali Ağa's father in the title/patronymic.",
        "Ali Ağa title and opening line",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Qasım Ağa",
        "Karbegan-side figure who plans the attack, deceives Ali Ağa into giving up weapons, and is stabbed by Ahmed. Ahmed addresses him as uncle/nephew language, but the exact kinship should be checked.",
        "Ali Ağa text and translation",
        "text_attested",
        "Clarify kinship terminology from the Zazaki line before publishing as a family relation.",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Weşinli Hasan Ağa",
        "Co-conspirator with Qasım Ağa in the attack on Ali Ağa.",
        "Ali Ağa text and translation",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Ahmed, son of Ali Ağa",
        "Warns against handing over weapons; obtains a dagger, attacks Qasım Ağa, kills Eysan and Hasan Kalan, then is killed.",
        "Ali Ağa text and translation",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Eysan",
        "Killed by Ahmed in the fighting. Metadata should not be read as 'Ahmed Êysan' without checking; the English translation treats Eysan as a separate person.",
        "Ali Ağa text and translation",
        "text_attested",
        "Review the exact line in Lerch before final public person table.",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Hasan Kalan",
        "Killed by Ahmed in the fighting.",
        "Ali Ağa text and translation",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Mela Resa",
        "Calls Mela Qasım of Desmun in the morning to remove and bury the dead.",
        "Ali Ağa text and translation",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Mela Qasım of Desmun",
        "Helps recover and bury Ali Ağa, his sons, and the foreign men.",
        "Ali Ağa text and translation",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Memed Ağa of Ğêytê",
        "Helps recover and bury the bodies after the attack.",
        "Ali Ağa text and translation",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "person",
        "Ramedan Ağa of Merzyelê",
        "Helps recover and bury the bodies after the attack.",
        "Ali Ağa text and translation",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "place",
        "Karbegan",
        "District over which Ali Ağa is said to be mir/chief; later thirty-four Karbegan villages are involved in counsel.",
        "Ali Ağa text and translation",
        "text_attested",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "place",
        "Narbêş",
        "Ali Ağa's village according to the story.",
        "Ali Ağa text and translation",
        "text_attested",
        "Needs modern identification.",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "place",
        "Syeraçur",
        "Place where Ali Ağa stays for thirty-six days after packing up his household.",
        "Ali Ağa text and translation",
        "text_attested",
        "Needs modern identification.",
    ),
    Entity(
        "ali-agha-ladi-kelhani",
        "place",
        "Weşin",
        "Place associated with Hasan Ağa; also appears in Hassan's Sivan village list as Wisheyn/Weşin.",
        "Ali Ağa text; Hassan interview",
        "text_attested",
    ),
]

CHRONOLOGY_NOTES = [
    (
        "Nerib-Hyêni",
        "If Temir Beg is the documented Timur/Temir Bey of Hani, the cleanest working range is c. 1819-1835: active as Hani notable by 1819 and defeated/exiled in 1835. This is a working historical identification, not a final date.",
    ),
    (
        "Sivan-Nyêrib",
        "The story appears to allude to the earlier Nerib-Hyêni conflict, so it likely follows that feud. The broad working range remains roughly 1820-1853, with 1853/Crimean War collection context as the upper horizon.",
    ),
    (
        "Ali Ağa",
        "No firm external date has been identified yet. Treat as a local feud narrative from the same remembered historical world, but do not attach it to the Temir Beg date range without evidence.",
    ),
    (
        "Hassan interview",
        "Not a feud event narrative; it is direct source/context evidence for Hassan, Sivan villages, and the feuds Hassan says he witnessed.",
    ),
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def text_label(slug: str, metadata: dict) -> str:
    return metadata.get("title") or metadata.get("title_tr") or slug


def load_text_metadata() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for metadata_path in sorted(TEXTS_ROOT.glob("*/metadata.json")):
        rows[metadata_path.parent.name] = read_json(metadata_path)
    return rows


def write_tsv(rows: list[Entity], metadata_by_slug: dict[str, dict]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fields = [
        "text_slug",
        "text_title",
        "entity_type",
        "name",
        "role_or_note",
        "source_basis",
        "confidence",
        "follow_up",
    ]
    with REPORT_TSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "text_slug": row.text_slug,
                    "text_title": text_label(row.text_slug, metadata_by_slug[row.text_slug]),
                    "entity_type": row.entity_type,
                    "name": row.name,
                    "role_or_note": row.role_or_note,
                    "source_basis": row.source_basis,
                    "confidence": row.confidence,
                    "follow_up": row.follow_up,
                }
            )


def md_table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return []
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    out: list[str] = []
    header = rows[0]
    out.append("| " + " | ".join(header[i].ljust(widths[i]) for i in range(len(header))) + " |")
    out.append("| " + " | ".join("---".ljust(widths[i]) for i in range(len(header))) + " |")
    for row in rows[1:]:
        out.append("| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(row))) + " |")
    return out


def write_markdown(rows: list[Entity], metadata_by_slug: dict[str, dict]) -> None:
    lines: list[str] = [
        "# Lerch Historical Context Index",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "- Consolidates the current people, places, groups, and dating notes for the historically framed Lerch Zazaki texts.",
        "- Uses only the current repository text metadata, translations, and already-recorded local research notes.",
        "- Keeps working identifications separate from text-attested facts.",
        "- Excludes folktales from historical people/place claims unless a future external source justifies adding them.",
        "",
        "## Text Overview",
        "",
    ]

    overview = [["Text", "Summary", "People", "Places", "Context note"]]
    for slug in HISTORICAL_TEXTS:
        metadata = metadata_by_slug[slug]
        publication = metadata.get("publication", {})
        overview.append(
            [
                text_label(slug, metadata),
                publication.get("public_summary_tr", ""),
                publication.get("people_tr", ""),
                publication.get("places_tr", ""),
                publication.get("historical_context_tr", ""),
            ]
        )
    lines.extend(md_table(overview))
    lines.extend(["", "## Curated Entity Notes", ""])

    entity_rows = [["Text", "Type", "Name", "Current note", "Confidence", "Follow-up"]]
    for row in rows:
        entity_rows.append(
            [
                text_label(row.text_slug, metadata_by_slug[row.text_slug]),
                row.entity_type,
                row.name,
                row.role_or_note,
                row.confidence,
                row.follow_up,
            ]
        )
    lines.extend(md_table(entity_rows))

    lines.extend(["", "## Raw Metadata Cross-Check", ""])
    raw_rows = [["Text", "Metadata people", "Metadata places"]]
    for slug in HISTORICAL_TEXTS:
        metadata = metadata_by_slug[slug]
        publication = metadata.get("publication", {})
        raw_rows.append(
            [
                text_label(slug, metadata),
                "; ".join(split_semicolon(publication.get("people_tr", ""))),
                "; ".join(split_semicolon(publication.get("places_tr", ""))),
            ]
        )
    lines.extend(md_table(raw_rows))

    lines.extend(["", "## Working Chronology", ""])
    for label, note in CHRONOLOGY_NOTES:
        lines.append(f"- **{label}:** {note}")

    lines.extend(["", "## Folktales Excluded From Historical Entity Index", ""])
    for slug in FOLKTALES:
        metadata = metadata_by_slug[slug]
        publication = metadata.get("publication", {})
        warning = publication.get("content_warning_tr") or "none"
        lines.append(f"- **{text_label(slug, metadata)}:** {publication.get('historical_context_tr', '')} Content warning: {warning}.")

    lines.extend(
        [
            "",
            "## Research Next Steps",
            "",
            "1. Verify Temir Beg / Timur Bey of Hani against the external Ottoman, dissertation, Zirki, and Brant sources before using the 1819-1835 range as anything stronger than a working note.",
            "2. Resolve Kasan/Kassau/Kaschan and the Sivan village list against modern place names.",
            "3. Split the raw village list from the Hassan interview into individually researched place entries once modern matches are known.",
            "4. Check whether Avdula Beg in Hassan's interview is the same person or tradition as Avdulah Ağa of Kelan in the Sivan-Nyêrib story.",
            "5. Review the Ali Ağa person list, especially Eysan versus the metadata string `Ahmed Êysan`, before publishing a final public person table.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    metadata_by_slug = load_text_metadata()
    missing = [slug for slug in HISTORICAL_TEXTS + FOLKTALES if slug not in metadata_by_slug]
    if missing:
        raise SystemExit(f"Missing Lerch text metadata for: {', '.join(missing)}")

    rows = sorted(CURATED_ENTITIES, key=lambda item: (HISTORICAL_TEXTS.index(item.text_slug), item.entity_type, item.name))
    write_tsv(rows, metadata_by_slug)
    write_markdown(rows, metadata_by_slug)
    print(f"Wrote {REPORT_MD.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_TSV.relative_to(REPO_ROOT)}")
    print(f"Curated entity rows: {len(rows)}")


if __name__ == "__main__":
    main()
