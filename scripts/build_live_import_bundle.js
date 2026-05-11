const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const textsRoot = path.join(repoRoot, 'texts', 'lerch');
const outRoot = path.join(repoRoot, 'dist', 'lltools-lerch-texts-webp-import');

function assertInsideRepo(targetPath) {
  const resolved = path.resolve(targetPath);
  const rootWithSep = repoRoot.endsWith(path.sep) ? repoRoot : repoRoot + path.sep;
  if (resolved !== repoRoot && !resolved.startsWith(rootWithSep)) {
    throw new Error(`Refusing to write outside repo: ${resolved}`);
  }
  return resolved;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, value) {
  fs.mkdirSync(assertInsideRepo(path.dirname(file)), { recursive: true });
  fs.writeFileSync(assertInsideRepo(file), `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function writeText(file, value) {
  fs.mkdirSync(assertInsideRepo(path.dirname(file)), { recursive: true });
  fs.writeFileSync(assertInsideRepo(file), value.replace(/\s+$/u, '') + '\n', 'utf8');
}

function copyFile(source, target) {
  fs.mkdirSync(assertInsideRepo(path.dirname(target)), { recursive: true });
  fs.copyFileSync(source, assertInsideRepo(target));
}

function collectImageRefs(value, refs = new Set()) {
  if (Array.isArray(value)) {
    value.forEach((item) => collectImageRefs(item, refs));
  } else if (value && typeof value === 'object') {
    Object.values(value).forEach((item) => collectImageRefs(item, refs));
  } else if (typeof value === 'string' && /\.(?:jpe?g|png|webp)$/i.test(value)) {
    refs.add(value);
  }
  return refs;
}

function textDirs() {
  return fs.readdirSync(textsRoot)
    .map((entry) => path.join(textsRoot, entry))
    .filter((dir) => fs.existsSync(path.join(dir, 'text-document.json')))
    .sort();
}

fs.rmSync(assertInsideRepo(outRoot), { recursive: true, force: true });
fs.mkdirSync(assertInsideRepo(outRoot), { recursive: true });

copyFile(path.join(repoRoot, 'README.md'), path.join(outRoot, 'README.md'));
copyFile(path.join(repoRoot, 'docs', 'lltools-text-document-v1.md'), path.join(outRoot, 'docs', 'lltools-text-document-v1.md'));
copyFile(path.join(repoRoot, 'scripts', 'import_lltools_corpus_text.php'), path.join(outRoot, 'scripts', 'import_lltools_corpus_text.php'));

const manifest = {
  generated_at: new Date().toISOString(),
  purpose: 'Minimal LL Tools live import bundle for Peter Lerch Zazaki corpus text posts.',
  notes: [
    'Includes only text payload files and referenced WebP line-crop assets.',
    'Original JPG/PNG crop files are intentionally excluded from this bundle.',
    'Run the importer after the live site has an LL Tools build that supports corpus_text documents.',
  ],
  texts: [],
};

const commands = [
  '# LL Tools Lerch Text Import Commands',
  '',
  'Replace `/path/to/wordpress` with the live WordPress document root containing `wp-load.php`.',
  'Run from this bundle root after the updated Language Learner Tools plugin is active.',
  '',
];

for (const textDir of textDirs()) {
  const slug = path.basename(textDir);
  const targetDir = path.join(outRoot, 'texts', 'lerch', slug);
  const payloadPath = path.join(textDir, 'text-document.json');
  const payload = readJson(payloadPath);
  const refs = [...collectImageRefs(payload)].sort();
  const copiedAssets = [];

  for (const entry of fs.readdirSync(textDir)) {
    const source = path.join(textDir, entry);
    if (fs.statSync(source).isFile() && entry !== 'text-document.json') {
      copyFile(source, path.join(targetDir, entry));
    }
  }
  copyFile(payloadPath, path.join(targetDir, 'text-document.json'));

  for (const ref of refs) {
    if (!/\.webp$/i.test(ref)) {
      throw new Error(`${slug} still references a non-WebP image: ${ref}`);
    }
    const source = path.join(textDir, ref.replace(/[\\/]/g, path.sep));
    if (!fs.existsSync(source)) {
      throw new Error(`${slug} references a missing asset: ${ref}`);
    }
    const size = fs.statSync(source).size;
    if (size > 300 * 1024) {
      throw new Error(`${slug} asset is above 300 KB: ${ref}`);
    }
    copyFile(source, path.join(targetDir, ref.replace(/[\\/]/g, path.sep)));
    copiedAssets.push({ path: ref, bytes: size });
  }

  manifest.texts.push({
    slug,
    lesson_id: payload.lesson_id || '',
    title: payload.title || '',
    payload: `texts/lerch/${slug}/text-document.json`,
    assets: copiedAssets.length,
    total_asset_bytes: copiedAssets.reduce((sum, item) => sum + item.bytes, 0),
    largest_asset_bytes: Math.max(0, ...copiedAssets.map((item) => item.bytes)),
  });

  commands.push(
    [
      '```bash',
      `php scripts/import_lltools_corpus_text.php --wp-root="/path/to/wordpress" --payload="texts/lerch/${slug}/text-document.json" --status=publish --no-wordset`,
      '```',
      '',
    ].join('\n')
  );
}

commands.push(
  'After import, use this shortcode on the Peter Lerch collection page:',
  '',
  '```text',
  '[ll_corpus_text_grid collection="lerch"]',
  '```',
  ''
);

writeJson(path.join(outRoot, 'manifest.json'), manifest);
writeText(path.join(outRoot, 'IMPORT_COMMANDS.md'), commands.join('\n'));

console.log(JSON.stringify({
  bundle_dir: path.relative(repoRoot, outRoot).replace(/\\/g, '/'),
  texts: manifest.texts.length,
  assets: manifest.texts.reduce((sum, item) => sum + item.assets, 0),
  total_asset_bytes: manifest.texts.reduce((sum, item) => sum + item.total_asset_bytes, 0),
  largest_asset_bytes: Math.max(0, ...manifest.texts.map((item) => item.largest_asset_bytes)),
}, null, 2));
