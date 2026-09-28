#!/usr/bin/env python3
"""
Google Drive Sync Tool for Bazel rule `sync`.

Synchronizes files between Google Drive and local courses:
Remote structure:
  helsinki/
    financial_economics_1/
      downloads/
      bin/
    maths_physics_3a/
      downloads/
      bin/

Local structure:
  helsinki/
    financial_economics_1/
      downloads/
      bin/
    maths_physics_3a/
      downloads/
      bin/
"""

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB chunks


def format_api_error(err: Exception) -> str:
    """Extracts informative error details from Google Drive API HTTP errors."""
    if isinstance(err, urllib.error.HTTPError):
        try:
            body = err.read().decode("utf-8", errors="replace")
            data = json.loads(body)
            error_info = data.get("error", {})
            msg = error_info.get("message")
            errors = error_info.get("errors", [])
            reason = errors[0].get("reason") if errors else None
            detail = f": {msg}" if msg else ""
            if reason:
                detail += f" [reason: {reason}]"
            return f"HTTP {err.code} {err.reason}{detail}"
        except Exception:
            pass
    return str(err)



class GoogleDriveAuth:
    """Handles authentication and token management for Google Drive API."""

    def __init__(self, token_path: Path):
        self.token_file_path = token_path
        self.access_token = None
        self.refresh_token = None
        self.client_id = None
        self.client_secret = None
        self.token_uri = "https://oauth2.googleapis.com/token"
        self.service_account_info = None
        self.token_data = None
        self.folder_id_from_token = None
        self.folder_name_from_token = None
        self.load_token()

    def load_token(self):
        if not self.token_file_path or not self.token_file_path.is_file():
            print(f"\n{'='*70}", file=sys.stderr)
            print(f"Error: Token file not found: {self.token_file_path}", file=sys.stderr)
            print(f"{'='*70}", file=sys.stderr)
            print(
                "Please create '.google_drive_token.json' in helsinki/ containing your credentials.\n"
                "Supported formats:\n"
                "  1. Google Service Account JSON key: {\"type\": \"service_account\", ...}\n"
                "  2. OAuth2 Credentials JSON: {\"access_token\": \"ya29...\", \"refresh_token\": \"...\", ...}\n"
                "  3. Plain OAuth2 Access Token: ya29.a0AfH6...\n",
                file=sys.stderr,
            )
            sys.exit(1)

        content = self.token_file_path.read_text(encoding="utf-8").strip()
        if not content:
            print(f"Error: Token file {self.token_file_path} is empty.", file=sys.stderr)
            sys.exit(1)

        if content.startswith("{"):
            try:
                data = json.loads(content)
                self.token_data = data
                if data.get("type") == "service_account":
                    self.service_account_info = data
                    self.access_token = self._get_service_account_token()
                elif "installed" in data or "web" in data:
                    print(f"\n{'='*70}", file=sys.stderr)
                    print(f"Error: '{self.token_file_path.name}' contains OAuth client credentials, not an authorized token.", file=sys.stderr)
                    print(f"{'='*70}", file=sys.stderr)
                    print("This file contains application client_id / client_secret from Google Cloud Console.", file=sys.stderr)
                    print("To authorize your account and obtain an active access token, run:\n", file=sys.stderr)
                    print(f"  python3 get_token.py --credentials-json {self.token_file_path.name}\n", file=sys.stderr)
                    print(f"{'='*70}\n", file=sys.stderr)
                    sys.exit(1)
                else:
                    self.access_token = data.get("access_token") or data.get("token")
                    self.refresh_token = data.get("refresh_token")
                    self.client_id = data.get("client_id")
                    self.client_secret = data.get("client_secret")
                    self.token_uri = data.get("token_uri", "https://oauth2.googleapis.com/token")
                    self.folder_id_from_token = data.get("folder_id")
                    self.folder_name_from_token = data.get("folder_name")
                    if not self.access_token and self.refresh_token:
                        self.refresh_access_token()
            except json.JSONDecodeError as exc:
                print(f"Warning: Failed to parse token JSON: {exc}. Treating as raw token.", file=sys.stderr)
                self.access_token = content
        else:
            self.access_token = content

        if not self.access_token:
            print(f"\nError: No valid access token found in {self.token_file_path}.", file=sys.stderr)
            print("Please run 'python3 get_token.py' to generate a valid token.", file=sys.stderr)
            sys.exit(1)


    def _get_service_account_token(self) -> str:
        """Exchanges service account private key for an access token via JWT assertion."""
        try:
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.primitives.serialization import load_pem_private_key
        except ImportError:
            print(
                "Error: 'cryptography' library is required to use service account keys.",
                file=sys.stderr,
            )
            sys.exit(1)

        sa = self.service_account_info
        private_key_pem = sa["private_key"].encode("utf-8")
        private_key = load_pem_private_key(private_key_pem, password=None)

        now = int(time.time())
        header = {"alg": "RS256", "typ": "JWT"}
        claim_set = {
            "iss": sa["client_email"],
            "scope": "https://www.googleapis.com/auth/drive",
            "aud": sa.get("token_uri", "https://oauth2.googleapis.com/token"),
            "exp": now + 3600,
            "iat": now,
        }

        def b64url(data: bytes) -> str:
            return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

        encoded_header = b64url(json.dumps(header).encode("utf-8"))
        encoded_claims = b64url(json.dumps(claim_set).encode("utf-8"))
        signing_input = f"{encoded_header}.{encoded_claims}".encode("ascii")

        signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
        jwt_token = f"{encoded_header}.{encoded_claims}.{b64url(signature)}"

        post_data = urllib.parse.urlencode({
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt_token,
        }).encode("utf-8")

        req = urllib.request.Request(
            sa.get("token_uri", "https://oauth2.googleapis.com/token"),
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            token_res = json.loads(resp.read().decode("utf-8"))
            return token_res["access_token"]

    def refresh_access_token(self) -> bool:
        """Refreshes the OAuth2 access token if credentials are present."""
        if self.service_account_info:
            self.access_token = self._get_service_account_token()
            return True

        if not (self.refresh_token and self.client_id and self.client_secret):
            return False

        post_data = urllib.parse.urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }).encode("utf-8")

        req = urllib.request.Request(
            self.token_uri,
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                new_token = data.get("access_token")
                if new_token:
                    self.access_token = new_token
                    if isinstance(self.token_data, dict):
                        self.token_data["access_token"] = new_token
                        try:
                            self.token_file_path.write_text(
                                json.dumps(self.token_data, indent=2), encoding="utf-8"
                            )
                        except Exception:
                            pass
                    return True
        except Exception as exc:
            print(f"Token refresh failed: {exc}", file=sys.stderr)
        return False


class GoogleDriveClient:
    """Client for Google Drive API v3."""

    DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"
    UPLOAD_API_BASE = "https://www.googleapis.com/upload/drive/v3"

    def __init__(self, auth: GoogleDriveAuth, dry_run: bool = False, verbose: bool = False):
        self.auth = auth
        self.dry_run = dry_run
        self.verbose = verbose

    def _request(
        self,
        url: str,
        method: str = "GET",
        headers: dict = None,
        data: bytes = None,
        retries: int = 1,
    ) -> urllib.request.urlopen:
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Bearer {self.auth.access_token}"

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            return urllib.request.urlopen(req)
        except urllib.error.HTTPError as exc:
            if exc.code == 401 and retries > 0:
                if self.verbose:
                    print("[HTTP 401] Access token expired, attempting refresh...", file=sys.stderr)
                if self.auth.refresh_access_token():
                    return self._request(url, method, headers, data, retries - 1)
            raise

    def get_json(self, url: str) -> dict:
        try:
            with self._request(url, method="GET") as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            err_msg = err.read().decode("utf-8", errors="replace")
            print(f"\nGoogle Drive API Error ({err.code}):", file=sys.stderr)
            try:
                err_json = json.loads(err_msg)
                print(json.dumps(err_json, indent=2), file=sys.stderr)
            except Exception:
                print(err_msg, file=sys.stderr)
            raise

    def list_files(self, query: str, fields: str = "nextPageToken, files(id, name, mimeType, md5Checksum, size, modifiedTime)") -> list:
        files = []
        page_token = None
        while True:
            params = {
                "q": query,
                "fields": fields,
                "pageSize": 1000,
                "supportsAllDrives": "true",
                "includeItemsFromAllDrives": "true",
            }
            if page_token:
                params["pageToken"] = page_token
            url = f"{self.DRIVE_API_BASE}/files?{urllib.parse.urlencode(params)}"
            result = self.get_json(url)
            files.extend(result.get("files", []))
            page_token = result.get("nextPageToken")
            if not page_token:
                break
        return files

    def find_root_folder(self, folder_id: str = None, folder_name: str = "helsinki") -> tuple[str, str]:
        """Finds the root Google Drive folder (e.g. 'helsinki')."""
        if folder_id:
            info = self.get_json(f"{self.DRIVE_API_BASE}/files/{folder_id}?fields=id,name,mimeType,trashed&supportsAllDrives=true")
            if info.get("trashed"):
                raise ValueError(f"Specified folder ID {folder_id} is in trash.")
            return info["id"], info.get("name", folder_id)

        target_name = folder_name or "helsinki"
        query = f"name = '{target_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        folders = self.list_files(query, fields="files(id, name)")

        if len(folders) == 1:
            return folders[0]["id"], folders[0]["name"]
        elif len(folders) > 1:
            # Score folders by whether they have financial_economics_1 or maths_physics_3a inside
            scored = []
            for f in folders:
                children = self.list_files(
                    f"'{f['id']}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
                    fields="files(id, name)",
                )
                child_names = {c["name"] for c in children}
                score = (1 if "financial_economics_1" in child_names else 0) + (1 if "maths_physics_3a" in child_names else 0)
                scored.append((score, f))
            scored.sort(key=lambda x: x[0], reverse=True)
            return scored[0][1]["id"], scored[0][1]["name"]

        # If not found by direct name, check folders shared with me
        shared_folders = self.list_files(
            "sharedWithMe = true and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
            fields="files(id, name)",
        )
        for sf in shared_folders:
            if sf["name"] == target_name:
                return sf["id"], sf["name"]

        if len(shared_folders) == 1:
            return shared_folders[0]["id"], shared_folders[0]["name"]

        raise FileNotFoundError(
            f"Could not find remote Google Drive folder '{target_name}'. "
            "Please ensure the folder is shared with the service account, or specify folder ID via --folder-id <id>."
        )

    def get_child_folder(self, parent_id: str, names: list[str]) -> dict | None:
        """Finds a child folder matching any name in `names`."""
        name_queries = " or ".join([f"name = '{n}'" for n in names])
        query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false and ({name_queries})"
        folders = self.list_files(query, fields="files(id, name)")
        return folders[0] if folders else None

    def create_folder(self, parent_id: str, name: str) -> str:
        """Creates a remote folder and returns its folder ID."""
        if self.dry_run:
            print(f"[DRY-RUN] Would create remote folder: {name} under parent {parent_id}")
            return "dry_run_folder_id"

        url = f"{self.DRIVE_API_BASE}/files?supportsAllDrives=true"
        body = json.dumps({
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }).encode("utf-8")
        with self._request(url, method="POST", headers={"Content-Type": "application/json"}, data=body) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["id"]

    def ensure_remote_path(self, root_id: str, relative_path: str) -> str:
        """Ensures a nested remote folder path exists, creating folders as needed."""
        parts = [p for p in relative_path.strip("/\\").split("/") if p and p != "."]
        curr_id = root_id
        for part in parts:
            child = self.get_child_folder(curr_id, [part])
            if child:
                curr_id = child["id"]
            else:
                curr_id = self.create_folder(curr_id, part)
        return curr_id

    def download_file(self, file_id: str, mime_type: str, dest_path: Path):
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dest = dest_path.with_suffix(dest_path.suffix + ".tmp_download")

        if mime_type.startswith("application/vnd.google-apps."):
            url = f"{self.DRIVE_API_BASE}/files/{file_id}/export?mimeType=application/pdf&supportsAllDrives=true"
        else:
            url = f"{self.DRIVE_API_BASE}/files/{file_id}?alt=media&supportsAllDrives=true"

        with self._request(url, method="GET") as resp, open(temp_dest, "wb") as f_out:
            while True:
                chunk = resp.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_out.write(chunk)

        temp_dest.replace(dest_path)

    def upload_file(self, local_path: Path, parent_id: str, existing_file_id: str = None):
        file_size = local_path.stat().st_size
        filename = local_path.name
        content_type, _ = mimetypes.guess_type(str(local_path))
        if not content_type:
            content_type = "application/octet-stream"

        if existing_file_id:
            init_url = (
                f"{self.UPLOAD_API_BASE}/files/{existing_file_id}"
                f"?uploadType=resumable&supportsAllDrives=true"
            )
            init_method = "PATCH"
            metadata = json.dumps({"name": filename}).encode("utf-8")
        else:
            init_url = (
                f"{self.UPLOAD_API_BASE}/files"
                f"?uploadType=resumable&supportsAllDrives=true"
            )
            init_method = "POST"
            metadata = json.dumps({"name": filename, "parents": [parent_id]}).encode("utf-8")

        init_headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": content_type,
            "X-Upload-Content-Length": str(file_size),
        }

        with self._request(init_url, method=init_method, headers=init_headers, data=metadata) as resp:
            upload_url = resp.headers.get("Location")

        if not upload_url:
            raise RuntimeError("Google Drive did not return Location header for resumable upload.")

        with open(local_path, "rb") as f_in:
            req = urllib.request.Request(
                upload_url,
                data=f_in,
                headers={
                    "Content-Length": str(file_size),
                    "Content-Type": content_type,
                },
                method="PUT",
            )
            with urllib.request.urlopen(req) as resp:
                if resp.status not in (200, 201):
                    raise RuntimeError(f"Upload failed with HTTP status {resp.status}")


