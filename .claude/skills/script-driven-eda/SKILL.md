---
name: script-driven-eda
description: Runs the full script-driven EDA workflow. Gathers context from the user before touching data, profiles the dataset on first run, then runs targeted investigation loops — writing scripts, generating charts, deriving findings, and updating notes and process files. Generates its own questions throughout and asks the user when data alone is insufficient. Use when the user says "investigate [topic]", "run the EDA", "start analysis", "close the loop", "analyze the open questions", or "start with this dataset".
---

# Script-Driven EDA

Full workflow for `script_driven_eda/<dataset>/`.

## Wikilink convention

Every cross-reference between files uses wikilinks — no plain filenames, no markdown links.

| File | Wikilink |
|------|----------|
| `context.md` | `[[context]]` |
| `beginning_knowledge.md` | `[[beginning_knowledge]]` |
| `process/active_questions.md` | `[[process/active_questions]]` |
| `process/decisions_made.md` | `[[process/decisions_made]]` |
| `notes/<topic>_notes.md` | `[[notes/<topic>_notes]]` |
| `notes/data_profile_notes.md` | `[[notes/data_profile_notes]]` |
| `notebook_logs/<topic>.json` | `[[notebook_logs/<topic>]]` |

Use wikilinks in: notes files, active_questions.md, decisions_made.md, context.md, beginning_knowledge.md.
Do NOT use wikilinks in: bash commands, Python scripts, or code blocks.

---

## Phase -1: Context Gathering (always first)

**Check first:** does `context.md` exist in the dataset folder?

- **Yes** → read it, then proceed to Phase 0
- **No** → run the context interview before touching any data

### Context interview

Ask the user these questions (all at once, not one by one):

```
1. What is this dataset? (domain, source, time period, geography)
2. What is the end goal — what decision or understanding are you building toward?
3. What specific areas do you want to explore first? (ranked if possible)
4. What columns or metrics matter most to you?
5. Are there any known data quality issues, caveats, or things to watch out for?
6. Is this real data or synthetic? Public or proprietary?
7. Anything else I should know before I start?
```

After the user responds, write `context.md`. See [CONTEXT_TEMPLATE.md](CONTEXT_TEMPLATE.md).
Pay particular attention to `## End goal` and `## Exploration directions` — these drive everything.

Then read `beginning_knowledge.md` if it exists — reconcile contradictions with what the user said.

### When the user gives direction mid-session

Whenever the user redirects, narrows, or reprioritizes — at any point in the workflow:

1. Append a row to `context.md → ## Direction log` immediately
2. Reorder `## Exploration directions` to reflect the new priority
3. Reorder open questions in `process/active_questions.md` to match — questions aligned with the new direction move to the top of `## Open`
4. Continue from where you are, now targeting the reprioritized direction

---

## Phase 0: Data Profiling (first time only)

**Check first:** does `notebook_logs/data_profile.json` exist?

- **Yes** → read it and `notes/data_profile_notes.md`, then proceed to Phase 1
- **No** → run profiling

```
Profiling checklist:
- [ ] Write code/data_profile.py (see DATA_PROFILE_TEMPLATE.md)
- [ ] Run it
- [ ] Read notebook_logs/data_profile.json + charts/
- [ ] Write notes/data_profile_notes.md (see PROFILE_NOTES_TEMPLATE.md)
- [ ] Add generated questions to process/active_questions.md
- [ ] Ask user about anything the data alone cannot explain
```

### Generating questions from the profile

After reading the profile output, add questions to `process/active_questions.md` for anything surprising, suspicious, or unexplained. Do not wait for the user to identify questions — generate them from the data.

Examples of what triggers a question:
- A column with unexpectedly low or zero variance → is this synthetic?
- Nulls that cluster on a specific value in another column → structural or random?
- A hard cap on a numeric column → platform limit or generation parameter?
- A category with implausibly uniform frequency → power law expected but absent?
- A correlation that should exist but doesn't → are these columns independently generated?

### Asking the user

If a finding cannot be resolved from the data alone, ask the user directly before proceeding:

> "I found [X]. This could mean [A] or [B]. Do you know which, or should I investigate further?"

Do not assume. Do not skip. Record the user's answer in `context.md` under `## User Clarifications`.

---

## Phase 1: Targeted Investigation

```
Progress:
- [ ] 1. Read context + open questions
- [ ] 2. Write script
- [ ] 3. Run script
- [ ] 4. Read outputs (JSON + charts)
- [ ] 5. Write notes + generate new questions
- [ ] 6. Update process files
```

### 1. Read context + open questions

Read `context.md` — specifically `## End goal` and `## Exploration directions`.
Read `process/active_questions.md`.
Pick the `## Open` cluster that most directly serves the user's current top direction.
If no open question aligns with the top direction, generate one and add it before proceeding.

### 2. Write script

Write `code/<topic>.py`. See [SCRIPT_TEMPLATE.md](SCRIPT_TEMPLATE.md).

### 3. Run script

```bash
cd script_driven_eda/<dataset> && python code/<topic>.py
```

If the script errors: read the traceback, fix, re-run. Only proceed when the script exits cleanly and the JSON exists.

### 4. Read outputs

- Read `notebook_logs/<topic>.json` for numeric results
- Read each PNG in `charts/` the script saved

### 5. Write notes + generate new questions

Write `notes/<topic>_notes.md`. Format:

```markdown
# <Topic> Findings
*Source data: [[notebook_logs/<topic>]] | Context: [[context]] | Questions: [[process/active_questions]]*

## <Section heading>
<observations derived from JSON numbers>

![](../charts/<chart_name>.png)
<interpretation>

---

## Answers
- **<question>**: <one-line answer> → [[process/active_questions]]

## New questions raised
- [ ] <question this finding opens up> → [[process/active_questions]]
```

Add every item from "New questions raised" to `process/active_questions.md` under `## Open`.

### 6. Update process files

**active_questions.md:**
- Move answered questions to `## Answered`:
  ```
  - [x] **<question>** — <one-line summary>. → [[notes/<topic>_notes]]
  ```
- Add new questions under `## Open`:
  ```
  - [ ] <question> → raised in [[notes/<topic>_notes]]
  ```

**decisions_made.md** — one entry per actionable decision:
```markdown
## <Decision title>
*Source: [[notes/<topic>_notes]] | Context: [[context]] | Date: <today>*

**Decision:** <what to do or not do>
**Reason:** <why, grounded in the numbers>
**Instead:** <alternative if applicable>
```

---

## Asking the user during investigation

At any point, if a finding is ambiguous or requires domain knowledge the data cannot provide, pause and ask. Record the answer in `context.md` under `## User Clarifications` with the date.

Do not proceed on an unresolved ambiguity that would materially affect the finding.
