#!/usr/bin/env python3
"""
Syncs all user stories in stories/*.md to GitHub Projects (Project 2 @zoiest's matalg).
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_NUMBER = 2
PROJECT_OWNER = "zoiest"
PROJECT_ID = "PVT_kwHOC6frCs4Blq9X"
STATUS_FIELD_ID = "PVTSSF_lAHOC6frCs4Blq9XzhkW3K4"
STATUS_READY_ID = "08afe404"
PRIORITY_FIELD_ID = "PVTSSF_lAHOC6frCs4Blq9XzhkW3mo"
PRIORITY_P1_ID = "0a877460"
SIZE_FIELD_ID = "PVTSSF_lAHOC6frCs4Blq9XzhkW3ms"
SIZE_M_ID = "9728cbdc"

def run_cmd(cmd: list[str]) -> str:
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {' '.join(cmd)}\nStderr: {res.stderr}\nStdout: {res.stdout}")
    return res.stdout.strip()

def get_existing_items() -> dict[str, str]:
    """Returns mapping of title -> item_id for existing items in project."""
    raw = run_cmd(["gh", "project", "item-list", str(PROJECT_NUMBER), "--owner", PROJECT_OWNER, "--format", "json"])
    data = json.loads(raw)
    items = {}
    for item in data.get("items", []):
        t = item.get("title", "")
        i_id = item.get("id", "")
        if t and i_id:
            items[t] = i_id
    return items

def sync_story(story_file: Path, existing_items: dict[str, str]):
    text = story_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip()
    body = "\n".join(lines[1:]).strip()

    print(f"Syncing: {title} ...")

    if title in existing_items:
        item_id = existing_items[title]
        print(f"  Item already exists ({item_id}), updating body...")
        # Update body
        run_cmd([
            "gh", "project", "item-edit",
            "--id", item_id,
            "--project-id", PROJECT_ID,
            "--body", body
        ])
    else:
        # Create item
        res_raw = run_cmd([
            "gh", "project", "item-create", str(PROJECT_NUMBER),
            "--owner", PROJECT_OWNER,
            "--title", title,
            "--body", body,
            "--format", "json"
        ])
        item_data = json.loads(res_raw)
        item_id = item_data["id"]
        print(f"  Created item ID: {item_id}")
        existing_items[title] = item_id

    # Set Status to 'Ready'
    try:
        run_cmd([
            "gh", "project", "item-edit",
            "--id", item_id,
            "--project-id", PROJECT_ID,
            "--field-id", STATUS_FIELD_ID,
            "--single-select-option-id", STATUS_READY_ID
        ])
    except Exception as exc:
        print(f"  Warning setting status: {exc}")

    # Set Priority to 'P1'
    try:
        run_cmd([
            "gh", "project", "item-edit",
            "--id", item_id,
            "--project-id", PROJECT_ID,
            "--field-id", PRIORITY_FIELD_ID,
            "--single-select-option-id", PRIORITY_P1_ID
        ])
    except Exception as exc:
        print(f"  Warning setting priority: {exc}")

    # Set Size to 'M'
    try:
        run_cmd([
            "gh", "project", "item-edit",
            "--id", item_id,
            "--project-id", PROJECT_ID,
            "--field-id", SIZE_FIELD_ID,
            "--single-select-option-id", SIZE_M_ID
        ])
    except Exception as exc:
        print(f"  Warning setting size: {exc}")

def main():
    stories_dir = Path("stories")
    story_files = sorted(stories_dir.glob("*.md"))
    if not story_files:
        print("No story files found in stories/!")
        sys.exit(1)

    print(f"Found {len(story_files)} stories in {stories_dir.resolve()}.")
    print(f"Fetching existing items in project {PROJECT_NUMBER} (@{PROJECT_OWNER})...")
    existing = get_existing_items()
    print(f"Found {len(existing)} existing items in project.")

    for f in story_files:
        sync_story(f, existing)

    print(f"\nSuccessfully synced all {len(story_files)} stories to https://github.com/users/{PROJECT_OWNER}/projects/{PROJECT_NUMBER}")

if __name__ == "__main__":
    main()
