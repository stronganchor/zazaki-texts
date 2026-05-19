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
    "goin-puhu-kusunun-hikayesi": {
        "en": "Sage of the Go'in / Eagle-Owl",
        "tr": "Go'in / Puhu Kuşunun Hikayesi",
        "de": "Sage vom Vogel gö'in",
    },
    "degirmenci-ve-tilki": {
        "en": "Tale of the Miller and the Fox",
        "tr": "Değirmenci ve Tilki",
        "de": "Mährchen von dem Müller und Fuchs",
    },
    "uc-kardes-masali": {
        "en": "The Tale of the Three Brothers",
        "tr": "Üç Kardeş Masalı",
        "de": "Das Märchen von den drei Brüdern",
    },
}

COMMON_BINGOL_URLS = [
    {
        "label": "Bingöl repository PDF",
        "url": "https://bnposta.bingol.edu.tr/bitstream/handle/20.500.12898/600/10053832.pdf?isAllowed=y&sequence=1",
    },
    {
        "label": "YÖK thesis record",
        "url": "https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id=XSxuloAAz12quT5oHaDwnA&no=lqmlps2zRpavNQmdt0OGGQ",
    },
]

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

ALI_READER_TRANSLATION_OVERRIDES = {
    "tr": [
        "Kelhan'ın oğlu Ali Ağa Karbegan nahiyesinin miriydi. Ali Ağa'nın köyünün adı Narbêş'ti.",
        "Ali Ağa dört köye saldırdı ve otuz dört kişiyi öldürdü. Ali Ağa'ya hiçbir şey olmadı; kimsenin eli Ali Ağa'ya değmedi.",
        "Ali Ağa evini toplayıp Syeraçur'a gitti. Syeraçur'da otuz altı gün kaldı.",
        "Karbegan'ın otuz dört köyü ve Sivan'ın otuz dört köyü bir araya gelip meşveret etti; Sivan ihtiyarları, Karbeganlı Qasım Ağa ve Weşinli Hasan Ağa bir araya gelip dedi ki: 'Ali Ağa'nın evine saldıralım.' Qasım Ağa dedi ki: 'Ali Ağa'yı kandıracağız; gece ordumuzu çağıracağız, köylerin askerleri hep toplansın, gece gidip Ali Ağa'yı ve dört oğlunun hepsini öldürelim.'",
        "Weşinli Hasan Ağa dedi ki: 'İyi olur, gidip Ali Ağa'yı öldürelim.' Sivan ihtiyarları dedi ki: 'Biz karışmayız.'",
        "Qasım Ağa dedi ki: 'Size ihtiyaç yok.' Sivan ihtiyarları çekilip evlerine gittiler.",
        "Qasım Ağa ile Hasan Ağa, ikisi, Ali Ağa'nın evine baskına gittiler; dört oğlunun hepsini götürüp Mehmed Hendani'nin odasına koydular. Qasım Ağa gece köylere haber gönderip dedi ki: 'Niye bekliyorsunuz?'",
        "'Ali Ağa'yı öldürmeye gidiyoruz.' Köylerin hepsi toplandı; gece kalktılar, dört yüz asker çıktı ve Qasım Ağa'nın yanına geldi.",
        "Qasım Ağa ata bindi, ordunun önüne geçti, Ğêytê'ye geldi, Ğêytê'den yüz kişi daha aldı ve beş yüz kişiyle Ali Ağa'nın yanına gitti. Qasım Ağa Ali Ağa'nın yanına gitti, oturdu ve dedi ki: 'Ağa, senden bir ricada bulunmaya geldim.'",
        "Ali Ağa dedi ki: 'Ağa, beni kandırma; silahlarımı sana vermem.' Qasım Ağa dedi ki: 'Korkma, sana hainlik etmem.'",
        "Ali Ağa dedi ki: 'Sen hainsin; silahlarımı sana vermem.' Qasım Ağa yemin etti.",
        "Ali Ağa kendi silahlarını ve dört oğlunun silahlarını topladı, Qasım Ağa'ya verdi. Qasım Ağa onları aldı.",
        "Ali Ağa'nın oğlu Ahmed dedi ki: 'Dayı, silahlarımızı alma. Sen hainsin; belki babamın başında akıl yok, bugün Ramazan günüdür. Bak dayı, silahlarımızı alır da sonra hain olarak çıkarsan seni öldürürüm.' Qasım Ağa Ahmed'e dedi ki: 'Yeğenim, korkma.'",
        "Ahmed dedi ki: 'Dayı, hançerimi ver; biliyorum, sen hainsin, dışarı çıkınca bizi öldüreceksin.' Dayısı Ahmed'e hançerini vermedi.",
        "Dayısı dışarı çıktı ve askerlerine dedi ki: 'Beklemeyin; Ali Ağa'nın ve dört oğlunun silahlarını aldım, dışarı çıktım. Beklemeyin, kapıyı kırın, içeri girin, Ali Ağa'yı ve dört oğlunun hepsini öldürün; burada yanlarında on sekiz yabancı adam daha var, onlara dokunmayın.' Qasım Ağa'nın askerleri kapıyı kırdı, Qasım Ağa öne geçti ve Ahmed'e seslenip dedi ki: 'Yeğenim, geldim; nereye gidersen bu defa başını keseceğim.'",
        "Ahmed seslenip dedi ki: 'Allah bana izin versin, önce ben seni kendi elimle öldüreceğim.' Dayısı Ahmed'i öldürmeye gitti.",
        "Ahmed duvarda bir açıklık gördü; duvarda bir kafes vardı. Elini kafesin içine soktu, kafesin içinde bir hançer bulup çıkardı ve dayısını göğsünün sağ altından vurdu. Dayısı düştü.",
        "Ahmed hançeri dayısından çıkardı; Ahmed Êysan'ı öldürdü, Hasan Kalan'ı öldürdü. Bir kılıç Ahmed'in iki gözünün arasına indi, kan Ahmed'in gözlerine geldi.",
        "Ahmed öfkelendi ve o hançerle yedi kişiyi öldürdü. Ahmed öldürüldü.",
        "Ahmed'in üç kardeşinin hepsi ve babası öldürüldü. On sekiz yabancı adam da öldürüldü.",
        "Askerler ağanın yanından ayrıldı, herkes evine gitti. Ali Ağa'nın, dört oğlunun ve on sekiz yabancı adamın cenazeleri hep odada kaldı.",
        "Sabah Mela Resa, Desmunlu Mela Qasım'a seslenip dedi ki: 'Ali Ağa'nın, oğullarının ve on sekiz yabancı adamın cenazelerini buraya getirin, dışarı çıkarın.' Mela Qasım Desmun'dan kalktı, Memed Ağa Ğêytê'den kalktı, Ramedan Ağa Merzyelê'den kalktı; gittiler, Ali Ağa'nın, oğullarının ve on sekiz yabancı adamın cesetlerini aldılar, getirdiler, götürdüler ve gömdüler.",
    ],
    "en": [
        "Ali Agha, son of Kelhan, was the mir of the Karbegan district. The name of Ali Agha's village was Narbyesh.",
        "Ali Agha attacked four villages and killed thirty-four people. Nothing happened to Ali Agha; no one's hand touched Ali Agha.",
        "Ali Agha packed up his household and went to Syerachur. He stayed in Syerachur for thirty-six days.",
        "Thirty-four villages of Karbegan and thirty-four villages of Sivan came together and held counsel; the elders of Sivan, Qasim Agha of Karbegan, and Hasan Agha of Weshin came together and said: 'Let us attack Ali Agha's house.' Qasim Agha said: 'We will deceive Ali Agha; at night we will call our army, let the village soldiers all gather, and at night we will go kill Ali Agha and all four of his sons.'",
        "Hasan Agha of Weshin said: 'That will be good; let us go kill Ali Agha.' The elders of Sivan said: 'We will not get involved.'",
        "Qasim Agha said: 'We have no need of you.' The elders of Sivan withdrew and went home.",
        "Qasim Agha and Hasan Agha, the two of them, went to raid Ali Agha's house; they took all four sons and put them in Mehmed Hendani's room. At night Qasim Agha sent word to the villages and said: 'Why are you waiting?'",
        "'We are going to kill Ali Agha.' All the villages gathered; they rose at night, four hundred soldiers came out and came to Qasim Agha's side.",
        "Qasim Agha mounted his horse, went before the army, came to Gheyte, took another hundred men from Gheyte, and with five hundred men went to Ali Agha. Qasim Agha went to Ali Agha, sat down, and said: 'Agha, I have come to ask a favor of you.'",
        "Ali Agha said: 'Agha, do not deceive me; I will not give you my weapons.' Qasim Agha said: 'Do not fear; I will not betray you.'",
        "Ali Agha said: 'You are a traitor; I will not give you my weapons.' Qasim Agha swore an oath.",
        "Ali Agha gathered his own weapons and the weapons of all four of his sons and gave them to Qasim Agha. Qasim Agha took them.",
        "Ahmed, Ali Agha's son, said: 'Uncle, do not take our weapons. You are a traitor; perhaps there is no sense in my father's head, today is Ramadan. Look, uncle, if you take our weapons and then come out as a traitor, I will kill you.' Qasim Agha said to Ahmed: 'Nephew, do not fear.'",
        "Ahmed said: 'Uncle, give me my dagger; I know you are a traitor, and when you go outside you will kill us.' His uncle did not give Ahmed his dagger.",
        "His uncle went outside and said to his soldiers: 'Do not wait; I have taken the weapons of Ali Agha and his four sons, and I have come outside. Do not wait, break down the door, go inside, and kill Ali Agha and all four of his sons; there are also eighteen foreign men there with them, do not touch them.' Qasim Agha's soldiers broke down the door, Qasim Agha went ahead and called out to Ahmed, saying: 'Nephew, I have come; wherever you go, this time I will cut off your head.'",
        "Ahmed called out and said: 'May God give me permission; first I will kill you with my own hand.' His uncle went to kill Ahmed.",
        "Ahmed saw an opening in the wall; there was a lattice in the wall. He put his hand inside the lattice, found a dagger inside the lattice and pulled it out, and struck his uncle under the right side of the chest. His uncle fell.",
        "Ahmed pulled the dagger out of his uncle; Ahmed killed Eysan and killed Hasan Kalan. A sword came down between Ahmed's two eyes, and blood came into Ahmed's eyes.",
        "Ahmed became enraged and killed seven people with that dagger. Ahmed was killed.",
        "All three of Ahmed's brothers and his father were killed. Eighteen foreign men were killed as well.",
        "The soldiers left the agha's side, and everyone went home. The bodies of Ali Agha, his four sons, and the eighteen foreign men all remained in the room.",
        "In the morning Mela Resa called to Mela Qasim of Desmun and said: 'Bring Ali Agha, his sons, and the eighteen foreign men here; take them outside.' Mela Qasim rose from Desmun, Memed Agha rose from Gheyte, Ramedan Agha rose from Merzyele; they went, took the bodies of Ali Agha, his sons, and the eighteen foreign men, brought them out, carried them away, and buried them.",
    ],
    "de": [
        "Ali Agha, Kelhans Sohn, war Mir des Bezirks Karbegan. Der Name von Ali Aghas Dorf war Narbyesh.",
        "Ali Agha überfiel vier Dörfer und tötete vierunddreißig Menschen. Ali Agha geschah nichts; niemand legte Hand an Ali Agha.",
        "Ali Agha packte sein Haus zusammen und ging nach Syerachur. In Syerachur blieb er sechsunddreißig Tage.",
        "Vierunddreißig Dörfer von Karbegan und vierunddreißig Dörfer von Sivan kamen zusammen und hielten Rat; die Ältesten von Sivan, Qasim Agha von Karbegan und Hasan Agha von Weshin kamen zusammen und sagten: 'Lasst uns Ali Aghas Haus überfallen.' Qasim Agha sagte: 'Wir werden Ali Agha täuschen; in der Nacht rufen wir unser Heer, die Soldaten der Dörfer sollen alle zusammenkommen, und in der Nacht gehen wir und töten Ali Agha und alle seine vier Söhne.'",
        "Hasan Agha von Weshin sagte: 'Das ist gut; gehen wir und töten Ali Agha.' Die Ältesten von Sivan sagten: 'Wir mischen uns nicht ein.'",
        "Qasim Agha sagte: 'Wir brauchen euch nicht.' Die Ältesten von Sivan zogen sich zurück und gingen nach Hause.",
        "Qasim Agha und Hasan Agha, die beiden, gingen, um Ali Aghas Haus zu überfallen; sie nahmen alle vier Söhne mit und brachten sie in Mehmed Hendanis Zimmer. In der Nacht schickte Qasim Agha Nachricht in die Dörfer und sagte: 'Warum wartet ihr?'",
        "'Wir gehen, um Ali Agha zu töten.' Alle Dörfer versammelten sich; in der Nacht standen sie auf, vierhundert Soldaten zogen aus und kamen zu Qasim Agha.",
        "Qasim Agha stieg zu Pferd, zog vor dem Heer her, kam nach Gheyte, nahm von Gheyte noch hundert Mann und ging mit fünfhundert Mann zu Ali Agha. Qasim Agha ging zu Ali Agha, setzte sich und sagte: 'Agha, ich bin gekommen, um dich um eine Gefälligkeit zu bitten.'",
        "Ali Agha sagte: 'Agha, täusche mich nicht; ich gebe dir meine Waffen nicht.' Qasim Agha sagte: 'Fürchte dich nicht; ich werde dich nicht verraten.'",
        "Ali Agha sagte: 'Du bist ein Verräter; ich gebe dir meine Waffen nicht.' Qasim Agha schwor einen Eid.",
        "Ali Agha sammelte seine eigenen Waffen und die Waffen aller seiner vier Söhne und gab sie Qasim Agha. Qasim Agha nahm sie.",
        "Ahmed, Ali Aghas Sohn, sagte: 'Onkel, nimm unsere Waffen nicht. Du bist ein Verräter; vielleicht ist im Kopf meines Vaters kein Verstand, heute ist Ramadan. Pass auf, Onkel, wenn du unsere Waffen nimmst und dann als Verräter hinausgehst, werde ich dich töten.' Qasim Agha sagte zu Ahmed: 'Neffe, fürchte dich nicht.'",
        "Ahmed sagte: 'Onkel, gib mir meinen Dolch; ich weiß, du bist ein Verräter, und wenn du hinausgehst, wirst du uns töten.' Sein Onkel gab Ahmed seinen Dolch nicht.",
        "Sein Onkel ging hinaus und sagte zu seinen Soldaten: 'Wartet nicht; ich habe die Waffen Ali Aghas und seiner vier Söhne genommen und bin hinausgegangen. Wartet nicht, brecht die Tür auf, geht hinein und tötet Ali Agha und alle seine vier Söhne; dort sind auch achtzehn fremde Männer bei ihnen, die rührt nicht an.' Qasim Aghas Soldaten brachen die Tür auf, Qasim Agha ging voran und rief Ahmed zu: 'Neffe, ich bin gekommen; wohin du auch gehst, diesmal schlage ich dir den Kopf ab.'",
        "Ahmed rief und sagte: 'Möge Gott mir die Erlaubnis geben; zuerst werde ich dich mit meiner eigenen Hand töten.' Sein Onkel ging, um Ahmed zu töten.",
        "Ahmed sah eine Öffnung in der Wand; in der Wand war ein Gitter. Er steckte seine Hand in das Gitter, fand im Gitter einen Dolch und zog ihn heraus, und er stieß seinem Onkel unter die rechte Seite der Brust. Sein Onkel fiel.",
        "Ahmed zog den Dolch aus seinem Onkel heraus; Ahmed tötete Eysan und tötete Hasan Kalan. Ein Schwert fuhr Ahmed zwischen die beiden Augen, und Blut kam in Ahmeds Augen.",
        "Ahmed wurde zornig und tötete mit jenem Dolch sieben Menschen. Ahmed wurde getötet.",
        "Alle drei Brüder Ahmeds und sein Vater wurden getötet. Auch achtzehn fremde Männer wurden getötet.",
        "Die Soldaten gingen vom Agha weg, und jeder ging nach Hause. Die Leichen Ali Aghas, seiner vier Söhne und der achtzehn fremden Männer blieben alle im Zimmer.",
        "Am Morgen rief Mela Resa dem Mela Qasim von Desmun zu und sagte: 'Bringt Ali Agha, seine Söhne und die achtzehn fremden Männer hierher; bringt sie hinaus.' Mela Qasim machte sich von Desmun auf, Memed Agha machte sich von Gheyte auf, Ramedan Agha machte sich von Merzyele auf; sie gingen, nahmen die Leichen Ali Aghas, seiner Söhne und der achtzehn fremden Männer, brachten sie heraus, trugen sie weg und begruben sie.",
    ],
}

