"""Use the actual Lerch HTTP handler with an isolated autosave fixture."""

import http.client
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

import serve_lerch_glossary_review as review
from review_security import configure_review_server


class LerchReviewSecurityTests(unittest.TestCase):
    def test_autosave_is_same_origin_and_session_protected(self):
        original = (review.REPO_ROOT, review.AUTOSAVE_PATH)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<head><script>originalUI();</script></head>', encoding="utf-8")
            review.REPO_ROOT = root
            review.AUTOSAVE_PATH = root / "autosave.json"
            saved = '{"rows":{"1":{"text":"şıê","status":"reviewed"}}}\n'
            review.AUTOSAVE_PATH.write_text(saved, encoding="utf-8")
            class Handler(review.ReviewHandler):
                def log_message(self, *args):
                    pass
            server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            configure_review_server(server)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            def request(method, path, headers=None, body=None):
                connection = http.client.HTTPConnection(*server.server_address, timeout=5)
                try:
                    raw = body.encode() if isinstance(body, str) else body
                    fields = {"Host": f"127.0.0.1:{server.server_port}", **(headers or {})}
                    if raw is not None:
                        fields["Content-Length"] = str(len(raw))
                    wire = f"{method} {path} HTTP/1.1\r\n" + "".join(f"{name}: {value}\r\n" for name, value in fields.items()) + "\r\n"
                    connection.connect()
                    connection.sock.sendall(wire.encode() + (raw or b""))
                    response = http.client.HTTPResponse(connection.sock)
                    response.begin()
                    return response.status, dict(response.getheaders()), response.read()
                finally:
                    connection.close()
            try:
                status, headers, page = request("GET", "/")
                self.assertEqual(status, 200)
                self.assertLess(page.index(b"review-security.js"), page.index(b"originalUI()"))
                self.assertNotIn("Access-Control-Allow-Origin", headers)
                self.assertEqual(headers["X-Frame-Options"], "DENY")
                status, headers, body = request("GET", "/api/review-session")
                token = json.loads(body)["token"]
                origin = f"http://127.0.0.1:{server.server_port}"
                valid = {"Origin": origin, "Content-Type": "application/json", "X-Review-Token": token}
                payload = json.dumps({"rows": {"2": {"text": "review fixture"}}})
                before = review.AUTOSAVE_PATH.read_bytes()
                for rejected, expected in [
                    ({"Content-Type": "application/json"}, 403),
                    ({**valid, "Origin": "https://attacker.example"}, 403),
                    ({**valid, "Origin": "null"}, 403),
                    ({**valid, "Host": "attacker.example"}, 403),
                    ({**valid, "X-Review-Token": "wrong"}, 403),
                    ({**valid, "Content-Type": "text/plain"}, 415),
                ]:
                    self.assertEqual(request("POST", review.AUTOSAVE_ROUTE + "?alias=1", rejected, payload)[0], expected)
                    self.assertEqual(review.AUTOSAVE_PATH.read_bytes(), before)
                self.assertEqual(request("GET", "/api/review-session", {"Host": "attacker.example"})[0], 403)
                self.assertEqual(request("OPTIONS", review.AUTOSAVE_ROUTE, {"Origin": "https://attacker.example"})[0], 403)
                self.assertEqual(request("POST", review.AUTOSAVE_ROUTE, valid, "[]")[0], 400)
                self.assertEqual(review.AUTOSAVE_PATH.read_bytes(), before)
                self.assertEqual(request("POST", review.AUTOSAVE_ROUTE, valid, payload)[0], 200)
                self.assertEqual(json.loads(review.AUTOSAVE_PATH.read_bytes()), json.loads(payload))
                status, _, readback = request("GET", review.AUTOSAVE_ROUTE)
                self.assertEqual(status, 200)
                self.assertEqual(json.loads(readback), json.loads(payload))
            finally:
                server.shutdown()
                server.server_close()
                thread.join()
                review.REPO_ROOT, review.AUTOSAVE_PATH = original


if __name__ == "__main__":
    unittest.main()
