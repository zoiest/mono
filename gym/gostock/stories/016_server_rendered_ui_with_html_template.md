# Story 016: Server-Rendered UI with html/template

## User Story
**As an** end user visiting `http://localhost:8080/`,  
**I want to** view a clean stock watchlist web page with financial metrics and visual green/red change indicators,  
**So that** I can track stock prices directly in my browser.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 9: *HTML and email template patterns*
* **Sections:**
  - 9.1 *Working with HTML templates (Standard library HTML package overview, Adding functionality inside templates, Mixing templates/layouts)*

---

## 🎯 What You Will Learn
1. Using the standard library `html/template` package (which provides contextual auto-escaping to protect against XSS).
2. Registering custom template helper functions with `template.FuncMap`.
3. Creating modular layouts (`base.html`) and partials (`quote_row.html`).
4. Rendering templates safely with data contexts.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Helper Functions
In `internal/server/templates.go`:
```go
package server

import (
	"fmt"
	"html/template"
)

func templateFuncs() template.FuncMap {
	return template.FuncMap{
		"formatMoney": func(v float64) string {
			return fmt.Sprintf("$%.2f", v)
		},
		"formatPercent": func(v float64) string {
			return fmt.Sprintf("%+.2f%%", v)
		},
		"colorClass": func(v float64) string {
			if v > 0 {
				return "text-success"
			} else if v < 0 {
				return "text-danger"
			}
			return "text-muted"
		},
	}
}
```

### 2. Create Layout & Views
In `web/templates/base.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>gostock Dashboard</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <h1>📈 gostock Dashboard</h1>
    </header>
    <main>
        {{ template "content" . }}
    </main>
</body>
</html>
```

In `web/templates/index.html`:
```html
{{ define "content" }}
<table class="table">
    <thead>
        <tr>
            <th>Symbol</th>
            <th>Price</th>
            <th>Change</th>
            <th>Change %</th>
            <th>Volume</th>
            <th>Provider</th>
        </tr>
    </thead>
    <tbody>
        {{ range .Quotes }}
        <tr>
            <td><strong>{{ .Symbol }}</strong></td>
            <td>{{ formatMoney .Price }}</td>
            <td class="{{ colorClass .Change }}">{{ formatMoney .Change }}</td>
            <td class="{{ colorClass .Change }}">{{ formatPercent .ChangePercent }}</td>
            <td>{{ .Volume }}</td>
            <td><span class="badge">{{ .Provider }}</span></td>
        </tr>
        {{ end }}
    </tbody>
</table>
{{ end }}
```

---

## ✅ Acceptance Criteria
- [ ] Visiting `/` renders the HTML table with current stock quotes.
- [ ] Positive price movements render with green styling; negative with red.
- [ ] Values are safely auto-escaped.
