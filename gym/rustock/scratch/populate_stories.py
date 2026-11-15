#!/usr/bin/env python3
import glob
import json
import os
import re
import subprocess
import sys

PROJECT_NUM = "1"
OWNER = "zoiest"
PROJECT_ID = "PVT_kwHOC6frCs4Blp4k"
STATUS_FIELD_ID = "PVTSSF_lAHOC6frCs4Blp4kzhkV3rE"

STATUS_OPTIONS = {
    "Backlog": "f75ad846",
    "Ready": "08afe404",
    "In progress": "47fc9ee4",
    "In review": "4cc61d42",
    "Done": "98236657",
}

def parse_story(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    title = lines[0].replace("# ", "").strip() if lines else os.path.basename(file_path)

    checks = re.findall(r"- \[([ xX])\]", content)
    dones = sum(1 for c in checks if c in "xX")
    total = len(checks)

    status = "Backlog"
    if total > 0 and dones == total:
        status = "Done"
    elif dones > 0:
        status = "In progress"

    return {
        "title": title,
        "body": content,
        "file": os.path.basename(file_path),
        "status": status,
        "dones": dones,
        "total": total
    }

def main():
    story_files = sorted(glob.glob("stories/*.md"))
    print(f"Found {len(story_files)} story files to populate into Project #{PROJECT_NUM} (owner: {OWNER}).")

    # Fetch existing items to prevent duplicates
    list_cmd = ["gh", "project", "item-list", PROJECT_NUM, "--owner", OWNER, "--format", "json"]
    res = subprocess.run(list_cmd, capture_output=True, text=True)
    existing_titles = set()
    if res.returncode == 0:
        try:
            data = json.loads(res.stdout)
            for item in data.get("items", []):
                title = item.get("title")
                if title:
                    existing_titles.add(title)
        except Exception as e:
            print(f"Warning: could not parse existing items: {e}")

    success_count = 0
    for sf in story_files:
        story = parse_story(sf)
        if story["title"] in existing_titles:
            print(f"⏭️  Skipping existing item: {story['title']}")
            continue

        print(f"➕ Creating item: {story['title']} (Status: {story['status']})...")
        create_cmd = [
            "gh", "project", "item-create", PROJECT_NUM,
            "--owner", OWNER,
            "--title", story["title"],
            "--body", story["body"],
            "--format", "json"
        ]
        res = subprocess.run(create_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  ❌ Error creating item: {res.stderr.strip()}", file=sys.stderr)
            continue

        try:
            created_item = json.loads(res.stdout)
            item_id = created_item.get("id")
            if item_id and story["status"] in STATUS_OPTIONS:
                status_id = STATUS_OPTIONS[story["status"]]
                edit_cmd = [
                    "gh", "project", "item-edit",
                    "--id", item_id,
                    "--project-id", PROJECT_ID,
                    "--field-id", STATUS_FIELD_ID,
                    "--single-select-option-id", status_id
                ]
                edit_res = subprocess.run(edit_cmd, capture_output=True, text=True)
                if edit_res.returncode != 0:
                    print(f"  ⚠️  Created item, but failed to set status: {edit_res.stderr.strip()}")
                else:
                    print(f"  ✅ Created and set status to '{story['status']}'")
            else:
                print(f"  ✅ Created item (id: {item_id})")
            success_count += 1
        except Exception as e:
            print(f"  ⚠️  Created item, but could not parse response JSON: {e}")

    print(f"\n🎉 Done! Successfully added {success_count} stories to Project #{PROJECT_NUM}.")

if __name__ == "__main__":
    main()
