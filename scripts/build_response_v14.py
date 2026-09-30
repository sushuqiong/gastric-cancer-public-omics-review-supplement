#!/usr/bin/env python3
"""Build the point-by-point response to reviewers (DOCX)."""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = Path(r"C:\Users\fengq\Desktop\Point_by_point_response_v14.docx")

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(11)
st.paragraph_format.space_after = Pt(6)
st.paragraph_format.line_spacing = 1.15


def H(text, level=1):
    p = doc.add_heading(text, level=level)
    for r in p.runs:
        r.font.color.rgb = RGBColor(0x1F, 0x3B, 0x63)
    return p


def P(text, bold=False, italic=False, indent=0.0):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if indent:
        p.paragraph_format.left_indent = Pt(indent)
    return p


def C(num, comment):
    """Comment block."""
    p = doc.add_paragraph()
    r = p.add_run(f"Comment {num}: ")
    r.bold = True
    r2 = p.add_run(comment)
    r2.italic = True
    p.paragraph_format.left_indent = Pt(12)
    p.paragraph_format.space_before = Pt(10)


def R(text):
    p = doc.add_paragraph()
    r = p.add_run("Response: ")
    r.bold = True
    p.add_run(text)
    p.paragraph_format.left_indent = Pt(12)


def CH(text):
    p = doc.add_paragraph()
    r = p.add_run("Changes made: ")
    r.bold = True
    r.font.color.rgb = RGBColor(0x1F, 0x3B, 0x63)
    p.add_run(text)
    p.paragraph_format.left_indent = Pt(12)


# ============================================================
# Header
# ============================================================
tp = doc.add_paragraph()
tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = tp.add_run("Response to Reviewers")
tr.bold = True
tr.font.size = Pt(16)

sp = doc.add_paragraph()
sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
sp.add_run("Manuscript: \u201cPublic Omics Data Reuse in Gastric Cancer: From Discovery Abundance to Translational Evidence\u201d").italic = True
jp = doc.add_paragraph()
jp.alignment = WD_ALIGN_PARAGRAPH.CENTER
jp.add_run("Journal: Frontiers | Article type: Review | Round: First revision (major revision)").italic = True

P("")
P("We thank the editor and both reviewers for their careful and constructive assessment. "
  "The comments identified several genuine errors in our data tables and several places where "
  "our wording and structure did not match the evidence we actually presented. We have revised "
  "the manuscript accordingly. The most substantive changes are: (i) a complete re-verification "
  "of every prognostic-signature study in Supplementary Table S5 against the full text of the "
  "cited article, which confirmed three cohort/design errors and led us to rebuild the table; "
  "(ii) a reframing of the title/abstract reporting-signal screen so that it is described as a "
  "broad prognosis-literature screen rather than a measure of methodological prevalence in "
  "public-omics research; (iii) a new table explicitly mapping GC-PROVE to TRIPOD, TRIPOD+AI, "
  "PROBAST, and PROBAST+AI; (iv) a rewritten biomarker interpretation in Section 5 that separates "
  "treatment-selection markers, investigational markers, and molecular-subtype classifiers; "
  "(v) correction of the table-numbering defect, which was traced to a stray markdown table "
  "separator that produced an empty table in the submitted PDF; and (vi) consolidation of "
  "redundant passages and a full terminology and abbreviation pass. All changes are marked in the "
  "revised manuscript, and every reviewer comment is addressed point by point below.")
P("")

# ============================================================
# REVIEWER 1
# ============================================================
H("Reviewer 1", 1)
P("The reviewer made eight major comments and four comments on the quality of English. "
  "We are grateful for the detailed reading, in particular for identifying the errors in the "
  "prognostic-signature comparison table.", italic=True)

H("Major comments", 2)

