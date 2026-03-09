# Profile Notes Template

Write `notes/data_profile_notes.md` after running `code/data_profile.py`.

```markdown
# Data Profile — <Dataset Name>
*Source data: [[notebook_logs/data_profile]] | Context: [[context]] | Assumptions: [[beginning_knowledge]]*

## Schema
| Column | Type | Unique | Notes |
|--------|------|--------|-------|
| <col>  | <dtype> | <n> | <observation> |

## Shape
- <N> rows, <M> columns
- <N> duplicate rows (<pct>%) — [keep/investigate]

## Nulls
| Column | Missing | % | Likely reason |
|--------|---------|---|---------------|
| <col>  | <n>     | <pct> | <structural / unknown> |

## Numeric Distributions
For each column note: range, whether it looks uniform/normal/skewed, hard caps.

- **<col>**: range <min>–<max>, mean <x>, std <y>. [Observation about shape.]

![](../charts/profile_hist_<col>.png)

## Categoricals
For each categorical column note: dominant values, long tail, unexpected entries.

- **<col>**: <N> unique values. Top value is "<val>" (<pct>%). [Power law / uniform / other.]

![](../charts/profile_bar_<col>.png)

## Null Pattern
![](../charts/profile_nulls.png)
[Are nulls structural (tied to a status/condition) or random?]

---

## Open Questions
*Seed [[process/active_questions]] from here.*

- [ ] <question raised by a surprising finding> → [[notes/data_profile_notes]]
- [ ] <question raised by a suspicious pattern> → [[notes/data_profile_notes]]
```

## After writing notes

- Copy every open question into `process/active_questions.md` under `## Open`, each linking back to `[[notes/data_profile_notes]]`
- Update `[[beginning_knowledge]]` if any prior assumption was immediately contradicted — note the contradiction and link to `[[notes/data_profile_notes]]`
