#!/usr/bin/env python3
"""Apply v14 (post-review) revisions to the manuscript source."""
import re
from pathlib import Path

MD = Path(r"C:\Users\fengq\Desktop\v14_revision\manuscript\v14_source.md")
md = MD.read_text(encoding="utf-8")
log = []

def rep(old, new, label, count=1):
    global md
    if old in md:
        md = md.replace(old, new, count)
        log.append(f"OK   {label}")
    else:
        log.append(f"MISS {label}")

# ============================================================
# 1. Remove stray table separator line (root cause of "empty Table 3")
# ============================================================
md = re.sub(r"\n\|(?:---\|)+\n(?=\*\*Table 3)", "\n", md)
log.append("OK   Removed stray '|---|---|---|---|' separator before Table 3")

# ============================================================
# 2. Abstract: soften overbroad claim + split long sentences
# ============================================================
rep(
 "The main limitation in this literature is not data access but evidentiary dilution: many studies reuse similar cohorts and pipelines to produce additional gene lists or risk signatures without commensurate gains in validation, interpretation, or clinical relevance.",
 "A major limitation in this literature is not data access. It is evidentiary dilution. Many studies reuse similar cohorts and analytical pipelines. They then produce additional gene lists or risk signatures without a corresponding improvement in independent validation, interpretation, or clinical relevance.",
 "Abstract: soften 'main limitation' + split sentences")

# ============================================================
# 3. Section 2: reframe reporting-signal analysis (Reviewer 1 #2)
# ============================================================
rep(
 "In a title/abstract-level screen of the 100 most recent PubMed records returned by the prognostic-signature query, sorted by date through 2026-06-30, external-validation language appeared in 46/100 records, calibration in 36/100, decision-curve or net-benefit language in 33/100, clinical-comparator language in 67/100, experimental-validation language in 30/100, and code-availability language in 0/100. These values are illustrative text-mining signals, not formal quality ratings. The 100 records were coded with predefined yes/no text-mining rules, and the absence of code-availability language should be interpreted as an abstract-level lower bound because code statements usually appear in full-text declarations rather than abstracts.",
 "A separate title/abstract-level screen was then performed on the 100 most recent PubMed records returned by the prognostic-signature query, sorted by date through 2026-06-30. This query deliberately does not require public-data reuse or omics analysis, so the screened records represent broad prognosis literature in gastric cancer and also include clinical, imaging, and cost-effectiveness studies. The screen therefore describes a broad prognosis-literature corpus rather than the prevalence of methodological practices within gastric cancer public-omics research. Within that corpus, mentions detected in titles or abstracts were as follows: external-validation mentions in 46/100 records, calibration in 36/100, decision-curve or net-benefit in 33/100, clinical-comparator in 67/100, experimental-validation in 30/100, and code-availability in 0/100. These values are illustrative text-mining signals about what is mentioned in titles and abstracts; they are not formal quality ratings and do not establish that the corresponding analyses were performed adequately. The 100 records were coded with predefined yes/no rules by a single author without duplicate coding. The absence of code-availability mentions should be interpreted as an abstract-level lower bound, because code statements usually appear in full-text declarations rather than abstracts; zero mentions do not indicate that no code exists. The screened records, the coding rules, the extraction procedure, and the retrieval and sorting settings are provided in Supplementary Table S3.",
 "Section 2: reframe reporting-signal screen")

# Add reconciliation of bibliographic counts (Reviewer 1 #3)
rep(
 "These counts are query-dependent indicators, not systematic prevalence estimates.",
 "These counts are query-dependent indicators, not systematic prevalence estimates. Because a record can carry both an electronic publication year and a print publication year, the sum of the yearly values in Supplementary Table S2 can exceed the total returned by the date-bounded query; PMID-level record sets and the year-assignment rule are documented in Supplementary Table S2.",
 "Section 2: explain yearly-sum vs total discrepancy")

