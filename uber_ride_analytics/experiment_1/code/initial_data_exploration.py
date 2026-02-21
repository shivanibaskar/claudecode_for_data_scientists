import marimo

__generated_with = "0.20.1"
app = marimo.App(
    width="medium",
    app_title="Uber NCR — Initial Data Exploration",
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Initial Data Exploration — Uber NCR Ride Bookings

    **Dataset:** `ncr_ride_bookings.csv`
    **Source:** Kaggle — `yashdevladdha/uber-ride-analytics-dashboard`
    **Rows:** 150,000 | **Columns:** 21

    ---

    ## How to download this dataset from Kaggle

    **Option A — Terminal (recommended)**
    ```bash
    # from experiment_1/
    uv run kaggle datasets download yashdevladdha/uber-ride-analytics-dashboard --unzip -p data/
    ```

    **Option B — In a Python cell**
    ```python
    import kaggle, os
    os.makedirs("data", exist_ok=True)
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        "yashdevladdha/uber-ride-analytics-dashboard",
        path="data/",
        unzip=True
    )
    ```

    **Credentials** — Kaggle reads from either:
    - `~/.kaggle/kaggle.json` → `{"username": "...", "key": "..."}`
    - Env var → `export KAGGLE_API_TOKEN=your_token`  *(already set in `~/.zshrc`)*
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import seaborn as sns
    import json
    from pathlib import Path

    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams["figure.dpi"] = 120
    pd.set_option("display.float_format", "{:.2f}".format)
    return Path, json, pd, plt


@app.cell
def _(Path):
    OUTPUT_DIR = Path("outputs")
    OUTPUT_DIR.mkdir(exist_ok=True)
    return (OUTPUT_DIR,)


@app.cell
def _(mo):
    mo.md("""
    ## 1. Load Data
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv("/Users/shivanibaskar/Desktop/github/claudecode_for_data_scientists/uber_ride_analytics/experiment_1/data/ncr_ride_bookings.csv")
    df.shape
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(mo):
    mo.md("""
    ## 2. Schema & Dtypes
    """)
    return


@app.cell
def _(df, pd):
    schema = pd.DataFrame({
        "dtype": df.dtypes,
        "non_null": df.notnull().sum(),
        "null_%": (df.isnull().mean() * 100).round(1),
        "nunique": df.nunique(),
    })
    schema
    return (schema,)


@app.cell
def _(mo):
    mo.md("""
    ## 3. Missing Values
    """)
    return


@app.cell
def _(df, pd, plt):
    nulls = df.isnull().sum()
    null_pct = (nulls / len(df) * 100).round(1)
    missing = pd.DataFrame({"null_count": nulls, "null_%": null_pct})
    missing_nonzero = missing[missing.null_count > 0].sort_values("null_%", ascending=True)

    fig_missing, ax_missing = plt.subplots(figsize=(8, 5))
    ax_missing.barh(missing_nonzero.index, missing_nonzero["null_%"], color="steelblue")
    ax_missing.set_xlabel("% Missing")
    ax_missing.set_title("Missing Values by Column")
    for i, v in enumerate(missing_nonzero["null_%"]):
        ax_missing.text(v + 0.5, i, f"{v}%", va="center", fontsize=9)
    plt.tight_layout()
    fig_missing
    return (missing_nonzero,)


@app.cell
def _(mo):
    mo.md("""
    ## 4. Booking Status
    """)
    return


@app.cell
def _(df, pd, plt):
    status_counts = df["Booking Status"].value_counts()
    status_pct = (status_counts / len(df) * 100).round(1)
    status_df = pd.DataFrame({"count": status_counts, "%": status_pct})

    fig_status, ax_status = plt.subplots(figsize=(7, 4))
    colors_status = ["#2ecc71", "#e74c3c", "#e67e22", "#c0392b", "#95a5a6"]
    status_counts.plot(kind="bar", ax=ax_status, color=colors_status, edgecolor="white")
    ax_status.set_title("Booking Status Distribution")
    ax_status.set_xlabel("")
    ax_status.set_ylabel("Count")
    ax_status.tick_params(axis="x", rotation=20)
    for pi in ax_status.patches:
        ax_status.annotate(
            f"{pi.get_height():,.0f}",
            (pi.get_x() + pi.get_width() / 2, pi.get_height()),
            ha="center", va="bottom", fontsize=9,
        )
    plt.tight_layout()
    fig_status
    return (status_df,)


@app.cell
def _(mo):
    mo.md("""
    ## 5. Vehicle Type
    """)
    return


@app.cell
def _(df, pd, plt):
    vehicle_ct = pd.crosstab(df["Vehicle Type"], df["Booking Status"], normalize="index") * 100
    vehicle_ct.plot(kind="bar", stacked=True, figsize=(9, 5), colormap="Set2", edgecolor="white")
    plt.title("Booking Status by Vehicle Type (%)")
    plt.xlabel("")
    plt.ylabel("%")
    plt.xticks(rotation=25)
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    fig_vehicle = plt.gcf()
    fig_vehicle
    return (vehicle_ct,)


@app.cell
def _(mo):
    mo.md("""
    ## 6. Numeric Distributions
    """)
    return


@app.cell
def _(df):
    numeric_cols = ["Booking Value", "Ride Distance", "Avg VTAT", "Avg CTAT", "Driver Ratings", "Customer Rating"]
    numeric_summary = df[numeric_cols].describe().T
    numeric_summary
    return numeric_cols, numeric_summary


@app.cell
def _(df, numeric_cols, plt):
    def _():
        fig_num, axes_num = plt.subplots(2, 3, figsize=(14, 8))
        axes_num = axes_num.flatten()
        for i, col in enumerate(numeric_cols):
            axes_num[i].hist(df[col].dropna(), bins=40, color="steelblue", edgecolor="white", alpha=0.85)
            axes_num[i].set_title(col)
            axes_num[i].set_ylabel("Count")
        plt.suptitle("Distribution of Numeric Features", fontsize=13)
        plt.tight_layout()
        return fig_num

    _()
    return


@app.cell
def _(mo):
    mo.md("""
    ## 7. Ratings (Completed Rides Only)
    """)
    return


@app.cell
def _(df, plt):
    completed = df[df["Booking Status"] == "Completed"].copy()

    fig_ratings, axes_ratings = plt.subplots(1, 2, figsize=(11, 4))
    for ax_r, col_r, color_r in zip(
        axes_ratings,
        ["Driver Ratings", "Customer Rating"],
        ["#3498db", "#e67e22"],
    ):
        ax_r.hist(completed[col_r].dropna(), bins=20, color=color_r, edgecolor="white", alpha=0.85)
        ax_r.axvline(
            completed[col_r].mean(), color="black", linestyle="--",
            linewidth=1.2, label=f"mean={completed[col_r].mean():.2f}",
        )
        ax_r.set_title(col_r)
        ax_r.legend(fontsize=9)
    plt.suptitle("Rating Distributions (Completed Rides Only)", fontsize=12)
    plt.tight_layout()
    fig_ratings
    ratings_summary = {
        col: {"mean": round(completed[col].mean(), 3), "median": round(completed[col].median(), 3),
              "std": round(completed[col].std(), 3)}
        for col in ["Driver Ratings", "Customer Rating"]
    }
    return (ratings_summary,)


@app.cell
def _(mo):
    mo.md("""
    ## 8. Cancellation Reasons
    """)
    return


@app.cell
def _(df, plt):
    customer_reasons = df["Reason for cancelling by Customer"].value_counts()
    driver_reasons = df["Driver Cancellation Reason"].value_counts()

    fig_cancel, axes_cancel = plt.subplots(1, 2, figsize=(13, 4))
    customer_reasons.plot(kind="barh", ax=axes_cancel[0], color="#e74c3c", edgecolor="white")
    axes_cancel[0].set_title("Customer Cancellation Reasons")
    axes_cancel[0].invert_yaxis()
    driver_reasons.plot(kind="barh", ax=axes_cancel[1], color="#c0392b", edgecolor="white")
    axes_cancel[1].set_title("Driver Cancellation Reasons")
    axes_cancel[1].invert_yaxis()
    plt.tight_layout()
    fig_cancel
    return customer_reasons, driver_reasons


@app.cell
def _(mo):
    mo.md("""
    ## 9. Payment Method
    """)
    return


@app.cell
def _(df, plt):
    payment = df["Payment Method"].value_counts()

    fig_pay, ax_pay = plt.subplots(figsize=(6, 4))
    payment.plot(kind="bar", ax=ax_pay, color="#9b59b6", edgecolor="white")
    ax_pay.set_title("Payment Method (Completed Rides)")
    ax_pay.set_xlabel("")
    ax_pay.tick_params(axis="x", rotation=20)
    for p in ax_pay.patches:
        ax_pay.annotate(
            f"{p.get_height():,.0f}",
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha="center", va="bottom", fontsize=9,
        )
    plt.tight_layout()
    fig_pay
    return (payment,)


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Save Outputs
    """)
    return


@app.cell
def _(
    OUTPUT_DIR,
    customer_reasons,
    driver_reasons,
    json,
    missing_nonzero,
    numeric_summary,
    payment,
    ratings_summary,
    schema,
    status_df,
    vehicle_ct,
):
    outputs = {
        "schema": schema.assign(dtype=schema["dtype"].astype(str)).to_dict(orient="index"),
        "missing_values": missing_nonzero.to_dict(orient="index"),
        "booking_status": status_df.to_dict(orient="index"),
        "vehicle_type_by_status": vehicle_ct.round(1).to_dict(orient="index"),
        "numeric_distributions": numeric_summary.to_dict(orient="index"),
        "ratings": ratings_summary,
        "cancellation_reasons": {
            "customer": customer_reasons.to_dict(),
            "driver": driver_reasons.to_dict(),
        },
        "payment_methods": payment.to_dict(),
    }
    json.dump(outputs, open(OUTPUT_DIR / "initial_data_exploration.json", "w"), indent=2)
    print("Saved → outputs/initial_data_exploration.json")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
