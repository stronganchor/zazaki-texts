<?php
/**
 * Import a repository text-document payload into an LL Tools content lesson.
 *
 * Usage:
 * php scripts/import_lltools_corpus_text.php \
 *   --wp-root="/path/to/wordpress" \
 *   --payload="texts/lerch/kauge-nyerib-u-sivani/text-document.json" \
 *   --post-slug="lerch-kauge-nyerib-u-sivani" \
 *   --status="publish"
 */

declare(strict_types=1);

function ll_texts_import_fail(string $message, int $code = 1): void {
    fwrite(STDERR, $message . PHP_EOL);
    exit($code);
}

function ll_texts_import_option(array $options, string $key, string $default = ''): string {
    $value = $options[$key] ?? $default;
    return is_scalar($value) ? trim((string) $value) : $default;
}

function ll_texts_import_normalize_path(string $path): string {
    return str_replace('\\', '/', $path);
}

function ll_texts_import_is_relative_path(string $path): bool {
    if ($path === '') {
        return false;
    }
    if (preg_match('/^[a-z][a-z0-9+.-]*:/i', $path)) {
        return false;
    }
    return !preg_match('/^(?:[A-Za-z]:[\/\\\\]|[\/\\\\]{2}|[\/\\\\])/', $path);
}

function ll_texts_import_find_post_by_slug(string $slug): ?WP_Post {
    $posts = get_posts([
        'post_type' => 'll_content_lesson',
        'post_status' => ['publish', 'draft', 'pending', 'private', 'future'],
        'name' => $slug,
        'posts_per_page' => 1,
        'no_found_rows' => true,
    ]);
    $post = $posts[0] ?? null;
    return $post instanceof WP_Post ? $post : null;
}

function ll_texts_import_ensure_wordset(string $slug, string $name): int {
    $slug = sanitize_title($slug);
    if ($slug === '') {
        ll_texts_import_fail('Provide a non-empty --wordset-slug.');
    }

    $term = get_term_by('slug', $slug, 'wordset');
    if ($term instanceof WP_Term && !is_wp_error($term)) {
        return (int) $term->term_id;
    }

    $inserted = wp_insert_term($name !== '' ? $name : $slug, 'wordset', ['slug' => $slug]);
    if (is_wp_error($inserted)) {
        ll_texts_import_fail('Could not create wordset: ' . $inserted->get_error_message());
    }

    return (int) ($inserted['term_id'] ?? 0);
}

function ll_texts_import_find_attachment_by_source(string $source_key): int {
    $attachments = get_posts([
        'post_type' => 'attachment',
        'post_status' => 'inherit',
        'posts_per_page' => 1,
        'fields' => 'ids',
        'no_found_rows' => true,
        'meta_query' => [
            [
                'key' => '_ll_texts_source_asset',
                'value' => $source_key,
            ],
        ],
    ]);

    return !empty($attachments) ? (int) $attachments[0] : 0;
}

function ll_texts_import_asset(string $asset_path, int $post_id, string $source_key = ''): array {
    $real_path = realpath($asset_path);
    if (!is_string($real_path) || $real_path === '' || !is_file($real_path)) {
        return ['attachment_id' => 0, 'url' => ''];
    }

    $legacy_source_key = ll_texts_import_normalize_path($real_path);
    $source_key = $source_key !== '' ? ll_texts_import_normalize_path($source_key) : $legacy_source_key;
    $existing_id = ll_texts_import_find_attachment_by_source($source_key);
    if ($existing_id <= 0 && $source_key !== $legacy_source_key) {
        $existing_id = ll_texts_import_find_attachment_by_source($legacy_source_key);
        if ($existing_id > 0) {
            update_post_meta($existing_id, '_ll_texts_source_asset', $source_key);
        }
    }
    if ($existing_id > 0) {
        $existing_url = wp_get_attachment_url($existing_id);
        return ['attachment_id' => $existing_id, 'url' => is_string($existing_url) ? $existing_url : ''];
    }

    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/image.php';

    $contents = file_get_contents($real_path);
    if (!is_string($contents)) {
        return ['attachment_id' => 0, 'url' => ''];
    }

    $upload = wp_upload_bits(basename($real_path), null, $contents);
    if (!empty($upload['error']) || empty($upload['file'])) {
        return ['attachment_id' => 0, 'url' => ''];
    }

    $filetype = wp_check_filetype((string) $upload['file']);
    $attachment_id = wp_insert_attachment([
        'post_mime_type' => (string) ($filetype['type'] ?? 'image/jpeg'),
        'post_title' => sanitize_file_name(pathinfo($real_path, PATHINFO_FILENAME)),
        'post_content' => '',
        'post_status' => 'inherit',
    ], (string) $upload['file'], $post_id);

    if (is_wp_error($attachment_id) || (int) $attachment_id <= 0) {
        return ['attachment_id' => 0, 'url' => ''];
    }

    $attachment_id = (int) $attachment_id;
    $metadata = wp_generate_attachment_metadata($attachment_id, (string) $upload['file']);
    if (is_array($metadata)) {
        wp_update_attachment_metadata($attachment_id, $metadata);
    }
    update_post_meta($attachment_id, '_ll_texts_source_asset', $source_key);

    $url = wp_get_attachment_url($attachment_id);
    return ['attachment_id' => $attachment_id, 'url' => is_string($url) ? $url : ''];
}

