#!/usr/bin/env python3
"""
md2pdf - Incremental Markdown-to-PDF Compiler for Bazel.

Compiles all .md files in a directory and its subdirectories to .pdf using
pandoc, with SHA-256 content tracking for incremental build avoidance.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

CACHE_FILE_NAME = ".md2pdf_cache.json"
COMPILER_VERSION = "3"
MAX_CODE_LINE_LEN = 86
IGNORED_DIR_NAMES = {
    "downloads",
    "__pycache__",
    ".git",
    "ltximg",
    "target",
    "node_modules",
}

TEX_ENGINES = {"xelatex", "lualatex", "pdflatex"}
PREFERRED_ENGINES = ["weasyprint", "pdflatex", "xelatex", "lualatex", "wkhtmltopdf"]

TEX_CHAR_REPLACEMENTS = {
    "✅": "[Done]",
    "⏳": "[Todo]",
    "📖": "[Book]",
    "🎯": "[Goals]",
    "🛠️": "[Guide]",
    "🛠": "[Guide]",
    "📚": "[Refs]",
    "🚀": "[Start]",
    "📁": "[Layout]",
    "🗺️": "[Roadmap]",
    "🗺": "[Roadmap]",
    "📊": "[Status]",
    "⚠️": "[Warning]",
    "⚠": "[Warning]",
    "❌": "[Error]",
    "⏭️": "[Skip]",
    "⏭": "[Skip]",
    "➕": "[Add]",
    "🎉": "[Complete]",
    "✓": "[x]",
    "✔": "[x]",
    "✗": "[ ]",
    "✘": "[ ]",
    "—": "--",
    "–": "-",
    "…": "...",
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    "•": "*",
    "·": "*",
    "×": "x",
    "÷": "/",
    "→": "->",
    "←": "<-",
    "↔": "<->",
    "⇒": "=>",
    "⇐": "<=",
    "⇔": "<=>",
    "≥": ">=",
    "≤": "<=",
    "≠": "!=",
    "≈": "~=",
    "├": "|",
    "└": "`",
    "┌": "+",
    "┐": "+",
    "┘": "+",
    "┬": "+",
    "┴": "+",
    "┼": "+",
    "│": "|",
    "─": "-",
    "═": "=",
    "║": "|",
    "©": "(c)",
    "®": "(R)",
    "™": "(TM)",
    "\u00a0": " ",
}


def compute_file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def load_cache(cache_path: Path) -> dict:
    if cache_path.is_file():
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache_path: Path, data: dict):
    try:
        cache_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as exc:
        print(f"Warning: Failed to save cache: {exc}", file=sys.stderr)


def has_newer_linked_images(md_file: Path, target_mtime: float) -> bool:
    """Checks if any linked image file has an mtime newer than target_mtime."""
    try:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        img_refs = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", content)
        for ref in img_refs:
            if ref.startswith(("http://", "https://", "data:")):
                continue
            ref_path = (md_file.parent / ref).resolve()
            if ref_path.is_file() and ref_path.stat().st_mtime > target_mtime:
                return True
    except Exception:
        pass
    return False


def collect_md_files(target_dir: Path) -> list[Path]:
    """Recursively collects all .md files, skipping ignored directories."""
    md_files = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith((".", "bazel-")) and d not in IGNORED_DIR_NAMES
        ]
        for f in files:
            if f.endswith(".md") and not f.startswith("."):
                md_files.append(Path(root) / f)
    return sorted(md_files)


def resolve_pdf_engine(requested: str) -> str | None:
    if requested != "auto":
        return shutil.which(requested) and requested or None
    for candidate in PREFERRED_ENGINES:
        if shutil.which(candidate):
            return candidate
    return None


def has_tex_package(pkg_file: str) -> bool:
    """Checks whether a LaTeX package file (e.g. fvextra.sty) is installed."""
    kpsewhich = shutil.which("kpsewhich")
    if not kpsewhich:
        return False
    proc = subprocess.run([kpsewhich, pkg_file], capture_output=True, text=True)
    return proc.returncode == 0 and bool(proc.stdout.strip())


def sanitize_for_tex(content: str, engine: str) -> str:
    """Normalizes emojis, box-drawing, and non-TeX symbols for LaTeX engines."""
    for src, replacement in TEX_CHAR_REPLACEMENTS.items():
        content = content.replace(src, replacement)
    max_codepoint = 0xFF if engine == "pdflatex" else 0xFFFF
    return "".join(
        ch
        for ch in content
        if ch not in ("\ufe0e", "\ufe0f", "\u200d") and ord(ch) <= max_codepoint
    )


def _is_pipe_separator(line: str) -> list[tuple[str, str]] | None:
    stripped = line.strip()
    if "|" not in stripped or "-" not in stripped:
        return None
    inner = stripped.strip("|")
    cells = [c.strip() for c in inner.split("|")]
    if len(cells) < 2:
        return None
    alignments = []
    for cell in cells:
        if not re.fullmatch(r":?-{1,}:?", cell):
            return None
        left = ":" if cell.startswith(":") else ""
        right = ":" if cell.endswith(":") else ""
        alignments.append((left, right))
    return alignments


def _split_pipe_cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [c.strip() for c in stripped.split("|")]


def _visible_cell_len(cell: str) -> int:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)
    text = text.replace("`", "").replace("**", "").replace("*", "")
    return len(text.strip())


def normalize_markdown_tables(content: str) -> str:
    """Expands GFM pipe-table separator dashes proportionally so pandoc wraps columns."""
    lines = content.splitlines()
    out: list[str] = []
    in_fence = False
    fence_char = ""
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
            elif marker[0] == fence_char:
                in_fence = False
                fence_char = ""
            out.append(line)
            i += 1
            continue

        if (
            not in_fence
            and i + 1 < len(lines)
            and "|" in line
        ):
            alignments = _is_pipe_separator(lines[i + 1])
            if alignments is not None:
                num_cols = len(alignments)
                header_cells = _split_pipe_cells(line)
                table_rows = [header_cells]
                j = i + 2
                while j < len(lines) and "|" in lines[j] and lines[j].strip():
                    table_rows.append(_split_pipe_cells(lines[j]))
                    j += 1

                weights = []
                for col in range(num_cols):
                    max_len = 4
                    for row in table_rows:
                        if col < len(row):
                            max_len = max(max_len, _visible_cell_len(row[col]))
                    weights.append(min(max_len, 48))

                total_weight = sum(weights) or num_cols
                target_total_dashes = 100
                sep_cells = []
                for col, (left, right) in enumerate(alignments):
                    dashes = max(3, round(target_total_dashes * weights[col] / total_weight))
                    sep_cells.append(f"{left}{'-' * dashes}{right}")

                out.append(line)
                out.append("| " + " | ".join(sep_cells) + " |")
                out.extend(lines[i + 2 : j])
                i = j
                continue

        out.append(line)
        i += 1

    return "\n".join(out) + ("\n" if content.endswith("\n") else "")


def wrap_long_code_lines(content: str, wrap_tagged: bool, max_len: int = MAX_CODE_LINE_LEN) -> str:
    """Soft-wraps overflowing lines inside fenced code blocks."""
    lines = content.splitlines()
    out: list[str] = []
    in_fence = False
    fence_char = ""
    fence_tagged = False

    for line in lines:
        stripped = line.lstrip()
        fence_match = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)
        if fence_match:
            marker, info = fence_match.group(1), fence_match.group(2).strip()
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_tagged = bool(info)
            elif marker[0] == fence_char and not info:
                in_fence = False
                fence_char = ""
                fence_tagged = False
            out.append(line)
            continue

        if in_fence and len(line) > max_len and (wrap_tagged or not fence_tagged):
            indent_len = len(line) - len(line.lstrip(" "))
            indent = line[:indent_len]
            wrapped = textwrap.wrap(
                line,
                width=max_len,
                subsequent_indent=indent + "  ",
                break_long_words=True,
                break_on_hyphens=False,
                drop_whitespace=False,
                replace_whitespace=False,
            )
            out.extend(wrapped if wrapped else [line])
        else:
            out.append(line)

    return "\n".join(out) + ("\n" if content.endswith("\n") else "")


def build_tex_header(has_fvextra: bool) -> str:
    highlighting_setup = (
        r"\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines=true,breakanywhere=true,fontsize=\footnotesize,commandchars=\\\{\}}"
        if has_fvextra
        else r"\DefineVerbatimEnvironment{Highlighting}{Verbatim}{fontsize=\footnotesize,commandchars=\\\{\}}"
    )
    fvextra_pkg = r"\usepackage{fvextra}" if has_fvextra else ""
    template = r"""
