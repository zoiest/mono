# Story 022: Dynamic Struct Tag Validation & Codegen

## User Story
**As an** advanced Go developer,  
**I want to** build a custom struct validator using runtime reflection and automate mock generation using `go:generate`,  
**So that** I understand Go's metaprogramming capabilities, the performance trade-offs of reflection, and tooling automation.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 13: *Reflection, code generation, and advanced Go*
* **Sections:**
  - 13.1 *Three features of reflection (Switching based on type and kind, Discovering whether a value implements an interface, Accessing fields on a struct)*
  - 13.2 *Structs, tags, and annotations (Annotating structs, Processing tags on a struct)*
  - 13.3 *Generating Go code with Go code (`go generate`)*

---

## 🎯 What You Will Learn
1. Laws of Reflection in Go: converting from interface value to reflection object and vice-versa.
2. Inspecting struct fields and custom tags using `reflect.TypeOf()`.
3. Validating rules (e.g. `tag:"required,min=1"`) at runtime.
4. Using Go comments to drive code generation via `//go:generate`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build Custom Tag Inspector
In `internal/domain/validator.go`:
```go
package domain

import (
	"errors"
	"fmt"
	"reflect"
	"strings"
)

func ValidateStruct(s any) error {
	v := reflect.ValueOf(s)
	if v.Kind() == reflect.Pointer {
		v = v.Elem()
	}
	if v.Kind() != reflect.Struct {
		return errors.New("validate expects a struct or pointer to struct")
	}

	t := v.Type()
	for i := 0; i < t.NumField(); i++ {
		field := t.Field(i)
		tag := field.Tag.Get("validate")
		if tag == "" {
			continue
		}

		fieldVal := v.Field(i)
		rules := strings.Split(tag, ",")
		for _, rule := range rules {
			if rule == "required" {
				if fieldVal.IsZero() {
					return fmt.Errorf("field %s is required", field.Name)
				}
			}
		}
	}
	return nil
}
```

### 2. Add Code Generation Directive
In `internal/provider/provider.go`:
```go
//go:generate go run github.com/matryer/moq -out mock/provider_mock.go -pkg mock . StockProvider
```

Run generation via:
```bash
go generate ./...
```

---

## ✅ Acceptance Criteria
- [ ] Reflection validator returns error if a field with `validate:"required"` is zero-valued.
- [ ] Running `go generate ./...` automatically regenerates mock implementations.