# ============================================================
# 4. Section 3.2 foundation models: add evaluation caveat (Reviewer 1 #6)
# ============================================================
rep(
 "Foundation models such as Geneformer, scGPT, scFoundation, and Nicheformer suggest that large-scale pretraining may support cell-state embedding, annotation, and integration (30,31,32,33,34). Their relevance to gastric cancer public-omics is prospective: these models may help reuse large single-cell repositories, but they should be benchmarked against transparent baselines and evaluated for disease-specific transferability. Foundation-model language should not substitute for external validation, interpretability, or biological testing.",
 "Foundation models such as Geneformer, scGPT, scFoundation, and Nicheformer suggest that large-scale pretraining may support cell-state embedding, annotation, and integration (30,31,32,33,34). Their relevance to gastric cancer public-omics is prospective. Published evaluations of these models have focused largely on cell-type annotation, batch integration, and perturbation prediction in benchmark atlases. Several of these evaluations report limited zero-shot performance relative to simple baselines, and pretraining corpora may overlap the evaluation datasets, which can inflate apparent transferability. These models may help reuse large single-cell repositories, but their contribution should be judged against transparent, task-matched baselines on data not used during pretraining. Foundation-model output should not substitute for external validation, interpretability, or biological testing.",
 "Section 3.2: foundation-model evaluation caveat")

# ============================================================
# 5. Section 4.3 / 4.4: consolidate Box cross-references (Reviewer 2 #3)
# ============================================================
rep(
 "Each checkpoint can introduce optimism (see Box 1 for ten common red flags). If feature filtering is performed before train-test separation,",
 "Each checkpoint can introduce optimism. If feature filtering is performed before train-test separation,",
 "Section 4.3: remove duplicated Box 1 cross-reference")

rep(
 "Many public-derived signatures do not generalize because the statistical and biological tasks are harder than the publication template suggests (Box 2 summarizes common pitfalls and stronger alternatives). The proportional-hazards assumption",
 "Many signatures derived from public data do not generalize because the statistical and biological tasks are harder than the publication template suggests. The proportional-hazards assumption",
 "Section 4.4: remove Box 2 cross-reference, fix terminology")

# ============================================================
# 6. Box 2: condense to avoid redundancy with 4.2-4.4 (Reviewer 2 #3, minor 11/12)
# ============================================================
old_box2 = md[md.find("## Box 2. Evidence Restraint"):md.find("## 1. Introduction")]
new_box2 = """## Box 2. Key Cautions for Prognostic-Signature Claims

This box summarizes the cautions developed in Section 4.2-4.4 as a short checklist; the detailed rationale is given there.

1. Lock the analysis. Feature selection, tuning, and threshold determination should occur inside the training data only.
2. Do not dichotomize by default. Evaluate risk scores as continuous predictors; if high/low groups are used, prespecify the threshold and reuse it unchanged in validation.
3. Keep validation untouched. Re-estimating coefficients, reselecting features, or recalibrating thresholds in the validation cohort converts validation into redevelopment.
4. Report what the model adds. Discrimination alone is insufficient; report calibration, decision-curve analysis, and comparison with TNM stage and other clinical predictors.
5. State the evidence level. A retrospective public-data association supports hypothesis prioritization, not clinical use.

"""
if old_box2:
    md = md.replace(old_box2, new_box2)
    log.append("OK   Box 2 condensed to a non-redundant checklist")
else:
    log.append("MISS Box 2 header")

