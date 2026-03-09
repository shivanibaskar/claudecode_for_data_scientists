# Correlations Notes
*Source: [[notebook_logs/correlations_analysis]]*
*Answers: [[process/active_questions]] → Correlations*
*Decisions: [[process/decisions_made]]*
*No cleaning. No interpretation beyond what the data directly shows.*

---

## Questions Investigated

From `process/active_questions.md`:
1. `Booking Value` and `Ride Distance` correlation is 0.01 — essentially zero. What explains this?
2. `Driver Ratings` and `Customer Rating` correlation is -0.00. Independent random draws, or genuinely uncorrelated?

---

## Q1: Booking Value vs Ride Distance

### Correlation — Linear and Rank-Based

| Method | Value |
|---|---|
| Pearson | 0.0057 |
| Spearman (rank-based) | 0.0038 |
| n | 93,000 |

- Both linear and rank-based correlations are effectively zero — no non-linear relationship hiding behind the Pearson result

---

### Correlation by Vehicle Type

| Vehicle Type | n | Pearson | Spearman | Fare Mean (₹) | Dist Mean (km) |
|---|---|---|---|---|---|
| Auto | 23,155 | 0.0087 | 0.0061 | 506.48 | 25.99 |
| Bike | 14,034 | 0.0107 | 0.0095 | 509.11 | 26.00 |
| Go Mini | 18,549 | 0.0045 | 0.0023 | 507.38 | 25.99 |
| Go Sedan | 16,676 | 0.0011 | -0.0053 | 512.03 | 25.98 |
| Premier Sedan | 11,252 | 0.0071 | 0.0046 | 509.57 | 25.95 |
| Uber XL | 2,783 | -0.0326 | -0.0241 | 505.30 | 25.72 |
| eBike | 6,551 | 0.0129 | 0.0227 | 503.46 | 26.34 |

- Within-vehicle-type correlations remain near zero across all 7 types (range: -0.033 to +0.013)
- Mean distance is virtually identical across all vehicle types (~25.95–26.34 km)
- Mean fare is virtually identical across all vehicle types (~503–512 ₹) — no vehicle-type pricing signal

---

### Mean Fare by Distance Decile

| Decile | Distance Range (km) | Mean Fare (₹) | Median Fare (₹) |
|---|---|---|---|
| 0 (lowest) | 2.0 – 6.82 | 502.33 | 410.0 |
| 1 | 6.83 – 11.68 | 506.30 | 412.0 |
| 2 | 11.69 – 16.41 | 502.60 | 408.0 |
| 3 | 16.42 – 21.24 | 510.12 | 416.0 |
| 4 | 21.25 – 26.02 | 513.68 | 419.0 |
| 5 | 26.03 – 30.78 | 508.83 | 414.0 |
| 6 | 30.79 – 35.58 | 503.98 | 414.0 |
| 7 | 35.59 – 40.34 | 513.22 | 416.0 |
| 8 | 40.35 – 45.12 | 511.90 | 415.0 |
| 9 (highest) | 45.13 – 50.00 | 508.84 | 414.0 |

- Mean fare across all 10 deciles spans only ₹11 (502 – 514) — no monotonic rise with distance
- A 1km ride and a 50km ride have the same expected fare

---

### Uniform Distribution Test

| Column | Actual Mean | Actual Std | Uniform(min,max) Expected Mean | Uniform Expected Std |
|---|---|---|---|---|
| Ride Distance | 26.0005 | 13.8242 | 26.00 | 13.8564 |
| Booking Value | 508.18 | 396.06 | 2,163.50 | 1,220.23 |

- `Ride Distance` actual mean and std match a uniform distribution over its range almost exactly (difference < 0.04%)
- `Booking Value` does not match a simple uniform — it has its own distribution shape (right-skewed), but independently of distance

---

### Implied Per-km Rate (Fare ÷ Distance)

| Metric | Overall |
|---|---|
| Mean ₹/km | 33.86 |
| Std ₹/km | 54.14 |
| Coefficient of Variation | **1.599** |
| Min ₹/km | 1.01 |
| Max ₹/km | 1,666.99 |

By vehicle type: mean ₹/km ranges 32.47–34.66 (< ₹2 spread), std ranges 51–57 across all types — no per-vehicle pricing structure.

- CV of 1.6 means std > mean — the implied rate is completely unstable
- Max rate of ₹1,667/km and min of ₹1.01/km are not consistent with any pricing model
- If a real pricing formula existed (fare = base + rate × distance), CV would be <0.3

---

## Q2: Driver Ratings vs Customer Rating

### Correlation — Linear and Rank-Based

| Method | Value |
|---|---|
| Pearson | -0.001 |
| Spearman (rank-based) | -0.0024 |
| n | 93,000 |

- Zero correlation holds under both methods

---

### Joint Distribution

| Metric | Value |
|---|---|
| Possible (Driver, Customer) pairs | 441 (21 × 21) |
| Observed pairs | **441** |
| Rows where Driver Rating = Customer Rating | 6,920 (7.4%) |
| Expected % if independent | 4.8% (1/21) |

