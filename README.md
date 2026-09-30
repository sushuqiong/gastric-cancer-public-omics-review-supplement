# Supplementary material and reproducibility package

**Public Omics Data Reuse in Gastric Cancer: From Discovery Abundance to Translational Evidence**

This repository contains the supplementary material and reproducibility package for a
methodological narrative review on the reuse of public omics data in gastric cancer.

The review is not a systematic review. The PubMed-based scans included here are supportive
landscape evidence used to contextualize the narrative; they are not PRISMA systematic-review
products and should not be read as prevalence estimates for the field.

## Contents

### `data/` — tabular supplementary material

| File | Description |
|---|---|
| `Supplementary_Table_S1_pubmed_scan_counts.csv` | Record counts for each PubMed query topic. |
| `Supplementary_Table_S2_publication_trends.csv` | Yearly PubMed counts (2019–2026) with the year-assignment rule. Because a record may carry both an electronic and a print publication year, yearly sums can exceed the total returned by the date-bounded query. |
| `Supplementary_Table_S3_signature_reporting_signals.csv` | Title/abstract-level screen of the 100 most recent prognostic-signature records, with the screened records, coding rules, extraction procedure, retrieval date, and sorting settings. This is a broad prognosis-literature screen and not a measure of methodological prevalence in public-omics research. |
| `Supplementary_Table_S4_public_metadata_scan.csv` | Public metadata scan (OpenAlex, Crossref, Semantic Scholar). Fields are separated into PubMed indexing status, search-corpus membership, and topic eligibility, so that absence from the retrieved corpus is distinguished from absence in PubMed. |
| `Supplementary_Table_S5_prognostic_signature_comparison.csv` | Validation design of 11 representative prognostic-signature studies, **verified against the full text of each cited article** and linked to the PMID of each source. |
| `Supplementary_Table_S6_single_cell_spatial_comparison.csv` | Comparison of single-cell and spatial methods in gastric cancer. |

### `files/` — documents

| File | Description |
|---|---|
| `Supplementary_File_S1_pubmed_search_log.docx` | Complete PubMed search strings, QueryTranslation outputs, retrieval dates, and sorting settings. |
| `Supplementary_GC_PROVE_Checklist.docx` | GC-PROVE practical appraisal checklist. |

### `figures/`

| File | Description |
|---|---|
| `Supplementary_Figure_S1_publication_trends.pdf` | Publication-trend figure. |

### `scripts/`

Scripts used to generate the manuscript, tables, and figures from the source files.

## Note on Supplementary Table S5

Supplementary Table S5 was rebuilt during the first revision round after every cited study was
re-examined against its full text. Entries record the theme, development cohort, validation design,
endpoint, whether calibration and decision-curve analysis were reported, and the clinical
comparator. "Not reported" indicates that an item was not described in the cited article; it does
not establish that the analysis was not performed. Validation designs differ substantially across
these studies, so comparisons of validation quality should be made at the level of individual
study designs rather than by theme.

## Licensing

Text and data: CC BY 4.0 (see `LICENSE`).
Code in `scripts/`: MIT.

## Citation

See `CITATION.cff`. If you use this material, please cite the deposited record and the
accompanying article.
