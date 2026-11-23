#!/usr/bin/env python3
"""Deduplication and transparent rule-based Stage-1 (title/abstract) screening.

Rules are keyword-based and documented in prisma_flow.md (section "Screening rules").
Output: dedup.json (all unique records with tags, decision, reason, priority score).
Stage-1 decisions are AI-assisted and must be validated by the student (20% dual-screen, kappa).
"""
import json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ["CORE-01", "C1", "C2", "C3", "C4", "C4-ETH", "C5", "C6", "C7", "C8", "C9", "SUP-PIPE", "SUP-PAY"]
ORDER += [q + "-CIT" for q in ORDER[:11]] + ["TTL-C1", "TTL-C2", "TTL-C4", "TTL-C6"]


def norm_title(t):
    t = (t or "").lower()
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def has(text, pats):
    return any(re.search(p, text) for p in pats)


CONSTR = [r"\bconstruction (site|project|industry|phase|work|management|equipment|worker|progress|process|stage|compan|firm|sector|machiner|activit|engineering|monitoring|operation)",
          r"\bcontractors?\b", r"\bsubcontract", r"\bearthwork", r"\bbuilding site", r"\bjob ?site",
          r"\bbuilt environment", r"\baeco?\b", r"\binfrastructure (project|construction|sector)", r"\bcivil (engineering|infrastructure|works)",
          r"\b(highway|road|railway|rail|bridge|tunnel|pipeline|building|infrastructure|civil|heavy|industrial|residential|offshore|modular|precast|off-site|offsite|prefabricated|onshore) construction", r"\bin construction\b",
          r"\bconstruction (workers?|environments?|scenes?|vehicles?|machines?|resources?|jobsites?|plants?|areas?|zones?|company|companies|industry|sector|professional|practitioner|manager|engineer|organi[sz]ation|contract|schedul|cost|claim|disput|payment|delay|quantit|productiv|labou?r|crew|material|logistic|operation|automation|robot|digital twin|informatics)",
          r"\bright[- ]of[- ]way", r"\bbim\b", r"\bbuilding information model", r"\bjobsites?\b"]
LINEAR = [r"\bpipelines?\b", r"\blinear (infrastructure|project|asset|construction)", r"\bright[- ]of[- ]way", r"\bhighways?\b",
          r"\broads?\b", r"\brailways?\b", r"\brail\b", r"\bcorridors?\b", r"\btransmission lines?\b", r"\bchainage", r"\bstationing",
          r"\blinear referenc", r"\balignment"]
PIPE = [r"\boil (and|&) gas\b", r"\bpetroleum\b", r"\b(gas|oil|water|natural gas|transmission|cross-country|buried|steel|onshore|hydrocarbon|sewer|utility|long-distance) pipelines?\b", r"\bpipelines? (construction|project|route|right|installation|laying|spread|corridor|engineering|network|alignment)", r"\bright[- ]of[- ]way", r"\bpipe ?laying", r"\btrench(ing|es)?\b", r"\bmidstream"]
OOD = [r"\bmanufactur", r"\bhealthcare\b", r"\bhospital patient", r"\bagricultur", r"\bcrop\b", r"\bforest(?! road)", r"\bglacier", r"\bcoastal",
       r"\blandslide", r"\bvolcan", r"\bmedical\b", r"\bsmart city\b", r"\burban digital twin", r"\bpost-harvest", r"\bfood\b",
       r"\bmining\b", r"\bmine\b", r"\barchaeolog", r"\bcultural heritage", r"\bheritage\b", r"\briver\b", r"\bbeach", r"\bdune",
       r"\bsupply chain finance", r"\btourism", r"\beducation\b", r"\bstudents?\b", r"\bautomotive"]
OM = [r"\bleak", r"\bcorrosion", r"\bin-line inspection", r"\bintegrity management", r"\bfacility management", r"\bfacilities management",
      r"\boperation and maintenance", r"\bo&m\b", r"\bstructural health monitoring", r"\bpredictive maintenance", r"\bpavement (condition|distress|crack)",
      r"\bcrack detection", r"\bdefect detection", r"\bencroachment", r"\bintrusion", r"\bthird[- ]party damage", r"\bwellbore", r"\breservoir",
      r"\bdrilling\b", r"\boffshore platform"]
