# Helsinki Courses Google Drive Sync

This Bazel module provides synchronized access between local course materials and the shared Google Drive directory.

## Directory Structure

```
Remote (Google Drive)                  Local (mono/helsinki)
helsinki/                              helsinki/
├── financial_economics_1/            ├── financial_economics_1/
│   ├── downloads/                    │   ├── downloads/
│   └── bin/                          │   └── bin/
└── maths_physics_3a/                 └── maths_physics_3a/
    ├── downloads/                        ├── downloads/
    └── bin/                              └── bin/
```

## How It Works

- **`downloads/` sync**: Remote `downloads/` (or `download/`) files are recursively downloaded to local `downloads/`.
- **`bin/` sync**: Local `bin/` files are uploaded to remote `bin/`.
- **Incremental updates**: Existing files are compared using MD5 checksums to prevent redundant transfers.
- **Unified Credentials**: Credentials are automatically loaded from `.google_drive_token.json` in `helsinki/` or course subfolders.

---

## Usage

### 1. Sync Financial Economics 1
From `financial_economics_1/` directory:
```bash
cd financial_economics_1
bazel run :sync
```
Or from `helsinki/` root:
```bash
bazel run //financial_economics_1:sync
```

### 2. Sync Maths Physics 3a
From `maths_physics_3a/` directory:
```bash
cd maths_physics_3a
bazel run :sync
```
Or from `helsinki/` root:
```bash
bazel run //maths_physics_3a:sync
```

### 3. Sync All Courses
From `helsinki/` root:
```bash
bazel run :sync
```

### 4. Dry-Run Mode
Preview changes without modifying local or remote files:
```bash
bazel run :sync -- --dry-run
```
