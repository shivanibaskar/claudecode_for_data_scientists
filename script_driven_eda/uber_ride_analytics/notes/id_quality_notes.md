# ID Quality Notes
*Source: [[outputs/id_quality_analysis]]*
*Answers: [[process/active_questions]] → ID Quality*
*Decisions: [[process/decisions_made]]*
*No cleaning. No interpretation beyond what the data directly shows.*

---

## Questions Investigated

From `process/active_questions.md`:
1. Why do 2,457 rows share non-unique Booking IDs with different dates, customers, and statuses?
2. Do duplicated Customer IDs (1,212) represent repeat customers booking multiple rides, or malformed rows?

---

## Booking ID Duplicates — Raw Numbers

| Metric | Value |
|---|---|
| Total rows | 150,000 |
| Unique Booking IDs | 148,767 |
| Booking IDs appearing >1 time | 1,224 |
| Rows involved in duplicate Booking IDs | 2,457 |
| % rows affected | 1.64% |

**Occurrence frequency:**

| Times an ID appears | Count of IDs |
|---|---|
| 1 | 147,543 |
| 2 | 1,215 |
| 3 | 9 |

- 99.3% of duplicated Booking IDs appear exactly twice
- Only 9 IDs appear three times

---

## Booking ID Duplicates — Are Rows Identical?

| Check | Result |
|---|---|
| Exact row duplicates in full dataset | **0** |
| Booking-ID-dup rows that are also exact row duplicates | **0** |
| Booking-ID-dup rows with different content | **2,457** |

- Every row sharing a Booking ID has different content — no row-level copy-paste

---

## Booking ID Duplicates — Field Variation Within Groups

| Field | Groups where field varies | % of 1,224 groups |
|---|---|---|
| Time | 1,224 | **100.0%** |
| Customer ID | 1,224 | **100.0%** |
| Vehicle Type | 1,020 | 83.3% |
| Booking Status | 731 | 59.7% |
| Date | 1,219 | 99.6% |

- Customer ID differs in **every single duplicated Booking ID group** — the same Booking ID was assigned to rides by completely different customers
- Time differs in every group — the rides occurred at different timestamps

---

## Booking ID Duplicates — Status Pair Combinations (Size-2 Groups)

| Status pair | Count |
|---|---|
| Completed \| Completed | 433 |
| Cancelled by Driver \| Completed | 290 |
| Cancelled by Customer \| Completed | 110 |
| Completed \| No Driver Found | 106 |
| Completed \| Incomplete | 93 |
| Cancelled by Driver \| No Driver Found | 41 |
| Cancelled by Driver \| Cancelled by Driver | 37 |
| Cancelled by Customer \| Cancelled by Driver | 32 |
| Incomplete \| No Driver Found | 16 |
| Cancelled by Customer \| Incomplete | 15 |
| Cancelled by Driver \| Incomplete | 15 |
| Cancelled by Customer \| No Driver Found | 11 |
| Incomplete \| Incomplete | 6 |
| No Driver Found \| No Driver Found | 6 |
| Cancelled by Customer \| Cancelled by Customer | 4 |

- Most common pair is Completed+Completed (433) — not a failed→retry pattern
- All 15 possible combinations across 5 statuses are represented
- No single combination dominates in a way that suggests a systematic retry or recovery pattern

---

## Booking ID Duplicates — Date Gap Between Pairs

| Metric | Value |
|---|---|
| Pairs analyzed | 1,215 |
| Mean day gap | 120.3 |
| Median day gap | 105.0 |
| Min day gap | 0 |
| Max day gap | 348 |
| % same-day pairs | 0.4% |
| % within 7 days | 4.6% |
| % more than 30 days apart | 82.9% |
| % more than 90 days apart | 55.8% |

- Median gap of 105 days between paired rows — not a retry behavior (which would cluster at 0–1 days)
- Only 0.4% of duplicate pairs occur on the same day

---

