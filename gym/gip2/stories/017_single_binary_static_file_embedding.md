# Story 017: Single-Binary Static File Embedding

## User Story
**As a** deployment engineer,  
**I want** HTML templates, CSS files, and JavaScript assets to be embedded directly into the compiled executable,  
**So that** the entire application ships as a single, portable binary with no filesystem dependencies on external assets.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 10: *Sending and receiving data*
* **Sections:**
  - 10.1 *Serving static content (Embedding files in a binary with `embed`, Serving subdirectories)*

---

## 🎯 What You Will Learn
1. Using the `embed` standard library package and the `//go:embed` directive.
2. Creating an `embed.FS` virtual filesystem.
3. Parsing templates from an embedded filesystem via `template.ParseFS`.
4. Serving embedded static CSS/JS assets using `http.FileServer(http.FS(subFS))`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Embed Web Assets
In `web/assets.go`:
```go
package web

import (
	"embed"
	"io/fs"
	"net/http"
)

//go:embed static/*
var StaticFS embed.FS

//go:embed templates/*
var TemplateFS embed.FS

// StaticHandler serves the embedded /static directory.
func StaticHandler() http.Handler {
	sub, err := fs.Sub(StaticFS, "static")
	if err != nil {
		panic(err)
	}
	return http.FileServer(http.FS(sub))
}
```

### 2. Mount Static Route in Router
In `internal/server/server.go`:
```go
// Mount static assets at /static/
s.mux.Handle("GET /static/", http.StripPrefix("/static/", web.StaticHandler()))
```

### 3. Parse Templates from Embedded FS
```go
tmpl, err := template.New("").Funcs(templateFuncs()).ParseFS(web.TemplateFS, "templates/*.html")
```

---

## ✅ Acceptance Criteria
- [ ] Running `go build -o bin/gostock-server ./cmd/gostock-server` produces a single binary.
- [ ] Moving `bin/gostock-server` to any other directory (e.g. `/tmp`) runs without missing CSS or templates.
- [ ] Static files are served with correct MIME types and HTTP cache headers.
