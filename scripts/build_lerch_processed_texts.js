const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const lerchRoot = path.join(repoRoot, 'texts', 'lerch');
const bundleRoot = path.resolve(
  'C:/Users/messy/OneDrive/Documents/Language/Z/Dictionaries/Lerch'
);

function assertInsideRepo(targetPath) {
  const resolved = path.resolve(targetPath);
  const rootWithSep = repoRoot.endsWith(path.sep) ? repoRoot : repoRoot + path.sep;
  if (resolved !== repoRoot && !resolved.startsWith(rootWithSep)) {
    throw new Error(`Refusing to write outside repo: ${resolved}`);
  }
  return resolved;
}

function ensureDir(dir) {
  fs.mkdirSync(assertInsideRepo(dir), { recursive: true });
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, value) {
  fs.writeFileSync(assertInsideRepo(file), `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function writeText(file, value) {
  fs.writeFileSync(assertInsideRepo(file), value.replace(/\s+$/u, '') + '\n', 'utf8');
}

function copyAssets(sourceDir, targetDir) {
  ensureDir(targetDir);
  fs.cpSync(sourceDir, assertInsideRepo(targetDir), { recursive: true, force: true });
}

function lineText(line, key) {
  return (line.tokens || []).map((token) => token[key] || '').filter(Boolean).join(' ');
}

function corpusToken(token) {
  const morphemes = Array.isArray(token.morphemes) ? token.morphemes : [];
  const firstMorph = morphemes[0] || {};
  return {
    form: token.lerch || token.core || '',
    ipa: token.ipa || '',
    zazaki: token.zazaki || '',
    lemma: firstMorph.lemma || token.core || token.lerch || '',
    display_gloss: token.gloss || '',
    gloss_tr: token.gloss_tr || '',
    gloss_de: token.gloss_de || '',
    pos: firstMorph.pos || '',
    morphemes: morphemes.map((morph) => ({
      form: morph.surface_lerch || morph.form || '',
      normalized: morph.normalized || '',
      lemma: morph.lemma || '',
      gloss: morph.gloss || '',
      pos: morph.pos || '',
      features: morph.features || '',
      confidence: morph.confidence || '',
      evidence: morph.evidence || '',
      notes: morph.notes || '',
    })),
  };
}

function sourceLine(line, sourceLabel) {
  const lerch = lineText(line, 'lerch');
  const ipa = lineText(line, 'ipa');
  const zazaki = lineText(line, 'zazaki');
  const displayRows = [
    { label: 'LERCH', value: lerch },
    { label: 'IPA', value: ipa },
    { label: 'ZAZAKI', value: zazaki },
  ];
  if (line.free_translation_en) {
    displayRows.push({ label: 'ENGLISH', value: line.free_translation_en });
  }
  if (line.free_translation_tr) {
    displayRows.push({ label: 'TURKISH', value: line.free_translation_tr });
  }

  const witnesses = [];
  if (line.russian_asset) {
    witnesses.push({
      label: 'Russian scan',
      image_url: line.russian_asset,
      source: `Lerch line crop; Russian printed page ${line.russian_print_page || ''}, scan page ${line.russian_page || ''}`.trim(),
    });
  }
  if (line.german_asset) {
    witnesses.push({
      label: 'German reprint scan',
      image_url: line.german_asset,
      source: `${sourceLabel} German line crop`,
    });
  }

  return {
    id: line.segment_id,
    title: line.title || line.segment_id,
    text: lerch,
    lerch,
    ipa,
    zazaki,
    source_note: line.source_note || '',
    russian_print_page: line.russian_print_page || null,
    russian_scan_page: line.russian_page || null,
    display_rows: displayRows,
    witnesses,
    tokens: (line.tokens || []).map(corpusToken),
    phrase_matches: line.phrases || [],
    hidden_rows: {
      bingol_transcription: line.bingol_transcription || '',
    },
  };
}

function mdParagraphs(file) {
  return fs.readFileSync(file, 'utf8')
    .replace(/^\uFEFF/u, '')
    .split(/\r?\n\s*\r?\n/u)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);
}

function bodyParagraphs(file) {
  return mdParagraphs(file).filter((paragraph) => !paragraph.startsWith('# '));
}

function parseHyeniText(file) {
  const text = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/u, '');
  const zazakiMatch = text.match(/## Zazaki Text\s*([\s\S]*?)\s*## Turkish Translation/u);
  const turkishMatch = text.match(/## Turkish Translation\s*([\s\S]*?)\s*## Translation Notes/u);
  if (!zazakiMatch || !turkishMatch) {
    throw new Error(`Could not parse Hyeni text sections from ${file}`);
  }
  const split = (value) => value.trim().split(/\r?\n\s*\r?\n/u).map((p) => p.trim()).filter(Boolean);
  return {
    zazaki: split(zazakiMatch[1]),
    tr: split(turkishMatch[1]),
  };
}

function normalizeForMatching(value) {
  return value
    .normalize('NFC')
    .toLowerCase()
    .replace(/[“”"':;,.!?()\[\]\-]/gu, '')
    .replace(/\s+/gu, '');
}

function groupLinesToParagraphs(lines, paragraphs, startIndex = 0) {
  const groups = [];
  let index = startIndex;
  for (const paragraph of paragraphs) {
    const target = normalizeForMatching(paragraph);
    let accumulated = '';
    const group = [];
    while (index < lines.length) {
      const lineZazaki = lineText(lines[index], 'zazaki');
      const next = normalizeForMatching(accumulated + lineZazaki);
      if (group.length > 0 && !target.startsWith(next) && next.length > target.length) {
        break;
      }
      group.push(lines[index]);
      accumulated += lineZazaki;
      index += 1;
      const normalizedAccumulated = normalizeForMatching(accumulated);
      if (normalizedAccumulated.length >= target.length || normalizedAccumulated === target) {
        break;
      }
    }
    groups.push(group);
  }
  return groups;
}

function cleanJoin(parts) {
  return parts.filter(Boolean).join(' ').replace(/\s+/gu, ' ').trim();
}

function hyeniReadingUnits(lines, zParagraphs, trParagraphs) {
  const bodyZ = zParagraphs.slice(1);
  const bodyTr = trParagraphs.slice(1);
  const groups = groupLinesToParagraphs(lines, bodyZ, 1);
  return bodyZ.map((source, index) => {
    const group = groups[index] || [];
    return {
      id: `u${String(index + 1).padStart(2, '0')}`,
      source,
      translations: {
        tr: bodyTr[index] || '',
        en: cleanJoin(group.map((line) => line.free_translation_en || '')),
      },
      source_line_ids: group.map((line) => line.segment_id),
    };
  });
}

function hyeniGermanParagraphs(file) {
  const paragraphs = mdParagraphs(file);
  const marker = "ich habe einen Menschen von H'yeni getödtet.";
  const splitIndex = paragraphs[2].indexOf(marker);
  const firstBattleStart = splitIndex >= 0
    ? paragraphs[2].slice(0, splitIndex + marker.length).trim()
    : paragraphs[2];
  const firstBattleRest = splitIndex >= 0
    ? paragraphs[2].slice(splitIndex + marker.length).trim()
    : '';
  return [
    cleanJoin([paragraphs[1], firstBattleStart]),
    cleanJoin([firstBattleRest, paragraphs[3], paragraphs[4]]),
    paragraphs[5],
    cleanJoin([paragraphs[6], paragraphs[7]]),
    cleanJoin([paragraphs[8], paragraphs[9]]),
    cleanJoin([paragraphs[10], paragraphs[11]]),
    paragraphs[12],
    cleanJoin([paragraphs[13], paragraphs[14]]),
    paragraphs[15],
    paragraphs[16],
  ];
}

function aliReadingUnits(lines, zParagraphs, enParagraphs, trParagraphs, deParagraphs) {
  const groups = [
    ['a01_l01', 'a01_l05'],
    ['a01_l06', 'a02_l03'],
    ['a02_l04', 'a02_l09'],
    ['a02_l10', 'a03_l01'],
    ['a03_l02', 'a03_l10'],
    ['a03_l11', 'a04_l02'],
    ['a04_l03', 'a04_l08'],
    ['a04_l09', 'a04_l13'],
  ].map(([start, end]) => {
    const startIndex = lines.findIndex((line) => line.segment_id === start);
    const endIndex = lines.findIndex((line) => line.segment_id === end);
    if (startIndex < 0 || endIndex < startIndex) {
      throw new Error(`Bad Ali line group: ${start}-${end}`);
    }
    return lines.slice(startIndex, endIndex + 1);
  });

  return groups.map((group, index) => ({
    id: `u${String(index + 1).padStart(2, '0')}`,
    source: zParagraphs[index] || cleanJoin(group.map((line) => lineText(line, 'zazaki'))),
    translations: {
      en: enParagraphs[index] || '',
      tr: trParagraphs[index] || '',
      de: deParagraphs[index] || '',
    },
    source_line_ids: group.map((line) => line.segment_id),
  }));
}

function aliGermanParagraphs(file) {
  const paragraphs = mdParagraphs(file)
    .filter((paragraph) => !paragraph.startsWith('# '))
    .filter((paragraph) => !paragraph.startsWith('Source:'));
  const p = paragraphs;
  const para8Marker = "Das Heer Qasim Agha's drang vor";
  const p8Index = p[5].indexOf(para8Marker);
  const warningTail = p8Index >= 0 ? p[5].slice(0, p8Index).trim() : '';
  const qasimAttack = p8Index >= 0 ? p[5].slice(p8Index).trim() : p[5];
  const fallMarker = 'Ahmed zog aus des Onkels Brust';
  const fallIndex = p[6].indexOf(fallMarker);
  const ahmedFalls = fallIndex >= 0 ? p[6].slice(0, fallIndex).trim() : '';
  const finalFight = fallIndex >= 0 ? p[6].slice(fallIndex).trim() : p[6];
  return [
    p[0],
    p[1],
    p[2],
    p[3],
    cleanJoin([p[4], warningTail]),
    cleanJoin([qasimAttack, ahmedFalls]),
    finalFight,
    p[7],
  ];
}

function documentPayload(config) {
  const bundleDir = path.join(bundleRoot, config.bundle);
  const targetDir = path.join(lerchRoot, config.slug);
  ensureDir(targetDir);
  copyAssets(path.join(bundleDir, 'assets'), path.join(targetDir, 'assets'));

  const interlinear = readJson(path.join(bundleDir, config.interlinearFile));
  const lines = interlinear.lines || [];
  const sourceLines = lines.map((line) => sourceLine(line, config.sourceLabel));
  const readingUnits = config.readingUnits(bundleDir, lines);

  const textMarkdown = `${config.title}\n\n${readingUnits.map((unit) => unit.source).join('\n\n')}\n`;
  writeText(path.join(targetDir, 'text.zazaki.md'), textMarkdown);
  for (const lang of ['en', 'tr', 'de']) {
    const paragraphs = readingUnits.map((unit) => unit.translations[lang] || '').filter(Boolean);
    if (paragraphs.length > 0) {
      writeText(path.join(targetDir, `translation.${lang}.md`), `${config.translationTitles[lang] || config.title}\n\n${paragraphs.join('\n\n')}\n`);
    }
  }

  fs.copyFileSync(
    path.join(bundleDir, config.morphemeFile),
    assertInsideRepo(path.join(targetDir, 'morphemes.tsv'))
  );

  const payload = {
    schema: 'll_tools_text_document.v1',
    kind: 'corpus_text',
    lesson_id: `lerch-${config.slug}`,
    title: config.title,
    source_label: 'Zazaki',
    translations: config.translations,
    metadata: {
      collection: 'lerch',
      collection_label: 'Peter Lerch Zazaki Texts',
      excerpt: config.excerpt,
      source_author: 'Peter Lerch',
      source_work: 'Forschungen über die Kurden und die iranischen Nordchaldäer / Russian original Zazaki transcriptions',
      story_title_lerch: config.lerchTitle,
      story_title_modern_zazaki: config.title,
      working_status: 'reviewed working edition; not final critical edition',
      created_from: config.createdFrom,
      exported_at: '2026-05-11',
      reader_unit: config.readerUnit,
    },
    summary: {
      lines: lines.length,
      source_lines: sourceLines.length,
      reading_units: readingUnits.length,
      tokens: lines.reduce((sum, line) => sum + ((line.tokens || []).length), 0),
    },
    witnesses: config.witnesses,
    reading_units: readingUnits,
    source_lines: sourceLines,
  };

  writeJson(path.join(targetDir, 'text-document.json'), payload);
  writeJson(path.join(targetDir, 'metadata.json'), {
    id: `lerch-${config.slug}`,
    title: config.title,
    title_lerch: config.lerchTitle,
    author_collector: 'Peter Lerch',
    language: 'Zazaki',
    dialect_region_note: config.dialectNote,
    status: 'reviewed working edition',
    line_count: lines.length,
    token_count: payload.summary.tokens,
    lltools_payload: 'text-document.json',
  });

  return {
    slug: config.slug,
    targetDir,
    sourceLines: sourceLines.length,
    readingUnits: readingUnits.length,
  };
}

const commonBingolUrls = [
  {
    label: 'Bingöl repository PDF',
    url: 'https://bnposta.bingol.edu.tr/bitstream/handle/20.500.12898/600/10053832.pdf?isAllowed=y&sequence=1',
  },
  {
    label: 'YÖK thesis record',
    url: 'https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id=XSxuloAAz12quT5oHaDwnA&no=lqmlps2zRpavNQmdt0OGGQ',
  },
];

const configs = [
  {
    slug: 'kauge-nyerib-u-hyeni',
    bundle: 'lerch_nerib_hyeni_review_bundle',
    interlinearFile: 'lerch_nerib_hyeni_interlinear_data.json',
    morphemeFile: 'lerch_nerib_hyeni_morpheme_segmentation.tsv',
    title: "Kawğê Nyêrib û 'Hyêni",
    lerchTitle: 'Kauγé Ńeríb u Hʿyẹ̄́ni.',
    translationTitles: {
      en: 'The Feud Between Nerib and Hyeni',
      tr: "Nyêrib ile Hyêni'nin Kavgası",
      de: 'Fehde zwischen Nerib und Hyeni',
    },
    translations: {
      tr: { label: 'Turkish' },
      en: { label: 'English' },
      de: { label: 'German' },
    },
    excerpt: "Nyêrib'den bir adamın Hyêni toprağında bir hizmetçiyi öldürmesiyle başlayan, Xalef Ağa ile Daqma Bey arasında savaşa dönüşen ve Ziriki ağalarının arabuluculuğuyla barışla biten bir kan davası anlatısı.",
    sourceLabel: 'Müller 1865',
    createdFrom: 'Lerch Nerib-Hyeni review bundle in Language/Z/Dictionaries/Lerch',
    readerUnit: 'paragraph',
    dialectNote: 'Nerib/Hyeni area material as discussed in local project notes.',
    readingUnits(bundleDir, lines) {
      const parsed = parseHyeniText(path.join(bundleDir, 'hyeni_full_text_zazaki_turkish.md'));
      const de = hyeniGermanParagraphs(path.join(bundleDir, 'hyeni_german_translation_transcription.txt'));
      return hyeniReadingUnits(lines, parsed.zazaki, parsed.tr).map((unit, index) => ({
        ...unit,
        translations: {
          ...unit.translations,
          de: de[index] || '',
        },
      }));
    },
    witnesses: [
      {
        label: 'Russian original edition',
        citation: 'Lerch, Peter Ivanovich. Izsledovaniia ob iranskikh kurdakh i ikh predkakh, severnykh khaldeiakh. Vol. 1. St. Petersburg: Imperial Academy of Sciences, 1856. Story on the Nerib-Hyeni feud, printed pp. 108-116.',
        pages: 'Russian RGO viewer images 122-130; printed pp. 108-116.',
        note: "Primary scan witness for Lerch's Zazaki transcription and Russian free translation.",
        urls: [
          {
            label: 'RGO viewer, story start',
            url: 'https://elib.rgo.ru/safe-view/123456789/218398/1/MTAwMDAyMTBfTGVya2gsIFBldHIgSXZhbm92aWNoICgxODI3LTE4ODQpLiBJc3NsZWRvdmFuaXlhIG8ucGRm#122',
          },
        ],
      },
      {
        label: 'German edition / reprint scan',
        citation: "Lerch, Peter. Forschungen über die Kurden und die iranischen Nordchaldäer. Abth. 1. St. Petersburg: Kaiserliche Akademie der Wissenschaften, 1857. Story 'Fehde zwischen Nerib und H'yeni,' pp. 71-79.",
        pages: 'Internet Archive scan pages n114-n122; printed pp. 71-79.',
        note: 'Used for the German free translation and as a second scan witness for the Zazaki transcription.',
        urls: [
          {
            label: 'Internet Archive, story start',
            url: 'https://archive.org/details/bub_gb_WlGVYoEkr7sC/page/n114/mode/1up',
          },
          {
            label: 'Internet Archive item',
            url: 'https://archive.org/details/bub_gb_WlGVYoEkr7sC',
          },
        ],
      },
      {
        label: 'Bingöl University thesis transcription',
        citation: "Aslanoğulları, Mehmet. Lerch'in Zazaki Derlemelerinin Çevrimyazımı ve Türlerine Göre Sözcüklerin Tahlili. Master's thesis, Bingöl Üniversitesi, 2014.",
        pages: 'PDF pp. 56-64; story heading "Qewğê Nêrib û Hêni."',
        note: 'Secondary transcription witness used during alignment and review. The transcription text is cited here but is not reproduced in the Interlinear view.',
        urls: commonBingolUrls,
      },
    ],
  },
  {
    slug: 'ali-agha-ladi-kelhani',
    bundle: 'lerch_ali_agha_review_bundle',
    interlinearFile: 'lerch_ali_agha_interlinear_data.json',
    morphemeFile: 'lerch_ali_agha_morpheme_segmentation.tsv',
    title: "Ali Ağa, Laci Kêlhani",
    lerchTitle: 'Áli aγá lā́d̮i Kelháni',
    translationTitles: {
      en: 'Ali Agha, Son of Kelhan',
      tr: "Kelhan'ın Oğlu Ali Ağa",
      de: "Ali Agha, der Sohn Kelhän's",
    },
    translations: {
      tr: { label: 'Turkish' },
      en: { label: 'English' },
      de: { label: 'German' },
    },
    excerpt: "Kelhan'ın oğlu Ali Ağa'nın Karbegan'daki gücü, Qasım Ağa ile Hasan Ağa'nın kurduğu tuzak, Ali Ağa'nın ailesinin öldürülmesi ve cenazelerin defnedilmesini anlatan bir kan davası hikayesi.",
    sourceLabel: 'Müller 1865',
    createdFrom: 'Lerch Ali Agha review bundle in Language/Z/Dictionaries/Lerch',
    readerUnit: 'paragraph',
    dialectNote: 'Karbegan/Sivan-area material as discussed in local project notes.',
    readingUnits(bundleDir, lines) {
      const en = bodyParagraphs(path.join(bundleDir, 'ali_agha_english_free_translation.md'));
      const tr = bodyParagraphs(path.join(bundleDir, 'ali_agha_turkish_free_translation.md'));
      const de = aliGermanParagraphs(path.join(bundleDir, 'ali_agha_german_free_translation_transcription.md'));
      const zGroups = [
        ['a01_l01', 'a01_l05'],
        ['a01_l06', 'a02_l03'],
        ['a02_l04', 'a02_l09'],
        ['a02_l10', 'a03_l01'],
        ['a03_l02', 'a03_l10'],
        ['a03_l11', 'a04_l02'],
        ['a04_l03', 'a04_l08'],
        ['a04_l09', 'a04_l13'],
      ].map(([start, end]) => {
        const startIndex = lines.findIndex((line) => line.segment_id === start);
        const endIndex = lines.findIndex((line) => line.segment_id === end);
        return cleanJoin(lines.slice(startIndex, endIndex + 1).map((line) => lineText(line, 'zazaki')));
      });
      return aliReadingUnits(lines, zGroups, en, tr, de);
    },
    witnesses: [
      {
        label: 'Russian original edition',
        citation: "Lerch, Peter Ivanovich. Izsledovaniia ob iranskikh kurdakh i ikh predkakh, severnykh khaldeiakh. Vol. 1. St. Petersburg: Imperial Academy of Sciences, 1856. Text 3, Ali Agha narrative, printed pp. 99-102.",
        pages: 'Russian RGO viewer images 113-116; printed pp. 99-102.',
        note: "Primary scan witness for Lerch's Zazaki transcription and Russian free translation; the Russian scan prints only the heading '3.' for this text.",
        urls: [
          {
            label: 'RGO viewer, story start',
            url: 'https://elib.rgo.ru/safe-view/123456789/218398/1/MTAwMDAyMTBfTGVya2gsIFBldHIgSXZhbm92aWNoICgxODI3LTE4ODQpLiBJc3NsZWRvdmFuaXlhIG8ucGRm#113',
          },
        ],
      },
      {
        label: 'German edition / reprint scan',
        citation: "Lerch, Peter. Forschungen über die Kurden und die iranischen Nordchaldäer. Abth. 1. St. Petersburg: Kaiserliche Akademie der Wissenschaften, 1857. Story 'Ali Agha, der Sohn Kelhän's,' pp. 61-65.",
        pages: 'Internet Archive scan pages n104-n108; printed pp. 61-65.',
        note: 'Used for the German free translation and as a second scan witness for the Zazaki transcription.',
        urls: [
          {
            label: 'Internet Archive, story start',
            url: 'https://archive.org/details/bub_gb_WlGVYoEkr7sC/page/n104/mode/1up',
          },
          {
            label: 'Internet Archive item',
            url: 'https://archive.org/details/bub_gb_WlGVYoEkr7sC',
          },
        ],
      },
      {
        label: 'Bingöl University thesis transcription',
        citation: "Aslanoğulları, Mehmet. Lerch'in Zazaki Derlemelerinin Çevrimyazımı ve Türlerine Göre Sözcüklerin Tahlili. Master's thesis, Bingöl Üniversitesi, 2014.",
        pages: 'PDF pp. 47-50; story heading "Meselê Eli Ağay Laci Kelxoni Qerbegoni."',
        note: 'Secondary transcription witness used during alignment and review. The transcription text is cited here but is not reproduced in the Interlinear view.',
        urls: commonBingolUrls,
      },
    ],
  },
];

const results = configs.map(documentPayload);
console.log(JSON.stringify(results, null, 2));
