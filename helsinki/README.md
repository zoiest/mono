# Helsinki Courses Google Drive Sync

This Bazel module provides synchronized access between local course materials and the shared Google Drive directory.

## Directory Structure

```
Remote (Google Drive)                  Local (mono/helsinki)
helsinki/                              helsinki/
├── 8.01/                              ├── 8.01/
│   ├── downloads/                     │   ├── downloads/
│   └── writings/                      │   └── writings/
├── financial_economics_1/             ├── financial_economics_1/
│   ├── downloads/                     │   ├── downloads/
│   └── writings/                      │   └── writings/
├── maths_physics_3a/                  ├── maths_physics_3a/
│   ├── downloads/                     │   ├── downloads/
│   └── writings/                      │   └── writings/
├── measure_integral/                  ├── measure_integral/
│   ├── downloads/                     │   ├── downloads/
│   └── writings/                      │   └── writings/
├── intro_fourier/                     ├── intro_fourier/
│   ├── downloads/                     │   ├── downloads/
│   └── writings/                      │   └── writings/
└── measure_probability_analysis/      └── measure_probability_analysis/
    ├── downloads/                         ├── downloads/
    └── writings/                          └── writings/
```

## How It Works

- **`downloads/` sync**: Remote `downloads/` (or `download/`) files are recursively downloaded to local `downloads/`.
- **`writings/` sync**: Local `writings/` files are uploaded to remote `writings/`.
- **Incremental updates**: Existing files are compared using MD5 checksums to prevent redundant transfers.
- **Unified Credentials**: Credentials are automatically loaded from `.google_drive_token.json` in `helsinki/` or course subfolders.

---

## Usage

### 1. Sync All Sub-Directories
From `helsinki/` directory:
```bash
bazel run :sync
```
Or from the monorepo root:
```bash
bazel run //helsinki:sync
```

### 2. Sync Individual Courses
From any course directory (or with target path):
```bash
bazel run //helsinki/financial_economics_1:sync
bazel run //helsinki/maths_physics_3a:sync
bazel run //helsinki/measure_integral:sync
bazel run //helsinki/intro_fourier:sync
bazel run //helsinki/measure_probability_analysis:sync
bazel run //helsinki/8.01:sync
```

### 3. Dry-Run Mode
Preview changes without modifying local or remote files:
```bash
bazel run //helsinki:sync -- --dry-run
```
