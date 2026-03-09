# Learnings — Uber Ride Analytics

## Conventions
- Log every notebook cell result with `AnalysisLog` — the JSON is what lets an LLM read the outputs without re-running the notebook
- Notebook logs go to `experiment_N/notebook_logs/`, not `outputs/` — set `OUTPUT_DIR = Path('../notebook_logs')` in the setup cell
- No pre-written findings in notebooks — `purpose` is one sentence on why the cell exists; findings come from reading the JSON after

---

## Investigation Process (per question set)

1. **Read `process/active_questions.md`** — identify the specific open questions to target
2. **Design a focused notebook** — one notebook per question cluster, not a catch-all; each cell tests one thing directly
3. **Run the notebook** → JSON saved to `notebook_logs/`
4. **Read the JSON** — derive findings from raw numbers, do not pre-interpret inside the notebook
5. **Write `notes/<topic>_notes.md`** — raw observations, tables from JSON, answers at the bottom under a clear heading; link back to source JSON and forward to `active_questions` and `decisions_made`
6. **Update `process/active_questions.md`** — move answered questions from `## Open` to `## Answered` with a one-line summary and `[[notes/...]]` link
7. **Update `process/decisions_made.md`** — translate answers into actionable decisions: what to do, what not to do, what to use instead; link back to notes

---

## Notebook Design Principles

- Target the question, not the data — design cells around the specific hypothesis to test, not general exploration
- For a "why is correlation zero?" question: test linear + rank correlation, within-group correlation, decile analysis, implied rate CV, and uniform distribution fit — don't just replot the scatter
- For a "are these duplicates real?" question: test row identity, field variation per group, date gaps, numeric range distribution — not just a count
- Replace `scipy` dependencies with pandas-native equivalents where possible (e.g. Spearman = `series.rank().corr(other.rank())`) — keeps the venv minimal
- Run notebooks as scripts first (`nbconvert --to script | python`) to catch errors before in-place execution

---

## Efficiency Notes

- **Parallel question design**: sketch all cells before writing any — avoids reloading data or restructuring mid-notebook
- **Birthday problem as a first check**: when ID collision counts are suspicious, compute `n² / (2 × range)` before building a full investigation — it either rules out the question immediately or confirms it needs depth
- **CV as a generation detector**: coefficient of variation > 1.0 on a derived ratio (e.g. fare/distance) is a strong signal that the numerator and denominator are independently generated — run this early
- **Conditional mean test for correlation**: groupby into tiers and check if the other variable's mean changes — faster to read than a scatter and directly answers the question
- **Uniform distribution fit**: compare actual mean/std against `(min+max)/2` and `(max-min)/sqrt(12)` — two numbers that immediately reveal whether a column was drawn from a uniform distribution
