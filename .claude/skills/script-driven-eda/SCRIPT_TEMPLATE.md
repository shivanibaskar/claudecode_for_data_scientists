# Script Template

Standard structure for every investigation script.

```python
import sys
import os
sys.path.insert(0, os.path.abspath("../../.."))  # reaches project root from code/

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from utils.analysis_log import AnalysisLog

DATA = Path("../data/ncr_ride_bookings.csv")   # adjust filename as needed
CHARTS = Path("../charts")
CHARTS.mkdir(exist_ok=True)
LOG_DIR = Path("../notebook_logs")
LOG_DIR.mkdir(exist_ok=True)

log = AnalysisLog()
log.add(
    section_id="00_setup",
    title="Setup",
    cell_type="setup",
    purpose="Load data and initialise analysis log",
    data={"file": str(DATA)},
)

df = pd.read_csv(DATA)

# --- analysis cells ---

result = ...  # compute something

log.add(
    section_id="01_<section>",
    title="<Title>",
    cell_type="analysis",
    purpose="One sentence: why does this cell exist?",
    data=result.to_dict(),  # raw result; Claude derives findings from this
)

# --- charts ---

fig, ax = plt.subplots(figsize=(8, 4))
# ... plot ...
fig.savefig(CHARTS / "<topic>_<chart_name>.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# --- save ---
log.save(LOG_DIR / "<topic>.json")
print("Done. JSON saved to", LOG_DIR / "<topic>.json")
```

## Rules

- One script per question cluster — do not combine unrelated questions
- `data` in `log.add()` must be a dict of raw computed values; no pre-written findings
- Save every chart with `plt.close(fig)` immediately after `savefig` to avoid memory leaks
- Print a confirmation at the end so the Bash output confirms success

## Chart naming

Chart filenames must be descriptive enough to understand without opening the file.

Pattern: `<subject>_<what_it_shows>.png`

Good:
- `booking_value_by_vehicle_type.png`
- `cancellation_rate_by_hour.png`
- `ride_distance_distribution.png`
- `driver_rating_vs_customer_rating.png`

Bad:
- `chart1.png`
- `plot.png`
- `fig_01.png`
- `analysis.png`
