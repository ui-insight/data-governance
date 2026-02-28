# Design Patterns

These patterns are adopted from the AI4RA-UDM reference implementation (OpenERA) and applied consistently across all database-backed applications in the portfolio.

## Architecture

### Three-Tier Stack

All applications share the same technology stack:

| Layer | Technology | Notes |
|---|---|---|
| Frontend | React + TypeScript + Tailwind CSS + Vite | Exception: StratPlanTacticsMB uses JSX + custom CSS |
| Backend | FastAPI + async SQLAlchemy 2.0 + Pydantic v2 | Python 3.11+ |
| Database | SQLite (dev) / PostgreSQL 16 (prod) | Switchable via `DATABASE_URL` |
| Docs | MkDocs Material | GitHub Pages |

### Service Layer Separation

API route handlers are thin -- they validate input, delegate to service functions, and return responses. Business logic lives in `app/services/`:

```
backend/app/
  api/v1/          # Route handlers (thin)
  services/        # Business logic
  models/          # SQLAlchemy ORM models
  schemas/         # Pydantic request/response schemas
```

### Async-First ORM

All database operations use `async def` with SQLAlchemy's async session. All relationships use `lazy="selectin"` to avoid N+1 query problems in async contexts:

```python
class Newsletter(Base):
    Items = sa.orm.relationship(
        "NewsletterItem",
        back_populates="Newsletter_Rel",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
```

## Primary Keys

All models use UUID primary keys stored as `String(36)`:

```python
Id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
```

!!! note "Variation"
    OpenERA and AuditDashboard use `String(50)` for primary keys with a `TableName_ID` naming pattern (e.g., `Organization_ID`). UCM Daily Register uses `String(36)` with a simple `Id` name. The `TableName_ID` pattern is preferred for new applications as it is self-documenting in joins.

## Model Documentation

Every model module includes a multi-paragraph docstring explaining:

1. What the entity represents in the domain
2. How it relates to other entities
3. Key design decisions (e.g., why records are immutable, why a polymorphic pattern is used)

```python
"""
An EditVersion captures an immutable snapshot of a submission's headline and body
at one stage of the editing pipeline.

The editing pipeline progresses through three stages: original (as submitted),
ai_suggested (the LLM's recommended edits), and editor_final (the human editor's
accepted version). Each stage creates a new EditVersion row rather than updating
the previous one, preserving a complete audit trail.

The Flags column stores a JSON object of pre-analysis results (first-person detected,
exclamation marks found, etc.) that informed the AI editing pass. Changes_Made stores
the structured diff between this version and its predecessor.
"""
```

## Controlled Vocabularies

All categorical values are stored in the `AllowedValue` table rather than as Python enums. See [AllowedValue Pattern](allowed-values.md) for details.

## Immutable Audit Records

For entities that track change history (e.g., `EditVersion` in UCM Daily Register, `StatusUpdate` in AuditDashboard, `ActivityLog` in both), records are **never updated** after creation. Each new state creates a new row, preserving a complete audit trail.

## AI Provider Abstraction

Applications that integrate AI services use an abstract provider pattern:

```python
class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, system_prompt: str, user_prompt: str, ...) -> LLMResponse:
        ...
```

Concrete implementations are selected at startup via environment variable (`LLM_PROVIDER`), supporting Claude, OpenAI, and MindRouter (University of Idaho on-prem). This decouples the application from any single vendor.

## Docker Deployment

All applications deploy as a three-container Docker Compose stack:

```
frontend (nginx)  ←── only container with host port mapping
    ↓ proxies /api/
backend (uvicorn) ←── internal only, port 8001
    ↓
db (postgres:16)  ←── internal only, port 5432
```

All containers use a `10.x.x.x` address space (custom subnet) rather than Docker's default `172.x.x.x` to avoid conflicts on the shared deployment server.

## Seed Data

Reference data is stored as JSON files in `backend/data/` and loaded idempotently at application startup. This includes AllowedValues, section definitions, style rules, and other configuration that should ship with the application but remain editable post-deployment.