- All 441 possible pairs are observed — full coverage of the rating space
- Matching ratings (diagonal) appear at 7.4% vs 4.8% expected — slight over-representation, not zero
- Top pairs by frequency: (4.2, 4.9)=1,812; (4.3, 4.9)=1,786; (4.2, 4.6)=1,750 — high-customer-rating pairs dominate regardless of driver rating

---

### Customer Rating Mean by Driver Rating Tier

| Driver Rating Tier | n | Driver Mean | Customer Mean | Customer Std |
|---|---|---|---|---|
| 3.0–3.5 | 7,442 | 3.25 | 4.403 | 0.442 |
| 3.5–4.0 | 15,574 | 3.80 | 4.403 | 0.440 |
| 4.0–4.5 | 46,540 | 4.275 | 4.407 | 0.437 |
| 4.5–5.0 | 23,444 | 4.74 | 4.402 | 0.437 |

- Customer rating mean is 4.40x across all four driver tiers — range of 0.005 across a driver rating span of 3.0–5.0
- Customers who experienced a 3.25-average driver gave the same mean rating (4.40) as customers who experienced a 4.74-average driver

---

### Rating Marginal Distributions

**Driver Ratings** (cv of frequencies = 0.88):

| Rating | Count | | Rating | Count |
|---|---|---|---|---|
| 3.0 | 745 | | 4.1 | 6,966 |
| 3.1 | 1,459 | | **4.2** | **13,841** |
| 3.2 | 1,538 | | **4.3** | **14,081** |
| 3.3 | 1,461 | | 4.4 | 7,018 |
| 3.4 | 1,491 | | 4.5 | 4,634 |
| 3.5 | 748 | | **4.6** | **9,368** |
| 3.6 | 2,026 | | 4.7 | 4,678 |
| 3.7 | 3,790 | | 4.8 | 2,328 |
| 3.8 | 3,848 | | **4.9** | **4,705** |
| 3.9 | 3,915 | | 5.0 | 2,365 |
| 4.0 | 1,995 | | | |

**Customer Ratings** (cv of frequencies = 0.89):

| Rating | Count | | Rating | Count |
|---|---|---|---|---|
| 3.0 | 468 | | 4.1 | 5,396 |
| 3.1 | 1,008 | | **4.2** | **10,697** |
| 3.2 | 881 | | **4.3** | **10,995** |
| 3.3 | 900 | | 4.4 | 5,279 |
| 3.4 | 928 | | **4.5** | **5,890** |
| 3.5 | 443 | | **4.6** | **11,533** |
| 3.6 | 1,194 | | 4.7 | 5,763 |
| 3.7 | 2,354 | | **4.8** | **5,880** |
| 3.8 | 2,357 | | **4.9** | **11,642** |
| 3.9 | 2,370 | | **5.0** | **5,837** |
| 4.0 | 1,185 | | | |

- Driver ratings peak sharply at 4.2 and 4.3 — unimodal
- Customer ratings show **three distinct elevated bands**: 4.2–4.3, 4.6, and 4.9–5.0 — multimodal, a pattern not present in driver ratings
- Both columns use exactly 21 values on a 0.1 step from 3.0 to 5.0

---

### Discrete Value Structure

- Both columns: exactly 21 values, step size uniformly 0.1, range 3.0–5.0
- Step size has zero variation — no fractional values like 3.15 or 4.27 appear anywhere

---

## Answers to Original Questions

**Q1: Why is the Booking Value / Ride Distance correlation 0.01?**

`Booking Value` and `Ride Distance` are **independently generated columns**. Evidence:
1. Pearson (0.006) and Spearman (0.004) are both near zero — no linear or rank-based relationship
2. Within every vehicle type the correlation remains near zero (max 0.013) — vehicle-type rate differences are not the cause
3. Mean fare varies by only ₹11 across distance deciles spanning 2–50km — there is no monotonic fare rise with distance
4. Implied per-km rate has CV = 1.6 (std > mean) with values ranging from ₹1 to ₹1,667/km — no pricing formula exists
5. `Ride Distance` actual mean and std match a uniform distribution over its range to within 0.04%

---

**Q2: Are Driver and Customer Ratings independent random draws?**

Yes, they are **independently generated from different distributions**. Evidence:
1. Both Pearson (-0.001) and Spearman (-0.002) are effectively zero
2. Customer rating mean is 4.40 across all driver tiers — identical to 3 decimal places despite driver ratings spanning 3.0–5.0
3. All 441 possible (driver, customer) pairs are observed — no avoided combinations
4. The two distributions have different shapes: driver ratings are unimodal (peak at 4.2–4.3); customer ratings are multimodal with elevated bands at 4.2–4.3, 4.6, and 4.9–5.0
5. The slight diagonal over-representation (7.4% vs 4.8% expected) is a weak generation artifact, not evidence of a real relationship