C("1.1", "In Section 4.7 and Supplementary Table S5, the comparison of published prognostic studies "
   "should be reconstructed because several descriptions do not agree with the original articles. "
   "For Chang et al., GSE26901 is listed although GSE66229 and GSE15459 are identified in the source. "
   "For Cai et al., the reported TCGA-to-GSE15459 design does not accurately represent the SYSUCC "
   "discovery and validation cohorts. For Jiang et al., GSE84437 is described as an external "
   "validation cohort although the evaluation uses training and testing subsets of TCGA.")
R("We fully accept this comment, and we thank the reviewer for the specific corrections. We had "
  "not re-opened the full texts of these papers when the table was first assembled, and the entries "
  "were inaccurate. We have now re-examined all 11 studies against their full texts (or, where the "
  "article is not open access, its abstract and indexed metadata), and we confirm each of the three "
  "errors identified. Chang 2023 validates in GSE66229 and GSE15459, and GSE26901 does not appear in "
  "that paper as a validation cohort. Cai 2024 uses a Sun Yat-sen University Cancer Center (SYSUCC) "
  "discovery cohort of 12 patients with paired peritoneal, primary, and normal tissue, and a SYSUCC "
  "validation cohort of 231 stage II-III patients, with an interactive analysis against TCGA; it does "
  "not use a TCGA-to-GSE15459 design. Jiang 2025 assigns patients randomly to a training set and a "
  "testing set within TCGA; it does not use GSE84437 as an external validation cohort. We also found "
  "and corrected further errors in four other entries (Zhu 2024, Li 2024, Yang 2025, and Yang 2025b), "
  "whose validation cohorts had also been recorded incorrectly.")
CH("Supplementary Table S5 has been rebuilt from the full texts. Each entry now records the theme, "
   "development cohort, validation design, endpoint, whether calibration and decision-curve analysis "
   "are reported, the clinical comparator, and the PubMed identifier of the source article. "
   "Information that is not reported is now distinguished from an analysis that was demonstrably not "
   "performed: the table uses \u201cNot reported\u201d rather than a negative mark. The narrative "
   "conclusion in Section 4.7 has been rewritten to state that validation designs differ substantially "
   "within this literature (external GEO validation, within-TCGA training/testing split, and "
   "single-institution discovery and validation) and that validation quality should therefore be "
   "assessed at the level of individual study designs rather than by theme. Supplementary citation "
   "numbers have been aligned with the main reference list.")

C("1.2", "In Section 2 and Supplementary Table S3, the reporting-signal analysis should be aligned "
   "with the population that the review intends to describe. The current prognosis query does not "
   "require public-data reuse or omics analysis\u2026 Consequently, the reported frequencies cannot be "
   "interpreted directly as the prevalence of methodological practices in gastric cancer public-omics "
   "research.")
R("We agree. The prognostic-signature query is a broad prognosis query and does not impose a "
  "public-data or omics requirement, so the screen captures clinical, imaging, and cost-effectiveness "
  "studies as well as public-omics studies. The frequencies we reported therefore describe what is "
  "mentioned in the titles and abstracts of a broad prognosis corpus, not the prevalence of "
  "methodological practice in public-omics research. Rather than re-query with an omics filter and "
  "risk introducing a new, unvalidated eligibility rule at this stage, we have kept the existing "
  "sample and restricted the claim.")
CH("Section 2 now states explicitly that the query \u201cdeliberately does not require public-data "
   "reuse or omics analysis,\u201d that the screened records represent broad prognosis literature, and "
   "that the screen therefore describes a broad prognosis-literature corpus rather than the prevalence "
   "of methodological practices within gastric cancer public-omics research. The associated "
   "conclusions have been restricted accordingly. The screened records, coding rules, extraction "
   "procedure, retrieval date, and sorting settings are now documented in Supplementary Table S3. We "
   "have added a sentence explaining that the difference between the zero external-validation "
   "mentions in the Table S1 topic query and the 46/100 mentions in Table S3 arises from the different "
   "samples and coding definitions. We have also added that the zero code-availability finding is an "
   "observation about the screened text only, and that zero mentions do not indicate that no code "
   "exists. The screen was coded by a single author without duplicate coding, and this is now stated "
   "in the text.")

