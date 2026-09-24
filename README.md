# Pace, Not Fatigue

**The step length–frequency partition across four years and a half-Ironman**

Single-subject (n = 1) analysis of Strava/Garmin running data, 2023–2026.
Full write-up: [`docs/report.pdf`](docs/report.pdf)

## Question

Running speed is the product of step frequency (*f*) and step length (*L*): `v = f × L`.
Any change in running speed must be absorbed by either the step frequency or the step
length, or both. This is what defines the partition: how much of a change in speed each
of the two terms carries.

Step length falling when pace falls is simply arithmetic, so saying that step length
decreases late in a run is not a finding — it is bound to happen. The real question is
whether the partition between the two parameters shifts under fatigue, beyond what
slowing alone accounts for. The running literature reports 2–5% stride shortening under
fatigue.

**It did not shift.** Speed increases are carried almost entirely by step length
(β_L = 0.88, β_f = 0.12). Once pace and gradient are controlled, and setting aside a
warm-up effect confined to the first 30 minutes, the 95% interval bounds step-length
change between −0.37% and +0.18% over 50 minutes, excluding the literature benchmark.
In the Ironman 70.3 run split, stride shortened in the final quarter and the drop in
pace accounted for all of it.

## Data

A Strava bulk export of Garmin FIT files from a single subject. The export contained
1,177 activities, of which 448 were runs, 446 had an accompanying file, and 441 had a
moving time longer than ten minutes. Excluding phone-recorded GPX activities, which
carry no cadence data, left 408 activities, all of which parsed without failure.
Cleaning reduced this to 402 activities, producing 40,376 thirty-second windows from
1,208,740 samples.

Year-on-year comparison spans 2023 to 2026. 2022 consists entirely of GPX files, 2020
contains a single run below the ten-minute threshold, and 2021 contributes only three
runs, retained as context rather than for comparison.

Raw and processed data are not published: GPS traces reveal personal locations.

Every decision taken in this project is recorded in [`docs/decisions.md`](docs/decisions.md).

## Results

| Figure | Shows |
|---|---|
| `fig01_02_decomposition.png` | Step length and step frequency against running speed, across 37,315 gradient-adjusted 30-second windows |
| `fig03_partition_by_year.png` | β_L by year under two specifications: all speeds, and restricted to the 2.53–3.49 m/s range shared by all four years |
| `fig04_fatigue.png` | Mean change in step length per 10 minutes under successive control specifications, and the distribution of the 85 individual post-warm-up slopes |
| `fig05_race.png` | Ironman 70.3 Belgrade run split: speed, step length and step frequency against distance, with observed minus predicted step length |
| `fig06_cadence_trend.png` | Cadence at 3.0 m/s by year, wrist-only against the uncorrected series that pools wrist and chest-strap runs |

Two secondary findings are reported with lower confidence: running off the bike raised
cadence by roughly 3% at matched speed, on two race observations; and cadence at
3.0 m/s rose 2.9 steps/min between 2024 and 2026 once a chest-strap sensor change was
removed.

## Reproduce

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Place the Strava bulk export under `data/raw/`, then run the notebooks in order:
`01` → `02` → `03` → `04`.

The notebooks were developed and run interactively. Later notebooks read the processed
parquet files written by earlier ones, so they expect those to exist.

## Repository layout

```
data/raw/        Strava export (not committed)
data/processed/  tidy + windowed datasets (not committed)
src/gait/        loader, cleaning, analysis code
notebooks/       exploration and figure generation
figures/         final figures
reports/qc/      QC summaries and discard logs
docs/            decision log, write-up
```

## Limitations

There is only one subject, the author. There is no force plate and no motion capture,
so there is no ground truth for any derived quantity.

The measurement chain is unvalidated. Step frequency comes from an accelerometer at the
wrist or chest, and speed comes from GPS. Step length is derived from these two.

The walking filter is the main constraint on the headline result. Late in a long run the
subject accumulates roughly 2.5 times more non-running time per second of running, and
those samples are removed by design. The null is therefore specifically that step length
does not shorten beyond the partition *while running*.

Nothing in this data measures joint angles, ground reaction forces or tissue loading. No
claim about kinematics, loading or injury risk follows from any of it.
