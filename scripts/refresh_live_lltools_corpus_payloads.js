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

async function requestJson(siteUrl, route, nonce, cookieHeader, options = {}) {
  const url = `${siteUrl.replace(/\/$/, '')}${route}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      Cookie: cookieHeader,
      'X-WP-Nonce': nonce,
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...(options.headers || {}),
    },
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch (error) {
    throw new Error(`Non-JSON response from ${route}: HTTP ${res.status}: ${text.slice(0, 500)}`);
  }
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status} from ${route}: ${JSON.stringify(data)}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

function sourceLines(payload) {
  return Array.isArray(payload && payload.source_lines) ? payload.source_lines : [];
}

function witnessAssetKey(witness) {
  if (!witness || typeof witness !== 'object') {
    return '';
  }
  const sourceAsset = typeof witness.source_asset === 'string' ? witness.source_asset.trim().replace(/\\/g, '/') : '';
  if (sourceAsset) {
    return sourceAsset;
  }
  const imageUrl = typeof witness.image_url === 'string' ? witness.image_url.trim().replace(/\\/g, '/') : '';
  if (!imageUrl || /^[a-z][a-z0-9+.-]*:/i.test(imageUrl) || imageUrl.startsWith('/')) {
    return '';
  }
  return imageUrl;
}

function buildLiveAssetMap(livePayload) {
  const map = new Map();
  for (const line of sourceLines(livePayload)) {
    const witnesses = Array.isArray(line && line.witnesses) ? line.witnesses : [];
    for (const witness of witnesses) {
      const key = witnessAssetKey(witness);
      if (!key || typeof witness.image_url !== 'string' || !/^[a-z][a-z0-9+.-]*:/i.test(witness.image_url)) {
        continue;
      }
      map.set(key, {
        image_url: witness.image_url,
        attachment_id: witness.attachment_id || 0,
      });
    }
  }
  return map;
}

function preserveLiveWitnessAssets(localPayload, livePayload) {
  const liveAssets = buildLiveAssetMap(livePayload);
  let replaced = 0;
  let missing = 0;

  for (const line of sourceLines(localPayload)) {
    const witnesses = Array.isArray(line && line.witnesses) ? line.witnesses : [];
    for (const witness of witnesses) {
      const key = witnessAssetKey(witness);
      if (!key) {
        continue;
      }
      const live = liveAssets.get(key);
      if (!live) {
        missing += 1;
        continue;
      }
      witness.source_asset = key;
      witness.image_url = live.image_url;
      if (live.attachment_id) {
        witness.attachment_id = live.attachment_id;
      }
      replaced += 1;
    }
  }

  return { replaced, missing };
}

async function main() {
  const args = parseArgs(process.argv);
  const siteUrl = args.site || process.env.LLTOOLS_SITE || 'https://zazacaogren.com';
  const cookieFile = args.cookie || process.env.LLTOOLS_COOKIE_FILE || path.join(process.env.TEMP || '', 'zazacaogren-live-cookies.txt');
  const nonce = args.nonce || process.env.LLTOOLS_REST_NONCE || '';
  const manifestPath = args.manifest || defaultManifestPath;
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
  for (const textEntry of texts) {
    const payload = readJson(path.join(repoRoot, textEntry.payload));
    const lessonId = String(payload.lesson_id || textEntry.lesson_id || textEntry.slug).trim();
    const postSlug = String(lessonId || `lerch-${textEntry.slug}`).trim();
    const live = await requestJson(
      siteUrl,
      `/wp-json/ll-tools/v1/corpus-texts/${encodeURIComponent(postSlug)}`,
      nonce,
      cookieHeader
    );
    const preserved = preserveLiveWitnessAssets(payload, live.payload || {});
    if (preserved.missing > 0) {
      throw new Error(`${postSlug}: ${preserved.missing} witness assets were not found in the live payload.`);
    }
    const imported = await requestJson(siteUrl, '/wp-json/ll-tools/v1/corpus-texts/import', nonce, cookieHeader, {
      method: 'POST',
      body: JSON.stringify({
        post_slug: postSlug,
        status,
        source: `zazaki-texts:${textEntry.payload}`,
        payload,
      }),
    });
    console.log(`${postSlug}: ${imported.action}, ${preserved.replaced} asset URLs preserved`);
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
