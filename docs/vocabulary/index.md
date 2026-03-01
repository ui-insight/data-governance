# Vocabulary Registry

The UI Insight application portfolio uses a **federated vocabulary** approach: each application maintains its own AllowedValue seed data tuned to its domain, but this registry provides a unified view across all applications. This makes it possible to identify shared concepts, spot inconsistencies, and guide new applications toward established patterns.

## Landscape Summary

| Domain | Application | Value Groups | Total Values |
|---|---|---|---|
| Research Admin | OpenERA | 21 | 156 |
| Communications | UCM Daily Register | 9 | 37 |
| Internal Audit | Audit Dashboard | 8 | 30 |
| Strategic Planning | StratPlan Tactics | 8 (inline/code-normalized) | 33 |

!!! info "StratPlan Tactics"
    StratPlan keeps canonical data in JSON and normalizes enum values in API/service layers (rather than an `AllowedValue` table). These values are documented here for governance consistency and potential future migration to a database-managed vocabulary model.

## Federation Approach

Each application is the **authoritative source** for its own vocabulary. There is no central vocabulary server or shared database table. Instead, governance happens through documentation and convention:

1. **Local ownership** -- Each application team defines, seeds, and maintains the AllowedValue rows relevant to their domain. DB-backed apps usually store seed values under `backend/data/`; StratPlan currently defines its enum domains in data/service layers.

2. **Registry observation** -- This governance repository catalogs all value groups across all applications, providing a read-only unified view. The catalog is updated when applications add or modify value groups.

3. **Pattern alignment** -- When multiple applications express the same concept (e.g., lifecycle status, severity levels), the [Shared Vocabulary Patterns](shared-patterns.md) page documents the overlap and recommends convergence strategies.

4. **Convention over enforcement** -- New applications are encouraged to adopt existing code values and casing conventions, but the federation model does not enforce this at the database level. Alignment is achieved through documentation, code review, and the [Extension Protocol](../governance/extension-protocol.md).

## How to Read This Registry

- **[Shared Patterns](shared-patterns.md)** -- Cross-cutting vocabulary concepts that appear in multiple applications. Start here to understand where domains overlap.
- **[Vocabularies by Domain](by-domain.md)** -- Complete listing of every value group and its codes, organized by application. Use this as a reference when building new features or onboarding to an application.

## Check-Constrained Enums

Some tables use SQL CHECK constraints rather than the AllowedValue pattern for categorical columns. These values are enforced at the database level and are not editable at runtime. Currently this applies to the RFA Analysis tables in OpenERA (4 constrained columns with 21 total values). OpenERA, UCM Daily Register, and StratPlan normalized enums use `snake_case` naming; Audit Dashboard uses `UPPER_CASE`. See [Research Administration](../domains/research-admin.md#check-constrained-enums-rfa-analysis) for the complete listing.

## Relationship to the AllowedValue Pattern

The AllowedValue table pattern is documented in the [Standards section](../standard/allowed-values.md). This registry focuses on the **content** of those tables (what groups and codes exist) rather than the **schema** (how the table is structured). For schema guidance, see the standards documentation.
