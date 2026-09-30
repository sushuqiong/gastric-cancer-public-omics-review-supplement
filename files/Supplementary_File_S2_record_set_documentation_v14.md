# Supplementary File S2. Record-set documentation and year-assignment rule

Companion to Supplementary Table S2 (publication trends) and Supplementary File S2
(PMID-level record sets).

## 1. What is provided

| File | Content |
|---|---|
| `Supplementary_File_S2_pmid_list_public_omics_v14.csv` | Complete PMID list for the public-omics secondary-analysis topic query |
| `Supplementary_File_S2_pmid_list_prognostic_v14.csv` | Complete PMID list for the prognostic-signature/risk-model topic query |
| `Supplementary_File_S2_pmid_list_single_cell_v14.csv` | Complete PMID list for the single-cell topic query |
| `Supplementary_File_S2_pmid_list_spatial_v14.csv` | Complete PMID list for the spatial-omics topic query |
| `Supplementary_File_S2_pmid_list_ai_ml_v14.csv` | Complete PMID list for the AI/machine-learning topic query |
| `Supplementary_File_S2_record_set_summary_v14.csv` | Record counts and PMID-list sizes per topic |
| `Supplementary_Table_S2_publication_trends_v14.csv` | Yearly counts per topic |

The topic queries are given in full, together with their PubMed QueryTranslation outputs, in
Supplementary File S1.

## 2. Year-assignment rule (why yearly sums exceed the date-bounded total)

Each record was assigned a publication year using the following rule, applied in order:

1. If PubMed reports a print publication date (`PubStatus = ppublish`), that year is used.
2. If no print year is available, the year of the journal issue (`<PubDate>`) is used.
3. If neither is present, the electronic publication year (`PubStatus = epublish`) is used.

A record can therefore carry an electronic publication year and a print publication year that fall
in **different calendar years**. When the yearly series is built, such a record is counted in both
years, while the date-bounded topic query counts it exactly once. This is why the yearly values in
Supplementary Table S2 sum to more than the corresponding date-bounded total:

| Topic | Sum of yearly values | Date-bounded total | Difference |
|---|---|---|---|
| Prognostic signatures and risk models | 1,951 | 1,812 | +139 (7.7%) |
| Single-cell gastric cancer omics | 950 | 876 | +74 (8.4%) |
| Spatial omics in gastric cancer | 162 | 148 | +14 (9.5%) |
| AI and machine-learning public-omics prognosis | 690 | 636 | +54 (8.5%) |

The consistent magnitude of the excess across all four topics is consistent with dual year
assignment rather than a difference in query scope. The date-bounded total is the figure quoted in
the main text, because it counts each record once.

## 3. Indexing lag within a fixed date window

The date window (2019-01-01 to 2026-06-30) is fixed, but PubMed continues to add records whose
publication date falls inside it. Re-running the identical queries at the revision date therefore
retrieves slightly more records than at the original search date:

| Topic | At first submission | At revision re-run |
|---|---|---|
| Public omics secondary analysis in gastric cancer | 4,416 | 4,460 |
| Prognostic signatures and risk models | 1,812 | 1,840 |
| Single-cell gastric cancer omics | 876 | 904 |
| Spatial omics in gastric cancer | 148 | 159 |
| AI and machine-learning public-omics prognosis | 636 | 662 |

The counts reported in the manuscript are those captured at the original search date. The
PMID-level lists provided here are from the revision re-run and are complete for each topic. Both
sets are query-dependent indicators of literature volume, not systematic prevalence estimates.

## 4. Reproducing the record sets

Run each query from Supplementary File S1 against the PubMed E-utilities `esearch` endpoint with
`usehistory=y` and `retmax` set to the full count, then retrieve the PMID list. A script that
performs exactly this is provided in the deposited reproducibility package as
`fetch_pmid_sets.py`.
