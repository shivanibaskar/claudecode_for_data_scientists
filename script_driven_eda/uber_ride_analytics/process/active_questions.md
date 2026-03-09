# Active Questions
*Questions raised by [[notes/data_exploration_notes]]. Updated as answers are found or new questions emerge.*

---

## Open

### Uniformity
- [ ] Vehicle type completion rates span only 1.2pp (61.4–62.6%). Is this plausible for real data, or is it a sign of synthetic generation?
- [ ] Driver cancellation reasons are spread across only 151 rows over 27,000 — effectively uniform. Real cancellation reasons would not be this balanced. Synthetic?
- [ ] Day-of-week ride volume varies by only 429 rides across 7 days (~2%). Real demand has weekend/weekday patterns. Why is this absent?
- [ ] Top 20 pickup locations span only 887–949 rides. Real city pickup data follows a power-law (a few hubs dominate). Why is this uniform?
- [ ] Monthly ride counts are nearly identical (range: 970 over 12 months). No seasonal variation at all?

### Hard Caps
- [ ] `Avg VTAT` is capped at 20 min, `Avg CTAT` at 45 min, `Ride Distance` at 50 km. Are these platform limits or data generation parameters?
- [ ] Rating min is 3.0 for both drivers and customers — 745 driver ratings and 468 customer ratings pile up at the floor. Is 3.0 the minimum allowed rating on this platform, or were sub-3 ratings filtered out?

### Structural Nulls
- [ ] `Avg VTAT` has 10,500 nulls matching `No Driver Found` count exactly. Confirmed structural. But what is VTAT measuring — per-ride vehicle arrival time, or a rolling average?
- [ ] `Incomplete` rides have booking value and distance but no ratings. Were ratings never collected for incomplete rides, or were they removed?

### Temporal
- [ ] Morning peak is at 10:00, not 8:00–9:00 as expected for commute traffic. Is the NCR commute pattern different, or is this a data artifact?
- [ ] Demand at 18:00 (12,397) is ~9x demand at 03:00 (1,339). Is the overnight floor real, or does the data exclude late-night rides?

---

## Answered

### Correlations
- [x] **Why is Booking Value / Ride Distance correlation 0.01?** — Both columns are independently generated: fare does not rise with distance (mean fare varies only ₹11 across deciles spanning 2–50km); implied per-km rate has CV=1.6 (std > mean); Ride Distance matches a uniform distribution to within 0.04%. No pricing formula exists in the data. → *[[notes/correlations_notes]]*
- [x] **Are Driver Ratings and Customer Rating independent random draws?** — Yes: Pearson=-0.001, Spearman=-0.002; customer rating mean is 4.40 across all driver rating tiers (range <0.005); the two columns have different distribution shapes (driver unimodal, customer multimodal). → *[[notes/correlations_notes]]*

### ID Quality
- [x] **Why do 2,457 rows share non-unique Booking IDs?** — Random ID collision from synthetic generation: birthday problem math predicts ~1,250 collisions for 150k draws from a 9M range; observed is 1,224. Every duplicate group has a different Customer ID and a median date gap of 105 days, ruling out retries or data entry errors. **Booking ID is not a reliable primary key.** → *[[notes/id_quality_notes]]*
- [x] **Do duplicated Customer IDs represent repeat customers or malformed rows?** — Legitimate repeat customers: 100% have different Booking IDs and timestamps; status mix matches the overall dataset within 0.6pp. → *[[notes/id_quality_notes]]*

---

## Discarded

*(Questions that turned out to be non-questions — with reason.)*

- **"5 booking statuses vs 4 on Kaggle page"** — `No Driver Found` is a real fifth status present in the data. Not an error.
