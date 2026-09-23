# Report working sheet — numbers by section

Companion to `docs/decisions.md` (the full record). This is the same material cut by
where it goes in the write-up. Target ~1,400 words total.

---

## Abstract (~120 w) — write this first

Question, method, finding, in that order. Must state the negative plainly.

---

## 1. Question (~180 w)

- Identity: `v = f × L`. Any speed change is absorbed by one term, the other, or both.
- Why the obvious analysis is worthless: step length falls when pace falls *by arithmetic*.
- The real question: does step length fall **more than the partition predicts**?
- Literature prediction (Olaya-Cuartero et al. 2024): stride length shortens **2–5%** under
  fatigue; stride frequency findings are mixed, so "frequency holds constant" must be tested.

---

## 2. Data and method (~320 w)

**Cascade:** 1,177 activities in the Strava export → 448 runs → 446 with a file →
441 with moving time > 600 s → 408 FIT parsed (0 failures) → **402 activities** after cleaning.

**Samples:** 1,325,123 → 1,208,740 (**8.8% dropped**) → **40,376** 30-second windows;
37,315 have gradient (370 runs; 32 activities have no altitude).

**Span:** 2023–2026 for comparison. 2021 = 3 runs, context only. 2022 excluded (all GPX,
no cadence). 2020 = one run under the 10-minute threshold. Say this in one sentence.

**Four decisions that matter (everything else → decision log):**

1. **Cadence ≥ 67 steps/min** separates running from walking. Histogram is bimodal:
   walking mode 58, running mode ~80–84, density trough 70. Removes 67,960 samples (5.1%).
   Other drops: cadence missing/0 = 27,175; first 60 s = 24,108; speed missing = 53.
2. **Gradient is a covariate, not a filter.** Window gradient noise SD ≈ 2.02% exceeds
   terrain SD ≈ 1.80% (from lag-1 autocorrelation, ρ = 0.44) — about 1.7 m of altitude
   error over a median 83 m window. Noise is speed-dependent: the slowest distance quintile
   passes a |grad| < 1% filter 34.7% of the time vs 47.7% for the fastest, which would
   truncate the low end of the predictor range.
3. **Step length as a ratio of means**, not a mean of ratios — preserves v = f × L at window
   level. Jensen predicts it sits below Garmin's averaged field; it does, by −0.25%
   (n = 40,313 windows).
4. **Standard errors clustered by activity**; per-run slopes aggregated by t-test, never pooled.

**Instrumentation (needed for §5):** watch fr235 → fr255 during 2023. HRM-Pro Plus chest
strap on 53% of 2023 runs, 73% of 2024, ~0% of 2025, 4.5% of 2026. Strap reads **0.77%
(1.27 spm) low** vs wrist, measured within year on 2023–24 (SE 0.26, p = 0.003).

---

## 3. Analysis A — the partition (~180 w)

- **β_L = 0.8781 (SE 0.0062), β_f = 0.1219.** Sum = 1.0000000000.
- Worked example: 2.5 → 3.5 m/s (**+40% speed**) gives step length 0.930 → 1.250 m
  (**+34.4%**) and cadence 161.2 → 168.0 spm (**+4.2%**).
- The sum-to-one is an **identity and a code check, not evidence**. Likewise R² = 0.965 on
  `log_L ~ log_v` is near-tautological — do not report it as explanatory power.
