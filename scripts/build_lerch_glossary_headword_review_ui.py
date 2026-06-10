#!/usr/bin/env python3
"""Build a static review UI for Lerch glossary headwords and glosses."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import fitz


REPO_ROOT = Path(__file__).resolve().parents[1]
LERCH_DIR = Path(r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch")
PDF_PATH = LERCH_DIR / "lerch glossary german.pdf"
CORRECTED_TSV = REPO_ROOT / "reports" / "lerch-glossary-corrected-layer.tsv"
REVIEW_DIR = REPO_ROOT / "reviews" / "lerch-glossary-headword-review"
ASSET_DIR = REVIEW_DIR / "assets"
ENTRY_ASSET_DIR = ASSET_DIR / "entries"
DATA_JS = REVIEW_DIR / "glossary-data.js"
INDEX_HTML = REVIEW_DIR / "index.html"
PDF_START_PAGE = 197
PDF_END_PAGE = 220


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


GLOBAL_HEADERS = {
    "II.",
    "GLOSSAR FÜR DAS IDIOM",
    "Z A Z Ä.",
}

LETTER_HEADINGS = {
    "A.",
    "B.",
    "C.",
    "D.",
    "E.",
    "F.",
    "G.",
    "G'.",
    "H'.",
    "I.",
    "J.",
    "K.",
    "L.",
    "M.",
    "N.",
    "O.",
    "P.",
    "Q.",
    "R.",
    "S.",
    "T.",
    "U.",
    "V.",
    "W.",
    "X.",
    "Y.",
    "Z.",
}

NOTE_PREFIXES = (
    "Vgl.",
    "vgl.",
    "cf.",
    "S.",
    "s.",
    "Gld:",
    "pl.",
    "auch ",
    "Vocat.",
    "a. k.",
    "a.",
)


def normalize_block(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = text.replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def is_page_number(text: str) -> bool:
    stripped = text.strip()
    if not stripped or "," in stripped:
        return False
    return bool(re.fullmatch(r"[0-9A-Za-z*»«I£()]+", stripped))


def is_header(text: str) -> bool:
    normalized = text.strip()
    lower = normalized.lower()
    if normalized in GLOBAL_HEADERS or normalized in LETTER_HEADINGS:
        return True
    if "digitized by google" in lower or "digilized by google" in lower:
        return True
    if normalized.startswith("Forsch,"):
        return True
    if lower.endswith("oogle") or lower.endswith("google •"):
        return True
    return False


def normalize_letter(text: str) -> str:
    normalized = text.strip()
    if normalized == "0.":
        return "O"
    return normalized.rstrip(".")


def is_letter_heading(text: str) -> bool:
    return text.strip() in LETTER_HEADINGS


def looks_like_entry_start(text: str) -> bool:
    if not text or is_header(text) or is_page_number(text):
        return False
    if any(text.startswith(prefix) for prefix in NOTE_PREFIXES):
        return False
    if "," not in text:
        return False
    head = text.split(",", 1)[0].strip()
    if len(head) > 40 or head.count(" ") > 4:
        return False
    if any(ch.isdigit() for ch in head):
        return False
    return bool(re.search(r"[A-Za-zÄÖÜäöüßÇçÊêÎîÛûĀāĒēĪīŌōŠšŽž]", head))


def split_multi_entry_text(text: str) -> list[str]:
    pattern = r"(?<=\.)\s+(?=[A-ZÄÖÜ][A-Za-zÄÖÜäöüßÇçÊêÎîÛûĀāĒēĪīŌōŠšŽž'’\-]+,)"
    return [part.strip() for part in re.split(pattern, text) if part.strip()]


def extract_entry_regions() -> dict[str, dict[str, object]]:
    """Return OCR-derived glossary-entry regions keyed by Lerch glossary entry id.

    The text layer is noisy, but its block coordinates are reliable enough for
    review crops. We deliberately include the whole source column and vertical
    padding so a bad segmentation still leaves neighboring context visible.
    """
    regions: dict[str, dict[str, object]] = {}
    entry_id = 1
    current: dict[str, object] | None = None

    def flush_current() -> None:
        nonlocal current, entry_id
        if not current:
            return
        boxes = current.get("boxes", [])
        if not boxes:
            current = None
            return
        x0 = min(box[0] for box in boxes)  # type: ignore[index]
        y0 = min(box[1] for box in boxes)  # type: ignore[index]
        x1 = max(box[2] for box in boxes)  # type: ignore[index]
        y1 = max(box[3] for box in boxes)  # type: ignore[index]
        regions[str(entry_id)] = {
            "page": current["page"],
            "column": current["column"],
            "bbox": [x0, y0, x1, y1],
        }
        entry_id += 1
        current = None

    with fitz.open(PDF_PATH) as doc:
        for pdf_page in range(PDF_START_PAGE, PDF_END_PAGE + 1):
            page = doc[pdf_page - 1]
            columns: dict[int, list[tuple[float, float, float, float, str]]] = {0: [], 1: []}
            for block in page.get_text("blocks"):
                x0, y0, x1, y1, raw_text, *_ = block
                text = normalize_block(raw_text)
                if not text:
                    continue
                column = 0 if x0 < 60 else 1
                columns[column].append((x0, y0, x1, y1, text))

            for column in (0, 1):
                column_blocks = columns[column]
                if not column_blocks:
                    continue
                column_blocks.sort(key=lambda item: (round(item[1], 1), item[0]))
                lexical_xs = [x0 for x0, _, _, _, text in column_blocks if looks_like_entry_start(text)]
                if not lexical_xs:
                    lexical_xs = [
                        x0
                        for x0, _, _, _, text in column_blocks
                        if not is_header(text)
                        and not is_page_number(text)
                        and not any(text.startswith(prefix) for prefix in NOTE_PREFIXES)
                    ]
                if not lexical_xs:
                    continue
                base_x = min(lexical_xs)

                for x0, y0, x1, y1, text in column_blocks:
                    if text.startswith("ZUSÄTZE, ANMERKUNGEN UND BERICHTIGUNGEN"):
                        flush_current()
                        return regions
                    if is_letter_heading(text):
                        flush_current()
                        normalize_letter(text)
                        continue
                    if is_header(text) or is_page_number(text):
                        continue

                    for index, subtext in enumerate(split_multi_entry_text(text)):
                        effective_x = x0 if index == 0 else base_x
                        if looks_like_entry_start(subtext) and effective_x <= base_x + 2:
                            flush_current()
                            current = {
                                "page": pdf_page,
                                "column": column,
                                "boxes": [(x0, y0, x1, y1)],
                            }
                        elif current:
                            current["boxes"].append((x0, y0, x1, y1))  # type: ignore[index, union-attr]
        flush_current()

    return regions


TERM_TRANSLATIONS: list[tuple[str, str, str]] = [
    ("Agha", "Agha", "Ağa"),
    ("Aga", "Agha", "Ağa"),
    ("Spiegel", "mirror", "ayna"),
    ("Wasser", "water", "su"),
    ("Quelle", "spring/source", "kaynak"),
    ("Bach", "stream", "dere"),
    ("Bier", "beer", "bira"),
    ("ziehe heraus", "I pull out", "çekip çıkarıyorum"),
    ("zog heraus", "pulled out", "çekip çıkardı"),
    ("jener", "that", "şu/o"),
    ("dieser", "this", "bu"),
    ("Monatsname", "month name", "ay adı"),
    ("Feuer", "fire", "ateş"),
    ("ruhe aus", "rest", "dinlen"),
    ("erhole dich", "recover/rest", "dinlen"),
    ("Himmel", "sky/heaven", "gök"),
    ("befreie", "I free/release", "kurtarıyorum"),
    ("Müller", "miller", "değirmenci"),
    ("Blutigel", "leech", "sülük"),
    ("Gott", "God", "Allah"),
    ("Wange", "cheek", "yanak"),
    ("Gold", "gold", "altın"),
    ("golden", "golden", "altın"),
    ("Schützling", "protégé/ward", "himaye edilen kişi"),
    ("im Sommer", "in summer", "yazın"),
    ("Oberarm", "upper arm", "üst kol"),
    ("Honig", "honey", "bal"),
    ("hierher", "here/to here", "buraya"),
    ("von hier", "from here", "buradan"),
    ("hier", "here", "burada"),
    ("Stern", "star", "yıldız"),
    ("warf", "threw", "attı"),
    ("Holz", "wood", "odun"),
    ("Kind", "child", "çocuk"),
    ("Held", "hero", "kahraman/yiğit"),
    ("Glück", "luck/fortune", "şans/baht"),
    ("ist", "is", "-dır/-dir"),
    ("bade mich", "bathe me", "beni yıka"),
    ("Bart", "beard", "sakal"),
    ("spät", "late", "geç"),
    ("komniandirte", "commanded", "komut verdi"),
    ("kommandirte", "commanded", "komut verdi"),
    ("marsch", "march", "marş/yürü"),
    ("schickte", "sent", "gönderdi"),
    ("schicke", "I send", "gönderiyorum"),
    ("Schulter", "shoulder", "omuz"),
    ("Leben", "life", "hayat/ömür"),
    ("mein Herr", "my lord/sir", "efendim"),
    ("Abend", "evening", "akşam"),
    ("Hoffnung", "hope", "umut"),
    ("Schlaf", "sleep", "uyku"),
    ("bereit", "ready", "hazır"),
    ("fertig", "ready/done", "hazır/bitmiş"),
    ("nieder", "down", "aşağı"),
    ("Postposition", "postposition", "edat"),
    ("zu, bei", "to/at/by", "-e/-de/yanında"),
    ("bis", "until", "-e kadar"),
    ("Kinn", "chin", "çene"),
    ("Bär", "bear", "ayı"),
    ("Harem", "harem", "harem"),
    ("Bad", "bath", "hamam/banyo"),
    ("Dolch", "dagger", "hançer"),
    ("sieben", "seven", "yedi"),
    ("siebzig", "seventy", "yetmiş"),
    ("siebzigste", "seventieth", "yetmişinci"),
    ("siebzehnte", "seventeenth", "on yedinci"),
    ("siebzebu", "seventeen", "on yedi"),
    ("siebente", "seventh", "yedinci"),
    ("Nest", "nest", "yuva"),
    ("Biene", "bee", "arı"),
    ("alle", "all", "hepsi"),
    ("Luft", "air", "hava"),
    ("Wind", "wind", "rüzgar"),
    ("warum", "why", "neden"),
    ("Gans", "goose", "kaz"),
    ("woher", "from where", "nereden"),
    ("wohiu", "to where", "nereye"),
    ("wohin", "to where", "nereye"),
    ("welcher", "which", "hangi"),
    ("wer", "who", "kim"),
    ("schloss sich", "closed/joined itself", "kapandı/katıldı"),
    ("springe", "I jump", "atlıyorum/sıçrıyorum"),
    ("Kampf", "fight", "kavga/savaş"),
    ("Streit", "conflict/quarrel", "kavga/anlaşmazlık"),
    ("Schlacht", "battle", "savaş"),
    ("Brief", "letter", "mektup"),
    ("Maul- thier", "mule", "katır"),
    ("Maultier", "mule", "katır"),
    ("Habicht", "hawk", "atmaca"),
    ("Messer", "knife", "bıçak"),
    ("geschlossen habend", "having closed", "kapatmış olarak"),
    ("Blei", "lead", "kurşun"),
    ("Kugel", "bullet", "kurşun"),
    ("Flamme", "flame", "alev"),
    ("kurz", "short", "kısa"),
    ("Schwerlscheide", "sword sheath", "kılıç kını"),
    ("Schwertscheide", "sword sheath", "kılıç kını"),
    ("spreche", "I speak", "konuşuyorum"),
    ("Kuckuk", "cuckoo", "guguk"),
    ("Kuckuck", "cuckoo", "guguk"),
    ("Kranich", "crane", "turna"),
    ("Braten", "roast meat", "kebap/kızartma et"),
    ("Diminutiv", "diminutive", "küçültme biçimi"),
    ("tödte", "I kill", "öldürüyorum"),
    ("tödtete", "killed", "öldürdü"),
    ("getödtet", "killed", "öldürülmüş"),
    ("Kurde", "Kurd", "Kürt"),
    ("Frosch", "frog", "kurbağa"),
    ("Eidechse", "lizard", "kertenkele"),
    ("ruhe, schlafe", "rest, sleep", "dinlen, uyu"),
    ("Taube", "dove/pigeon", "güvercin"),
    ("Nasenlöcher", "nostrils", "burun delikleri"),
    ("abschenlich", "repulsive", "iğrenç"),
    ("abscheulich", "repulsive", "iğrenç"),
    ("Kohle", "coal", "kömür"),
    ("mache", "make/do", "yap"),
    ("klopfe", "I knock", "vuruyorum/çarpıyorum"),
    ("Feld", "field", "tarla/alan"),
    ("Acker", "field/acre", "tarla"),
    ("Fell", "hide/pelt", "post/kürk"),
    ("Pelz", "fur", "kürk"),
    ("beisse", "bite", "ısır"),
    ("gehe", "I go", "gidiyorum"),
    ("Mal", "time/occasion", "kez/defa"),
    ("Haar", "hair", "saç/kıl"),
    ("Ast", "branch", "dal"),
    ("Kalb", "calf", "buzağı"),
    ("Knöchel", "ankle", "ayak bileği"),
    ("Tanz", "dance", "dans/oyun"),
    ("Kälberweide", "calf pasture", "buzağı merası"),
    ("wann", "when", "ne zaman"),
    ("vierzigste", "fortieth", "kırkıncı"),
    ("vierzig", "forty", "kırk"),
    ("vierzehnte", "fourteenth", "on dördüncü"),
    ("vierzehn", "fourteen", "on dört"),
    ("Schienbein", "shin", "kaval kemiği"),
    ("Fledermaus", "bat", "yarasa"),
    ("Stirn", "forehead", "alın"),
    ("Mittwoch", "Wednesday", "çarşamba"),
    ("Markt", "market", "pazar"),
    ("wie viel", "how much/how many", "ne kadar/kaç"),
    ("vierte", "fourth", "dördüncü"),
    ("Pistole", "pistol", "tabanca"),
    ("Speise", "food", "yemek/yiyecek"),
    ("Brust", "breast/chest", "göğüs"),
    ("n. pr.", "proper name", "özel ad"),
    ("Chirurg", "surgeon", "cerrah"),
    ("Gerste", "barley", "arpa"),
    ("bitter", "bitter", "acı"),
    ("Antwort", "answer", "cevap"),
    ("antworte", "I answer", "cevap veriyorum"),
    ("nicht", "not", "değil/-me"),
    ("waren nicht", "were not", "değildi/değillerdi"),
    ("Heimchen", "cricket", "cırcır böceği"),
    ("Stab", "staff/stick", "sopa/değnek"),
    ("Säugling", "infant", "bebek"),
    ("Leiche", "corpse", "ceset"),
    ("pfeife", "I whistle", "ıslık çalıyorum"),
    ("Pflug", "plough", "saban"),
    ("Pfluggespaun", "plough team", "saban takımı"),
    ("pflüge", "I plough", "sürüyorum"),
    ("einst", "once/formerly", "bir zamanlar"),
    ("Grube", "pit", "çukur"),
    ("schrieb nicht", "did not write", "yazmadı"),
    ("höre nicht", "I do not hear", "duymuyorum"),
    ("hörte nicht", "did not hear", "duymadı"),
    ("Appellativ", "appellative/demonym", "adlandırma/nisbe"),
    ("eilf", "eleven", "on bir"),
    ("eilfte", "eleventh", "on birinci"),
    ("erste", "first", "birinci"),
    ("längst", "long ago/already", "çoktan"),
    ("Ring am Finger", "finger ring", "yüzük"),
    ("Fehde", "feud", "kan davası/kavga"),
    ("Türke", "Turk", "Türk"),
    ("Frucht", "fruit", "meyve"),
    ("Schein", "shine/appearance", "parıltı/görünüş"),
    ("Glanz", "shine/splendor", "parıltı"),
    ("Talisman", "talisman", "tılsım"),
    ("sammelte", "gathered", "topladı"),
    ("versammelte", "assembled/gathered", "topladı/bir araya getirdi"),
    ("Hagel", "hail", "dolu"),
    ("Flinte", "rifle/gun", "tüfek"),
    ("Maulbeerbaum", "mulberry tree", "dut ağacı"),
    ("reisse aus", "tear out", "kopar"),
    ("schlage ab", "cut/strike off", "kes/kopar"),
    ("riss ab", "tore off", "kopardı"),
    ("schlug ab", "cut/struck off", "kesti/kopardı"),
    ("Trommel", "drum", "davul"),
    ("gebe", "I give", "veriyorum"),
    ("zehnte", "tenth", "onuncu"),
    ("geschieht", "happens", "olur"),
    ("Waschung", "washing/ablution", "yıkanma/abdest"),
    ("verborgen", "hidden", "gizli"),
    ("heimlich", "secretly/hidden", "gizlice/gizli"),
    ("zweite", "second", "ikinci"),
    ("Flöte", "flute", "flüt/kaval"),
    ("zwölfte", "twelfth", "on ikinci"),
    ("zwölf", "twelve", "on iki"),
    ("Höhle", "cave", "mağara"),
    ("Nagel", "nail", "tırnak/çivi"),
    ("Grossmutier", "grandmother", "büyükanne"),
    ("Grossmutter", "grandmother", "büyükanne"),
    ("Waud", "wall", "duvar"),
    ("Wand", "wall", "duvar"),
    ("jetzt", "now", "şimdi"),
    ("bückten sich", "bent down", "eğildiler"),
    ("nah", "near", "yakın"),
    ("Gebet", "prayer", "namaz/dua"),
    ("zart", "tender/delicate", "nazik/körpe"),
    ("Faust", "fist", "yumruk"),
    ("Stadt", "city", "şehir"),
    ("Regenwurm", "earthworm", "solucan"),
    ("fremd", "foreign/strange", "yabancı"),
    ("sechszig", "sixty", "altmış"),
    ("scchszigste", "sixtieth", "altmışıncı"),
    ("sechszehute", "sixteenth", "on altıncı"),
    ("sechste", "sixth", "altıncı"),
    ("sechs", "six", "altı"),
    ("Gitterfenster", "lattice window", "kafesli pencere"),
    ("Gitterthür", "lattice door", "kafesli kapı"),
    ("gingen", "went", "gittiler"),
    ("Weinmoost", "grape must", "şıra"),
    ("Löwe", "lion", "aslan"),
    ("hart", "hard", "sert"),
    ("fest", "firm/solid", "sağlam"),
    ("gegen", "against/toward", "karşı/-e doğru"),
    ("Zazd", "Zaza", "Zaza"),
    ("Gefängniss", "prison", "hapishane"),
    ("Sattel", "saddle", "eyer"),
    ("Knabe", "boy", "oğlan/erkek çocuk"),
    ("Sommerlager", "summer pasture", "yayla"),
    ("Zunge", "tongue", "dil"),
    ("lief", "ran", "koştu"),
    ("floh", "fled", "kaçtı"),
    ("Rede", "speech/word", "söz/konuşma"),
    ("warte", "I wait", "bekliyorum"),
    ("koche", "I cook", "pişiriyorum"),
    ("fünfzigste", "fiftieth", "ellinci"),
    ("fünfzehnte", "fifteenth", "on beşinci"),
    ("fünfzehn", "fifteen", "on beş"),
    ("fünfte", "fifth", "beşinci"),
    ("fünf", "five", "beş"),
    ("Bein", "leg", "bacak"),
    ("Jacke", "jacket", "ceket"),
    ("Vieh", "livestock", "hayvan/sürü"),
    ("mit", "with", "ile"),
    ("darauf", "after that/thereupon", "sonra/bunun üzerine"),
    ("nachher", "afterward", "sonra"),
    ("folgte", "followed", "takip etti"),
    ("verfolgte", "pursued", "kovaladı"),
    ("Feder", "feather", "tüy"),
    ("Katze", "cat", "kedi"),
    ("Hemd", "shirt", "gömlek"),
    ("frage", "I ask", "soruyorum"),
    ("blase", "blow", "üfle"),
    ("Bauch", "belly", "karın"),
    ("Unterleib", "lower abdomen", "alt karın"),
    ("neunzigste", "ninetieth", "doksanıncı"),
    ("neunzig", "ninety", "doksan"),
    ("neun", "nine", "dokuz"),
    ("Schnabel", "beak", "gaga"),
    ("Apfelbaum", "apple tree", "elma ağacı"),
    ("was", "what", "ne"),
    ("Käse", "cheese", "peynir"),
    ("Flügel", "wing", "kanat"),
    ("Spinne", "spider", "örümcek"),
    ("viel", "much/many", "çok"),
    ("Pilav", "pilaf", "pilav"),
    ("zusammen", "together", "birlikte"),
    ("Armband", "bracelet", "bilezik"),
    ("lasse los", "let go/release", "bırak"),
    ("dünn", "thin", "ince"),
    ("Kissen", "pillow", "yastık"),
    ("getragen", "carried/worn", "taşınmış/giyilmiş"),
    ("hoch", "high", "yüksek"),
    ("erhöhe", "I raise", "yükseltiyorum"),
    ("weinte", "wept", "ağladı"),
    ("weine", "I weep", "ağlıyorum"),
    ("Standartenträger", "standard-bearer", "sancaktar"),
    ("drang vor", "advanced/pressed forward", "ileri atıldı"),
    ("dringet vor", "advance", "ileri atılın"),
    ("bringe", "bring", "getir"),
    ("ohne", "without", "olmadan/-sız"),
    ("wir", "we", "biz"),
    ("Ruh", "rest/peace", "rahat/huzur"),
    ("Fisch", "fish", "balık"),
    ("heirathete", "married", "evlendi"),
    ("Machal", "quarter/district", "mahalle"),
    ("Kupferschale", "copper bowl", "bakır tas"),
    ("gestorben", "died", "öldü/ölmüş"),
    ("sterbe", "I die", "ölüyorum"),
    ("Fliege", "fly", "sinek"),
    ("Leichnam", "corpse", "ceset"),
    ("Affe", "monkey", "maymun"),
    ("hielt Rath", "held council", "meşveret etti"),
    ("Birne", "pear", "armut"),
    ("Mullah", "mullah", "molla"),
    ("mir", "to me/me", "bana/beni"),
    ("meine", "my/mine", "benim"),
    ("Fürst", "prince/ruler", "bey/hükümdar"),
    ("Sperling", "sparrow", "serçe"),
    ("gleich", "same/equal/immediately", "aynı/hemen"),
    ("Euphrat", "Euphrates", "Fırat"),
    ("fliege", "I fly", "uçuyorum"),
    ("Ausrufung", "exclamation", "ünlem"),
    ("Regenbo", "rainbow", "gökkuşağı"),
    ("Maus", "mouse", "fare"),
    ("Maulwurf", "mole", "köstebek"),
    ("Blindmaus", "blind mole-rat", "kör fare"),
    ("Ofen", "oven", "fırın"),
    ("Bäcker", "baker", "fırıncı"),
    ("Elephant", "elephant", "fil"),
    ("Schnee", "snow", "kar"),
    ("Lamm", "lamb", "kuzu"),
    ("Kegen", "rain", "yağmur"),
    ("Regen", "rain", "yağmur"),
    ("regnete", "rained", "yağdı"),
    ("brenne", "burn", "yanıyorum"),
    ("brannte", "burned", "yandı"),
    ("Blätter", "leaves", "yapraklar"),
    ("Laub", "foliage", "yaprak"),
    ("er, sie", "he/she/it", "o"),
    ("wünschte", "wished", "istedi/diledi"),
    ("Zeit", "time", "zaman"),
    ("zwanzigste", "twentieth", "yirminci"),
    ("zwanzig", "twenty", "yirmi"),
    ("Blümchen", "little flower", "çiçekçik"),
    ("Winterlager", "winter quarters", "kışlak"),
    ("dort", "there", "orada"),
    ("der, die, das andere", "the other", "öteki/diğer"),
    ("auch du", "you too", "sen de"),
    ("sein, seine", "his/its", "onun"),
    ("ihr, ihre", "her/their", "onun/onların"),
    ("noch", "still/yet/more", "hâlâ/daha"),
    ("gegeu", "against/toward", "karşı/-e doğru"),
    ("zu.", "to", "-e/-a"),
    ("Greis", "old man", "ihtiyar"),
    ("einige", "some", "bazı"),
    ("wenn", "if", "eğer"),
    ("sobald", "as soon as", "olur olmaz"),
    ("sogleich", "immediately", "hemen"),
    ("sehe", "I see", "görüyorum"),
    ("sahen", "they saw", "gördüler"),
    ("sah", "saw", "gördü"),
    ("sieh", "look", "bak"),
    ("schau zu", "look/watch", "bak/seyret"),
    ("seht", "look", "bakın"),
    ("Mensch", "person/human", "insan"),
    ("Mann", "man", "adam/erkek"),
    ("Frau", "woman", "kadın"),
    ("Sohn", "son", "oğul"),
    ("Tochter", "daughter", "kız evlat"),
    ("Vater", "father", "baba"),
    ("Mutter", "mother", "anne"),
    ("Bruder", "brother", "erkek kardeş"),
    ("Haus", "house", "ev"),
    ("Dorf", "village", "köy"),
    ("Name", "name", "ad"),
    ("Pferd", "horse", "at"),
    ("Schaf", "sheep", "koyun"),
    ("Fuchs", "fox", "tilki"),
    ("Hase", "hare/rabbit", "tavşan"),
    ("Hund", "dog", "köpek"),
    ("Brot", "bread", "ekmek"),
    ("Mehl", "flour", "un"),
    ("Salz", "salt", "tuz"),
    ("Milch", "milk", "süt"),
    ("Hand", "hand", "el"),
    ("Fuss", "foot", "ayak"),
    ("Kopf", "head", "baş"),
    ("Auge", "eye", "göz"),
    ("Ohr", "ear", "kulak"),
    ("Mund", "mouth", "ağız"),
    ("Zahn", "tooth", "diş"),
    ("Blut", "blood", "kan"),
    ("Stein", "stone", "taş"),
    ("Berg", "mountain", "dağ"),
    ("Weg", "road/way", "yol"),
    ("Tag", "day", "gün"),
    ("Nacht", "night", "gece"),
    ("Jahr", "year", "yıl"),
]


OTTOMAN_NOTES = {
    "1": {
        "german": "(Osmanisch-Türkisch: آینه/ayna) Spiegel",
        "english": "(Ottoman Turkish: آینه/ayna) mirror",
        "turkish": "(Osmanlıca: آینه) ayna",
    },
    "10": {
        "headword": "áγa",
        "modern": "ağa",
        "group": "ağa",
        "german": "(Osmanisch-Türkisch: اغا/ağa) Agha",
        "english": "(Ottoman Turkish: اغا/ağa) Agha",
        "turkish": "(Osmanlıca: اغا) Ağa",
    },
    "34": {
        "german": "(Osmanisch-Türkisch: التون/altun) Gold",
        "english": "(Ottoman Turkish: التون/altun) gold",
        "turkish": "(Osmanlıca: التون) altın",
    },
    "55": {
        "german": "(Osmanisch-Türkisch: يگيت/yiğit) Held",
        "english": "(Ottoman Turkish: يگيت/yiğit) hero/brave man",
        "turkish": "(Osmanlıca: يگيت) yiğit, kahraman",
    },
    "56": {
        "headword": "oγúr",
        "modern": "oğûr",
        "group": "uğur",
        "german": "(Osmanisch-Türkisch: اوغر/uğur) Glück",
        "english": "(Ottoman Turkish: اوغر/uğur) luck/fortune",
        "turkish": "(Osmanlıca: اوغر) uğur, talih",
    },
    "71": {
        "german": "(Osmanisch-Türkisch: افندم/efendim) mein Herr",
        "english": "(Ottoman Turkish: افندم/efendim) my lord/sir",
        "turkish": "(Osmanlıca: افندم) efendim",
    },
    "123": {
        "german": "(Osmanisch-Türkisch: قاطر/katır) Maultier",
        "english": "(Ottoman Turkish: قاطر/katır) mule",
        "turkish": "(Osmanlıca: قاطر) katır",
    },
    "126": {
        "german": "(Osmanisch-Türkisch: قرا قوش/kara kuş) Habicht",
        "english": "(Ottoman Turkish: قرا قوش/kara kuş) hawk",
        "turkish": "(Osmanlıca: قرا قوش) atmaca/karakuş",
    },
    "129": {
        "german": "(Osmanisch-Türkisch: قورشن/kurşun) Blei, Kugel",
        "english": "(Ottoman Turkish: قورشن/kurşun) lead; bullet",
        "turkish": "(Osmanlıca: قورشن) kurşun",
    },
    "168": {
        "german": "(Osmanisch-Türkisch: كومور/kömür) Kohle",
        "english": "(Ottoman Turkish: كومور/kömür) coal",
        "turkish": "(Osmanlıca: كومور) kömür",
    },
    "292": {
        "headword": "dahā́",
        "modern": "daha",
        "group": "daha",
        "german": "(Osmanisch-Türkisch: دخى/dahi) noch",
        "english": "(Ottoman Turkish: دخى/dahi) still/yet/more",
        "turkish": "(Osmanlıca: دخى) dahi/daha",
    },
    "577": {
        "german": "(Osmanisch-Türkisch: اوطه/oda) Zimmer",
        "english": "(Ottoman Turkish: اوطه/oda) room",
        "turkish": "(Osmanlıca: اوطه) oda",
    },
}


def auto_translate_gloss(german: str) -> tuple[str, str]:
    found_en: list[str] = []
    found_tr: list[str] = []
    for needle, english, turkish in TERM_TRANSLATIONS:
        if needle.lower() in german.lower():
            if english not in found_en:
                found_en.append(english)
            if turkish not in found_tr:
                found_tr.append(turkish)
    return "; ".join(found_en), "; ".join(found_tr)


def prepare_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    prepared: list[dict[str, str]] = []
    for row in rows:
        item = dict(row)
        note = OTTOMAN_NOTES.get(item.get("row_id", ""))
        if note:
            if note.get("headword"):
                item["corrected_lerch_headword"] = note["headword"]
            if note.get("modern"):
                item["modern_zazaki_guess"] = note["modern"]
            if note.get("group"):
                item["proposed_group_headword"] = note["group"]
            item["german_gloss_clean"] = note["german"]
            item["english_gloss"] = note["english"]
            item["english_gloss_source"] = "auto_ottoman_note"
            item["turkish_gloss"] = note["turkish"]
            item["turkish_gloss_source"] = "auto_ottoman_note"
        else:
            english, turkish = auto_translate_gloss(item.get("german_gloss_clean", ""))
            if english and not item.get("english_gloss"):
                item["english_gloss"] = english
                item["english_gloss_source"] = "auto_from_german_gloss"
            if turkish and not item.get("turkish_gloss"):
                item["turkish_gloss"] = turkish
                item["turkish_gloss_source"] = "auto_from_german_gloss"
        prepared.append(item)
    return prepared


def render_page_assets(rows: list[dict[str, str]]) -> dict[str, str]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    pages = sorted({int(row["source_page"]) for row in rows if row.get("source_page", "").isdigit()})
    page_assets: dict[str, str] = {}
    with fitz.open(PDF_PATH) as doc:
        for page_no in pages:
            out = ASSET_DIR / f"german_glossary_p{page_no}_x4.webp"
            if not out.exists():
                page = doc[page_no - 1]
                pix = page.get_pixmap(matrix=fitz.Matrix(4.0, 4.0), alpha=False)
                try:
                    pix.pil_save(str(out), format="WEBP", optimize=True, quality=86)
                except Exception:
                    out = ASSET_DIR / f"german_glossary_p{page_no}.png"
                    if not out.exists():
                        pix.save(str(out))
            page_assets[str(page_no)] = f"assets/{out.name}"
    return page_assets


def render_entry_assets(rows: list[dict[str, str]]) -> dict[str, dict[str, list[dict[str, str]]]]:
    ENTRY_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    regions = extract_entry_regions()
    entry_assets: dict[str, dict[str, list[dict[str, str]]]] = {}
    with fitz.open(PDF_PATH) as doc:
        for row in rows:
            entry_id = row.get("row_id") or row.get("entry_id")
            region = regions.get(str(entry_id))
            if not region:
                continue
            page_no = int(region["page"])  # type: ignore[arg-type]
            page = doc[page_no - 1]
            column = int(region["column"])  # type: ignore[arg-type]
            _x0, y0, _x1, y1 = region["bbox"]  # type: ignore[assignment]
            if column == 0:
                clip_x0, clip_x1 = 20, min(98, page.rect.width)
            else:
                clip_x0, clip_x1 = max(92, page.rect.width / 2 - 4), page.rect.width - 8
            clip = fitz.Rect(
                clip_x0,
                max(0, float(y0) - 7),
                clip_x1,
                min(page.rect.height, float(y1) + 7),
            )
            out = ENTRY_ASSET_DIR / f"german_entry_r{row['row_id']}_p{page_no}.webp"
            pix = page.get_pixmap(matrix=fitz.Matrix(8.0, 8.0), clip=clip, alpha=False)
            try:
                pix.pil_save(str(out), format="WEBP", optimize=True, quality=90)
            except Exception:
                out = ENTRY_ASSET_DIR / f"german_entry_r{row['row_id']}_p{page_no}.png"
                pix.save(str(out))
            entry_assets[row["row_id"]] = {
                "german": [
                    {
                        "label": f"German glossary p. {page_no}, entry crop",
                        "src": f"assets/entries/{out.name}",
                    }
                ]
            }
    return entry_assets


def write_data(
    rows: list[dict[str, str]],
    page_assets: dict[str, str],
    entry_assets: dict[str, dict[str, list[dict[str, str]]]],
) -> None:
    payload = {
        "source_pdf": str(PDF_PATH),
        "rows": rows,
        "page_assets": page_assets,
        "entry_assets": entry_assets,
    }
    DATA_JS.write_text(
        "window.LERCH_GLOSSARY_REVIEW_DATA = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )


def write_html() -> None:
    INDEX_HTML.write_text(
        r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lerch Glossary Headword Review</title>
  <script src="glossary-data.js"></script>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f2ea;
      --panel: #fffaf2;
      --ink: #16120e;
      --muted: #6e6255;
      --line: #dacbbb;
      --accent: #0f766e;
      --warn: #8a4b0f;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      padding-bottom: 92px;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 20;
      background: rgba(247, 242, 234, .96);
      border-bottom: 1px solid var(--line);
      padding: 14px 18px;
      backdrop-filter: blur(10px);
    }
    h1 {
      margin: 0 0 10px;
      font-size: 22px;
      line-height: 1.2;
    }
    .controls {
      display: grid;
      grid-template-columns: minmax(220px, 1fr) 140px 170px 140px 130px;
      gap: 10px;
      align-items: end;
    }
    label {
      display: grid;
      gap: 4px;
      font-size: 12px;
      color: var(--muted);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .03em;
    }
    input, textarea, select, button {
      font: inherit;
      border: 1px solid var(--line);
      background: #fffdf8;
      color: var(--ink);
      border-radius: 7px;
    }
    input, select {
      min-height: 38px;
      padding: 8px 10px;
    }
    textarea {
      width: 100%;
      min-height: 58px;
      resize: vertical;
      padding: 8px 10px;
      line-height: 1.35;
    }
    button {
      min-height: 38px;
      padding: 8px 12px;
      cursor: pointer;
      font-weight: 700;
    }
    button.primary {
      background: var(--accent);
      border-color: var(--accent);
      color: white;
    }
    .layout {
      display: block;
      padding: 16px;
    }
    .page-pane {
      display: none;
    }
    .page-meta {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 8px;
    }
    #pageImage {
      display: block;
      width: 100%;
      min-width: 700px;
      height: auto;
      background: #e5dbc9;
      border: 1px solid #cdbba6;
    }
    .rows {
      display: grid;
      gap: 12px;
    }
    .row-card {
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 8px;
      overflow: hidden;
    }
    .row-card.is-active {
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(15, 118, 110, .18);
    }
    .row-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: #fff7e9;
    }
    .row-title {
      font-weight: 800;
    }
    .row-meta {
      color: var(--muted);
      font-size: 13px;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      border: 1px solid #b8a891;
      border-radius: 999px;
      padding: 3px 8px;
      font-size: 12px;
      color: #513f2f;
      background: #f8ead6;
      white-space: nowrap;
    }
    .body-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      padding: 12px;
    }
    .full { grid-column: 1 / -1; }
    .readonly {
      min-height: 38px;
      padding: 8px 10px;
      border: 1px dashed var(--line);
      border-radius: 7px;
      background: #f6efe3;
      line-height: 1.35;
      white-space: pre-wrap;
    }
    .auto-preview {
      border-style: solid;
      background: #eef8f6;
      color: #073f3a;
      font-weight: 700;
    }
    .source-crops {
      display: grid;
      gap: 10px;
    }
    .crop-card {
      margin: 0;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #efe5d4;
      overflow: hidden;
    }
    .crop-card figcaption {
      padding: 7px 9px;
      font-size: 12px;
      color: var(--muted);
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .03em;
      border-bottom: 1px solid var(--line);
      background: #f7edde;
    }
    .entry-crop {
      display: block;
      width: 100%;
      height: auto;
    }
    .source-text {
      font-family: "Times New Roman", serif;
      font-size: 18px;
    }
    .muted {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
    }
    .keyboard {
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 30;
      display: grid;
      gap: 6px;
      padding: 10px 14px;
      background: rgba(33, 28, 24, .96);
      border-top: 1px solid #5f5147;
    }
    .key-group {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }
    .key-label {
      width: 78px;
      color: #e9ddcf;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .keyboard button {
      min-height: 34px;
      min-width: 36px;
      padding: 4px 8px;
      border-color: #736258;
      background: #fffaf2;
      border-radius: 5px;
    }
    .keyboard .mark {
      background: #e3f3f1;
    }
    .status-line {
      color: var(--muted);
      font-size: 13px;
      margin-top: 8px;
    }
    @media (max-width: 1000px) {
      .controls { grid-template-columns: 1fr 1fr; }
      .page-pane { position: relative; top: auto; max-height: 55vh; }
      .body-grid { grid-template-columns: 1fr; }
      .key-label { width: 100%; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Lerch Glossary Headword Review</h1>
    <div class="controls">
      <label>Search <input id="search" type="search" placeholder="headword, gloss, page, notes"></label>
      <label>Page <select id="pageFilter"></select></label>
      <label>Status <select id="statusFilter"></select></label>
      <label>Confidence <select id="confidenceFilter"></select></label>
      <button class="primary" id="exportBtn" type="button">Export JSON</button>
    </div>
    <div class="status-line" id="statusLine"></div>
  </header>

  <main class="layout">
    <aside class="page-pane">
      <div class="page-meta">
        <strong id="pageTitle">German source page</strong>
        <span id="sourcePdf"></span>
      </div>
      <img id="pageImage" alt="German glossary source page">
    </aside>
    <section class="rows" id="rows"></section>
  </main>

  <div class="keyboard" id="keyboard" aria-label="Lerch special-character keyboard"></div>

  <script>
    const data = window.LERCH_GLOSSARY_REVIEW_DATA;
    const storageKey = "lerch-glossary-headword-review:v1";
    const rowsEl = document.getElementById("rows");
    const pageImage = document.getElementById("pageImage");
    const pageTitle = document.getElementById("pageTitle");
    const statusLine = document.getElementById("statusLine");
    const sourcePdf = document.getElementById("sourcePdf");
    const filters = {
      search: document.getElementById("search"),
      page: document.getElementById("pageFilter"),
      status: document.getElementById("statusFilter"),
      confidence: document.getElementById("confidenceFilter"),
    };
    const autosaveEndpoint = "api/autosave";
    let activeInput = null;
    let activePage = "";
    let saved = {};
    let saveTimer = null;
    let diskSaveAvailable = false;
    const autoPreviewEls = new Map();

    try {
      saved = JSON.parse(localStorage.getItem(storageKey) || "{}");
    } catch (_error) {
      saved = {};
    }

    sourcePdf.textContent = data.source_pdf;

    function unique(values) {
      return Array.from(new Set(values.filter(Boolean))).sort((a, b) => String(a).localeCompare(String(b), undefined, {numeric: true}));
    }

    function optionList(select, label, values) {
      select.innerHTML = "";
      select.append(new Option(label, ""));
      values.forEach(value => select.append(new Option(value, value)));
    }

    optionList(filters.page, "All pages", unique(data.rows.map(row => row.source_page)));
    optionList(filters.status, "All statuses", unique(data.rows.map(row => row.entry_review_status || "(blank)")));
    optionList(filters.confidence, "All", unique(data.rows.map(row => row.correction_confidence)));

    function rowValue(row, field) {
      return saved[row.row_id]?.[field] ?? row[field] ?? "";
    }

    function lerchToZazaki(value) {
      let text = String(value || "").normalize("NFD");
      text = text
        .replace(/H\u0314/g, "'H").replace(/h\u0314/g, "'h")
        .replace(/H\u02bf/g, "'H").replace(/h\u02bf/g, "'h")
        .replace(/H\u2018/g, "'H").replace(/h\u2018/g, "'h")
        .replace(/\u0393/g, "Ğ").replace(/\u03b3/g, "ğ")
        .replace(/\u03a7/g, "X").replace(/\u03c7/g, "x")
        .replace(/N\u0307(?=[gkqxX\u03c7\u03a7])/g, "N")
        .replace(/n\u0307(?=[gkqxX\u03c7\u03a7])/g, "n")
        .replace(/N\u0307/g, "Ng").replace(/n\u0307/g, "ng")
        .replace(/N\u0301/g, "Ny").replace(/n\u0301/g, "ny")
        .replace(/D\u0301/g, "Dy").replace(/d\u0301/g, "dy")
        .replace(/T\u032e/g, "Ç").replace(/t\u032e/g, "ç")
        .replace(/D\u032e/g, "C").replace(/d\u032e/g, "c")
        .replace(/S\u030c/g, "Ş").replace(/s\u030c/g, "ş")
        .replace(/Z\u030c/g, "J").replace(/z\u030c/g, "j")
        .replace(/C\u030c/g, "Ç").replace(/c\u030c/g, "ç")
        .replace(/J\u030c/g, "C").replace(/j\u030c/g, "c")
        .replace(/I\u0325/g, "\uE001")
        .replace(/i\u0325/g, "ı")
        .replace(/U[\u0324\u0308]/g, "Ü")
        .replace(/u[\u0324\u0308]/g, "ü")
        .replace(/O[\u0324\u0308]/g, "Ö")
        .replace(/o[\u0324\u0308]/g, "ö")
        .replace(/E\u0331/g, "\uE000")
        .replace(/e\u0331/g, "\uE002")
        .replace(/E\u0323/g, "Ê")
        .replace(/e\u0323/g, "ê");
      text = text.replace(/[AEIOUaeiou]/g, char => {
        if (char === "E") return "Ê";
        if (char === "e") return "ê";
        if (char === "U") return "Û";
        if (char === "u") return "û";
        if (char === "I") return "İ";
        return char;
      });
      return text
        .replace(/\uE000/g, "E")
        .replace(/\uE001/g, "I")
        .replace(/\uE002/g, "e")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[ʿʼ’']/g, "")
        .replace(/\s+/g, " ")
        .trim();
    }

    function updateGeneratedFields(rowId) {
      const row = data.rows.find(item => item.row_id === rowId);
      const target = autoPreviewEls.get(rowId);
      if (!row || !target) return;
      target.textContent = lerchToZazaki(rowValue(row, "corrected_lerch_headword"));
    }

    function setRowValue(rowId, field, value) {
      if (!saved[rowId]) saved[rowId] = {};
      saved[rowId][field] = value;
      localStorage.setItem(storageKey, JSON.stringify(saved));
      statusLine.textContent = diskSaveAvailable
        ? `Saving to disk ${new Date().toLocaleTimeString()}`
        : `Saved in browser ${new Date().toLocaleTimeString()}`;
      updateGeneratedFields(rowId);
      scheduleDiskSave();
    }

    async function loadDiskAutosave() {
      try {
        const response = await fetch(autosaveEndpoint, {cache: "no-store"});
        if (!response.ok) throw new Error("autosave endpoint unavailable");
        const payload = await response.json();
        if (payload && payload.rows) {
          saved = {...saved, ...payload.rows};
          localStorage.setItem(storageKey, JSON.stringify(saved));
        }
        diskSaveAvailable = true;
      } catch (_error) {
        diskSaveAvailable = false;
      }
    }

    function scheduleDiskSave() {
      if (!diskSaveAvailable) return;
      clearTimeout(saveTimer);
      saveTimer = setTimeout(saveDiskAutosave, 450);
    }

    async function saveDiskAutosave() {
      if (!diskSaveAvailable) return;
      try {
        const response = await fetch(autosaveEndpoint, {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({saved_at: new Date().toISOString(), rows: saved})
        });
        if (!response.ok) throw new Error("autosave failed");
        statusLine.textContent = `Saved to disk ${new Date().toLocaleTimeString()}`;
      } catch (_error) {
        diskSaveAvailable = false;
        statusLine.textContent = "Disk autosave unavailable; browser backup is still active.";
      }
    }

    function setPage(page) {
      if (!page || page === activePage) return;
      activePage = page;
      pageTitle.textContent = `German glossary source page ${page}`;
      pageImage.src = data.page_assets[page] || "";
      pageImage.alt = `German glossary source page ${page}`;
    }

    function field(label, content, className = "") {
      const wrap = document.createElement("label");
      if (className) wrap.className = className;
      wrap.append(label);
      wrap.append(content);
      return wrap;
    }

    function inputField(row, key, labelText) {
      const input = document.createElement("input");
      input.value = rowValue(row, key);
      input.spellcheck = false;
      input.dataset.row = row.row_id;
      input.dataset.field = key;
      input.addEventListener("focus", () => {
        activeInput = input;
        setPage(row.source_page);
      });
      input.addEventListener("input", () => setRowValue(row.row_id, key, input.value));
      return field(labelText, input);
    }

    function textareaField(row, key, labelText, full = false) {
      const textarea = document.createElement("textarea");
      textarea.value = rowValue(row, key);
      textarea.spellcheck = false;
      textarea.dataset.row = row.row_id;
      textarea.dataset.field = key;
      textarea.addEventListener("focus", () => {
        activeInput = textarea;
        setPage(row.source_page);
      });
      textarea.addEventListener("input", () => {
        textarea.style.height = "auto";
        textarea.style.height = `${textarea.scrollHeight + 2}px`;
        setRowValue(row.row_id, key, textarea.value);
      });
      setTimeout(() => {
        textarea.style.height = "auto";
        textarea.style.height = `${textarea.scrollHeight + 2}px`;
      }, 0);
      return field(labelText, textarea, full ? "full" : "");
    }

    function readonly(labelText, value, extraClass = "") {
      const div = document.createElement("div");
      div.className = `readonly ${extraClass}`;
      div.textContent = value || "";
      return field(labelText, div);
    }

    function autoZazakiField(row) {
      const div = document.createElement("div");
      div.className = "readonly auto-preview";
      div.textContent = lerchToZazaki(rowValue(row, "corrected_lerch_headword"));
      autoPreviewEls.set(row.row_id, div);
      return field("Modern Zazaki orthography (auto)", div);
    }

    function sourceCropBlock(row) {
      const wrap = document.createElement("div");
      wrap.className = "source-crops";
      const assets = data.entry_assets?.[row.row_id] || {};
      const sourceGroups = [
        ["russian", "Russian source crop"],
        ["german", "German source crop"]
      ];
      sourceGroups.forEach(([key, fallbackLabel]) => {
        (assets[key] || []).forEach(asset => {
          const figure = document.createElement("figure");
          figure.className = "crop-card";
          const caption = document.createElement("figcaption");
          caption.textContent = asset.label || fallbackLabel;
          const img = document.createElement("img");
          img.className = "entry-crop";
          img.src = asset.src;
          img.alt = asset.label || fallbackLabel;
          figure.append(caption, img);
          wrap.append(figure);
        });
      });
      if (!wrap.childElementCount) {
        const missing = document.createElement("div");
        missing.className = "readonly muted";
        missing.textContent = "No source crop was generated for this row; use the source page fallback if needed.";
        wrap.append(missing);
      }
      return field("Source witness crop", wrap, "full");
    }

    function selectField(row) {
      const select = document.createElement("select");
      ["needs_review", "headword_checked", "gloss_checked", "ready", "skip_name_place", "uncertain"].forEach(value => {
        select.append(new Option(value, value));
      });
      select.value = rowValue(row, "review_status") || "needs_review";
      select.addEventListener("focus", () => setPage(row.source_page));
      select.addEventListener("change", () => setRowValue(row.row_id, "review_status", select.value));
      return field("Review status", select);
    }

    function renderRow(row) {
      const card = document.createElement("article");
      card.className = "row-card";
      card.dataset.page = row.source_page;
      card.tabIndex = 0;
      card.addEventListener("focusin", () => {
        document.querySelectorAll(".row-card.is-active").forEach(item => item.classList.remove("is-active"));
        card.classList.add("is-active");
        setPage(row.source_page);
      });

      const head = document.createElement("div");
      head.className = "row-head";
      const title = document.createElement("div");
      title.innerHTML = `<div class="row-title">Row ${row.row_id}: ${escapeHtml(row.raw_lerch_headword || "")}</div><div class="row-meta">page ${row.source_page}; ${row.corrected_headword_source}; ${row.entry_review_status || "no status"}</div>`;
      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = row.correction_confidence;
      head.append(title, badge);

      const body = document.createElement("div");
      body.className = "body-grid";
      body.append(
        sourceCropBlock(row),
        readonly("Raw OCR headword", row.raw_lerch_headword, "source-text"),
        inputField(row, "corrected_lerch_headword", "Corrected Lerch headword"),
        autoZazakiField(row),
        inputField(row, "proposed_group_headword", "Group under headword"),
        textareaField(row, "german_gloss_clean", "German gloss", true),
        textareaField(row, "english_gloss", "English gloss"),
        textareaField(row, "turkish_gloss", "Turkish gloss"),
        selectField(row),
        textareaField(row, "reviewer_notes", "Reviewer notes", true),
        readonly("Raw German extraction", row.german_gloss_raw, "full"),
        readonly("Generated notes", row.notes || "", "full muted")
      );

      card.append(head, body);
      return card;
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#039;"
      }[char]));
    }

    function matches(row) {
      const term = filters.search.value.trim().toLocaleLowerCase();
      if (filters.page.value && row.source_page !== filters.page.value) return false;
      if (filters.status.value) {
        const status = row.entry_review_status || "(blank)";
        if (status !== filters.status.value) return false;
      }
      if (filters.confidence.value && row.correction_confidence !== filters.confidence.value) return false;
      if (!term) return true;
      const blob = [
        row.row_id,
        row.source_page,
        row.raw_lerch_headword,
        row.corrected_lerch_headword,
        row.modern_zazaki_guess,
        row.proposed_group_headword,
        row.german_gloss_clean,
        row.english_gloss,
        row.turkish_gloss,
        row.notes,
      ].join(" ").toLocaleLowerCase();
      return blob.includes(term);
    }

    function renderRows() {
      rowsEl.innerHTML = "";
      const visible = data.rows.filter(matches);
      visible.forEach(row => rowsEl.append(renderRow(row)));
      statusLine.textContent = `${visible.length} of ${data.rows.length} rows shown. Edits autosave to disk when opened through the review server; browser backup is also active.`;
      if (visible[0]) setPage(visible[0].source_page);
    }

    Object.values(filters).forEach(filter => filter.addEventListener("input", renderRows));
    Object.values(filters).forEach(filter => filter.addEventListener("change", renderRows));

    document.getElementById("exportBtn").addEventListener("click", () => {
      const merged = data.rows.map(row => {
        const item = {...row, ...(saved[row.row_id] || {})};
        item.modern_zazaki_guess = lerchToZazaki(item.corrected_lerch_headword || "");
        return item;
      });
      const blob = new Blob([JSON.stringify({exported_at: new Date().toISOString(), rows: merged}, null, 2)], {type: "application/json"});
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "lerch-glossary-headword-review-autosave.json";
      link.click();
      URL.revokeObjectURL(link.href);
    });

    const keyboard = document.getElementById("keyboard");
    const keyRows = [
      {
        label: "letters",
        keys: [
          "\u03b3", "\u0393", "\u03c7", "\u03a7", "\u0161", "\u0160", "\u017e", "\u017d",
          "t\u032e", "d\u032e", "d\u0301", "n\u0301", "n\u0307", "h\u0314", "H\u0314", "\u02bf", "\u02bc"
        ]
      },
      {
        label: "vowels",
        keys: [
          "\u0101", "\u0113", "\u012b", "\u014d", "\u016b", "\u0103", "\u0115", "\u012d", "\u014f", "\u016d",
          "e\u0331", "e\u0323", "i\u0325", "u\u0324", "o\u0324", "o\u0323", "\u1e01"
        ]
      },
      {
        label: "marks",
        keys: [
          {label: "acute", value: "\u0301", mark: true, title: "Add acute accent to the preceding character"},
          {label: "macron", value: "\u0304", mark: true, title: "Add macron to the preceding character"},
          {label: "line below", value: "\u0331", mark: true, title: "Add line below to the preceding character"},
          {label: "dot below", value: "\u0323", mark: true, title: "Add dot below to the preceding character"},
          {label: "ring below", value: "\u0325", mark: true, title: "Add small circle below to the preceding character"},
          {label: "diaeresis below", value: "\u0324", mark: true, title: "Add diaeresis below to the preceding character"},
          {label: "crescent below", value: "\u032e", mark: true, title: "Add half-moon/crescent below to the preceding character"},
          {label: "h mark", value: "\u0314", mark: true, title: "Add rough-breathing h mark to the preceding character"}
        ]
      }
    ];

    function insertKeyboardValue(spec) {
      if (!activeInput) return;
      const start = activeInput.selectionStart ?? activeInput.value.length;
      const end = activeInput.selectionEnd ?? activeInput.value.length;
      activeInput.value = activeInput.value.slice(0, start) + spec.value + activeInput.value.slice(end);
      const pos = start + spec.value.length;
      activeInput.setSelectionRange(pos, pos);
      activeInput.dispatchEvent(new Event("input", {bubbles: true}));
      activeInput.focus();
    }

    keyRows.forEach(row => {
      const group = document.createElement("div");
      group.className = "key-group";
      const label = document.createElement("span");
      label.className = "key-label";
      label.textContent = row.label;
      group.append(label);
      row.keys.forEach(item => {
        const spec = typeof item === "string" ? {label: item, value: item} : item;
        const btn = document.createElement("button");
        btn.type = "button";
        btn.textContent = spec.label;
        btn.title = spec.title || spec.label;
        if (spec.mark) btn.className = "mark";
        btn.addEventListener("click", () => insertKeyboardValue(spec));
        group.append(btn);
      });
      keyboard.append(group);
    });

    loadDiskAutosave().then(renderRows);
  </script>
</body>
</html>
''',
        encoding="utf-8",
    )


def main() -> None:
    rows = prepare_rows(read_tsv(CORRECTED_TSV))
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    page_assets = render_page_assets(rows)
    entry_assets = render_entry_assets(rows)
    write_data(rows, page_assets, entry_assets)
    write_html()
    print(f"Wrote {INDEX_HTML}")
    print(f"Wrote {DATA_JS}")
    print(f"Rendered {len(page_assets)} source page images")
    print(f"Rendered {len(entry_assets)} glossary entry crops")


if __name__ == "__main__":
    main()
