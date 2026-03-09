# Data Exploration Notes
*Source: [[outputs/initial_data_exploration]]*
*No cleaning. No interpretation. Raw observations from the JSON.*

---

## Dataset Shape

- File: `ncr_ride_bookings.csv`
- 150,000 rows, 21 columns
- Date range: 365 unique dates — full calendar year 2024

---

## Schema & Dtypes

| Column | dtype | null_% | nunique |
|---|---|---|---|
| Date | str | 0% | 365 |
| Time | str | 0% | 62,910 |
| Booking ID | str | 0% | 148,767 |
| Booking Status | str | 0% | 5 |
| Customer ID | str | 0% | 148,788 |
| Vehicle Type | str | 0% | 7 |
| Pickup Location | str | 0% | 176 |
| Drop Location | str | 0% | 176 |
| Avg VTAT | float64 | 7% | 181 |
| Avg CTAT | float64 | 32% | 351 |
| Cancelled Rides by Customer | float64 | 93% | 1 |
| Reason for cancelling by Customer | str | 93% | 5 |
| Cancelled Rides by Driver | float64 | 82% | 1 |
| Driver Cancellation Reason | str | 82% | 4 |
| Incomplete Rides | float64 | 94% | 1 |
| Incomplete Rides Reason | str | 94% | 3 |
| Booking Value | float64 | 32% | 2,566 |
| Ride Distance | float64 | 32% | 4,901 |
| Driver Ratings | float64 | 38% | 21 |
| Customer Rating | float64 | 38% | 21 |
| Payment Method | str | 32% | 5 |

- `Pickup Location` and `Drop Location` both have exactly 176 unique values
- `Driver Ratings` and `Customer Rating` both have nunique=21 — discrete scale, likely 0.1 increments from 3.0–5.0
- `Cancelled Rides by Customer`, `Cancelled Rides by Driver`, `Incomplete Rides` all have nunique=1 — pure flag columns

---

## Missing Values

| Column | null_count | null_% |
|---|---|---|
| Avg VTAT | 10,500 | 7% |
| Avg CTAT | 48,000 | 32% |
| Booking Value | 48,000 | 32% |
| Ride Distance | 48,000 | 32% |
| Payment Method | 48,000 | 32% |
| Driver Ratings | 57,000 | 38% |
| Customer Rating | 57,000 | 38% |
| Cancelled Rides by Driver | 123,000 | 82% |
| Driver Cancellation Reason | 123,000 | 82% |
| Cancelled Rides by Customer | 139,500 | 93% |
| Reason for cancelling by Customer | 139,500 | 93% |
| Incomplete Rides | 141,000 | 94% |
| Incomplete Rides Reason | 141,000 | 94% |

- Four columns share exactly 48,000 nulls (32%): `Avg CTAT`, `Booking Value`, `Ride Distance`, `Payment Method`
- `Driver Ratings` and `Customer Rating` share exactly 57,000 nulls (38%)
- `Avg VTAT` null count (10,500) matches `No Driver Found` booking count exactly

---

## Null Pattern by Booking Status

| Status | Booking Value | Ride Distance | Avg CTAT | Driver Ratings | Customer Rating | Payment Method |
|---|---|---|---|---|---|---|
| Completed | 0% null | 0% null | 0% null | 0% null | 0% null | 0% null |
| Incomplete | 0% null | 0% null | 0% null | 100% null | 100% null | 0% null |
| Cancelled by Customer | 100% null | 100% null | 100% null | 100% null | 100% null | 100% null |
| Cancelled by Driver | 100% null | 100% null | 100% null | 100% null | 100% null | 100% null |
| No Driver Found | 100% null | 100% null | 100% null | 100% null | 100% null | 100% null |

- Nulls are structural, not random — they are 100% determined by booking status
- `Incomplete` rides have booking value and distance but no ratings
- Only `Completed` and `Incomplete` ever have CTAT, distance, value, payment

---

## Booking Status Distribution

| Status | count | % |
|---|---|---|
| Completed | 93,000 | 62% |
| Cancelled by Driver | 27,000 | 18% |
| No Driver Found | 10,500 | 7% |
| Cancelled by Customer | 10,500 | 7% |
| Incomplete | 9,000 | 6% |

- `No Driver Found` and `Cancelled by Customer` have identical row counts (10,500 each)
- Non-completed rows total 57,000 (38%) — matches null count in ratings exactly

---

## Vehicle Type by Booking Status (%)

