const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const repoRoot = path.resolve(__dirname, '..');
const defaultTextsRoot = path.join(repoRoot, 'texts', 'lerch');
const maxBytes = Number.parseInt(process.env.MAX_IMAGE_BYTES || `${300 * 1024}`, 10);
const webpQualities = [92, 88, 82, 76, 70, 64, 58, 52];

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
  fs.writeFileSync(assertInsideRepo(file), `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function isImageRef(value) {
  return typeof value === 'string' && /\.(?:jpe?g|png|webp)$/i.test(value);
}

function collectImageRefs(value, refs = new Set()) {
  if (Array.isArray(value)) {
    value.forEach((item) => collectImageRefs(item, refs));
  } else if (value && typeof value === 'object') {
    Object.values(value).forEach((item) => collectImageRefs(item, refs));
  } else if (isImageRef(value)) {
    refs.add(value);
  }
  return refs;
}

function replaceImageRefs(value, replacements) {
  if (Array.isArray(value)) {
    return value.map((item) => replaceImageRefs(item, replacements));
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, replaceImageRefs(item, replacements)])
    );
  }
  return typeof value === 'string' && replacements.has(value) ? replacements.get(value) : value;
}

function runMagick(args) {
  const result = spawnSync('magick', args, { encoding: 'utf8' });
  if (result.status !== 0) {
    throw new Error((result.stderr || result.stdout || 'ImageMagick failed').trim());
  }
}

function convertToWebp(inputPath, outputPath) {
  fs.mkdirSync(assertInsideRepo(path.dirname(outputPath)), { recursive: true });

  runMagick([
    inputPath,
    '-auto-orient',
    '-strip',
    '-define',
    'webp:lossless=true',
    '-define',
    'webp:method=6',
    outputPath,
  ]);
  let size = fs.statSync(outputPath).size;
  if (size <= maxBytes) {
    return { size, mode: 'lossless' };
  }

  for (const quality of webpQualities) {
    runMagick([
      inputPath,
      '-auto-orient',
      '-strip',
      '-quality',
      String(quality),
      '-define',
      'webp:method=6',
      outputPath,
    ]);
    size = fs.statSync(outputPath).size;
    if (size <= maxBytes) {
      return { size, mode: `lossy-q${quality}` };
    }
  }

  throw new Error(`${outputPath} is still above ${maxBytes} bytes after WebP conversion`);
}

function textDirsFromArgs() {
  const args = process.argv.slice(2).filter((arg) => !arg.startsWith('--'));
  if (args.length > 0) {
    return args.map((arg) => path.resolve(repoRoot, arg));
  }
  return fs.readdirSync(defaultTextsRoot)
    .map((entry) => path.join(defaultTextsRoot, entry))
    .filter((dir) => fs.existsSync(path.join(dir, 'text-document.json')));
}

const dryRun = process.argv.includes('--dry-run');
const report = [];

for (const textDir of textDirsFromArgs()) {
  const payloadPath = path.join(textDir, 'text-document.json');
  if (!fs.existsSync(payloadPath)) {
    continue;
  }

  const payload = readJson(payloadPath);
  const refs = [...collectImageRefs(payload)].sort();
  const replacements = new Map();
  const converted = [];
  const existingWebp = [];

  for (const ref of refs) {
    const inputPath = path.join(textDir, ref.replace(/[\\/]/g, path.sep));
    if (!fs.existsSync(inputPath)) {
      throw new Error(`Missing image referenced by ${payloadPath}: ${ref}`);
    }

    if (/\.webp$/i.test(ref)) {
      const size = fs.statSync(inputPath).size;
      if (size > maxBytes) {
        throw new Error(`${ref} is ${size} bytes, above ${maxBytes}`);
      }
      existingWebp.push({ ref, size });
      continue;
    }

    const webpRef = ref.replace(/\.(?:jpe?g|png)$/i, '.webp');
    const outputPath = path.join(textDir, webpRef.replace(/[\\/]/g, path.sep));
    if (!dryRun) {
      const result = convertToWebp(inputPath, outputPath);
      converted.push({ from: ref, to: webpRef, ...result });
    } else {
      converted.push({ from: ref, to: webpRef, size: 0, mode: 'dry-run' });
    }
    replacements.set(ref, webpRef);
  }

  if (replacements.size > 0 && !dryRun) {
    writeJson(payloadPath, replaceImageRefs(payload, replacements));
  }

  report.push({
    text: path.relative(repoRoot, textDir).replace(/\\/g, '/'),
    payload: path.relative(repoRoot, payloadPath).replace(/\\/g, '/'),
    references: refs.length,
    converted: converted.length,
    existingWebp: existingWebp.length,
    totalWebpBytes: converted.reduce((sum, item) => sum + item.size, 0)
      + existingWebp.reduce((sum, item) => sum + item.size, 0),
    largestWebpBytes: Math.max(0, ...converted.map((item) => item.size), ...existingWebp.map((item) => item.size)),
    modes: [...new Set(converted.map((item) => item.mode))].sort(),
  });
}

console.log(JSON.stringify(report, null, 2));
