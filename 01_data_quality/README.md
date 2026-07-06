# Module 1 — Data Quality Assessment

## What This Module Is About

Before any AI model can be trusted, the data it learns from must be trustworthy.
UGRO Capital's GRO Score 3.0 uses three external data sources — credit bureau
data, bank statement data, and GST data — to score MSME loan applicants. If any
of those sources contains missing values, impossible numbers, or contradictory
fields, the model's output is unreliable, and lending decisions built on top of
it carry hidden risk.

This module asks a simple governance question: how good is the data going into
GRO Score, and how would we know if it degraded?

To answer that, we built a complete data quality assessment pipeline from scratch:
generate realistic data, deliberately break it in known ways, run automated checks,
and measure how many problems the checks actually caught. The headline result:
an overall DQ score of 97.4/100, with a validation suite that caught 94.3% of
all known issues across 6 data quality dimensions.

---

## The Six Data Quality Dimensions

Data quality is not one thing — it has six distinct dimensions, each measuring
something different. Understanding these is important because a dataset can score
perfectly on five dimensions and catastrophically fail the sixth.

| Dimension | What It Measures | Example Failure |
|---|---|---|
| Completeness | Are all required values present? | Bureau score missing for 2% of applicants |
| Accuracy | Are values correct and plausible? | Bureau score of 950 (max is 900) |
| Validity | Are values in the right format and domain? | PAN number with 7 characters instead of 10 |
| Uniqueness | Are records that should be unique actually unique? | Two loan applications sharing the same applicant ID |
| Consistency | Do fields agree with each other logically? | Approved amount greater than requested amount |
| Timeliness | Was the data fresh when it was used? | Bureau data pulled 200 days before the application decision |

---

## Why We Used Synthetic Data

We have no access to UGRO Capital's real customer data — and we should not.
Using real personal financial data without authorization would itself be a
data governance violation. Instead, we generated a synthetic dataset of 15,000
rows that mirrors the *structure* and *statistical shape* of the data UGRO
publicly describes using: credit bureau fields, bank statement fields, and GST
fields. The synthetic data uses realistic distributions (e.g. bureau scores
follow a normal distribution centered at 670, loan amounts follow a log-normal
distribution) so that any findings are meaningful rather than artifacts of
random noise.

---

## Why We Injected Issues Deliberately

Most data quality projects run validation checks on real data and report whatever
they find. The problem with that approach is you never know how good your checks
are — maybe your suite is only catching 20% of real problems and missing 80%.

We took a different approach called **ground-truth methodology**:

1. Generate a perfectly clean dataset with zero quality issues
2. Deliberately inject known issues across all 6 dimensions, logging every single change
3. Run the validation suite against the now-broken dataset
4. Compare what the suite flagged against what we know we broke

This lets us calculate **recall** — the percentage of known issues the suite
actually detected. Our suite achieved 94.3% recall across 2,370 injected issues.
That is a verifiable, defensible number, not a claim.

---

## Scripts — What Each One Does and Why

### `src/schema.py`
**What:** Defines all controlled vocabularies (allowed states, sectors, loan
statuses), numeric ranges (bureau score: 300–900, interest rate: 8–36%), and
statistical distributions used across the module.

**Why:** Having one central file that every other script imports from means
there is one place to update if a business rule changes. It also means the
Great Expectations checks and the data generator always use identical rules —
they cannot accidentally drift apart.

### `src/generate_synthetic_data.py`
**What:** Generates a clean 15,000-row synthetic MSME loan dataset with 35
columns across four categories: application metadata, credit bureau data, bank
statement data, and GST data. Uses `--seed 42` for reproducibility — running
it twice always produces identical output.

**Why:** We need a realistic baseline dataset to inject issues into and validate
against. The seed ensures that anyone who clones this repo and runs the script
gets the exact same dataset we built and tested with.

### `src/inject_quality_issues.py`
**What:** Takes the clean dataset and deliberately injects 2,370 data quality
issues across all 6 dimensions. Logs every single change — row index, column,
dimension, original value, injected value — to a ground-truth CSV file.

**Why:** This is the foundation of the ground-truth methodology. Without this
log, we cannot measure whether our validation suite is any good. The log is
written before Great Expectations ever sees the data, so it is completely
independent of the validation results.

