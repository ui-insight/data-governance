# Shared Vocabulary Patterns

Four conceptual patterns recur across multiple applications in the portfolio. Recognizing these patterns helps new applications adopt existing conventions and supports future cross-domain reporting.

---

## 1. Severity / Priority Level

Ranked importance scales used to triage items by urgency or impact.

| Application | Value Group | Codes | Casing |
|---|---|---|---|
| UCM Daily Register | Severity | `error`, `warning`, `info` | snake_case |
| Audit Dashboard | Severity | `HIGH`, `MEDIUM`, `LOW` | UPPER_CASE |
| Audit Dashboard | Priority | `HIGH`, `MEDIUM`, `LOW` | UPPER_CASE |

!!! note "Semantic overlap"
    The Audit Dashboard maintains separate Severity and Priority groups with identical code values. Severity measures the impact of a finding; Priority measures how urgently it should be addressed. UCM Daily Register uses Severity only, applied to style-rule violations detected during AI editing.

---

## 2. Lifecycle Status

Ordered workflow progressions that track an entity from creation through completion. Every database-backed application in the portfolio has at least one status group.

### UCM Daily Register

| Value Group | Values | Count |
|---|---|---|
| Submission_Status | `new`, `ai_edited`, `in_review`, `revision_requested`, `approved`, `scheduled`, `published` | 7 |
| Newsletter_Status | `draft`, `assembling`, `ready`, `sent`, `archived` | 5 |

### Audit Dashboard

| Value Group | Values | Count |
|---|---|---|
| ObservationStatus | `DRAFT`, `OPEN`, `RESOLVED`, `CLOSED` | 4 |
| ActionItemStatus | `OPEN`, `IN_PROGRESS`, `COMPLETED`, `OVERDUE`, `CANCELLED` | 5 |
| ExtractionStatus | `PENDING`, `PROCESSING`, `EXTRACTED`, `REVIEWED`, `APPROVED`, `REJECTED`, `FAILED`, `ARCHIVED` | 8 |

### OpenERA

| Value Group | Values | Count |
|---|---|---|
| ProposalStatus | `draft`, `submitted`, `under_review`, `approved`, `rejected`, `active`, `completed`, `closed` | 8 |
| ApprovalStatus | `pending`, `approved`, `rejected`, `conditional` | 4 |

!!! tip "Common progression"
    Despite different code values, all lifecycle groups follow the same structural pattern: an initial state (draft/new/pending), one or more intermediate states (review, processing), and terminal states (approved/completed/closed, rejected/cancelled). New applications should model their status groups with this progression in mind.

---

## 3. Document / Content Type

Classification values that categorize content items within an application.

| Application | Value Group | Codes | Count |
|---|---|---|---|
| UCM Daily Register | Submission_Category | `announcement`, `event`, `deadline`, `achievement`, `grant`, `resource`, `other` | 7 |
| Audit Dashboard | DocumentType | `REPORT`, `WORKPAPER`, `EVIDENCE`, `CORRESPONDENCE` | 4 |
| Audit Dashboard | ReportType | `ANNUAL`, `SPECIAL`, `FOLLOW_UP` | 3 |
| OpenERA | DocumentType | `proposal`, `budget`, `biosketches`, `facilities`, `data_management`, `compliance`, `subaward`, `other` | 8 |

!!! note "Domain specificity"
    Document/content type groups are the most domain-specific vocabulary. Unlike severity or status, there is little opportunity for convergence here -- each application classifies content relevant to its own domain. The shared pattern is the use of an AllowedValue group (rather than a hard-coded enum) to keep these classifications extensible.

---

## 4. Role Assignment

Roles assigned to people within the context of an application.

| Application | Value Group | Codes | Count |
|---|---|---|---|
| Audit Dashboard | AssignmentRole | `LEAD`, `SUPPORT` | 2 |
| OpenERA | ProjectRole | `pi`, `co_pi`, `senior_personnel`, `postdoc`, `graduate_student`, `undergraduate_student`, `technician`, `consultant`, `other_professional`, `administrator` | 10 |

OpenERA has the most granular role vocabulary, reflecting the complexity of research team composition. Audit Dashboard uses a simpler lead/support distinction appropriate for audit engagement staffing.

---

## Casing Conventions

A notable inconsistency across applications is the casing of AllowedValue codes:

| Application | Code Casing | Example |
|---|---|---|
| UCM Daily Register | `snake_case` | `ai_edited`, `in_review` |
| Audit Dashboard | `UPPER_CASE` | `HIGH`, `IN_PROGRESS` |
| OpenERA | `snake_case` | `under_review`, `co_pi` |
| StratPlan Tactics | `snake_case` | `on_track`, `high` |

!!! warning "Recommendation for new applications"
    New applications should adopt **`snake_case`** for AllowedValue codes. This aligns with the majority of existing applications (OpenERA, UCM, StratPlan) and with Python/JSON conventions. The Audit Dashboard's UPPER_CASE convention predates the establishment of this standard and will be considered for migration in a future update.
