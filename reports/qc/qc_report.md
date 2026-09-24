# QC report — parsed running dataset

Generated 18 September 2026, from `data/processed/activity_summary.parquet`.
Source: Strava bulk export, original Garmin `.fit` files.

## What is in the dataset

408 running activities, 1,325,123 per-second samples, 3,788 km.

| Year | Activities | Samples | Median gap (s) | % at 1 Hz | With cadence | With speed | With altitude | Runs with pauses | Paused (h) | Distance (km) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2021 | 3 | 598 | 6.0 | 0.0 | 3 | 3 | 3 | 1 | 0.1 | 9.0 |
| 2023 | 37 | 97,761 | 1.0 | 83.8 | 37 | 37 | 29 | 7 | 0.4 | 279.2 |
| 2024 | 131 | 422,483 | 1.0 | 100.0 | 131 | 131 | 121 | 33 | 2.7 | 1,193.4 |
| 2025 | 149 | 511,942 | 1.0 | 100.0 | 149 | 149 | 145 | 17 | 1.4 | 1,449.7 |
| 2026 | 88 | 292,339 | 1.0 | 100.0 | 88 | 88 | 78 | 10 | 0.5 | 856.8 |

| 2026 | 88 | 292,339 | 1.0 | 100.0 | 88 | 88 | 78 | 10 | 0.5 | 856.8 |

Note: distances here are total recorded activity distance at parse time. Activity
12671640206 (July 2024) is an Olympic-distance triathlon whose 52.1 km includes the
swim and bike legs; running volume reported in the write-up counts only its 10.35 km
run leg, giving 1,152 km for 2024. See `docs/decisions.md`, 2026-09-23.

## How the 408 were selected

## How the 408 were selected

| Step | Activities remaining |
|---|---|
| All activities in the Strava export | 1,177 |
| Type = Run | 448 |
| With a recorded file (drops manual entries) | 446 |
| Moving time > 600 s | 441 |
| FIT format (drops GPX, which has no cadence) | 408 |
| Parsed without error | 408 |

Two years disappear at the GPX step: all 12 runs of 2022 were phone-recorded GPX, as were 19 of the 56 runs in 2023, and the single 2020 run fell below the 10-minute moving-time threshold. Serious run training began in 2023, so the sparse earlier years reflect low running volume rather than missing recording.

## Data quality

**Cadence and speed: complete.** All 408 activities have both. No treadmill runs (which would lack GPS speed) survived the filters, and no activity lacks the cadence needed for step frequency.

**Altitude: 94% coverage.** 32 activities (8 in 2023, 10 in 2024, 4 in 2025, 10 in 2026) have no altitude data, so gradient cannot be computed for them and they are excluded from the flat-terrain subset used in Analysis A.

**Sampling rate: 1 Hz from 2023 onward.** Every 2024–2026 activity is recorded at one sample per second. Six of the 37 activities in 2023 (16%) are not, and the three 2021 activities use Garmin smart recording at 5–6 s intervals. The sampling interval is carried per activity so that sparsely sampled runs can be filtered or tested as a sensitivity check.

**Pauses: 68 of 408 activities (17%) contain a gap longer than 30 s**, totalling 5.1 hours. The largest single gap observed was 528 s. Time into the run is therefore measured as moving time, with gaps over 30 s excluded, so that stops at crossings do not enter a fatigue slope as if they were running time.

## What this dataset can and cannot support

It supports a four-year analysis (2023–2026, 405 activities) with a year-by-year comparison, since each of those years has 37 or more activities. 2021 is shown as context only, at 3 activities.

It cannot support a claim about 2020 or 2022, and it cannot support any statement about joint kinematics, loading or injury risk, since step length and step frequency are derived from watch cadence and GPS speed with no reference measurement.
