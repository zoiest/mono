"""Bazel rule for compiling Org files to HTML with incremental build avoidance."""

def _org2html_impl(ctx):
    runner = ctx.actions.declare_file(ctx.label.name + ".sh")
    py_tool = ctx.file._compiler

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
else
    SCRIPT_PATH="$(find "$(dirname "${{BASH_SOURCE[0]}}")" -name "org2html.py" 2>/dev/null | head -n 1 || true)"
fi

if [ -z "$SCRIPT_PATH" ] || [ ! -f "$SCRIPT_PATH" ]; then
    if [ -f "$WORKSPACE_DIR/{tool_short_path}" ]; then
        SCRIPT_PATH="$WORKSPACE_DIR/{tool_short_path}"
    fi
fi

if [ -z "$SCRIPT_PATH" ] || [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Could not locate org2html.py" >&2
    exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_PATH" \\
    --target-dir "$TARGET_DIR" \\
    "$@"
""".format(
        tool_short_path = py_tool.short_path,
        workspace_name = ctx.workspace_name,
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

org2html = rule(
    implementation = _org2html_impl,
    executable = True,
    attrs = {
        "_compiler": attr.label(
            default = "//:org2html.py",
            allow_single_file = True,
        ),
    },
    doc = "Compiles Org files to HTML with incremental build avoidance.",
)