function ll_texts_import_prepare_payload_images(array $payload, string $payload_dir, int $post_id): array {
    if (empty($payload['source_lines']) || !is_array($payload['source_lines'])) {
        return $payload;
    }

    $lesson_id = isset($payload['lesson_id']) && is_scalar($payload['lesson_id'])
        ? sanitize_title((string) $payload['lesson_id'])
        : sanitize_title(basename($payload_dir));

    foreach ($payload['source_lines'] as &$line) {
        if (!is_array($line) || empty($line['witnesses']) || !is_array($line['witnesses'])) {
            continue;
        }

        foreach ($line['witnesses'] as &$witness) {
            if (!is_array($witness)) {
                continue;
            }
            $image_url = isset($witness['image_url']) && is_scalar($witness['image_url'])
                ? trim((string) $witness['image_url'])
                : '';
            if ($image_url === '' || !ll_texts_import_is_relative_path($image_url)) {
                continue;
            }

            $asset_path = $payload_dir . DIRECTORY_SEPARATOR . str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $image_url);
            $source_key = $lesson_id !== ''
                ? $lesson_id . '/' . ll_texts_import_normalize_path($image_url)
                : ll_texts_import_normalize_path($image_url);
            $asset = ll_texts_import_asset($asset_path, $post_id, $source_key);
            if (!empty($asset['url'])) {
                $witness['source_asset'] = $image_url;
                $witness['image_url'] = (string) $asset['url'];
                $witness['attachment_id'] = (int) $asset['attachment_id'];
            }
        }
        unset($witness);
    }
    unset($line);

    return $payload;
}

$options = getopt('', [
    'wp-root:',
    'payload:',
    'wordset-slug:',
    'wordset-name::',
    'no-wordset',
    'post-slug::',
    'status::',
]);
if (!is_array($options)) {
    ll_texts_import_fail('Could not parse arguments.');
}

$wp_root = ll_texts_import_option($options, 'wp-root');
$payload_path = ll_texts_import_option($options, 'payload');
$wordset_slug = ll_texts_import_option($options, 'wordset-slug');
$wordset_name = ll_texts_import_option($options, 'wordset-name', 'Zazaki Historical Texts');
$no_wordset = array_key_exists('no-wordset', $options) || $wordset_slug === '';
$post_slug = ll_texts_import_option($options, 'post-slug');
$status = ll_texts_import_option($options, 'status', 'publish');

if ($wp_root === '' || !is_file($wp_root . DIRECTORY_SEPARATOR . 'wp-load.php')) {
    ll_texts_import_fail('Provide --wp-root pointing to a WordPress root.');
}
if ($payload_path === '') {
    ll_texts_import_fail('Provide --payload.');
}
if (!is_file($payload_path)) {
    $payload_path = dirname(__DIR__) . DIRECTORY_SEPARATOR . str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $payload_path);
}
$payload_real_path = realpath($payload_path);
if (!is_string($payload_real_path) || !is_file($payload_real_path)) {
    ll_texts_import_fail('Payload file not found: ' . $payload_path);
}

require_once $wp_root . DIRECTORY_SEPARATOR . 'wp-load.php';

if (!function_exists('ll_tools_interlinear_set_payload')) {
    ll_texts_import_fail('LL Tools is not loaded or does not expose ll_tools_interlinear_set_payload().');
}

$payload_json = file_get_contents($payload_real_path);
$payload = is_string($payload_json) ? json_decode($payload_json, true) : null;
if (!is_array($payload)) {
    ll_texts_import_fail('Payload must be valid JSON object.');
}

$post_slug = $post_slug !== ''
    ? sanitize_title($post_slug)
    : sanitize_title((string) ($payload['lesson_id'] ?? ($payload['title'] ?? 'corpus-text')));
