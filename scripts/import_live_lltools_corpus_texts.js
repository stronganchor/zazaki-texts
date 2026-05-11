#!/usr/bin/env node
/* eslint-disable no-console */

const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const defaultManifestPath = path.join(repoRoot, 'dist', 'lltools-lerch-texts-webp-import', 'manifest.json');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) {
      continue;
    }
    const eq = arg.indexOf('=');
    if (eq !== -1) {
      args[arg.slice(2, eq)] = arg.slice(eq + 1);
      continue;
    }
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      args[key] = next;
      i += 1;
    } else {
      args[key] = '1';
    }
  }
  return args;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchWithTimeout(url, options, timeoutMs) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, {
      ...options,
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }
}

async function retryRequest(label, attempts, fn) {
  let lastError = null;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    try {
      return await fn(attempt);
    } catch (error) {
      lastError = error;
      if (attempt >= attempts) {
        break;
      }
      console.warn(`  retry ${attempt}/${attempts - 1} for ${label}: ${error.message}`);
      await sleep(2000 * attempt);
    }
  }
  throw lastError;
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function readCookieHeader(cookieFile, siteUrl) {
  const host = new URL(siteUrl).hostname.replace(/^www\./, '');
  const lines = fs.readFileSync(cookieFile, 'utf8').split(/\r?\n/);
  const pairs = [];
  for (const line of lines) {
    if (!line || line.startsWith('# ') || line.startsWith('# Netscape')) {
      continue;
    }
    const normalized = line.startsWith('#HttpOnly_') ? line.slice('#HttpOnly_'.length) : line;
    const parts = normalized.split('\t');
    if (parts.length < 7) {
      continue;
    }
    const domain = parts[0].replace(/^\./, '').replace(/^www\./, '');
    if (domain !== host && !host.endsWith(`.${domain}`)) {
      continue;
    }
    const name = parts[5];
    const value = parts.slice(6).join('\t');
    if (name && value) {
      pairs.push(`${name}=${value}`);
    }
  }
  if (pairs.length === 0) {
    throw new Error(`No cookies for ${host} found in ${cookieFile}`);
  }
  return pairs.join('; ');
}

function collectWitnessAssets(payload) {
  const assets = new Map();
  const sourceLines = Array.isArray(payload.source_lines) ? payload.source_lines : [];
  for (const line of sourceLines) {
    const witnesses = line && Array.isArray(line.witnesses) ? line.witnesses : [];
    for (const witness of witnesses) {
      if (!witness || typeof witness.image_url !== 'string') {
        continue;
      }
      const imageUrl = witness.image_url.trim().replace(/\\/g, '/');
      if (!imageUrl || /^[a-z][a-z0-9+.-]*:/i.test(imageUrl) || imageUrl.startsWith('/')) {
        continue;
      }
      assets.set(imageUrl, imageUrl);
    }
  }
  return Array.from(assets.keys()).sort();
}

function replaceWitnessAsset(payload, relativePath, uploaded) {
  const sourceLines = Array.isArray(payload.source_lines) ? payload.source_lines : [];
  for (const line of sourceLines) {
    const witnesses = line && Array.isArray(line.witnesses) ? line.witnesses : [];
    for (const witness of witnesses) {
      if (!witness || typeof witness.image_url !== 'string') {
        continue;
      }
      const imageUrl = witness.image_url.trim().replace(/\\/g, '/');
      if (imageUrl !== relativePath) {
        continue;
      }
      witness.source_asset = relativePath;
      witness.image_url = uploaded.url;
      witness.attachment_id = uploaded.attachment_id;
    }
  }
}

async function postJson(siteUrl, route, nonce, cookieHeader, body, timeoutMs, retries) {
  const url = `${siteUrl.replace(/\/$/, '')}${route}`;
  const jsonBody = JSON.stringify(body);
  return retryRequest(route, retries + 1, async () => {
    const res = await fetchWithTimeout(url, {
      method: 'POST',
      headers: {
        Cookie: cookieHeader,
        'X-WP-Nonce': nonce,
        'Content-Type': 'application/json',
      },
      body: jsonBody,
    }, timeoutMs);
    const text = await res.text();
    let data = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch (error) {
      throw new Error(`Non-JSON response from ${route}: HTTP ${res.status}: ${text.slice(0, 500)}`);
    }
    if (!res.ok) {
      throw new Error(`HTTP ${res.status} from ${route}: ${JSON.stringify(data)}`);
    }
    return data;
  });
}

