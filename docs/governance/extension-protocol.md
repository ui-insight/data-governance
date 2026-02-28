# Extension Protocol

This page describes how to add a new domain or application to the UI Insight portfolio. Following this protocol ensures the new application integrates cleanly with shared infrastructure, adopts established conventions, and is visible in this governance registry.

## Step-by-Step Process

### 1. Start from TEMPLATE-app

Clone the scaffold repository to get a consistent project structure with pre-configured tooling:

```bash
gh repo create ui-insight/NewApp --template ui-insight/TEMPLATE-app --private
```

The template provides:

- FastAPI backend with async SQLAlchemy 2.0 boilerplate
- React + TypeScript + Tailwind CSS + Vite frontend
- Docker Compose stack (frontend, backend, db)
- MkDocs Material documentation scaffold
- Pre-configured linting (ruff, eslint)
- GitHub Actions CI workflow
- `.env.example` with standard environment variables

### 2. Adopt naming conventions

All column and table names must follow the portfolio's naming conventions, documented in [Naming Conventions](../standard/naming-conventions.md):

- **Columns:** `PascalCase_With_Underscores` (e.g., `Created_At`, `Organization_Name`)
- **Primary keys:** `{TableName}_ID` as `String(50)` with UUID default
- **Foreign keys:** Named by role, not generically (e.g., `Lead_Organization_ID`)
- **Booleans:** `Is_` prefix (e.g., `Is_Active`)
- **Pydantic schemas:** `{Entity}Create`, `{Entity}Update`, `{Entity}Response`, `{Entity}DetailResponse`

### 3. Implement the AllowedValue table

Use the OpenERA/AuditDashboard column naming for consistency with the majority of the portfolio:

```python
import sqlalchemy as sa

class AllowedValue(Base):
    __tablename__ = "AllowedValues"

    Allowed_Value_ID          = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    Allowed_Value_Group       = sa.Column(sa.String(50), nullable=False, index=True)
    Allowed_Value_Code        = sa.Column(sa.String(50), nullable=False)
    Allowed_Value_Label       = sa.Column(sa.String(255), nullable=False)
    Allowed_Value_Description = sa.Column(sa.Text, nullable=True)

    __table_args__ = (
        sa.UniqueConstraint("Allowed_Value_Group", "Allowed_Value_Code"),
    )
```

!!! tip "Code casing"
    Use **`snake_case`** for all `Allowed_Value_Code` values in new applications. See [Shared Patterns](../vocabulary/shared-patterns.md) for rationale.

### 4. Define domain tables

Create SQLAlchemy models in `backend/app/models/`. Every model module must include:

- A multi-paragraph docstring explaining the entity's domain context, relationships, and design decisions
- The `sa.` prefix for all SQLAlchemy usage (`import sqlalchemy as sa`)
- `lazy="selectin"` on all relationships for async compatibility
- UUID primary keys as `String(50)` with the `{TableName}_ID` naming pattern

```python
"""
A Report represents a completed audit engagement document.

Reports are the top-level entity in the audit hierarchy. Each report contains
one or more observations (findings), and each observation may have associated
action items for corrective measures.

Reports are immutable once finalized -- status transitions are tracked via
StatusUpdate records rather than in-place edits to the Report row.
"""

import sqlalchemy as sa
import uuid

class Report(Base):
    __tablename__ = "Report"

    Report_ID = sa.Column(sa.String(50), primary_key=True,
                          default=lambda: str(uuid.uuid4()))
    Report_Title = sa.Column(sa.String(255), nullable=False)
    Report_Type = sa.Column(sa.String(50), nullable=False)  # AllowedValue: ReportType
    Current_Status = sa.Column(sa.String(50), nullable=False)  # AllowedValue: ReportStatus
    Created_At = sa.Column(sa.DateTime, server_default=sa.func.now())
```

### 5. Create seed data

Place JSON seed files in `backend/data/` for AllowedValues and any reference data that should ship with the application:

```json
[
  {
    "Allowed_Value_Group": "ReportType",
    "Allowed_Value_Code": "annual",
    "Allowed_Value_Label": "Annual Report",
    "Allowed_Value_Description": "Regularly scheduled annual audit report"
  },
  {
    "Allowed_Value_Group": "ReportType",
    "Allowed_Value_Code": "special",
    "Allowed_Value_Label": "Special Report",
    "Allowed_Value_Description": "Ad-hoc audit report outside the annual schedule"
  }
]
```

Seeding must be idempotent -- use the `(Allowed_Value_Group, Allowed_Value_Code)` unique constraint to skip existing records.

### 6. Register in this governance repository

Add the following artifacts to the `data-governance` repository:

1. **Catalog JSON** in `catalog/` -- Schema metadata for all tables in the new application
2. **Vocabulary JSON** in `vocabulary/` -- All AllowedValue groups and codes
3. **Domain documentation page** in `docs/domains/` -- Domain context, data model overview, and relationship to other domains
4. Update the [Application Portfolio](../portfolio/applications.md) summary table
5. Update the [Vocabulary Registry](../vocabulary/index.md) landscape summary
6. Update the [Vocabularies by Domain](../vocabulary/by-domain.md) with the new application's value groups

### 7. Assign port allocation

Request a prod/dev port pair from the deployment administrator. Ports are allocated in increments of 20, with dev ports offset by 10:

| Slot | Prod | Dev |
|---|---|---|
| Next available | 9320 | 9330 |
| Following | 9340 | 9350 |

Update the [Architecture](../portfolio/architecture.md) port allocation table after assignment.

### 8. Deploy

Deploy using Docker Compose on the shared server following the standard container pattern:

```bash
# SSH to the deployment server
ssh devops@openera.insight.uidaho.edu

# Clone and deploy
git clone https://github.com/ui-insight/NewApp.git
cd NewApp

HOST_PORT=9320 POSTGRES_PASSWORD=<secure> \
  docker compose up -d --build
```

Coordinate with the network administrator to set up the DNS record (e.g., `newapp.insight.uidaho.edu`) pointing to the deployment server on the assigned port.

---

## Adding AllowedValue Groups

To propose a new AllowedValue group for an existing application:

1. **Check the vocabulary registry** -- Verify the concept is not already covered by an existing group in any application. See [Shared Patterns](../vocabulary/shared-patterns.md).
2. **Define the group** -- Choose a group name, code values, labels, and descriptions. Use `snake_case` for codes.
3. **Add seed data** -- Add the new group to the application's `backend/data/allowed_values.json` file.
4. **Update the governance registry** -- Add the new group to the vocabulary JSON and update [Vocabularies by Domain](../vocabulary/by-domain.md).
5. **Document cross-domain implications** -- If the new group overlaps with existing groups in other applications, update [Shared Patterns](../vocabulary/shared-patterns.md).

## Adding Values to Existing Groups

To add a new code value to an existing AllowedValue group:

1. **Check for conflicts** -- Ensure the new code does not duplicate an existing code in the same group.
2. **Follow casing conventions** -- Use the same casing as existing codes in the group.
3. **Add to seed data** -- Append the new value to the seed JSON file.
4. **Update the governance registry** -- Update the vocabulary JSON and the [Vocabularies by Domain](../vocabulary/by-domain.md) listing.

!!! note "Runtime additions"
    Applications also support adding AllowedValues at runtime via the `/api/v1/allowed-values` endpoint. Runtime additions should be reflected back into the seed data and governance registry to keep the documentation current.
