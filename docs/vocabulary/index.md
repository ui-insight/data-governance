# Vocabulary Registry

The UI Insight application portfolio uses a **federated vocabulary** approach: each application maintains its own AllowedValue seed data tuned to its domain, but this registry provides a unified view across all applications. This makes it possible to identify shared concepts, spot inconsistencies, and guide new applications toward established patterns.

## Landscape Summary

| Domain | Application | Value Groups | Total Values |
|---|---|---|---|
| Research Admin | OpenERA | 10 | 72 |
| Communications | UCM Daily Register | 9 | 37 |
| Internal Audit | Audit Dashboard | 8 | 30 |
| Strategic Planning | StratPlan Tactics | N/A (inline) | ~15 |

!!! info "StratPlan Tactics"
    StratPlan Tactics is a JSON-file-backed application without a database. Its categorical values are defined inline in configuration files rather than in an AllowedValue table. They are included here for completeness because they still represent controlled vocabularies that could migrate to the AllowedValue pattern in the future.

## Federation Approach

Each application is the **authoritative source** for its own vocabulary. There is no central vocabulary server or shared database table. Instead, governance happens through documentation and convention:

1. **Local ownership** -- Each application team defines, seeds, and maintains the AllowedValue rows relevant to their domain. Values are stored in JSON seed files under `backend/data/` and loaded idempotently at startup.

2. **Registry observation** -- This governance repository catalogs all value groups across all applications, providing a read-only unified view. The catalog is updated when applications add or modify value groups.

3. **Pattern alignment** -- When multiple applications express the same concept (e.g., lifecycle status, severity levels), the [Shared Vocabulary Patterns](shared-patterns.md) page documents the overlap and recommends convergence strategies.

4. **Convention over enforcement** -- New applications are encouraged to adopt existing code values and casing conventions, but the federation model does not enforce this at the database level. Alignment is achieved through documentation, code review, and the [Extension Protocol](../governance/extension-protocol.md).

## How to Read This Registry

- **[Shared Patterns](shared-patterns.md)** -- Cross-cutting vocabulary concepts that appear in multiple applications. Start here to understand where domains overlap.
- **[Vocabularies by Domain](by-domain.md)** -- Complete listing of every value group and its codes, organized by application. Use this as a reference when building new features or onboarding to an application.

## Relationship to the AllowedValue Pattern

The AllowedValue table pattern is documented in the [Standards section](../standard/allowed-values.md). This registry focuses on the **content** of those tables (what groups and codes exist) rather than the **schema** (how the table is structured). For schema guidance, see the standards documentation.
