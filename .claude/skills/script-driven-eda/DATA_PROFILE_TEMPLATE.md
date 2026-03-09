# Data Profiling Script Template

Run once per dataset. Covers schema, distributions, nulls, cardinality, and outliers.

```python
import sys
import os
sys.path.insert(0, os.path.abspath("../../.."))

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from utils.analysis_log import AnalysisLog

DATA = Path("../data/<filename>.csv")   # update filename
CHARTS = Path("../charts")
CHARTS.mkdir(exist_ok=True)
LOG_DIR = Path("../notebook_logs")
LOG_DIR.mkdir(exist_ok=True)

log = AnalysisLog()
df = pd.read_csv(DATA)

# --- 1. Schema ---
schema = {
    col: {"dtype": str(df[col].dtype), "n_unique": int(df[col].nunique())}
    for col in df.columns
}
log.add(section_id="01_schema", title="Schema", cell_type="setup",
        purpose="Column names, dtypes, and cardinality",
        data=schema)

# --- 2. Shape and duplicates ---
log.add(section_id="02_shape", title="Shape", cell_type="analysis",
        purpose="Row/column count and duplicate rows",
        data={"rows": len(df), "cols": len(df.columns),
              "duplicate_rows": int(df.duplicated().sum())})

# --- 3. Null counts ---
nulls = df.isnull().sum()
log.add(section_id="03_nulls", title="Nulls", cell_type="analysis",
        purpose="Missing value count and rate per column",
        data={col: {"count": int(nulls[col]),
                    "pct": round(nulls[col] / len(df) * 100, 2)}
              for col in df.columns if nulls[col] > 0})

# --- 4. Numeric distributions ---
num_cols = df.select_dtypes("number").columns.tolist()
desc = df[num_cols].describe().round(3)
log.add(section_id="04_numeric", title="Numeric Distributions", cell_type="analysis",
        purpose="Min, max, mean, std, quartiles for all numeric columns",
        data=desc.to_dict())

# Histograms for each numeric column
for col in num_cols:
    fig, ax = plt.subplots(figsize=(6, 3))
    df[col].dropna().hist(bins=40, ax=ax, color="steelblue", edgecolor="none")
    ax.set_title(col)
    ax.set_xlabel(col)
    ax.set_ylabel("count")
    fig.tight_layout()
    # Name: <dataset>_<column>_distribution.png — descriptive, no abbreviations
    safe_col = col.lower().replace(" ", "_")
    fig.savefig(CHARTS / f"{safe_col}_distribution.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

# --- 5. Categorical value counts (top 20 per column) ---
cat_cols = df.select_dtypes(["object", "category"]).columns.tolist()
cat_summary = {}
for col in cat_cols:
    vc = df[col].value_counts().head(20)
    cat_summary[col] = vc.to_dict()
log.add(section_id="05_categoricals", title="Categorical Value Counts", cell_type="analysis",
        purpose="Top 20 values per categorical column to spot dominant categories and long tails",
        data=cat_summary)

# Bar charts for categoricals with <= 20 unique values
for col in cat_cols:
    if df[col].nunique() <= 20:
        fig, ax = plt.subplots(figsize=(7, 3))
        df[col].value_counts().plot(kind="bar", ax=ax, color="steelblue", edgecolor="none")
        ax.set_title(col)
        ax.set_ylabel("count")
        fig.tight_layout()
        # Name: <column>_value_counts.png
        safe_col = col.lower().replace(" ", "_")
        fig.savefig(CHARTS / f"{safe_col}_value_counts.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

# --- 6. Null pattern chart ---
if nulls[nulls > 0].any():
    fig, ax = plt.subplots(figsize=(7, 3))
    (nulls[nulls > 0] / len(df) * 100).sort_values().plot(kind="barh", ax=ax, color="tomato")
    ax.set_xlabel("% missing")
    ax.set_title("Missing value rates by column")
    fig.tight_layout()
    fig.savefig(CHARTS / "missing_value_rates.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

log.save(LOG_DIR / "data_profile.json")
print("Done. Profile saved to", LOG_DIR / "data_profile.json")
```
