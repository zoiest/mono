# Story 022: Cargo Workspaces, Custom Macros & Advanced Rust

## User Story
**As an** advanced Rust developer,
**I want to** organize `rustock` as a multi-crate Cargo Workspace, enforce domain invariants with the Newtype pattern, and generate boilerplate validation via macros,
**So that** I understand how Rust achieves compile-time metaprogramming without runtime reflection overhead.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 14: *More About Cargo and Crates.io*
    - 14.3 *Cargo Workspaces*
  - Chapter 20: *Advanced Features*
    - 20.1 *Unsafe Rust* (Understanding when `unsafe` is justified vs safe abstractions)
    - 20.2 *Advanced Traits* (Associated types, operator overloading, supertraits)
    - 20.3 *Advanced Types* (The Newtype pattern for type safety and external trait impls)
    - 20.5 *Macros* (Declarative `macro_rules!` and Procedural Derive Macros)

---

## 🎯 What You Will Learn
1. Refactoring a single package into a Cargo Workspace (`crates/rustock-core`, `crates/rustock-macros`, `crates/rustock-server`).
2. Applying the **Newtype pattern** (`pub struct TickerSymbol(String);`) to enforce uppercase, non-empty ticker invariants at construction time ("parse, don't validate").
3. Writing a declarative macro (`macro_rules!`) to eliminate repetitive test or provider builder boilerplate.
4. Writing a custom `#[derive(Validate)]` procedural macro in `crates/rustock-macros` (`proc-macro = true`) as Rust's zero-runtime-cost alternative to reflection!

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Convert to a Cargo Workspace
In root `Cargo.toml`:
```toml
[workspace]
resolver = "3"
members = [
    "crates/rustock-core",
    "crates/rustock-macros",
    "crates/rustock-server",
]
```

### 2. Apply the Newtype Pattern (`TickerSymbol`)
In `crates/rustock-core/src/domain/symbol.rs`:
```rust
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct TickerSymbol(String);

impl TickerSymbol {
    pub fn parse(raw: &str) -> Result<Self, String> {
        let trimmed = raw.trim().to_ascii_uppercase();
        if trimmed.is_empty() || trimmed.len() > 10 {
            return Err(format!("invalid ticker symbol: '{raw}'"));
        }
        if !trimmed.chars().all(|c| c.is_ascii_alphanumeric() || c == '.' || c == '-') {
            return Err(format!("invalid characters in symbol: '{raw}'"));
        }
        Ok(Self(trimmed))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for TickerSymbol {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}
```

### 3. Build a Declarative Macro & Procedural Derive Macro
- Use `macro_rules! quote_fixture` to concisely generate test `Quote` instances.
- Create `crates/rustock-macros` (`proc-macro = true`) with `syn` and `quote` to implement `#[derive(Validate)]`, generating compile-time field validation methods on structs without runtime reflection!

---

## ✅ Acceptance Criteria
- [ ] Project compiles cleanly as a multi-crate Cargo Workspace (`cargo test --workspace`).
- [ ] `TickerSymbol` newtype enforces valid ticker invariants at construction time.
- [ ] Declarative `macro_rules!` reduces test fixture boilerplate cleanly.
- [ ] Procedural macro `#[derive(Validate)]` generates compile-time `fn validate(&self) -> Result<(), Vec<String>>` implementations.
