# UI Insight Data Governance

Institutional data governance documentation for the University of Idaho's UI Insight application portfolio. Defines the adopted data modeling standard, catalogs domain-specific data models for the currently onboarded governance applications, and provides a unified vocabulary registry.

## Adopted Standard

All database-backed applications adopt conventions from the [AI4RA Unified Data Model](https://github.com/ui-insight/AI4RA-UDM), an open-source data modeling specification for research administration. While the UDM's domain scope is research administration, its naming conventions, design patterns, and controlled vocabulary approach serve as the institutional standard across all domains.

## Application Portfolio

| Application | Domain | Tables | Status |
|---|---|---|---|
| [OpenERA](https://github.com/ui-insight/OpenERA) | Research Administration | 32 | Production |
| [UCM Daily Register](https://github.com/ui-insight/UCMDailyRegister) | Communications | 10 | Production |
| [Audit Dashboard](https://github.com/ui-insight/AuditDashboard) | Internal Audit | 13 | Production |
| [StratPlan Tactics](https://github.com/ui-insight/StratPlanTacticsMB) | Strategic Planning | Hybrid: JSON canonical + optional insight-db projection (10 tables) | Production |
| [ProcessMapping](https://github.com/ui-insight/ProcessMapping) | Process Intelligence | 15 canonical process maps + 11 workflows + optional `process_maps` projection | Production |

`AISPEG` remains part of the broader UI Insight portfolio, but it is tracked here as adjacent program infrastructure rather than a governed application data model.

## Documentation

Full documentation is published via MkDocs Material:

```bash
pip install mkdocs-material
mkdocs serve
```

## Validation

Run the governance drift check locally:

```bash
python3 scripts/check_governance_drift.py
```

## Structure

```
docs/
  standard/       # Adopted conventions from AI4RA-UDM
  domains/        # Per-application data model documentation
  vocabulary/     # Cross-app AllowedValue landscape
  portfolio/      # Infrastructure, deployment, AI services
  governance/     # Extension protocol and review process
catalog/          # Machine-readable model catalogs (JSON)
vocabularies/     # Federated AllowedValue seed data
```
