# Six Years of Gait

How step length and step frequency organise running speed, and which one gives way under fatigue.
Single-subject (n = 1) longitudinal analysis of Strava/Garmin running data, October 2020 – September 2026.

## Question
<!-- 2–3 sentences: v = f × L, Analysis A (partition), Analysis B (fatigue beyond the partition) -->

## Data
<!-- Source, date range, filters, final activity count (from reports/qc). Note: raw data is not published. -->

## Reproduce
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```
<!-- Then: where to put the export, which scripts/notebooks to run, in what order -->

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

## Results
<!-- Figures 1–6 with one-line captions -->

## Limitations
<!-- n = 1, no ground truth, cadence/GPS unvalidated, no kinematics/loading/injury claims -->