\IfFileExists{xurl.sty}{\usepackage{xurl}}{}
__FVEXTRA_PKG__
\setlength{\emergencystretch}{3em}
\sloppy
\providecommand{\texorpdfstring}[2]{#1}
\makeatletter
\DeclareRobustCommand{\_}{\texorpdfstring{\ifmmode\mbox{\textunderscore}\else\textunderscore\hspace{0pt}\fi}{\textunderscore}}
\@ifundefined{longtable}{}{
  \let\orig@longtable\longtable
  \let\endorig@longtable\endlongtable
  \renewenvironment{longtable}{\footnotesize\setlength{\tabcolsep}{4pt}\orig@longtable}{\endorig@longtable}
}
\@ifundefined{Highlighting}{}{
  __HIGHLIGHTING__
}
\makeatother
""".lstrip()
    return (
        template.replace("__FVEXTRA_PKG__", fvextra_pkg)
        .replace("__HIGHLIGHTING__", highlighting_setup)
    )


def compile_md_file(
    md_file: Path,
    pdf_file: Path,
    pandoc_bin: str,
    engine: str,
    has_fvextra: bool = False,
    header_path: Path | None = None,
    verbose: bool = False,
) -> bool:
    content = md_file.read_text(encoding="utf-8")
    if engine in TEX_ENGINES:
        content = sanitize_for_tex(content, engine)
        content = normalize_markdown_tables(content)
        content = wrap_long_code_lines(content, wrap_tagged=not has_fvextra)

    cmd = [
        pandoc_bin,
        "-f",
        "gfm",
        "--columns=60",
        "--pdf-engine",
        engine,
        "--resource-path",
        ".",
        "-o",
        str(pdf_file),
    ]
    if engine in TEX_ENGINES:
        cmd.extend(
            [
                "-V",
                "geometry:margin=0.65in",
                "-V",
                "colorlinks=true",
                "-V",
                "linkcolor=blue",
                "-V",
                "urlcolor=blue",
            ]
        )
        if header_path is not None:
            cmd.extend(["-H", str(header_path)])

    if verbose:
        print(f"[md2pdf] Running: {' '.join(cmd)} (cwd={md_file.parent})")

    proc = subprocess.run(
        cmd,
        cwd=str(md_file.parent),
        input=content,
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        print(
            f"Error compiling {md_file.name} (exit code {proc.returncode}):",
            file=sys.stderr,
        )
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return False

    return True


def process_directory(
    target_dir: Path,
    force: bool = False,
    verbose: bool = False,
    pdf_engine: str = "auto",
) -> int:
    """Processes all .md files in target_dir and subdirectories with build avoidance."""
    target_dir = target_dir.resolve()
    cache_path = target_dir / CACHE_FILE_NAME
    cache = {} if force else load_cache(cache_path)

    md_files = collect_md_files(target_dir)

    if not md_files:
        print(f"[md2pdf] No .md files found in: {target_dir}")
        return 0

    to_compile = []
    skipped = []
    active_keys = set()

    for md_file in md_files:
        rel_key = str(md_file.relative_to(target_dir))
        active_keys.add(rel_key)
        pdf_file = md_file.with_suffix(".pdf")
        current_hash = compute_file_sha256(md_file)
        cached_info = cache.get(rel_key)

        if not force and pdf_file.is_file() and cached_info:
            cached_hash = cached_info.get("hash")
            cached_ver = cached_info.get("compiler_version")
            cached_pdf_mtime = cached_info.get("pdf_mtime", 0)
            current_pdf_mtime = pdf_file.stat().st_mtime

            if (
                cached_ver == COMPILER_VERSION
                and cached_hash == current_hash
                and current_pdf_mtime >= cached_pdf_mtime
            ):
                if not has_newer_linked_images(md_file, current_pdf_mtime):
                    skipped.append(md_file)
                    continue

        to_compile.append((md_file, rel_key, current_hash))

    total = len(md_files)
    print("=" * 70)
    print("Markdown-to-PDF Compiler (Recursive)")
    print(f"Directory:    {target_dir}")
    print(f"Total Files:  {total}")
    print(f"To Compile:   {len(to_compile)}")
    print(f"Up-to-Date:   {len(skipped)} (build avoided)")
    print("=" * 70)

    if not to_compile:
        stale_keys = [k for k in cache if k not in active_keys]
        if stale_keys:
            for k in stale_keys:
                del cache[k]
            save_cache(cache_path, cache)

        print(f"All {total} files are up-to-date. (0 recompiled, {len(skipped)} skipped)")
        return 0

    pandoc_bin = shutil.which("pandoc")
    if not pandoc_bin:
        print("Error: 'pandoc' executable not found in PATH.", file=sys.stderr)
        return 1

    engine = resolve_pdf_engine(pdf_engine)
    if not engine:
        print(
            f"Error: No supported PDF engine found (requested: {pdf_engine}; "
            f"tried: {', '.join(PREFERRED_ENGINES)}).",
            file=sys.stderr,
        )
        return 1

    print(f"\nCompiling {len(to_compile)} file(s) using pandoc ({engine})...")

    t0 = time.time()
    has_errors = False
    compiled_count = 0
    has_fvextra = engine in TEX_ENGINES and has_tex_package("fvextra.sty")
    header_file: tempfile.NamedTemporaryFile | None = None
    header_path: Path | None = None
    if engine in TEX_ENGINES:
        header_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", encoding="utf-8", delete=False
        )
        header_file.write(build_tex_header(has_fvextra))
        header_file.close()
        header_path = Path(header_file.name)

    try:
        for md_file, rel_key, file_hash in to_compile:
            pdf_file = md_file.with_suffix(".pdf")
            ok = compile_md_file(
                md_file,
                pdf_file,
                pandoc_bin,
                engine,
                has_fvextra=has_fvextra,
                header_path=header_path,
                verbose=verbose,
            )
            if ok and pdf_file.is_file():
                cache[rel_key] = {
                    "compiler_version": COMPILER_VERSION,
                    "hash": file_hash,
                    "md_mtime": md_file.stat().st_mtime,
                    "pdf_mtime": pdf_file.stat().st_mtime,
                    "pdf_file": str(pdf_file.relative_to(target_dir)),
                    "engine": engine,
                }
                compiled_count += 1
                print(f"  ✓ {rel_key} -> {pdf_file.relative_to(target_dir)}")
            else:
                print(
                    f"  ✗ {rel_key} -> failed to produce {pdf_file.relative_to(target_dir)}",
                    file=sys.stderr,
                )
                has_errors = True
    finally:
        if header_path is not None and header_path.exists():
            try:
                header_path.unlink()
            except OSError:
                pass

    elapsed = time.time() - t0

    for k in list(cache.keys()):
        if k not in active_keys:
            del cache[k]

    save_cache(cache_path, cache)

    status_str = (
        f"Completed in {elapsed:.2f}s: "
        f"{compiled_count} compiled, {len(skipped)} skipped."
    )
    if has_errors:
        print(f"\n{status_str} (some errors occurred)", file=sys.stderr)
        return 1

    print(f"\n{status_str}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Compile Markdown files to PDF with recursive build avoidance."
    )
    parser.add_argument(
        "--target-dir",
        default="",
        help="Directory to process (default: current working directory)",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force recompilation of all files ignoring cache",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--pdf-engine",
        default="auto",
        help="Pandoc PDF engine to use (default: auto)",
    )

    args = parser.parse_args()

    if args.target_dir:
        target_dir = Path(args.target_dir)
    elif "BUILD_WORKING_DIRECTORY" in os.environ:
        target_dir = Path(os.environ["BUILD_WORKING_DIRECTORY"])
    elif "BUILD_WORKSPACE_DIRECTORY" in os.environ:
        target_dir = Path(os.environ["BUILD_WORKSPACE_DIRECTORY"])
    else:
        target_dir = Path.cwd()

    ret = process_directory(
        target_dir,
        force=args.force,
        verbose=args.verbose,
        pdf_engine=args.pdf_engine,
    )
    sys.exit(ret)


if __name__ == "__main__":
    main()
