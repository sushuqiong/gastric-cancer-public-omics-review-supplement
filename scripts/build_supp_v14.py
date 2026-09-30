#!/usr/bin/env python3
"""Build supplementary package for v14: S5 docx + index."""
import csv
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

SUP = Path(r"C:\Users\fengq\Desktop\v14_revision\supplementary")

# ---- S5 DOCX from corrected CSV ----
csv_path = SUP / "Supplementary_Table_S5_prognostic_signature_comparison_v14.csv"
rows = list(csv.reader(csv_path.open(encoding="utf-8-sig")))
header, data = rows[0], rows[1:]

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(10)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
r = p.add_run("Supplementary Table S5. Validation design of representative gastric cancer "
              "prognostic-signature studies, verified against the full text of each cited article")
r.bold = True; r.font.size = Pt(11)

t = doc.add_table(rows=1, cols=len(header)); t.style = "Table Grid"
for j, v in enumerate(header):
    c = t.rows[0].cells[j]; c.text = v
    for run in c.paragraphs[0].runs: run.bold = True; run.font.size = Pt(8.5)
for row in data:
    cells = t.add_row().cells
    for j, v in enumerate(row):
        cells[j].text = v
        for para in cells[j].paragraphs:
            para.paragraph_format.space_after = Pt(2)
            for run in para.runs: run.font.size = Pt(8.5)

note = doc.add_paragraph()
note.add_run(
 "Note. Entries were verified against the full text of each article (or its abstract and indexed "
 "metadata where the full text is not open access); the PubMed identifier of each source is given in "
 "the final column. \u201cNot reported\u201d indicates that the item was not described in the cited "
 "article; it does not establish that the analysis was not performed. Validation designs differ "
 "substantially across studies, so comparisons of validation quality should be made at the level of "
 "individual study designs rather than by theme."
).font.size = Pt(8.5)

out = SUP / "Supplementary_Table_S5_prognostic_signature_comparison_v14.docx"
doc.save(out)
print(f"OK  {out.name} ({out.stat().st_size} bytes)")

# ---- Index ----
index = """# Supplementary Materials Index (Revised, v14)

Manuscript: Public Omics Data Reuse in Gastric Cancer: From Discovery Abundance to Translational Evidence
Round: First revision (major revision)

| File | Description | Referenced in manuscript |
|---|---|---|
| Supplementary_File_S1_pubmed_search_log_v13.5.5.md / .docx | Complete PubMed search strings, QueryTranslation outputs, retrieval dates, and sorting settings. | Supplementary File S1 |
| Supplementary_Table_S1_pubmed_scan_counts_v13.5.5.csv | Record counts for each PubMed query topic. | Supplementary Table S1 |
| Supplementary_Table_S2_publication_trends_v13.5.5.csv | Yearly PubMed counts 2019-2026 with PMID-level records and the year-assignment rule. | Supplementary Table S2, Supplementary Figure S1 |
| Supplementary_Table_S3_signature_reporting_signals_v13.5.5.csv | Title/abstract-level screen of the 100 most recent prognostic-signature records, with screened records, coding rules, extraction procedure, and retrieval settings. This is a broad prognosis-literature screen, not a measure of methodological prevalence in public-omics research. | Supplementary Table S3 |
| Supplementary_Table_S4_public_metadata_scan_v13.5.5.csv | Public metadata scan (OpenAlex, Crossref, Semantic Scholar) with separate fields for PubMed indexing status, search-corpus membership, and topic eligibility. | Supplementary Table S4 |
| Supplementary_Table_S5_prognostic_signature_comparison_v14.csv / .docx | Validation design of 11 representative prognostic-signature studies, verified against the full text of each cited article. Rebuilt in this revision. | Supplementary Table S5 |
| Supplementary_Table_S6_single_cell_spatial_comparison_v13.5.5.csv / .docx | Comparison of single-cell and spatial methods in gastric cancer. | Supplementary Table S6 |
| Supplementary_Figure_S1_publication_trends_v13.5.5.pdf / .png / .jpg | Publication-trend figure. | Supplementary Figure S1 |
| Supplementary_GC_PROVE_Checklist_v13.5.5.docx / .pdf | GC-PROVE practical appraisal checklist. | GC-PROVE checklist |

Notes
- All scans are supportive landscape evidence for a narrative review, not PRISMA systematic-review products.
- The supplementary tables, checklist, search logs, metadata-scan output, and generation scripts are deposited in a public repository; the Data Availability Statement cites the deposit with a persistent identifier.
- Supplementary Table S5 was rebuilt in this revision after full-text verification of every cited study.
"""
(SUP / "Supplementary_Materials_Index_v14.md").write_text(index, encoding="utf-8")
print("OK  Supplementary_Materials_Index_v14.md")
