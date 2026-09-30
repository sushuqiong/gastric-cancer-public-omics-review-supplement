#!/usr/bin/env python3
"""Second round of v14 revisions."""
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

# 1. Section 4.7: point to full-text-verified S5 + corrected narrative
rep(
 "A detailed comparison of prognostic signature themes and quality dimensions is provided as Supplementary Table S5.",
 "Prognostic signature studies are compared in Supplementary Table S5, which records the development cohort, validation design, endpoint, and reported performance assessment for each study as verified against the full text of the cited article. That table shows that validation designs differ substantially within this literature: some studies perform external validation in independent GEO cohorts, one performs validation only through a random training/testing split of the same TCGA cohort, and one uses a single-institution discovery and validation cohort rather than TCGA. Comparisons of validation quality should therefore be made at the level of individual study designs rather than by theme.",
 "Section 4.7: point to full-text-verified S5 with corrected narrative")

# 2. Figure 2 explicitness (Reviewer 1 #6)
rep(
 "This generic workflow is summarized in Figure 2, and the main failure modes are shown in Figure 3.",
 "This generic workflow is summarized in Figure 2, which also shows the decision points that determine whether the analysis remains interpretable. Three of these points are worth stating explicitly. First, development and validation data should be separated at the patient level, not at the sample or cell level, so that no individual contributes to both. Second, any data-dependent transformation, including normalization parameters, batch correction, imputation, and feature scaling, should be estimated on the training data and then applied unchanged to validation data; where model selection is performed, tuning should use nested resampling within the training data. Third, an untouched external validation, in which the locked model is applied to a new cohort, should be distinguished from subsequent recalibration or model updating, which uses the validation data and therefore no longer constitutes an external test. Biological interpretation and functional experiments are not compulsory stages for every prognostic model; their role depends on the intended claim and should be linked to it explicitly. The main failure modes addressed by these points are shown in Figure 3.",
 "Section 4.2: explicit Figure 2 methodological guidance")

# 3. Box 1 item 7: split ceRNA / WGCNA / cell-cell communication
rep(
 "7. Immune, competing endogenous RNA (ceRNA), weighted gene co-expression network analysis (WGCNA), or cell-cell communication outputs interpreted as mechanisms without orthogonal evidence.",
 "7. Co-expression modules from weighted gene co-expression network analysis (WGCNA) interpreted as regulatory mechanisms without independent replication.\n8. Competing endogenous RNA (ceRNA) networks interpreted as established regulation without direct binding, stoichiometry, or perturbation evidence.\n9. Cell-cell communication inferred from ligand-receptor co-expression and interpreted as measured signaling.\n10. Immune or stromal deconvolution estimates interpreted as immune function.",
 "Box 1: split item 7 into distinct red flags")

# renumber remaining Box 1 items (old 8,9,10 -> 11,12,13)
rep("8. Single-cell or spatial data used illustratively rather than inferentially, without source attribution or tissue-level validation.",
    "11. Single-cell or spatial data used illustratively rather than inferentially, without source attribution or tissue-level validation.",
    "Box 1: renumber item 8 -> 11")
rep("9. No code, package versions, model formula, coefficients, feature list, or random seed.",
    "12. No code, package versions, model formula, coefficients, feature list, or random seed.",
    "Box 1: renumber item 9 -> 12")
rep("10. Conclusions imply clinical utility despite retrospective public-data evidence only.",
    "13. Conclusions imply clinical utility despite retrospective public-data evidence only.",
    "Box 1: renumber item 10 -> 13")
rep("## Box 1. Ten Red Flags in Public-Omics Manuscripts",
    "## Box 1. Thirteen Red Flags in Public-Omics Manuscripts",
    "Box 1: rename title to Thirteen Red Flags")

# 4. Table 1 dagger footnote -> remove dagger (no marker in table)
rep("† Abbreviations: TCGA-STAD, The Cancer Genome Atlas stomach adenocarcinoma cohort;",
    "Note. Abbreviations: TCGA-STAD, The Cancer Genome Atlas stomach adenocarcinoma cohort;",
    "Table 1: replace dagger with 'Note.'")

# 5. Table 2 dagger footnote -> 'Note.'
rep("† Abbreviations: AI, artificial intelligence; CAF, cancer-associated fibroblast;",
    "Note. Abbreviations: AI, artificial intelligence; CAF, cancer-associated fibroblast;",
    "Table 2: replace dagger with 'Note.'")

# 6. Table 3 dagger -> 'Note.'
rep("† Abbreviations: AUC, area under the receiver operating characteristic curve;",
    "Note. Abbreviations: AUC, area under the receiver operating characteristic curve;",
    "Table 3: replace dagger with 'Note.'")

# 7. Table 4 footnote: reconcile rows 1-5 and 6-8 wording with actual 8 rows
rep("† This is a practical appraisal guide, not a validated scoring scale. Categories (Low / Partial / Preferred) are intended as directional guidance for authors and reviewers, not as formal quality metrics. Rows 1-5 are the core GC-PROVE domains; rows 6-8 operationalize prediction-model, high-resolution omics, and reproducibility appraisal.",
    "Note. This is a practical appraisal guide, not a validated scoring scale. Categories (Low / Partial / Preferred) are intended as directional guidance for authors and reviewers, not as formal quality metrics. The first five rows are the core GC-PROVE domains (problem anchoring, resource provenance, omics workflow transparency, validation hierarchy, and evidence restraint). The final three rows extend the same appraisal to prediction-model rigor, high-resolution omics rigor, and reproducibility.",
    "Table 4: reconcile footnote with the eight rows actually present")

# 8. Section 7 reference to "rows 6-8 of Table 4" -> consistent wording
rep("Its five core domains (rows 1-5 of Table 4) address problem anchoring, resource provenance, workflow transparency, validation hierarchy, and evidence restraint; rows 6-8 extend the appraisal to prediction-model rigor, high-resolution omics quality, and reproducibility.",
    "Its five core domains (the first five rows of Table 4) address problem anchoring, resource provenance, workflow transparency, validation hierarchy, and evidence restraint; the final three rows extend the appraisal to prediction-model rigor, high-resolution omics quality, and reproducibility.",
    "Section 7: consistent Table 4 row description")

# 9. Table 2 header check: the source already uses 'Study or resource'
if "| Study or resource | Data/resource type |" not in md:
    rep("| Resource or platform | Data/resource type |", "| Study or resource | Data/resource type |",
        "Table 2: rename first column header")
else:
    log.append("OK   Table 2 header already 'Study or resource'")

# 10. Terminology: 'external-validation language' already reframed; check others
n2 = md.count("external-validation language")
if n2:
    md = md.replace("external-validation language", "external-validation mentions")
    log.append(f"OK   replaced {n2} residual 'external-validation language'")

# 11. Consistent hyphenation: 'public omics' -> 'public-omics' when adjectival (careful)
# leave noun usages; targeted fixes only
rep("Public omics resources have changed", "Public-omics resources have changed", "hyphenation: public-omics resources")
rep("public omics data are now widely reused", "public-omics data are now widely reused", "hyphenation: public-omics data (abstract)")
rep("Public omics data are now widely reused", "Public-omics data are now widely reused", "hyphenation: abstract opening")

md = re.sub(r"\n{4,}", "\n\n\n", md)
MD.write_text(md, encoding="utf-8")

print("=== ROUND 2 LOG ===")
for l in log:
    print(" ", l)
print(f"\nFinal size: {len(md)} chars")
