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
        "Hassan interview text; Lerch collection intro notes; Köse 2016 Sivan nahiye article; Kiepert 1850s map",
        "text_attested",
        "Keep the common Kasan/Kasun = Günkondu identification unless stronger evidence connects Hassan's village to the separate Kaşan/Qaşan name.",
    ),
    Entity(
        "gespraech-mit-hassan",
        "group",
        "Sivan",
        "Hassan's tribe/territorial frame; the interview says it had thirty-four villages. External records show an 1841 Sivan nahiye attached to Palu, later transferred to Genç/Servi.",
        "Hassan interview text; Köse 2016 Sivan nahiye article",
        "source_supported",
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
        "Hassan's village; described as having sixty houses in the interview. Working match is Kasan/Kasun = Günkondu in the published Sivan village lists. Köse's 1841 table lists a separate Kaşan, and later lists preserve Kaşan/Qaşan around Doğanlı/Kelahsı, but there is no indication that Hassan pronounced his village name with š, so this is treated as a separate, similar-sounding place rather than the primary identification.",
        "Hassan interview text; Köse 2016 Sivan nahiye article; Atan 2020 Genç thesis; Cewlik local place-name list; Kiepert 1850s map",
        "source_supported",
        "Kiepert's Kaschan may be the separate Kaşan/Qaşan near Doğanlı; keep that as an internal caution, not as the public primary match.",
    ),
    Entity(
        "gespraech-mit-hassan",
        "place",
        "Sivan village list",
        "The interview gives a Sivan village list. Several names now have source-backed matches in the 1841 Sivan nahiye list: Kasan/Kasun = Günkondu, Horsig/Horsik = Saklıca, Aldun = Alaaddin, Hopsor/Hapsor = Ericek, Tenik/Tinik = Doludere, Rezuan/Rızvan = Harmancık, Zimag/Zimak = Bahçebaşı, Melekan = Sarıbudak. Köse also lists a separate Kaşan entry, but it is not treated as Hassan's Kasan. Kiepert shows Melken south of Sivan Maaden and northwest of Hani, strengthening the Melêkang/Melekan = Sarıbudak comparison.",
        "Hassan interview text; Köse 2016 Sivan nahiye article; Atan 2020 Genç thesis; Kiepert 1850s map",
        "source_supported",
        "Continue splitting the raw village list into individually researched place rows; verify Gewel, Talek, Kavare, Gowman, Hoena, Sama, Emera, Akeragi, Letan, Gahar, and related forms.",
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
        "The story mentions Temir Beg's house as a gathering point. A likely external match is Timur/Temir Bey of Hani/Khini: documented as Hani emin in February 1835, described by Brant as the exiled ruler of Khiní, and included among the beys defeated and sent to Istanbul/Edirne in 1835.",
        "Nerib-Hyêni text; yurtluk-ocaklık dissertation; Brant 1841; Zirki Beylikleri study",
        "working_hypothesis",
        "Use c. 1819-1835 as a working dating window only if Temir Beg's house is his active Hani residence, not merely a later landmark.",
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
        "Main opposing territory/town in the Nerib-Hyêni feud. Verheij's 19th-century place-name index aligns Brant's Khini and Taylor's Heyni with modern Hani.",
        "Nerib-Hyêni text; Verheij place-name index; Brant/Taylor annotations",
        "source_supported",
        "Use Hani as the working modern Turkish identification; still distinguish this from smaller Hyêni-linked localities mentioned inside the story.",
    ),
    Entity(
        "kauge-nyerib-u-hyeni",
        "place",
        "Nyêrib",
        "Nerib-side home territory and Xalef Ağa's base. Verheij's Taylor 1865 annotation gives Nerib = Kuyular, a village/neighbourhood in Hani district.",
        "Nerib-Hyêni text; Verheij Taylor 1865 annotation",
        "source_supported",
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
        "Sivan-associated place where the opening theft takes place. Best working match is Horsig/Horsik = Saklıca in the 1841 Sivan nahiye village list.",
        "Sivan-Nyêrib text; Hassan interview village list; Köse 2016 Sivan nahiye article",
        "source_supported",
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
        "Battle rendezvous point named by Avdulah Ağa. The Hêvî/Malmîsanij note points to the Hani-side Şelli/Turalı villages, and Kiepert's map shows a Schel/Schel-like label northeast of Hani near Gjaurköi.",
        "Sivan-Nyêrib text and translation; Hêvî/Malmîsanij note; Kiepert 1850s map",
        "source_supported",
        "Treat as Hani-side Şelê/Şelli rather than the Sivan-side Şelê Heydan/Yaydere unless stronger contrary evidence appears.",
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
        "District over which Ali Ağa is said to be mir/chief; later thirty-four Karbegan villages are involved in counsel. External Sivan research notes a Karabegan nahiye associated with Sivan in the 1870-1871 Diyarbakır salname.",
        "Ali Ağa text and translation; Köse/Servi-region article citing Diyarbakır salname",
        "source_supported",
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
        "If Temir Beg is the documented Timur/Temir Bey of Hani, the cleanest working range is c. 1819-1835: the broader source trail places him in Hani politics by 1819, names him Hani emin in February 1835, and shows him defeated/exiled in 1835. This is a working historical identification, not a final date.",
    ),
    (
        "Sivan-Nyêrib",
        "The story appears to allude to the earlier Nerib-Hyêni conflict, so it likely follows that feud. The broad working range remains roughly 1820-1853, with the Crimean War collection context as the upper horizon. The place frame links Sivan/Servi-Palu to Nerib/Kuyular-Hani.",
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

EXTERNAL_SOURCE_NOTES = [
    (
        "Sivan / Servi / Kasan / Kaşan / Horsik",
        "Muhammed Köse's 2016 Sivan nahiye article says Sivan was a 42-village nahiye of Palu in 1841, later transferred to Genç and renamed Servi; its table lists Kaşan as row 3 and Kasan/Günkondu as row 13, so these should not be merged automatically.",
        "https://dergipark.org.tr/tr/pub/bad/article/468213",
    ),
    (
        "Doğanlı / Kelahsı / Qaşan and Günkondu / Kasan alternatives",
        "Fırat Atan's 2020 Genç thesis preserves Doğanlı as Kelahsi/Kelhisi with Heciyun and Kaşan, and separately gives Günkondu as Kasun/Kasan. Because Hassan's own village name is Kasan rather than Kaşan, keep Günkondu as the working match and treat the Doğanlı-area Kaşan/Qaşan as a separate, similar-sounding caution.",
        "https://bnposta.bingol.edu.tr/xmlui%3B/bitstream/handle/20.500.12898/5759/F%C4%B1rat%20ATAN-Y.L.%20Tezi.pdf?isAllowed=y&sequence=1",
    ),
    (
        "Kiepert map evidence: Kaschan, Sivan Maaden, Melken, Schel",
        "Kiepert's 1850s map labels Kaschan east of Palu and just north of Sivan Maaden. Given the separate Kaşan entry in the 1841 Sivan table, this map label may refer to that similar-sounding place rather than Hassan's Kasan/Günkondu, which may have been too small to appear. The same map also shows Melken south of Sivan Maaden, strengthening the Melêkang/Melekan = Sarıbudak comparison, and a Schel/Schel-like label near Gjaurköi northeast of Hani.",
        "https://gallica.bnf.fr/ark:/12148/btv1b531026744 ; https://commons.wikimedia.org/wiki/Category:Karte_von_Armenien,_Kurdistan_und_Azerbeidschan_in_vier_Blatt,_im_Anschluss_an_die_IV_westlichen_und_mittleren_Bl%C3%A4tter_der_Karte_von_Klein-Asien_-_entworfen_und_bearbeitet_1852-53_von_Dr_Heinrich_Kiepert_-_btv1b531026744",
    ),
    (
        "Nyêrib / Nerib / Kuyular and Hyêni / Hani",
        "Jelle Verheij's 19th-century place-name index and Taylor 1865 annotation identify Nerib with Kuyular in Hani district and align Khini/Heyni with Hani.",
        "https://www.jelleverheij.net/research-tools/place-name-index/diyarbakir.html ; https://www.jelleverheij.net/sources/1861---1870/Taylor-1865/Taylor-1865-038.html",
    ),
    (
        "Temir Beg / Timur Bey of Hani",
        "The yurtluk-ocaklık dissertation quotes an 1835 document naming Timur Bey as Hani emin; Brant's 1838 journey report says Khiní was under Temir Beg, then in exile at Adrianople; the Zirki Beylikleri study says Timur Bey was defeated in 1835 and sent with others to Istanbul/Edirne.",
        "https://digitalarchive.library.bogazici.edu.tr/bitstreams/02a6dfc7-77e0-41f8-913c-4fcab780ef94/download ; https://fundamentalarmenology.am/datas/pdfs/528.pdf ; https://www.kurdolojiakademi.net/wp-content/uploads/2021/11/Zirki-Beylikleri-1.pdf",
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
                    "follow_up": row.follow_up or "none",
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

    lines.extend(["", "## External Source Notes", ""])
    for label, note, url in EXTERNAL_SOURCE_NOTES:
        lines.append(f"- **{label}:** {note} Source: {url}")

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
            "1. Keep Temir Beg / Timur Bey of Hani as a working identification until an Ottoman document or independent local source directly ties Lerch's Temir Beg house to the same person.",
            "2. Continue resolving the Sivan village list against modern place names, prioritizing Gewel, Talek, Kavare, Gowman, Hoena, Sama, Emera, Akeragi, Letan, and Gahar.",
            "3. Split the raw village list from the Hassan interview into individually researched place entries once enough modern matches are known.",
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
