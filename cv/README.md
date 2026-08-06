Hiêu Nguyên's LaTeX CV
----------------------

This repository contains an ATS (Applicant Tracking System)-optimized
LaTeX curriculum vitae for **Hiêu Nguyên**, built using a
reproducible Bazel build setup.

---

# Features

- **ATS Optimized**: Built with a single-column layout, standard font
  encodings (`T1`, `utf8`, `lmodern`), and PDF Unicode glyph mapping
  (`\pdfgentounicode=1`) to ensure 100% accurate text extraction by ATS
  parsers.
- **Single Page Design**: Styled to fit cleanly onto a single page while
  maintaining excellent typography and visual hierarchy.
- **Reproducible Build**: Managed with Bazel / Bazelisk using a custom
  Starlark LaTeX compilation rule (`latex.bzl`).

---

# Prerequisites & Installation

To build this CV project, you need **Bazelisk** (or Bazel) and a TeX
distribution with `xelatex` or `pdflatex`.

## macOS

1. **Install Bazelisk**:
   ```bash
   brew install bazelisk
   ```

2. **Install TeX Distribution (MacTeX or BasicTeX)**:
   ```bash
   # Option A: Full TeX Live distribution (Recommended)
   brew install --cask mactex-no-gui

   # Option B: Minimal BasicTeX (Smaller download size)
   brew install --cask basictex
   sudo tlmgr update --self
   sudo tlmgr install titlesec enumitem microtype \
     hyperref xcolor lmodern
   ```

---

## Ubuntu (24.04 / 26.04 LTS)

1. **Install Bazelisk**:
   ```bash
   GH="https://github.com/bazelbuild/bazelisk/releases/latest/download"
   sudo wget -O /usr/local/bin/bazel "$GH/bazelisk-linux-amd64"
   sudo chmod +x /usr/local/bin/bazel
   ```

2. **Install TeX Live & XeLaTeX Packages**:
   ```bash
   sudo apt update
   sudo apt install -y \
     texlive-latex-base \
     texlive-latex-extra \
     texlive-xetex \
     texlive-fonts-recommended \
     texlive-plain-generic
   ```

---

# Building the Project

Run Bazel from the `cv/` directory:

```bash
cd cv
bazel build //:cv
```

## Output Location

After a successful build, the compiled PDF will be located at:
```bash
cv/bazel-bin/cv.pdf
```

---

# Automated Monorepo GitHub Releases

The root GitHub Actions workflow is located at
`.github/workflows/build-cv.yml`:

1. **Strict SemVer Validation**: Automatically verifies that new tag
   versions (`cv-X.Y.Z`) follow Semantic Versioning (`MAJOR.MINOR.PATCH`)
   and are strictly greater than all previous tagged versions.
2. **Monorepo Tag Trigger (`cv-*`)**: Pushing a tag like `cv-1.0.0`
   extracts `1.0.0` and generates `cv-Hieu_Nguyen-1.0.0.pdf`.
3. **Build on Push & PR**: Untagged commits on `main`/`master` build
   `cv-Hieu_Nguyen-0.0.1.pdf` as a workflow artifact.
4. **Publishing a CV Release**:

   ```bash
   git tag cv-1.0.0
   git push origin cv-1.0.0
   ```

---

# Repository Structure

```
<monorepo-root>/
├── .github/
│   └── workflows/
│       └── build-cv.yml # Root GitHub Actions CI/CD workflow
└── cv/
    ├── BUILD.bazel      # Bazel target definitions (//:cv)
    ├── MODULE.bazel     # Bazel module configuration
    ├── latex.bzl        # Custom Starlark rule for LaTeX compilation
    ├── cv.tex           # Main ATS-friendly LaTeX source file
    ├── .gitignore       # Git ignore rules for Bazel & TeX temp files
    └── README.md        # Documentation and build instructions
```
