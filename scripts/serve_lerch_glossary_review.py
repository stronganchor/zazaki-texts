#!/usr/bin/env python3
"""Serve the Lerch glossary review UI with a small disk autosave API."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from review_security import ReviewSecurityMixin, configure_review_server, review_html


REPO_ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = REPO_ROOT / "reviews" / "lerch-glossary-headword-review"
AUTOSAVE_PATH = REVIEW_DIR / "glossary-review-autosave.json"
AUTOSAVE_ROUTE = "/reviews/lerch-glossary-headword-review/api/autosave"


class ReviewHandler(ReviewSecurityMixin, SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def do_GET(self) -> None:
        # Inject the session helper without rebuilding or altering reviewed text.
        route = self.path.split("?", 1)[0]
        path = Path(self.translate_path(route))
        if path.is_dir():
            path = path / "index.html"
        if path.suffix.lower() == ".html" and path.is_file():
            self._review_reply(200, review_html(path.read_bytes()), "text/html; charset=utf-8")
            return
        if self.path.split("?", 1)[0] == AUTOSAVE_ROUTE:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            if AUTOSAVE_PATH.exists():
                self.wfile.write(AUTOSAVE_PATH.read_bytes())
            else:
                self.wfile.write(b'{"rows":{}}')
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path.split("?", 1)[0] != AUTOSAVE_ROUTE:
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0:
                raise ValueError("Negative body length")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON")
            return

        rows = payload.get("rows") if isinstance(payload, dict) else None
        if not isinstance(rows, dict):
            self.send_error(HTTPStatus.BAD_REQUEST, "Missing rows object")
            return

        AUTOSAVE_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')


def main() -> None:
    host = "127.0.0.1"
    port = 8792
    server = ThreadingHTTPServer((host, port), ReviewHandler)
    configure_review_server(server)
    print(f"Serving Lerch glossary review at http://localhost:{port}/reviews/lerch-glossary-headword-review/index.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
