# Beginning Knowledge — French Motor Claims

*What I know, assume, and expect before touching the data.*

---

## What I Know About This Dataset

- 677,991 motor TPL policies observed over one year in France
- 11 features + policy ID — fully described, no hidden columns
- Sourced from CASDatasets, a standard actuarial benchmark dataset
- Commonly used to teach Poisson GLM / claim frequency modelling

## What I Know About the Domain

- **Claim frequency** = ClaimNb / Exposure — the standard actuarial target
- **BonusMalus** is the French no-claims discount system: it accumulates over a driver's history, so it's a strong proxy for latent risk
- **Exposure < 1** for mid-year policies — must be used as a model offset, not ignored
- **Poisson distribution** is the standard model for claim counts; zero-inflation is common in TPL data
- **DrivAge** typically shows a U-shaped risk curve — young drivers (<25) and elderly drivers (>70) are both higher risk
- **VehPower** and **VehAge** are standard pricing factors — newer and more powerful cars often cost more to repair

## Assumptions Going In

- ClaimNb will be 0 for the majority of policies (~90%+ expected)
- BonusMalus will be the strongest univariate predictor of ClaimNb
- DrivAge will show a U-shaped relationship with claim frequency
- Exposure distribution will be right-skewed — most policies observed close to a full year
- Density (urban vs rural) will correlate with claim frequency — urban = higher frequency
- Region and Area will show geographic clustering of risk

## What I'm Uncertain About

- How granular Area codes are — whether they map to departments, communes, or something else
- Whether VehBrand has any signal given the anonymisation
- Whether there are interaction effects worth flagging (e.g. young driver + high-power vehicle)
- The exact distribution of BonusMalus — whether it's bimodal (most drivers at 100 or below)

## Questions I Want to Answer

1. What fraction of policies have at least one claim?
2. Is BonusMalus the strongest univariate predictor, as expected?
3. Does DrivAge show the expected U-shaped risk curve?
4. Is Exposure roughly uniform, or concentrated near 1.0?
5. Are there any data quality issues that would affect a Poisson model?

---

*Assumptions will be tested in `notes/` and reconciled in `reweave.md`.*
