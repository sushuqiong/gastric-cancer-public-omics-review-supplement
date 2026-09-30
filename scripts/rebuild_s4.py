#!/usr/bin/env python3
"""Rebuild S4 with properly separated fields."""
import csv, os, time, json, urllib.request, urllib.parse, glob

SUP = r"C:\Users\fengq\Desktop\v14_revision\supplementary"
SRC = os.path.join(SUP, "Supplementary_Table_S4_public_metadata_scan_v13.5.5.csv")
OUT = os.path.join(SUP, "Supplementary_Table_S4_public_metadata_scan_v14.csv")
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig", newline="")))
print(f"S4 记录数: {len(rows)}")

# corpus PMIDs from the topic query record sets
corpus = set()
for f in glob.glob(os.path.join(SUP, "Supplementary_File_S2_pmid_list_*_v14.csv")):
    for r in csv.reader(open(f, encoding="utf-8", newline="")):
        for c in r:
            c = c.strip()
            if c.isdigit():
                corpus.add(c)
print(f"检索语料 PMID 数: {len(corpus)}")

def pubmed_by_doi(doi):
    if not doi:
        return None
    u = BASE + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "retmode": "json", "term": f'{doi}[DOI] OR {doi}[AID]',
         "retmax": 3, "tool": "hermes", "email": "liuaiqun_2004@163.com"})
    for k in range(2):
        try:
            d = json.loads(urllib.request.urlopen(u, timeout=40).read().decode())
            ids = d.get("esearchresult", {}).get("idlist", [])
            return ids[0] if ids else None
        except Exception:
            time.sleep(3)
    return None

def topic_ok(title):
    t = (title or "").lower()
    gc = ("gastric" in t or "stomach" in t or "gastroesophageal" in t)
    omics = any(k in t for k in ("omics", "transcriptom", "bioinformatic", "tcga", "gene expression",
                                 "single-cell", "single cell", "spatial", "prognostic", "signature",
                                 "biomarker", "methylation", "proteom"))
    return gc and omics

out_rows = []
need = [r for r in rows if not (r.get("pmid_or_pubmed_id") or "").strip()]
print(f"缺少 PMID 需核查的记录: {len(need)}\n")

cache = {}
for i, r in enumerate(need):
    doi = (r.get("doi") or "").strip()
    cache[id(r)] = pubmed_by_doi(doi) if doi else None
    if (i + 1) % 10 == 0:
        print(f"  ... {i+1}/{len(need)}")
    time.sleep(0.35)

for r in rows:
    pmid_meta = (r.get("pmid_or_pubmed_id") or "").strip()
    rechecked = cache.get(id(r))
    eff_pmid = pmid_meta or (rechecked or "")

    if eff_pmid and eff_pmid.isdigit() and eff_pmid in corpus:
        in_corpus = "yes"
    elif eff_pmid and eff_pmid.isdigit():
        in_corpus = "no"
    else:
        in_corpus = "not_determined"

    if eff_pmid:
        idx = "indexed_in_pubmed"
    elif doi_present := bool((r.get("doi") or "").strip()):
        idx = "not_found_by_doi_query"
    else:
        idx = "no_identifier_available"

    out_rows.append({
        "source": r.get("source", ""),
        "query": r.get("query", ""),
        "title": r.get("title", ""),
        "year": r.get("year", ""),
        "venue": r.get("venue", ""),
        "doi": r.get("doi", ""),
        "pmid_in_metadata": pmid_meta,
        "pmid_verified": rechecked or "",
        "pubmed_indexing_status": idx,
        "search_corpus_membership": in_corpus,
        "topic_eligible_for_review": "yes" if topic_ok(r.get("title", "")) else "no",
        "original_field_likely_not_in_pubmed": r.get("likely_not_in_pubmed", ""),
        "url": r.get("url", ""),
    })

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
    w.writeheader(); w.writerows(out_rows)

import collections
idx_stat = collections.Counter(x["pubmed_indexing_status"] for x in out_rows)
cor_stat = collections.Counter(x["search_corpus_membership"] for x in out_rows)
top_stat = collections.Counter(x["topic_eligible_for_review"] for x in out_rows)
print(f"\n✅ 已写出 {os.path.basename(OUT)} ({len(out_rows)} 行)")
print(f"  索引状态: {dict(idx_stat)}")
print(f"  语料归属: {dict(cor_stat)}")
print(f"  主题合格: {dict(top_stat)}")

json.dump({"n_rows": len(out_rows), "indexing": dict(idx_stat),
           "corpus": dict(cor_stat), "topic": dict(top_stat),
           "n_need_recheck": len(need),
           "n_recovered_in_pubmed": sum(1 for v in cache.values() if v)},
          open(os.path.join(SUP, "s4_restructure_summary_v14.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
