#!/usr/bin/env python3
"""Serve the built game on loopback, with fresh assets and the correct WASM MIME."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading
import webbrowser


class PreviewHandler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, ".wasm": "application/wasm"}

    def end_headers(self):
        # Art and scripts are rebuilt in place. Always revalidate browser caches.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Keep the launch terminal useful; show errors, not each asset download.
        if len(args) > 1 and str(args[1]).startswith(("4", "5")):
            super().log_message(fmt, *args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8042)
    parser.add_argument("--no-open", action="store_true", help="Print the URL without opening a browser.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "builds" / "web"
    if not (root / "index.html").is_file():
        parser.error("Web build missing. Run visual-novel/build-web.sh first.")
    if not 1 <= args.port <= 65535:
        parser.error("Port must be between 1 and 65535.")
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(PreviewHandler, directory=str(root)))
    except OSError as exc:
        print(f"Could not start the preview: {exc}. Try --port 8043.", file=sys.stderr)
        return 1
    url = f"http://127.0.0.1:{args.port}/"
    print(f"The Ending We Never Got: {url}\nKeep this terminal open; Ctrl+C stops the preview.", flush=True)
    if not args.no_open:
        # The server must be listening before an eager browser requests the page.
        opener = threading.Timer(0.2, webbrowser.open, args=(url,))
        opener.daemon = True
        opener.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
