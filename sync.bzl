"""Bazel rule for syncing workspace courses and projects with Google Drive."""

def _sync_impl(ctx):
    runner = ctx.actions.declare_file(ctx.label.name + ".sh")
    py_tool = ctx.file._sync_tool

    # Resolve remote path (e.g. 'helsinki/financial_economics_1', 'gostock')
    remote_path = ctx.attr.remote_path
    if not remote_path:
        if ctx.attr.root_folder_name and ctx.attr.course_name:
            remote_path = ctx.attr.root_folder_name + "/" + ctx.attr.course_name
        elif ctx.attr.root_folder_name:
            remote_path = ctx.attr.root_folder_name
        elif ctx.label.package:
            remote_path = ctx.label.package
        else:
            remote_path = "helsinki"

    course_name = ctx.attr.course_name
    root_folder_name = ctx.attr.root_folder_name

    script_content = """#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="${{BUILD_WORKSPACE_DIRECTORY:-$(pwd)}}"
TARGET_DIR="${{BUILD_WORKING_DIRECTORY:-$(pwd)}}"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "Error: Python 3 is required." >&2
    exit 1
fi

SCRIPT_PATH=""
if [ -f "{tool_short_path}" ]; then
    SCRIPT_PATH="{tool_short_path}"
elif [ -f "${{BASH_SOURCE[0]}}.runfiles/_main/{tool_short_path}" ]; then
    SCRIPT_PATH="${{BASH_SOURCE[0]}}.runfiles/_main/{tool_short_path}"
elif [ -f "${{BASH_SOURCE[0]}}.runfiles/{workspace_name}/{tool_short_path}" ]; then
    SCRIPT_PATH="${{BASH_SOURCE[0]}}.runfiles/{workspace_name}/{tool_short_path}"
elif [ -n "${{RUNFILES_DIR:-}}" ] && [ -f "${{RUNFILES_DIR}}/_main/{tool_short_path}" ]; then
    SCRIPT_PATH="${{RUNFILES_DIR}}/_main/{tool_short_path}"
elif [ -n "${{RUNFILES_DIR:-}}" ] && [ -f "${{RUNFILES_DIR}}/{workspace_name}/{tool_short_path}" ]; then
    SCRIPT_PATH="${{RUNFILES_DIR}}/{workspace_name}/{tool_short_path}"
else
    SCRIPT_PATH="$(find "$(dirname "${{BASH_SOURCE[0]}}")" -name "sync_drive.py" 2>/dev/null | head -n 1 || true)"
fi

if [ -z "$SCRIPT_PATH" ] || [ ! -f "$SCRIPT_PATH" ]; then
    if [ -f "$WORKSPACE_DIR/{tool_short_path}" ]; then
        SCRIPT_PATH="$WORKSPACE_DIR/{tool_short_path}"
    fi
fi

if [ -z "$SCRIPT_PATH" ] || [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Could not locate sync_drive.py" >&2
    exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_PATH" \\
    --workspace-dir "$WORKSPACE_DIR" \\
    --target-dir "$TARGET_DIR" \\
    --remote-path "{remote_path}" \\
    --course-name "{course_name}" \\
    --root-folder-name "{root_folder_name}" \\
    --root-folder-id "{root_folder_id}" \\
    --token-file "{token_file}" \\
    "$@"
""".format(
        tool_short_path = py_tool.short_path,
        workspace_name = ctx.workspace_name,
        remote_path = remote_path,
        course_name = course_name,
        root_folder_name = root_folder_name,
        root_folder_id = ctx.attr.root_folder_id,
        token_file = ctx.attr.token_file,
    )

    ctx.actions.write(
        output = runner,
        content = script_content,
        is_executable = True,
    )

    return [
        DefaultInfo(
            executable = runner,
            runfiles = ctx.runfiles(files = [py_tool]),
        ),
    ]

sync = rule(
    implementation = _sync_impl,
    executable = True,
    attrs = {
        "remote_path": attr.string(
            default = "",
            doc = "Remote path in Google Drive (e.g. 'helsinki/financial_economics_1', 'gostock').",
        ),
        "course_name": attr.string(
            default = "",
            doc = "Optional subfolder/course name.",
        ),
        "root_folder_name": attr.string(
            default = "",
            doc = "Optional root Google Drive folder name.",
        ),
        "root_folder_id": attr.string(
            default = "",
            doc = "Optional Google Drive ID for the root directory.",
        ),
        "token_file": attr.string(
            default = "",
            doc = "Optional explicit path to .google_drive_token.json.",
        ),
        "_sync_tool": attr.label(
            default = "//:sync_drive.py",
            allow_single_file = True,
        ),
    },
    doc = "Syncs files between configured Google Drive remote path and local directories.",
)

def _sync_test_impl(ctx):
    runner = ctx.actions.declare_file(ctx.label.name + ".sh")
    test_file = ctx.file.test_file
    all_files = ctx.files.data + [test_file]

    content = """#!/usr/bin/env bash
set -euo pipefail
TEST_DIR="$(dirname "${{BASH_SOURCE[0]}}")"
if [ -f "$TEST_DIR/{test_path}" ]; then
    EXEC_PATH="$TEST_DIR/{test_path}"
elif [ -f "${{BASH_SOURCE[0]}}.runfiles/_main/{test_path}" ]; then
    EXEC_PATH="${{BASH_SOURCE[0]}}.runfiles/_main/{test_path}"
elif [ -f "${{BASH_SOURCE[0]}}.runfiles/{workspace_name}/{test_path}" ]; then
    EXEC_PATH="${{BASH_SOURCE[0]}}.runfiles/{workspace_name}/{test_path}"
else
    EXEC_PATH="{test_path}"
fi
exec python3 "$EXEC_PATH"
""".format(
        test_path = test_file.short_path,
        workspace_name = ctx.workspace_name,
    )

    ctx.actions.write(
        output = runner,
        content = content,
        is_executable = True,
    )

    return [
        DefaultInfo(
            executable = runner,
            runfiles = ctx.runfiles(files = all_files),
        ),
    ]

sync_test = rule(
    implementation = _sync_test_impl,
    test = True,
    attrs = {
        "test_file": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "data": attr.label_list(
            allow_files = True,
            default = [],
        ),
    },
    doc = "Runs unit tests.",
)