HYENI_READER_TRANSLATION_OVERRIDES = {
    "tr": [
        "Bir zamanlar Nyêrib'den bir adam yola çıkıp Dawz'a gitti; Dawz'dan Hyêni toprağına geldi. Hyêni'li bir adam kendi toprağını sürüyordu.",
        "Nyêribli adam Hyêni'li adama yaklaşıp dedi ki: 'Sen kimsin de burada çift sürüyorsun?' Hyêni'li adam dedi ki: 'Ben Mela Haseynê Mûğara'nın hizmetçisiyim; burada çift sürüyorum.'",
        "Nyêribli adam dedi ki: 'Mela Haseynê Mûğara benim düşmanımdır; dedemin zamanında dedemin bir hizmetçisini öldürdü, bugün senden intikam alacağım.' Hyêni'li adam dedi ki: 'Ben bir hizmetçiyim; senin derdine benden derman olmaz.'",
        "Nyêribli adam dedi ki: 'Seni öldüreceğim.' Hyêni'li adam silahlarını almaya gitti, tabancalarını aldı, beline soktu, kılıcını eline aldı ve Nyêribli adamın üzerine yürüdü.",
        "Nyêribli adam hemen sıçradı, Hyêni'linin silahlarını elinden aldı, başını kesti, onu öldürdü, cesedini bir yana attı, Nyêrib'e Xalef Ağa'nın yanına gitti ve ona dedi ki: 'Hyêni'lilerden bir adam öldürdüm.' Xalef Ağa o adama dedi ki: 'Öldürdüğün Hyêni'li nasıl bir adamdı?'",
        "O adam Xalef Ağa'ya dedi ki: 'Mela Haseynê Mûğara'nın hizmetçisiydi.' Xalef Ağa dedi ki: 'Dikkatli ol; yabancı bir adam öldürdünüz, yabancı gelir, malınızı alır ve sizi öldürür.'",
        "O adam Xalef Ağa'ya dedi ki: 'Ağa, Küçük Nyêrib'e ve Deştê Henzi'ye haber gönder; dikkatli olsunlar, mallarını sahipsiz bırakmasınlar. Hyêni'den haber geldiği gün kimse eksik olmasın, savaşacağız.' Xalef Ağa Küçük Nyêrib'e, Wesman Ağa'ya haber gönderdi: 'Haberi Deştê Henzi'de Mêhmêt Ağa'ya gönder.'",
        "Wesman Ağa Deştê Henzi'de Mêhmêt Ağa'ya haber gönderdi: 'Hazırlan; Hyêni'liler bizimle savaşacak. Barut al, hazır ol; Hyêni'den haber geldiği gün savaşacağız.' Mêhmêt Ağa Wesman Ağa'ya haber gönderdi: 'Xalef Ağa'ya söyle: hazırız; Hyêni'den haber geldiği gün savaşacağız.'",
        "Bir ay geçince Hyêni'li Daqma Bey Büyük Nyêrib'e, Xalef Ağa'ya haber gönderdi: 'Benim bu adamımı neden öldürdün? Kendi vaktinde hazır ol; beş gün içinde savaşacağız.' Xalef Ağa Hyêni'de Daqma Bey'e haber gönderdi: 'Beş gün içinde, olmazsa yarın gel; savaşalım.'",
        "Daqma Bey Hyêni içinde tellala bağırttı: 'Hiçbir yabancı şehre girmesin, kimse izinsiz toplanmasın. Ben Daqma Bey diyorum: izinsiz gördüğüm kişinin başını kestiririm.' Daqma Bey dedi ki: 'Nyêrib'den Xalef Ağa'dan haber geldi: yarın savaş var. Evde eline sopa alabilen herkes gelsin, kimse kalmasın; yarın savaş var.'",
        "Daqma Bey Nyêrib'e, Xalef Ağa'ya haber gönderdi: 'Ordum hazır; yarın bağların arasından geleceğiz.' Xalef Ağa Hyêni'deki Daqma Bey'e haber gönderdi: 'Bu gece dikkatli ol; bu gece şehri yakacağım.'",
        "Daqma Bey bütün ordusunu topladı, Temir Bey'in evinin önünde bir araya getirdi, askerlerine barut ve kurşun verdi, ata bindi, bütün piyadeleri sokaklardan ve bütün atlıları bağların arasından gönderdi. Şafak söküp sabah aydınlanırken Nyêrib'e, Xalef Ağa'ya haber gönderdi: 'Lanetli, bu gece sabaha kadar uyumadım; sözün ne oldu, hani savaşa gelecektin? Ordum hazır.'",
        "Xalef Ağa ata bindi, davulu çaldırdı, ordusunun önüne geçti ve askerlerine dedi ki: 'Korkmayın; onlar Türk'tür, savaşmayı bilmezler. Biz yiğit aşiret adamlarıyız; korkmayın, ben sizin önünüzdeyim; ben ölsem bile siz yine savaşa gidin.' Xalef Ağa'nın askerleri dedi ki: 'Peki Ağa; biz ölmedikçe seni bırakmayız, savaşa gideriz.'",
        "Xalef Ağa dedi ki: 'Aferin ağalarım.' Xalef Ağa ordusunun önüne geçti, Hyêni toprağına çıktı ve baktı ki Daqma Bey'in bütün ordusu orada oturuyor: kimi at sürüyor, kimi yaya, kimi yemek yiyor, kimi govend çekiyor.",
        "Xalef Ağa seslendi. Daqma Bey'e dedi ki: 'Kendi vaktinde hazır ol; geldim.'",
        "Daqma Bey ata bindi, ordusuna seslenip dedi ki: 'Yerlerinize geçin; Xalef Ağa'nın ordusu geldi. Kalkın, gidin, korkmayın.' Xalef Ağa ordusuna dedi ki: 'Daqma Bey'in ordusundan kimse kaçmasın; hepsini öldürün.'",
        "Xalef Ağa'nın askerleri Xalef Ağa'ya dedi ki: 'Bize izin ver, sen de seyret.' Xalef Ağa dedi ki: 'Hücum!'",
        "Xalef Ağa'nın ordusu 'wakê, wakê' diye bağırdı. Daqma Bey'in ordusundan otuz dört kişi öldürüldü ve Daqma Bey'in ordusu kaçtı.",
        "Xalef Ağa'nın ordusu peşlerine düştü, şehre girdi, Hyêni'de bir mahalleyi yaktı, Xalil Efendi'nin başını kesti, getirip Xalef Ağa'ya verdi. Daqma Bey dedi ki: 'Aman efendim, artık savaşmayacağım; ordum kalmadı.'",
        "Xalef Ağa Daqma Bey'e haber gönderdi: 'Şehirden dışarı çık; şehri yakmaya geliyorum.' Daqma Bey hemen Xalef Ağa'ya bir kürk gönderip dedi ki: 'Aman efendim, kimsem yok; savaşamam. Benimle neden savaşacaksın?'",
        "'Ben senin üzerine gelmiyorum.' Xalef Ağa dedi ki: 'Gel; sana asker vereceğim, git benimle savaş. Üç güne kadar savaşacağız; ordun ve şehrinden kimseyi bırakmayacağım, hepsini öldüreceğim, seni de öldüreceğim.'",
        "'Karını da götüreceğim.' Daqma Bey Xalef Ağa'ya haber gönderdi: 'Bana on gün mühlet ver.'",
        "Xalef Ağa dedi ki: 'Peki, sana yirmi gün mühlet olsun; sonra hemen gel, savaşalım. Gelmezsen bütün şehri yakarım, başını keserim.' Daqma Bey Xalef Ağa'ya haber gönderdi: 'Yirmi güne kadar savaşım yok; sonra sana haber göndereceğim.'",
        "Xalef Ağa dedi ki: 'Peki efendim, sana izin olsun.' Daqma Bey'e yirmi gün mühlet verdi. Daqma Bey gitti, asker topladı ve yirmi gün içinde dört bin asker topladı.",
        "Yirmi bir gün tamam olunca Daqma Bey Nyêrib'e, Xalef Ağa'ya haber gönderdi: 'Ordum hazır; yarın savaşa geliyorum, savaşacağız.' Xalef Ağa Daqma Bey'e haber gönderdi: 'Kendi vaktinde hazır ol; yarın şafakta Dûzê Hemyê'ye geleceğim. Ordunu al, bağların arasından gel, korkma; savaşalım, ya sen benim başımı kesersin ya da ben senin başını keserim.'",
        "Daqma Bey Xalef Ağa'ya haber gönderdi: 'Gecikme, akşam gel; sabah olunca gel.' Xalef Ağa Daqma Bey'e haber gönderdi: 'Bu defa geliyorum.'",
        "Daqma Bey Xalef Ağa'ya haber gönderdi: 'Kalk gel; gözlerini çıkaracağım.' Xalef Ağa kalktı, davulları çaldırdı.",
        "Xalef Ağa'nın bütün ordusu toplandı. Xalef Ağa ordusuna dedi ki: 'Dinleyin ağalar, savaşa gidiyoruz. Korkmayın; Daqma Bey'in ordusu çoktur ama hepsi Türk'tür, bizimle savaşmayı bilmezler. Biz hepimiz yiğit Kürtleriz, aşiret adamlarıyız; korkmayın, gidiyoruz; benim başım kesilmedikçe size hiçbir şey olmaz.' Askerleri Xalef Ağa'ya dedi ki: 'Gidiyoruz; biz ölmedikçe sana bir şey olmaz.'",
        "Xalef Ağa dedi ki: 'Aferin ağalarım.' Xalef Ağa kalktı, ordusunun önüne geçti, Hyêni toprağına çıktı ve baktı ki Daqma Bey'in ordusu bağların yanında fişekleri hazırlamış.",
        "Daqma Bey'in ordusu dört bin, Xalef Ağa'nın ordusu iki bin kişiydi. Xalef Ağa'nın askerleri Xalef Ağa'ya dedi ki: 'Aman efendim, bize izin ver, savaşa gidelim.'",
        "Xalef Ağa dedi ki: 'Hücum!' Bayraktar Daqma Bey'in ordusuna karşı yürüdü, ordular birbirine girdi, iki saat savaştılar; sonunda Daqma Bey aman istedi ve Xalef Ağa'ya dedi ki: 'Seninle savaşamıyorum.'",
        "Xalef Ağa ordusunu geri çekti, Nyêrib'e geldi ve ordusunda altmış kişinin eksik olduğunu gördü. Daqma Bey'e haber gönderdi: 'Ordumdan altmış kişi eksik.' Daqma Bey Xalef Ağa'ya haber gönderdi: 'Senin ordudan altmış kişi eksik; benim ordudan yüz seksen kişi eksik, hepsi öldürüldü. Gel, ölülerini al; benim ölülerimi gömecek kimsem yok.'",
        "Xalef Ağa adamlar gönderdi ve dedi ki: 'Gidin, ölülerimizi getirin.' Adamlar gitti, ölüleri getirdi ve orada kaldı.",
        "Daqma Bey Ziriki ağalarına haber gönderdi: 'Gelin, beni Xalef Ağa ile barıştırın; hepiniz gelin, barışalım.' Ziriki ağaları kalkıp Hyêni'ye geldiler, Daqma Bey'i aldılar ve Nyêrib'e, Xalef Ağa'nın evine geldiler.",
        "Daqma Bey gidip Xalef Ağa'nın ayaklarını öptü; Xalef Ağa Daqma Bey'in elini öptü. Xalef Ağa Daqma Bey'e iki yüz koyun verdi.",
        "Daqma Bey Xalef Ağa'ya bir bağ verdi; birlikte barıştılar ve kan davası kalmadı.",
    ],
}


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
    return split_sentence_segments(text)


