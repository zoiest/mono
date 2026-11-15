# Story 021: Minimal Distroless Dockerization

## User Story
**As a** cloud security and release engineer,
**I want to** package `rustock-server` in a minimal multi-stage static Docker image,
**So that** the production container is tiny (< 25MB), free of shells or package managers, and runs as a non-root user.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 14: *More About Cargo and Crates.io*
    - 14.1 *Customizing Builds with Release Profiles* (`strip`, `lto`, `panic = "abort"`)

---

## 🎯 What You Will Learn
1. Compiling a 100% statically linked Linux Rust binary using the `x86_64-unknown-linux-musl` target.
2. Using `rustls` (pure Rust TLS) instead of OpenSSL so zero dynamic `.so` C libraries are needed at runtime.
3. Caching Cargo dependency builds cleanly in Docker multi-stage builds (or with `cargo-chef`).
4. Stripping symbols in `[profile.release]` and running on `gcr.io/distroless/static-debian12:nonroot`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Configure Release Stripping in `Cargo.toml`
```toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = "symbols"
panic = "abort"
```

### 2. Create Multi-Stage `Dockerfile`
```dockerfile
# Stage 1: Build static musl binary
FROM rust:1.86-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src
COPY templates ./templates
COPY web ./web

RUN cargo build --release --bin rustock-server

# Stage 2: Minimal distroless runtime
FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /app/target/release/rustock-server /rustock-server

EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/rustock-server"]
```

### 3. Build and Verify Image Size & Probes
```bash
docker build -t rustock:latest .
docker images rustock:latest
docker run --rm -p 8080:8080 rustock:latest
```

---

## ✅ Acceptance Criteria
- [ ] `Dockerfile` builds a statically linked `rustock-server` binary using `musl` and `rustls`.
- [ ] Runtime image uses `distroless/static-debian12:nonroot` (or `scratch` + CA certs) with no shell.
- [ ] Outbound HTTPS calls to Yahoo/Finviz succeed inside the minimal container.
- [ ] Final image size is under 25MB.