def compute_md5(file_path: Path) -> str:
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def sync_single_course(client: GoogleDriveClient, remote_course_id: str, course_name: str, local_course_dir: Path):
    """Syncs downloads and bin for a single course directory."""
    print(f"\n{'='*70}")
    print(f"Course: {course_name}")
    print(f"Local:  {local_course_dir}")
    print(f"{'='*70}")

    local_downloads = local_course_dir / "downloads"
    local_bin = local_course_dir / "bin"

    # 1. Sync remote downloads -> local downloads
    local_downloads.mkdir(parents=True, exist_ok=True)
    remote_dl = client.get_child_folder(remote_course_id, ["downloads", "download"])
    if not remote_dl:
        print(f"Notice: No remote 'downloads' or 'download' folder in {course_name}.")
    else:
        print(f"Found remote downloads folder: '{remote_dl['name']}' (ID: {remote_dl['id']})")
        queue = [(remote_dl["id"], "")]
        dl_count = 0
        dl_skip = 0

        while queue:
            f_id, rel_path = queue.pop(0)
            items = client.list_files(
                f"'{f_id}' in parents and trashed = false",
                fields="files(id, name, mimeType, md5Checksum, size, modifiedTime)",
            )

            for item in items:
                name = item["name"]
                item_rel = os.path.join(rel_path, name)
                is_folder = item.get("mimeType") == "application/vnd.google-apps.folder"

                if is_folder:
                    (local_downloads / item_rel).mkdir(parents=True, exist_ok=True)
                    queue.append((item["id"], item_rel))
                else:
                    target_file = local_downloads / item_rel
                    remote_md5 = item.get("md5Checksum")
                    remote_size = int(item.get("size", 0))

                    if target_file.is_file():
                        if remote_md5 and compute_md5(target_file) == remote_md5:
                            if client.verbose:
                                print(f"  [SKIP] downloads/{item_rel} (MD5 matches)")
                            dl_skip += 1
                            continue
                        elif not remote_md5 and target_file.stat().st_size == remote_size:
                            if client.verbose:
                                print(f"  [SKIP] downloads/{item_rel} (size matches)")
                            dl_skip += 1
                            continue

                    size_str = f" ({remote_size:,} bytes)" if remote_size else ""
                    if client.dry_run:
                        print(f"  [DRY-RUN DOWNLOAD] downloads/{item_rel}{size_str}")
                        dl_count += 1
                    else:
                        print(f"  [DOWNLOADING] downloads/{item_rel}{size_str}...")
                        try:
                            client.download_file(item["id"], item.get("mimeType", ""), target_file)
                            dl_count += 1
                        except Exception as err:
                            print(f"    Error downloading {item_rel}: {format_api_error(err)}", file=sys.stderr)

        print(f"Downloads: {dl_count} downloaded, {dl_skip} up-to-date.")

    # 2. Sync local bin -> remote bin
    local_bin.mkdir(parents=True, exist_ok=True)
    remote_bin = client.get_child_folder(remote_course_id, ["bin"])
    if not remote_bin:
        remote_bin_id = client.create_folder(remote_course_id, "bin")
    else:
        remote_bin_id = remote_bin["id"]

    local_files = []
    for root, _, files in os.walk(local_bin):
        for f in files:
            full_path = Path(root) / f
            rel_path = full_path.relative_to(local_bin)
            local_files.append((full_path, rel_path))

    up_count = 0
    up_skip = 0

    if not local_files:
        print("Bin: local 'bin/' is empty. Nothing to upload.")
    else:
        for full_path, rel_path in local_files:
            parent_rel = str(rel_path.parent) if rel_path.parent != Path(".") else ""
            if parent_rel:
                dest_id = client.ensure_remote_path(remote_bin_id, parent_rel)
            else:
                dest_id = remote_bin_id

            filename = full_path.name
            local_md5 = compute_md5(full_path)
            file_size = full_path.stat().st_size

            existing = client.list_files(
                f"'{dest_id}' in parents and trashed = false and name = '{filename}'",
                fields="files(id, name, md5Checksum, size)",
            )
            existing_file = existing[0] if existing else None

            if existing_file:
                if existing_file.get("md5Checksum") == local_md5:
                    if client.verbose:
                        print(f"  [SKIP] bin/{rel_path} (already up-to-date remotely)")
                    up_skip += 1
                    continue

                if client.dry_run:
                    print(f"  [DRY-RUN UPDATE] bin/{rel_path} ({file_size:,} bytes)")
                    up_count += 1
                else:
                    print(f"  [UPDATING] bin/{rel_path} ({file_size:,} bytes)...")
                    try:
                        client.upload_file(full_path, dest_id, existing_file_id=existing_file["id"])
                        up_count += 1
                    except Exception as err:
                        print(f"    Error updating bin/{rel_path}: {format_api_error(err)}", file=sys.stderr)
            else:
                if client.dry_run:
                    print(f"  [DRY-RUN UPLOAD] bin/{rel_path} ({file_size:,} bytes)")
                    up_count += 1
                else:
                    print(f"  [UPLOADING] bin/{rel_path} ({file_size:,} bytes)...")
                    try:
                        client.upload_file(full_path, dest_id)
                        up_count += 1
                    except Exception as err:
                        print(f"    Error uploading bin/{rel_path}: {format_api_error(err)}", file=sys.stderr)

        print(f"Bin: {up_count} uploaded, {up_skip} up-to-date.")