| Vehicle | Completed | Cancelled by Driver | No Driver Found | Cancelled by Customer | Incomplete |
|---|---|---|---|---|---|
| Auto | 61.9 | 17.8 | 7.2 | 7.2 | 6.0 |
| Bike | 62.3 | 18.1 | 6.7 | 7.0 | 5.9 |
| Go Mini | 62.2 | 17.9 | 6.8 | 7.0 | 6.1 |
| Go Sedan | 61.4 | 18.5 | 7.2 | 6.7 | 6.0 |
| Premier Sedan | 62.1 | 17.9 | 7.1 | 7.0 | 5.9 |
| Uber XL | 62.6 | 17.1 | 7.1 | 7.3 | 5.9 |
| eBike | 62.1 | 18.1 | 7.1 | 6.8 | 6.0 |

- Completion rate is nearly identical across all 7 vehicle types (~61–63%)
- Driver cancellation range: 17.1% (Uber XL) to 18.5% (Go Sedan) — only 1.4pp spread across all types

---

## Numeric Distributions

| Column | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|
| Booking Value | 102,000 | 508.3 | 395.8 | 50.0 | 234.0 | 414.0 | 689.0 | 4,277.0 |
| Ride Distance | 102,000 | 24.6 | 14.0 | 1.0 | 12.5 | 23.7 | 36.8 | 50.0 |
| Avg VTAT | 139,500 | 8.5 | 3.8 | 2.0 | 5.3 | 8.3 | 11.3 | 20.0 |
| Avg CTAT | 102,000 | 29.1 | 8.9 | 10.0 | 21.6 | 28.8 | 36.8 | 45.0 |
| Driver Ratings | 93,000 | 4.23 | 0.44 | 3.0 | 4.1 | 4.3 | 4.6 | 5.0 |
| Customer Rating | 93,000 | 4.40 | 0.44 | 3.0 | 4.2 | 4.5 | 4.8 | 5.0 |

- `Ride Distance` hard-capped at 50.0 max (9 rows hit the ceiling)
- `Avg VTAT` range: 2.0–20.0 exactly
- `Avg CTAT` range: 10.0–45.0 exactly — hard floor and ceiling
- `Driver Ratings` and `Customer Rating` both floor at 3.0 — no rating below 3 in the dataset
- `Booking Value` mean (508) > median (414) — right skew

---

## Ratings (Completed Rides Only)

| | mean | median | std |
|---|---|---|---|
| Driver Ratings | 4.231 | 4.3 | 0.437 |
| Customer Rating | 4.405 | 4.5 | 0.438 |

- Customer rating mean (4.40) is higher than driver rating mean (4.23)
- Both have nearly identical std (~0.44)

---

## Cancellation Reasons

**Customer** (total: 10,500):

| Reason | count |
|---|---|
| Wrong Address | 2,362 |
| Change of plans | 2,353 |
| Driver is not moving towards pickup location | 2,335 |
| Driver asked to cancel | 2,295 |
| AC is not working | 1,155 |

**Driver** (total: 27,000):

| Reason | count |
|---|---|
| Customer related issue | 6,837 |
| The customer was coughing/sick | 6,751 |
| Personal & Car related issues | 6,726 |
| More than permitted people in there | 6,686 |

- Driver reasons sum: 6,837+6,751+6,726+6,686 = 27,000 ✓
- Driver cancellation reasons nearly perfectly evenly distributed — spread of only 151 across 4 categories
- Customer reasons fairly even except "AC is not working" (1,155) is roughly half the other four (~2,300 each)

---

## Payment Method Distribution (Completed Rides: 102,000)

| Method | count |
|---|---|
| UPI | 45,909 |
| Cash | 25,367 |
| Uber Wallet | 12,276 |
| Credit Card | 10,209 |
| Debit Card | 8,239 |

- Sum: 102,000 ✓
- UPI is the dominant method (~45%)
- Cash is second (~25%)

---

## ID Quality

| Column | total_rows | unique | duplicates | sample_raw_value |
|---|---|---|---|---|
| Booking ID | 150,000 | 148,767 | 1,233 | `"CNR5884300"` |
| Customer ID | 150,000 | 148,788 | 1,212 | `"CID1982111"` |

- Both ID columns are stored with surrounding quotes in the raw CSV (e.g., `"CNR5884300"`)
- 1,233 non-unique Booking IDs; 2,457 rows are involved in those duplicates

---

## Duplicate Booking IDs Sample

- 2,457 rows share a non-unique Booking ID
- Sample duplicates have different dates, times, customers, statuses, and vehicle types for the same Booking ID
- Example: `CNR1026036` appears as both "Completed" (Oct 15) and "No Driver Found" (Jul 21) with different customers and different dates — these are not identical rows

---

## Flag Columns