def split_sentence_segments(text: str) -> list[str]:
    text = join_source_parts([text])
    marked = re.sub(r"([.?!][\"'’”]?)\s+", r"\1\n", text)
    return [segment.strip() for segment in marked.splitlines() if segment.strip()]


def chunk_source_segments(segments: list[str], max_sentences: int) -> list[list[str]]:
    if max_sentences <= 1:
        return [[segment] for segment in segments]
    return [segments[index : index + max_sentences] for index in range(0, len(segments), max_sentences)]


def distribute_segments(segments: list[str], chunk_count: int) -> list[str]:
    if chunk_count <= 0:
        return []
    if not segments:
        return [""] * chunk_count
    if len(segments) < chunk_count:
        return [join_source_parts([segments[index]]) if index < len(segments) else "" for index in range(chunk_count)]

    chunks = []
    total = len(segments)
    for index in range(chunk_count):
        start = round(index * total / chunk_count)
        end = round((index + 1) * total / chunk_count)
        if end <= start:
            end = min(start + 1, total)
        chunks.append(join_source_parts(segments[start:end]))
    return chunks


def distribute_segments_for_source_chunks(segments: list[str], source_chunks: list[list[str]]) -> list[str]:
    chunk_count = len(source_chunks)
    if chunk_count <= 0:
        return []
    if not segments:
        return [""] * chunk_count

    source_sentence_count = sum(len(chunk) for chunk in source_chunks)
    if len(segments) >= source_sentence_count:
        sizes = [len(chunk) for chunk in source_chunks]
        extra = len(segments) - source_sentence_count
        start_extra = max(0, chunk_count - extra)
        for index in range(start_extra, chunk_count):
            sizes[index] += 1
        chunks = []
        cursor = 0
        for size in sizes:
            chunks.append(join_source_parts(segments[cursor : cursor + size]))
            cursor += size
        return chunks

    return distribute_segments(segments, chunk_count)