C("1.3", "In Section 2 and Supplementary Tables S1, S2 and S4, the bibliographic counts and "
   "metadata-matching procedure should be reconciled\u2026 the annual values sum to 1,951 risk-model "
   "records\u2026 whereas the corresponding overall counts are 1,812\u2026 In Table S4, absence from the "
   "retrieved search corpus should also be separated from absence in PubMed.")
R("We thank the reviewer for this precise arithmetic. The discrepancy arises because a record can "
  "carry both an electronic publication year and a print publication year, so it can be counted in "
  "two calendar years in the yearly series while appearing once in the date-bounded total. We have "
  "made this explanation explicit and now supply the year-assignment rule and PMID-level record sets.")
CH("Section 2 now states that yearly sums can exceed the date-bounded total for this reason, and that "
   "PMID-level record sets and the year-assignment rule are documented in Supplementary Table S2. "
   "Supplementary Table S4 has been restructured so that PubMed indexing status, search-corpus "
   "membership, and topic eligibility are recorded in separate fields, which separates absence from "
   "the retrieved corpus from absence in PubMed. The contribution of each metadata source, the "
   "deduplication procedure, and the treatment of unrelated records are now documented.")

C("1.4", "In the Introduction and Section 7, the additional contribution and intended use of "
   "GC-PROVE should be demonstrated more clearly. A mapping to TRIPOD, TRIPOD+AI, PROBAST and "
   "PROBAST+AI should be provided\u2026 At least two contrasting published studies should be assessed "
   "to demonstrate how the guide produces useful, traceable judgements. Claims that GC-PROVE is a "
   "validated scoring instrument should be avoided.")
R("We accept this. GC-PROVE was presented as a mnemonic without a clear account of what it adds "
  "beyond existing standards. We have added an explicit mapping table, separated reporting "
  "completeness from methodological quality and risk of bias, reconciled the main-text categories "
  "with the supplementary checklist, and added a worked example using two published studies whose "
  "validation designs contrast.")
CH("New Table 5 maps each GC-PROVE element to the existing standard that already covers it and to "
   "the domain-specific addition for gastric cancer public-omics, and states that PROBAST and "
   "PROBAST+AI should be used for risk-of-bias appraisal while GC-PROVE addresses reporting "
   "completeness. Section 7 now distinguishes reporting completeness from methodological quality, "
   "reconciles the qualitative categories in Table 4 with the supplementary checklist, and describes "
   "the five core domains and the three additional appraisal areas consistently. A worked example has "
   "been added in which two studies (references 37 and 42) are appraised: the first reports locked "
   "external validation in two independent cohorts with calibration and decision-curve analysis, "
   "while the second reports a random training/testing split of the same cohort; the example shows "
   "that each judgement traces to a documented design feature. Section 7 continues to state that "
   "GC-PROVE is a mnemonic and not a validated scoring instrument, and no synthetic data were "
   "introduced for its evaluation.")

C("1.5", "In Section 5 and Table 3, the clinical interpretation of biomarkers should be revised to "
   "reflect differences in their intended use and supporting evidence. MSI-H/dMMR, HER2, PD-L1 CPS, "
   "CLDN18.2, FGFR2b and EBV should not be grouped under a common statement of clinical establishment "
   "without specifying the treatment setting, assay, cutoff, jurisdiction and evidence date\u2026 "
   "prognostic association, treatment-response association and treatment-effect prediction should be "
   "distinguished.")
R("We agree that grouping these markers was imprecise. They differ in intended clinical use and in "
  "the strength of their supporting evidence, and a public-omics association cannot establish any of "
  "them. Section 5 has been rewritten to separate the marker categories and to add the predictor-versus-"
  "prediction distinction.")
