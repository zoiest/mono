# Story 016: Server-Rendered UI with Askama Templates

## User Story
**As an** end user visiting `http://localhost:8080/`,
**I want to** view a clean stock watchlist web page with financial metrics and green/red price change indicators,
**So that** I can track stock prices directly in my browser with compile-time verified HTML templates.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 5: *Using Structs to Structure Related Data* (Template view-model structs)
  - Chapter 6: *Enums and Pattern Matching* (Formatting conditional positive/negative price states)
  - Chapter 10: *Generic Types, Traits, and Lifetimes* (Deriving traits like `askama::Template`)

---

## 🎯 What You Will Learn
1. Type-safe, compile-time checked HTML templating using `askama` (catching missing fields or typos at `cargo build` time!).
2. Automatic HTML escaping for XSS safety.
3. Structuring template inheritance (`base.html` + `dashboard.html` + partials).
4. Mapping a Rust `Quote` domain model to a presentation view-model struct.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add `askama` to `Cargo.toml`
```toml
askama = "0.12"
```

### 2. Create HTML Templates in `templates/`
Create `templates/base.html` and `templates/dashboard.html`:
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{% block title %}rustock Dashboard{% endblock %}</title>
  <link rel="stylesheet" href="/static/styles.css" />
</head>
<body>
  <main>{% block content %}{% endblock %}</main>
</body>
</html>
```

### 3. Define Compile-Time Checked Template Structs
In `src/server/templates.rs`:
```rust
use askama::Template;
use axum::http::StatusCode;
use axum::response::{Html, IntoResponse, Response};

use crate::domain::Quote;

#[derive(Template)]
#[template(path = "dashboard.html")]
pub struct DashboardTemplate {
    pub quotes: Vec<Quote>,
}

pub fn render_template<T: Template>(tmpl: T) -> Response {
    match tmpl.render() {
        Ok(html) => Html(html).into_response(),
        Err(err) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("template error: {err}"),
        )
            .into_response(),
    }
}
```

---

## ✅ Acceptance Criteria
- [ ] `templates/base.html` and `templates/dashboard.html` render a clean stock watchlist table.
- [ ] `askama::Template` validates template variable names at compile time.
- [ ] Positive and negative changes render with distinct CSS classes (`gain` / `loss`).
- [ ] Visiting `GET /` returns `text/html; charset=utf-8` with XSS-escaped output.
