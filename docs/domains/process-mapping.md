# Process Intelligence (ProcessMapping)

ProcessMapping is a process intelligence application and canonical data repository for University of Idaho research-administration operations. It combines governed process maps, transcript-derived metadata, and Vandalizer-compatible workflow definitions in a single repository so teams can document operational reality, identify automation candidates, and project curated process records into `insight_db` when relational access is needed.

The canonical source remains JSON-first. The application can run directly from repository data assets or project approved process maps into a single operational table for shared infrastructure use.

## Key Statistics

| Attribute | Value |
|---|---|
| **Domain** | Process intelligence for research administration operations |
| **Repository** | [github.com/ui-insight/ProcessMapping](https://github.com/ui-insight/ProcessMapping) |
| **Canonical Process Maps** | 24 |
| **Workflow Definitions** | 15 |
| **Extraction Task Prompt Files** | 65 |
| **Controlled Value Groups** | 10 (78 codes) |
| **Runtime Modes** | `json` (canonical), `insight_db` (optional projection) |
| **Auth Model** | None |
| **AI Integration** | None direct; stores workflow specifications for external extraction systems |
| **Prod URL** | `processmapping.insight.uidaho.edu` (port 9240) |
| **Dev URL** | `processmapping-dev.insight.uidaho.edu` (port 9250) |

## Canonical Data Assets

The source-of-truth assets live directly in repository-managed JSON and transcript files:

| Asset | Location | Purpose |
|---|---|---|
| Process maps | `processes/*/process.json` | Canonical structured process definitions |
| Process metadata | `processes/*/metadata.json` | Lineage, parse notes, and asset-level metadata |
| Workflow definitions | `workflows/*/workflow.json` | Vandalizer-compatible extraction workflow specifications |
| Extraction prompts | `workflows/*/extraction-tasks/*.md` | Task-level prompt assets referenced by workflows |
| Controlled values | `data/allowed_values.json` | Governed coded values for process categories, steps, roles, systems, and transcript-governance metadata |
| Raw transcripts | `transcripts/raw/` | Source inputs with the highest sensitivity and strongest lineage requirements |

## Canonical Logical Model

| Entity | Count | Description |
|---|---|---|
| `ProcessMap` | 24 | Top-level process definitions with identifiers, descriptions, category, actors, systems, steps, and lineage fields |
| `Actor` | variable | Nested people, roles, systems, or external entities participating in a process |
| `System` | variable | Systems referenced within a process map |
| `Step` | variable | Ordered process steps with automation notes, pain points, inputs, outputs, and next-step references |
| `DecisionOption` | variable | Branching outcomes attached to decision-type steps |
| `WorkflowDefinition` | 15 | Vandalizer-compatible extraction workflows derived from operational process knowledge |
| `WorkflowStep` | variable | Ordered workflow stages such as extraction, consolidation, and formatting |
| `WorkflowTask` | variable | Task-level units within a workflow step, including prompt references and search guidance |
| `ExtractionField` | variable | Structured extraction targets expected from a workflow task |

## API Surface

The backend exposes three primary API surfaces under `/api/v1`:

- `GET /processes` and `GET /processes/{slug}` for canonical process maps
- `POST /processes/ingest/transcript` for transcript-to-process skeleton generation
- `GET /workflows` and `GET /workflows/{slug}` for workflow definitions

The `/api/v1/health` endpoint reports the active runtime mode and includes `insight_db` connectivity details when DB-backed mode is enabled.

## Optional Relational Projection (`insight_db` mode)

When DB-backed runtime is enabled, canonical process maps are projected into a single relational table:

| Table | Purpose |
|---|---|
| `process_maps` | Stores process-map summary fields plus the full canonical JSON payload and optional metadata for operational reads |

The projection is intentionally thin. The canonical JSON remains the source of truth, while the projected table supports shared infrastructure access and repository-backed operational browsing.

## Controlled Values

ProcessMapping does not currently expose a runtime `AllowedValue` table. Instead, it keeps governed coded values in `data/allowed_values.json`.

| Group | Codes |
|---|---|
| `ProcessCategory` | `PRE_AWARD`, `POST_AWARD`, `COMPLIANCE`, `FINANCIAL`, `SUBAWARD`, `REPORTING`, `CONTRACTING` |
| `StepType` | `ACTION`, `DECISION`, `REVIEW`, `APPROVAL`, `DATA_ENTRY`, `COMMUNICATION`, `WAIT`, `SUBPROCESS` |
| `ActorType` | `PERSON`, `ROLE`, `SYSTEM`, `EXTERNAL` |
| `ActorRole` | `GRANTS_SPECIALIST`, `GRANTS_OFFICER`, `PI`, `DEPT_ADMIN`, `FISCAL_OFFICER`, `COMPLIANCE_OFFICER`, `SPONSOR`, `POST_AWARD_SPECIALIST`, `FINANCIAL_UNIT_SPECIALIST`, `PRE_AWARD_SPA`, `DGA`, `PRE_AWARD_MANAGER`, `AOR`, `SENIOR_GRANTS_ANALYST`, `SPONSORED_PROGRAMS_OFFICER`, `ASSISTANT_DIRECTOR_SPONSORED_ACCOUNTING` |
| `SystemName` | `BANNER`, `CAYUSE`, `GRANTS_GOV`, `RESEARCH_GOV`, `ERA_COMMONS`, `SAM_GOV`, `EMAIL`, `VANDALIZER`, `VERAS`, `EXCEL`, `TEAMS`, `EXPORT_TO_BANNER_FORM`, `CHROME_RIVER`, `JAGGAER`, `KUALI`, `ARGOS`, `SOFTDOCS` |
| `ActivityType` | `DATA_ENTRY`, `REVIEW_APPROVAL`, `SYSTEM_LOOKUP`, `DOCUMENT_GENERATION`, `COMMUNICATION`, `DECISION_POINT`, `CALCULATION_VALIDATION`, `FILING_ARCHIVAL` |
| `FileType` | `VTT`, `TXT`, `DOCX`, `MD` |
| `RedactionStatus` | `NOT_REDACTED`, `PARTIALLY_REDACTED`, `FULLY_REDACTED` |
| `ProcessingStatus` | `RAW`, `PARSED`, `MAPPED` |

!!! note "Casing exception"
    ProcessMapping currently uses `UPPER_CASE` codes in its governed JSON reference data. This is a documented exception to the preferred `snake_case` convention for new applications.

## Deployment

ProcessMapping deploys as a frontend/backend container pair, with `insight_db` connectivity available when projection mode is enabled:

| Container | Role | Port |
|---|---|---|
| `frontend` (nginx) | Serves React build and proxies `/api/` | Host-mapped (`HOST_PORT`, defaults to 9240 in deploy config) |
| `backend` (uvicorn) | FastAPI application server | 8000 (internal) |
| `insight-db` (shared) | Shared PostgreSQL 16 instance | 5432 (internal, `insight-db-net`) |

## Governance Notes

- Canonical process maps and workflow definitions are validated with JSON Schema before merge.
- `transcripts/raw/` assets are the highest-risk content class and should be minimized or redacted when possible.
- Lineage is preserved from transcript source to process/workflow outputs through repository-managed metadata files.
- The `process_maps` table is a projection, not the canonical store.