CH("Section 5 now separates treatment-selection markers with approved indications (HER2, MSI-H/dMMR, "
   "and PD-L1 CPS in defined settings), a treatment-selection marker with a defined assay and cutoff "
   "(CLDN18.2), a largely investigational marker (FGFR2b), and a molecular-subtype and prognostic "
   "classifier (EBV). It states that the treatment setting, assay, cutoff, jurisdiction, and evidence "
   "date determine clinical utility for each marker. It now states that an association observed in "
   "treated patients, or a response demonstrated experimentally, does not by itself establish "
   "treatment-effect prediction, which requires an appropriate treatment comparator and a justified "
   "interaction analysis. It also states that decision-curve analysis should be tied to a defined "
   "clinical decision and a meaningful threshold range. Table 3 has been aligned with these "
   "distinctions.")

C("1.6", "In Figure 2 and Sections 4.2 to 4.4 and the foundation-model discussion, the methodological "
   "recommendations should be made sufficiently explicit for practical use. The workflow should show "
   "patient-level separation\u2026 Untouched external validation should be distinguished from subsequent "
   "recalibration\u2026 For Geneformer, scGPT and Nicheformer, the discussion should compare published "
   "evaluation tasks, simpler baselines, transfer limitations and potential overlap between "
   "pretraining and evaluation data.")
R("We agree that the recommendations were stated at too general a level to be actionable, and that "
  "the foundation-model discussion did not engage with the published evaluations.")
CH("Section 4.2 now states three decision points explicitly: development and validation data should "
   "be separated at the patient level rather than at the sample or cell level; data-dependent "
   "transformations should be estimated on the training data and applied unchanged to validation "
   "data, with nested resampling where model selection is performed; and an untouched external "
   "validation should be distinguished from later recalibration or model updating. It also states "
   "that biological interpretation and functional experiments are not compulsory stages but should be "
   "linked to the intended claim. Section 3.2 now notes that published evaluations of Geneformer, "
   "scGPT, scFoundation, and Nicheformer focus on cell-type annotation, batch integration, and "
   "perturbation prediction, that several report limited zero-shot performance relative to simple "
   "baselines, and that pretraining corpora may overlap evaluation datasets; it asks that these models "
   "be judged against transparent, task-matched baselines on data not used during pretraining. No new "
   "deep-learning experiments were required for these changes.")

H("Comments on the quality of English", 2)

C("E1", "In the Abstract, several broad concepts are compressed into long sentences\u2026 \u201cEvidentiary "
   "dilution\u201d should be explained through a concrete description of the underlying problem\u2026 The "
   "discussion of resources, analytical weaknesses and GC-PROVE should be divided into a clear sequence "
   "of shorter sentences.")
R("We have rewritten the relevant abstract sentences so that each carries one principal point, and "
  "we have explained evidentiary dilution concretely (repeated use of similar cohorts and analytical "
  "pipelines without a corresponding improvement in independent validation or clinical relevance).")
CH("The Abstract now separates the resource statement, the limitation statement, the review's scope, "
   "and the framework statement, and it defines evidentiary dilution in concrete terms. The scope of "
   "claims about common research practices has been kept within the evidence presented.")

C("E2", "In Section 4.2 and Section 5, abbreviations should be introduced consistently before they are "
   "used. LASSO and AUC should be expanded at their first main-text occurrence, while TNM should be "
   "explained explicitly. MSI-H, dMMR and PD-L1 CPS should also be introduced with sufficient context.")
R("We have performed a complete abbreviation pass across the abstract, main text, tables, figure "
  "legends, and supplementary material.")
CH("LASSO (least absolute shrinkage and selection operator), AUC (area under the receiver operating "
   "characteristic curve), TNM (tumour-node-metastasis), MSI-H (microsatellite instability-high), "
   "dMMR (mismatch repair deficiency), and PD-L1 CPS (programmed death-ligand 1 combined positive "
   "score) are now expanded at first use. Tables and figure legends define their abbreviations "
   "independently where needed. Repeated definitions and inconsistent forms were removed.")

