#!/usr/bin/env python3
"""Round 3: worked example + core search strings + abbreviation fixes."""
import re
from pathlib import Path

MD = Path(r"C:\Users\fengq\Desktop\v14_revision\manuscript\v14_source.md")
md = MD.read_text(encoding="utf-8")
log = []

def rep(old, new, label, count=1):
    global md
    if old in md:
        md = md.replace(old, new, count); log.append(f"OK   {label}")
    else: log.append(f"MISS {label}")

# 1. Core search strings in main text (Reviewer 2 major 4)
rep(
 "Searches covered 2019-01-01 through 2026-06-30. The complete search strings and PubMed QueryTranslation outputs are provided in Supplementary File S1, and the search counts are provided in Supplementary Table S1.",
 "Searches covered 2019-01-01 through 2026-06-30. The core search strings are: (gastric cancer[Title/Abstract] OR stomach adenocarcinoma[Title/Abstract] OR stomach cancer[Title/Abstract]) AND (TCGA[Title/Abstract] OR GEO[Title/Abstract] OR public database[Title/Abstract] OR public datasets[Title/Abstract] OR bioinformatics[Title/Abstract] OR secondary analysis[Title/Abstract] OR transcriptome[Title/Abstract]); a second query replaced the second bracket with (risk signature[Title/Abstract] OR prognostic signature[Title/Abstract] OR prognostic model[Title/Abstract] OR nomogram[Title/Abstract] OR survival model[Title/Abstract]); parallel queries used single-cell, spatial omics, machine-learning, and reproducibility terms. The complete search strings, PubMed QueryTranslation outputs, retrieval dates, and sorting settings are provided in Supplementary File S1, and the search counts are provided in Supplementary Table S1.",
 "Section 2: core search strings in main text")

# 2. GC-PROVE worked example with two contrasting studies (Reviewer 1 #4)
rep(
 "Hypothesis prioritization is itself a legitimate endpoint when it is stated explicitly and kept within the evidence available.",
 """Hypothesis prioritization is itself a legitimate endpoint when it is stated explicitly and kept within the evidence available.

Two published studies illustrate how GC-PROVE produces traceable judgements, and they were selected because their validation designs contrast sharply and are documented against their full texts in Supplementary Table S5. The first study (Chang 2023, reference 37) anchors a mitochondrial-gene risk score to a stated biological question, reports a locked LASSO-Cox formula, applies it to two independent external cohorts (GSE66229 and GSE15459), and reports calibration and decision-curve analysis; under GC-PROVE it scores favourably on resource provenance, workflow transparency, validation hierarchy, and prediction-model rigor. Its main residual limitation is that the model is not compared against a molecular subtype or a full clinical model, which limits the claim to a candidate prognostic stratification rather than demonstrated incremental utility. The second study (Jiang 2025, reference 42) also defines a clear question and reports calibration and decision-curve analysis, but its validation is a random training/testing split of the same TCGA cohort rather than an independent cohort. Under GC-PROVE this design places the work at the discovery end of the validation hierarchy, and the appropriate claim is hypothesis prioritization rather than external validation. The two entries differ only in their documented design features, showing that GC-PROVE judgements can be traced to specific reported evidence rather than to an overall impression.""",
 "Section 7: GC-PROVE worked example (two contrasting studies)")

# 3. TNM expansion at first use
n = 0
if "TNM stage and other clinical predictors" in md:
    md = md.replace("TNM stage and other clinical predictors",
                    "tumour-node-metastasis (TNM) stage and other clinical predictors", 1)
    n += 1
if "beyond TNM stage" in md:
    md = md.replace("beyond TNM stage", "beyond tumour-node-metastasis (TNM) stage", 1)
    n += 1
log.append(f"OK   TNM expanded at first use ({n} edits)")

# 4. Verify LASSO/AUC expansions exist
log.append(("OK   LASSO expanded" if "least absolute shrinkage and selection operator (LASSO)" in md else "MISS LASSO expansion"))
log.append(("OK   AUC expanded" if "area under the receiver operating characteristic curve (AUC)" in md else "MISS AUC expansion"))
log.append(("OK   MSI-H/dMMR expanded" if "microsatellite instability-high (MSI-H)" in md else "MISS MSI-H expansion"))

md = re.sub(r"\n{4,}", "\n\n\n", md)
MD.write_text(md, encoding="utf-8")
print("=== ROUND 3 LOG ===")
for l in log: print(" ", l)
print(f"Final: {len(md)} chars")
