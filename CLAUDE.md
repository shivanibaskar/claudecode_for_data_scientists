# Project: claudecode_for_data_scientists

## Notebook conventions — AnalysisLog (MANDATORY)

Every Jupyter notebook in this project must use `AnalysisLog` to capture cell
results for LLM consumption.

### Setup (first code cell of every notebook)

```python
import sys
import os
# Adjust the number of ".." to reach the project root from the notebook's location
sys.path.insert(0, os.path.abspath("../../.."))
from utils.analysis_log import AnalysisLog

log = AnalysisLog()
log.add(
    section_id="00_setup",
    title="Setup",
    cell_type="setup",
    purpose="Initialize libraries and analysis log",
    data={"libraries": [...]},
)
```

### Every cell that produces a result must call log.add()

```python
log.add(
    section_id="07_missing_values",   # zero-padded, sortable
    title="Missing Values",
    cell_type="analysis",             # "setup" or "analysis"
    purpose="One sentence: why does this cell exist?",
    data=result.to_dict(orient="index"),  # the computed result as a dict
)
```

### Rules

- `section_id` must be zero-padded and sortable: `"01_"`, `"02_"`, `"03_"`, ...
- `cell_type` is `"setup"` for imports/config/data loading, `"analysis"` for everything that produces a result
- `purpose` is one sentence — no bullet points, no pre-written findings
- `data` should be the raw computed result; the LLM will derive findings itself
- Markdown-only cells do NOT need `log.add()`
- The final cell of every notebook must be: `log.save("../notebook_logs/<notebook_name>.json")`
- Notebooks live in `experiment_N/code/`; logs land in `experiment_N/notebook_logs/`

### utils location

`utils/analysis_log.py` lives at the project root.
Import depth from common notebook locations:
- `experiment_N/code/` → `sys.path.insert(0, os.path.abspath("../../.."))`