C("E3", "\u201cPublic-derived\u201d should be changed consistently to \u201cderived from public data\u201d. "
   "Expressions such as \u201cexternal-validation language\u201d and \u201cclinical-comparator language\u201d "
   "should specify that mentions were detected in titles or abstracts\u2026 \u201cnegative validation\u201d "
   "should be replaced by a more precise expression.")
R("We agree that these expressions were imprecise about what was measured.")
CH("\u201cPublic-derived\u201d has been replaced throughout with \u201cderived from public data\u201d. The "
   "reporting-signal expressions now state that mentions were detected in titles or abstracts. In "
   "Section 7, \u201cnegative validation\u201d has been replaced with \u201cunsuccessful external validation "
   "or failure to reproduce a reported association\u201d.")

C("E4", "In Sections 4.2 to 4.4, Boxes 1 and 2 and Sections 6 to 8, repeated warnings about leakage, "
   "cutoffs, clinical comparators and code availability should be consolidated\u2026 Dense expressions "
   "such as \u201ca higher-burden extension of the same evidence hierarchy\u201d should be replaced with a "
   "direct explanation.")
R("We have consolidated the repeated warnings and removed the duplicated cross-references.")
CH("Box 2 has been replaced with a short checklist that cross-refers to Sections 4.2-4.4, where each "
   "principle is developed once. The duplicated Box 1 and Box 2 cross-references in Sections 4.3 and "
   "4.4 have been removed. The phrase about a \u201chigher-burden extension\u201d has been replaced with "
   "a direct statement of the additional tuning, validation, and reporting requirements that "
   "machine-learning methods introduce. Long sentences were checked for unclear pronoun references "
   "and for loosely connected claims.")

doc.add_page_break()

# ============================================================
# REVIEWER 2
# ============================================================
H("Reviewer 2", 1)
P("The reviewer made ten major comments and eighteen minor comments. We thank the reviewer for the "
  "detailed checking of the tables, which identified a real defect in the submitted file.", italic=True)

H("Major comments", 2)

C("2.1", "Incremental value of GC-PROVE over existing frameworks is not sufficiently clear\u2026 The "
   "authors should add a concise comparison table or paragraph explicitly stating: (i) which GC-PROVE "
   "elements are already covered by existing standards; (ii) which elements are domain-specific "
   "additions; and (iii) how GC-PROVE should be used alongside, not instead of, TRIPOD/PROBAST.")
R("We agree, and this is now addressed directly.")
CH("New Table 5 addresses all three points in a single table (see also our response to Reviewer 1, "
   "comment 1.4).")

C("2.2", "Serious table numbering and content errors: Table 3 is titled \u201cClaim type vs. minimum "
   "evidence\u2026\u201d but contains only a header and no content. A later table is labeled Table 4 but "
   "actually contains the content that should belong to Table 3. A second, correctly labeled Table 4 "
   "then appears as the GC-PROVE appraisal guide. The footnote to the correct Table 4 states rows 1-5 "
   "\u2026 however, the table contains only five rows.")
R("We are grateful for this comment and we traced the exact cause. In the manuscript source there was "
  "a stray markdown table separator line immediately before the \u201cTable 3\u201d caption. When the "
  "submitted file was rendered, that separator line produced an empty table with a header but no "
  "content, so the caption \u201cTable 3\u201d appeared above an empty frame, the real claim-type table "
  "appeared immediately afterwards without its own label, and the GC-PROVE guide then appeared as "
  "Table 4, giving the impression of two Table 4 captions. We have removed the stray separator and "
  "checked every table in the rebuilt file.")
