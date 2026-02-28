# Upstream: AI4RA Unified Data Model

The UI Insight application portfolio adopts its data modeling conventions from the **AI4RA Unified Data Model (UDM)**, an open-source specification for research administration data.

## What is AI4RA-UDM?

The AI4RA-UDM is a database-agnostic schema specification that defines:

- **29 tables** across 8 research administration domains (Reference, Core, Pre-Award, Post-Award, Financial, Personnel & Effort, Compliance, System)
- **72 foreign key relationships** with role-based naming
- **8 pre-built SQL views** for common analytical queries
- A **naming ontology** (`PascalCase_With_Underscores`) and standard column suffixes
- The **AllowedValue pattern** for institution-specific controlled vocabularies
- **CHECK constraints** for universal standards (GAAP account types, lifecycle statuses)

The specification is maintained at [github.com/ui-insight/AI4RA-UDM](https://github.com/ui-insight/AI4RA-UDM) and published via GitHub Pages.

## What We Adopt

We adopt the UDM's **conventions and design patterns** as our institutional data modeling standard. These are domain-agnostic principles that apply equally well to research administration, communications, audit, and strategic planning:

| What | Source | Applied Across |
|---|---|---|
| `PascalCase_With_Underscores` column naming | UDM naming ontology | All DB-backed apps |
| Standard column suffixes (`_ID`, `_Date`, `_Status`, etc.) | UDM naming ontology | All DB-backed apps |
| Role-based foreign key naming | UDM relationship design | All DB-backed apps |
| `AllowedValue` controlled vocabulary table | UDM `AllowedValues` table | All DB-backed apps |
| `import sqlalchemy as sa` with `sa.` prefix | UDM reference implementation | All DB-backed apps |
| `lazy="selectin"` for async relationships | UDM reference implementation | All DB-backed apps |
| Immutable audit records | UDM System domain | UCM Daily Register, Audit Dashboard |

## What We Don't Adopt

The UDM's **domain tables** (Award, Proposal, Organization, Personnel, etc.) are specific to research administration. Our non-research applications define their own domain entities following the adopted conventions:

- **UCM Daily Register** defines `Submission`, `Newsletter`, `EditVersion`, etc. for the communications domain
- **Audit Dashboard** defines `AuditReport`, `Observation`, `ActionItem`, etc. for the audit domain
- **StratPlan Tactics** defines `Pillar`, `Priority`, `Unit`, `Tactic` as JSON entities for the strategic planning domain

Only **OpenERA** directly implements the UDM's research administration domain tables, as it is the reference implementation for that specification.

## Relationship to AI4RA-UDM

```
AI4RA-UDM (open source, any institution)
    │
    │  We adopt: conventions, patterns, AllowedValue design
    │  We don't adopt: domain-specific tables
    │
    ▼
UI Insight Institutional Standard (this documentation)
    │
    ├── OpenERA         → implements UDM research admin tables
    ├── UCM Daily Register → follows UDM conventions, own domain tables
    ├── Audit Dashboard    → follows UDM conventions, own domain tables
    └── StratPlan Tactics  → follows UDM conventions, JSON-based
```

## Contributing Back

Our institutional experience applying UDM conventions beyond research administration validates the specification's design. Contributions back to the AI4RA-UDM project may include:

- Formalizing the convention standard as a standalone document (independent of the research admin domain tables)
- Documenting the AllowedValue pattern as a reusable design pattern with examples from multiple domains
- Sharing lessons learned from applying the conventions to communications, audit, and strategic planning
