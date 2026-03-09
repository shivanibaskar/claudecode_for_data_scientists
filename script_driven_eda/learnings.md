# Learnings — script_driven_eda workflow

---

## Repo Structure

- Organise by **workflow first**, dataset second — `script_driven_eda/<dataset>/`, not `<dataset>/experiment_N/`
- No `experiment_N` nesting — the workflow folder is the experiment; a different approach means a different workflow folder
- `learnings.md` lives at the workflow level (here), not inside a dataset — learnings are about the approach, not the data
- `utils/` stays at the project root, shared across all workflows and datasets

---

## Workflow Design

- **Scripts over notebooks** for targeted question investigation — `python script.py` is faster and more reliable than `nbconvert --execute`; notebooks are fine for open-ended exploration
- **One script per question cluster** — don't combine unrelated questions; a focused script produces a focused JSON and focused notes
- **Charts via `savefig()`**, never `plt.show()` — Claude reads PNGs directly (multimodal); always `plt.close(fig)` after saving
- **Descriptive chart names**: `<subject>_<what_it_shows>.png` — e.g. `driver_age_claim_frequency.png`, never `chart1.png`
- **AnalysisLog JSON** is the persistent output — Claude reads it across sessions; `data` field holds raw computed results, never pre-written findings

---

## Context Before Data

- Always run the **context interview** before touching data — ask all questions at once, not one by one
- Write `context.md` immediately after — it is the north star for every investigation decision
- `beginning_knowledge.md` captures assumptions before data is seen — reconcile it with findings in `reweave.md`
- **User direction is logged**, not just noted — `context.md → ## Direction log` is append-only; `## Exploration directions` is reordered live when the user redirects

---

## Investigation Loop

- Phase order: context → profiling → targeted investigation — never skip profiling on a new dataset
- **Data profiling first**: schema, nulls, distributions, value counts, null pattern chart — all saved before any hypothesis testing
- Claude **generates questions from the data** during profiling — don't wait for the user to identify them; suspicious findings (zero variance, hard caps, uniform categoricals) go straight into `active_questions.md`
- **Ask the user** when data alone can't resolve an ambiguity — record the answer in `context.md → ## User clarifications` with a link to the source note
- Pick question clusters by alignment with `context.md → ## Exploration directions`, not by order in the file

---

## Wikilinks

- Every cross-reference between files uses `[[wikilinks]]` — no plain filenames, no markdown links
- Notes files carry source links at the top: `*Source: [[notebook_logs/<topic>]] | Context: [[context]]*`
- Answered questions in `active_questions.md` link to their notes: `→ [[notes/<topic>_notes]]`
- Decisions in `decisions_made.md` link to both notes and context

---

## Process Files

- `active_questions.md` grows throughout the session — new questions raised by findings go under `## Open` immediately
- `decisions_made.md` is actionable — every entry says what to do, why (grounded in numbers), and what to use instead
- `log.md` is a running diary — written as you go, not summarised at the end

---

## Hooks & Automation

- **Stop hook** (`verify_loop.py`) blocks Claude from stopping if a new JSON exists with no corresponding notes, or if process files weren't updated — catches incomplete loops automatically
- Hook must use **absolute path** in `settings.json` and resolve project root via `Path(__file__).parents[2]` — `Path.cwd()` is unreliable when Claude cd's into subdirectories
- `settings.local.json` contains personal API tokens in permission patterns — always gitignore it

---

## Efficiency Notes

- **Parallel question design**: sketch all cells/sections before writing any — avoids reloading data mid-script
- **CV as a generation detector**: CV > 1.0 on a derived ratio is a strong signal of independently generated columns
- **Conditional mean test**: groupby into tiers and check if the other variable's mean changes — faster than a scatter for answering correlation questions
- **Uniform distribution fit**: compare actual mean/std against `(min+max)/2` and `(max-min)/sqrt(12)` — two numbers reveal uniform generation immediately