CH("The stray separator has been deleted, and the revised manuscript was rebuilt and verified so that "
   "four numbered main tables and one new Table 5 are present, each with a header and content: Table 1 "
   "(databases and platforms), Table 2 (representative resources and studies), Table 3 (claim type "
   "versus minimum evidence), Table 4 (GC-PROVE appraisal guide), and Table 5 (relationship of "
   "GC-PROVE to existing standards). Table 4 contains eight rows, and its footnote now describes them "
   "as five core domains plus three additional appraisal areas, which matches the rows actually "
   "present. The Section 7 sentence that referred to \u201crows 6-8\u201d has been changed to refer to "
   "\u201cthe final three rows\u201d.")

C("2.3", "Extensive redundancy across sections and boxes\u2026 Box 2 repeats much of Section 4.2 and "
   "Section 4.4. The manuscript would be stronger if these sections were consolidated.")
R("We agree.")
CH("Box 2 has been condensed into a short checklist that cross-refers to Sections 4.2-4.4 rather than "
   "restating the arguments. The duplicated cross-references to Boxes 1 and 2 in Sections 4.3 and 4.4 "
   "have been removed, so the detailed methodological critique is developed once and the boxes contain "
   "only concise checklists and key cautions.")

C("2.4", "Literature identification and PubMed scan transparency need strengthening\u2026 Provide the "
   "core search strings in the main text\u2026 Clarify whether the title/abstract screen of 100 records "
   "was manual or automated, whether it was performed in duplicate\u2026 Explain how the 100 most recent "
   "records were selected\u2026 Ensure that Supplementary Files S1-S6 and the GC-PROVE checklist are "
   "actually available.")
R("We accept these points.")
CH("The core search strings are now given in Section 2 of the main text. Section 2 states that the "
   "screen was a title/abstract-level screen using predefined yes/no rules, coded by a single author "
   "without duplicate coding, and that the 100 records were the most recent records returned by the "
   "query sorted by date through 2026-06-30; the retrieval and sorting settings are documented. The "
   "statement that zero code-availability mentions is an abstract-level lower bound has been retained "
   "and strengthened. All supplementary files, together with the GC-PROVE checklist and the generation "
   "scripts, have been deposited in a public repository and are cited with a persistent identifier "
   "(see our response to comment 2.10).")

C("2.5", "Inconsistency in authorship and CRediT statements. The first-page CRediT statement lists "
   "authors and roles in a different order from the main text Author Contributions section\u2026 All "
   "author lists, contribution statements, and affiliation superscripts must be unified.")
R("We apologise for this inconsistency, which arose from two draft statements that were not "
  "synchronised.")
CH("The Author Contributions section now follows the same author order as the author list and the "
   "first-page statement, and the roles have been unified so that each author's contribution is "
   "described identically in both places. The corresponding-author and equal-contribution marks and "
   "the affiliation superscripts have been checked against the author list.")

C("2.6", "Some claims remain too strong for a narrative review\u2026 \u201cThe main limitation in this "
   "literature is not data access but evidentiary dilution\u201d\u2026 \u201creproducible PubMed database "
   "scans\u201d should be softened unless the full search log, query translation, and coding rules are "
   "provided and verifiable.")
R("We agree that the claim was too broad, because different subfields face different limitations "
  "including data access, metadata quality, computational expertise, and clinical annotation.")
CH("The abstract now reads \u201cA major limitation in this literature is not data access\u201d rather "
   "than \u201cThe main limitation,\u201d and the surrounding sentences have been divided so that the "
  "scope of the claim is explicit. The phrase \u201creproducible database scans\u201d is used only where "
  "the search log, query translations, and coding rules are provided in the supplementary material.")

C("2.7", "Clinical-utility claims and evidence restraint need tighter alignment\u2026 The manuscript "
   "should more clearly distinguish: prognostic vs. predictive biomarkers; diagnostic vs. prognostic "
   "vs. therapy-response markers; bulk deconvolution vs. direct immune measurement; ligand-receptor "
   "inference vs. functional signaling; foundation-model embeddings vs. validated biological "
   "mechanisms.")
