# Lerch Text Forms vs Local Glossary Comparison

Generated: 2026-05-19

## Scope

- Compares `texts/lerch/*/morphemes.tsv` against the current local 600-row Lerch glossary TSV.
- This is a review aid only. It uses broad accent-insensitive matching, so it can find obvious candidates but cannot replace manual lemma review.
- No source text, translation, or glossary files were modified.

## Inputs

- Glossary: `C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch\lltools_import\lltools_dictionary_lerch_glossary_full.tsv`
- Text source: `texts/lerch/*/morphemes.tsv`

## Counts

| Metric | Count |
| --- | ---: |
| Glossary rows | 600 |
| Glossary rows with German gloss | 598 |
| Glossary rows with English gloss | 95 |
| Glossary rows with Turkish gloss | 131 |
| Token records scanned | 5301 |
| Unique normalized text forms | 1260 |
| Forms with at least one glossary match | 200 |
| Forms without an obvious glossary match | 1060 |
| High-priority unmatched review candidates | 368 |

## Glossary Review State

| Review status | Rows |
| --- | ---: |
| ocr_extracted | 468 |
| headword_parented | 116 |
| qa_reviewed | 16 |

## Match Sources

| Source | Unique forms matched |
| --- | ---: |
| morpheme | 184 |
| lemma | 174 |
| surface_lerch | 158 |
| surface_zazaki | 104 |

## Top Unmatched Review Candidates

These are good candidates for glossary review/addition because they are frequent or occur in multiple texts and do not have an obvious match under the broad matching policy.

