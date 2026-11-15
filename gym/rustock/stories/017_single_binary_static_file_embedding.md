# Story 017: Single-Binary Static File Embedding

## User Story
**As a** deployment engineer,
**I want** CSS stylesheets, JavaScript files, and icons to be embedded directly into the compiled Rust executable,
**So that** `rustock-server` ships as a single self-contained binary with zero external asset directory dependencies.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 14: *More About Cargo and Crates.io*
    - Crate packaging and asset inclusion
  - Chapter 20: *Advanced Features*
    - 20.5 *Macros* (Built-in macros `include_str!`, `include_bytes!`, and derive macros like `rust-embed`)

---

## 🎯 What You Will Learn
1. Using Rust's built-in compile-time macros `include_str!` and `include_bytes!`.
2. Embedding entire `web/static/` asset trees with `rust-embed` (and `mime_guess`).
3. Serving embedded assets from Axum with correct `Content-Type` and `Cache-Control` headers.
4. Preventing path traversal when resolving asset paths.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add `rust-embed` and `mime_guess` to `Cargo.toml`
```toml
rust-embed = "8"
mime_guess = "2"
```

### 2. Embed `web/static/`
In `src/server/assets.rs`:
```rust
use axum::{
    extract::Path,
    http::{header, StatusCode},
    response::{IntoResponse, Response},
};
use rust_embed::Embed;

#[derive(Embed)]
#[folder = "web/static/"]
struct StaticAssets;

pub async fn serve_static(Path(path): Path<String>) -> Response {
    let trimmed = path.trim_start_matches('/');
    match StaticAssets::get(trimmed) {
        Some(file) => {
            let mime = mime_guess::from_path(trimmed).first_or_octet_stream();
            (
                StatusCode::OK,
                [
                    (header::CONTENT_TYPE, mime.as_ref().to_string()),
                    (header::CACHE_CONTROL, "public, max-age=3600".to_string()),
                ],
                file.data.into_owned(),
            )
                .into_response()
        }
        None => StatusCode::NOT_FOUND.into_response(),
    }
}
```

### 3. Mount Route in Axum Router
```rust
.route("/static/{*path}", get(serve_static))
```

---

## ✅ Acceptance Criteria
- [ ] `web/static/styles.css` and `web/static/app.js` are embedded directly into the compiled binary.
- [ ] Running the binary from an empty `/tmp` working directory still serves `/static/styles.css` with HTTP 200 and `text/css`.
- [ ] Missing asset paths return HTTP 404 cleanly.
