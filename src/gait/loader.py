"""Load Strava/Garmin FIT files into tidy per-second dataframes."""

import gzip
from pathlib import Path

import fitdecode
import pandas as pd


def _first_value(frame, names):
    """Return the first field present out of several possible names."""
    for name in names:
        value = frame.get_value(name, fallback=None)
        if value is not None:
            return value
    return None


def load_fit(path):
    """Read one FIT (or .fit.gz) file into a DataFrame of per-second records."""
    path = Path(path)
    opener = gzip.open if path.suffix == ".gz" else open

    rows = []
    with opener(path, "rb") as f:
        with fitdecode.FitReader(f) as fit:
            for frame in fit:
                if isinstance(frame, fitdecode.FitDataMessage) and frame.name == "record":
                    rows.append({
                        "timestamp": frame.get_value("timestamp", fallback=None),
                        "distance_m": frame.get_value("distance", fallback=None),
                        "speed_ms": _first_value(frame, ["enhanced_speed", "speed"]),
                        "altitude_m": _first_value(frame, ["enhanced_altitude", "altitude"]),
                        "heart_rate": frame.get_value("heart_rate", fallback=None),
                        "cadence": frame.get_value("cadence", fallback=None),
                        "fractional_cadence": frame.get_value("fractional_cadence", fallback=None),
                        "garmin_step_length_mm": frame.get_value("step_length", fallback=None),
                    })

    df = pd.DataFrame(rows)
    df["activity_id"] = path.name.split(".")[0]
    return df


def load_device(path):
    """Extract recording device and paired sensors from one FIT file."""
    path = Path(path)
    opener = gzip.open if path.suffix == ".gz" else open

    watch, serial, sensors = None, None, set()
    with opener(path, "rb") as f:
        with fitdecode.FitReader(f) as fit:
            for frame in fit:
                if not isinstance(frame, fitdecode.FitDataMessage):
                    continue
                if frame.name == "file_id" and watch is None:
                    watch = _first_value(frame, ["garmin_product", "product"])
                    serial = frame.get_value("serial_number", fallback=None)
                elif frame.name == "device_info":
                    product = _first_value(frame, ["garmin_product", "product"])
                    dtype = _first_value(frame, ["antplus_device_type", "device_type"])
                    if product is not None or dtype is not None:
                        sensors.add(f"{product}:{dtype}")

    return {
        "activity_id": path.name.split(".")[0],
        "watch": watch,
        "serial": serial,
        "sensors": "|".join(sorted(str(s) for s in sensors)),
    }