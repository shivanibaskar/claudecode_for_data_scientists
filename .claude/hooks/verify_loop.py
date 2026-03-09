#!/usr/bin/env python3
"""
Stop hook for the script-driven-eda skill.
Verify the EDA loop is closed before Claude stops.

Checks each dataset under script_driven_eda/ for incomplete loop state:
  - New JSON in notebook_logs/ with no corresponding new notes
  - active_questions.md or decisions_made.md not updated after new analysis

Exit codes:
  0 — loop is clean, Claude may stop
  2 — loop incomplete, Claude is blocked and shown what to fix
"""

import sys
from pathlib import Path
from datetime import datetime, date


def modified_today(path: Path) -> bool:
    return datetime.fromtimestamp(path.stat().st_mtime).date() == date.today()


def check_dataset(dataset_dir: Path) -> list[str]:
    issues = []

    notebook_logs = dataset_dir / "notebook_logs"
    notes_dir = dataset_dir / "notes"
    active_questions = dataset_dir / "process" / "active_questions.md"
    decisions_made = dataset_dir / "process" / "decisions_made.md"

    # Only run checks if new analysis was produced today
    new_jsons = (
        [f for f in notebook_logs.glob("*.json") if modified_today(f)]
        if notebook_logs.exists()
        else []
    )

    if not new_jsons:
        return []  # nothing ran today — no checks needed

    # New JSON exists — verify the rest of the loop is closed
    new_notes = (
        [f for f in notes_dir.glob("*.md") if modified_today(f)]
        if notes_dir.exists()
        else []
    )
    if not new_notes:
        issues.append(
            f"New JSON in notebook_logs/ but no notes written today — "
            f"write notes/{new_jsons[0].stem}_notes.md"
        )

    if active_questions.exists() and not modified_today(active_questions):
        issues.append(
            "active_questions.md not updated — move answered questions to ## Answered"
        )

    if decisions_made.exists() and not modified_today(decisions_made):
        issues.append(
            "decisions_made.md not updated — add decisions from today's findings"
        )

    return issues


def main():
    root = Path.cwd()
    workflow_dir = root / "script_driven_eda"

    if not workflow_dir.exists():
        sys.exit(0)  # not a script-driven EDA project — pass silently

    dataset_dirs = [
        p for p in workflow_dir.iterdir()
        if p.is_dir() and (p / "process" / "active_questions.md").exists()
    ]

    all_issues = []
    for d in dataset_dirs:
        for issue in check_dataset(d):
            all_issues.append(f"[{d.name}] {issue}")

    if all_issues:
        print("EDA loop incomplete — resolve before stopping:\n")
        for issue in all_issues:
            print(f"  ✗ {issue}")
        print()
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