def source_line_translation(line: dict, lang: str) -> str:
    label = {"en": "ENGLISH", "tr": "TURKISH", "de": "GERMAN"}.get(lang, lang.upper())
    for row in line.get("display_rows", []):
        if row.get("label") == label:
            return str(row.get("value", "") or "")
    return ""


def reader_translation_cleanup(slug: str, lang: str, text: str) -> str:
    if slug == "ali-agha-ladi-kelhani" and lang == "tr":
        fixes = {
            "Köyünün adı Ali Ağa'nın köyü Narbêş'ti.": "Köyünün adı Narbêş'ti.",
            "Qasım'a verdi Ağa'ya.": "Qasım Ağa'ya verdi.",
            "haber köylere gönderip": "köylere haber gönderip",
        }
        for old, new in fixes.items():
            text = text.replace(old, new)
    if slug == "ali-agha-ladi-kelhani" and lang == "en":
        fixes = {
            "The name of Ali Agha's village was Narbyes.": "The name of his village was Narbyes.",
            "gave them to Qasim Agha to.": "gave them to Qasim Agha.",
        }
        for old, new in fixes.items():
            text = text.replace(old, new)
    return text


def rebuild_reader_units_from_line_translations(
    slug: str,
    doc: dict,
    source_lines: list[dict],
    max_source_sentences: int,
    skip_first_source_line: bool = False,
    translation_overrides: dict[str, list[str]] | None = None,
) -> list[dict]:
    usable_source_lines = source_lines[1:] if skip_first_source_line else source_lines
    source = join_source_parts([str(line.get("zazaki", "")) for line in usable_source_lines])
    source_chunks = chunk_source_segments(split_sentence_segments(source), max_source_sentences)
    if not source_chunks:
        return []

    translation_overrides = translation_overrides or {}
    translation_chunks = {}
    for lang in doc.get("translations", {}):
        override = translation_overrides.get(lang)
        if override and len(override) == len(source_chunks):
            translation_chunks[lang] = override
            continue
        line_translation = clean_join([source_line_translation(line, lang) for line in usable_source_lines])
        if line_translation:
            segments = split_sentence_segments(line_translation)
        else:
            full_translation = clean_join([unit.get("translations", {}).get(lang, "") for unit in doc.get("reading_units", [])])
            segments = split_sentence_segments(full_translation)
        translation_chunks[lang] = distribute_segments_for_source_chunks(segments, source_chunks)

    rebuilt = []
    for index, source_chunk in enumerate(source_chunks, start=1):
        unit_id = f"u{index:03d}"
        translations = {}
        for lang in doc.get("translations", {}):
            value = translation_chunks[lang][index - 1] if index - 1 < len(translation_chunks.get(lang, [])) else ""
            value = reader_translation_cleanup(slug, lang, value)
            if value:
                translations[lang] = value
        rebuilt.append(
            {
                "id": unit_id,
                "source": join_source_parts(source_chunk),
                "translations": translations,
            }
        )
    return rebuilt