def find_token_file(candidates: list[Path]) -> Path | None:
    """Searches a list of paths for the .google_drive_token.json or .google_drive_token file."""
    for p in candidates:
        if p and p.is_file():
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Sync Helsinki courses with Google Drive.")
    parser.add_argument("--workspace-dir", default=".", help="Workspace root directory (helsinki)")
    parser.add_argument("--target-dir", default=".", help="Directory where bazel run was invoked")
    parser.add_argument("--course-name", default="", help="Subfolder/course name (e.g. financial_economics_1, maths_physics_3a)")
    parser.add_argument("--root-folder-id", default="", help="Google Drive root folder ID (helsinki)")
    parser.add_argument("--root-folder-name", default="helsinki", help="Google Drive root folder name")
    parser.add_argument("--token-file", default="", help="Path to token file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without modifying files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).resolve()
    target_dir = Path(args.target_dir).resolve()

    # Search candidates for token file (.google_drive_token.json prioritized)
    token_candidates = []
    if args.token_file:
        token_candidates.append(Path(args.token_file).resolve())
    token_candidates.extend([
        target_dir / ".google_drive_token.json",
        target_dir / ".google_drive_token",
        workspace_dir / ".google_drive_token.json",
        workspace_dir / ".google_drive_token",
        target_dir.parent / ".google_drive_token.json",
        target_dir.parent / ".google_drive_token",
    ])
    token_path = find_token_file(token_candidates)
    if not token_path:
        token_path = workspace_dir / ".google_drive_token.json"

    print(f"{'='*70}")
    print(f"Helsinki Google Drive Sync")
    print(f"Workspace Dir:   {workspace_dir}")
    print(f"Target Dir:      {target_dir}")
    print(f"Token File:      {token_path}")
    if args.dry_run:
        print(f"Mode:            DRY RUN")
    print(f"{'='*70}")

    auth = GoogleDriveAuth(token_path)
    client = GoogleDriveClient(auth, dry_run=args.dry_run, verbose=args.verbose)

    # Resolve remote root folder (helsinki)
    root_id = args.root_folder_id or auth.folder_id_from_token or os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    root_name = args.root_folder_name or auth.folder_name_from_token or "helsinki"

    try:
        remote_root_id, remote_root_name = client.find_root_folder(folder_id=root_id, folder_name=root_name)
    except Exception as exc:
        print(f"\nError finding root folder: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Connected to remote Google Drive folder: '{remote_root_name}' (ID: {remote_root_id})")

    # Determine which course(s) to sync
    course_name = args.course_name
    if not course_name:
        # Check if target_dir is a subfolder inside workspace
        try:
            rel = target_dir.relative_to(workspace_dir)
            if str(rel) != ".":
                course_name = str(rel).split("/")[0]
        except ValueError:
            pass

    if course_name:
        courses_to_sync = [course_name]
    else:
        # At root helsinki: find all course folders that have bin or downloads
        courses_to_sync = []
        for child in workspace_dir.iterdir():
            if child.is_dir() and not child.name.startswith((".", "bazel-")):
                if (child / "downloads").exists() or (child / "bin").exists() or (child / "BUILD.bazel").exists():
                    courses_to_sync.append(child.name)
        courses_to_sync.sort()

    print(f"Courses to sync: {', '.join(courses_to_sync)}")

    for cname in courses_to_sync:
        local_c_dir = workspace_dir / cname
        if not local_c_dir.is_dir():
            local_c_dir.mkdir(parents=True, exist_ok=True)

        # Get or create remote course folder under helsinki
        remote_c_folder = client.get_child_folder(remote_root_id, [cname])
        if not remote_c_folder:
            print(f"\nCreating remote course folder '{cname}' in '{remote_root_name}'...")
            remote_c_id = client.create_folder(remote_root_id, cname)
        else:
            remote_c_id = remote_c_folder["id"]

        sync_single_course(client, remote_c_id, cname, local_c_dir)

    print(f"\n{'='*70}")
    print("Sync process completed!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