CONSTR_PHASE = [r"\bconstruction (phase|stage|site|progress|project|productivity|process|management|equipment|worker|activit|monitoring)", r"\bprogress monitoring", r"\bas-built", r"\bearthwork", r"\bcontractor", r"\bpipeline construction"]
OFFTOPIC_T = [r"\bsafety\b", r"\bergonomic", r"\bposture", r"\bfatigue", r"\bhealth\b", r"\bemission", r"\bcarbon\b", r"\bcircular economy", r"\bsustainab", r"\benergy (consumption|efficien|performance)", r"\bcost estimat", r"\barchive", r"\bcurricul", r"\bdesign review", r"\bfire\b", r"\bheat stress", r"\bstress\b", r"\bfinite element", r"\bconcrete (strength|curing|mix)"]
CORE_T = [r"\bprogress", r"\bproductivity", r"\btracking", r"\blocali[sz]", r"\bquantit", r"\bpayment", r"\bvolume", r"\bearthwork", r"\bdigital twin", r"\buav", r"\bdrone", r"\bmonitoring", r"\binteroperab", r"\bdata quality", r"\badoption", r"\bacceptance", r"\bgis\b", r"\bifc\b", r"\bequipment", r"\bsubcontract", r"\bclaim", r"\bdispute", r"\btelematic", r"\bgps\b", r"\brfid", r"\bwearable", r"\bprivacy", r"\bsurveillance", r"\bethic", r"\brtls", r"\buwb", r"\bbluetooth", r"\breal-time locat"]
ALGO = [r"\bwe propose a (novel )?(network|algorithm)", r"\bdeep learning\b", r"\bneural network", r"\bdataset\b", r"\bbenchmark"]
APPL = [r"\bconstruction site", r"\bprogress", r"\bearthwork", r"\bvolume", r"\bstockpile", r"\bquantit", r"\bas-built", r"\bfield (test|trial|study|experiment|validation)", r"\bcase study"]
NONPEER = [r"^(editorial|preface|foreword|call for papers|front matter|back matter|table of contents|index)\b", r"^proceedings of", r"\bkeynote\b", r"^\s*$"]
IT_PIPELINE = [r"\b(ci/cd|data|processing|image|software|machine learning|ml|etl) pipelines?\b"]

CLUSTER_PATS = {
 "C1": [r"\bdigital twin", r"\bcyber[- ]physical"],
 "C2": [r"\buav", r"\buas\b", r"\bdrone", r"\bunmanned aerial", r"\bphotogrammetr", r"\bstructure[- ]from[- ]motion", r"\borthophoto", r"\borthomosaic", r"\bpoint cloud"],
 "C3": [r"\bgis\b", r"\bgeographic information", r"\bgeospatial", r"\blinear referenc", r"\bchainage", r"\bstationing", r"\bifc alignment", r"\bbim[- ]gis"],
 "C4": [r"\brfid", r"\bbluetooth", r"\bble\b", r"\buwb\b", r"\bultra[- ]wide", r"\bgnss", r"\bgps\b", r"\btelematics", r"\bwearable", r"\bactivity recognition", r"\btracking", r"\blocali[sz]ation", r"\biot\b", r"\binternet of things"],
 "C5": [r"\bproductivity", r"\bearned value", r"\bschedule performance", r"\bidle time", r"\butili[sz]ation"],
 "C6": [r"\bprogress (monitoring|measurement|tracking|payment|estimation)", r"\bquantity take[- ]?off", r"\bquantity survey", r"\bpayment", r"\binvoic", r"\bsubcontract", r"\bearthwork volume", r"\bvolume (calculation|estimation|measurement)", r"\bas-built", r"\bclaims?\b", r"\bdisputes?\b"],
 "C7": [r"\bifc\b", r"\bindustry foundation classes", r"\blandxml", r"\biso 19650", r"\bopc ua", r"\bogc\b", r"\bcitygml", r"\bpods\b", r"\binteroperab", r"\bontolog", r"\blinked data", r"\bsemantic web", r"\bdata exchange", r"\bapi\b"],
 "C8": [r"\bdata quality", r"\buncertaint", r"\bprovenance", r"\baudit", r"\btraceab", r"\bdata integrity", r"\bblockchain", r"\bvalidation", r"\baccuracy", r"\brmse\b"],
 "C9": [r"\badoption", r"\btechnology acceptance", r"\btam\b", r"\butaut", r"\bdiffusion of innovation", r"\bresistance to change", r"\bchange management", r"\bdigital transformation", r"\bbarriers?\b", r"\bprivacy", r"\bethic"],
}
EMPIRICAL = [r"\bcase study", r"\bfield (test|trial|study|experiment|data|validation|implementation)", r"\bvalidat", r"\bexperiment", r"\bpilot", r"\brmse\b",
             r"\baccuracy of", r"\b\d+(\.\d+)? ?(cm|mm|%)\b", r"\bsurvey of \d+", r"\bquestionnaire", r"\binterviews?\b", r"\breal[- ]world", r"\bimplemented on", r"\bdemonstrat"]
HIGHREL = [r"\bquantit", r"\bpayment", r"\bsubcontract", r"\bearthwork", r"\bvolum", r"\bprogress", r"\bproductivity", r"\bequipment", r"\bworkers?\b",
           r"\binvoic", r"\bclaims?\b", r"\bdisputes?\b", r"\bas-built", r"\bpipelines?\b", r"\bright[- ]of[- ]way", r"\blinear", r"\bdigital twin",
           r"\binteroperab", r"\bdata quality", r"\buncertaint", r"\badoption", r"\baccuracy"]


