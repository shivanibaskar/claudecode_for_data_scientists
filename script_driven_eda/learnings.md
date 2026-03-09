# Learnings — Script-Driven EDA Workflow

*What we learned about this way of working. Not conventions — those live in the skill and CLAUDE.md.*

---

## What worked well

- **Context interview before data** removed ambiguity that would have shaped the analysis wrong. Having the end goal (Poisson GLM) written down meant every question in `active_questions.md` was framed around modelling relevance, not just curiosity.
- **Claude generating questions from the profile** surfaced things a human scan would miss — the skill's list of question triggers (zero variance, uniform categoricals, hard caps) acts as a checklist that doesn't get skipped.
- **Wikilinks between files** made the investigation traceable. Being able to follow `decisions_made → notes → notebook_logs` is the difference between a reproducible analysis and a folder of scripts.
- **Stop hook** caught the incomplete loop pattern before it became a habit. The first time it fired it was right — notes had been skipped.

---

## What didn't work / friction points

- **Hook path was CWD-dependent** — broke the first time we cd'd into a subdirectory. Absolute paths and `Path(__file__)` resolution are non-negotiable for hooks.

- **`settings.local.json` isn't gitignored by default** — caught it before it was pushed, but the API token was already in the file. Add it to `.gitignore` at project setup, not after.

---

## Open questions about the workflow

- Does the profiling script need to run every new session, or only once? Currently once — but if the data changes (new data drop, joined table), re-running profiling should be explicit, not assumed.
- How should `reweave.md` be used? It exists but hasn't been written yet. Probably most useful at the end of an investigation cluster, not continuously.
- What's the right moment to move from EDA into modelling? The workflow doesn't define this transition — it should probably be a separate workflow folder.
