# Active Questions — French Motor Claims
*Seeded from [[beginning_knowledge]] and [[context]]. Updated as answers are found or new questions emerge.*

---

## Open

### Claim Distribution
- [ ] What fraction of policies have ClaimNb = 0? Is zero-inflation severe enough to warrant a hurdle/ZIP model over plain Poisson? → raised in [[beginning_knowledge]]
- [ ] What is the distribution of ClaimNb for policies that do have claims — is it mostly 1, or are multi-claim policies common?
- [ ] What does claim frequency (ClaimNb / Exposure) look like — what is the mean, and how heavy is the tail?

### Exposure
- [ ] Is Exposure concentrated near 1.0 (most policies observed a full year), or is it spread? → raised in [[beginning_knowledge]]
- [ ] Are there policies with very low Exposure (< 0.1)? How many, and do they have disproportionate claim rates?

### BonusMalus
- [ ] Is BonusMalus the strongest univariate predictor of claim frequency? → raised in [[beginning_knowledge]]
- [ ] What does the BonusMalus distribution look like — bimodal, or concentrated at the bonus end (<100)?
- [ ] Are malus policies (BonusMalus > 100) a small minority? What is their claim rate vs the bonus population?

### Driver & Vehicle Risk Factors
- [ ] Does DrivAge show the expected U-shaped claim frequency curve? → raised in [[beginning_knowledge]]
- [ ] Does VehPower correlate with claim frequency, or is it flat?
- [ ] Does VehAge matter — are newer or older vehicles associated with more claims?
- [ ] Does VehGas (Diesel vs regular) show a meaningful difference in claim frequency?

### Geography
- [ ] Does Density correlate with claim frequency — are urban policies riskier? → raised in [[beginning_knowledge]]
- [ ] Do Region and Area show geographic clustering of risk?

### Data Quality
- [ ] Are there nulls in any column?
- [ ] Are there outliers in numeric columns (BonusMalus, Density)?
- [ ] Are there any policies with implausibly high ClaimNb relative to Exposure?

---

## Answered

---

## Discarded

*(Questions that turned out to be non-questions — with reason.)*
