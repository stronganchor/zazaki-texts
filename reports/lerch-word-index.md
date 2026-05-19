# Lerch All-Text Word Index

Generated: 2026-05-19

## Scope

- Groups every token in `texts/lerch/*/morphemes.tsv` by the current interlinear lemma key, falling back to the normalized surface form when no lemma is present.
- Preserves the Zazaki and Lerch-orthography variants that occur in the processed texts.
- Compares each bucket against the current local Lerch glossary with the same broad matching and known-alias policy used by the candidate review report.
- This report is a review aid; it does not add or modify glossary entries.

## Inputs

- Token records: 5301
- Glossary rows: 600
- Glossary: `C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lltools_import\lltools_dictionary_lerch_glossary_full.tsv`

## Status Counts

| Status | Lemma/form buckets |
| --- | ---: |
| low_frequency_unmatched | 543 |
| glossary_match | 272 |
| review_candidate | 226 |
| proper_name_or_place | 64 |

## Highest-Priority Review Candidates

These forms occur often enough to review, are not currently classified as names/places, and did not match the working Lerch glossary.

| Form key | Tokens | Texts | Zazaki variants | Lerch variants | Gloss hints | Example |
| --- | ---: | ---: | --- | --- | --- | --- |
| bi | 72 | 6 | bi; bıdê; bıki; bıkşi | bi̥dé,; bi; bi̥kí,; bi̥dé | CONJ/FUT; give; bring; was | ali-agha-ladi-kelhani:a01_l08:2 |
| eskeri | 68 | 4 | eskêri; Eskêri; eskêrira; Êskêri | e̱skéri; E̱skéri; e̱skéri; E̱skéri | army; soldiers; RECIP | ali-agha-ladi-kelhani:a01_l09:5 |
| ne | 40 | 7 | nyê; nyêvêrdana; nê; nyêşyêna | ńešyén’a; ńeverdā́na,; ńe; ńe | NEG; spare/leave; not; be | ali-agha-ladi-kelhani:a01_l03:5 |
| begi | 37 | 2 | begi; begiri; begira | bé̱gi; bé̱giri; bé̱gi,; bé̱gi | Beg, title; Beg; GOAL/RECIP; ABL/SOURCE | gespraech-mit-hassan:h03_l10:9 |
| deniai | 23 | 3 | cênyay; Cênyay; dênyay | d̮éniai; D̮éniai; d̮éniai; D̮éniai | woman; wife | goin-puhu-kusunun-hikayesi:g01_l01:4 |
| lad | 21 | 4 | laci; lacana; Laci; lacan | Lā́d̮i; lā́d̮i; lad̮ā́na; lā́d̮i | son; EZ/GEN; PL; EZ/OBL | ali-agha-ladi-kelhani:a01_l01:2 |
| pasai | 20 | 1 | paşay; Paşay | pašai; pašaí; Pašaí; Pašai | pasha | degirmenci-ve-tilki:mf02_l10:5 |
| tinu | 18 | 7 | çinyu; çinu; çınu | t̮ínu,; t̮íńu.; t̮ínu.; t̮íńu. | there is none; there is not; is not; does not exist | ali-agha-ladi-kelhani:a03_l02:8 |
| kagit | 17 | 1 | kağit | kaγít |  | uc-kardes-masali:tb03_l01:5 |
| het | 14 | 5 | 'hêt; 'het | h̔ēt,; h̔et,; h̔et.; h̔e̱t, | side; to | ali-agha-ladi-kelhani:a02_l08:2 |
| gelanke | 14 | 3 | gêlankê | gelā́ṅke; gelā́ṅke; gelāṅke; gelānke | occasion | ali-agha-ladi-kelhani:a03_l12:5 |
| de | 12 | 4 | dê; cê; dye | de,; de; d̮e.; de. | in; to him | ali-agha-ladi-kelhani:a03_l06:5 |
| na | 12 | 4 | na; nya | nā; ńa; nā.; ńa, | ended; not | goin-puhu-kusunun-hikayesi:g03_l02:1 |
| gai | 11 | 1 | gay | gai; gaí | ox | uc-kardes-masali:tb03_l09:8 |
| pasa | 11 | 1 | paşa; Paşa | pašá; Pašá; pašá, | pasha | degirmenci-ve-tilki:mf03_l03:9 |
| tera | 10 | 5 | têra | terá; terá; téra; téra | from; with; off | degirmenci-ve-tilki:mf04_l13:7 |
| sue | 10 | 4 | şwê | šúe,; šúe; šúe; šúe, | go; come | degirmenci-ve-tilki:mf03_l12:4 |
| namei | 9 | 4 | namêy; Namêy | nameí; Nāmeí; Nameí; nāmeí | name | ali-agha-ladi-kelhani:a01_l01:7 |
| emsoe | 9 | 3 | emşoê | é̱mšoe; ḗ̱mšoe; é̱mšoe | tonight | kauge-nyerib-u-hyeni:h04_l03:5 |
| hete | 9 | 2 | 'hêtê; hetê; 'hetê | h̔ēte; hé̱te; h̔é̱te | with; side | ali-agha-ladi-kelhani:a02_l10:5 |
| keinek | 9 | 1 | Kêynêk; kêynêk; kêynêkra | Keínek; keínek; keínekra | girl; RECIP | goin-puhu-kusunun-hikayesi:g02_l03:3 |
| daw | 8 | 3 | dawani; dawang; dawê; dawana | dauā́ni; daú’āṅ; daúe; dauwā́na | village; PL; EZ/OBL; EZ/GEN | ali-agha-ladi-kelhani:a01_l02:6 |
| etia | 8 | 3 | etya; etyara | e̱tía; e̱tía; e̱tía.; e̱tia | here; here (modern Zazaki: itiya); ABL | goin-puhu-kusunun-hikayesi:g02_l13:5 |
| hadre | 8 | 3 | 'hadre; 'hadrê | h̔adré̱; h̔ādré̱; h̔ādré; h̔adré̱ | ready | kauge-nyerib-u-hyeni:h03_l01:0 |
| enie | 8 | 2 | enyê; Enyê; ênyê; Ênyê | ḗ̱n’ie; ḗ̱n’ie; Ḗ̱n’ie; én’ie | these | ali-agha-ladi-kelhani:a02_l04:1 |
| meiste | 8 | 2 | mêyştê | meíšte | tomorrow | kauge-nyerib-u-hyeni:h03_l08:9 |
| kauta | 7 | 4 | kawta | kaúta; kaúta,; kaúta; kautá | went | ali-agha-ladi-kelhani:a02_l08:8 |
| wena | 7 | 4 | wêna | wén’a.; wén’a. | cut; PRS.1SG | ali-agha-ladi-kelhani:a03_l12:6 |
| auna | 7 | 3 | awnya; awna | auńā́; auńā́; auná; aunā́ | saw | ali-agha-ladi-kelhani:a03_l14:2 |
| rod | 7 | 3 | roc; Roc | rōd̮; Rōd̮; rōd̮, | day(s); day; days | degirmenci-ve-tilki:mf01_l02:1 |
| soba | 7 | 3 | soba; Soba | so̤bā́; So̤bá; söbā́; sobā́. | morning | ali-agha-ladi-kelhani:a04_l08:6 |
| suena | 7 | 3 | şwêna | šuén’a; šuén’a.; šuen’a; šuen’a, | I go; goes | degirmenci-ve-tilki:mf05_l04:5 |
| waxte | 7 | 3 | waxtê | wáχte; waχte; wā́χte | time | gespraech-mit-hassan:h03_l02:2 |
| beg | 7 | 2 | beg; Beg | be̱g; Be̱g | Beg, title; Beg | gespraech-mit-hassan:h02_l01:1 |
| vist | 7 | 2 | vist; Vist | vīst; vīst; Vīst | twenty | kauge-nyerib-u-hyeni:h06_l09:10 |
| wida | 6 | 4 | wica; Wica; wida | wíd̮a; Wíd̮ā; wíd̮ā; widā | there; at once; immediately | degirmenci-ve-tilki:mf03_l04:3 |
| ameia | 6 | 3 | amêya | āmeía; āmeía.]; āmeía:; āmeía. | I came; came | degirmenci-ve-tilki:mf03_l04:7 |
| aunai | 6 | 3 | awnyay; awnay | auńaí; aunái | saw | degirmenci-ve-tilki:mf02_l01:2 |
| desmat | 6 | 3 | dêsmaç | desmā́t̮; desmāt̮,; desmāt̮.; desmā́t̮ | ablution | degirmenci-ve-tilki:mf05_l03:2 |
| bani | 6 | 2 | bani; banidê | bā́ni; bā́nide | houses; LOC; house | gespraech-mit-hassan:h02_l06:1 |
| bu | 6 | 2 | bu | bu,; bu.; bū.; bú. | be | goin-puhu-kusunun-hikayesi:g02_l09:6 |
| launa | 6 | 2 | lawna | launā́; launā | kissed | kauge-nyerib-u-hyeni:h09_l08:3 |
| tina | 6 | 2 | çına; çina | t̮í̥na; t̮ína,; t̮í̥na,; t̮í̥na, | cuts; is not there | goin-puhu-kusunun-hikayesi:g04_l05:9 |
| kidi | 6 | 1 | kıci | ki̥d̮i; kí̥d̮i | small | uc-kardes-masali:tb01_l01:9 |
| we | 5 | 5 | we; wê | we̱; we̱-; we- | out-; let; and; to | ali-agha-ladi-kelhani:a04_l10:10 |
| alah | 5 | 4 | Alah | Aláh | God | ali-agha-ladi-kelhani:a03_l13:0 |
| ge | 5 | 4 | gê | ge-; ǵe, | put on; go; occasion-; took- | degirmenci-ve-tilki:mf03_l13:4 |
| izmi | 5 | 3 | izmi | ī́zmi; ī́zmí | permission | degirmenci-ve-tilki:mf02_l12:1 |
| vadi | 5 | 3 | vaci; vadi | vā́d̮i; vā́d̮i; vā́di: | say; tell | gespraech-mit-hassan:h03_l15:2 |
| bera | 5 | 2 | bêra | berá; berá; berā́; berá, | brother; here | kauge-nyerib-u-sivani:s01_l10:1 |
| esker | 5 | 2 | eskêr; Eskêr | e̱skér; e̱skér; E̱skér | army; soldier | ali-agha-ladi-kelhani:a02_l07:8 |
| rez | 5 | 2 | rezan; rez | re̱z; ré̱zān.; ré̱zān.; re̱zā́n | vineyard; PL; vine | gespraech-mit-hassan:h02_l12:1 |
| simsyeri | 5 | 2 | şimşyêri; şımşyêri | šimšyẹ̄́ri; ši̥mšyẹ̄́ri | sword | kauge-nyerib-u-hyeni:h02_l01:7 |
| biaru | 5 | 1 | byaru | biáru. | bring | uc-kardes-masali:tb03_l11:2 |
| deni | 5 | 1 | cêni; cênira; Cêni | d̮éni; d̮énira; D̮éni; d̮énira, | woman; RECIP | goin-puhu-kusunun-hikayesi:g01_l02:8 |
| eistu | 5 | 1 | êyştu | eíštu | threw | goin-puhu-kusunun-hikayesi:g02_l07:0 |
| kaugau | 5 | 1 | kawğaw | kauγaú.; kauγaú, | fought | kauge-nyerib-u-hyeni:h03_l04:2 |
| keineke | 5 | 1 | kêynêkê; Kêynêkê | keíneke; Keíneke; keíneke, | the girl | goin-puhu-kusunun-hikayesi:g02_l03:0 |
| ladeki | 5 | 1 | lacêki | lā́d̮eki; lā́d̮eki | of the boy | goin-puhu-kusunun-hikayesi:g03_l05:3 |
| laser | 5 | 1 | la; seri; laser | la; sé̱ri; lasé̱r | flood; flood-cont. | degirmenci-ve-tilki:mf02_l14:5 |
| nost | 5 | 1 | noşt | no̤št,; no̤št:; nošt,; nöšt, | wrote | uc-kardes-masali:tb03_l01:6 |
| nostu | 5 | 1 | noştu | nó̤štu; no̤štu; no̤štu,; nó̤štu. | wrote | uc-kardes-masali:tb03_l05:10 |
| qaifeti | 5 | 1 | qayfeçi; qayfêçira; Qayfeçi; qayfetira | qaife̱t̮í; qaifet̮íra:; Qaife̱t̮í; qaife̱tíra | coffeehouse keeper; RECIP | uc-kardes-masali:tb07_l11:2 |
| sahrestan | 5 | 1 | şahrêstan; şahrêstang | šahrestān; šáhrestān; šahrestāṅ,; šahrestā́n | town | kauge-nyerib-u-hyeni:h03_l10:9 |
| taalan | 5 | 1 | taalan | tá’alan | plunder | kauge-nyerib-u-sivani:s03_l11:12 |
| sebah | 4 | 4 | sêbah; Sêbah | sebáh; Sebáh; sebāh; Sebáh | morning | degirmenci-ve-tilki:mf01_l03:0 |
| su | 4 | 4 | şu; su; şü | šu; šu; su-; šṳ́- | went; shepherds- | degirmenci-ve-tilki:mf05_l08:5 |
| vinde | 4 | 4 | vındê; vindê | vínde,; ví̥nde.; ví̥nde,; vi̥ndé, | stay | degirmenci-ve-tilki:mf04_l14:4 |
| geraute | 4 | 3 | gêrawtê | geraúte; geraúte; geraúte, | took | ali-agha-ladi-kelhani:a04_l01:9 |
| lingeru | 4 | 3 | lingêru | língeru.; língeru,; líṅgeru; líṅgeru, | feet | degirmenci-ve-tilki:mf05_l01:2 |
| teber | 4 | 3 | tebêr | te̱bér,; te̱bér, | outside | ali-agha-ladi-kelhani:a03_l06:8 |
| tewi | 4 | 3 | çewi | t̮é̱wi; t̮é̱wi; t̮é̱wi | no one | ali-agha-ladi-kelhani:a01_l03:6 |
| akerd | 4 | 2 | akêrd; akerd | ākérd,; āké̱rd,; aké̱rd,; akērd, | opened | kauge-nyerib-u-sivani:s01_l03:3 |
| dumilbazi | 4 | 2 | dümilbazi; dumilbazi; Dumilbazi | dṳ́milbā́zi; dúmilbā́zi; Dúmilbāzi | drum | kauge-nyerib-u-hyeni:h04_l11:5 |
| eru | 4 | 2 | eru | é̱ru,; é̱ru. | earth | degirmenci-ve-tilki:mf05_l07:6 |
| garib | 4 | 2 | ğaribana; ğarib | γaribā́na; γarib | stranger; PL; EZ/OBL; outsider | ali-agha-ladi-kelhani:a04_l08:2 |
| hemam | 4 | 2 | 'hemam; 'hêmam; 'hêmamra | h̔é̱m’ām,; h̔e̱m’ām,; h̔emám,; h̔emā́mra | bath; ABL | degirmenci-ve-tilki:mf03_l12:5 |
| ka | 4 | 2 | ka | ka-; ka; ka, | would | kauge-nyerib-u-sivani:s05_l14:2 |
| qamek | 4 | 2 | qamêk | qā́mek; qāmek; qā́meḱ | some; whoever | degirmenci-ve-tilki:mf04_l05:3 |
| qauwi | 4 | 2 | qawi | qaúwi; qaúwi | surely; why | goin-puhu-kusunun-hikayesi:g03_l06:4 |
| teni | 4 | 2 | teni; têni | té̱ni; tén’i | persons | ali-agha-ladi-kelhani:a04_l04:9 |
| vesnai | 4 | 2 | veşnay | ve̱šnaí,; vé̱šnai,; ve̱šnai, | burned | kauge-nyerib-u-hyeni:h05_l13:1 |
| vesnena | 4 | 2 | veşnêna; vêşnêna | ve̱šnén’a,; vešnén’a.; ve̱šnén’a. | I will burn | kauge-nyerib-u-hyeni:h04_l04:2 |
| warzi | 4 | 2 | warzi | wárzi,; wārzi,; wárzi | get up; rise | kauge-nyerib-u-hyeni:h05_l07:2 |
| wesi | 4 | 2 | weşi; weşı | wé̱ši̥; wé̱ši,; wé̱ši; wé̱ši, | reconciliation | kauge-nyerib-u-hyeni:h09_l06:7 |
| yauna | 4 | 2 | yawna | yaúna; yaúna; yaū́na | another | goin-puhu-kusunun-hikayesi:g01_l02:7 |
| auke | 4 | 1 | awkê; awkêra | aúke; aúkera | water; from | degirmenci-ve-tilki:mf03_l03:5 |
| basi | 4 | 1 | başira; başi | baší; bašíra; bašīra: | captain; RECIP | uc-kardes-masali:tb08_l09:7 |
| bia | 4 | 1 | bya | bía;; bía,; bía. | was | gespraech-mit-hassan:h03_l11:2 |
| eman | 4 | 1 | eman | e̱mán; e̱mán, | mercy | kauge-nyerib-u-hyeni:h05_l14:5 |
| heist | 4 | 1 | hêyşt; 'hêyşt | h̔eíšt; heišt; heíšt; heíšt | eight | ali-agha-ladi-kelhani:a04_l06:4 |
| hiris | 4 | 1 | hiris; Hiris | híris; Híris | thirty | ali-agha-ladi-kelhani:a01_l02:9 |
| mina | 4 | 1 | mina; mına | mína; mí̥na | my | uc-kardes-masali:tb03_l10:6 |
| nan | 4 | 1 | nang | nāṅ | food | uc-kardes-masali:tb04_l05:4 |
| neribu | 4 | 1 | Nyêribu | Ńeríbu; Ńeríbu, | to Nerib | kauge-nyerib-u-hyeni:h02_l10:0 |
| pasade | 4 | 1 | paşadê | pašáde | of the pasha | degirmenci-ve-tilki:mf02_l04:5 |
| peinai | 4 | 1 | pêynyay | peíńai; peíńai; peińai | all | kauge-nyerib-u-sivani:s02_l14:1 |
| qabas | 4 | 1 | qabas; Qabas | Qabás; qabā́s; qabās | captain | uc-kardes-masali:tb08_l09:6 |
| sebake | 4 | 1 | şêbakê; şêbakêdê | šebā́ke; šebā́kede | lattice; at the grating; LOC | uc-kardes-masali:tb09_l01:7 |
| selam | 4 | 1 | sêlam | selám | greeting | degirmenci-ve-tilki:mf03_l08:6 |
| sie | 4 | 1 | şyê | šíe; šíe, | went | degirmenci-ve-tilki:mf02_l01:10 |
| ten | 4 | 1 | tên | ten | person | kauge-nyerib-u-hyeni:h08_l13:2 |
| daue | 3 | 3 | dawê; dawe | daú’e,; daúe̱; dau’e | attack; of village; village | ali-agha-ladi-kelhani:a02_l04:8 |
| dei | 3 | 3 | cêy; cey | d̮ei; d̮e̱i | place; that; him | degirmenci-ve-tilki:mf04_l10:10 |
| dine | 3 | 3 | cinê; dinê | d̮íne; d̮īne; dī́ne | women; herds | degirmenci-ve-tilki:mf03_l01:8 |
| gna | 3 | 3 | gna | gnā; gnā | struck; fell; this time | ali-agha-ladi-kelhani:a04_l03:7 |
| keri | 3 | 3 | kêri | kéri.; kéri,; kéri | -army; make | goin-puhu-kusunun-hikayesi:g04_l09:1 |
| kunagi | 3 | 3 | kunaği | kunáγi | before | degirmenci-ve-tilki:mf04_l08:2 |
| la | 3 | 3 | la | la; la- | but- | goin-puhu-kusunun-hikayesi:g04_l01:5 |
| pand | 3 | 3 | pangc; pangd | pāṅd; paṅd̮; pāṅd̮ | five | ali-agha-ladi-kelhani:a02_l09:6 |
| peini | 3 | 3 | pêynıdê | peíni̥de | end; LOC/TEMP | ali-agha-ladi-kelhani:a03_l03:6 |
| rind | 3 | 3 | rınd; rınyd | ri̥nd; ri̥ńd | good; fine | ali-agha-ladi-kelhani:a02_l01:3 |
| sei | 3 | 3 | sêy | sei | hundred | ali-agha-ladi-kelhani:a02_l07:7 |
| teres | 3 | 3 | têres; têrês; teres | teré̱s,; terés,; te̱ré̱s, | cursed one; accursed one; damned | degirmenci-ve-tilki:mf04_l12:4 |
| aferem | 3 | 2 | afêrêm | ā́ferem,; āferém; ā́ferem | thanks | kauge-nyerib-u-hyeni:h05_l01:2 |
| aqil | 3 | 2 | aqıl | āqí̥l; áqi̥l | sense; reason | ali-agha-ladi-kelhani:a03_l02:7 |
| bikeru | 3 | 2 | bıkêru; bikêru | bi̥kéru.; bikeru.; bi̥kéru, | do; make | goin-puhu-kusunun-hikayesi:g04_l02:7 |
| diari | 3 | 2 | dyari | diári; diā́ri; diā́ri | territory; district | kauge-nyerib-u-hyeni:h05_l02:0 |
| hadrau | 3 | 2 | 'hadraw | h̔ādrāu,; h̔ādraú.; h̔adraú, | is ready | kauge-nyerib-u-hyeni:h04_l02:1 |
| heni | 3 | 2 | 'hêni; hêni | h̔én’i; hén’ī | again | goin-puhu-kusunun-hikayesi:g02_l13:0 |

