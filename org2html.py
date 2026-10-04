#!/usr/bin/env python3
"""
org2html - Incremental Org-to-HTML Compiler for Bazel.

Compiles all .org files in a directory and its subdirectories (e.g. writings/) to .html
using Emacs Org-mode, with SHA-256 content tracking for build avoidance.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

CACHE_FILE_NAME = ".org2html_cache.json"
IGNORED_DIR_NAMES = {"downloads", "__pycache__", ".git"}


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


def collect_org_files(target_dir: Path) -> list[Path]:
    """Recursively collects all .org files, skipping ignored directories."""
    org_files = []
    for root, dirs, files in os.walk(target_dir):
        # Prune hidden directories, bazel symlinks, downloads, etc.
        dirs[:] = [
            d for d in dirs
            if not d.startswith((".", "bazel-")) and d not in IGNORED_DIR_NAMES
        ]
        for f in files:
            if f.endswith(".org") and not f.startswith("."):
                org_files.append(Path(root) / f)
    return sorted(org_files)


def compile_org_files(target_dir: Path, files_to_compile: list[Path], all_org_files: list[Path], verbose: bool = False) -> bool:
    """Compiles a list of .org files to .html using Emacs batch mode in one process."""
    if not files_to_compile:
        return True

    emacs_bin = shutil.which("emacs")
    if not emacs_bin:
        print("Error: 'emacs' executable not found in PATH.", file=sys.stderr)
        return False

    # Relative paths from target_dir
    rel_all_files = [str(f.relative_to(target_dir)) for f in all_org_files]
    rel_compile_files = [str(f.relative_to(target_dir)) for f in files_to_compile]

    all_files_elisp = " ".join([f'"{f}"' for f in rel_all_files])
    compile_files_elisp = " ".join([f'"{f}"' for f in rel_compile_files])

    elisp_code = f"""
(progn
  (require 'org)
  (require 'org-id)
  (require 'ox-html)
  (setq org-export-with-broken-links t)
  (setq org-html-validation-link nil)
  (setq org-id-extra-files (list {all_files_elisp}))
  (org-id-update-id-locations org-id-extra-files)
  (dolist (f '({compile_files_elisp}))
    (message "Compiling %s -> %s..." f (concat (file-name-sans-extension f) ".html"))
    (with-current-buffer (find-file-noselect f)
      (org-html-export-to-html))))
"""

    cmd = [emacs_bin, "-Q", "--batch", "--eval", elisp_code]

    if verbose:
        print(f"[org2html] Running Emacs in: {target_dir}")

    proc = subprocess.run(cmd, cwd=str(target_dir), capture_output=True, text=True)

    if proc.returncode != 0:
        print(f"Error during Org-to-HTML export (exit code {proc.returncode}):", file=sys.stderr)
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return False

    if verbose and proc.stdout:
        for line in proc.stdout.splitlines():
            if "Compiling" in line:
                print(f"  {line}")

    return True


def process_directory(target_dir: Path, force: bool = False, verbose: bool = False) -> int:
    """Processes all .org files in target_dir and subdirectories with build avoidance."""
    target_dir = target_dir.resolve()
    cache_path = target_dir / CACHE_FILE_NAME
    cache = {} if force else load_cache(cache_path)

    org_files = collect_org_files(target_dir)

    if not org_files:
        print(f"[org2html] No .org files found in: {target_dir}")
        return 0

    to_compile = []
    skipped = []
    active_keys = set()

    for org_file in org_files:
        rel_key = str(org_file.relative_to(target_dir))
        active_keys.add(rel_key)
        html_file = org_file.with_suffix(".html")
        current_hash = compute_file_sha256(org_file)
        cached_info = cache.get(rel_key)

        if not force and html_file.is_file() and cached_info:
            cached_hash = cached_info.get("hash")
            cached_html_mtime = cached_info.get("html_mtime", 0)
            current_html_mtime = html_file.stat().st_mtime

            if cached_hash == current_hash and current_html_mtime >= cached_html_mtime:
                skipped.append(org_file)
                continue

        to_compile.append((org_file, rel_key, current_hash))

    total = len(org_files)
    print(f"{'='*70}")
    print(f"Org-to-HTML Compiler (Recursive)")
    print(f"Directory:    {target_dir}")
    print(f"Total Files:  {total}")
    print(f"To Compile:   {len(to_compile)}")
    print(f"Up-to-Date:   {len(skipped)} (build avoided)")
    print(f"{'='*70}")

    if not to_compile:
        # Prune dead keys from cache
        stale_keys = [k for k in cache if k not in active_keys]
        if stale_keys:
            for k in stale_keys:
                del cache[k]
            save_cache(cache_path, cache)

        print(f"All {total} files are up-to-date. (0 recompiled, {len(skipped)} skipped)")
        return 0

    print(f"\nCompiling {len(to_compile)} file(s)...")
    compile_list = [f for f, _, _ in to_compile]

    t0 = time.time()
    success = compile_org_files(target_dir, compile_list, org_files, verbose=verbose)
    elapsed = time.time() - t0

    if not success:
        return 1

    # Update cache for successfully compiled files
    for org_file, rel_key, file_hash in to_compile:
        html_file = org_file.with_suffix(".html")
        if html_file.is_file():
            cache[rel_key] = {
                "hash": file_hash,
                "org_mtime": org_file.stat().st_mtime,
                "html_mtime": html_file.stat().st_mtime,
                "html_file": str(html_file.relative_to(target_dir)),
            }
            print(f"  ✓ {rel_key} -> {html_file.relative_to(target_dir)}")

    # Prune dead keys
    for k in list(cache.keys()):
        if k not in active_keys:
            del cache[k]

    save_cache(cache_path, cache)

    print(f"\nCompleted in {elapsed:.2f}s: {len(to_compile)} compiled, {len(skipped)} skipped.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Compile Org files to HTML with recursive build avoidance.")
    parser.add_argument("--target-dir", default="", help="Directory to process (default: current working directory)")
    parser.add_argument("--force", "-f", action="store_true", help="Force recompilation of all files ignoring cache")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.target_dir:
        target_dir = Path(args.target_dir)
    elif "BUILD_WORKING_DIRECTORY" in os.environ:
        target_dir = Path(os.environ["BUILD_WORKING_DIRECTORY"])
    elif "BUILD_WORKSPACE_DIRECTORY" in os.environ:
        target_dir = Path(os.environ["BUILD_WORKSPACE_DIRECTORY"])
    else:
        target_dir = Path.cwd()

    ret = process_directory(target_dir, force=args.force, verbose=args.verbose)
    sys.exit(ret)


if __name__ == "__main__":
    main()
