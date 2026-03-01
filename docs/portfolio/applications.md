# Application Portfolio

The UI Insight portfolio comprises six applications serving four institutional domains at the University of Idaho. All applications share a FastAPI + React foundation and common deployment practices; most use PostgreSQL as the operational store.

## Summary

| Application | Domain | Tables | AI Integration | Auth | Production Status |
|---|---|---|---|---|---|
| OpenERA | Research Administration | 31 | Multi-endpoint configurable | JWT (5 roles) | Production |
| UCM Daily Register | Communications | 10 | Claude / OpenAI / MindRouter | None | Production |
| Audit Dashboard | Internal Audit | 13 | MindRouter OCR + LLM | JWT (2 roles) | Production |
| StratPlan Tactics | Strategic Planning | JSON canonical model + optional insight-db projection (10 tables) | None | None | Production |
| ProcessMapping | Process Improvement | TBD | None | None | Development |
| AISPEG | Strategic Planning | TBD | Claude / OpenAI | None | Development |

---

## OpenERA

**Domain:** Research Administration
**Repository:** [ui-insight/OpenERA](https://github.com/ui-insight/OpenERA)
**Domain docs:** [Research Administration](../domains/research-admin.md)

OpenERA is a comprehensive research administration platform for managing proposals, awards, compliance, and institutional data related to sponsored programs. It is the original application from which the AI4RA Unified Data Model (UDM) was derived, and serves as the reference implementation for portfolio-wide conventions.

The application has the most complex data model in the portfolio (31 tables), the most granular role-based access control (5 JWT roles), and supports multi-endpoint AI configuration where different LLM providers can be assigned to different tasks.

---

## UCM Daily Register

**Domain:** University Communications and Marketing
**Repository:** [ui-insight/UCMDailyRegister-App](https://github.com/ui-insight/UCMDailyRegister-App)
**Domain docs:** [Communications](../domains/communications.md)

UCM Daily Register is an AI-assisted newsletter production pipeline for the University of Idaho's University Communications and Marketing team. It produces two newsletters: The Daily Register (TDR) for faculty and staff, and My UI for students. Submissions pass through an AI editing pipeline that applies institutional style rules, generating structured diffs for human review.

The application supports three LLM providers (Claude, OpenAI, MindRouter) switchable via environment variable, and uses a database-driven style rule system that is injected into AI prompts at runtime.

---

## Audit Dashboard

**Domain:** Internal Audit
**Repository:** [ui-insight/AuditDashboard](https://github.com/ui-insight/AuditDashboard)
**Domain docs:** [Internal Audit](../domains/internal-audit.md)

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

**Domain:** Process Improvement
**Repository:** [ui-insight/ProcessMapping](https://github.com/ui-insight/ProcessMapping)

ProcessMapping is a visual process modeling tool for documenting and analyzing institutional workflows. It is currently in early development and does not yet have a domain documentation page.

---

## AISPEG

**Domain:** Strategic Planning
**Repository:** [ui-insight/AISPEG](https://github.com/ui-insight/AISPEG)

AISPEG (AI-assisted Strategic Planning Evaluation and Governance) extends the strategic planning domain with AI-powered analysis of tactic effectiveness and strategic alignment. It is currently in development and integrates with Claude and OpenAI for analytical capabilities.
