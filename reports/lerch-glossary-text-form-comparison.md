# Lerch Text Forms vs Local Glossary Comparison

Generated: 2026-05-19

## Scope

- Compares `texts/lerch/*/morphemes.tsv` against the current local 600-row Lerch glossary TSV.
- This is a review aid only. It uses broad accent-insensitive matching plus a known-alias map for common inflected forms, pronouns, and spelling variants. It can find obvious candidates but cannot replace manual lemma review.
- Proper names and known place names are filtered out before the review list is generated.
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
| Forms with at least one glossary match | 430 |
| Forms without an obvious glossary match | 830 |
| High-priority unmatched review candidates | 201 |

## Glossary Review State

| Review status | Rows |
| --- | ---: |
| ocr_extracted | 468 |
| headword_parented | 116 |
| qa_reviewed | 16 |

## Match Sources

| Source | Unique forms matched |
| --- | ---: |
| morpheme | 402 |
| lemma | 356 |
| surface_lerch | 330 |
| surface_zazaki | 262 |

## Top Unmatched Review Candidates

These are good candidates for glossary review/addition because they are frequent or occur in multiple texts and do not have an obvious match under the broad matching and known-alias policy.

| Form | Tokens | Texts | Variants | Gloss hint | Example |
| --- | ---: | ---: | --- | --- | --- |
| eskeri | 67 | 4 | eskêri; e̱skéri; Eskêri; E̱skéri | army | ali-agha-ladi-kelhani:a01_l09:5 eskêri = army |
| begi | 28 | 2 | begi; bé̱gi; bé̱gi,; bé̱gi | Beg, title; Beg | gespraech-mit-hassan:h03_l10:9 begi = Beg |
| cenyay | 22 | 3 | cênyay; Cênyay; d̮éniai; D̮éniai | woman; wife | goin-puhu-kusunun-hikayesi:g01_l01:4 cênyay = woman |
| pasay | 20 | 1 | paşay; pašai; Paşay; pašaí | pasha | degirmenci-ve-tilki:mf02_l10:5 paşay = pasha |
| kagit | 17 | 1 | kağit; kaγít |  | uc-kardes-masali:tb03_l01:5 kağit |
| bi | 16 | 6 | bi; bī; bī,; bi, | was; to | ali-agha-ladi-kelhani:a02_l09:5 bi = to |
| het | 14 | 5 | 'hêt; 'het; h̔ēt,; h̔et, | side; to | ali-agha-ladi-kelhani:a02_l08:2 'hêt = side |
| gelanke | 14 | 3 | gêlankê; gelā́ṅke; gelā́ṅke; gelāṅke | occasion | ali-agha-ladi-kelhani:a03_l12:5 gêlankê = occasion |
| namey | 11 | 4 | namêy; Namêy; nameí; Nāmeí | name; EZ/GEN | ali-agha-ladi-kelhani:a01_l01:7 Namêy = name |
| pasa | 11 | 1 | paşa; pašá; Paşa; Pašá | pasha | degirmenci-ve-tilki:mf03_l03:9 paşa = pasha |
| tera | 10 | 5 | têra; terá; terá; téra | from; with | degirmenci-ve-tilki:mf04_l13:7 têra = from |
| de | 9 | 3 | dê; de,; de; de. | in | degirmenci-ve-tilki:mf02_l04:1 dê = in |
| emsoe | 9 | 3 | emşoê; é̱mšoe; ḗ̱mšoe; é̱mšoe | tonight | kauge-nyerib-u-hyeni:h04_l03:5 emşoê = tonight |
| na | 9 | 3 | na; nā; nā.; nā. | ended; not | kauge-nyerib-u-hyeni:h05_l03:7 na = not |
| hete | 9 | 2 | 'hêtê; h̔ēte; hetê; hé̱te | with; side | ali-agha-ladi-kelhani:a02_l10:5 hetê = side |
| hadre | 8 | 3 | 'hadre; h̔adré̱; h̔ādré̱; 'hadrê | ready | kauge-nyerib-u-hyeni:h03_l01:0 'hadre = ready |
| roc | 7 | 3 | roc; rōd̮; Roc; Rōd̮ | day(s); day | degirmenci-ve-tilki:mf01_l02:1 Roc = day |
| soba | 7 | 3 | soba; so̤bā́; Soba; So̤bá | morning | ali-agha-ladi-kelhani:a04_l08:6 Soba = morning |
| waxte | 7 | 3 | waxtê; wáχte; waχte; wā́χte | time | gespraech-mit-hassan:h03_l02:2 waxtê = time |
| beg | 7 | 2 | beg; be̱g; Beg; Be̱g | Beg, title; Beg | gespraech-mit-hassan:h02_l01:1 Beg = Beg |
| vist | 7 | 2 | vist; vīst; vīst; Vist | twenty | kauge-nyerib-u-hyeni:h06_l09:10 vist = twenty |
| begiri | 7 | 1 | begiri; bé̱giri; bé̱giri. | Beg; GOAL/RECIP | kauge-nyerib-u-hyeni:h03_l08:3 begiri = Beg; GOAL/RECIP |
| bu | 6 | 2 | bu; bu,; bu.; bū. | be | goin-puhu-kusunun-hikayesi:g02_l09:6 bu = be |
| cina | 6 | 2 | çına; t̮í̥na; çina; t̮ína, | cuts; is not there | goin-puhu-kusunun-hikayesi:g04_l05:9 çına = is not there |
| lawna | 6 | 2 | lawna; launā́; launā | kissed | kauge-nyerib-u-hyeni:h09_l08:3 lawna = kissed |
| kici | 6 | 1 | kıci; ki̥d̮i; kí̥d̮i | small | uc-kardes-masali:tb01_l01:9 kıci = small |
| we | 5 | 5 | we; we̱; we̱-; wê | out-; let | ali-agha-ladi-kelhani:a04_l10:10 we = out- |
| alah | 5 | 4 | Alah; Aláh | God | ali-agha-ladi-kelhani:a03_l13:0 Alah = God |
| ge | 5 | 4 | gê; ge-; ǵe, | put on; go | degirmenci-ve-tilki:mf03_l13:4 gê = put on |
| la | 5 | 4 | la; la- | but- | degirmenci-ve-tilki:mf03_l01:3 la = but- |
| izmi | 5 | 3 | izmi; ī́zmi; ī́zmí | permission | degirmenci-ve-tilki:mf02_l12:1 izmi = permission |
| nye | 5 | 3 | nyê; ńe; ńe; Nyê | not; Nerib- | goin-puhu-kusunun-hikayesi:g03_l02:7 nyê = not |
| qawi | 5 | 3 | qawi; qaúwi; qaúwi; qaú’i | surely; why | goin-puhu-kusunun-hikayesi:g03_l06:4 qawi = surely |
| bani | 5 | 2 | bani; bā́ni | houses; house | gespraech-mit-hassan:h02_l06:1 bani = houses |
| bera | 5 | 2 | bêra; berá; berá; berā́ | brother; here | kauge-nyerib-u-sivani:s01_l10:1 bêra = here |
| bikeri | 5 | 2 | bıkêri; bi̥kéri.; bi̥kéri,; bi̥kérí, | CONJ/FUT; fight/do | kauge-nyerib-u-hyeni:h02_l12:3 bıkêri = CONJ/FUT; fight/do |
| esker | 5 | 2 | eskêr; e̱skér; e̱skér; Eskêr | army; soldier | ali-agha-ladi-kelhani:a02_l07:8 eskêr = soldier |
| simsyeri | 5 | 2 | şimşyêri; šimšyẹ̄́ri; şımşyêri; ši̥mšyẹ̄́ri | sword | kauge-nyerib-u-hyeni:h02_l01:7 şımşyêri = sword |
| byaru | 5 | 1 | byaru; biáru. | bring | uc-kardes-masali:tb03_l11:2 byaru = bring |
| eystu | 5 | 1 | êyştu; eíštu | threw | goin-puhu-kusunun-hikayesi:g02_l07:0 êyştu = threw |
| kawgaw | 5 | 1 | kawğaw; kauγaú.; kauγaú, | fought | kauge-nyerib-u-hyeni:h03_l04:2 kawğaw = fought |
| laceki | 5 | 1 | lacêki; lā́d̮eki; lā́d̮eki | of the boy | goin-puhu-kusunun-hikayesi:g03_l05:3 lacêki = of the boy |
| nost | 5 | 1 | noşt; no̤št,; no̤št:; nošt, | wrote | uc-kardes-masali:tb03_l01:6 noşt = wrote |
| nostu | 5 | 1 | noştu; nó̤štu; no̤štu; no̤štu, | wrote | uc-kardes-masali:tb03_l05:10 noştu = wrote |
| taalan | 5 | 1 | taalan; tá’alan | plunder | kauge-nyerib-u-sivani:s03_l11:12 taalan = plunder |
| sebah | 4 | 4 | sêbah; Sêbah; sebáh; Sebáh | morning | degirmenci-ve-tilki:mf01_l03:0 sêbah = morning |
| su | 4 | 4 | şu; šu; šu; su | went; shepherds- | degirmenci-ve-tilki:mf05_l08:5 şu = went |
| vinde | 4 | 4 | vındê; vindê; vínde,; ví̥nde. | stay | degirmenci-ve-tilki:mf04_l14:4 vindê = stay |
| bigi | 4 | 3 | bıgi; bi̥ǵí,; bigi; bigí, | CONJ/FUT; lead/take | degirmenci-ve-tilki:mf05_l03:3 bigi = CONJ/FUT; lead/take |
| cewi | 4 | 3 | çewi; t̮é̱wi; t̮é̱wi; t̮é̱wi | no one | ali-agha-ladi-kelhani:a01_l03:6 çewi = no one |
| gerawte | 4 | 3 | gêrawtê; geraúte; geraúte; geraúte, | took | ali-agha-ladi-kelhani:a04_l01:9 gêrawtê = took |
| lingeru | 4 | 3 | lingêru; língeru.; língeru,; líṅgeru | feet | degirmenci-ve-tilki:mf05_l01:2 lingêru = feet |
| teber | 4 | 3 | tebêr; te̱bér,; te̱bér, | outside | ali-agha-ladi-kelhani:a03_l06:8 tebêr = outside |
| akerd | 4 | 2 | akêrd; akerd; ākérd,; āké̱rd, | opened | kauge-nyerib-u-sivani:s01_l03:3 akêrd = opened |
| dumilbazi | 4 | 2 | dümilbazi; dṳ́milbā́zi; dumilbazi; dúmilbā́zi | drum | kauge-nyerib-u-hyeni:h04_l11:5 dumilbazi = drum |
| eru | 4 | 2 | eru; é̱ru,; é̱ru. | earth | degirmenci-ve-tilki:mf05_l07:6 eru = earth |
| ka | 4 | 2 | ka; ka-; ka, | would | kauge-nyerib-u-sivani:s05_l14:2 ka = would |
| qamek | 4 | 2 | qamêk; qā́mek; qāmek; qā́meḱ | some; whoever | degirmenci-ve-tilki:mf04_l05:3 qamêk = some |
| teni | 4 | 2 | teni; té̱ni; têni; tén’i | persons | ali-agha-ladi-kelhani:a04_l04:9 teni = persons |
| vaci | 4 | 2 | vaci; vā́d̮i; vā́d̮i | say; tell | gespraech-mit-hassan:h03_l15:2 vaci = tell |
| vesnay | 4 | 2 | veşnay; ve̱šnaí,; vé̱šnai,; ve̱šnai, | burned | kauge-nyerib-u-hyeni:h05_l13:1 veşnay = burned |
| vesnena | 4 | 2 | veşnêna; ve̱šnén’a,; vêşnêna; vešnén’a. | I will burn | kauge-nyerib-u-hyeni:h04_l04:2 vêşnêna = I will burn |
| warzi | 4 | 2 | warzi; wárzi,; wārzi,; wárzi | get up; rise | kauge-nyerib-u-hyeni:h05_l07:2 warzi = rise |
| wesi | 4 | 2 | weşi; weşı; wé̱ši̥; wé̱ši, | reconciliation | kauge-nyerib-u-hyeni:h09_l06:7 weşı = reconciliation |
| yawna | 4 | 2 | yawna; yaúna; yaúna; yaū́na | another | goin-puhu-kusunun-hikayesi:g01_l02:7 yawna = another |
| bya | 4 | 1 | bya; bía;; bía,; bía. | was | gespraech-mit-hassan:h03_l11:2 bya = was |
| eman | 4 | 1 | eman; e̱mán; e̱mán, | mercy | kauge-nyerib-u-hyeni:h05_l14:5 eman = mercy |
| heyst | 4 | 1 | hêyşt; 'hêyşt; h̔eíšt; heišt | eight | ali-agha-ladi-kelhani:a04_l06:4 'hêyşt = eight |
| hiris | 4 | 1 | hiris; híris; Hiris; Híris | thirty | ali-agha-ladi-kelhani:a01_l02:9 hiris = thirty |
| kasan | 4 | 1 | Kasan; Kasán; Kasán, | Kasan | gespraech-mit-hassan:h01_l09:6 Kasan = Kasan |
| mina | 4 | 1 | mina; mína; mına; mí̥na | my | uc-kardes-masali:tb03_l10:6 mına = my |
| nang | 4 | 1 | nang; nāṅ | food | uc-kardes-masali:tb04_l05:4 nang = food |
| nyeribu | 4 | 1 | Nyêribu; Ńeríbu; Ńeríbu, | to Nerib | kauge-nyerib-u-hyeni:h02_l10:0 Nyêribu = to Nerib |
| pasade | 4 | 1 | paşadê; pašáde | of the pasha | degirmenci-ve-tilki:mf02_l04:5 paşadê = of the pasha |
| peynyay | 4 | 1 | pêynyay; peíńai; peíńai; peińai | all | kauge-nyerib-u-sivani:s02_l14:1 pêynyay = all |
| qabas | 4 | 1 | qabas; Qabas; Qabás; qabā́s | captain | uc-kardes-masali:tb08_l09:6 qabas = captain |
| sahrestan | 4 | 1 | şahrêstan; šahrestān; šáhrestān; šahrestā́n | town | kauge-nyerib-u-hyeni:h03_l10:9 şahrêstan = town |
| selam | 4 | 1 | sêlam; selám | greeting | degirmenci-ve-tilki:mf03_l08:6 sêlam = greeting |
| ten | 4 | 1 | tên; ten | person | kauge-nyerib-u-hyeni:h08_l13:2 tên = person |
| cey | 3 | 3 | cêy; d̮ei; cey; d̮e̱i | place; that | degirmenci-ve-tilki:mf04_l10:10 cey = place |

## Next Review Actions

1. Use `reports/lerch-glossary-text-form-comparison.tsv` as the editable checklist.
2. Mark each candidate as `add_entry`, `merge_with_existing`, `inflected_form_only`, `proper_name`, or `ignore` in the `review_action` column.
3. Promote reviewed candidates into a publication glossary table only after checking Lerch's scanned glossary page for the headword/diacritics.
