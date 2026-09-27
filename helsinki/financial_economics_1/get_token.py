#!/usr/bin/env python3
"""
Helper script to generate a Google Drive OAuth2 token for .google_drive_token.
Supports:
1. Interactive OAuth flow using client_id and client_secret
2. Using a downloaded client_secret_xxx.json file
"""

import argparse
import http.server
import json
import socketserver
import sys
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

SCOPES = "https://www.googleapis.com/auth/drive"
REDIRECT_URI = "http://localhost:8085"


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    code = None

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            OAuthCallbackHandler.code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Authentication successful!</h1><p>You can close this tab and return to your terminal.</p>")
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def get_token(client_id: str, client_secret: str, out_file: Path):
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urllib.parse.urlencode({
            "client_id": client_id,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": SCOPES,
            "access_type": "offline",
            "prompt": "consent",
        })
    )

    print("\n1. Opening browser for authorization...")
    print(f"If the browser doesn't open automatically, visit this URL:\n\n{auth_url}\n")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    # Start local server to capture redirect code
    code = None
    try:
        with socketserver.TCPServer(("localhost", 8085), OAuthCallbackHandler) as httpd:
            httpd.timeout = 120
            httpd.handle_request()
            code = OAuthCallbackHandler.code
    except Exception as exc:
        print(f"Local server error ({exc}).")

    if not code:
        code = input("Enter the authorization code from the browser redirect URL: ").strip()

    if not code:
        print("Error: No code provided.", file=sys.stderr)
        sys.exit(1)

    # Exchange authorization code for token
    token_url = "https://oauth2.googleapis.com/token"
    data = urllib.parse.urlencode({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode("utf-8")

    req = urllib.request.Request(token_url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            token_data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(f"Error exchanging code: {exc.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

    token_data["client_id"] = client_id
    token_data["client_secret"] = client_secret

    out_file.write_text(json.dumps(token_data, indent=2), encoding="utf-8")
    print(f"\nSuccess! Credentials saved to: {out_file}")
    print("This token includes a refresh_token, so it will renew automatically.")


def main():
    parser = argparse.ArgumentParser(description="Generate Google Drive token.")
    parser.add_argument("--client-id", help="Google OAuth Client ID")
    parser.add_argument("--client-secret", help="Google OAuth Client Secret")
    parser.add_argument("--credentials-json", help="Path to client_secret_xxx.json")
    parser.add_argument("--out", default=".google_drive_token.json", help="Output token file path")

    args = parser.parse_args()

    client_id = args.client_id
    client_secret = args.client_secret

    if args.credentials_json:
        creds = json.loads(Path(args.credentials_json).read_text(encoding="utf-8"))
        info = creds.get("installed") or creds.get("web") or creds
        client_id = info["client_id"]
        client_secret = info["client_secret"]

    if not client_id or not client_secret:
        print("Please provide client_id and client_secret, or a credentials JSON file.")
        print("You can get these from Google Cloud Console -> APIs & Services -> Credentials.")
        client_id = input("Client ID: ").strip()
        client_secret = input("Client Secret: ").strip()

    get_token(client_id, client_secret, Path(args.out).resolve())


if __name__ == "__main__":
    main()