## Most Frequent Glossary-Matched Forms

| Form key | Tokens | Texts | Glossary entries | Gloss hints |
| --- | ---: | ---: | --- | --- |
| ke | 187 | 6 | ke | that |
| va | 172 | 6 | va; va$ | said |
| me | 128 | 7 | mjri; ez | my; NEG.IMP; 1SG |
| xoe | 112 | 6 | ez | own; self/own; REFL/OBL |
| ez | 103 | 7 | ez | I; 1SG.DIR |
| agai | 89 | 3 | ayä | Agha; GOAL/RECIP; Agha, title |
| aga | 87 | 4 | ayä | Agha; agha; EZ/OBL |
| tue | 77 | 7 | tü; tu | your; 2SG.OBL; GOAL/RECIP |
| ma | 71 | 6 | rna | we; us; RECIP |
| yau | 58 | 7 | yau | one |
| dewi | 57 | 4 | dau; d'au | of the dev; villages; dev |
| te | 53 | 7 | tü; tu | you; it; LOC |
| kauge | 51 | 3 | kauyä | fight; feud; EZ/GEN |
| berai | 46 | 3 | berd | brother; brothers |
| kerd | 43 | 6 | ers kerd; top kerd; müSore (ar. L») kerd | did; do/make; PRS.1SG |
| merdum | 38 | 6 | merdüm | man/person; OBL/EZ; person |
| be | 36 | 6 | asän be; bye | be; PRS.1SG; be/take |
| se | 36 | 6 | se; set = se | went; what; left |
| da | 33 | 5 | da | gave; called; overran |
| ver | 33 | 6 | ver; ver ken’a; veri | front; front of; LOC |
| lue | 32 | 1 | lu | fox; RECIP |
| di | 29 | 7 | di; du | saw; two; in |
| enoe | 29 | 5 | äna; awe | this; that |
| ersauute | 28 | 3 | eräau’üte | sent |
| miri | 27 | 3 | mjri; ez | to me; mine |
| si | 27 | 6 | Sia; sußn’a; Sc; Sl | went |
| ti | 27 | 7 | tu | you; thing; what |
| werist | 27 | 6 | weriät; warzdn’a | got up; set out; mounted |
| ame | 26 | 5 | amá; yen’a | came |
| avdulah | 26 | 1 | Avdul’ah | Avdulah, personal name |
| dau | 26 | 5 | dau; d'au | dev; village; PL |
| ena | 25 | 5 | äna; awe | this |
| ali | 24 | 2 | Ali | Ali, personal name; Ali |
| amei | 24 | 6 | amá; yen’a | came |
| pyeru | 24 | 4 | pyeru | all |
| u | 24 | 7 | Sre’u; pures neydn’u; manün’u | and |
| bye | 23 | 5 | bye | come |
| serei | 22 | 6 | ser; ser (postpos.) | head |
| dai | 21 | 6 | da; däna; pero däna | struck; gave; there |
| syeri | 21 | 5 | Syer; Sia; sußn’a | go |
| habere | 20 | 4 | häl | message; news |
| kist | 20 | 5 | kisen’a | kill; PRS/FUT.1SG; killed |
| nerib | 19 | 2 | Nerib | Nerib; Nerib, place name; AFFIL |
| ha | 18 | 5 | ha in | here; there; was |
| haber | 18 | 2 | häl | message |
| teher | 18 | 4 | tehtir | four |
| eke | 17 | 5 | ek’e | if |
| keiye | 17 | 6 | kei | house; LOC |
| estu | 16 | 3 | estii | there is; exists |
| wa | 16 | 4 | wa | let |
| ahmedi | 15 | 2 | Ahmed | Ahmed, personal name |
| arewanti | 15 | 1 | arewantf | miller; RECIP |
| kei | 15 | 6 | kei | house |
| keinai | 15 | 3 | kcina | daughter; girl |
| pilau | 15 | 1 | pilau | pilaf |
| sere | 15 | 4 | ser; ser (postpos.) | head; heads; LOC |
| suma | 15 | 3 | Simä | you.PL; 2PL; GOAL/RECIP |
| berd | 14 | 4 | berd | took; carried; put |
| geraut | 14 | 5 | terd geraut | took |
| ra | 14 | 4 | ra kdn’a; ra kuen’a | to; from |
| pei | 13 | 4 | pei | after; then; between |
| hirye | 12 | 5 | diei | three |
| kaut | 12 | 5 | kaut | went; fell |
| kistu | 12 | 2 | kisen’a | killed |
| mela | 12 | 3 | möl’a | mullah; Mela, religious title |
| sueni | 12 | 4 | Sia; sußn’a | we go |
| bauki | 11 | 3 | bauk | father; perhaps |
| hemine | 11 | 3 | heme | all |
| sima | 11 | 3 | Simä | you; 2PL; GOAL/POSS |
| efendim | 10 | 4 | efendim | my lord |
| ek | 10 | 2 | ek’e | that; if |
| seri | 10 | 4 | ser; ser (postpos.) | on; head |
| yena | 10 | 4 | yen’a | I come |
| zeindan | 10 | 2 | zeindän | pit; prison; LOC |
| espar | 9 | 3 | Sstere | horse |
| esti | 9 | 2 | estii | there are |
| heme | 9 | 3 | heme | all |
| rodi | 9 | 4 | ya rödi | days; day |
| tau | 9 | 4 | tau | no one |
| tu | 9 | 6 | tü; tu | you; 2SG.OBL; RECIP |

## Files

- Full TSV index: `reports/lerch-word-index.tsv`
- Summary report: `reports/lerch-word-index.md`
