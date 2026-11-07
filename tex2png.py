#!/usr/bin/env python3
"""
TikZ-to-PNG Compiler with Incremental Build Avoidance.
Compiles standalone TikZ .tex files into high-resolution PNG images.
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

CACHE_FILE_NAME = ".tex2png_cache.json"
IGNORED_DIR_NAMES = {"downloads", "__pycache__", ".git", "ltximg", "bazel-"}
AUX_EXTENSIONS = [".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk", ".synctex.gz"]


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


def is_tikz_figure_file(tex_file: Path) -> bool:
    """Returns True if the .tex file is a standalone TikZ figure."""
    # Files inside a 'figures' directory are assumed to be figures
    if tex_file.parent.name == "figures":
        return True

    # Otherwise inspect content for standalone or tikzpicture
    try:
        content = tex_file.read_text(encoding="utf-8", errors="ignore")
        return "tikzpicture" in content and "\\documentclass" in content
    except Exception:
        return False


def collect_tex_files(target_dir: Path) -> list[Path]:
    """Recursively collects all standalone TikZ .tex files."""
    tex_files = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [
            d for d in dirs
            if not d.startswith((".", "bazel-")) and d not in IGNORED_DIR_NAMES
        ]
        for f in files:
            if f.endswith(".tex") and not f.startswith("."):
                p = Path(root) / f
                if is_tikz_figure_file(p):
                    tex_files.append(p)
    return sorted(tex_files)


def compile_single_tex(tex_file: Path, dpi: int = 250, verbose: bool = False) -> tuple[Path, bool, str]:
    """Compiles a single .tex file to PNG using pdflatex and pdftoppm."""
    pdflatex_bin = shutil.which("pdflatex")
    if not pdflatex_bin:
        return tex_file, False, "pdflatex executable not found in PATH"

    pdftoppm_bin = shutil.which("pdftoppm")
    if not pdftoppm_bin:
        return tex_file, False, "pdftoppm executable not found in PATH"

    fig_dir = tex_file.parent
    base_name = tex_file.stem
    pdf_file = fig_dir / f"{base_name}.pdf"
    png_file = fig_dir / f"{base_name}.png"
    tmp_prefix = f"{base_name}_tmp"

    # Step 1: pdflatex
    cmd_pdf = [pdflatex_bin, "-interaction=nonstopmode", tex_file.name]
    proc_pdf = subprocess.run(cmd_pdf, cwd=str(fig_dir), capture_output=True, text=True)

    if not pdf_file.is_file():
        err_msg = proc_pdf.stderr or proc_pdf.stdout or "pdflatex failed to produce PDF"
        return tex_file, False, err_msg.strip()

    # Step 2: pdftoppm
    cmd_ppm = [pdftoppm_bin, "-png", "-r", str(dpi), pdf_file.name, tmp_prefix]
    proc_ppm = subprocess.run(cmd_ppm, cwd=str(fig_dir), capture_output=True, text=True)

    if proc_ppm.returncode != 0:
        err_msg = proc_ppm.stderr or "pdftoppm failed"
        return tex_file, False, err_msg.strip()

    # Locate tmp-1.png or tmp.png
    tmp_out_1 = fig_dir / f"{tmp_prefix}-1.png"
    tmp_out = fig_dir / f"{tmp_prefix}.png"

    if tmp_out_1.is_file():
        tmp_out_1.replace(png_file)
    elif tmp_out.is_file():
        tmp_out.replace(png_file)
    else:
        return tex_file, False, "pdftoppm did not generate output PNG"

    # Clean up temporary aux, log, tmp files
    for ext in AUX_EXTENSIONS:
        aux = fig_dir / f"{base_name}{ext}"
        if aux.is_file():
            try:
                aux.unlink()
            except OSError:
                pass

    for tmp_file in fig_dir.glob(f"{tmp_prefix}*"):
        try:
            tmp_file.unlink()
        except OSError:
            pass

    return tex_file, True, ""


def process_directory(target_dir: Path, dpi: int = 250, force: bool = False, verbose: bool = False) -> int:
    """Processes all TikZ .tex files in target_dir with incremental build avoidance."""
    target_dir = target_dir.resolve()
    cache_path = target_dir / CACHE_FILE_NAME
    cache = {} if force else load_cache(cache_path)

    tex_files = collect_tex_files(target_dir)

    total = len(tex_files)
    if total == 0:
        if verbose:
            print(f"[tex2png] No TikZ .tex figure files found in: {target_dir}")
        return 0

    to_compile = []
    skipped = []
    active_keys = set()

    for tex_file in tex_files:
        rel_key = str(tex_file.relative_to(target_dir))
        active_keys.add(rel_key)
        png_file = tex_file.with_suffix(".png")
        current_hash = compute_file_sha256(tex_file)
        cached_info = cache.get(rel_key)

        if not force and png_file.is_file() and cached_info:
            cached_hash = cached_info.get("hash")
            cached_png_mtime = cached_info.get("png_mtime", 0)
            current_png_mtime = png_file.stat().st_mtime

            if cached_hash == current_hash and current_png_mtime >= cached_png_mtime:
                skipped.append(tex_file)
                continue

        to_compile.append((tex_file, rel_key, current_hash))

    print(f"{'='*70}")
    print(f"TikZ-to-PNG Compiler (Recursive)")
    print(f"Directory:    {target_dir}")
    print(f"Total Files:  {total}")
    print(f"To Compile:   {len(to_compile)}")
    print(f"Up-to-Date:   {len(skipped)} (build avoided)")
    print(f"{'='*70}")

    if not to_compile:
        # Prune stale keys
        stale_keys = [k for k in cache if k not in active_keys]
        if stale_keys:
            for k in stale_keys:
                del cache[k]
            save_cache(cache_path, cache)

        print(f"All {total} figures are up-to-date. (0 recompiled, {len(skipped)} skipped)")
        return 0

    print(f"\nCompiling {len(to_compile)} figure(s)...")

    t0 = time.time()
    max_workers = min(8, os.cpu_count() or 4)
    has_errors = False

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(compile_single_tex, tex_f, dpi, verbose): (tex_f, rel_k, h)
            for tex_f, rel_k, h in to_compile
        }
        for future in concurrent.futures.as_completed(futures):
            tex_f, rel_k, h = futures[future]
            try:
                _, success, err_msg = future.result()
                png_f = tex_f.with_suffix(".png")
                if success and png_f.is_file():
                    cache[rel_k] = {
                        "hash": h,
                        "tex_mtime": tex_f.stat().st_mtime,
                        "png_mtime": png_f.stat().st_mtime,
                        "png_file": str(png_f.relative_to(target_dir)),
                    }
                    print(f"  ✓ {rel_k} -> {png_f.name}")
                else:
                    print(f"  ✗ {rel_k} failed: {err_msg[:120]}", file=sys.stderr)
                    has_errors = True
            except Exception as exc:
                print(f"  ✗ {rel_k} crashed: {exc}", file=sys.stderr)
                has_errors = True

    elapsed = time.time() - t0

    for k in list(cache.keys()):
        if k not in active_keys:
            del cache[k]

    save_cache(cache_path, cache)

    status_str = f"Completed in {elapsed:.2f}s: {len(to_compile)} compiled, {len(skipped)} skipped."
    if has_errors:
        print(f"\n{status_str} (some errors occurred)", file=sys.stderr)
        return 1

    print(f"\n{status_str}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Compile TikZ TeX files to PNG with recursive build avoidance.")
    parser.add_argument("--target-dir", default="", help="Directory to process (default: current working directory)")
    parser.add_argument("--dpi", type=int, default=250, help="Resolution in DPI for PNG rendering (default: 250)")
    parser.add_argument("--force", "-f", action="store_true", help="Force recompilation of all figures ignoring cache")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.target_dir:
        target_dir = Path(args.target_dir)
    else:
        target_dir = Path.cwd()

    if not target_dir.is_dir():
        print(f"Error: Target directory does not exist: {target_dir}", file=sys.stderr)
        sys.exit(1)

    sys.exit(process_directory(target_dir, dpi=args.dpi, force=args.force, verbose=args.verbose))


if __name__ == "__main__":
    main()
