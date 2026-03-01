# Architecture

All applications in the UI Insight portfolio share a single deployment server and a common container architecture. This page documents the shared infrastructure, networking, and port allocation scheme.

## Deployment Server

All applications are deployed to a single server managed by the UI Insight team:

| Property | Value |
|---|---|
| Host | `devops@openera.insight.uidaho.edu` |
| Network | University of Idaho campus network |
| Container runtime | Docker + Docker Compose |
| Subnet | Custom `10.x.x.x` address space |

!!! warning "Custom subnet"
    All Docker Compose stacks use a `10.x.x.x` address space rather than Docker's default `172.x.x.x` range. This avoids IP address conflicts on the shared deployment server where multiple Compose stacks run simultaneously.

## Shared Database Infrastructure

Database-backed applications connect to a shared PostgreSQL 16 instance managed by the [insight-db](https://github.com/ui-insight/insight-db) repository. This single container provides isolated databases and credentials for each application, eliminating per-app database containers.

```
frontend (nginx)  <-- only container with host port mapping
    | proxies /api/
    v
backend (uvicorn) <-- internal only, port 8001
    |
    v  (insight-db-net Docker network)
insight-db (postgres:16)  <-- shared container, port 5432
```

- **frontend** -- Serves the production React build via nginx. Proxies all `/api/` requests to the backend container. This is the only container with a port mapped to the host.
- **backend** -- Runs the FastAPI application via uvicorn on port 8001. Accessible only within the Docker network. Connects to the shared database via the `insight-db-net` external network when DB mode is enabled.
- **insight-db** -- Shared PostgreSQL 16 instance on the `insight-db-net` Docker network (subnet 10.20.0.0/24). Each database-backed app has its own database and credentials. Managed via the [insight-db](https://github.com/ui-insight/insight-db) repository.

| Database | User | Application |
|---|---|---|
| `openera` / `openera_dev` | `openera` | OpenERA |
| `ucm_newsletter` / `ucm_newsletter_dev` | `ucm` | UCM Daily Register |
| `audit_dashboard` / `audit_dashboard_dev` | `audit_user` | Audit Dashboard |
| `stratplan` / `stratplan_dev` | `stratplan` | StratPlan Tactics (optional `insight_db` mode) |

!!! note "StratPlan runtime modes"
    StratPlan defaults to JSON-backed runtime and can run without a database. When `DATA_SOURCE=insight_db` is enabled, its backend joins `insight-db-net` and reads from a projected canonical schema.

## Port Allocations

Each application is assigned a dedicated prod/dev port pair on the host. Ports are allocated in increments of 20, with dev ports offset by 10 from their prod counterpart.

| Application | Prod Port | Dev Port | URL |
|---|---|---|---|
| OpenERA | 9200 | 9210 | openera.insight.uidaho.edu |
| StratPlan Tactics | 9220 | 9230 | stratplan.insight.uidaho.edu |
| ProcessMapping | 9240 | 9250 | processmap.insight.uidaho.edu |
| AISPEG | 9260 | 9270 | aispeg.insight.uidaho.edu |
| UCM Daily Register | 9280 | 9290 | ucmnews.insight.uidaho.edu |
| Audit Dashboard | 9300 | -- | audit.insight.uidaho.edu |

!!! tip "Requesting a new port"
    New applications should request the next available port pair from the deployment administrator. The next available prod port is **9320** (dev: 9330). See the [Extension Protocol](../governance/extension-protocol.md) for the full onboarding process.

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
            db[(postgres :5432\nopenera | ucm_newsletter | audit_dashboard | stratplan optional)]
        end

        subgraph openera["OpenERA :9200/:9210"]
            oe_fe[nginx] --> oe_be[uvicorn :8001]
        end

        subgraph stratplan["StratPlan Tactics :9220/:9230"]
            sp_fe[nginx] --> sp_be[uvicorn :8001]
        end

        subgraph processmap["ProcessMapping :9240/:9250"]
            pm_fe[nginx] --> pm_be[uvicorn :8001]
        end

        subgraph aispeg["AISPEG :9260/:9270"]
            as_fe[nginx] --> as_be[uvicorn :8001]
        end

        subgraph ucm["UCM Daily Register :9280/:9290"]
            ucm_fe[nginx] --> ucm_be[uvicorn :8001]
        end

        subgraph audit["Audit Dashboard :9300"]
            ad_fe[nginx] --> ad_be[uvicorn :8001]
        end
    end

    mindrouter[MindRouter\nmindrouter.uidaho.edu]
    claude[Claude API\ncloud]
    openai[OpenAI API\ncloud]

    oe_be --> db
    ucm_be --> db
    ad_be --> db
    pm_be --> db
    as_be --> db
    sp_be -. optional DATA_SOURCE=insight_db .-> db

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
HOST_PORT=9220 DATA_SOURCE=json docker compose up -d --build

# StratPlan optional DB mode
HOST_PORT=9220 DATA_SOURCE=insight_db INSIGHT_DB_HOST=insight-db \
INSIGHT_DB_PORT=5432 INSIGHT_DB_NAME=stratplan INSIGHT_DB_USER=stratplan \
INSIGHT_DB_PASSWORD=<password> docker compose up -d --build
```

The `HOST_PORT` variable controls which host port the frontend nginx container binds to. DB-mode applications connect to the shared `insight-db` container via the `insight-db-net` external Docker network.

## Environment Variables

Each application requires a subset of the following environment variables:

| Variable | Required By | Purpose |
|---|---|---|
| `HOST_PORT` | All | Host port for the frontend nginx container |
| `DATA_SOURCE` | StratPlan | Select runtime source (`json` or `insight_db`) |
| `INSIGHT_DB_*` / `INSIGHT_DB_DSN` | StratPlan (`insight_db` mode) | Shared Postgres connection settings |
| `POSTGRES_PASSWORD` | insight-db host | PostgreSQL superuser password |
| `DATABASE_URL` | DB-backed backends using URL pattern | Full database connection string |
| `LLM_PROVIDER` | AI-integrated apps | Active LLM provider (`claude`, `openai`, `mindrouter`) |
| `ANTHROPIC_API_KEY` | Claude users | Anthropic API key |
| `OPENAI_API_KEY` | OpenAI users | OpenAI API key |
| `MINDROUTER_URL` | MindRouter users | MindRouter endpoint URL |
| `SECRET_KEY` | Auth-enabled apps | JWT signing secret |
