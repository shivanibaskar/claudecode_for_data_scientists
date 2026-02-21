# RECORD — Raw Observations
*Source: `outputs/initial_data_exploration.json`*
*No interpretations. No fixes. Just what is there.*

---

## Dataset Shape

- File: `ncr_ride_bookings.csv`
- Rows: 150,000
- Columns: 21
- Kaggle page listed 148,770 rows — actual file has 150,000. Small discrepancy, source unclear.

---

## Schema

All 21 columns — dtypes, null %, and unique counts:

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

**Flagged observations:**
- `Booking ID` has 148,767 unique values in 150,000 rows — 1,233 duplicate booking IDs exist. Not investigated yet.
- `Customer ID` has 148,788 unique values — 1,212 repeat customers or duplicate rows. Not investigated yet.
- `Vehicle Type` shows 7 unique values. Kaggle description listed 6 (Go Mini, Go Sedan, Auto, eBike/Bike, UberXL, Premier Sedan). The 7th type is unconfirmed — Bike and eBike appear as separate categories in the data.
- `Pickup Location` and `Drop Location` both have exactly 176 unique values. May be the same set of location names.
- `Cancelled Rides by Customer` and `Cancelled Rides by Driver` have nunique=1 — pure flag columns (single value, likely 1.0). Similarly `Incomplete Rides`.
- `Driver Ratings` and `Customer Rating` both have nunique=21 — discrete values, likely 0.1 increments from 3.0 to 5.0.
- `Date` has 365 unique values — full calendar year covered.
- `Time` has 62,910 unique values — highly granular, individual timestamps per booking.

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

**Flagged observations:**
- 48,000 nulls (32%) in `Avg CTAT`, `Booking Value`, `Ride Distance`, `Payment Method` — all exactly the same count. Strongly suggests these columns are populated only for completed rides (93,000 non-null = completed row count).
- 57,000 nulls (38%) in `Driver Ratings` and `Customer Rating` — both the same count, both missing for 57,000 rows. Non-null count is 93,000 = completed rides. But 93,000 + 57,000 = 150,000 ✓. So ratings are also completed-only, same as booking value.
- 10,500 nulls (7%) in `Avg VTAT` — matches exactly the count of "No Driver Found" bookings (10,500). Suggests VTAT is null when no driver was ever assigned.
- `Incomplete Rides` flag column: 9,000 non-null rows (6% of total) — matches "Incomplete" booking status count.
- 3 unique values in `Incomplete Rides Reason` — not yet seen what they are.

---

## Booking Status

| Status | count | % |
|---|---|---|
| Completed | 93,000 | 62% |
| Cancelled by Driver | 27,000 | 18% |
| No Driver Found | 10,500 | 7% |
| Cancelled by Customer | 10,500 | 7% |
| Incomplete | 9,000 | 6% |

**Flagged observations:**
- 5 distinct statuses (confirmed). "No Driver Found" is a separate status from cancellations — not mentioned on Kaggle page.
- Kaggle page stated customer cancellation rate of 19.15%. Actual data shows 7% (10,500 / 150,000). Driver cancellations at 18% in data vs 7.45% on Kaggle. The numbers are swapped. Possible Kaggle description error, or different denominator used.
- "No Driver Found" (10,500) and "Cancelled by Customer" (10,500) have identical row counts. Could be coincidence.
- Non-completed rows total: 57,000 (38%) = nulls in Driver Ratings / Customer Rating ✓.

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

**Flagged observations:**
- Completion rate is nearly identical across all 7 vehicle types (~61–63%). Virtually no differentiation.
- Driver cancellation ranges from 17.1% (Uber XL) to 18.5% (Go Sedan) — narrow band, ~1.4pp spread.
- The uniformity across vehicle types is striking. Either the data is synthetic/simulated, or vehicle type genuinely has no effect on ride outcomes.

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

**Flagged observations:**
- `Booking Value` max is 4,277, std is 395. Mean (508) >> median (414) — right skew. High-value outliers present.
- `Ride Distance` hard-capped at 50.0km max. Could be a data cap or platform limit.
- `Avg VTAT` capped at 20.0 min max. 181 unique values over a 2–20 range — granular but bounded.
- `Avg CTAT` range is 10–45 min exactly. Hard floor and ceiling suggest capping.
- Both `Driver Ratings` and `Customer Rating` have min=3.0. No ride has a rating below 3. This seems artificial — either by platform design (minimum possible rating is 3) or the data was filtered.
- `Driver Ratings` and `Customer Rating` have nunique=21 — confirming discrete 0.1-increment scale from 3.0 to 5.0.

---

## Ratings (Completed Rides Only)

| | mean | median | std |
|---|---|---|---|
| Driver Ratings | 4.231 | 4.3 | 0.437 |
| Customer Rating | 4.405 | 4.5 | 0.438 |

**Flagged observations:**
- Customers are rated higher than drivers on average (4.40 vs 4.23).
- Both distributions have identical std (~0.44) — unusual symmetry.
- Min=3.0 for both — no rating below 3 in the dataset (see numeric distributions above).

---

## Cancellation Reasons

**Customer cancellation reasons** (total: 10,500):

| Reason | count |
|---|---|
| Wrong Address | 2,362 |
| Change of plans | 2,353 |
| Driver is not moving towards pickup location | 2,335 |
| Driver asked to cancel | 2,295 |
| AC is not working | 1,155 |

**Driver cancellation reasons** (total: 27,000):

| Reason | count |
|---|---|
| Customer related issue | 6,837 |
| The customer was coughing/sick | 6,751 |
| Personal & Car related issues | 6,726 |
| More than permitted people in there | 6,686 |

**Flagged observations:**
- Customer reasons sum: 2,362+2,353+2,335+2,295+1,155 = 10,500 ✓
- Driver reasons sum: 6,837+6,751+6,726+6,686 = 27,000 ✓
- Driver cancellation reasons are nearly perfectly evenly distributed (~6,700–6,837 each, spread of only 151). Extremely uniform — suspicious of synthetic data.
- Customer reasons are also fairly even except "AC is not working" (1,155) which is roughly half the others (~2,300). The drop-off is abrupt with no gradation.
- "Driver asked to cancel" is counted as a customer cancellation — the customer clicked cancel but at the driver's request.
- "Driver is not moving towards pickup location" is a customer-reported driver behavior.

---

## Payment Methods (Completed Rides: 102,000)

| Method | count | approx % |
|---|---|---|
| UPI | 45,909 | 45% |
| Cash | 25,367 | 25% |
| Uber Wallet | 12,276 | 12% |
| Credit Card | 10,209 | 10% |
| Debit Card | 8,239 | 8% |

Total: 102,000 ✓

**Flagged observations:**
- UPI dominates at 45% — consistent with India/NCR market (UPI is the dominant digital payment method in India).
- Cash is second at 25% — notable for a ride-hailing app.
- Card payments (Credit + Debit) combined: ~18%.

---

*All ❓ resolved. Next layer: [[reduce.md]] — distil signal from these observations.*
