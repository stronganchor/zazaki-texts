<?php
/**
 * Import a repository text-document payload into an LL Tools content lesson.
 *
 * Usage:
 * php scripts/import_lltools_corpus_text.php \
 *   --wp-root="/path/to/wordpress" \
 *   --payload="texts/lerch/kauge-nyerib-u-sivani/text-document.json" \
 *   --wordset-slug="zazaki-historical-texts" \
 *   --wordset-name="Zazaki Historical Texts" \
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

function ll_texts_import_asset(string $asset_path, int $post_id): array {
    $real_path = realpath($asset_path);
    if (!is_string($real_path) || $real_path === '' || !is_file($real_path)) {
        return ['attachment_id' => 0, 'url' => ''];
    }

    $source_key = ll_texts_import_normalize_path($real_path);
    $existing_id = ll_texts_import_find_attachment_by_source($source_key);
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
            $asset = ll_texts_import_asset($asset_path, $post_id);
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
    'post-slug::',
    'status::',
]);
if (!is_array($options)) {
    ll_texts_import_fail('Could not parse arguments.');
}

$wp_root = ll_texts_import_option($options, 'wp-root');
$payload_path = ll_texts_import_option($options, 'payload');
$wordset_slug = ll_texts_import_option($options, 'wordset-slug', 'zazaki-historical-texts');
$wordset_name = ll_texts_import_option($options, 'wordset-name', 'Zazaki Historical Texts');
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
$wordset_id = ll_texts_import_ensure_wordset($wordset_slug, $wordset_name);

$post = ll_texts_import_find_post_by_slug($post_slug);
if ($post instanceof WP_Post) {
    $post_id = wp_update_post([
        'ID' => (int) $post->ID,
        'post_title' => $title,
        'post_status' => $status,
        'post_type' => 'll_content_lesson',
    ], true);
} else {
    $post_id = wp_insert_post([
        'post_type' => 'll_content_lesson',
        'post_status' => $status,
        'post_title' => $title,
        'post_name' => $post_slug,
        'post_excerpt' => 'Historical Zazaki text with source witnesses, interlinear analysis, and translations.',
    ], true);
}
if (is_wp_error($post_id) || (int) $post_id <= 0) {
    $message = is_wp_error($post_id) ? $post_id->get_error_message() : 'unknown error';
    ll_texts_import_fail('Could not create/update content lesson: ' . $message);
}
$post_id = (int) $post_id;

update_post_meta($post_id, LL_TOOLS_CONTENT_LESSON_WORDSET_META, (string) $wordset_id);
if (defined('LL_TOOLS_CONTENT_LESSON_KIND_META')) {
    update_post_meta($post_id, LL_TOOLS_CONTENT_LESSON_KIND_META, 'corpus_text');
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