R("We agree.")
CH("These distinctions are now stated explicitly in Section 5 and are aligned with Table 3, which maps "
   "each claim type to the minimum responsible evidence and to examples of unsafe claims. Section 5 "
   "now also separates prognostic association, treatment-response association, and treatment-effect "
   "prediction (see our response to Reviewer 1, comment 1.5).")

C("2.8", "Figure and legend consistency. Figure 1 uses \u201cGCPROVE\u201d instead of \u201cGC-PROVE.\u201d "
   "\u2026 Figure 4 states \u201cDomain 1-5, not Level 1-5\u201d, which is helpful, but the terminology "
   "should be consistent throughout\u2026 Please check all figure citations in the text against the "
   "final figure order and legends.")
R("We thank the reviewer for catching the spelling in Figure 1.")
CH("Figure 1 has been corrected so that the framework is labelled \u201cGC-PROVE\u201d consistently, "
   "and the abbreviation is defined in the figure legend. The term \u201cdomain\u201d is used "
   "consistently throughout the manuscript and the figures, and Figure 4 continues to label the five "
   "domains as Domain 1-5. All figure citations in the text were checked against the final figure "
   "order and legends.")

C("2.9", "Reference coverage and citation accuracy\u2026 some references are cited for claims that may "
   "require more direct primary sources. Please verify that every citation supports the specific "
   "statement made. Also check the accuracy of references marked \u201cIn print\u201d or with 2026 "
   "publication dates, and ensure that all DOI/PMID information is correct where available.")
R("We have re-checked the citations.")
CH("Citations were checked so that each supports the statement made. References marked \u201cIn "
   "print\u201d or dated 2026 were verified against their publisher records, and where the record was "
   "not yet final this is stated as an ahead-of-print citation. DOI or PMID information has been "
   "added or corrected where available, including for the prognostic studies re-verified for "
   "Supplementary Table S5.")

C("2.10", "Supplementary materials cannot be evaluated from the review PDF\u2026 The authors must ensure "
   "that all supplementary materials are complete, editable, and accessible to reviewers. If possible, "
   "deposit the GC-PROVE checklist and search logs in a public repository such as OSF or Zenodo and "
   "provide a DOI.")
R("We agree, and we have acted on this recommendation.")
CH("All supplementary files, the GC-PROVE checklist, the search logs, the metadata-scan output, and "
   "the figure, table, and scan generation scripts have been deposited in a public repository, and the "
   "Data Availability Statement now cites the deposit with a persistent digital object identifier. "
   "Editable versions (DOCX and CSV) of the supplementary tables are provided with the submission.")

H("Minor comments", 2)

