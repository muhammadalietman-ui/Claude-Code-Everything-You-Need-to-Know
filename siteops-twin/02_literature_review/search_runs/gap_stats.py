#!/usr/bin/env python3
"""Corpus-level keyword counts used in gap_analysis.md (Stage-1 pool = Include + Unsure; title+abstract text).
Counts are indicative (keyword-based, abstract availability ~80%)."""
import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from coding import CODES
recs = json.load(open(os.path.join(HERE, "dedup.json")))["records"]
OV = {"R2072", "R0147", "R3025"}
pool = [r for r in recs if r["stage1_decision"] in ("Include", "Unsure") or r["record_id"] in OV]
T = lambda r: ((r["title"] or "") + " " + (r["abstract"] or "")).lower()
def n(rs, *pats): return [r for r in rs if all(re.search(p, T(r)) for p in pats)]
DT = r"digital twin|cyber[- ]physical"
PAY = r"payment|invoic|certif(y|ied|ication) .{0,30}(quantit|work|payment)|subcontract|interim valuation|valuation of work|claims?\b|disputes?\b"
PAYSTRICT = r"payment|invoic|subcontract|valuation"
TECH = r"progress|schedul|geometr|safety|quality|monitor"
UAV = r"\buav|\buas\b|drone|unmanned aerial|photogrammetr"
ACC = r"accura|rmse|error|uncertaint|deviation"
TOL = r"toleran|acceptance (criteri|rule|threshold)|specification|requirement|contract|payment|certif"
PIPE = r"\boil (and|&) gas\b|\b(gas|oil|natural gas|transmission|cross-country|buried|steel|onshore|hydrocarbon) pipelines?\b|\bpipelines? (construction|project|route|right|installation|laying|spread|corridor)|right[- ]of[- ]way|pipe ?laying"
LIN = r"\bpipelines?\b|linear (infrastructure|project)|right[- ]of[- ]way|\bhighways?\b|\broads?\b|\brailways?\b|\brail\b|corridor|transmission line"
SCHEMA = r"data model|schema|ontolog|information model|\bifc\b|landxml|pods\b|common data environment"
COMM = r"payment|invoic|subcontract|bill of quantit|boq|cost|claim|quantit"
TRACK = r"rfid|bluetooth|\bble\b|uwb|ultra[- ]wide|gnss|\bgps\b|telematic|wearable|real[- ]time locat|rtls|tracking|locali[sz]ation"
PRIV = r"privacy|ethic|consent|gdpr|surveillance|data protection|trust"
REMOTE = r"remote|connectivity|network coverage|rural|long[- ]distance|kilomet|\bkm\b"
DUR = r"\b(\d+)[- ](weeks?|months?)\b"
DESIGN = r"baseline|before and after|pre[- ]and[- ]post|pre-?post|control group|comparative (study|analysis|case)|case studies .{0,40}(existing|traditional)|compared with (the )?(traditional|conventional|manual|existing)"
COUT = r"dispute|payment (delay|time|cycle)|administrative|rework|certification time|claim"
out = {}
out["pool"] = len(pool)
dt = n(pool, DT); out["G1_DT_records"] = len(dt)
out["G1_DT_with_payment_or_dispute_terms"] = len(n(dt, PAY))
out["G1_DT_with_payment_strict"] = len(n(dt, PAYSTRICT))
out["G1_DT_with_technical_state_terms"] = len(n(dt, TECH))
out["G1_DT_payment_titles"] = [r["title"] for r in n(dt, PAYSTRICT)][:40]
out["G2_pipeline_context"] = len(n(pool, PIPE)); out["G2_linear_context"] = len(n(pool, LIN))
out["G2_pipeline_and_progress_or_quantity"] = len(n(pool, PIPE, r"progress|quantit|productiv|as-built|volume"))
out["G2_pipeline_DT"] = len(n(pool, PIPE, DT))
out["G3_UAV_accuracy"] = len(n(pool, UAV, ACC))
g3 = n(pool, UAV, ACC, TOL); out["G3_UAV_accuracy_and_tolerance_contract_terms"] = len(g3)
out["G3_UAV_accuracy_and_payment_or_contract"] = len(n(pool, UAV, ACC, r"payment|contract|certif|toleran"))
out["G3_titles"] = [r["title"] for r in n(pool, UAV, ACC, r"payment|contract|certif|toleran")]
out["G4_schema_records"] = len(n(pool, SCHEMA)); out["G4_schema_with_commercial_terms"] = len(n(pool, SCHEMA, r"payment|invoic|subcontract|bill of quantit|boq"))
out["G4_schema_linear_commercial"] = len(n(pool, SCHEMA, LIN, r"payment|invoic|subcontract|bill of quantit|boq|quantit"))
out["G4_titles"] = [r["title"] for r in n(pool, SCHEMA, LIN, r"payment|invoic|subcontract|bill of quantit|boq|quantit")]
tr = n(pool, TRACK); out["G5_tracking"] = len(tr)
out["G5_tracking_privacy"] = len(n(tr, PRIV)); out["G5_tracking_linear"] = len(n(tr, LIN)); out["G5_tracking_remote"] = len(n(tr, REMOTE))
out["G5_tracking_pipeline"] = len(n(tr, PIPE))
long = [r for r in tr if any((int(m.group(1)) >= 4 and m.group(2).startswith("week")) or m.group(2).startswith("month") for m in re.finditer(DUR, T(r)))]
out["G5_tracking_duration_ge4weeks_mentioned"] = len(long)
c56 = n(pool, r"productiv|progress|payment|quantit|earned value")
out["G6_C5C6"] = len(c56); out["G6_with_comparative_design"] = len(n(c56, DESIGN))
out["G6_with_commercial_outcome"] = len(n(c56, COUT)); out["G6_comparative_and_commercial"] = len(n(c56, DESIGN, COUT))
out["G6_titles"] = [r["title"] for r in n(c56, DESIGN, COUT)]
# core-set counts from coding
core = {k: v.split("|") for k, v in CODES.items()}
out["core_n"] = len(core)
out["core_pipeline"] = sorted(k for k, f in core.items() if "pipeline" in (f[2] + f[3]).lower())
out["core_linear"] = sorted(k for k, f in core.items() if re.search("linear|pipeline|road|highway|rail", (f[3]).lower()))
out["core_payment_outcome"] = sorted(k for k, f in core.items() if re.search("payment|valuation|billing|certif", (f[7] + f[10]).lower()))
out["core_C1_and_payment"] = sorted(k for k, f in core.items() if "C1" in f[0] and re.search("payment|billing|certif", (f[7] + f[10]).lower()))
out["core_H3_high"] = sorted(k for k, f in core.items() if f[14] == "High")
out["core_H1_high"] = sorted(k for k, f in core.items() if f[12] == "High")
out["core_quant_accuracy"] = sorted(k for k, f in core.items() if re.search(r"\d", f[9]) and "n.r" not in f[9][:4])
json.dump(out, open(os.path.join(HERE, "gap_stats.json"), "w"), indent=1)
for k, v in out.items():
    print(k, v if not isinstance(v, list) else (len(v), v[:25]))
