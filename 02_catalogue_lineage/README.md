# Module 2 — Data Catalogue and Lineage

## What This Module Is About

Module 1 asked "is the data good?" Module 2 asks a different but
equally important governance question: do we know what data we have,
where it came from, and what it means?

This sounds obvious but in practice most financial organisations
fail it badly. Data scientists build models using fields whose
business definitions they have never formally confirmed. Compliance
teams cannot answer regulators' questions about what data was used
in a credit decision. New employees spend weeks figuring out what
a column actually means. A data catalogue fixes all of this by
creating a single, trusted source of documentation for every data
asset in the organisation.

This module builds a complete data catalogue for UGRO Capital's
GRO Score 3.0 data ecosystem — covering the four source systems
UGRO publicly discloses (Loan Origination System, Credit Bureau
feed, Bank Statement Analyzer, GSTN API), the derived Feature Store,
and the model output itself.

---

## Why These Four Deliverables

**Data Asset Inventory** — before you can catalogue anything, you
need to know what exists. The inventory formally documents each
system: what it is, who owns it, what fields it contains, what
downstream systems consume it, and what regulations govern it.
This is the foundation everything else builds on.

**Business Glossary** — a data asset inventory tells you what
systems exist. A business glossary tells you what the words mean.
Without formally defined terms, "bureau score" means something
slightly different to every person who uses it. The glossary
eliminates that ambiguity permanently — one definition, one source
of truth, agreed by both business and technical teams.

**Data Lineage Map** — documents how data flows from raw source
to credit decision. Answers the question: if the GSTN API changes
its data format, which downstream models and decisions are affected?
Also answers the regulator's question: what data was used to make
this lending decision, and where did it come from?

**Data Classification Policy** — assigns every data field to one
of four sensitivity tiers (Public, Internal, Confidential,
Restricted) and defines what handling rules apply to each tier.
This is the foundational document that DPDP Act compliance builds
on — you cannot protect data you have not classified.

---

## Deliverables

| File | What It Contains |
|---|---|
| `catalogue/data_assets.json` | Structured inventory of 6 data assets from LOS through GRO Score model output |
| `glossary/business_glossary.json` | 34 defined terms across credit risk, MSME business, data, and regulatory categories |
| `glossary/business_glossary.csv` | Same glossary in CSV format for easy viewing |
| `lineage/gro_score_lineage.md` | Mermaid flowchart tracing every field from source to credit decision |
| `policies/data_classification_policy.md` | 4-tier classification policy with field-level register for all 35 dataset columns |

---

## How to Run

```bash
cd ~/Desktop/gro-shield-ugro-governance

# Build data asset inventory
python3 02_catalogue_lineage/src/build_asset_inventory.py

# Build business glossary
python3 02_catalogue_lineage/src/build_glossary.py
```

The lineage map and classification policy are static documents —
they do not require running a script. View the lineage diagram
by navigating to `lineage/gro_score_lineage.md` on GitHub, where
it renders as a visual Mermaid flowchart.

---

## The Data Pipeline in Plain English

A loan application triggers three simultaneous external data pulls:
credit bureau data (CIBIL/Experian), bank statement data (via
Account Aggregator), and GST data (via GSTN API). All three feeds
flow into a Feature Engineering Pipeline that produces 25,000+
engineered features. Those features are scored by GRO Score 3.0,
which outputs a credit decision. The full chain:
---

## Key Findings

**All 35 dataset fields formally classified** — 18 fields are
Restricted (personal financial data subject to DPDP Act), 9 are
Confidential (business financial data), and 8 are Internal
(operational metadata). Zero fields are Public — consistent with
UGRO Capital operating exclusively in sensitive personal and
financial data categories.

**Lineage opacity is a governance risk** — UGRO Capital publicly
discloses the three source data categories but not the specific
feature engineering logic applied in the Feature Store. With
25,000+ features, the inability to trace individual model inputs
back to their source makes independent model risk assessment
difficult and limits the explainability of credit decisions.

**proprietor_gender requires special governance attention** —
classified as Restricted because it is a personal characteristic
of an individual. Its presence as a model feature also raises
potential indirect discrimination concerns assessed in Module 5's
bias audit.

---

## Note on DataHub

This module was designed to be deployed on DataHub — an
open-source enterprise data catalogue platform. A Docker Compose
configuration for DataHub deployment is documented below for
reference. Due to local resource constraints (8GB RAM), the
catalogue was implemented as structured Python and JSON outputs
rather than a live DataHub instance. The metadata schema used
here is compatible with DataHub's ingestion API and could be
pushed to a DataHub instance with minimal modification.

DataHub quickstart (requires 16GB+ RAM):
```bash
pip install acryl-datahub
datahub docker quickstart
```

---

## What This Module Demonstrates

This module demonstrates that data governance is not only about
technology — it is about creating shared understanding. The
business glossary, lineage map, and classification policy are
artifacts that bridge the gap between technical teams who build
models and business teams who are accountable for them. A
regulator asking "what personal data do you process and for what
purpose" can be answered precisely and immediately from these
documents.

The field-level classification register also demonstrates the
kind of systematic, row-by-row analysis that DPDP Act compliance
actually requires — not a high-level claim that "we protect
personal data," but a documented decision for every single field
explaining why it was classified as it was.

---

## Disclaimer

This module is part of an independent portfolio project. It is
not affiliated with or commissioned by UGRO Capital Limited.
All catalogue entries are based on publicly available information
about UGRO Capital's disclosed data practices. See
`docs/disclaimer.md`.
