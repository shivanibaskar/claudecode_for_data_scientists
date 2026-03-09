# Workflow: Script-Driven EDA

Claude writes and runs Python scripts to answer specific questions about a dataset, generates charts, derives findings, and updates the analysis process files — all in one session.

## How It Works

1. **Claude reads `process/active_questions.md`** — picks a question cluster to target
2. **Claude writes a focused Python script** — one script per question cluster, not a catch-all
3. **Claude runs the script** — saves charts to `charts/`, structured results via `AnalysisLog`
4. **Claude reads the output** — JSON log for numbers, PNG files for visual interpretation
5. **Claude writes `notes/<topic>_notes.md`** — raw observations, tables, answers
6. **Claude updates process files** — moves answered questions, adds decisions

## Folder Structure per Dataset

```
<dataset>/
├── data/                        # raw data (gitignored)
├── experiment_1/
│   ├── scripts/                 # analysis scripts (one per question cluster)
│   ├── charts/                  # saved matplotlib PNGs
│   ├── notebook_logs/           # AnalysisLog JSON outputs
│   ├── notes/                   # findings per topic
│   ├── process/
│   │   ├── active_questions.md
│   │   └── decisions_made.md
│   ├── beginning_knowledge.md   # assumptions before touching data
│   ├── reweave.md               # how findings changed prior assumptions
│   └── log.md                   # running diary
└── ideas.md                     # next experiments, open questions
```

## Datasets Tested

| Dataset | Description | Status |
|---------|-------------|--------|
| [uber_ride_analytics](uber_ride_analytics/) | 148K Uber bookings, NCR 2024 | In progress |
