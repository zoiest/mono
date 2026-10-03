# Story 021: Minimal Distroless Dockerization

## User Story
**As a** cloud security and release engineer,  
**I want to** build a minimal multi-stage Docker container image for `gostock`,  
**So that** the image size is tiny (< 25MB), free of shell/package manager vulnerabilities, and runs as an unprivileged user.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 12: *Cloud-ready applications and communications*
* **Sections:**
  - 12.1 *Containers and cloud-native applications*
  - 12.5 *Building for the cloud (Static compilation with `CGO_ENABLED=0`)*

---

## 🎯 What You Will Learn
1. Docker multi-stage builds for compiled Go binaries.
2. Disabling CGO (`CGO_ENABLED=0`) for a 100% statically linked binary.
3. Stripping debugging symbols with `-ldflags="-s -w"` to reduce binary footprint.
4. Including root CA certificates (`ca-certificates`) so outbound HTTPS to Yahoo/Finviz succeeds inside scratch/distroless containers.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Create Multi-Stage Dockerfile
In `Dockerfile`:
```dockerfile
# Build Stage
FROM golang:1.23-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Compile static binary
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /bin/gostock-server ./cmd/gostock-server

# Runtime Stage
FROM gcr.io/distroless/static-debian12:nonroot

USER nonroot:nonroot
WORKDIR /app

COPY --from=builder /bin/gostock-server /app/gostock-server

EXPOSE 8080

ENTRYPOINT ["/app/gostock-server"]
```

---

## ✅ Acceptance Criteria
- [ ] Multi-stage `Dockerfile` created at repository root.
- [ ] Container image size is under 25MB.
- [ ] Runs as non-root user (`nonroot:nonroot`).
- [ ] Outbound HTTPS requests to Yahoo Finance work properly with bundled TLS root certificates.
