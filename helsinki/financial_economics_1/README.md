# Financial Economics 1 - Google Drive Sync

This package contains Bazel rules and tools to synchronize files between local directories and a Google Drive folder.

## Features

- **Downloads Sync**: Recursively downloads all files from the remote Google Drive `downloads/` (or `download/`) folder into local `downloads/`.
- **Bin Sync**: Uploads local files from `bin/` (including nested folders) to the remote Google Drive `bin/` folder.
- **Smart Incremental Sync**: Compares MD5 checksums and sizes to skip files that are already up-to-date.
- **Token Flexibility**: Supports plain OAuth2 access tokens (`ya29...`), full OAuth2 credentials JSON (with automatic token refresh), and Google Service Account JSON keys.

---

## Setup & Credentials

Create a `.google_drive_token.json` file in this directory:

### Option 1: Plain Access Token
```text
ya29.a0AfH6...
```

### Option 2: OAuth2 Credentials JSON
```json
{
  "access_token": "ya29.a0AfH6...",
  "refresh_token": "1//0...",
  "client_id": "your-client-id.apps.googleusercontent.com",
  "client_secret": "GOCSPX-...",
  "folder_id": "optional-google-drive-folder-id"
}
```

### Option 3: Service Account Key JSON
```json
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...",
  "client_email": "...@...iam.gserviceaccount.com"
}
```

> **Note**: `.google_drive_token.json` is included in `.gitignore` to prevent committing sensitive keys.

---

## Usage

### Run Sync
```bash
bazel run :sync
```

### Dry Run (Preview changes without downloading or uploading)
```bash
bazel run :sync -- --dry-run
```

### Specify Folder ID or Folder Name explicitly
```bash
# Pass via command line
bazel run :sync -- --folder-id <GOOGLE_DRIVE_FOLDER_ID>
bazel run :sync -- --folder-name "financial_economics_1"

# Or configure folder_id in BUILD.bazel:
# sync(
#     name = "sync",
#     folder_id = "1AbCdEfGhIjKlMnOpQrStUvWxYz",
# )
```

### Verbose Output
```bash
bazel run :sync -- --verbose
```

---

## Running Unit Tests

```bash
bazel test //:sync_unit_test --test_output=all
```