- **No year effect to report.** Naive interaction F = 3.15, p = 0.025; restricted to the
  speed range common to all four years (2.53–3.49 m/s), F = 1.84, p = 0.139. Mechanism:
  the log–log relationship is slightly concave (log_v² = −0.042, p = 0.068) and the years
  span different speed ranges (2023 reached 3.96 m/s at its 95th pct vs 2025's 3.49).
  Matched β_L: 2023 0.898, 2024 0.886, 2025 0.895, 2026 0.847.
  Counter-caution: matching cuts 2023 from 2,408 to 1,388 windows.
- Robustness: flat-window subset (the pre-registered version) gives 0.8785 vs 0.8781.

---

## 4. Analysis B — fatigue (~350 w, the core)

**Sample:** 93 runs ≥ 60 min moving; 85 after the gradient requirement; 16,198 windows.
One regression per run, then a t-test on the 85 slopes.

**The specification ladder** (% change in step length per 10 min):

| specification | slope | 95% CI |
|---|---|---|
| no controls | +0.780 | [+0.451, +1.109] |
| + speed | +0.093 | [+0.051, +0.135] |
| + speed, gradient | +0.098 | [+0.055, +0.141] |
| + speed, gradient, HR | +0.068 | [+0.024, +0.111] |
| **first 30 min only** | **+0.549** | [+0.441, +0.657] |
| **after 30 min** | **−0.018** | [−0.073, +0.036], p = 0.51 |
| after 30 min + HR | −0.040 | [−0.095, +0.015], p = 0.155 |

*HR is a mediator, not a confound* — cardiac drift is a symptom of the fatigue being
measured, so controlling for it risks absorbing the effect. Report as robustness, not primary.

**The warm-up finding** (own short paragraph): stride opens ~0.55%/10 min over roughly the
first 30 minutes at constant speed, then flat. Corroborated by duration — 60–90 min runs
+0.126, 90–120 min +0.095, **> 120 min +0.007 (p = 0.82)** — a fixed early-run effect diluted
over longer runs. No intensity gradient (HR tertiles +0.129 / +0.076 / +0.088).

**The bound — state the null as an exclusion.** Over a 50-minute post-warm-up stretch the
interval bounds total step-length change between **−0.37% and +0.18%**, excluding the
literature's 2–5% shortening. Only **5% of the 85 runs** fall inside that band.

**Trying to break it.** Walking-filter selection was a real concern: across thirds of a long
run, non-running time per running second rises 0.052 → 0.084 → **0.130**, gap-flagged windows
0.9% → 2.4%, and mean step length rises 1.042 → 1.087 m. But the slope is stable as
walk-affected runs are stripped: all 85 runs +0.098; pause rate < 0.05 (44 runs) +0.113;
< 0.02 (26 runs) +0.104; < 0.02 and zero gaps (18 runs) +0.110. Per-run slope correlates
**negatively** with pause rate (−0.24) — the opposite sign to selection inflation.
Sensitivity: retained ≥ 0.70 −0.020; ≥ 0.80 −0.021; wrist-only −0.038. Null throughout.

**The race.** Ironman 70.3 Belgrade, 13 Sep 2026: 20.89 km, 107 min moving, mean 3.26 m/s
(5:07/km), 211 windows, HR 148–171 (mean 157). By quarter, speed 3.275 / 3.275 / 3.310 /
3.169 m/s; step length 1.125 / 1.135 / 1.148 / **1.109** m; cadence 174.7 / 173.1 / 173.0 /
171.5 spm. **Naive slope after 30 min −0.569%/10 min** — the literature signature is visibly
present. **Controlled for speed and gradient, +0.094%.** The shortening is fully accounted
for by slowing. The race sits at the **73rd percentile** of the 85 training-run slopes.
Residual-vs-distance slope after the first 5 km is +0.055 %/km (+0.83% over 15 km).

---

## 5. What did move the partition (~250 w) — lower confidence, say so

**Running off the bike.** At matched speed, cadence is elevated by **+3.09%** in the
Olympic-distance triathlon run leg (14 Jul 2024; strap-matched to 89 comparison runs) and
**+3.33%** in the 70.3 (2026 has only 2 other strap runs so it cannot be strap-matched;
since the strap reads low, the wrist-equivalent gap is nearer +4%). A **level shift present
from the first kilometre**, not fatigue drift.

*Caveat to state explicitly:* both are races, so arousal, race shoes and pacing are
confounded with running off the bike; there are no brick sessions in the dataset; n = 2 events.

The triathlon was found by screening for samples above 5.5 m/s with no cadence recorded —
**exactly 1 activity of 408**, with nothing else above 0.02%.

**Cadence trend (secondary — flag it as such).** Cadence at 3.0 m/s, wrist-only runs:
2023 **163.89**, 2024 **164.54**, 2025 **164.69**, 2026 **167.42**. A rise of **+2.88 spm
from 2024 to 2026**, concentrated entirely in 2026. The uncorrected series gave +4.25 —
about a third of the apparent rise was the chest-strap sensor change.
Volume: 279 / 1,193 / 1,450 / 857 km (2026 is Jan–Sep; 2024 ≈ 1,151 excluding the
triathlon's bike leg).

---

## 6. Limitations (~220 w) — not a formality

- **n = 1.** No force plate, no motion capture, no ground truth on any derived quantity.
- Step length and step frequency derive from a wrist or chest accelerometer and GPS speed,
  **neither validated against a reference here**. Garmin's own `step_length` agrees to
  −0.25%, but Garmin derives it the same way — that confirms arithmetic, not accuracy.
- **The walking filter makes Analysis B blind to fatigue expressed as walk breaks.** Late in
  a long run he runs 2.5× less of the time; those windows are removed by design.
- **Off the bike cannot be separated from racing.** Two events, both races, no brick sessions.
- The cadence trend is one subject over four years with shoes and training content
  uncontrolled.
- **Cannot claim anything about joint kinematics, loading, or injury risk.**

---

## Figures

| # | File | Shows |
|---|---|---|
| 1–2 | `fig01_02_decomposition.png` | step length and cadence vs speed, 37,315 windows, β annotated |
| 3 | `fig03_partition_by_year.png` | β_L by year, all speeds vs matched range |
| 4 | `fig04_fatigue.png` | specification ladder + per-run slope distribution vs literature band |
| 5 | `fig05_race.png` | race: speed, step length, cadence, residual vs distance |
| 6 | `fig06_cadence_trend.png` | cadence at 3.0 m/s by year, wrist-only vs sensor-confounded |

## Writing reminders

- **Confidence hierarchy must show in the prose.** §3–4 rest on 37,315 windows / 370 runs.
  §5's off-the-bike rests on 2 events. Different verbs: "is" / "shows" vs "is consistent
  with" / "suggests, on two observations".
- **Null as exclusion**, never "no significant effect was found".
- **Cut ruthlessly** — 47 logged decisions, room for about six. Link the log; don't summarise it.
- Numbers here are the source of truth for the README and the LinkedIn post too. Write the
  report first so all three agree.