### `src/run_validation.py`
**What:** Runs a Great Expectations v1.x validation suite against the dirty
dataset. The suite contains 15 expectations covering all 6 DQ dimensions.
Saves results to a JSON file.

**Why:** Great Expectations is an industry-standard data quality framework.
Using it (rather than writing raw if/else checks) produces structured,
auditable results that a CDO or regulator can review. The `mostly` threshold
parameter on each expectation mirrors how real production monitoring works —
you set a tolerance level and alert when violations exceed it.

### `src/dq_scorecard.py`
**What:** Reads the ground-truth log and GE validation results to produce a
per-dimension scorecard with violation rates, dimension scores (0–100), and
GE detection status.

**Why:** The scorecard translates raw validation output into business-readable
metrics. A CDO does not need to read JSON validation logs — they need a table
that shows which dimensions are healthy and which need attention.

### `src/generate_dq_report.py`
**What:** Generates a professional PDF report from the scorecard, written for
a Chief Data Officer audience. Covers executive summary, methodology, per-dimension
findings with business risk narratives, the scorecard table, and prioritised
recommendations.

**Why:** Code and numbers alone do not drive governance decisions — narrative
does. The report translates every technical finding into a business risk
statement and a concrete recommended action.

---

## How to Run (in order)

Run all commands from the project root with your virtual environment active.

```bash
# Step 1 — Generate the clean baseline dataset
python3 01_data_quality/src/generate_synthetic_data.py \
    --rows 15000 --seed 42 \
    --out 01_data_quality/data/raw/ugro_msme_clean.csv

# Step 2 — Inject quality issues and log every change
python3 01_data_quality/src/inject_quality_issues.py \
    --in 01_data_quality/data/raw/ugro_msme_clean.csv \
    --out 01_data_quality/data/raw/ugro_msme_dirty.csv \
    --log 01_data_quality/reports/injected_issues_log.csv \
    --seed 42

# Step 3 — Run Great Expectations validation suite
python3 01_data_quality/src/run_validation.py \
    --data 01_data_quality/data/raw/ugro_msme_dirty.csv \
    --out 01_data_quality/reports/validation_results.json

# Step 4 — Calculate per-dimension scorecard
python3 01_data_quality/src/dq_scorecard.py \
    --log 01_data_quality/reports/injected_issues_log.csv \
    --results 01_data_quality/reports/validation_results.json \
    --out 01_data_quality/reports/dq_scorecard.csv

# Step 5 — Generate PDF report
python3 01_data_quality/src/generate_dq_report.py \
    --scorecard 01_data_quality/reports/dq_scorecard.csv \
    --out 01_data_quality/reports/dq_assessment_report.pdf
```

---

## Key Findings

**Completeness is the weakest dimension (score: 91.2/100)**
8.83% of records had missing values, concentrated in bank statement and GST
fields. This is the highest violation rate across all six dimensions and the
most operationally significant — missing model inputs mean underwriting
decisions are made on incomplete information.

**The validation suite achieved 94.3% recall**
Of 2,370 deliberately injected issues, the Great Expectations suite detected
94.3%. This is a measured, verifiable number — not a claim. The 5.7% it missed
consists of two issue types documented below.

**Two known gaps remain**
Decimal shift errors on interest rates (e.g. 1800 instead of 18.00) inject at
a rate just below our detection threshold — a threshold calibration issue, not
a missing check. Cross-field date consistency (GST registration after application
date) requires comparing two columns simultaneously, which standard GE
expectations cannot do without a custom implementation.

---

## What This Module Demonstrates

This module demonstrates that data quality governance is not just about running
automated checks — it is about designing a measurement framework that lets you
know how trustworthy your checks are. The ground-truth methodology, threshold
calibration analysis, and per-dimension scoring show the kind of structured,
defensible thinking that distinguishes a governance analyst from someone who
simply ran a tool and reported its output.

The translation of every technical finding into a business risk statement in the
PDF report demonstrates the communication skill that governance roles require:
the ability to explain what a data problem means for the business, not just
what it looks like in the data.

---

## Disclaimer

This module is part of an independent portfolio project. It is not affiliated
with or commissioned by UGRO Capital Limited. All data is synthetic. See the
project-level disclaimer at `docs/disclaimer.md`.
