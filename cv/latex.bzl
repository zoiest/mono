"""Starlark rule for compiling LaTeX documents to PDF using local TeX distribution."""

def _latex_pdf_impl(ctx):
    out_pdf = ctx.actions.declare_file(ctx.label.name + ".pdf")
    main_tex = ctx.file.main
    srcs = ctx.files.srcs + [main_tex]

    compiler = ctx.attr.compiler

    # Main filename without extension
    main_basename = main_tex.basename
    if main_basename.endswith(".tex"):
        main_basename = main_basename[:-4]

    # Command script to build LaTeX in temporary directory and output PDF
    cmd = """
    set -e
    # Save absolute output PDF path before changing directory
    ABS_OUT_PDF="$(pwd)/{out_pdf_path}"
    BUILD_DIR=$(mktemp -d)
    
    # Copy all source files to temporary build directory
    for f in {src_paths}; do
        cp "$f" "$BUILD_DIR/"
    done

    cd "$BUILD_DIR"
    
    # Pass 1 & Pass 2 to resolve page numbers, hyperlinks, cross-references
    {compiler} -interaction=nonstopmode -halt-on-error "{main_name}" > /dev/null 2>&1 || {compiler} -interaction=nonstopmode "{main_name}"
    {compiler} -interaction=nonstopmode -halt-on-error "{main_name}"
    
    cp "{main_basename}.pdf" "$ABS_OUT_PDF"
    rm -rf "$BUILD_DIR"
    """.format(
        out_pdf_path = out_pdf.path,
        src_paths = " ".join([f.path for f in srcs]),
        compiler = compiler,
        main_name = main_tex.basename,
        main_basename = main_basename,
    )

    ctx.actions.run_shell(
        inputs = srcs,
        outputs = [out_pdf],
        command = cmd,
        env = {
            "PATH": "/Library/TeX/texbin:/usr/local/bin:/usr/bin:/bin",
        },
        mnemonic = "LatexPdf",
        progress_message = "Compiling LaTeX document %s -> %s.pdf" % (main_tex.basename, ctx.label.name),
    )

    return [DefaultInfo(files = depset([out_pdf]))]

latex_pdf = rule(
    implementation = _latex_pdf_impl,
    attrs = {
        "main": attr.label(
            mandatory = True,
            allow_single_file = [".tex"],
            doc = "The main LaTeX entrypoint file (.tex)",
        ),
        "srcs": attr.label_list(
            allow_files = True,
            default = [],
            doc = "Additional source files required for compilation (e.g. style files, images, bibliography)",
        ),
        "compiler": attr.string(
            default = "pdflatex",
            doc = "LaTeX compiler executable (pdflatex, xelatex, lualatex)",
        ),
    },
    doc = "Compiles a LaTeX entrypoint file into a PDF document.",
)
