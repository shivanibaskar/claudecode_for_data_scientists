# Beginning Knowledge — Uber Ride Analytics

*What I know, assume, and expect before touching the data.*

---

## What I Know About This Dataset

- 148,770 Uber bookings from 2024
- Covers ride outcomes (completed, cancelled), vehicle types, locations, fares, distances, ratings, and payment methods
- ~66% success rate, ~25% cancellation rate (split between customer and driver cancellations)

## What I Know About Uber's Business

- Uber's core tension: supply (drivers) vs demand (riders) — cancellations are a signal of imbalance
- Driver ratings and customer ratings are both present — this is a two-sided marketplace
- Vehicle type mix (eBike, Auto, Go Mini, UberXL, Premier) reflects different price points and use cases
- Payment method diversity (UPI, Cash, Card, Wallet) may reflect regional or demographic patterns

## Assumptions Going In

- Peak demand likely clusters around morning and evening commute hours
- Cancellation reasons will differ between customer and driver — drivers may cancel due to long pickup distances, customers due to wait time
- Higher booking value rides are probably less likely to be cancelled (more commitment)
- Driver ratings and customer ratings are likely correlated — bad rides are bad for both
- Ride distance and booking value will be strongly correlated (price ~ distance)

## What I'm Uncertain About

- Whether "location" is granular (coordinates) or categorical (zone names) — this affects what spatial analysis is possible
- Whether the data is from a single city or multiple cities — changes interpretation significantly
- Whether `Avg VTAT` and `Avg CTAT` are per-ride or rolling averages

## Questions I Want to Answer

1. What drives cancellations — is it time of day, vehicle type, wait time, or location?
2. Are there patterns in driver vs customer cancellation reasons?
3. What does the rating distribution look like — is it skewed high (as ratings typically are)?
4. Which vehicle types generate the most revenue vs. the most cancellations?
5. Is there a time-of-day or day-of-week pattern in demand and cancellations?

---

*These assumptions will be tested and updated in `notes/` and reconciled in `reweave.md`.*
