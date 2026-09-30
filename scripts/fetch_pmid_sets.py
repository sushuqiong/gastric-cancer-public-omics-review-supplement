#!/usr/bin/env python3
"""Fetch PMID-level record sets for each topic query and compute year assignments."""
import json, time, re, urllib.request, urllib.parse, csv, os

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
OUT = r"C:\Users\fengq\Desktop\v14_revision\supplementary"
DATE = '("2019/01/01"[Date - Publication] : "2026/06/30"[Date - Publication])'

GA = '(("gastric cancer"[Title/Abstract] OR "stomach adenocarcinoma"[Title/Abstract] OR "stomach cancer"[Title/Abstract])'
RET = 'NOT retracted publication[Publication Type])'

QUERIES = {
 "public_omics": f'{GA} AND (TCGA[Title/Abstract] OR GEO[Title/Abstract] OR "public database"[Title/Abstract] OR "public datasets"[Title/Abstract] OR bioinformatics[Title/Abstract] OR "secondary analysis"[Title/Abstract] OR transcriptome[Title/Abstract]) {RET} AND {DATE}',
 "prognostic": f'((("gastric cancer"[Title/Abstract] OR "stomach adenocarcinoma"[Title/Abstract]) AND ("risk signature"[Title/Abstract] OR "prognostic signature"[Title/Abstract] OR "prognostic model"[Title/Abstract] OR nomogram[Title/Abstract] OR "survival model"[Title/Abstract]) NOT retracted publication[Publication Type])) AND {DATE}',
 "single_cell": f'{GA} AND ("single-cell"[Title/Abstract] OR scRNA[Title/Abstract] OR "single cell"[Title/Abstract]) {RET} AND {DATE}',
 "spatial": f'{GA} AND ("spatial transcriptomics"[Title/Abstract] OR "spatial omics"[Title/Abstract] OR "spatial multi-omics"[Title/Abstract] OR "multiplex immunofluorescence"[Title/Abstract] OR Xenium[Title/Abstract] OR Visium[Title/Abstract] OR CosMx[Title/Abstract] OR MERFISH[Title/Abstract] OR "Stereo-seq"[Title/Abstract]) {RET} AND {DATE}',
 "ai_ml": f'{GA} AND ("machine learning"[Title/Abstract] OR "artificial intelligence"[Title/Abstract] OR "deep learning"[Title/Abstract] OR XGBoost[Title/Abstract] OR transformer[Title/Abstract]) AND (prognosis[Title/Abstract] OR survival[Title/Abstract] OR "risk model"[Title/Abstract] OR "public database"[Title/Abstract] OR transcriptome[Title/Abstract] OR TCGA[Title/Abstract] OR GEO[Title/Abstract]) {RET} AND {DATE}',
}

def get(url, tries=3):
    for k in range(tries):
        try:
            return urllib.request.urlopen(url, timeout=60).read().decode("utf-8", "ignore")
        except Exception as e:
            time.sleep(3 * (k + 1))
    return ""

def esearch_count(q):
    u = BASE + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "retmode": "json", "term": q, "rettype": "count",
         "tool": "hermes", "email": "liuaiqun_2004@163.com"})
    d = json.loads(get(u) or "{}")
    return int(d.get("esearchresult", {}).get("count", 0))

def fetch_all_pmids(q, cap=6000):
    """Use history server + efetch in batches."""
    u = BASE + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "retmode": "json", "term": q, "retmax": 0, "usehistory": "y",
         "tool": "hermes", "email": "liuaiqun_2004@163.com"})
    d = json.loads(get(u) or "{}")
    r = d.get("esearchresult", {})
    total = int(r.get("count", 0))
    if total == 0 or total > cap:
        return total, []
    u2 = BASE + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "retmode": "json", "term": q, "retmax": min(total, cap),
         "usehistory": "y", "tool": "hermes", "email": "liuaiqun_2004@163.com"})
    d2 = json.loads(get(u2) or "{}")
    return total, d2.get("esearchresult", {}).get("idlist", [])

summary = []
os.makedirs(OUT, exist_ok=True)
for key, q in QUERIES.items():
    total, pmids = fetch_all_pmids(q)
    print(f"{key}: {total} records" + (f", retrieved {len(pmids)} PMIDs" if pmids else " (too many to list)"))
    if pmids:
        with open(os.path.join(OUT, f"Supplementary_File_S2_pmid_list_{key}_v14.csv"), "w",
                  newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["pmid"]); [w.writerow([p]) for p in pmids]
    summary.append({"topic": key, "date_bounded_total": total,
                    "pmids_retrieved": len(pmids),
                    "pmid_list_file": f"Supplementary_File_S2_pmid_list_{key}_v14.csv" if pmids else ""})
    time.sleep(1.5)

with open(os.path.join(OUT, "Supplementary_File_S2_record_set_summary_v14.csv"), "w",
          newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["topic", "date_bounded_total", "pmids_retrieved", "pmid_list_file"])
    w.writeheader(); w.writerows(summary)

print("\n=== 汇总 ===")
for s in summary:
    print(f"  {s['topic']:14} 总数 {s['date_bounded_total']:5}  PMID 列表 {s['pmids_retrieved']}")
