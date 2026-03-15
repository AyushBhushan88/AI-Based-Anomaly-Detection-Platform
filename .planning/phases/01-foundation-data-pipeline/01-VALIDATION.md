---
phase: 1
slug: foundation-data-pipeline
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-03-15
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | pytest.ini |
| **Quick run command** | `pytest tests/unit` |
| **Full suite command** | `pytest tests` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/unit`
- **After every plan wave:** Run `pytest tests`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | STREAM-01 | integration | `pytest tests/integration/test_kafka_connection.py` | ❌ W0 | ⬜ pending |
| 01-01-02 | 01 | 1 | DB-01 | integration | `pytest tests/integration/test_db_connection.py` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 1 | DB-01, DB-03 | unit | `pytest tests/unit/test_schema.py` | ❌ W0 | ⬜ pending |
| 01-03-01 | 03 | 2 | STREAM-02, DB-01 | integration | `pytest tests/integration/test_ingestion_pipeline.py` | ❌ W0 | ⬜ pending |
| 01-03-02 | 03 | 2 | DB-02 | unit | `pytest tests/unit/test_audit_trail.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/conftest.py` — shared fixtures for Kafka and DB connections
- [ ] `tests/unit/test_schema.py` — stubs for DB-01, DB-03
- [ ] `tests/integration/test_kafka_connection.py` — stubs for STREAM-01
- [ ] `tests/integration/test_db_connection.py` — stubs for DB-01
- [ ] `pytest-postgresql`, `pytest-docker` — install if not detected

---

## Manual-Only Verifications

"All phase behaviors have automated verification."

---

## Validation Sign-Off

- [ ] All tasks have <automated> verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending 2026-03-15