def grouped_old_reader_units(doc: dict) -> list[dict]:
    grouped: list[dict] = []
    by_base: dict[str, dict] = {}
    languages = list(doc.get("translations", {}))
    for unit in doc.get("reading_units", []):
        base_id = unit.get("source_unit_id") or unit.get("id")
        if not base_id:
            continue
        if base_id not in by_base:
            by_base[base_id] = {
                "id": base_id,
                "source_line_ids": unit.get("source_line_ids") or [],
                "translations": {lang: [] for lang in languages},
            }
            grouped.append(by_base[base_id])
        if not by_base[base_id]["source_line_ids"] and unit.get("source_line_ids"):
            by_base[base_id]["source_line_ids"] = unit.get("source_line_ids")
        for lang in languages:
            value = unit.get("translations", {}).get(lang, "")
            if value:
                by_base[base_id]["translations"][lang].append(value)
    for unit in grouped:
        unit["translations"] = {lang: clean_join(parts) for lang, parts in unit["translations"].items() if parts}
    return grouped


def rebuild_segmented_reader_units(doc: dict, source_by_id: dict[str, dict], max_source_sentences: int) -> list[dict]:
    old_by_id = {unit.get("id"): unit for unit in doc.get("reading_units", []) if unit.get("id")}
    rebuilt = []
    for base_unit in grouped_old_reader_units(doc):
        base_id = base_unit["id"]
        line_ids = base_unit.get("source_line_ids") or []
        source = join_source_parts([source_by_id[line_id]["zazaki"] for line_id in line_ids if line_id in source_by_id])
        source_segments = split_sentence_segments(source)
        source_chunks = chunk_source_segments(source_segments, max_source_sentences)
        if not source_chunks:
            continue

        translation_chunks = {}
        for lang in doc.get("translations", {}):
            segments = split_sentence_segments(base_unit.get("translations", {}).get(lang, ""))
            translation_chunks[lang] = distribute_segments(segments, len(source_chunks))

        for index, source_chunk in enumerate(source_chunks, start=1):
            unit_id = f"{base_id}_{index:02d}"
            exact_old = old_by_id.get(unit_id, {})
            translations = {}
            for lang in doc.get("translations", {}):
                value = exact_old.get("translations", {}).get(lang, "")
                if not value and index - 1 < len(translation_chunks.get(lang, [])):
                    value = translation_chunks[lang][index - 1]
                if value:
                    translations[lang] = value
            rebuilt.append(
                {
                    "id": unit_id,
                    "source_unit_id": base_id,
                    "source_line_ids": line_ids,
                    "source": join_source_parts(source_chunk),
                    "translations": translations,
                }
            )
    return rebuilt


