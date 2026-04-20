#!/usr/bin/env python3
"""Validate that governance docs still match the portfolio state they describe."""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


class CheckRunner:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def ok(self, message: str) -> None:
        self.passes.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def require(self, condition: bool, message: str) -> None:
        if condition:
            self.ok(message)
        else:
            self.fail(message)

    def require_contains(self, path: Path, snippet: str, label: str) -> None:
        text = path.read_text(encoding="utf-8")
        self.require(snippet in text, f"{label} in {path.relative_to(ROOT)}")

    def print_summary(self) -> int:
        for message in self.passes:
            print(f"PASS {message}")
        for message in self.warnings:
            print(f"WARN {message}")
        for message in self.failures:
            print(f"FAIL {message}")
        return 0 if not self.failures else 1


class RemoteUnavailable(RuntimeError):
    pass


class RemoteMissing(RuntimeError):
    pass


class GitHubClient:
    def __init__(self) -> None:
        self.token = (
            os.environ.get("PORTFOLIO_GH_TOKEN")
            or os.environ.get("GH_TOKEN")
            or os.environ.get("GITHUB_TOKEN")
        )

    def _http_json(self, endpoint: str) -> Any:
        request = urllib.request.Request(
            f"https://api.github.com/{endpoint}",
            headers={
                "Accept": "application/vnd.github+json",
                **(
                    {"Authorization": f"Bearer {self.token}"}
                    if self.token
                    else {}
                ),
            },
        )
        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise RemoteMissing(f"GitHub resource not found for {endpoint}") from exc
            raise RemoteUnavailable(
                f"GitHub API request failed for {endpoint}: HTTP {exc.code}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RemoteUnavailable(
                f"GitHub API request failed for {endpoint}: {exc.reason}"
            ) from exc

    def _gh_json(self, endpoint: str) -> Any:
        try:
            completed = subprocess.run(
                ["gh", "api", endpoint],
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise RemoteUnavailable("Neither GitHub token nor gh CLI is available") from exc
        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr.strip() or exc.stdout.strip() or "unknown error"
            if "404" in stderr or "Not Found" in stderr:
                raise RemoteMissing(f"GitHub resource not found for {endpoint}") from exc
            raise RemoteUnavailable(
                f"gh api request failed for {endpoint}: {stderr}"
            ) from exc
        return json.loads(completed.stdout)

    def api_json(self, endpoint: str) -> Any:
        if self.token:
            return self._http_json(endpoint)
        return self._gh_json(endpoint)

    def repo_exists(self, repo: str) -> bool:
        try:
            self.api_json(f"repos/{repo}")
        except RemoteMissing:
            return False
        return True

    def file_text(self, repo: str, path: str) -> str:
        payload = self.api_json(f"repos/{repo}/contents/{path}")
        encoded = payload["content"].replace("\n", "")
        return base64.b64decode(encoded).decode("utf-8")

    def tree_paths(self, repo: str) -> list[str]:
        payload = self.api_json(f"repos/{repo}/git/trees/main?recursive=1")
        return [item["path"] for item in payload["tree"]]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def count_group_values(vocabulary_path: Path) -> tuple[int, int]:
    payload = read_json(vocabulary_path)
    groups = payload["value_groups"]
    return len(groups), sum(len(group["values"]) for group in groups)


def run_local_checks(checks: CheckRunner) -> None:
    onboarding_files = [
        ROOT / "docs/domains/process-mapping.md",
        ROOT / "catalog/processmapping.json",
        ROOT / "vocabularies/processmapping/allowed_values.json",
    ]
    for path in onboarding_files:
        checks.require(path.exists(), f"{path.relative_to(ROOT)} exists")

    processmapping_catalog = read_json(ROOT / "catalog/processmapping.json")
    checks.require(
        processmapping_catalog["process_map_count"] == 24,
        "ProcessMapping catalog process count is 24",
    )
    checks.require(
        processmapping_catalog["workflow_count"] == 15,
        "ProcessMapping catalog workflow count is 15",
    )
    checks.require(
        processmapping_catalog["prompt_file_count"] == 65,
        "ProcessMapping catalog prompt file count is 65",
    )
    checks.require(
        processmapping_catalog["projection_table_count"] == 1,
        "ProcessMapping catalog projection table count is 1",
    )

    open_era_groups, open_era_values = count_group_values(
        ROOT / "vocabularies/research-admin/allowed_values.json"
    )
    ucm_groups, ucm_values = count_group_values(
        ROOT / "vocabularies/communications/allowed_values.json"
    )
    audit_groups, audit_values = count_group_values(
        ROOT / "vocabularies/audit/allowed_values.json"
    )
    pm_groups, pm_values = count_group_values(
        ROOT / "vocabularies/processmapping/allowed_values.json"
    )
    stratplan_groups = len(read_json(ROOT / "catalog/stratplan.json")["controlled_vocabularies"])
    stratplan_values = sum(
        len(values)
        for values in read_json(ROOT / "catalog/stratplan.json")["controlled_vocabularies"].values()
    )

    total_groups = open_era_groups + ucm_groups + audit_groups + pm_groups + stratplan_groups
    total_values = open_era_values + ucm_values + audit_values + pm_values + stratplan_values

    checks.require(total_groups == 56, "Total vocabulary group count is 56")
    checks.require(total_values == 315, "Total vocabulary value count is 315")

    checks.require_contains(
        ROOT / "README.md",
        "| [ProcessMapping](https://github.com/ui-insight/ProcessMapping) | Process Intelligence | 24 canonical process maps + 15 workflows + optional `process_maps` projection | Production |",
        "README ProcessMapping row",
    )
    checks.require_contains(
        ROOT / "README.md",
        "`AISPEG` remains part of the broader UI Insight portfolio, but it is tracked here as adjacent program infrastructure rather than a governed application data model.",
        "README AISPEG scope note",
    )
    checks.require_contains(
        ROOT / "docs/index.md",
        "| [ProcessMapping](domains/process-mapping.md) | Process Intelligence | 24 process maps + 15 workflows + optional `process_maps` projection | None |",
        "docs/index ProcessMapping row",
    )
    checks.require_contains(
        ROOT / "docs/index.md",
        f"The currently onboarded governance applications define {total_groups} vocabulary groups and normalized enum domains totaling {total_values} controlled values.",
        "docs/index aggregate vocabulary summary",
    )
    checks.require_contains(
        ROOT / "docs/portfolio/applications.md",
        "| ProcessMapping | Process Intelligence | 24 process maps + 15 workflows + optional `process_maps` projection | None | None | Complete |",
        "portfolio summary ProcessMapping row",
    )
    checks.require_contains(
        ROOT / "docs/portfolio/applications.md",
        "| AISPEG | Strategic Planning collaboration site | Content/site-oriented app | None documented in repo | None | Out of scope |",
        "portfolio summary AISPEG scope row",
    )
    checks.require_contains(
        ROOT / "docs/portfolio/architecture.md",
        "| `processmapping` / `processmapping_dev` | `processmapping` | ProcessMapping |",
        "architecture processmapping database row",
    )
    checks.require_contains(
        ROOT / "docs/portfolio/architecture.md",
        "| ProcessMapping | `${HOST_PORT:-9240}` frontend host mapping | `docker-compose.deploy.yml` |",
        "architecture processmapping port row",
    )
    checks.require_contains(
        ROOT / "docs/portfolio/architecture.md",
        "pm_be -. optional DATA_SOURCE=insight_db .-> db",
        "architecture processmapping DB connection",
    )
    checks.require_contains(
        ROOT / "docs/governance/extension-protocol.md",
        "### 0. Confirm governance scope",
        "extension protocol scope gate",
    )
    checks.require_contains(
        ROOT / "docs/vocabulary/index.md",
        "| Process Intelligence | ProcessMapping | 9 (JSON-managed) | 70 |",
        "vocabulary index ProcessMapping row",
    )
    checks.require_contains(
        ROOT / "docs/vocabulary/by-domain.md",
        "## Process Intelligence -- ProcessMapping",
        "vocabulary by-domain ProcessMapping section",
    )
    checks.require_contains(
        ROOT / "docs/vocabulary/shared-patterns.md",
        "| ProcessMapping | `UPPER_CASE` | `PRE_AWARD`, `GRANTS_SPECIALIST` |",
        "shared patterns ProcessMapping casing row",
    )
    checks.require_contains(
        ROOT / "mkdocs.yml",
        "- Process Intelligence: domains/process-mapping.md",
        "mkdocs nav ProcessMapping entry",
    )


def run_remote_checks(checks: CheckRunner) -> None:
    client = GitHubClient()

    repos = [
        "ui-insight/OpenERA",
        "ui-insight/UCMDailyRegister",
        "ui-insight/AuditDashboard",
        "ui-insight/StratPlanTacticsMB",
        "ui-insight/ProcessMapping",
        "ui-insight/AISPEG",
    ]

    try:
        for repo in repos:
            checks.require(client.repo_exists(repo), f"remote repository exists: {repo}")
    except RemoteUnavailable as exc:
        checks.warn(str(exc))
        checks.warn("Skipping remaining remote checks")
        return

    open_era_compose = client.file_text("ui-insight/OpenERA", "docker-compose.yml")
    checks.require(
        '- "9200:80"' in open_era_compose and '- "8000"' in open_era_compose,
        "OpenERA remote compose exposes current frontend/backend ports",
    )

    ucm_compose = client.file_text("ui-insight/UCMDailyRegister", "docker-compose.yml")
    checks.require(
        '"${HOST_PORT:-9280}:80"' in ucm_compose and "insight-db-net" in ucm_compose,
        "UCM remote compose documents shared DB and HOST_PORT default",
    )

    audit_compose = client.file_text("ui-insight/AuditDashboard", "docker-compose.yml")
    checks.require(
        '"9380:80"' in audit_compose
        and '"9390:80"' in audit_compose
        and "localhost:8000/api/v1/health" in audit_compose,
        "Audit Dashboard remote compose matches documented ports and backend health endpoint",
    )

    processmapping_deploy = client.file_text(
        "ui-insight/ProcessMapping", "docker-compose.deploy.yml"
    )
    checks.require(
        '"${HOST_PORT:-9240}:80"' in processmapping_deploy
        and "processmapping.insight.uidaho.edu" in processmapping_deploy,
        "ProcessMapping remote deploy config matches documented host binding",
    )

    processmapping_allowed = json.loads(
        client.file_text("ui-insight/ProcessMapping", "data/allowed_values.json")
    )
    pm_remote_groups = len(
        {item["Allowed_Value_Group"] for item in processmapping_allowed["AllowedValues"]}
    )
    pm_remote_values = len(processmapping_allowed["AllowedValues"])
    checks.require(
        pm_remote_groups == 9 and pm_remote_values == 70,
        "ProcessMapping remote controlled-value counts match local governance registry",
    )

    processmapping_tree = client.tree_paths("ui-insight/ProcessMapping")
    process_count = sum(
        path.startswith("processes/") and path.endswith("/process.json")
        for path in processmapping_tree
    )
    workflow_count = sum(
        path.startswith("workflows/") and path.endswith("/workflow.json")
        for path in processmapping_tree
    )
    prompt_count = sum(
        path.startswith("workflows/")
        and "/extraction-tasks/" in path
        and path.endswith(".md")
        for path in processmapping_tree
    )
    checks.require(
        process_count == 24 and workflow_count == 15 and prompt_count == 65,
        "ProcessMapping remote asset counts match local governance registry",
    )

    stratplan_data = json.loads(
        client.file_text(
            "ui-insight/StratPlanTacticsMB", "backend/app/data/strategic_plan_data.json"
        )
    )
    tactic_count = sum(len(unit["tactics"]) for unit in stratplan_data["units"])
    checks.require(
        len(stratplan_data["pillars"]) == 5
        and len(stratplan_data["units"]) == 27
        and tactic_count == 457
        and len(stratplan_data["spigp_awards"]) == 3,
        "StratPlan remote canonical counts match local governance registry",
    )


def main() -> int:
    checks = CheckRunner()
    run_local_checks(checks)
    run_remote_checks(checks)
    return checks.print_summary()


if __name__ == "__main__":
    sys.exit(main())
