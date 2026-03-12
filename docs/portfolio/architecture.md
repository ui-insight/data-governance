# Architecture

This page documents the shared infrastructure patterns used by the currently onboarded governance applications. The broader UI Insight portfolio now includes additional repositories with differing runtime models, so this page should not be treated as the authoritative source for every repo's live deployment settings.

## Deployment Server

All currently onboarded governance applications are deployed to a single server managed by the UI Insight team:

| Property | Value |
|---|---|
| Host | `devops@openera.insight.uidaho.edu` |
| Network | University of Idaho campus network |
| Container runtime | Docker + Docker Compose |
| Subnet | Custom `10.x.x.x` address space |

!!! warning "Custom subnet"
    All Docker Compose stacks use a `10.x.x.x` address space rather than Docker's default `172.x.x.x` range. This avoids IP address conflicts on the shared deployment server where multiple Compose stacks run simultaneously.

## Shared Database Infrastructure

Database-backed governance applications connect to a shared PostgreSQL 16 instance managed by the [insight-db](https://github.com/ui-insight/insight-db) repository. This single container provides isolated databases and credentials for each application, eliminating per-app database containers.

```
frontend (nginx)  <-- only app container with host port mapping
    | proxies /api/
    v
backend (uvicorn) <-- internal only, app-specific port (commonly 8000/8001)
    |
    v  (insight-db-net Docker network)
insight-db (postgres:16)  <-- shared container, port 5432
```

- **frontend** -- Serves the production UI build via nginx when present. Proxies `/api/` requests to the backend container. This is typically the only app container with a host port mapping.
- **backend** -- Runs the application API via uvicorn on an internal app-specific port. Accessible only within the Docker network. Connects to the shared database via the `insight-db-net` external network when DB mode is enabled.
- **insight-db** -- Shared PostgreSQL 16 instance on the `insight-db-net` Docker network (subnet 10.20.0.0/24). Each database-backed app has its own database and credentials. Managed via the [insight-db](https://github.com/ui-insight/insight-db) repository.

| Database | User | Application |
|---|---|---|
| `openera` / `openera_dev` | `openera` | OpenERA |
| `ucm_newsletter` / `ucm_newsletter_dev` | `ucm` | UCM Daily Register |
| `audit_dashboard` / `audit_dashboard_dev` | `audit_user` | Audit Dashboard |
| `stratplan` / `stratplan_dev` | `stratplan` | StratPlan Tactics (optional `insight_db` mode) |
| `processmapping` / `processmapping_dev` | `processmapping` | ProcessMapping |

!!! note "StratPlan runtime modes"
    StratPlan defaults to JSON-backed runtime and can run without a database. When `DATA_SOURCE=insight_db` is enabled, its backend joins `insight-db-net` and reads from a projected canonical schema.

## Deployment Port Notes

This repository no longer maintains a fully reliable global port registry for every UI Insight repository. Use the application repo's deployment configuration as the source of truth, then reflect confirmed values back here during governance updates.

| Application | Current Documented Host Binding | Source in App Repo |
|---|---|---|
| OpenERA | 9200 frontend host mapping | `docker-compose.yml` |
| UCM Daily Register | `${HOST_PORT:-9280}` frontend host mapping | `docker-compose.yml` |
| Audit Dashboard | 9380 prod / 9390 dev frontend host mappings | `docker-compose.yml` |
| StratPlan Tactics | Local compose defaults to 9200 frontend / 8000 backend | `docker-compose.yml` |
| ProcessMapping | `${HOST_PORT:-9240}` frontend host mapping | `docker-compose.deploy.yml` |

!!! tip "Requesting a new port"
    Confirm host-port assignments with the deployment administrator before deploying a new application. After assignment, update this page and the relevant domain page with the verified value rather than assuming the next sequential slot.

## AI Services

Applications that integrate AI capabilities connect to one or more LLM providers through an abstract provider interface:

| Provider | Endpoint | Use Cases | Applications |
|---|---|---|---|
| MindRouter | `mindrouter.uidaho.edu` | On-prem LLM inference, OCR | UCM Daily Register, Audit Dashboard |
| Claude (Anthropic) | Cloud API | Text editing, structured extraction | UCM Daily Register, OpenERA |
| OpenAI | Cloud API | Text editing, embeddings | UCM Daily Register, OpenERA |

The active provider is selected at startup via the `LLM_PROVIDER` environment variable. All providers implement the same `LLMProvider` abstract base class, so switching providers requires no code changes.

MindRouter is the University of Idaho's on-premises AI gateway, providing LLM inference and OCR capabilities without sending data to external cloud services. It is the preferred provider for workloads involving sensitive institutional data.

## Architecture Diagram

```mermaid
graph TB
    subgraph "openera.insight.uidaho.edu"
        direction TB

        subgraph insightdb["insight-db (shared PostgreSQL 16)"]
            db[(postgres :5432\nopenera | ucm_newsletter | audit_dashboard | stratplan optional | processmapping optional)]
        end

        subgraph openera["OpenERA"]
            oe_fe[nginx] --> oe_be[uvicorn]
        end

        subgraph stratplan["StratPlan Tactics"]
            sp_fe[nginx] --> sp_be[uvicorn]
        end

        subgraph ucm["UCM Daily Register"]
            ucm_fe[nginx] --> ucm_be[uvicorn]
        end

        subgraph audit["Audit Dashboard"]
            ad_fe[nginx] --> ad_be[uvicorn]
        end

        subgraph processmap["ProcessMapping"]
            pm_fe[nginx] --> pm_be[uvicorn]
        end
    end

    mindrouter[MindRouter\nmindrouter.uidaho.edu]
    claude[Claude API\ncloud]
    openai[OpenAI API\ncloud]

    oe_be --> db
    ucm_be --> db
    ad_be --> db
    sp_be -. optional DATA_SOURCE=insight_db .-> db
    pm_be -. optional DATA_SOURCE=insight_db .-> db

    ucm_be -.-> mindrouter
    ucm_be -.-> claude
    ucm_be -.-> openai
    ad_be -.-> mindrouter
    oe_be -.-> claude
    oe_be -.-> openai
```

## Deploy Command Pattern

The shared database must be running before any DB-backed application starts:

```bash
# Start the shared database (once)
cd insight-db && docker compose up -d

# Example DB-backed deploy
HOST_PORT=<PORT> DATABASE_URL=<url> ANTHROPIC_API_KEY=<key> \
  docker compose up -d --build

# StratPlan JSON mode (default)
HOST_PORT=<assigned_or_local_port> DATA_SOURCE=json docker compose up -d --build

# StratPlan optional DB mode
HOST_PORT=<assigned_or_local_port> DATA_SOURCE=insight_db INSIGHT_DB_HOST=insight-db \
INSIGHT_DB_PORT=5432 INSIGHT_DB_NAME=stratplan INSIGHT_DB_USER=stratplan \
INSIGHT_DB_PASSWORD=<password> docker compose up -d --build
```

The `HOST_PORT` variable controls which host port the frontend nginx container binds to when the application's deployment config exposes that setting. DB-mode applications connect to the shared `insight-db` container via the `insight-db-net` external Docker network.

## Environment Variables

Each application requires a subset of the following environment variables:

| Variable | Required By | Purpose |
|---|---|---|
| `HOST_PORT` | Apps that externalize frontend host binding | Host port for the frontend nginx container |
| `DATA_SOURCE` | StratPlan, ProcessMapping | Select runtime source (`json` or `insight_db`) |
| `INSIGHT_DB_*` / `INSIGHT_DB_DSN` | StratPlan or ProcessMapping (`insight_db` mode) | Shared Postgres connection settings |
| `POSTGRES_PASSWORD` | insight-db host | PostgreSQL superuser password |
| `DATABASE_URL` | DB-backed backends using URL pattern | Full database connection string |
| `LLM_PROVIDER` | AI-integrated apps | Active LLM provider (`claude`, `openai`, `mindrouter`) |
| `ANTHROPIC_API_KEY` | Claude users | Anthropic API key |
| `OPENAI_API_KEY` | OpenAI users | OpenAI API key |
| `MINDROUTER_URL` | MindRouter users | MindRouter endpoint URL |
| `SECRET_KEY` | Auth-enabled apps | JWT signing secret |
