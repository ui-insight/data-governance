# Application Portfolio

The UI Insight portfolio includes several active repositories serving University of Idaho administrative and planning needs. This governance repository currently has complete domain-model coverage for five applications. AISPEG remains in the broader portfolio, but it is tracked as adjacent program infrastructure rather than a governed application data model.

## Summary

| Application | Domain | Tables / Model | AI Integration | Auth | Governance Coverage |
|---|---|---|---|---|---|
| OpenERA | Research Administration | 32 tables | Multi-endpoint configurable | JWT (5 roles) | Complete |
| UCM Daily Register | Communications | 10 tables | Claude / OpenAI / MindRouter | None | Complete |
| Audit Dashboard | Internal Audit | 13 tables | MindRouter OCR + LLM | JWT (2 roles) | Complete |
| StratPlan Tactics | Strategic Planning | JSON canonical model + optional insight-db projection (10 tables) | None | None | Complete |
| ProcessMapping | Process Intelligence | 15 process maps + 11 workflows + optional `process_maps` projection | None | None | Complete |
| AISPEG | Strategic Planning collaboration site | Content/site-oriented app | None documented in repo | None | Out of scope |

---

## OpenERA

**Domain:** Research Administration
**Repository:** [ui-insight/OpenERA](https://github.com/ui-insight/OpenERA)
**Domain docs:** [Research Administration](../domains/research-admin.md)

OpenERA is a comprehensive research administration platform for managing proposals, awards, compliance, and institutional data related to sponsored programs. It is the original application from which the AI4RA Unified Data Model (UDM) was derived, and serves as the reference implementation for portfolio-wide conventions.

The application has the most complex data model in the portfolio (32 tables), the most granular role-based access control (5 JWT roles), and supports multi-endpoint AI configuration where different LLM providers can be assigned to different tasks.

---

## UCM Daily Register

**Domain:** University Communications and Marketing
**Repository:** [ui-insight/UCMDailyRegister](https://github.com/ui-insight/UCMDailyRegister)
**Domain docs:** [Communications](../domains/communications.md)

UCM Daily Register is an AI-assisted newsletter production pipeline for the University of Idaho's University Communications and Marketing team. It produces two newsletters: The Daily Register (TDR) for faculty and staff, and My UI for students. Submissions pass through an AI editing pipeline that applies institutional style rules, generating structured diffs for human review.

The application supports three LLM providers (Claude, OpenAI, MindRouter) switchable via environment variable, and uses a database-driven style rule system that is injected into AI prompts at runtime.

---

## Audit Dashboard

**Domain:** Internal Audit
**Repository:** [ui-insight/AuditDashboard](https://github.com/ui-insight/AuditDashboard)
**Domain docs:** [Internal Audit](../domains/audit.md)

The Audit Dashboard supports the University of Idaho's Office of Internal Audit in managing audit reports, observations, corrective action items, and supporting documentation. It integrates MindRouter for OCR-based document extraction, enabling auditors to upload PDF reports and automatically extract structured observations and findings.

The application uses JWT authentication with two roles (auditor and administrator) and features an eight-stage extraction pipeline for processing audit documents through AI-assisted analysis.

---

## StratPlan Tactics

**Domain:** Strategic Planning
**Repository:** [ui-insight/StratPlanTacticsMB](https://github.com/ui-insight/StratPlanTacticsMB)
**Domain docs:** [Strategic Planning](../domains/strategic-planning.md)

StratPlan Tactics is a strategic execution and investment analytics application for University of Idaho planning workflows. It combines alignment analytics with execution status rollups, SPIGP portfolio tracking, investment analysis, and horizon reporting.

The canonical model is JSON-based, with optional `insight_db` runtime for integration and operational DB-backed reads. The application has no authentication and no AI integration.

---

## ProcessMapping

**Domain:** Process Intelligence
**Repository:** [ui-insight/ProcessMapping](https://github.com/ui-insight/ProcessMapping)
**Domain docs:** [Process Intelligence](../domains/process-mapping.md)

ProcessMapping is a full-stack process intelligence application plus canonical process-data repository. It supports interactive process-map exploration, transcript-to-process ingestion workflows, and optional `insight_db` projection for operational reads and integration.

---

## AISPEG

**Domain:** Strategic Planning
**Repository:** [ui-insight/AISPEG](https://github.com/ui-insight/AISPEG)

AISPEG is a Next.js collaboration site for the AI Strategic Planning & Evaluation Group. It does not currently define an institutionally governed application data model, controlled-vocabulary registry, or cross-app schema surface, so this repository tracks it as adjacent program infrastructure outside the schema registry.