def rebuild_full_text_reader_units(
    doc: dict,
    source_lines: list[dict],
    max_source_sentences: int,
    skip_first_source_line: bool = False,
) -> list[dict]:
    usable_source_lines = source_lines[1:] if skip_first_source_line else source_lines
    source = join_source_parts([str(line.get("zazaki", "")) for line in usable_source_lines])
    source_chunks = chunk_source_segments(split_sentence_segments(source), max_source_sentences)
    if not source_chunks:
        return []

    translation_chunks = {}
    for lang in doc.get("translations", {}):
        full_translation = clean_join([unit.get("translations", {}).get(lang, "") for unit in doc.get("reading_units", [])])
        translation_chunks[lang] = distribute_segments_for_source_chunks(split_sentence_segments(full_translation), source_chunks)

    rebuilt = []
    for index, source_chunk in enumerate(source_chunks, start=1):
        unit_id = f"u{index:03d}"
        translations = {}
        for lang in doc.get("translations", {}):
            value = translation_chunks[lang][index - 1] if index - 1 < len(translation_chunks.get(lang, [])) else ""
            if value:
                translations[lang] = value
        rebuilt.append(
            {
                "id": unit_id,
                "source": join_source_parts(source_chunk),
                "translations": translations,
            }
        )
    return rebuilt


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


