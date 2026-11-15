# Story 003: Multi-Source Configuration Loader

## User Story
**As an** operator of `rustock`,
**I want to** configure the application using command-line flags, environment variables, or a config file,
**So that** configuration adheres to 12-factor principles with deterministic precedence: CLI Flags > Environment Variables > Config File > Defaults.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 4: *Understanding Ownership*
    - 4.1 *What Is Ownership?*
    - 4.2 *References and Borrowing* (`String` vs `&str`, `Path` vs `PathBuf`)
  - Chapter 12: *An I/O Project: Building a Command Line Program*
    - 12.1 *Accepting Command Line Arguments* (`std::env::args`)
    - 12.2 *Reading a File* (`std::fs::read_to_string`)
    - 12.3 *Refactoring to Improve Modularity and Error Handling*
    - 12.5 *Working with Environment Variables* (`std::env::var`)
    - 12.6 *Writing Error Messages to Standard Error Instead of Standard Output* (`eprintln!`)

---

## 🎯 What You Will Learn
1. Building a `Config` struct implementing `std::default::Default`.
2. Reading CLI arguments with `std::env::args` (and upgrading to `clap` derive macros).
3. Reading environment variables safely with `std::env::var` and parsing values with `.parse()`.
4. Loading and deserializing TOML/JSON configuration files using `std::fs::read_to_string` and `std::path::Path`.
5. Understanding ownership when merging layered configuration sources.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define `AppConfig` and `Default`
In `src/config/mod.rs`:
```rust
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::Duration;

use serde::Deserialize;

use crate::domain::ProviderType;

#[derive(Debug, Clone)]
pub struct AppConfig {
    pub port: u16,
    pub provider: ProviderType,
    pub cache_ttl: Duration,
    pub request_timeout: Duration,
    pub max_workers: usize,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            port: 8080,
            provider: ProviderType::Yahoo,
            cache_ttl: Duration::from_secs(60),
            request_timeout: Duration::from_secs(5),
            max_workers: 8,
        }
    }
}
```

### 2. Define a Partial File Overlay Struct
Use `Option<T>` fields so missing keys in a config file do not overwrite defaults:
```rust
#[derive(Debug, Default, Deserialize)]
struct FileConfig {
    port: Option<u16>,
    provider: Option<ProviderType>,
    cache_ttl_secs: Option<u64>,
    request_timeout_secs: Option<u64>,
    max_workers: Option<usize>,
}
```

### 3. Implement Layered Loading (File -> Env -> CLI)
```rust
#[derive(Debug, Default)]
pub struct CliOverrides {
    pub config_path: Option<PathBuf>,
    pub port: Option<u16>,
    pub provider: Option<ProviderType>,
    pub max_workers: Option<usize>,
}

impl AppConfig {
    pub fn load(cli: CliOverrides) -> Result<Self, Box<dyn std::error::Error>> {
        let mut cfg = Self::default();

        // 1. Config file layer
        if let Some(path) = cli.config_path.as_deref() {
            cfg.apply_file(path)?;
        }

        // 2. Environment variables layer
        cfg.apply_env()?;

        // 3. CLI flags layer (highest precedence)
        if let Some(port) = cli.port {
            cfg.port = port;
        }
        if let Some(provider) = cli.provider {
            cfg.provider = provider;
        }
        if let Some(workers) = cli.max_workers {
            cfg.max_workers = workers;
        }

        Ok(cfg)
    }

    fn apply_file(&mut self, path: &Path) -> Result<(), Box<dyn std::error::Error>> {
        let contents = fs::read_to_string(path)?;
        let file_cfg: FileConfig = serde_json::from_str(&contents)?;
        if let Some(port) = file_cfg.port {
            self.port = port;
        }
        if let Some(provider) = file_cfg.provider {
            self.provider = provider;
        }
        if let Some(secs) = file_cfg.cache_ttl_secs {
            self.cache_ttl = Duration::from_secs(secs);
        }
        if let Some(secs) = file_cfg.request_timeout_secs {
            self.request_timeout = Duration::from_secs(secs);
        }
        if let Some(workers) = file_cfg.max_workers {
            self.max_workers = workers;
        }
        Ok(())
    }

    fn apply_env(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        if let Ok(val) = env::var("RUSTOCK_PORT") {
            self.port = val.parse()?;
        }
        if let Ok(val) = env::var("RUSTOCK_PROVIDER") {
            self.provider = val.parse()?;
        }
        if let Ok(val) = env::var("RUSTOCK_CACHE_TTL_SECS") {
            self.cache_ttl = Duration::from_secs(val.parse()?);
        }
        if let Ok(val) = env::var("RUSTOCK_MAX_WORKERS") {
            self.max_workers = val.parse()?;
        }
        Ok(())
    }
}
```

### 4. Parse CLI Arguments and Report Errors to `stderr`
Follow TRPL Ch 12.6 by printing configuration errors to `stderr` and exiting with a non-zero code (`std::process::exit(1)`) in `src/bin/rustock_cli.rs` (or optionally integrating `clap` with `#[derive(Parser)]`).

---

## ✅ Acceptance Criteria
- [ ] `AppConfig` implements `Default` with sensible fallback values.
- [ ] Configuration loads cleanly from JSON/TOML files, `RUSTOCK_*` environment variables, and CLI arguments.
- [ ] Precedence is strictly enforced: CLI > Env > File > Defaults.
- [ ] Unit tests verify precedence rules and invalid input handling without mutating global state unsafely.
