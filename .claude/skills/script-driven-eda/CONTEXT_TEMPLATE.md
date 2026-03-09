# Context Template

Write `context.md` at `script_driven_eda/<dataset>/context.md` after the user interview.
Update it live whenever the user gives new direction during a session.

```markdown
# Dataset Context — <Dataset Name>
*See also: [[beginning_knowledge]] | [[process/active_questions]] | [[process/decisions_made]]*

## What this dataset is
- **Domain**: <e.g. ride-hailing, e-commerce, healthcare>
- **Source**: <Kaggle / internal / scraped / provided by client>
- **Time period**: <date range>
- **Geography**: <city / country / global>
- **Real or synthetic**: <real / synthetic / unknown>

## End goal
*The outcome the user is working toward. Read this before every investigation step.*

<One paragraph. What decision, model, or understanding is this analysis building toward?>

## Exploration directions
*Specific areas the user wants to explore, in priority order. Update when user redirects.*

1. <highest priority direction, e.g. "understand what drives cancellations">
2. <next direction>
3. <next direction>

## Columns that matter most
- **<col>**: <why it matters to the user's goal>

## Known issues and caveats
<Anything the user flagged before analysis started.>

## Direction log
*Append every time the user gives new direction mid-session. Never delete entries.*

| Date | What the user said | Action taken |
|------|--------------------|--------------|
| <date> | <verbatim or close paraphrase> | reprioritised [[process/active_questions]], updated `## Exploration directions` |

## User clarifications
*Factual clarifications added when data alone cannot resolve a question.*

| Date | Finding | User's answer | Source note |
|------|---------|---------------|-------------|
| <date> | <what was unclear> | <what the user said> | [[notes/<topic>_notes]] |
```

## Rules

- Write verbatim from the user's answers — do not paraphrase or editorialize
- "I don't know" is valid and useful — record it explicitly
- **Exploration directions** are the active investigation agenda — reorder them when the user reprioritizes
- **Direction log** is append-only — it is a record of how the investigation evolved
- Read `## End goal` and `## Exploration directions` before picking a question cluster in Phase 1