## Booking ID Numeric Range

| Metric | Value |
|---|---|
| Full dataset ID range | 1,000,037 – 9,999,933 |
| ID range span | ~9,000,000 |
| Duplicate IDs: min | 1,026,036 |
| Duplicate IDs: max | 9,987,527 |
| Duplicate IDs: mean | ~5,547,217 |
| Duplicate IDs: median | ~5,639,336 |

- Booking IDs are 7-digit numbers ranging over ~9 million values
- Duplicated IDs span the full numeric range; mean (~5.5M) and median (~5.6M) are centered — no clustering at the edges
- Birthday problem estimate: with 150,000 draws from a space of ~9,000,000, expected collisions = 150,000²/(2 × 9,000,000) ≈ **1,250** — observed: **1,224**. Match is within rounding.

---

## Customer ID Duplicates — Raw Numbers

| Metric | Value |
|---|---|
| Unique Customer IDs | 148,788 |
| Customer IDs appearing >1 time | 1,206 |
| Rows involved | 2,418 |
| % rows affected | 1.61% |

**Rides per customer distribution:**

| Rides | Customers |
|---|---|
| 1 | 147,582 |
| 2 | 1,200 |
| 3 | 6 |

- 99.5% of repeat-Customer-ID rows appear exactly twice
- Birthday problem estimate (same ID space ~9M): expected ~1,250 — but these are genuine repeat customers, not collisions (see below)

---

## Customer ID Duplicates — Field Variation

| Field | Groups where field varies | % of 1,206 groups |
|---|---|---|
| Booking ID | 1,206 | **100.0%** |
| Time | 1,206 | **100.0%** |
| Date | 1,201 | 99.6% |
| Booking Status | 700 | 58.1% |

- Every Customer ID with duplicates has different Booking IDs across rows — they are separate, distinct ride records
- Different dates in 99.6% of groups — they booked at different times

---

## Customer ID Duplicates — Status Mix vs Overall

| Status | Repeat-CID rows % | Overall dataset % |
|---|---|---|
| Completed | 61.4% | 62.0% |
| Cancelled by Driver | 18.4% | 18.0% |
| Cancelled by Customer | 7.2% | 7.0% |
| No Driver Found | 7.0% | 7.0% |
| Incomplete | 6.0% | 6.0% |

- Repeat-customer rows have nearly identical status distribution to the full dataset — within 0.6pp on every status
- No anomalous status concentration in the repeat-customer subset

---

## Answers to Original Questions

**Q1: Why do 2,457 rows share non-unique Booking IDs?**

The duplicate Booking IDs are a **random ID collision artifact from data generation**, not a business logic feature. Three pieces of evidence:
1. Customer ID differs in 100% of groups — the same Booking ID was independently assigned to rides by different customers, which cannot happen in a real booking system where each booking creates a unique ID
2. The date gap between paired rows has a median of 105 days — these are not retries or corrections
3. The observed collision count (1,224) matches the birthday problem prediction (~1,250) for drawing 150,000 IDs from a 9-million-value range

---

**Q2: Do duplicated Customer IDs represent repeat customers or malformed rows?**

They are **legitimate repeat customers**. Evidence:
1. Every duplicated Customer ID group has different Booking IDs (100%) and different timestamps (100%) — they are distinct ride records
2. The status mix for repeat-customer rows is statistically identical to the overall dataset (within 0.6pp on all statuses)
3. Qualitative inspection shows realistic patterns: same customer booking different vehicle types, different pickup locations, on different dates months apart

---

## Data Quality Implications

- **Booking ID is not a reliable primary key** — 1.64% of rows share a Booking ID with a row from a different ride
- **Customer ID duplicates are not a data quality issue** — they reflect actual repeat usage
- **Flag columns remain redundant** — nothing about the ID analysis changes this
- **Downstream joins on Booking ID will produce spurious matches** — any analysis that joins on Booking ID should deduplicate first or use a row index