$title = isset($payload['title']) && is_scalar($payload['title']) ? (string) $payload['title'] : $post_slug;
$metadata = isset($payload['metadata']) && is_array($payload['metadata']) ? $payload['metadata'] : [];
$excerpt = '';
foreach (['excerpt', 'summary_text', 'description'] as $excerpt_key) {
    if (isset($metadata[$excerpt_key]) && is_scalar($metadata[$excerpt_key]) && trim((string) $metadata[$excerpt_key]) !== '') {
        $excerpt = trim((string) $metadata[$excerpt_key]);
        break;
    }
    if (isset($payload[$excerpt_key]) && is_scalar($payload[$excerpt_key]) && trim((string) $payload[$excerpt_key]) !== '') {
        $excerpt = trim((string) $payload[$excerpt_key]);
        break;
    }
}
if ($excerpt === '') {
    $excerpt = 'Historical Zazaki text with source witnesses, interlinear analysis, and translations.';
}
$wordset_id = $no_wordset ? 0 : ll_texts_import_ensure_wordset($wordset_slug, $wordset_name);

$post = ll_texts_import_find_post_by_slug($post_slug);
if ($post instanceof WP_Post) {
    $post_id = wp_update_post([
        'ID' => (int) $post->ID,
        'post_title' => $title,
        'post_excerpt' => $excerpt,
        'post_status' => $status,
        'post_type' => 'll_content_lesson',
    ], true);
} else {
    $post_id = wp_insert_post([
        'post_type' => 'll_content_lesson',
        'post_status' => $status,
        'post_title' => $title,
        'post_name' => $post_slug,
        'post_excerpt' => $excerpt,
    ], true);
}
if (is_wp_error($post_id) || (int) $post_id <= 0) {
    $message = is_wp_error($post_id) ? $post_id->get_error_message() : 'unknown error';
    ll_texts_import_fail('Could not create/update content lesson: ' . $message);
}
$post_id = (int) $post_id;

if ($wordset_id > 0) {
    update_post_meta($post_id, LL_TOOLS_CONTENT_LESSON_WORDSET_META, (string) $wordset_id);
} else {
    delete_post_meta($post_id, LL_TOOLS_CONTENT_LESSON_WORDSET_META);
}
if (defined('LL_TOOLS_CONTENT_LESSON_KIND_META')) {
    update_post_meta($post_id, LL_TOOLS_CONTENT_LESSON_KIND_META, 'corpus_text');
}

$collection = isset($metadata['collection']) && is_scalar($metadata['collection']) ? sanitize_title((string) $metadata['collection']) : '';
$collection_label = isset($metadata['collection_label']) && is_scalar($metadata['collection_label']) ? sanitize_text_field((string) $metadata['collection_label']) : '';
$source_author = isset($metadata['source_author']) && is_scalar($metadata['source_author']) ? sanitize_text_field((string) $metadata['source_author']) : '';
$collection_meta = defined('LL_TOOLS_CONTENT_LESSON_CORPUS_COLLECTION_META') ? LL_TOOLS_CONTENT_LESSON_CORPUS_COLLECTION_META : '_ll_tools_corpus_text_collection';
$collection_label_meta = defined('LL_TOOLS_CONTENT_LESSON_CORPUS_COLLECTION_LABEL_META') ? LL_TOOLS_CONTENT_LESSON_CORPUS_COLLECTION_LABEL_META : '_ll_tools_corpus_text_collection_label';
$source_author_meta = defined('LL_TOOLS_CONTENT_LESSON_CORPUS_SOURCE_AUTHOR_META') ? LL_TOOLS_CONTENT_LESSON_CORPUS_SOURCE_AUTHOR_META : '_ll_tools_corpus_text_source_author';
if ($collection !== '') {
    update_post_meta($post_id, $collection_meta, $collection);
} else {
    delete_post_meta($post_id, $collection_meta);
}
if ($collection_label !== '') {
    update_post_meta($post_id, $collection_label_meta, $collection_label);
} else {
    delete_post_meta($post_id, $collection_label_meta);
}
if ($source_author !== '') {
    update_post_meta($post_id, $source_author_meta, $source_author);
} else {
    delete_post_meta($post_id, $source_author_meta);
}

$payload = ll_texts_import_prepare_payload_images($payload, dirname($payload_real_path), $post_id);
$updated = ll_tools_interlinear_set_payload($post_id, $payload, 'zazaki-texts:' . ll_texts_import_normalize_path($payload_real_path));
if (is_wp_error($updated)) {
    ll_texts_import_fail('Could not save LL Tools payload: ' . $updated->get_error_message());
}

$url = get_permalink($post_id);
echo wp_json_encode([
    'post_id' => $post_id,
    'post_slug' => $post_slug,
    'wordset_id' => $wordset_id,
    'url' => is_string($url) ? $url : '',
], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . PHP_EOL;
