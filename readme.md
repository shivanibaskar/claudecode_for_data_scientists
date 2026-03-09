# Claude Code for Data Scientists

A hands-on exploration of data science workflows with Claude Code — figuring out what actually works efficiently.

## What This Repo Is

This is an experiment in workflow design, not a polished guide. Each folder represents a different way of working with Claude Code on real data science tasks. The goal is to think through what makes an AI-assisted DS workflow genuinely efficient — and document what we learn along the way.

Datasets are the vehicle. Workflows are the thing being studied.

## Workflows

| Workflow | What it tests | Datasets |
|----------|--------------|---------|
| [script_driven_eda](script_driven_eda/) | Claude writes + runs focused Python scripts, generates charts, derives findings, updates notes — full loop in one session | French Motor Claims |

Each workflow folder has a `learnings.md` capturing what worked, what didn't, and open questions about the approach.

## Repo Structure

```
claudecode_for_data_scientists/
├── <workflow>/
│   ├── README.md        # how this workflow works
│   ├── learnings.md     # honest account of what worked and what didn't
│   └── <dataset>/
│       ├── context.md
│       ├── code/
│       ├── notes/
│       └── process/
├── utils/
└── readme.md
```

---

*Work in progress — actively being figured out.*