async function uploadAsset(siteUrl, nonce, cookieHeader, assetPath, sourceKey, postId, timeoutMs, retries) {
  const url = `${siteUrl.replace(/\/$/, '')}/wp-json/ll-tools/v1/corpus-texts/asset`;
  const bytes = await fs.promises.readFile(assetPath);
  return retryRequest(sourceKey, retries + 1, async () => {
    const form = new FormData();
    const blob = new Blob([bytes], { type: 'image/webp' });
    form.append('asset', blob, path.basename(assetPath));
    form.append('source_key', sourceKey);
    if (postId > 0) {
      form.append('post_id', String(postId));
    }

    const res = await fetchWithTimeout(url, {
      method: 'POST',
      headers: {
        Cookie: cookieHeader,
        'X-WP-Nonce': nonce,
      },
      body: form,
    }, timeoutMs);
    const text = await res.text();
    let data = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch (error) {
      throw new Error(`Non-JSON asset upload response for ${sourceKey}: HTTP ${res.status}: ${text.slice(0, 500)}`);
    }
    if (!res.ok || !data || !data.url) {
      throw new Error(`Asset upload failed for ${sourceKey}: HTTP ${res.status}: ${JSON.stringify(data)}`);
    }
    return data;
  });
}

async function importText({ siteUrl, nonce, cookieHeader, textEntry, delayMs, timeoutMs, retries, status }) {
  const payloadPath = path.join(repoRoot, textEntry.payload);
  const payloadDir = path.dirname(payloadPath);
  const payload = readJson(payloadPath);
  const lessonId = String(payload.lesson_id || textEntry.lesson_id || textEntry.slug).trim();
  const postSlug = String(lessonId || `lerch-${textEntry.slug}`).trim();
  const assets = collectWitnessAssets(payload);

  console.log(`\n${postSlug}: ${assets.length} assets`);
  let uploadedCount = 0;
  let reusedCount = 0;
  for (const relativePath of assets) {
    const assetPath = path.join(payloadDir, relativePath.replace(/\//g, path.sep));
    if (!fs.existsSync(assetPath)) {
      throw new Error(`Missing asset for ${postSlug}: ${relativePath}`);
    }
    const sourceKey = `${lessonId}/${relativePath}`;
    const uploaded = await uploadAsset(siteUrl, nonce, cookieHeader, assetPath, sourceKey, 0, timeoutMs, retries);
    replaceWitnessAsset(payload, relativePath, uploaded);
    if (uploaded.created) {
      uploadedCount += 1;
    } else {
      reusedCount += 1;
    }
    if ((uploadedCount + reusedCount) % 25 === 0 || uploadedCount + reusedCount === assets.length) {
      console.log(`  ${uploadedCount + reusedCount}/${assets.length} assets (${uploadedCount} new, ${reusedCount} reused)`);
    }
    if (delayMs > 0) {
      await sleep(delayMs);
    }
  }

  const imported = await postJson(siteUrl, '/wp-json/ll-tools/v1/corpus-texts/import', nonce, cookieHeader, {
    post_slug: postSlug,
    status,
    source: `zazaki-texts:${textEntry.payload}`,
    payload,
  }, timeoutMs, retries);
  console.log(`  ${imported.action}: ${imported.url}`);
  return {
    slug: textEntry.slug,
    lesson_id: lessonId,
    post_id: imported.post_id,
    url: imported.url,
    assets: assets.length,
    uploaded: uploadedCount,
    reused: reusedCount,
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const siteUrl = args.site || process.env.LLTOOLS_SITE || 'https://zazacaogren.com';
  const cookieFile = args.cookie || process.env.LLTOOLS_COOKIE_FILE || path.join(process.env.TEMP || '', 'zazacaogren-live-cookies.txt');
  const nonce = args.nonce || process.env.LLTOOLS_REST_NONCE || '';
  const manifestPath = args.manifest || defaultManifestPath;
  const delayMs = Number.parseInt(args.delay || process.env.LLTOOLS_IMPORT_DELAY_MS || '250', 10);
  const timeoutMs = Number.parseInt(args.timeout || process.env.LLTOOLS_IMPORT_TIMEOUT_MS || '60000', 10);
  const retries = Number.parseInt(args.retries || process.env.LLTOOLS_IMPORT_RETRIES || '2', 10);
  const status = args.status || process.env.LLTOOLS_IMPORT_STATUS || 'publish';
  const only = new Set(
    String(args.only || process.env.LLTOOLS_TEXT_SLUGS || '')
      .split(',')
      .map((value) => value.trim())
      .filter(Boolean)
  );

  if (!nonce) {
    throw new Error('Provide --nonce or LLTOOLS_REST_NONCE.');
  }
  if (!fs.existsSync(cookieFile)) {
    throw new Error(`Cookie file not found: ${cookieFile}`);
  }

  const manifest = readJson(manifestPath);
  let texts = Array.isArray(manifest.texts) ? manifest.texts : [];
  if (only.size > 0) {
    texts = texts.filter((entry) => only.has(entry.slug) || only.has(entry.lesson_id));
  }
  if (texts.length === 0) {
    throw new Error('No texts matched the requested import filter.');
  }

  const cookieHeader = readCookieHeader(cookieFile, siteUrl);
  const results = [];
  for (const textEntry of texts) {
    results.push(await importText({ siteUrl, nonce, cookieHeader, textEntry, delayMs, timeoutMs, retries, status }));
    await sleep(1000);
  }

  console.log('\nImport complete:');
  for (const result of results) {
    console.log(`- ${result.lesson_id}: ${result.url} (${result.assets} assets, ${result.uploaded} new, ${result.reused} reused)`);
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
