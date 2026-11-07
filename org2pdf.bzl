"""Bazel rule for compiling Org files to PDF with incremental build avoidance."""

def _org2pdf_impl(ctx):
    runner = ctx.actions.declare_file(ctx.label.name + ".sh")
    py_tool = ctx.file._compiler

    package_path = ctx.label.package

    tex2png_cmd = ""
    runfiles_list = [py_tool]

    if ctx.attr.tex2png:
        tex2png_bin = ctx.executable.tex2png
        runfiles_list.append(tex2png_bin)
        tex2png_cmd = """
# Run pre-requisite tex2png compiler
TEX2PNG_EXE="{tex2png_short_path}"
if [ -f "$TEX2PNG_EXE" ]; then
    "$TEX2PNG_EXE"
elif [ -f "${{BASH_SOURCE[0]}}.runfiles/_main/$TEX2PNG_EXE" ]; then
    "${{BASH_SOURCE[0]}}.runfiles/_main/$TEX2PNG_EXE"
elif [ -f "${{BASH_SOURCE[0]}}.runfiles/{workspace_name}/$TEX2PNG_EXE" ]; then
    "${{BASH_SOURCE[0]}}.runfiles/{workspace_name}/$TEX2PNG_EXE"
elif [ -n "${{RUNFILES_DIR:-}}" ] && [ -f "${{RUNFILES_DIR}}/_main/$TEX2PNG_EXE" ]; then
    "${{RUNFILES_DIR}}/_main/$TEX2PNG_EXE"
fi
""".format(
            tex2png_short_path = tex2png_bin.short_path,
            workspace_name = ctx.workspace_name,
        )

    script_content = """#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="${{BUILD_WORKSPACE_DIRECTORY:-$(pwd)}}"
PACKAGE_PATH="{package_path}"

if [ -n "$PACKAGE_PATH" ]; then
    TARGET_DIR="$WORKSPACE_DIR/$PACKAGE_PATH"
else
    TARGET_DIR="${{BUILD_WORKING_DIRECTORY:-$(pwd)}}"
fi
{tex2png_cmd}
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
    SCRIPT_PATH="$(find "$(dirname "${{BASH_SOURCE[0]}}")" -name "org2pdf.py" 2>/dev/null | head -n 1 || true)"
fi

if [ -z "$SCRIPT_PATH" ] || [ ! -f "$SCRIPT_PATH" ]; then
    if [ -f "$WORKSPACE_DIR/{tool_short_path}" ]; then
        SCRIPT_PATH="$WORKSPACE_DIR/{tool_short_path}"
    fi
fi

if [ -z "$SCRIPT_PATH" ] || [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Could not locate org2pdf.py" >&2
    exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_PATH" \\
    --target-dir "$TARGET_DIR" \\
    "$@"
""".format(
        tool_short_path = py_tool.short_path,
        workspace_name = ctx.workspace_name,
        package_path = package_path,
        tex2png_cmd = tex2png_cmd,
    )

    ctx.actions.write(
        output = runner,
        content = script_content,
        is_executable = True,
    )

    default_runfiles = ctx.runfiles(files = runfiles_list)
    if ctx.attr.tex2png:
        default_runfiles = default_runfiles.merge(ctx.attr.tex2png[DefaultInfo].default_runfiles)

    return [
        DefaultInfo(
            executable = runner,
            runfiles = default_runfiles,
        ),
    ]

org2pdf = rule(
    implementation = _org2pdf_impl,
    executable = True,
    attrs = {
        "_compiler": attr.label(
            default = "//:org2pdf.py",
            allow_single_file = True,
        ),
        "tex2png": attr.label(
            executable = True,
            cfg = "exec",
            doc = "Optional tex2png target to execute before compiling org files.",
        ),
    },
    doc = "Compiles Org files to PDF with incremental build avoidance.",
)
