# AllowedValue Pattern

The AllowedValue pattern is the most transferable design element from the AI4RA-UDM. It replaces hard-coded enums with a database-driven controlled vocabulary table, enabling administrators to extend, rename, or deactivate categorical values without code changes.

## The Problem with Hard-Coded Enums

```python
# Fragile: requires code deployment to change
class SubmissionStatus(str, Enum):
    NEW = "new"
    AI_EDITED = "ai_edited"
    IN_REVIEW = "in_review"
    # Adding a new status requires a code change, test, and deploy
```

## The AllowedValue Solution

A single lookup table stores all categorical values, grouped by purpose:

```python
class AllowedValue(Base):
    __tablename__ = "AllowedValues"

    Allowed_Value_ID    = sa.Column(sa.Integer, primary_key=True)
    Allowed_Value_Group = sa.Column(sa.String(50), nullable=False, index=True)
    Allowed_Value_Code  = sa.Column(sa.String(50), nullable=False)
    Allowed_Value_Label = sa.Column(sa.String(255), nullable=False)
    Allowed_Value_Description = sa.Column(sa.Text, nullable=True)

    __table_args__ = (
        sa.UniqueConstraint("Allowed_Value_Group", "Allowed_Value_Code"),
    )
```

Domain columns reference codes by convention rather than foreign key:

```python
class Observation(Base):
    # References AllowedValue where Group = "Severity"
    Severity = sa.Column(sa.String(50), nullable=True)
    # References AllowedValue where Group = "ObservationStatus"
    Current_Status = sa.Column(sa.String(50), nullable=False)
```

## Schema Variations

The core pattern is consistent across the currently onboarded DB-backed governance applications, with minor variations in column naming:

| Application | Table Name | PK Column | Group Column | Code Column |
|---|---|---|---|---|
| OpenERA | `AllowedValues` | `Allowed_Value_ID` (Integer) | `Allowed_Value_Group` | `Allowed_Value_Code` |
| AuditDashboard | `AllowedValues` | `Allowed_Value_ID` (Integer) | `Allowed_Value_Group` | `Allowed_Value_Code` |
| UCM Daily Register | `allowed_values` | `Id` (UUID String) | `Value_Group` | `Code` |

!!! info "Convergence opportunity"
    The UCM Daily Register uses a slightly simplified column naming scheme. Future applications should follow the OpenERA/AuditDashboard naming for consistency, as it more closely matches the AI4RA-UDM specification.

## Seed Data

AllowedValues are populated via JSON seed files loaded at application startup. Each application maintains its own seed data appropriate to its domain:

```json
[
  {
    "Value_Group": "Severity",
    "Code": "error",
    "Label": "Error",
    "Display_Order": 1,
    "Description": "Must be fixed before publication"
  }
]
```

Seeding is idempotent -- existing records are skipped based on the `(Group, Code)` unique constraint.

## API Access

Applications that implement the pattern expose an `/api/v1/allowed-values` endpoint that returns active values grouped by value group. Frontend components use this to populate dropdowns and filter options dynamically.

## When to Use AllowedValues

**Use AllowedValues for:**

- Status fields with a defined lifecycle (e.g., `new` -> `in_review` -> `approved`)
- Category and type discriminators (e.g., report types, document types)
- Severity and priority levels
- Role assignments
- Any categorical value that an administrator might need to extend

**Use CHECK constraints for:**

- Universal standards that will never change (e.g., GAAP account types, ISO country codes)
- Boolean flags (`Is_Active`, `Has_Image`)
- Values tightly coupled to application logic (where adding a new value requires code changes regardless)

## Cross-Application Value Groups

Several value groups express the same concept across multiple applications. See the [Shared Patterns](../vocabulary/shared-patterns.md) page for a cross-reference of these overlapping vocabularies.
