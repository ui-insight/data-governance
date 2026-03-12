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
| Submission_Status | `new`, `ai_edited`, `in_review`, `approved`, `scheduled`, `published`, `rejected` | 7 |
| Newsletter_Status | `draft`, `in_progress`, `ready_for_review`, `submitted`, `published` | 5 |

### Audit Dashboard

| Value Group | Values | Count |
|---|---|---|
| ObservationStatus | `OPEN`, `IN_PROGRESS`, `CLOSED`, `CLOSED_FIRST_FOLLOWUP` | 4 |
| ActionItemStatus | `OPEN`, `IN_PROGRESS`, `COMPLETED`, `OVERDUE`, `CLOSED` | 5 |
| ExtractionStatus | `PENDING`, `OCR_IN_PROGRESS`, `OCR_COMPLETE`, `LLM_IN_PROGRESS`, `REVIEW_PENDING`, `APPROVED`, `REJECTED`, `FAILED` | 8 |

### OpenERA

OpenERA tracks lifecycle status through inline column values rather than AllowedValue groups. One lifecycle-related AllowedValue group exists:

| Source | Values | Count |
|---|---|---|
| `ChecklistStatus` (AllowedValue) | `not_started`, `in_progress`, `complete`, `not_applicable` | 4 |
| `Proposal.Internal_Approval_Status` (inline) | `Draft`, `In Review`, `Approved`, `Rejected`, `Returned` | 5 |
| `Proposal.Decision_Status` (inline) | `Pending`, `Awarded`, `Declined`, `Withdrawn` | 4 |
| `ApprovalStep.status` (inline) | `pending`, `approved`, `rejected`, `returned` | 4 |

!!! tip "Common progression"
    Despite different code values, all lifecycle groups follow the same structural pattern: an initial state (draft/new/pending), one or more intermediate states (review, processing), and terminal states (approved/completed/closed, rejected/cancelled). New applications should model their status groups with this progression in mind.

---

## 3. Document / Content Type

Classification values that categorize content items within an application.

| Application | Value Group | Codes | Count |
|---|---|---|---|
| UCM Daily Register | Submission_Category | `faculty_staff`, `student`, `job_opportunity`, `kudos`, `in_memoriam`, `news_release`, `calendar_event` | 7 |
| Audit Dashboard | DocumentType | `SOURCE_PDF`, `EVIDENCE`, `CORRESPONDENCE`, `OTHER` | 4 |
| Audit Dashboard | ReportType | `FULL_REPORT`, `FOLLOW_UP`, `LETTER` | 3 |
| OpenERA | DocumentType | `proposal_narrative`, `budget_justification`, `biosketch`, `current_pending`, `facilities`, `data_mgmt`, `letter_support`, `rfa_document`, `subaward_docs`, `coi_disclosure`, `other` | 11 |

!!! note "Domain specificity"
    Document/content type groups are the most domain-specific vocabulary. Unlike severity or status, there is little opportunity for convergence here -- each application classifies content relevant to its own domain. The shared pattern is the use of an AllowedValue group (rather than a hard-coded enum) to keep these classifications extensible.

---

## 4. Role Assignment

Roles assigned to people within the context of an application.

| Application | Value Group | Codes | Count |
|---|---|---|---|
| Audit Dashboard | AssignmentRole | `IMPLEMENTER`, `REVIEWER` | 2 |
| OpenERA | ProjectRole | `pi`, `co_pi`, `co_i`, `key_person`, `senior_person`, `postdoc`, `grad_student`, `undergrad`, `technician`, `consultant` | 10 |
| ProcessMapping | ActorRole | `GRANTS_SPECIALIST`, `GRANTS_OFFICER`, `PI`, `DEPT_ADMIN`, `FISCAL_OFFICER`, `COMPLIANCE_OFFICER`, `SPONSOR`, `POST_AWARD_SPECIALIST`, `FINANCIAL_UNIT_SPECIALIST`, `PRE_AWARD_SPA`, `DGA`, `PRE_AWARD_MANAGER`, `AOR` | 13 |

OpenERA has the most granular project-team vocabulary, reflecting the complexity of research team composition. Audit Dashboard uses a simple remediation assignment pair. ProcessMapping captures operational roles that recur across research-administration processes and workflow assets.

---

## Casing Conventions

A notable inconsistency across applications is the casing of AllowedValue codes:

| Application | Code Casing | Example |
|---|---|---|
| UCM Daily Register | `snake_case` | `ai_edited`, `in_review` |
| Audit Dashboard | `UPPER_CASE` | `HIGH`, `IN_PROGRESS` |
| OpenERA | `snake_case` | `proposal_narrative`, `co_pi` |
| StratPlan Tactics | `snake_case` | `in_progress`, `quick_wins` |
| ProcessMapping | `UPPER_CASE` | `PRE_AWARD`, `GRANTS_SPECIALIST` |

!!! warning "Casing convention"
    OpenERA, UCM Daily Register, and StratPlan normalized enums use `snake_case` codes. Audit Dashboard and ProcessMapping currently use `UPPER_CASE`. New applications should adopt `snake_case` and document their chosen convention explicitly.