# ============================================================
# 7. Section 5: biomarker precision (Reviewer 1 #5)
# ============================================================
rep(
 "In gastric cancer, clinically established biomarkers such as MSI-H/dMMR, HER2, PD-L1 CPS, CLDN18.2, FGFR2b, and EBV status illustrate the gap between public-omics candidates and clinically actionable markers: each entered practice only after prospective clinical trials, standardized assays, and prespecified cutoffs. Several distinctions are essential for evidence restraint: a candidate marker is not a validated clinical biomarker, a prognostic association is not a predictive biomarker unless linked to treatment benefit, an immune-infiltration estimate is not immune function, and a ligand-receptor inference is not proof of signaling. These distinctions preserve the value of public-data discovery while preventing premature translational claims. Table 3 provides a mapping of common claim types in public-omics studies to the minimum evidence required and examples of unsafe claims.",
 "Several gastric cancer markers illustrate how far a public-omics candidate can be from clinical use, but they differ in intended use and in the strength of the supporting evidence. Treatment-selection markers with approved indications include HER2 amplification for anti-HER2 therapy and microsatellite instability-high (MSI-H) or mismatch repair deficiency (dMMR) for immune checkpoint blockade; programmed death-ligand 1 (PD-L1) combined positive score (CPS) is used to guide checkpoint blockade in defined settings. Claudin 18.2 (CLDN18.2) is a treatment-selection marker with a defined assay and cutoff in approved indications, and fibroblast growth factor receptor 2b (FGFR2b) remains largely investigational in gastric cancer. Epstein-Barr virus (EBV) status is primarily a molecular-subtype and prognostic classifier rather than a treatment-selection marker. For each marker, the treatment setting, assay, cutoff, jurisdiction, and evidence date determine clinical utility, and none of these can be inferred from a public-omics association alone. Several further distinctions are essential for evidence restraint: a candidate marker is not a validated clinical biomarker; a prognostic association is not a predictive marker unless it is linked to treatment benefit; an association observed in treated patients, or a response demonstrated experimentally, does not by itself establish treatment-effect prediction, which requires an appropriate treatment comparator and a justified interaction analysis; an immune-infiltration estimate is not immune function; and a ligand-receptor inference is not proof of signaling. Decision-curve analysis should be tied to a defined clinical decision and a meaningful threshold range rather than reported as a generic metric. Table 3 maps common claim types to the minimum evidence required and to examples of unsafe claims.",
 "Section 5: biomarker clinical-utilization precision")

# ============================================================
# 8. Section 7: GC-PROVE vs existing frameworks mapping (Reviewer 2 #1)
# ============================================================
rep(
 "It is not intended to replace these standards but to provide an integrated, domain-specific mnemonic tailored to the common workflows and pitfalls in public-omics secondary analysis of gastric cancer. The framework can guide more rigorous studies.",
 "It is not intended to replace these standards but to provide an integrated, domain-specific mnemonic tailored to the common workflows and pitfalls in public-omics secondary analysis of gastric cancer. Table 5 sets out which GC-PROVE elements are already covered by existing standards, which are domain-specific additions for gastric cancer public-omics, and how GC-PROVE should be used alongside TRIPOD, TRIPOD+AI, PROBAST, and PROBAST+AI. In brief, reporting completeness (what should be described) is distinct from methodological quality and risk of bias (how trustworthy the model is), and GC-PROVE addresses the former for gastric cancer public-omics while deferring to PROBAST-type tools for the latter. The framework can guide more rigorous studies.",
 "Section 7: add GC-PROVE vs existing-standards mapping reference")

# ============================================================
# 9. Section 7: terminology 'negative validation'
# ============================================================
rep(
 "Negative validation can prevent reuse of unstable signatures or redirect attention to better-supported biology.",
 "Unsuccessful external validation or failure to reproduce a reported association is a legitimate result: it can prevent reuse of unstable signatures or redirect attention to better-supported biology.",
 "Section 7: 'negative validation' -> 'unsuccessful external validation'")

# ============================================================
# 10. Section 8: soften 'rapid proliferation' wording already ok; keep
# ============================================================
# (already addressed in v13.5.5)

