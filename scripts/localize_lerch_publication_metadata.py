"""Add English/German publication metadata to the Lerch text payloads.

The WordPress post title stays Turkish for now, but LL Tools reads these
localized payload fields at render time according to the active site locale.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_ROOT = ROOT / "texts" / "lerch"

COLLECTION_LABELS = {
    "tr": "Peter Lerch Metinleri",
    "en": "Peter Lerch Texts",
    "de": "Peter-Lerch-Texte",
}

LOCALIZED = {
    "kauge-nyerib-u-sivani": {
        "titles": {
            "tr": "Nyêrib ve Sivan'ın Kavgası",
            "en": "The Feud Between Nyêrib and Sivan",
            "de": "Die Fehde zwischen Nyêrib und Sivan",
        },
        "publication": {
            "public_summary_en": "A feud story that begins when a young man from Nyêrib steals in Horsig and is killed, then moves through threats, battle, and eventual reconciliation between Xalef Agha and Avdulah Agha.",
            "public_summary_de": "Eine Fehde-Erzählung, die damit beginnt, dass ein junger Mann aus Nyêrib in Horsig stiehlt und getötet wird; danach folgen Drohungen, Kampf und schließlich Versöhnung zwischen Xalef Agha und Avdulah Agha.",
            "content_warning_en": "violence; death",
            "content_warning_de": "Gewalt; Tod",
            "people_en": "Xalef Agha; Avdulah Agha; Mela Ahmed/Qafon; Huseyin; Hayder Agha; Sele.",
            "people_de": "Xalef Agha; Avdulah Agha; Mela Ahmed/Qafon; Huseyin; Hayder Agha; Sele.",
            "places_en": "Nyêrib/Nerib/Kuyular; Sivan/Servi; Horsig/Horsik/Saklıca; Deştê Henzi; Şeynan; Hêni/Hyêni/Hani; Kelan.",
            "places_de": "Nyêrib/Nerib/Kuyular; Sivan/Servi; Horsig/Horsik/Saklıca; Deştê Henzi; Şeynan; Hêni/Hyêni/Hani; Kelan.",
            "historical_context_en": "This narrative connects local conflict memory along the Sivan/Servi-Palu line with the Nyêrib/Hani line. Horsig is very probably the place listed as Horsik among Sivan villages, today's Saklıca. Xalef Agha is warned in the text that he already fought in Hyêni, which places this story after the Nyêrib-Hyêni feud; a reasonable working date range is roughly 1820-1853.",
            "historical_context_de": "Diese Erzählung verbindet lokale Konflikterinnerungen der Linie Sivan/Servi-Palu mit der Linie Nyêrib/Hani. Horsig ist sehr wahrscheinlich der in Sivan-Dorflisten als Horsik belegte Ort, das heutige Saklıca. Im Text wird Xalef Agha daran erinnert, dass er bereits in Hyêni gekämpft habe; dadurch steht diese Erzählung nach der Nyêrib-Hyêni-Fehde. Als Arbeitsdatierung eignet sich ungefähr 1820-1853.",
            "editorial_note_en": "The identifications Sivan/Servi, Horsig/Horsik/Saklıca, and Nyêrib/Nerib/Kuyular are externally supported. Şelê fits better with the Şelli/Turalı villages on the Hani side, and Kiepert's map also shows a Schel-like name northeast of Hani near Gjaurköi. For Kelan the strongest current candidate is Kelahsı/Kelaxsi in Sivan village lists, today's Doğanlı; Tawricyê remains uncertain.",
            "editorial_note_de": "Die Zuordnungen Sivan/Servi, Horsig/Horsik/Saklıca und Nyêrib/Nerib/Kuyular sind durch externe Quellen gestützt. Şelê passt am besten zu den Dörfern Şelli/Turalı auf der Hani-Seite; auch Kieperts Karte zeigt nordöstlich von Hani bei Gjaurköi einen Schel-ähnlichen Namen. Für Kelan ist der derzeit stärkste Kandidat Kelahsı/Kelaxsi in Sivan-Dorflisten, das heutige Doğanlı; Tawricyê bleibt unsicher.",
        },
    },
    "kauge-nyerib-u-hyeni": {
        "titles": {
            "tr": "Nyêrib ile Hyêni'nin Kavgası",
            "en": "The Feud Between Nyêrib and Hyêni",
            "de": "Die Fehde zwischen Nyêrib und Hyêni",
        },
        "publication": {
            "public_summary_en": "A feud story beginning with a man from Nyêrib killing a servant on Hyêni land, escalating into a battle between Xalef Agha and Daqma Bey, and ending through mediation by the Ziriki aghas.",
            "public_summary_de": "Eine Fehde-Erzählung, die damit beginnt, dass ein Mann aus Nyêrib auf Hyêni-Gebiet einen Diener tötet; daraus entsteht ein Kampf zwischen Xalef Agha und Daqma Bey, der durch Vermittlung der Ziriki-Aghas endet.",
            "content_warning_en": "violence; death",
            "content_warning_de": "Gewalt; Tod",
            "people_en": "Xalef Agha; Daqma Bey; Temir Beg; Mela Haseynê Mûğara; Wesman Agha; Mêhmêt Agha; Ziriki aghas; Bayraktar.",
            "people_de": "Xalef Agha; Daqma Bey; Temir Beg; Mela Haseynê Mûğara; Wesman Agha; Mêhmêt Agha; Ziriki-Aghas; Bayraktar.",
            "places_en": "Nyêrib/Nerib/Kuyular; Hyêni/Hêni/Hani/Khini; Dawz; Little Nyêrib; Deştê Henzi; Ziriki.",
            "places_de": "Nyêrib/Nerib/Kuyular; Hyêni/Hêni/Hani/Khini; Dawz; Klein-Nyêrib; Deştê Henzi; Ziriki.",
            "historical_context_en": "Hyêni/Hêni corresponds to Hani/Khini in outside sources, and Nyêrib/Nerib corresponds to Kuyular/Nerib in nineteenth-century place-name material for Hani. The army gathering in front of Temir Beg's house is important: this is most likely Timur/Temir Bey, documented as a Hani notable in 1819, as Hani emin in 1835, and exiled after defeat that same year. This points to a likely event window of 1819-1835.",
            "historical_context_de": "Hyêni/Hêni entspricht in externen Quellen Hani/Khini, und Nyêrib/Nerib entspricht Kuyular/Nerib in Ortsnamenmaterial des 19. Jahrhunderts für Hani. Wichtig ist die Versammlung des Heeres vor Temir Begs Haus: Gemeint ist sehr wahrscheinlich Timur/Temir Bey, der 1819 als Hani-Notable, 1835 als Emin von Hani belegt ist und nach seiner Niederlage im selben Jahr verbannt wurde. Das spricht für einen wahrscheinlichen Zeitraum von 1819-1835.",
            "editorial_note_en": "The Nyêrib/Kuyular and Hyêni/Hani identifications are externally supported. Little Nyêrib probably refers to a smaller settlement in the Nêrib village cluster around Hani; Dûzê Hemyê appears to be a plain or locality in the same area.",
            "editorial_note_de": "Die Zuordnungen Nyêrib/Kuyular und Hyêni/Hani sind durch externe Quellen gestützt. Klein-Nyêrib bezeichnet wahrscheinlich eine kleinere Siedlung im Nêrib-Dorfverband um Hani; Dûzê Hemyê wirkt wie eine Ebene oder Flurbezeichnung in derselben Gegend.",
        },
    },
    "ali-agha-ladi-kelhani": {
        "titles": {
            "tr": "Kelhan'ın Oğlu Ali Ağa",
            "en": "Ali Agha, Son of Kelhan",
            "de": "Ali Agha, Sohn Kelhans",
        },
        "publication": {
            "public_summary_en": "A feud story about Ali Agha, son of Kelhan, his power around Karbegan, the trap set by Qasım Agha and Weşinli Hasan Agha, the killing of Ali Agha's family, and the burial of the dead.",
            "public_summary_de": "Eine Fehde-Erzählung über Ali Agha, Sohn Kelhans, seine Macht im Raum Karbegan, die Falle von Qasım Agha und Weşinli Hasan Agha, die Tötung von Ali Aghas Familie und die Bestattung der Toten.",
            "content_warning_en": "violence; death",
            "content_warning_de": "Gewalt; Tod",
            "people_en": "Ali Agha; Qasım Agha; Weşinli Hasan Agha; Ahmed; Eysan; Mela Qasım; Ramedan Agha; Memed Agha; Hasan Kalan; Mela Resa.",
            "people_de": "Ali Agha; Qasım Agha; Weşinli Hasan Agha; Ahmed; Eysan; Mela Qasım; Ramedan Agha; Memed Agha; Hasan Kalan; Mela Resa.",
            "places_en": "Karbegan/Karabegan; Narbêş; Syeraçur; Sivan/Servi; Weşin; Desmun; Merzyelê; Ğêytê.",
            "places_de": "Karbegan/Karabegan; Narbêş; Syeraçur; Sivan/Servi; Weşin; Desmun; Merzyelê; Ğêytê.",
            "historical_context_en": "This text reflects local power relations around Karbegan/Karabegan and Sivan/Servi. The 1870-1871 Diyarbakır salname mentions the Karabegan nahiye together with villages attached to Sivan, supporting a Palu-Genç/Servi historical geography for Karbegan. The story is published here as part of the Zaza material Lerch collected from prisoners of war in Roslavl in 1856.",
            "historical_context_de": "Dieser Text spiegelt lokale Machtverhältnisse um Karbegan/Karabegan und Sivan/Servi wider. Das Diyarbakır-Salname von 1870-1871 nennt die Nahiye Karabegan zusammen mit Dörfern, die Sivan zugeordnet sind; das stützt eine historische Geographie Palu-Genç/Servi für Karbegan. Die Erzählung wird hier als Teil des Zaza-Materials veröffentlicht, das Lerch 1856 in Roslavl von Kriegsgefangenen sammelte.",
            "editorial_note_en": "The names Narbêş, Syeraçur, Desmun, Merzyelê, and Ğêytê show the local geography of the narrative; the Karbegan/Karabegan and Sivan/Servi connection is also supported by outside sources.",
            "editorial_note_de": "Die Namen Narbêş, Syeraçur, Desmun, Merzyelê und Ğêytê zeigen die lokale Geographie der Erzählung; die Verbindung Karbegan/Karabegan und Sivan/Servi wird auch durch externe Quellen gestützt.",
        },
    },
    "gespraech-mit-hassan": {
        "titles": {
            "tr": "Hassan ile Söyleşi",
            "en": "Conversation with Hassan",
            "de": "Gespräch mit Hassan",
        },
        "publication": {
            "public_summary_en": "A short question-and-answer conversation with Hassan about the villages of the Sivan tribe, Kasan/Kassau/Kaschan, gardens, highland life, and feuds he had witnessed.",
            "public_summary_de": "Ein kurzes Frage-Antwort-Gespräch mit Hassan über die Dörfer des Sivan-Stammes, Kasan/Kassau/Kaschan, Gärten, Sommerweiden und Fehden, die er gesehen hatte.",
            "content_warning_en": "",
            "content_warning_de": "",
            "people_en": "Hassan; Avdula Beg; Mistefa Ali; Ali Beg Aldun; Ahmed Beg.",
            "people_de": "Hassan; Avdula Beg; Mistefa Ali; Ali Beg Aldun; Ahmed Beg.",
            "places_en": "Sivan/Servi; Kasan/Kassau/Kaschan/Günkondu; Gewel/Gevil; Aldun/Alaaddin; Talek; Weşin; Karbegan/Karabegan; Hyêni/Hêni/Hani; Nyêrib/Nerib/Kuyular; Kavare; Gowman.",
            "places_de": "Sivan/Servi; Kasan/Kassau/Kaschan/Günkondu; Gewel/Gevil; Aldun/Alaaddin; Talek; Weşin; Karbegan/Karabegan; Hyêni/Hêni/Hani; Nyêrib/Nerib/Kuyular; Kavare; Gowman.",
            "historical_context_en": "This conversation gives the most direct information about Hassan, Lerch's main Zaza source. Hassan's Sivan framework matches the region that appears in the 1841 Palu population register as a 42-village Sivan nahiye and was later attached to Genç and known as Servi. The working identification for Kasan/Kassau/Kaschan is today's Günkondu, listed as Kasan/Kasun in Sivan village lists.",
            "historical_context_de": "Dieses Gespräch liefert die direktesten Informationen über Hassan, Lerchs wichtigsten Zaza-Gewährsmann. Hassans Sivan-Rahmen passt zu der Region, die im Palu-Bevölkerungsregister von 1841 als Sivan-Nahiye mit 42 Dörfern erscheint und später Genç zugeordnet wurde und als Servi bekannt war. Die Arbeitsidentifikation für Kasan/Kassau/Kaschan ist das heutige Günkondu, das in Sivan-Dorflisten als Kasan/Kasun erscheint.",
            "editorial_note_en": "The spelling Hassan/Hasan follows Lerch's form. Kasan/Günkondu, Horsik/Saklıca, Aldun/Alaaddin, and Hêmek/Hamek/Yeniler are supported by sources; Weşin, Talek, Kavare, and Gowman document additional local geography. The name Melken on Kiepert's map strengthens the Melêkang/Melekan = Sarıbudak identification.",
            "editorial_note_de": "Die Schreibung Hassan/Hasan folgt Lerchs Form. Kasan/Günkondu, Horsik/Saklıca, Aldun/Alaaddin und Hêmek/Hamek/Yeniler sind quellenmäßig gestützt; Weşin, Talek, Kavare und Gowman dokumentieren weitere lokale Geographie. Der Name Melken auf Kieperts Karte stärkt die Identifikation Melêkang/Melekan = Sarıbudak.",
        },
    },
    "degirmenci-ve-tilki": {
        "titles": {
            "tr": "Değirmenci ve Tilki",
            "en": "The Miller and the Fox",
            "de": "Der Müller und der Fuchs",
        },
        "publication": {
            "public_summary_en": "A tale in which a fox is caught stealing the miller's flour and tries to save his life by promising to marry the miller to the daughter of the Pasha of Egypt. The story turns on trickery, invented identity, and negotiation.",
            "public_summary_de": "Ein Märchen, in dem ein Fuchs beim Diebstahl von Mehl beim Müller erwischt wird und sein Leben retten will, indem er verspricht, den Müller mit der Tochter des Paschas von Ägypten zu verheiraten. Die Erzählung dreht sich um List, erfundene Identität und Verhandlung.",
            "content_warning_en": "",
            "content_warning_de": "",
            "people_en": "",
            "people_de": "",
            "places_en": "Egypt.",
            "places_de": "Ägypten.",
            "historical_context_en": "",
            "historical_context_de": "",
            "editorial_note_en": "The bracketed passage on MF03 was left untranslated by Lerch; the published meaning here is inferred from the Zaza text analysis and narrative context.",
            "editorial_note_de": "Die in MF03 geklammerte Passage blieb bei Lerch unübersetzt; die hier veröffentlichte Bedeutung wird aus der Analyse des Zaza-Textes und aus dem Erzählkontext erschlossen.",
        },
    },
    "uc-kardes-masali": {
        "titles": {
            "tr": "Üç Kardeş Masalı",
            "en": "The Tale of the Three Brothers",
            "de": "Märchen von den drei Brüdern",
        },
        "publication": {
            "public_summary_en": "A tale about three brothers named Hasanek, Qasım, and Şaban, their encounter with a dev, Hasanek's trick of changing the letters, and the eventual killing of the dev.",
            "public_summary_de": "Ein Märchen von drei Brüdern namens Hasanek, Qasım und Şaban, ihrer Begegnung mit einem Dev, Hasaneks List beim Vertauschen der Briefe und der schließlichen Tötung des Devs.",
            "content_warning_en": "violence; adult theme",
            "content_warning_de": "Gewalt; erwachsenes Thema",
            "people_en": "",
            "people_de": "",
            "places_en": "",
            "places_de": "",
            "historical_context_en": "",
            "historical_context_de": "",
            "editorial_note_en": "",
            "editorial_note_de": "",
        },
    },
    "goin-puhu-kusunun-hikayesi": {
        "titles": {
            "tr": "Go'in / Puhu Kuşunun Hikayesi",
            "en": "The Story of the Go'in Bird",
            "de": "Die Geschichte vom Go'in-Vogel",
        },
        "publication": {
            "public_summary_en": "A girl dreams of the brother killed by her stepmother; after conflict within the family, she asks God to turn her into the go'in bird.",
            "public_summary_de": "Ein Mädchen träumt von ihrem Bruder, den ihre Stiefmutter getötet hat; nach einem Konflikt in der Familie bittet sie Gott, sie in den Go'in-Vogel zu verwandeln.",
            "content_warning_en": "violence; child death",
            "content_warning_de": "Gewalt; Tod eines Kindes",
            "people_en": "",
            "people_de": "",
            "places_en": "",
            "places_de": "",
            "historical_context_en": "",
            "historical_context_de": "",
            "editorial_note_en": "",
            "editorial_note_de": "",
        },
    },
    "bacmeister-ornek-cumleleri": {
        "titles": {
            "tr": "Bacmeister Örnek Cümleleri",
            "en": "Bacmeister Sample Sentences",
            "de": "Bacmeisters Beispielsätze",
        },
        "publication": {
            "public_summary_en": "Forty-four short Kurmanji and Zaza sample sentences that Lerch produced from Bacmeister's language examples. The Zaza column preserves Lerch's historical phonetic transcription.",
            "public_summary_de": "Vierundvierzig kurze Kurmandschi- und Zaza-Beispielsätze, die Lerch aus Bacmeisters Sprachbeispielen erstellte. Die Zaza-Spalte bewahrt Lerchs historische phonetische Transkription.",
            "content_warning_en": "",
            "content_warning_de": "",
            "people_en": "",
            "people_de": "",
            "places_en": "",
            "places_de": "",
            "historical_context_en": "This section is not a narrative text, but a set of short sample sentences. Lerch explains that he first translated Bacmeister's examples into Turkish and then asked Kurdish speakers for the Kurmanji and Zaza equivalents.",
            "historical_context_de": "Dieser Abschnitt ist kein Erzähltext, sondern eine Sammlung kurzer Beispielsätze. Lerch erklärt, dass er Bacmeisters Beispiele zuerst ins Türkische übersetzte und dann kurdische Sprecher nach den Kurmandschi- und Zaza-Entsprechungen fragte.",
            "editorial_note_en": "The Zaza sentences are given in Lerch's historical phonetic writing, not normalized to modern Zazaki orthography. Notes mark witness differences or probable spelling/transcription errors visible in the source.",
            "editorial_note_de": "Die Zaza-Sätze werden in Lerchs historischer phonetischer Schreibung wiedergegeben, nicht in moderne Zazaki-Orthographie normalisiert. Notizen markieren Zeugenunterschiede oder wahrscheinliche Schreib- bzw. Transkriptionsfehler in der Quelle.",
        },
    },
    "lerch-book-zazaki-sections": {
        "titles": {
            "tr": "Peter Lerch'in Zazaca Bölümleri",
            "en": "Peter Lerch's Zaza-Related Sections",
            "de": "Peter Lerchs zazabezogene Abschnitte",
        },
        "publication": {
            "public_summary_en": "A multilingual selection from Lerch's own book sections about the Zaza texts, his sources, his transcription system, and his glossary.",
            "public_summary_de": "Eine mehrsprachige Auswahl aus Lerchs eigenen Buchabschnitten über die Zaza-Texte, seine Gewährsleute, sein Transkriptionssystem und sein Glossar.",
            "content_warning_en": "",
            "content_warning_de": "",
            "people_en": "Peter Lerch; Hassan; B. von Dorn; Hussein.",
            "people_de": "Peter Lerch; Hassan; B. von Dorn; Hussein.",
            "places_en": "Roslavl; Palu; Sivan; Kasan/Kassau/Kaschan; Muş; Tujik/Tuzik; Dúmbeli.",
            "places_de": "Roslavl; Palu; Sivan; Kasan/Kassau/Kaschan; Muş; Tujik/Tuzik; Dúmbeli.",
            "historical_context_en": "This text brings together passages in which Lerch explains how he collected the Zaza material and why he considered the Zaza texts scientifically important.",
            "historical_context_de": "Dieser Text stellt Passagen zusammen, in denen Lerch erklärt, wie er das Zaza-Material gesammelt hat und warum er die Zaza-Texte wissenschaftlich für wichtig hielt.",
            "editorial_note_en": "This is not a narrative or interlinear text, but a multilingual reading text made from the Zaza-related explanations in the source book.",
            "editorial_note_de": "Dies ist kein Erzähl- oder Interlineartext, sondern ein mehrsprachiger Lesetext aus den zazabezogenen Erläuterungen des Quellenbuches.",
        },
    },
}


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_payload(slug: str, spec: dict) -> None:
    text_dir = TEXT_ROOT / slug
    payload_path = text_dir / "text-document.json"
    metadata_path = text_dir / "metadata.json"
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    metadata = payload.setdefault("metadata", {})
    publication = metadata.setdefault("publication", {})

    titles = spec["titles"]
    payload["titles"] = titles
    payload["excerpts"] = {
        "tr": publication.get("public_summary_tr", ""),
        "en": spec["publication"].get("public_summary_en", ""),
        "de": spec["publication"].get("public_summary_de", ""),
    }
    metadata["collection_labels"] = COLLECTION_LABELS
    metadata["excerpt"] = publication.get("public_summary_tr", metadata.get("excerpt", ""))
    metadata["excerpts"] = payload["excerpts"]

    publication["title_tr"] = titles["tr"]
    publication["title_en"] = titles["en"]
    publication["title_de"] = titles["de"]
    publication.update(spec["publication"])

    payload["metadata"] = metadata
    write_json(payload_path, payload)

    if metadata_path.exists():
        meta_doc = json.loads(metadata_path.read_text(encoding="utf-8"))
        meta_doc["title"] = titles["tr"]
        meta_doc["titles"] = titles
        meta_doc["publication"] = publication
        write_json(metadata_path, meta_doc)


def main() -> None:
    for slug, spec in LOCALIZED.items():
        update_payload(slug, spec)
    print(f"Localized {len(LOCALIZED)} Lerch text payloads.")


if __name__ == "__main__":
    main()
