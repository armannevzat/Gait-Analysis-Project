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
| 2026-09-18 | Exclude GPX activities from the analysis | 40 of 1,166 files (~3%); GPX generally lacks cadence, which both derived variables depend on |
