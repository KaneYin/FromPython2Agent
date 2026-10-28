"""Local web server to visualize LLM log files."""
from __future__ import annotations

import json
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

_HTML_PATH = Path(__file__).parent / "index.html"


class _Handler(BaseHTTPRequestHandler):
    log_dir = "logs"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_html()
        elif parsed.path == "/api/files":
            self._serve_file_list()
        elif parsed.path == "/api/log":
            params = parse_qs(parsed.query)
            name = params.get("file", [""])[0]
            self._serve_log(name)
        else:
            self.send_error(404)

    def _serve_html(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        with open(_HTML_PATH, "rb") as f:
            self.wfile.write(f.read())

    def _serve_file_list(self) -> None:
        p = Path(self.log_dir)
        files = sorted(f.name for f in p.glob("*.jsonl")) if p.exists() else []
        self._json_response(files)

    def _serve_log(self, filename: str) -> None:
        if not filename or ".." in filename or "/" in filename:
            self._json_response([])
            return
        path = Path(self.log_dir) / filename
        if not path.exists():
            self._json_response([])
            return
        entries = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        self._json_response(entries)

    def _json_response(self, data: object) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args) -> None:
        pass  # suppress default logging


def _resolve_log_dir(log_dir: str) -> str:
    """Resolve log_dir relative to project root (where pyproject.toml lives)."""
    p = Path(log_dir)
    if p.is_absolute():
        return str(p)
    # Walk up from this file to find project root
    candidate = Path(__file__).resolve().parent.parent.parent / log_dir
    if candidate.exists():
        return str(candidate)
    # Fallback to cwd
    return str(Path.cwd() / log_dir)


def start(log_dir: str = "logs", port: int = 8765, open_browser: bool = True) -> None:
    resolved = _resolve_log_dir(log_dir)
    _Handler.log_dir = resolved
    server = HTTPServer(("127.0.0.1", port), _Handler)
    url = f"http://127.0.0.1:{port}"
    print(f"Log Viewer running at {url}")
    print(f"Watching directory: {Path(resolved).resolve()}")
    print("Press Ctrl+C to stop")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    import sys
    log_dir = sys.argv[1] if len(sys.argv) > 1 else "logs"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
    start(log_dir=log_dir, port=port)
