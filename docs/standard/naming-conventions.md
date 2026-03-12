# Naming Conventions

All database-backed applications in the UI Insight portfolio adopt the column and table naming conventions defined by the [AI4RA Unified Data Model](https://github.com/ui-insight/AI4RA-UDM). These conventions ensure consistency across domains and make cross-application data analysis predictable.

## Column Naming: `PascalCase_With_Underscores`

Every column name uses PascalCase words separated by underscores.

```
Created_At          (not created_at or createdAt)
Submission_Id       (not submission_id or submissionId)
Is_Active           (not is_active or isActive)
Organization_Name   (not organization_name or organizationName)
```

### Standard Suffixes

| Suffix | Meaning | Examples |
|---|---|---|
| `_ID` | Primary or foreign key identifier | `Personnel_ID`, `Award_ID`, `Submission_Id` |
| `_Date` | Date value | `Report_Date`, `Publish_Date`, `Created_At` |
| `_Status` | Lifecycle state (AllowedValue reference) | `Current_Status`, `Review_Status` |
| `_Type` | Category discriminator (AllowedValue reference) | `Report_Type`, `Newsletter_Type`, `Document_Type` |
| `_Name` | Human-readable name | `Organization_Name`, `Full_Name` |
| `_Code` | Machine-readable code | `Allowed_Value_Code`, `Priority_Code` |
| `_Amount` | Monetary value | `Total_Award`, `Budget_Amount` |
| `_Number` | Sequence or reference number | `Award_Number`, `Observation_Number` |
| `_Description` | Free-text explanation | `Allowed_Value_Description`, `Description` |
| `Is_` | Boolean flag (prefix) | `Is_Active`, `Is_Daily` |

### Foreign Key Naming

Foreign keys are named by **role**, not generically. When a table has multiple references to the same target, each FK describes its semantic role:

```python
# Good: role-based naming
Sponsor_Organization_ID   = sa.Column(sa.ForeignKey("Organization.Organization_ID"))
Lead_Organization_ID      = sa.Column(sa.ForeignKey("Organization.Organization_ID"))

# Avoid: generic naming
Organization_ID_1         = ...
Organization_ID_2         = ...
```

## Table Naming

| Context | Convention | Example |
|---|---|---|
| SQLAlchemy `__tablename__` | `PascalCase` (singular or plural depending on app) | `Organization`, `submissions`, `AllowedValues` |
| Model class name | `PascalCase` (singular) | `Organization`, `Submission`, `AllowedValue` |

!!! note "Table name variation"
    The AI4RA-UDM spec uses singular `PascalCase` table names (e.g., `Organization`). Some applications use plural lowercase (e.g., `submissions`). The column naming convention is the more important consistency point across applications.

## Schema Naming (Pydantic)

All Pydantic request/response schemas follow a consistent naming pattern:

| Pattern | Purpose | Example |
|---|---|---|
| `{Entity}Create` | Request body for creation | `SubmissionCreate`, `ProposalCreate` |
| `{Entity}Update` | Request body for partial update | `SubmissionUpdate`, `ProposalUpdate` |
| `{Entity}Response` | Standard response | `SubmissionResponse`, `ProposalResponse` |
| `{Entity}DetailResponse` | Response with nested relationships | `SubmissionDetailResponse` |
| `{Entity}ListResponse` | Paginated list response | `SubmissionListResponse` |

Schema field names match ORM column names exactly (`PascalCase_With_Underscores`), ensuring frontend TypeScript interfaces can mirror them without translation.

## TypeScript Conventions

Frontend TypeScript interfaces mirror Pydantic schemas:

```typescript
// Matches SubmissionResponse schema exactly
interface SubmissionResponse {
  Id: string;
  Category: string;
  Target_Newsletter: string;
  Original_Headline: string;
  Status: string;
  Created_At: string;
}
```

## Python Import Convention

All SQLAlchemy usage follows a single import style:

```python
import sqlalchemy as sa

# Always use sa. prefix
class Submission(Base):
    __tablename__ = "submissions"
    Id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    Category = sa.Column(sa.String(50), nullable=False)
```

This convention is adopted from the AI4RA-UDM reference implementation and maintained across the currently onboarded governance applications for readability and consistency.
