# Vocabulary Registry

The UI Insight application portfolio uses a **federated vocabulary** approach: each onboarded governance application maintains its own AllowedValue seed data tuned to its domain, and this registry provides a unified view across the currently documented set. This makes it possible to identify shared concepts, spot inconsistencies, and guide new applications toward established patterns.

## Landscape Summary

| Domain | Application | Value Groups | Total Values |
|---|---|---|---|
| Research Admin | OpenERA | 21 | 142 |
| Communications | UCM Daily Register | 10 | 37 |
| Internal Audit | Audit Dashboard | 8 | 32 |
| Process Intelligence | ProcessMapping | 9 (JSON-managed) | 70 |
| Strategic Planning | StratPlan Tactics | 8 (inline/code-normalized) | 34 |

!!! info "StratPlan Tactics"
    StratPlan keeps canonical data in JSON and normalizes enum values in API/service layers (rather than an `AllowedValue` table). These values are documented here for governance consistency and potential future migration to a database-managed vocabulary model.

!!! info "ProcessMapping"
    ProcessMapping stores controlled values in governed JSON reference data (`data/allowed_values.json`) rather than a runtime database table. These groups are included in the registry because they shape canonical process maps, workflow definitions, and transcript-derived assets.

## Federation Approach

Each application is the **authoritative source** for its own vocabulary. There is no central vocabulary server or shared database table. Instead, governance happens through documentation and convention:

1. **Local ownership** -- Each application team defines and maintains the coded values relevant to its domain. DB-backed apps usually store seed values under `backend/data/`; ProcessMapping stores governed values in `data/allowed_values.json`; StratPlan currently defines its enum domains in data/service layers.

2. **Registry observation** -- This governance repository catalogs value groups for the onboarded governance applications, providing a read-only unified view. The catalog is updated when applications add or modify value groups.

3. **Pattern alignment** -- When multiple applications express the same concept (e.g., lifecycle status, severity levels), the [Shared Vocabulary Patterns](shared-patterns.md) page documents the overlap and recommends convergence strategies.

4. **Convention over enforcement** -- New applications are encouraged to adopt existing code values and casing conventions, but the federation model does not enforce this at the database level. Alignment is achieved through documentation, code review, and the [Extension Protocol](../governance/extension-protocol.md).

## How to Read This Registry

- **[Shared Patterns](shared-patterns.md)** -- Cross-cutting vocabulary concepts that appear in multiple applications. Start here to understand where domains overlap.
- **[Vocabularies by Domain](by-domain.md)** -- Complete listing of every value group and its codes, organized by application. Use this as a reference when building new features or onboarding to an application.

## Check-Constrained Enums

Some tables use SQL CHECK constraints rather than the AllowedValue pattern for categorical columns. These values are enforced at the database level and are not editable at runtime. Currently this applies to the RFA Analysis tables in OpenERA (4 constrained columns with 21 total values). OpenERA, UCM Daily Register, and StratPlan normalized enums use `snake_case` naming; Audit Dashboard and ProcessMapping use `UPPER_CASE`. See [Research Administration](../domains/research-admin.md#check-constrained-enums-rfa-analysis) for the complete listing.

## Relationship to the AllowedValue Pattern

The AllowedValue table pattern is documented in the [Standards section](../standard/allowed-values.md). This registry focuses on the **content** of those tables (what groups and codes exist) rather than the **schema** (how the table is structured). For schema guidance, see the standards documentation.
