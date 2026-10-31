# Helsinki Courses Google Drive Sync

This Bazel module provides synchronized access between local course materials and the shared Google Drive directory.

## Directory Structure

```
Remote (Google Drive)                  Local (mono/helsinki)
helsinki/                              helsinki/
├── financial_economics_1/             ├── financial_economics_1/
│   ├── downloads/                     │   ├── downloads/
│   └── writings/                      │   └── writings/
├── intro_fourier/                     ├── intro_fourier/
│   ├── downloads/                     │   ├── downloads/
│   └── writings/                      │   └── writings/
├── master_thesis/                     ├── master_thesis/
│   ├── downloads/                     │   ├── downloads/
│   └── writings/                      │   └── writings/
├── measure_integral/                  ├── measure_integral/
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

### 1. Google Drive Sync

#### Sync All Sub-Directories
From `helsinki/` directory:
```bash
bazel run :sync
```
Or from the monorepo root:
```bash
bazel run //helsinki:sync
```

#### Sync Individual Courses
From any course directory (or with target path):
```bash
bazel run //helsinki/financial_economics_1:sync
bazel run //helsinki/intro_fourier:sync
bazel run //helsinki/master_thesis:sync
bazel run //helsinki/measure_integral:sync
bazel run //helsinki/measure_probability_analysis:sync
```

#### Dry-Run Mode
Preview changes without modifying local or remote files:
```bash
bazel run //helsinki:sync -- --dry-run
```

---

### 2. Org-mode Document Compilers

#### Compile to HTML (`org2html`)
Incrementally compile `.org` notes to `.html`:
```bash
# All Helsinki courses
bazel run //helsinki:org2html

# Specific course
bazel run //helsinki/measure_probability_analysis:org2html
```

#### Compile to PDF (`org2pdf`)
Incrementally compile `.org` notes to `.pdf` via LaTeX:
```bash
# All Helsinki courses
bazel run //helsinki:org2pdf

# Specific course
bazel run //helsinki/measure_probability_analysis:org2pdf
```
