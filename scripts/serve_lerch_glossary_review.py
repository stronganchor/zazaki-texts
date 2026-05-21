#!/usr/bin/env python3
"""Serve the Lerch glossary review UI with a small disk autosave API."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = REPO_ROOT / "reviews" / "lerch-glossary-headword-review"
AUTOSAVE_PATH = REVIEW_DIR / "glossary-review-autosave.json"
AUTOSAVE_ROUTE = "/reviews/lerch-glossary-headword-review/api/autosave"


class ReviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self) -> None:
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

        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON")
            return

        rows = payload.get("rows")
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
    print(f"Serving Lerch glossary review at http://localhost:{port}/reviews/lerch-glossary-headword-review/index.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
