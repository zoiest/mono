#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Rendering TikZ figures to 250-DPI PNGs..."
count=0
for tex_file in *.tex; do
    base="${tex_file%.tex}"
    pdflatex -interaction=nonstopmode "$tex_file" > /dev/null 2>&1
    if [ -f "${base}.pdf" ]; then
        pdftoppm -png -r 250 "${base}.pdf" "${base}_tmp"
        if [ -f "${base}_tmp-1.png" ]; then
            mv "${base}_tmp-1.png" "${base}.png"
            count=$((count + 1))
        fi
        rm -f "${base}_tmp"* "${base}.aux" "${base}.log"
    fi
done

echo "Successfully rendered $count figures to PNG."