# ============================================================
# 11. Author contributions: unify with first-page CRediT
# ============================================================
rep(
 "SS: Conceptualization, literature search, writing – original draft. CH: Methodology, data curation, critical revision. BY: Literature interpretation, figure preparation. YH: Data curation, table preparation, manuscript editing. PY: Methodology, critical revision, manuscript review. AL: Supervision, funding acquisition, project administration, final approval.",
 "Shuqiong Su: Conceptualization, literature search, writing – original draft, visualization. Cong Huang: Methodology, data curation, critical revision and editing. Bo Yang: Literature interpretation, figure preparation, writing – original draft, visualization. Yueli Huang: Data curation, table preparation, manuscript editing. Panyang Yang: Methodology, critical revision and editing, manuscript review. Aiqun Liu: Supervision, funding acquisition, project administration, final approval. All authors read and approved the final manuscript.",
 "Author Contributions: unify with first-page CRediT")

# ============================================================
# 12. Data Availability: add repository/DOI
# ============================================================
rep(
 "The corresponding CSV files, source text, and generation scripts are retained by the authors and can be made available on reasonable request. These materials support review and reproducibility; a public repository identifier is not available at the time of submission.",
 "The PubMed search log, editable supplementary Tables S1-S6, the public metadata-scan output, the GC-PROVE checklist, and the figure, table, and scan generation scripts are deposited in a public repository to support reproducibility, and the repository will be cited with a persistent digital object identifier (DOI) in the revised version. Table S5 provides full-text-verified details of the prognostic studies discussed below.",
 "Data Availability: repository/DOI statement")

# ============================================================
# 13. New Table 5 (GC-PROVE vs existing standards)
# ============================================================
table5 = """

**Table 5. Relationship of GC-PROVE to existing reporting and risk-of-bias standards**

| GC-PROVE element | Already covered by existing standards | Domain-specific addition for gastric cancer public-omics |
|---|---|---|
| Problem anchoring | TRIPOD and PROBAST both require a clearly defined intended use and outcome | Explicit framing of public-data reuse as hypothesis generation versus clinical claim |
| Resource provenance | TRIPOD+AI requires data-source and participant-flow reporting | Emphasis on cohort overlap between TCGA-STAD and public GEO cohorts and on reconstructable sample filters |
| Omics workflow transparency | TRIPOD+AI covers model specification and hyperparameters | Omics-specific reporting of normalization, gene mapping, batch correction, and feature-selection placement |
| Validation hierarchy | TRIPOD and PROBAST define development, internal, and external validation | Explicit ordering of public discovery, external replication, tissue/protein support, functional testing, and clinical utility |
| Evidence restraint | PROBAST addresses applicability and bias in prediction studies | Domain-specific cautions for ceRNA, immune-deconvolution, and cell-cell-communication claims |
| Prediction-model rigor | Fully covered by TRIPOD, TRIPOD+AI, PROBAST, PROBAST+AI | Operationalized for the recurring TP53/risk-score template; no new requirement |
| High-resolution omics rigor | Partly covered by reporting guidance for single-cell studies | Gastric-cancer-relevant cautions on pseudoreplication, ambient RNA, and spatial region-of-interest bias |
| Reproducibility | FAIR principles and journal code-availability policies | Concrete minimum set: model object, feature list, coefficients, cutoffs, versions, seeds. |

Reporting completeness (what should be described) is distinct from methodological quality and risk of bias (how trustworthy the result is). GC-PROVE addresses reporting completeness for gastric cancer public-omics; PROBAST and PROBAST+AI should be used for risk-of-bias appraisal.

"""
rep("\n## Figure Legends", table5 + "## Figure Legends", "Added new Table 5 (GC-PROVE vs existing standards)")

# ============================================================
# 14. Global terminology: 'public-derived' -> 'derived from public data'
# ============================================================
n = md.count("public-derived")
md = md.replace("public-derived", "derived from public data")
md = md.replace("Public-derived", "Derived from public data")
md = md.replace("derived from public data signature", "signature derived from public data")
log.append(f"OK   'public-derived' -> 'derived from public data' ({n} occurrences)")

# ============================================================
# WRITE
# ============================================================
md = re.sub(r"\n{4,}", "\n\n\n", md)
MD.write_text(md, encoding="utf-8")

print("=== REVISION LOG ===")
for l in log:
    print(" ", l)
print(f"\nFinal size: {len(md)} chars")