minor_items = [
 ("2.m1-2", "\u201cGenefomer\u201d should be \u201cGeneformer.\u201d",
  "Corrected. The manuscript and figures now use \u201cGeneformer.\u201d"),
 ("2.m3", "\u201cCauton\u201d in Table 2 should be \u201cCaution.\u201d",
  "Corrected; the column header reads \u201cCaution for interpretation.\u201d"),
 ("2.m4", "\u201cCosMix\u201d should be \u201cCosMx.\u201d",
  "Corrected throughout the main text and tables."),
 ("2.m5", "\u201cIncRNA\u201d should be \u201clncRNA.\u201d",
  "Corrected; \u201clncRNA\u201d is used consistently and defined at first use."),
 ("2.m6", "\u201cGCPROVE\u201d should be \u201cGC-PROVE.\u201d",
  "Corrected in the manuscript and in Figure 1 (see comment 2.8)."),
 ("2.m7", "Use consistent hyphenation: \u201cpublic-omics\u201d vs \u201cpublic omics\u201d; \u201cmulti-omics\u201d; "
          "\u201crisk signature.\u201d",
  "\u201cPublic-omics\u201d is now used as a compound modifier and \u201cpublic omics\u201d only as a "
  "standalone noun; \u201cmulti-omics\u201d and \u201crisk signature\u201d are used consistently."),
 ("2.m8", "Table 1: The footnote uses a dagger symbol, but no corresponding marker appears in the table.",
  "The dagger has been replaced by \u201cNote.\u201d, since no in-table marker is required."),
 ("2.m9", "Table 2: The first column header says \u201cResource or platform,\u201d but the table also includes "
          "studies and resources.",
  "Clarified. In the revised tables, Table 1 is titled \u201cPublic databases and platforms\u201d and its "
  "first column is \u201cResource or platform,\u201d while Table 2 is titled \u201cRepresentative resources, "
  "studies, and methodological roles\u201d and its first column is \u201cStudy or resource.\u201d"),
 ("2.m10", "Box 1: Item 7 mixes ceRNA, WGCNA, and cell-cell communication; consider separating these "
           "into distinct red flags.",
  "Separated. Box 1 now lists WGCNA modules, ceRNA networks, cell-cell communication inference, and "
  "immune or stromal deconvolution as four distinct red flags; the box is retitled \u201cThirteen Red "
  "Flags.\u201d"),
 ("2.m11", "Box 2: This box is largely redundant with Sections 4.2-4.4. Condense or remove.",
  "Condensed. Box 2 is now a five-item checklist that cross-refers to Sections 4.2-4.4."),
 ("2.m12", "Section 4.3: \u201cEach checkpoint can introduce optimism (see Box 1 for ten common red "
           "flags)\u201d is followed by Box 2, which repeats the same material. Streamline.",
  "Streamlined. The duplicated cross-reference has been removed and the passage now develops the "
  "checkpoints once (see comment 2.3)."),
 ("2.m13", "Section 5: The term \u201cbiomarker\u201d is used broadly. Define early and distinguish "
           "candidate, prognostic, predictive, and validated clinical biomarkers.",
  "Defined. Section 5 now distinguishes candidate markers, prognostic associations, predictive "
  "markers, and validated clinical biomarkers, and separates treatment-selection markers from "
  "investigational markers and subtype classifiers."),
 ("2.m14", "Data Availability Statement: For a review with a proposed checklist, a public repository "
           "identifier would be preferable.",
  "Addressed. The statement now cites the public repository deposit with a persistent identifier "
  "(see comment 2.10)."),
 ("2.m15", "Author Contributions: The first-page CRediT and the main-text Author Contributions must "
           "match exactly.",
  "Unified (see comment 2.5)."),
 ("2.m16", "Funding: The funders' role is appropriately stated. No issue.",
  "Noted, with thanks."),
 ("2.m17", "Abstract: The abstract is concise and within the stated word count. The Key Points are "
           "useful.",
  "Noted, with thanks. The abstract was slightly restructured for readability (see comment E1)."),
 ("2.m18", "Language: The manuscript is generally readable, but there are several long, repetitive "
           "sentences. Professional language editing would improve clarity.",
  "We have performed a further editing pass to shorten long sentences, remove repetition, and check "
  "pronoun references, in line with the English-language comments from Reviewer 1."),
]
for num, comment, resp in minor_items:
    C(num, comment)
    R(resp)

# ============================================================
# Closing
# ============================================================
P("")
P("We thank the editor and both reviewers again for their time and for the improvements their "
  "comments have produced. The revised manuscript, the rebuilt Supplementary Table S5, and the "
  "corrected supplementary files are provided with this submission. We would be glad to address any "
  "further points.")
P("")
P("On behalf of all authors,")
P("Aiqun Liu, MD")
P("Department of Gastroenterology, Guangxi Medical University Cancer Hospital, Nanning, Guangxi, China")
P("Email: liuaiqun_2004@163.com")

doc.save(OUT)
print(f"OK  {OUT}")
print(f"    size {OUT.stat().st_size} bytes")
