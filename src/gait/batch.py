"""Batch-parse FIT files and summarise each activity for QC."""

import pandas as pd

from .loader import load_fit


def summarise_activity(df):
    """One row of QC facts about a parsed activity."""
    if len(df) == 0:
        return None

    gaps = df["timestamp"].diff().dt.total_seconds()
    long_gaps = gaps[gaps > 30]

    return {
        "activity_id": df["activity_id"].iloc[0],
        "n_samples": len(df),
        "start_time": df["timestamp"].iloc[0],
        "wall_clock_s": (df["timestamp"].iloc[-1] - df["timestamp"].iloc[0]).total_seconds(),
        "median_gap_s": gaps.median(),
        "max_gap_s": gaps.max(),
        "n_gaps_over_30s": len(long_gaps),
        "paused_s": long_gaps.sum(),
        "distance_m": df["distance_m"].max(),
        "has_speed": df["speed_ms"].notna().any(),
        "has_cadence": df["cadence"].notna().any(),
        "has_altitude": df["altitude_m"].notna().any(),
    }


def parse_activities(paths):
    """Parse many files. Returns (list of dataframes, summary table, failures)."""
    frames = []
    summaries = []
    failures = []

    for path in paths:
        try:
            df = load_fit(path)
        except Exception as error:
            failures.append({"path": str(path), "error": repr(error)})
            continue

        summary = summarise_activity(df)
        if summary is None:
            failures.append({"path": str(path), "error": "no records"})
            continue

        frames.append(df)
        summaries.append(summary)

    return frames, pd.DataFrame(summaries), failures