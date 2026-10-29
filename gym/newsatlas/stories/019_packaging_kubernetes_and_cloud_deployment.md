# Story 019: Packaging, Kubernetes & Cloud Deployment

## User Story
**As a** DevOps engineer,  
**I want to** package all services into minimal distroless container images and author cloud-neutral Helm / Kubernetes manifests,  
**So that** NewsAtlas can be deployed reliably to any Kubernetes cluster or a single cheap VM with production security settings.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 12: Cloud-Ready Applications](../writings/go_in_practice_notes.md#chapter-12-cloud-ready-applications-and-communications) — §12.1 Minimal multi-stage container builds with `CGO_ENABLED=0`, §12.4 Kubernetes health probes (`/livez`, `/readyz`), §12.5 Distroless deployments and non-root execution.
- [The Ten Cardinal Rules](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Rule 9: *Build cloud-native, minimal binaries*.

---

## 🎯 What You Will Learn
- **Core Objective:** Run the whole thing the way production systems run.
- **Architectural Concepts:** Multi-stage Docker builds, distroless/non-root images, SBOMs, Helm
(umbrella + subcharts), values schemas, probes, resource requests/limits,
HPA, PodDisruptionBudgets, NetworkPolicies, Ingress + TLS, secrets, config maps,
rolling updates, init containers/Jobs for migrations.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Multi-stage Dockerfile template; build all images in CI with
   `docker buildx`; push to **GHCR or Docker Hub** (any registry works).
2. Helm: one subchart per service from a shared **library chart** (deployment,
   service, probes, config, HPA). Umbrella chart `newsatlas`.
3. `k3d`/`kind` local cluster: `task k8s:up` deploys everything.
4. Migrations as a Helm hook Job (or init container) - discuss trade-offs.
5. NetworkPolicies: only `api-gateway` is reachable from Ingress; plug-in pods
   have **no egress**.
6. Secrets via Kubernetes Secrets sealed with `sops`/`sealed-secrets`, or
   OpenBao/Vault with the CSI/agent injector (stretch).
7. HPA on CPU and on a custom metric (consumer lag via KEDA - stretch).
8. Deploy to a real cluster/VM (see section 13) and put TLS in front.
9. Rolling update test: deploy while k6 runs; zero failed requests.
10. **Stateful pieces**: TimescaleDB and Postgres need backups (`pg_dump`/WAL
    archiving to any object storage) and a *restore drill*; Redis Streams
    persistence (AOF) and `MAXLEN` sizing; test "rebuild everything derived from
    raw events" (links, bars -> aggregates, events) after restoring.
11. Cost control for a personal deployment: right-size, use one small node,
    compression on old chunks, short retention for 1m bars, and a monthly cost
    note in `docs/notes`.

---

## 🤔 Reflection & Architectural Questions
Why separate **liveness** from **readiness**, and why should a broken Redis
make pods *unready* rather than *restart*?