def copy_referenced_assets(bundle_dir: Path, target_dir: Path, source_lines: list[dict]) -> None:
    source_assets = bundle_dir / "assets"
    if not source_assets.exists():
        return
    target_assets = assert_inside_repo(target_dir / "assets")
    target_assets.mkdir(parents=True, exist_ok=True)
    refs: set[str] = set()
    for line in source_lines:
        for witness in line.get("witnesses", []):
            image_url = witness.get("image_url")
            if isinstance(image_url, str) and image_url.startswith("assets/"):
                refs.add(image_url.removeprefix("assets/"))
    for ref in sorted(refs):
        source = source_assets / ref
        if source.exists() and source.is_file():
            shutil.copy2(source, target_assets / ref)


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
    elif slug == "gespraech-mit-hassan":
        doc["reading_units"] = rebuild_segmented_reader_units(doc, source_by_id, max_source_sentences=1)
    elif slug == "ali-agha-ladi-kelhani":
        doc["reading_units"] = rebuild_reader_units_from_line_translations(
            slug,
            doc,
            fresh_source_lines,
            max_source_sentences=2,
            translation_overrides=ALI_READER_TRANSLATION_OVERRIDES,
        )
    elif slug == "kauge-nyerib-u-hyeni":
        doc["reading_units"] = rebuild_reader_units_from_line_translations(
            slug,
            doc,
            fresh_source_lines,
            max_source_sentences=2,
            skip_first_source_line=True,
            translation_overrides=HYENI_READER_TRANSLATION_OVERRIDES,
        )
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
    reading_units = rebuild_segmented_reader_units(
        {
            "translations": {
                "tr": {"label": "Turkish"},
                "en": {"label": "English"},
            },
            "reading_units": reading_units,
        },
        source_by_id,
        max_source_sentences=1,
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
            "reader_unit": "dialogue_turn",
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


def translation_markdown_text(
    path: Path,
    start_marker: str | None = None,
    stop_marker: str | None = None,
    skip_titles: set[str] | None = None,
) -> str:
    text = path.read_text(encoding="utf-8").replace("\ufeff", "")
    if start_marker and start_marker in text:
        text = text.split(start_marker, 1)[1]
    if stop_marker and stop_marker in text:
        text = text.split(stop_marker, 1)[0]
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
    body = []
    title_like = {
        "Sage vom Vogel gö'in.",
        "Sage vom Vogel go'in.",
        "Mährchen von dem Müller und Fuchs.",
    }
    if skip_titles:
        title_like.update(skip_titles)
    for paragraph in paragraphs:
        if paragraph.startswith("#"):
            continue
        if paragraph.startswith("Source:") or paragraph.startswith("Source note:"):
            continue
        if paragraph.startswith("This is a cleaned OCR transcription"):
            continue
        if paragraph in title_like:
            continue
        body.append(paragraph)
    return "\n\n".join(body).strip()


def translation_markdown_paragraphs(
    path: Path,
    *,
    skip_titles: set[str] | None = None,
    start_marker: str | None = None,
    stop_marker: str | None = None,
) -> list[str]:
    text = translation_markdown_text(
        path,
        start_marker=start_marker,
        stop_marker=stop_marker,
        skip_titles=skip_titles,
    )
    return [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]


def build_reader_units_from_translation_texts(
    source_lines: list[dict],
    translation_texts: dict[str, str],
    max_source_sentences: int = 2,
) -> list[dict]:
    source = join_source_parts([str(line.get("zazaki", "")) for line in source_lines])
    source_chunks = chunk_source_segments(split_sentence_segments(source), max_source_sentences)
    translation_chunks = {
        lang: distribute_segments_for_source_chunks(split_sentence_segments(text), source_chunks)
        for lang, text in translation_texts.items()
        if text.strip()
    }

    reading_units = []
    source_line_ids = [line["id"] for line in source_lines]
    for index, source_chunk in enumerate(source_chunks, start=1):
        translations = {}
        for lang, chunks in translation_chunks.items():
            value = chunks[index - 1] if index - 1 < len(chunks) else ""
            if value:
                translations[lang] = value
        reading_units.append(
            {
                "id": f"u{index:03d}",
                "source": join_source_parts(source_chunk),
                "translations": translations,
                "source_line_ids": source_line_ids,
            }
        )
    return reading_units


def folk_tale_witnesses(
    russian_story: str,
    russian_pages: str,
    russian_url_anchor: int,
    german_story: str,
    german_pages: str,
    german_archive_page: str,
    bingol_pages: str,
    bingol_heading: str,
) -> list[dict]:
    return [
        {
            "label": "Russian original edition",
            "citation": f"Lerch, Peter Ivanovich. Izsledovaniia ob iranskikh kurdakh i ikh predkakh, severnykh khaldeiakh. Vol. 1. St. Petersburg: Imperial Academy of Sciences, 1856. {russian_story}.",
            "pages": russian_pages,
            "note": "Primary scan witness for Lerch's Zazaki transcription and Russian free translation.",
            "urls": [
                {
                    "label": "RGO viewer, text start",
                    "url": f"https://elib.rgo.ru/safe-view/123456789/218398/1/MTAwMDAyMTBfTGVya2gsIFBldHIgSXZhbm92aWNoICgxODI3LTE4ODQpLiBJc3NsZWRvdmFuaXlhIG8ucGRm#{russian_url_anchor}",
                }
            ],
        },
        {
            "label": "German edition / reprint scan",
            "citation": f"Lerch, Peter. Forschungen über die Kurden und die iranischen Nordchaldäer. Abth. 1. St. Petersburg: Kaiserliche Akademie der Wissenschaften, 1857. Story '{german_story}'.",
            "pages": german_pages,
            "note": "Used for the German free translation and as a second scan witness for the Zazaki transcription.",
            "urls": [
                {
                    "label": "Internet Archive, text start",
                    "url": f"https://archive.org/details/bub_gb_WlGVYoEkr7sC/page/{german_archive_page}/mode/1up",
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
            "pages": f"{bingol_pages}; heading '{bingol_heading}'.",
            "note": "Secondary transcription witness used during alignment and review. The transcription text is cited here but is not reproduced in the Interlinear view.",
            "urls": COMMON_BINGOL_URLS,
        },
    ]


def create_bundle_text(
    *,
    slug: str,
    bundle: str,
    interlinear_file: str,
    morpheme_file: str,
    title: str,
    lerch_title: str,
    excerpt: str,
    created_from: str,
    dialect_note: str,
    translation_texts: dict[str, str],
    aligned_translation_paths: dict[str, Path] | None = None,
    witnesses: list[dict],
    max_source_sentences: int = 2,
) -> dict:
    target_dir = TEXTS_ROOT / slug
    bundle_dir = LERCH_ROOT / bundle
    data = read_json(bundle_dir / interlinear_file)
    lines = data.get("lines", [])
    source_lines = [source_line(line, "Müller 1865") for line in lines]
    translation_texts = {lang: text for lang, text in translation_texts.items() if text.strip()}
    reading_units = build_reader_units_from_translation_texts(
        source_lines,
        translation_texts,
        max_source_sentences=max_source_sentences,
    )
    aligned_translation_paths = aligned_translation_paths or {}
    title_skips = set(TRANSLATION_TITLES.get(slug, {}).values()) | {title, lerch_title}
    for lang, path in aligned_translation_paths.items():
        if not path.exists():
            continue
        paragraphs = translation_markdown_paragraphs(path, skip_titles=title_skips)
        if len(paragraphs) != len(reading_units):
            raise ValueError(
                f"{path} has {len(paragraphs)} body paragraphs; expected {len(reading_units)} for {slug}"
            )
        translation_texts.setdefault(lang, "\n\n".join(paragraphs))
        for index, paragraph in enumerate(paragraphs):
            reading_units[index].setdefault("translations", {})[lang] = paragraph
    translations = {
        lang: {"label": {"en": "English", "tr": "Turkish", "de": "German"}.get(lang, lang.upper())}
        for lang in translation_texts
    }

    doc = {
        "schema": "ll_tools_text_document.v1",
        "kind": "corpus_text",
        "lesson_id": f"lerch-{slug}",
        "title": title,
        "source_label": "Zazaki",
        "translations": translations,
        "metadata": {
            "collection": "lerch",
            "collection_label": "Peter Lerch Zazaki Texts",
            "excerpt": excerpt,
            "source_author": "Peter Lerch",
            "source_work": "Forschungen über die Kurden und die iranischen Nordchaldäer / Russian original Zazaki transcriptions",
            "story_title_lerch": lerch_title,
            "story_title_modern_zazaki": title,
            "working_status": "reviewed working edition; not final critical edition",
            "created_from": created_from,
            "exported_at": EXPORT_DATE,
            "reviewed_transcription_synced_at": EXPORT_DATE,
            "reader_unit": "sentence_group",
        },
        "summary": {
            "lines": len(lines),
            "source_lines": len(source_lines),
            "reading_units": len(reading_units),
            "tokens": sum(len(line.get("tokens", [])) for line in lines),
        },
        "witnesses": witnesses,
        "reading_units": reading_units,
        "source_lines": source_lines,
    }
    write_json(target_dir / "text-document.json", doc)
    write_json(
        target_dir / "metadata.json",
        {
            "id": f"lerch-{slug}",
            "title": title,
            "title_lerch": lerch_title,
            "author_collector": "Peter Lerch",
            "language": "Zazaki",
            "dialect_region_note": dialect_note,
            "status": "reviewed working edition",
            "line_count": len(lines),
            "token_count": doc["summary"]["tokens"],
            "lltools_payload": "text-document.json",
            "reviewed_transcription_synced_at": EXPORT_DATE,
        },
    )
    write_public_text_files(target_dir, doc)
    copy_referenced_assets(bundle_dir, target_dir, source_lines)
    copy_morphemes(bundle_dir, target_dir, morpheme_file)
    return {"slug": slug, "lines": len(lines), "tokens": doc["summary"]["tokens"]}


def create_goin_text() -> dict:
    bundle_dir = LERCH_ROOT / "lerch_goin_review_bundle"
    return create_bundle_text(
        slug="goin-puhu-kusunun-hikayesi",
        bundle="lerch_goin_review_bundle",
        interlinear_file="lerch_goin_interlinear_data.json",
        morpheme_file="lerch_morpheme_segmentation.tsv",
        title="Go'in / Puhu Kuşunun Hikayesi",
        lerch_title="Sage vom Vogel gö'in",
        excerpt="Üvey annesinin öldürdüğü kardeşini rüyasında gören bir kız, sonunda Allah'tan kendisini go'in / puhu kuşuna çevirmesini ister.",
        created_from="Lerch Goin review bundle in Language/Z/Dictionaries/Lerch",
        dialect_note="Sivan-area Zazaki tale material as discussed in local project notes.",
        translation_texts={
            "tr": translation_markdown_text(bundle_dir / "goin_turkish_free_translation.md", stop_marker="## Not"),
            "en": translation_markdown_text(bundle_dir / "goin_english_free_translation.md", stop_marker="## Note"),
            "de": translation_markdown_text(bundle_dir / "goin_german_translation_ocr.md", start_marker="## Cleaned OCR", stop_marker="## Notes"),
        },
        witnesses=folk_tale_witnesses(
            "Sage vom Vogel go'in, printed pp. 116-119",
            "Russian RGO viewer images 130-133; printed pp. 116-119.",
            130,
            "Sage vom Vogel gö'in",
            "Internet Archive scan pages around n123-n126; printed pp. 80-83.",
            "n123",
            "PDF pp. 64-66",
            "Goin",
        ),
    )


def create_miller_fox_text() -> dict:
    bundle_dir = LERCH_ROOT / "lerch_miller_fox_review_bundle"
    text_dir = TEXTS_ROOT / "degirmenci-ve-tilki"
    skip_titles = set(TRANSLATION_TITLES["degirmenci-ve-tilki"].values())
    return create_bundle_text(
        slug="degirmenci-ve-tilki",
        bundle="lerch_miller_fox_review_bundle",
        interlinear_file="lerch_miller_fox_interlinear_data.json",
        morpheme_file="lerch_morpheme_segmentation.tsv",
        title="Değirmenci ve Tilki",
        lerch_title="Mährchen von dem Müller und Fuchs",
        excerpt="Bir tilki, değirmencinin ununu çalarken yakalanınca canını kurtarmak için onu Mısır Paşası'nın kızıyla evlendireceğini söyler.",
        created_from="Lerch Miller/Fox review bundle in Language/Z/Dictionaries/Lerch",
        dialect_note="Sivan-area Zazaki tale material as discussed in local project notes.",
        translation_texts={
            "tr": translation_markdown_text(text_dir / "translation.tr.md", skip_titles=skip_titles),
            "en": translation_markdown_text(bundle_dir / "miller_fox_english_free_translation.md"),
            "de": translation_markdown_text(bundle_dir / "miller_fox_german_translation_ocr.md"),
        },
        aligned_translation_paths={
            "tr": text_dir / "translation.tr.md",
        },
        witnesses=folk_tale_witnesses(
            "Mährchen von dem Müller und Fuchs, printed pp. 119-123",
            "Russian RGO viewer images 133-137; printed pp. 119-123.",
            133,
            "Mährchen von dem Müller und Fuchs",
            "Internet Archive scan pages around n126-n130; printed pp. 83-87.",
            "n126",
            "PDF pp. 67-70",
            "Çemçequ Paşa",
        ),
    )


def create_three_brothers_text() -> dict:
    extraction = LERCH_ROOT / "lerch_zazaki_german_extraction.md"
    text_dir = TEXTS_ROOT / "uc-kardes-masali"
    skip_titles = set(TRANSLATION_TITLES["uc-kardes-masali"].values())
    return create_bundle_text(
        slug="uc-kardes-masali",
        bundle="lerch_three_brothers_review_bundle",
        interlinear_file="lerch_three_brothers_interlinear_data.json",
        morpheme_file="lerch_morpheme_segmentation.tsv",
        title="Üç Kardeş Masalı",
        lerch_title="Das Märchen von den drei Brüdern",
        excerpt="Hasanek, Qasım ve Şaban adlı üç kardeşin bir devle karşılaşmasını, Hasanek'in mektupları değiştirerek devi kandırmasını ve sonunda devi öldürmesini anlatan masal.",
        created_from="Lerch Three Brothers review bundle in Language/Z/Dictionaries/Lerch",
        dialect_note="Sivan-area Zazaki tale material as discussed in local project notes.",
        translation_texts={
            "tr": translation_markdown_text(text_dir / "translation.tr.md", skip_titles=skip_titles),
            "en": translation_markdown_text(text_dir / "translation.en.md", skip_titles=skip_titles),
            "de": translation_markdown_text(extraction, start_marker="### German Translation", stop_marker="### Needs Review"),
        },
        aligned_translation_paths={
            "tr": text_dir / "translation.tr.md",
            "en": text_dir / "translation.en.md",
        },
        witnesses=folk_tale_witnesses(
            "Das Märchen von den drei Brüdern, printed pp. 87-96",
            "Russian RGO viewer images 101-110; printed pp. 87-96.",
            101,
            "Das Märchen von den drei Brüdern",
            "Internet Archive scan pages around n92-n101; printed pp. 49-58.",
            "n92",
            "PDF pp. 36-43",
            "Vıstonıkê Hirye Bırayon",
        ),
    )


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
        create_goin_text(),
        create_miller_fox_text(),
        create_three_brothers_text(),
    ]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
