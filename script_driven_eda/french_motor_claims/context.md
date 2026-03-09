# Dataset Context — French Motor Claims (freMTPL2freq)
*See also: [[beginning_knowledge]] | [[process/active_questions]] | [[process/decisions_made]]*

## What this dataset is
- **Domain**: Motor third-party liability (TPL) insurance — actuarial / pricing
- **Source**: R-Package CASDatasets v1.0.6 (2016), via Kaggle (floser)
- **Time period**: Policies observed over one year (snapshot, not time series)
- **Geography**: France — regions based on standard French administrative classification
- **Real or synthetic**: Real French TPL insurance data

## End goal
Predict how often a driver will file an insurance claim in a year (claim frequency modelling). The target is ClaimNb with Exposure as an offset — standard Poisson/GLM setup in actuarial pricing. EDA should surface which risk features drive claim frequency and how they interact.

## Exploration directions
1. Understand the claim frequency distribution — how sparse is it, how does Exposure affect it
2. BonusMalus as a claim predictor — it's the French no-claims discount system, should be the strongest signal
3. Driver and vehicle risk factors — DrivAge, VehAge, VehPower, VehGas
4. Geographic patterns — Area code and Region
5. Data quality — nulls, outliers, suspicious values, anything that affects modelling

## Columns that matter most
- **ClaimNb**: target variable — number of claims per policy
- **Exposure**: offset for the model — fraction of year the policy was active
- **BonusMalus**: strongest expected predictor — encodes historical claim behaviour
- **DrivAge**: driver age — U-shaped risk curve expected (young and old drivers riskier)
- **VehPower**: vehicle power — higher power may correlate with higher risk

## Known issues and caveats
- VehBrand categories are anonymised (B1, B2, etc.) — no mapping to real brands available
- Exposure is a fraction of a year — policies observed mid-year will have Exposure < 1
- Most policies will have ClaimNb = 0 — zero-heavy distribution expected
- BonusMalus range is 50–350; <100 is bonus (good driver), >100 is malus (bad driver)

## Direction log
*Append when user redirects mid-session.*

| Date | What the user said | Action taken |
|------|--------------------|--------------|
| 2026-03-08 | End goal is claim frequency prediction; interested in full EDA first | Set up all 5 exploration directions; profiling before targeted investigation |

## User clarifications

| Date | Finding | User's answer | Source note |
|------|---------|---------------|-------------|