def screen(r):
    t = (r["title"] or "")
    tl = t.lower()
    ab = (r["abstract"] or "").lower()
    txt = tl + " " + ab
    tags = [c for c, p in CLUSTER_PATS.items() if has(txt, p)]
    r["clusters_kw"] = tags
    constr = has(txt, CONSTR)
    linear = has(txt, LINEAR)
    pipe = has(txt, PIPE) and not has(txt, IT_PIPELINE)
    r["ctx_construction"], r["ctx_linear"], r["ctx_pipeline"] = constr, linear, pipe
    emp = sum(1 for p in EMPIRICAL if re.search(p, txt))
    rel = sum(1 for p in HIGHREL if re.search(p, txt))
    # --- decision rules (applied in order) ---
    if has(tl, NONPEER) or r["type"] not in ("article", "review", "book-chapter", "conference-paper"):
        dec, code, why = "Exclude", "EX4", "non-peer-reviewed / front matter"
    elif (r.get("publication_year") or 0) < 2010:
        dec, code, why = "Exclude", "EX7", "before 2010"
    elif not constr and not (pipe and has(txt, CONSTR_PHASE)) :
        dec, code, why = "Exclude", "EX1", "no construction/infrastructure context in title/abstract"
    elif has(txt, OOD) and not has(txt, [r"\bconstruction (site|project|industry|phase|equipment|worker|progress)", r"\bearthwork", r"\bcontractor"]):
        dec, code, why = "Exclude", "EX1", "out-of-domain term without construction-site context"
    elif (has(tl, OM) and not has(txt, CONSTR_PHASE)) or (has(ab, OM) and not has(txt, [r"\bconstruction"])):
        dec, code, why = "Exclude", "EX2", "operations/maintenance focus without construction-phase relevance"
    elif not tags:
        dec, code, why = "Exclude", "EX1", "no cluster C1-C9 concept in title/abstract (IN4 not met)"
    elif has(tl, OFFTOPIC_T) and not has(tl, CORE_T):
        dec, code, why = "Exclude", "IN4", "topic outside review constructs (e.g. safety/ergonomics/sustainability/cost-estimation only)"
    elif sum(1 for p in ALGO if re.search(p, txt)) >= 2 and not has(txt, APPL) and "C2" in tags:
        dec, code, why = "Exclude", "EX3", "algorithmic CV/photogrammetry without construction measurement application"
    elif not ab:
        dec, code, why = "Unsure", "", "no abstract in OpenAlex; title in scope -> full text check"
    else:
        dec, code, why = "Include", "", "IN1-IN5 met at title/abstract level (keyword rules)"
    # priority score for core-set selection (only meaningful for Include)
    score = rel + 1.5 * min(emp, 4) + (3 if pipe else 0) + (2 if linear else 0) + (2 if constr else 0)
    score += 2 if has(txt, [r"\bquantit", r"\bpayment", r"\bsubcontract", r"\binvoic", r"\bearthwork volume"]) else 0
    cites = r.get("cited_by_count") or 0
    score += min(cites, 300) / 75.0
    r.update(stage1_decision=dec, stage1_reason_code=code, stage1_reason=why, priority=round(score, 2), n_empirical=emp)
    return r


def main():
    recs, by_doi, by_title = [], {}, {}
    identified = 0
    for qid in ORDER:
        d = json.load(open(os.path.join(HERE, f"{qid}.json")))
        for w in d["records"]:
            identified += 1
            key_t = norm_title(w["title"])
            hit = None
            if w["doi"] and w["doi"] in by_doi:
                hit = by_doi[w["doi"]]
            elif key_t and key_t in by_title:
                hit = by_title[key_t]
            if hit is not None:
                if qid not in hit["queries"]:
                    hit["queries"].append(qid)
                if not hit["abstract"] and w["abstract"]:
                    hit["abstract"] = w["abstract"]
                continue
            w = dict(w)
            w["queries"] = [qid]
            recs.append(w)
            if w["doi"]:
                by_doi[w["doi"]] = w
            if key_t:
                by_title[key_t] = w
    s2 = json.load(open(os.path.join(HERE, "S2_enrichment.json")))["records"] if os.path.exists(os.path.join(HERE, "S2_enrichment.json")) else {}
    for i, r in enumerate(recs, 1):
        r["record_id"] = f"R{i:04d}"
        r["abstract_source"] = "OpenAlex" if r["abstract"] else ""
        if not r["abstract"] and r["doi"] in s2:
            e = s2[r["doi"]]
            if e["abstract"]:
                r["abstract"], r["abstract_source"] = e["abstract"], "SemanticScholar"
            elif e["tldr"]:
                r["abstract"], r["abstract_source"] = e["tldr"], "SemanticScholar-TLDR (machine summary)"
        screen(r)
    json.dump({"identified": identified, "unique": len(recs), "records": recs}, open(os.path.join(HERE, "dedup.json"), "w"), indent=1)
    from collections import Counter
    print("identified", identified, "unique", len(recs))
    print(Counter(r["stage1_decision"] for r in recs))
    print(Counter(r["stage1_reason_code"] for r in recs))


if __name__ == "__main__":
    main()
