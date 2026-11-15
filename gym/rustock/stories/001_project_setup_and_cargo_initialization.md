# Story 001: Project Setup & Cargo Initialization

## User Story
**As a** Rust developer,
**I want to** initialize a Cargo package and configure the project workspace,
**So that** I have a reproducible dependency workspace adhering to standard Rust module and crate conventions.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 1: *Getting Started*
    - 1.1 *Installation* (`rustup`, `rustc`, `cargo`)
    - 1.2 *Hello, World!*
    - 1.3 *Hello, Cargo!* (`Cargo.toml`, `cargo build`, `cargo run`, `cargo check`)
  - Chapter 7: *Managing Growing Projects with Packages, Crates, and Modules*
    - 7.1 *Packages and Crates* (Library crate `src/lib.rs` + Binary crates in `src/bin/`)
    - 7.2 *Defining Modules to Control Scope and Privacy*

---

## 🎯 What You Will Learn
1. Installing and verifying the Rust toolchain with `rustup`, `rustc`, and `cargo`.
2. How Cargo manages packages, editions, and dependencies via `Cargo.toml` and `Cargo.lock`.
3. Structuring a Rust package with both a reusable library crate (`src/lib.rs`) and binary entrypoints (`src/bin/`).
4. Using core Cargo workflow commands: `cargo check`, `cargo build`, `cargo run`, `cargo clippy`, and `cargo fmt`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Install the Rust Toolchain (if not yet installed)
Install Rust via `rustup`:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustc --version
cargo --version
```

### 2. Configure `Cargo.toml`
Define the `rustock` package and `rustock-cli` binary target in `Cargo.toml`:
```toml
[package]
name = "rustock"
version = "0.1.0"
edition = "2024"
description = "Multi-provider stock data aggregator and web dashboard written in Rust"

[[bin]]
name = "rustock-cli"
path = "src/bin/rustock_cli.rs"
```

### 3. Create the Library Root and CLI Entrypoint
Create `src/lib.rs`:
```rust
//! `rustock`: Multi-provider financial data aggregator library.

pub mod domain;
```

Create `src/bin/rustock_cli.rs`:
```rust
fn main() {
    println!(
        "rustock: Financial data aggregator v{}",
        env!("CARGO_PKG_VERSION")
    );
}
```

### 4. Verify Toolchain Formatting and Linting
Run standard Rust hygiene tools:
```bash
cargo fmt --check
cargo clippy --all-targets
cargo run --bin rustock-cli
```

---

## ✅ Acceptance Criteria
- [X] `Cargo.toml` is configured at the project root with package `rustock` and binary `rustock-cli`.
- [X] `src/lib.rs` defines the library root module structure.
- [X] `src/bin/rustock_cli.rs` prints the version message cleanly using `env!("CARGO_PKG_VERSION")`.
- [X] `.gitignore` excludes `/target` and build artifacts.