| Form | Tokens | Texts | Variants | Gloss hint | Example |
| --- | ---: | ---: | --- | --- | --- |
| me | 98 | 7 | mê; me; me,; me. | my; 1SG | ali-agha-ladi-kelhani:a02_l11:7 mê = my |
| agay | 83 | 4 | ağay; aγaí; aγái; aγái | Agha; agha | ali-agha-ladi-kelhani:a01_l02:1 ağay = agha; EZ/OBL |
| xalef | 78 | 2 | Xalef; Χalé̱f; Xalêf; Χaléf | Xalef, personal name | kauge-nyerib-u-hyeni:h02_l04:4 Xalef = Xalef, personal name |
| xoe | 73 | 6 | xoê; χóe; χóe; χóe. | own | ali-agha-ladi-kelhani:a01_l04:2 xoê = own |
| ma | 69 | 6 | ma; mā; mā; Ma | we; 1PL.POSS | ali-agha-ladi-kelhani:a01_l07:8 ma = we |
| eskeri | 67 | 4 | eskêri; e̱skéri; Eskêri; E̱skéri | army | ali-agha-ladi-kelhani:a01_l09:5 eskêri = army |
| aga | 55 | 4 | ağa; aγá; aγá; aγá, | Agha; Agha, title | ali-agha-ladi-kelhani:a01_l01:1 ağa = Agha |
| te | 44 | 7 | tê; te; te̱-; te, | you; 2SG.POSS | ali-agha-ladi-kelhani:a02_l13:3 tê = you |
| kawge | 43 | 3 | kawğe; kauγé̱; kawğê; kauγé̱ | fight | gespraech-mit-hassan:h03_l08:2 kawğe = fight |
| daqma | 39 | 1 | Daqma; Dáqma | Daqma, personal name | kauge-nyerib-u-hyeni:h03_l05:3 Daqma = Daqma, personal name |
| beray | 38 | 2 | bêray; beraí; beraí; Bêray | brother | goin-puhu-kusunun-hikayesi:g02_l04:1 bêray = brother |
| dyewi | 37 | 1 | dyewi; d́é̱wi; d́é̱wi.; Dyewi | of the dev | uc-kardes-masali:tb02_l06:2 dyewi = of the dev |
| hasaneki | 37 | 1 | 'Hasanêki; H̔asanéki; Hʿasanéki; H̔asanékī | Hasanek | uc-kardes-masali:tb01_l06:10 'Hasanêki = Hasanek |
| kerd | 30 | 6 | kêrd; kerd; kerd,; ke̱rd, | did; cut | ali-agha-ladi-kelhani:a01_l04:4 kêrd = did |
| enoe | 29 | 5 | enoê; ḗ̱n’oe; Enoê; ênoê | this; that | degirmenci-ve-tilki:mf03_l03:2 enoê = this |
| ersawute | 28 | 3 | erşawutê; e̱ršau’úte; e̱ršau’úte; êrşawutê | sent | ali-agha-ladi-kelhani:a02_l06:0 erşawutê = sent |
| begi | 28 | 2 | begi; bé̱gi; bé̱gi,; bé̱gi | Beg, title; Beg | gespraech-mit-hassan:h03_l10:9 begi = Beg |
| si | 27 | 6 | şi; ši; šī; ši, | went | ali-agha-ladi-kelhani:a02_l03:6 şi = went |
| miri | 27 | 3 | miri; mıri; míri; mí̥ri | to me; mine | degirmenci-ve-tilki:mf02_l11:8 mıri = to me |
| werist | 26 | 6 | werişt; we̱ríšt; we̱ríšt,; we̱ríšt | got up; set out | ali-agha-ladi-kelhani:a02_l08:5 werişt = rose |
| ame | 26 | 5 | ame; amê; āmé; amé | came | degirmenci-ve-tilki:mf01_l03:2 ame = came |
| be | 25 | 6 | bê; be,; be; bẹ̄, | be; with/by | ali-agha-ladi-kelhani:a02_l08:6 bê = with/by |
| ena | 25 | 5 | ena; ḗ̱n’a; ḗ̱n’a; ḗ̱n’a | this | ali-agha-ladi-kelhani:a03_l12:4 ena = this |
| u | 24 | 7 | û; u | and | ali-agha-ladi-kelhani:a01_l02:10 û = and |
| amey | 24 | 6 | amêy; āmeí; āmeí; āmeí, | came | ali-agha-ladi-kelhani:a01_l06:1 amêy = came |
| serey | 22 | 6 | serêy; sé̱rei; sé̱rei; sé̱rei | head | ali-agha-ladi-kelhani:a03_l12:2 serêy = head |
| cenyay | 22 | 3 | cênyay; Cênyay; d̮éniai; D̮éniai | woman; wife | goin-puhu-kusunun-hikayesi:g01_l01:4 cênyay = woman |
| syeri | 21 | 5 | şyêri; šyẹ̄́ri; šyẹ̄́ri; šyẹ̄́ri | go | ali-agha-ladi-kelhani:a01_l07:9 şyêri = go |
| agayri | 21 | 2 | ağayri; aγáiri; aγaíri; aγāiri | Agha; GOAL/RECIP | kauge-nyerib-u-hyeni:h02_l13:1 ağayri = Agha; GOAL/RECIP |
| habere | 20 | 4 | 'habêrê; 'haberê; h̔abé̱re; h̔abére | message; news | ali-agha-ladi-kelhani:a02_l05:8 'habêrê = news |
| qasim | 20 | 2 | Qasim; Qasím; Qasím; Qasím, | Qasim, personal name; Qasim | ali-agha-ladi-kelhani:a01_l06:7 Qasim = Qasim, personal name |
| pasay | 20 | 1 | paşay; pašai; Paşay; pašaí | pasha | degirmenci-ve-tilki:mf02_l10:5 paşay = pasha |
| misri | 19 | 1 | Mısri; Mí̥sri; Mi̥sri; Mí̥sri. | Egypt | degirmenci-ve-tilki:mf02_l04:6 Mısri = Egypt |
| ha | 18 | 5 | 'ha; h̔a; h̔ā; h̔ā | here; there | ali-agha-ladi-kelhani:a03_l14:7 'ha = was |
| ceher | 18 | 4 | çêhêr; t̮ehér; t̮ehér | four | ali-agha-ladi-kelhani:a01_l02:5 çêhêr = four |
| haber | 18 | 2 | 'haber; h̔abé̱r; 'habêr; h̔abér | message | kauge-nyerib-u-hyeni:h02_l14:2 'haber = message |
| tweri | 17 | 5 | twêri; túeri; túeri | 2SG.OBL; GOAL/RECIP | degirmenci-ve-tilki:mf02_l04:3 twêri = 2SG.OBL; GOAL/RECIP |
| hasanek | 17 | 1 | 'Hasanêk; H̔asanék; Hʿasanék; Hʿasanék, | Hasanek | uc-kardes-masali:tb01_l01:10 'Hasanêk = Hasanek |
| kagit | 17 | 1 | kağit; kaγít |  | uc-kardes-masali:tb03_l01:5 kağit |
| bi | 16 | 6 | bi; bī; bī,; bi, | was; to | ali-agha-ladi-kelhani:a02_l09:5 bi = to |
| keye | 16 | 6 | kêyê; keíye,; keíye,; kêye | house | ali-agha-ladi-kelhani:a01_l04:1 kêyê = house |
| estu | 16 | 3 | estu; é̱stu,; é̱stu; é̱stu. | there is; exists | gespraech-mit-hassan:h02_l01:5 estu = there is |
| lwe | 16 | 1 | Lwê; Lúe; lwê; lúe | fox | degirmenci-ve-tilki:mf03_l10:6 lwê = fox |
| day | 15 | 6 | day; dai; dai.; dai, | struck; gave | ali-agha-ladi-kelhani:a02_l14:11 day = gave |
| xoeri | 15 | 4 | xoêri; χóeri; χóeri,; χóeri | self/own; REFL/OBL | degirmenci-ve-tilki:mf02_l14:1 xoêri = self/own; REFL/OBL |
| agayra | 15 | 3 | ağayra; aγáira:; aγáira; aγaíra. | Agha; GOAL/RECIP | ali-agha-ladi-kelhani:a03_l01:0 ağayra = agha; EZ/OBL; RECIP |
| keynay | 15 | 3 | kêynay; keínai; keínai; Kêynay | daughter; girl | degirmenci-ve-tilki:mf02_l04:4 kêynay = daughter |
| ahmedi | 15 | 2 | A'hmêdi; Ah̔médi | Ahmed, personal name | ali-agha-ladi-kelhani:a03_l04:8 A'hmêdi = Ahmed, personal name |
| hasanekira | 15 | 1 | 'Hasanêkira; H̔asanékira; H̔asanékira:; H̔asanékira, | Hasanek; RECIP | uc-kardes-masali:tb02_l12:7 'Hasanêkira = Hasanek; RECIP |
| gerawt | 14 | 5 | gêrawt; geraút,; geraút,; geraút | took | ali-agha-ladi-kelhani:a02_l09:4 gêrawt = took |
| het | 14 | 5 | 'hêt; 'het; h̔ēt,; h̔et, | side; to | ali-agha-ladi-kelhani:a02_l08:2 'hêt = side |
| dewi | 14 | 4 | dewi; dé̱wi; dé̱wi; Dewi | villages; of the dev | ali-agha-ladi-kelhani:a01_l05:4 dewi = villages |
| ra | 14 | 4 | ra; rā; rā | to; from | degirmenci-ve-tilki:mf01_l02:10 ra = from |
| xoera | 14 | 4 | xoêra; χóera; χóera:; χóera: | self/own; REFL/RECIP | goin-puhu-kusunun-hikayesi:g02_l07:5 xoêra = self/own; REFL/RECIP |
| gelanke | 14 | 3 | gêlankê; gelā́ṅke; gelā́ṅke; gelāṅke | occasion | ali-agha-ladi-kelhani:a03_l12:5 gêlankê = occasion |
| suma | 14 | 2 | şüma; Şüma; Šṳ́ma; šṳ́ma | you.PL | gespraech-mit-hassan:h01_l05:3 şüma = you.PL |
| sere | 13 | 3 | serê; sé̱re; sé̱re; sé̱re. | head; heads | degirmenci-ve-tilki:mf03_l14:7 serê = head |
| bide | 12 | 5 | bıdê; bi̥dé,; bi̥dé; bi̥dé, | CONJ/FUT; give | ali-agha-ladi-kelhani:a03_l05:4 bıdê = CONJ/FUT; give |
| hirye | 12 | 5 | hiryê; hī́rye; hírye; 'Hiryê | three | ali-agha-ladi-kelhani:a04_l05:5 'Hiryê = three |
| seri | 12 | 5 | seri; sé̱ri; sé̱ri; sé̱ri | head; on | degirmenci-ve-tilki:mf03_l01:4 seri = head |
| laci | 12 | 4 | laci; Laci; Lā́d̮i; lā́d̮i | son; EZ/GEN | ali-agha-ladi-kelhani:a01_l01:2 laci = son; EZ/GEN |
| sweni | 12 | 4 | şwêni; šuén’i; šuén’i,; šuén’i | we go | gespraech-mit-hassan:h02_l16:1 şwêni = we go |
| mela | 12 | 3 | Mêla; Mél’a; Mél’a; mêla | mullah; Mela, religious title | ali-agha-ladi-kelhani:a04_l09:4 mêla = mullah |
| kistu | 12 | 2 | kiştu; kíštu,; kíštu,; kíštu, | killed | goin-puhu-kusunun-hikayesi:g02_l06:10 kiştu = killed |
| arewangci | 12 | 1 | arêwangçi; Arêwangçi; Ārewāṅt̮í; ārewāṅt̮í | miller | degirmenci-ve-tilki:mf01_l01:8 arêwangçi = miller |
| lue | 12 | 1 | Luê; Lú’e; luê; lú’e | fox | degirmenci-ve-tilki:mf02_l01:7 luê = fox |
| namey | 11 | 4 | namêy; Namêy; nameí; Nāmeí | name; EZ/GEN | ali-agha-ladi-kelhani:a01_l01:7 Namêy = name |
| bawki | 11 | 3 | Bawki; Baúki; bawki; baúki | father; perhaps | ali-agha-ladi-kelhani:a03_l02:4 bawki = perhaps |
| hemine | 11 | 3 | heminê; hé̱mine; hé̱mine; hé̱mine | all | kauge-nyerib-u-hyeni:h05_l08:6 heminê = all |
| cemcaqu | 11 | 1 | çêmçaqu; t̮emt̮aqú; Çêmçaqu; T̮emt̮aqú | Çemçequ | degirmenci-ve-tilki:mf03_l07:7 çêmçaqu = Çemçequ |
| gay | 11 | 1 | gay; gai; gaí | ox | uc-kardes-masali:tb03_l09:8 gay = ox |
| pasa | 11 | 1 | paşa; pašá; Paşa; Pašá | pasha | degirmenci-ve-tilki:mf03_l03:9 paşa = pasha |
| tera | 10 | 5 | têra; terá; terá; téra | from; with | degirmenci-ve-tilki:mf04_l13:7 têra = from |
| swe | 10 | 4 | şwê; šúe,; šúe; šúe | go; come | degirmenci-ve-tilki:mf03_l12:4 şwê = go |
| sivani | 10 | 3 | Sivani; Sivā́ni; Sivā́ni; Sivā́ni, | Sivan tribe; Sivan | ali-agha-ladi-kelhani:a01_l06:0 Sivani = Sivan tribe |
| ek | 10 | 2 | ek; e̱k; Ek; E̱k | that; if | goin-puhu-kusunun-hikayesi:g02_l04:0 ek = that |
| cinyu | 9 | 5 | çinyu; t̮íńu.; t̮íńu.; t̮íńu, | there is none; there is not | ali-agha-ladi-kelhani:a03_l02:8 çinyu = does not exist |
| cinu | 9 | 3 | çinu; t̮ínu,; t̮ínu.; çınu | there is none; is not | degirmenci-ve-tilki:mf04_l07:8 çinu = there is not |
| de | 9 | 3 | dê; de,; de; de. | in | degirmenci-ve-tilki:mf02_l04:1 dê = in |
| emsoe | 9 | 3 | emşoê; é̱mšoe; ḗ̱mšoe; é̱mšoe | tonight | kauge-nyerib-u-hyeni:h04_l03:5 emşoê = tonight |

## Next Review Actions

1. Use `reports/lerch-glossary-text-form-comparison.tsv` as the editable checklist.
2. Mark each candidate as `add_entry`, `merge_with_existing`, `inflected_form_only`, `proper_name`, or `ignore` in the `review_action` column.
3. Promote reviewed candidates into a publication glossary table only after checking Lerch's scanned glossary page for the headword/diacritics.
