# Decision log

One line per decision: date, what, why. This becomes the methods section.

| Date | Decision | Reason |
|---|---|---|
| 2026-09-16 | Raw and processed data excluded from the repo | GPS traces reveal personal locations |
| 2026-09-18 | Derive step length from speed and cadence rather than using Garmin's `step_length` field | Running-dynamics fields are not recorded on all devices/years; derived value agreed with Garmin's to within 0.6% on the test activity (1.068 m vs 1.074 m) |
| 2026-09-18 | Treat Garmin `step_length` as a cross-check only, not validation | Garmin almost certainly derives it from speed and cadence too, so agreement confirms the arithmetic, not physical accuracy |
| 2026-09-18 | Step frequency = (cadence + fractional_cadence) x 2 | Garmin records cadence for one leg, with the decimal part stored separately |
| 2026-09-18 | Use `enhanced_speed` / `enhanced_altitude`, falling back to `speed` / `altitude` | Newer devices record only the enhanced fields; older files may use the original names |
| 2026-09-18 | Candidate rule: drop samples with cadence = 0 | Not running. Test activity showed no auto-pause, so the watch keeps recording while stopped at crossings |
| 2026-09-18 | Candidate rule: drop samples with step length outside 0.5-2.5 m | Stationary shuffling at crossings produced ~0.48 m at ~214 steps/min; two such clusters in the test activity |
| 2026-09-18 | Exclude GPX activities from the analysis | Verified: no cadence field in three sampled GPX files (checked full file text, not just the header). Cost is larger than the 3% estimate - it removes all 12 runs of 2022 and 19 of 56 runs in 2023 |
| 2026-09-18 | Record the sampling interval (median gap between samples) for every activity as a column in the tidy dataset | Sampling rate varies by device and era; needed as a filter, a covariate, and a QC statistic |
| 2026-09-18 | Split or flag gaps longer than 30 s; measure time-into-run as moving time, not wall-clock time | Oldest test activity contained a single 508 s stop inside a 1,375 s wall-clock duration; an unflagged pause would corrupt any within-run fatigue slope |
| 2026-09-18 | QC report (Chunk 3) to include, by year: median sampling interval, count of gaps > 30 s, total paused time | Turns the smart-recording question below into a decision made on counts rather than on one file |

## Open question: irregular sampling in early years (raised 2026-09-18, to resolve in Chunk 3)

The oldest test activity (2020) was recorded with Garmin "smart recording": gaps between samples were mostly 6 s, with a spread of 1-5 s, giving 173 samples across 1,375 s. The 2026 test activity was recorded at 1 Hz (2,886 samples across 2,886 s).

Why it matters: 30-second windows would be built from roughly 5 samples in 2020 and 30 in 2026, so a window mean is not strictly the same quantity in each era. Analysis A compares the speed partition across years, so a device-driven change in sampling is a confound that runs along the same axis as the effect of interest.

Cross-check on the same file: mean sampled speed was 3.38 m/s while distance / wall-clock time gave 2.18 m/s. Removing the 508 s stop gives 3,002 m / 867 s = 3.46 m/s, which reconciles the two. Irregularly sampled means are therefore not time-weighted and need care.

Options, to decide once the QC counts show how many activities are affected:
1. Resample every activity to a common time base before windowing, so each window is formed the same way.
2. Restrict the analysis to activities sampled at or near 1 Hz. Cleaner, but may cost the early years and with them the six-year claim.
3. Keep all activities, carry the sampling interval per activity, and re-run the headline results excluding the sparsely sampled ones as a sensitivity check.

Current preference: option 3, with option 2 as the sensitivity check. Not yet decided.
