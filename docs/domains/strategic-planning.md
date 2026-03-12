# Strategic Planning (StratPlan Tactics Dashboard)

StratPlan Tactics is a full-stack strategic planning analytics application for the University of Idaho 2025-2030 plan. It supports alignment, execution-health, investment, and time-horizon reporting for institutional tactics.

The canonical dataset is JSON-based, and the backend can run in either:

- `DATA_SOURCE=json` (default canonical mode)
- `DATA_SOURCE=insight_db` (optional PostgreSQL-backed runtime using imported canonical data)

## Key Statistics

| Attribute | Value |
|---|---|
| **Domain** | Strategic planning execution and investment analytics |
| **Repository** | [github.com/ui-insight/StratPlanTacticsMB](https://github.com/ui-insight/StratPlanTacticsMB) |
| **Strategic Plan** | University of Idaho 2025-2030 |
| **Units** | 26 |
| **Tactics** | 453 |
| **Pillars / Priorities** | 5 / 20 |
| **SPIGP Awards** | 3 |
| **Frontend Views** | 12 |
| **Runtime Modes** | `json` (default), `insight_db` (optional) |
| **Auth Model** | None |
| **AI Integration** | None |
| **Prod URL** | Port 9220 |
| **Dev URL** | Port 9230 |

## Canonical Logical Model (JSON)

The source-of-truth model is stored in `backend/app/data/strategic_plan_data.json`.

| Entity | Count | Description |
|---|---|---|
| `Pillar` | 5 | Top-level strategic pillars (`A`..`E`) with embedded priorities |
| `Priority` | 20 | Strategic objectives under each pillar |
| `Unit` | 26 | Academic and administrative units submitting tactics |
| `Tactic` | 453 | Tactical actions with alignment, execution, and investment metadata |
| `PriorityCodeMapping` | variable | Multi-priority linkage with confidence/source metadata |
| `SPIGPAward` | 3 | Strategic Plan Implementation Grant Program awards linked to tactics |

## API Surface

The backend exposes read-only API routes (`/api/v1`, plus legacy `/api` mount) across four groups:

- Core entities: `pillars`, `units`, `tactics`, `spigp-awards`, `metadata`
- Alignment analytics: matrix, confidence, coverage, synergies, redundancies, themes
- Execution/investment analytics: execution-health, investment-portfolio, horizon-summary
- Portfolio rollups: pillar-summary, unit-portfolio, resource-concentration, spigp-portfolio

## Optional Relational Projection (`insight_db` mode)

When DB-backed runtime is enabled, importer workflows project the canonical model into these tables:

| Table | Purpose |
|---|---|
| `pillars` | Pillar definitions |
| `priorities` | Priority definitions |
| `units` | Unit metadata |
| `unit_source_files` | Source-document lineage |
| `tactics` | Core tactic record + execution/investment fields |
| `tactic_priority_codes` | Multi-priority mappings |
| `tactic_metrics` | Tactic metric text rows |
| `spigp_awards` | SPIGP administrative/execution/financial fields |
| `spigp_award_tactics` | SPIGP-to-tactic link table |
| `dataset_metadata` | Snapshot provenance |

This projection is used for integration parity, import validation, and operational DB mode.

## Controlled Vocabularies (Normalized Enums)

StratPlan currently does not use an `AllowedValue` table. Enum domains are defined in application code and normalized in API/service layers.

| Group | Codes |
|---|---|
| `pillar_code` | `A`, `B`, `C`, `D`, `E` |
| `alignment_level` | `explicit_subpillar`, `mixed`, `pillar_only` |
| `priority_code_confidence` | `explicit`, `inferred`, `pillar_only` |
| `execution_status` | `not_started`, `in_progress`, `completed`, `delayed_at_risk` |
| `funding_source` | `spigp`, `base`, `philanthropy`, `external`, `unfunded` |
| `roi_type` | `revenue`, `retention`, `efficiency`, `compliance`, `reputation` |
| `horizon_category` | `quick_wins`, `mid_term`, `long_term`, `ongoing_operations` |
| `spigp_status` | `not_started`, `in_progress`, `completed`, `delayed_at_risk` |

## Deployment

StratPlan runs as a frontend/backend container pair:

| Container | Role | Port |
|---|---|---|
| `frontend` (nginx) | Serves React build and proxies `/api/` | Host-mapped (9220 prod / 9230 dev) |
| `backend` (uvicorn) | FastAPI analytics API (`/api/v1`) | 8000 internal |

Database connectivity is optional and only required for `DATA_SOURCE=insight_db` runtime.

## Governance Notes

- Canonical source remains the JSON dataset.
- Data quality gates are defined in the StratPlan repository and run before import workflows.
- End-user API remains read-only; update workflows are managed through governed data refresh processes.