| Column | non_null_count | unique values when non-null |
|---|---|---|
| Cancelled Rides by Customer | 10,500 | `[1.0]` |
| Cancelled Rides by Driver | 27,000 | `[1.0]` |
| Incomplete Rides | 9,000 | `[1.0]` |

- All three flag columns contain only `1.0` when non-null — binary indicators fully redundant with `Booking Status`

---

## Temporal Patterns

**By hour of day** (top hours):

| Hour | count |
|---|---|
| 18 | 12,397 |
| 17 | 11,044 |
| 19 | 11,047 |
| 10 | 9,577 |
| 16 | 9,633 |
| 0–4 | ~1,300–1,380 each |

- Peak demand at 18:00 (12,397 rides)
- Evening block (17–19h) is the busiest period
- Morning secondary peak at 10:00
- Overnight hours (0–4) have roughly equal, low volume (~1,300–1,400 each)
- Demand rises sharply from 5:00 (2,786) to 6:00 (4,160) to 7:00 (5,450)

**By day of week:**

| Day | count |
|---|---|
| Monday | 21,644 |
| Tuesday | 21,391 |
| Wednesday | 21,413 |
| Thursday | 21,215 |
| Friday | 21,397 |
| Saturday | 21,542 |
| Sunday | 21,398 |

- Virtually no variation across days of week — range is only 429 rides (21,215–21,644)

**By month:**

| Month | count |
|---|---|
| Jan | 12,861 |
| Feb | 11,927 |
| Mar | 12,719 |
| Apr | 12,199 |
| May | 12,778 |
| Jun | 12,440 |
| Jul | 12,897 |
| Aug | 12,636 |
| Sep | 12,248 |
| Oct | 12,651 |
| Nov | 12,394 |
| Dec | 12,250 |

- Monthly counts are nearly uniform — range is 970 rides across 12 months
- February is lowest (11,927) consistent with fewer days in month

---

## Location Distribution (Top 20 Pickup Locations)

| Location | count |
|---|---|
| Khandsa | 949 |
| Barakhamba Road | 946 |
| Saket | 931 |
| Badarpur | 921 |
| Pragati Maidan | 920 |
| Madipur | 919 |
| AIIMS | 918 |
| Mehrauli | 915 |
| Dwarka Sector 21 | 914 |
| Pataudi Chowk | 907 |
| Tilak Nagar | 900 |
| Shivaji Park | 900 |
| Udyog Vihar | 897 |
| Kanhaiya Nagar | 895 |
| Vishwavidyalaya | 895 |
| Greater Kailash | 895 |
| Tagore Garden | 889 |
| Jasola | 887 |
| Inderlok | 887 |
| Subhash Chowk | 887 |

- Top 20 locations span a narrow range (887–949) — near-uniform distribution across 176 locations
- No power-law concentration — top location (Khandsa, 949) is only ~1.07x the 20th location (Subhash Chowk, 887)

---

## Correlation Matrix

| | Avg VTAT | Avg CTAT | Booking Value | Ride Distance | Driver Ratings | Customer Rating |
|---|---|---|---|---|---|---|
| Avg VTAT | 1.0 | 0.06 | 0.00 | 0.06 | -0.01 | -0.00 |
| Avg CTAT | 0.06 | 1.0 | 0.00 | 0.10 | 0.00 | 0.00 |
| Booking Value | 0.00 | 0.00 | 1.0 | 0.01 | -0.00 | -0.00 |
| Ride Distance | 0.06 | 0.10 | 0.01 | 1.0 | -0.00 | 0.00 |
| Driver Ratings | -0.01 | 0.00 | -0.00 | -0.00 | 1.0 | -0.00 |
| Customer Rating | -0.00 | 0.00 | -0.00 | 0.00 | -0.00 | 1.0 |

- All pairwise correlations are near zero (max: 0.10 between `Avg CTAT` and `Ride Distance`)
- `Booking Value` and `Ride Distance` correlation is only 0.01 — almost no linear relationship
- `Driver Ratings` and `Customer Rating` correlation is -0.00 — effectively independent

---

## Hard Caps in the Data

| Column | bound | value | count_at_bound | % of non-null |
|---|---|---|---|---|
| Avg VTAT | max | 20.0 | 38 | 0.0% |
| Avg CTAT | max | 45.0 | 144 | 0.1% |
| Ride Distance | max | 50.0 | 9 | 0.0% |
| Driver Ratings | min | 3.0 | 745 | 0.8% |
| Customer Rating | min | 3.0 | 468 | 0.5% |

- Five columns show hard bounds — three at the max, two at the min
- Rating floors (min=3.0) have more rows piled up (745 and 468) than the distance/time ceilings
- `Ride Distance` ceiling (50.0km) has only 9 rows at the bound — nearly no pileup
