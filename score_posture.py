#!/usr/bin/env python3
"""Deterministic TriggerIQ posture scorer."""

from __future__ import annotations
import json
import sys
from pathlib import Path

SEVERITY_WEIGHT = {"critical": 40.0, "high": 25.0, "medium": 10.0}
STATUS_PENALTY = {"pass": 0.0, "fail": 1.0, "unknown": 0.5, "not_applicable": 0.0}
ORDER = {"critical": 0, "high": 1, "medium": 2}


def score(assessment: dict) -> dict:
    checks = assessment.get("checks", [])
    if not isinstance(checks, list):
        raise ValueError("'checks' must be a list")

    maximum = penalty = 0.0
    open_triggers, unknown = [], []
    counts = {"critical": 0, "high": 0, "medium": 0}

    for check in checks:
        cid = check.get("id")
        severity = check.get("severity", "medium")
        status = check.get("status")
        if not cid:
            raise ValueError("Every check requires an id")
        if severity not in SEVERITY_WEIGHT:
            raise ValueError(f"{cid}: invalid severity {severity!r}")
        if status not in STATUS_PENALTY:
            raise ValueError(f"{cid}: invalid status {status!r}")

        weight = SEVERITY_WEIGHT[severity]
        if status != "not_applicable":
            maximum += weight
            penalty += weight * STATUS_PENALTY[status]

        if status == "fail":
            counts[severity] += 1
            open_triggers.append({
                "id": cid,
                "severity": severity,
                "title": check.get("title", ""),
                "action": check.get("remediation", ""),
            })
        elif status == "unknown":
            unknown.append({
                "id": cid,
                "severity": severity,
                "title": check.get("title", ""),
                "required_action": "Manual verification required",
            })

    posture_score = 100.0 if maximum == 0 else 100.0 * (1.0 - penalty / maximum)
    return {
        "score": round(max(0.0, min(100.0, posture_score)), 2),
        "checks_evaluated": len(checks),
        "open_trigger_count": len(open_triggers),
        "unknown_count": len(unknown),
        "failed_by_severity": counts,
        "open_triggers": sorted(open_triggers, key=lambda x: (ORDER[x["severity"]], x["id"])),
        "manual_verification": sorted(unknown, key=lambda x: (ORDER[x["severity"]], x["id"])),
        "interpretation": "Heuristic posture score. Unknown controls are not treated as secure.",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python score_posture.py <assessment.json>", file=sys.stderr)
        return 2
    try:
        assessment = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(json.dumps(score(assessment), indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
