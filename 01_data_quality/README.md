# Module 1 — Data Quality Assessment

## Dataset Versioning Note

**Dataset v2** was regenerated during Module 4 (Model Risk Management) development.

### What changed
The `default_flag` generation formula in `generate_synthetic_data.py` was
strengthened to produce a more realistic credit signal for XGBoost training:

| Parameter | v1 (original) | v2 (current) |
|-----------|--------------|--------------|
| bureau_score divisor | 1500 | 400 |
| dpd_90_count_12m coefficient | 0.06 | 0.12 |
| write_off_flag term | not included | +0.15 |
| bounce_count_6m term | not included | +0.015 |

Diagnostic analysis on v1 showed AUC-ROC of 0.55 (near-random), confirming
the original formula produced insufficient signal for model training.

### What did NOT change
- All 35 column definitions and data types (schema.py unchanged)
- All quality issues injection logic (inject_quality_issues.py unchanged)
- Random seed (seed=42 throughout)
- Row count (15,000 rows)
- loan_status distribution
- All non-default columns

### Why DQ findings remain valid
The Module 1 DQ assessment evaluated six data quality dimensions
(completeness, accuracy, consistency, timeliness, validity, uniqueness).
Quality issues were injected independently of the default_flag formula
via inject_quality_issues.py. No Great Expectations validation rule
tests default_flag values against a specific expected rate.

The 2,370 injected issues, 94.3% recall, and 97.4/100 DQ scorecard
are fully reproducible on v2 with seed=42.

### Regeneration commands
From project root with venv active:
```bash
cd 01_data_quality/src
python3 generate_synthetic_data.py
python3 inject_quality_issues.py
cd ../..
```
