import json
from pathlib import Path


class AnalysisLog:
    """
    Collects analysis results from notebook cells and saves them to JSON
    for LLM consumption.

    Usage (Jupyter):
        import sys
        sys.path.insert(0, "../../..")  # adjust depth to reach project root
        from utils.analysis_log import AnalysisLog

        log = AnalysisLog()

        # In each cell:
        log.add(
            section_id="07_missing_values",
            title="Missing Values",
            cell_type="analysis",           # "setup" or "analysis"
            purpose="Identify columns with nulls and their rates",
            data=missing_df.to_dict(orient="index"),
        )

        # Final cell:
        log.save("outputs/analysis.json")
    """

    def __init__(self):
        self.entries = []

    def add(
        self,
        section_id: str,
        title: str,
        cell_type: str,
        purpose: str,
        data: dict = None,
    ):
        """
        Register one notebook cell's result.

        Parameters
        ----------
        section_id : str
            Zero-padded sortable identifier, e.g. "07_missing_values".
        title : str
            Human-readable name shown to the LLM.
        cell_type : str
            "setup"    — imports, config, data loading (no analytical result)
            "analysis" — produces a result worth reasoning about
        purpose : str
            One sentence explaining why this cell exists.
        data : dict, optional
            The computed result serialised to a plain dict.
            Use {} or omit for setup cells.
        """
        self.entries.append({
            "section_id": section_id,
            "title": title,
            "cell_type": cell_type,
            "purpose": purpose,
            "data": data or {},
        })

    def save(self, path):
        """Write all collected entries to a JSON file."""
        out = {"sections": self.entries}
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(out, f, indent=2, default=str)
        print(f"Saved → {path}  ({len(self.entries)} sections)")
