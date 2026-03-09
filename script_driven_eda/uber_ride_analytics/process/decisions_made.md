# Decisions Made
*Decisions that affect how the data is used downstream. Each entry links to the investigation that produced it.*

---

## Booking ID is not a primary key
*Source: [[notes/id_quality_notes]] | Date: 2026-02-21*

**Decision:** Do not use `Booking ID` as a unique row identifier in any downstream join, aggregation, or deduplication logic.

**Reason:** 1,224 Booking IDs appear more than once across genuinely different rides (different customers, dates, locations). The collision count matches the birthday problem prediction for drawing 150,000 IDs from a ~9M-value range — this is a synthetic generation artifact, not business logic. Joining on `Booking ID` will produce spurious matches.

**Instead:** Use the DataFrame row index, or construct a composite key from `(Booking ID, Customer ID, Date, Time)` if a stable identifier is required.

---

## Duplicate Customer IDs are kept as-is; no deduplication needed
*Source: [[notes/id_quality_notes]] | Date: 2026-02-21*

**Decision:** Rows with a repeated `Customer ID` are treated as independent ride records from the same customer. No rows are dropped or merged on this basis.

**Reason:** Every repeated Customer ID group has a distinct Booking ID and a different timestamp — these are separate rides, not duplicate rows. The status mix for repeat-customer rows is statistically identical to the overall dataset (within 0.6pp on all statuses), confirming no anomaly.

---

## Do not use Booking Value or Ride Distance as proxies for each other
*Source: [[notes/correlations_notes]] | Date: 2026-02-21*

**Decision:** Do not impute, predict, or infer `Booking Value` from `Ride Distance` (or vice versa). Treat them as unrelated columns.

**Reason:** Both Pearson (0.006) and Spearman (0.004) correlations are effectively zero across all 93,000 completed rides and within every vehicle type. Mean fare varies by only ₹11 across distance deciles spanning 2–50km. The implied per-km rate has a coefficient of variation of 1.6 (std > mean, range ₹1–₹1,667/km) — no consistent pricing formula exists. `Ride Distance` distribution matches uniform(1, 50) to within 0.04%, confirming it was generated independently of fare.

**Instead:** Use each column only for its own stated meaning. Any fare model must be built on external pricing rules, not this dataset's internal distance values.

---

## Do not treat Driver Ratings and Customer Rating as correlated signals
*Source: [[notes/correlations_notes]] | Date: 2026-02-21*

**Decision:** Analyse `Driver Ratings` and `Customer Rating` as independent columns. Do not average them, use one to fill the other, or treat a high driver rating as predictive of a high customer rating.

**Reason:** Pearson correlation is -0.001 and Spearman is -0.002. Customer rating mean is 4.40 across all driver rating tiers from 3.0 to 5.0 — the conditional mean varies by less than 0.005. The two columns were drawn from different distributions (driver unimodal at 4.2–4.3; customer multimodal with peaks at 4.3, 4.6, 4.9) and are statistically independent.

**Instead:** Use each rating independently. If a single quality signal is needed, do not combine them without an explicit business rationale and external validation data.

---
